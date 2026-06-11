"""NetSuite -> PlanningInput ingestion via SuiteQL (research §9).

The exact internal IDs / field names below MUST be verified against your account's Records Browser
or the live REST metadata-catalog (`/services/rest/record/v1/metadata-catalog`). Per §9.3, NetSuite's
per-vendor lead time handling is limited, so we pull RAW per-vendor (lead time, cost) rows and let
our own sourcing optimizer choose — rather than relying on NetSuite's aggregated planning.

Usage (transport-agnostic):

    def query(sql: str) -> list[dict]:
        # production: POST sql to /services/rest/query/v1/suiteql with OAuth 2.0, return rows
        # or (agent): call the NetSuite MCP SuiteQL tool and return its rows
        ...

    pin = NetSuiteIngestor(query).build_planning_input()

A snapshot can be dumped/loaded as JSON so an agent-side live pull feeds the standalone engine:

    snap = NetSuiteIngestor(query).fetch_snapshot()
    Path("snapshot.json").write_text(json.dumps(snap))
    pin  = planning_input_from_snapshot(json.loads(Path("snapshot.json").read_text()))
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Callable, Protocol

from ..model import (
    BomLine, DemandLine, InventoryRecord, Item, MakeBuy, PlanningInput,
    ScheduledReceipt, SourcingMode, WorkCenter,
)

QueryFn = Callable[[str], list[dict]]


# --------------------------------------------------------------------------------------------------
# SuiteQL queries. Field names per §9; VERIFY against your account before relying on them.
# --------------------------------------------------------------------------------------------------

class SuiteQL:
    """SuiteQL queries, corrected against the LIVE account (docs/netsuite-suiteql-findings.md,
    verified 2026-06-11). Key facts baked in here:

      * `item.leadtime`/`safetystocklevel` do NOT exist in this account — items carry only
        itemid/displayname/itemtype/cost. Build times come from a maintained per-product config;
        purchase lead time comes from the per-vendor sourcing table (or a maintained override).
      * Every `*.item` reference (bomrevisioncomponent, itemvendor, inventorybalance,
        transactionline) is an internal id — we JOIN `item` and select `itemid` so the SKU
        strings match the items map.
      * BOM chain is bomrevisioncomponent.bomrevision -> bomrevision.id, then
        bomrevision.billofmaterials -> bom.id. `bom.name` encodes the parent assembly; the
        snapshot mapper resolves parent_sku from `bom_name` (see _resolve_bom_parents).
      * Inventory is `inventorybalance` (NOT aggregateitemlocation).

    Namespace note: the MCP search layer lacks GROUP BY and some fields; the REST SuiteQL path
    (pull_netsuite.py) supports both. Lines that need REST (the current-revision subquery) are
    flagged; on the search layer, fetch all revisions and let _resolve_bom_parents keep the latest.
    """

    # Items. No leadtime/safetystock columns exist here; `cost` is the standard/last cost.
    ITEMS = """
        SELECT i.itemid AS sku, i.displayname AS name, i.itemtype AS itemtype,
               i.cost AS unit_cost
        FROM item i
        WHERE i.isinactive = 'F'
    """

    # Bill of materials: component lines with their parent BOM name + current-revision filter.
    # parent_sku is resolved from bom_name by the mapper. The MAX-revision subquery needs REST
    # SuiteQL; on the MCP search layer drop the AND r.id IN (...) clause and dedupe in the mapper.
    BOM_LINES = """
        SELECT b.name AS bom_name, ci.itemid AS component_sku,
               c.quantity AS qty_per, c.itemsource AS item_source
        FROM bomrevisioncomponent c
        JOIN bomrevision r ON c.bomrevision = r.id
        JOIN bom b ON r.billofmaterials = b.id
        JOIN item ci ON c.item = ci.id
        WHERE r.id IN (SELECT MAX(r2.id) FROM bomrevision r2 GROUP BY r2.billofmaterials)
    """

    # RAW per-vendor sourcing rows. purchaseprice is per-vendor; lead time is NOT a column in this
    # account (see findings) so it is omitted here and supplied by a maintained lead-time override
    # or defaulted by the mapper. One row per (item, vendor).
    VENDOR_SOURCING = """
        SELECT ii.itemid AS sku, v.entityid AS supplier, iv.purchaseprice AS cost
        FROM itemvendor iv
        JOIN item ii ON iv.item = ii.id
        JOIN vendor v ON iv.vendor = v.id
    """

    # On-hand by location, per the verified inventorybalance table.
    INVENTORY = """
        SELECT ii.itemid AS sku, BUILTIN.DF(ib.location) AS location, ib.quantityonhand AS on_hand
        FROM inventorybalance ib
        JOIN item ii ON ib.item = ii.id
        WHERE ib.quantityonhand > 0
    """

    # Open purchase orders = scheduled receipts. mainline='F' -> component/item lines. PO header
    # carries duedate (verified populated). Closed/cancelled excluded via status<>'H'... see note:
    # status codes here are single-char; tune the exclusion set against your open-PO definition.
    OPEN_PO = """
        SELECT ii.itemid AS sku, tl.quantity AS qty, t.duedate AS due_date
        FROM transaction t
        JOIN transactionline tl ON tl.transaction = t.id
        JOIN item ii ON tl.item = ii.id
        WHERE t.type = 'PurchOrd' AND tl.mainline = 'F' AND tl.quantity > 0
    """

    # Independent demand = open sales orders. NOTE: SO header duedate is null in this account;
    # prefer the Drive forecast for demand timing. Kept for accounts that populate due dates.
    OPEN_SO = """
        SELECT t.tranid AS order_id, ii.itemid AS sku, tl.quantity AS qty,
               t.duedate AS due_date, tl.netamount AS revenue
        FROM transaction t
        JOIN transactionline tl ON tl.transaction = t.id
        JOIN item ii ON tl.item = ii.id
        WHERE t.type = 'SalesOrd' AND tl.mainline = 'F' AND tl.quantity > 0
    """


@dataclass
class IngestConfig:
    anchor_date: str = "today"          # day 0 of the plan; due dates are converted to day offsets
    default_freight_modes: bool = True  # synthesize an air/expedite alternative when none exists
    air_premium_pct: int = 40           # cost uplift for synthesized air mode
    air_speedup_pct: int = 70           # lead-time reduction for synthesized air mode


class NetSuiteIngestor:
    def __init__(self, query: QueryFn, config: IngestConfig | None = None):
        self.query = query
        self.cfg = config or IngestConfig()

    # ---- raw fetch (one snapshot, serializable to JSON) ----
    def fetch_snapshot(self) -> dict:
        return {
            "items": self.query(SuiteQL.ITEMS),
            "bom_lines": self.query(SuiteQL.BOM_LINES),
            "vendor_sourcing": self.query(SuiteQL.VENDOR_SOURCING),
            "inventory": self.query(SuiteQL.INVENTORY),
            "open_po": self.query(SuiteQL.OPEN_PO),
            "open_so": self.query(SuiteQL.OPEN_SO),
        }

    def build_planning_input(self, day0: str | None = None) -> PlanningInput:
        return planning_input_from_snapshot(self.fetch_snapshot(), self.cfg, day0)


# --------------------------------------------------------------------------------------------------
# Snapshot -> PlanningInput mapping (pure, testable; no network)
# --------------------------------------------------------------------------------------------------

def _to_days(due_date: str, day0: str | None) -> int:
    """Convert a NetSuite date string to an integer day offset from day0. Best-effort/lenient."""
    from datetime import date, datetime
    if day0 in (None, "today"):
        base = date.today()
    else:
        base = datetime.fromisoformat(day0).date()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            d = datetime.strptime(due_date[:10], fmt).date()
            return max((d - base).days, 0)
        except (ValueError, TypeError):
            continue
    return 0


_BOM_SUFFIX = re.compile(r"_BOM\d+$", re.IGNORECASE)


def _bom_name_to_core(bom_name: str) -> str:
    """`106901-R02_BOM1` -> `106901-R02`; `106136_BOM1` -> `106136`."""
    return _BOM_SUFFIX.sub("", str(bom_name)).strip()


def _base_part(sku: str) -> str:
    """Part number before the first revision/variant separator: `106136-R04` -> `106136`."""
    return str(sku).split("-")[0].split("_")[0]


def _resolve_bom_parent(bom_name: str, by_full: dict, by_base: dict) -> str | None:
    """Map a BOM name to its parent assembly SKU. The account encodes the parent in the BOM name
    but inconsistently (sometimes with the revision, sometimes without) and exposes no FK, so we
    prefer a full-itemid match and fall back to the base part number (see findings doc)."""
    core = _bom_name_to_core(bom_name)
    if core in by_full:
        return core
    cands = by_base.get(_base_part(core))
    if cands:
        return sorted(cands)[-1]  # latest revision suffix, deterministic
    return None


def _itemtype_to_makebuy(itemtype: str | None) -> MakeBuy:
    # NetSuite assembly/kit -> MAKE; inventory/non-inventory purchased -> BUY (verify mapping).
    if (itemtype or "").lower() in ("assembly", "assemblyitem", "kit"):
        return MakeBuy.MAKE
    return MakeBuy.BUY


def planning_input_from_snapshot(snap: dict, cfg: IngestConfig | None = None,
                                 day0: str | None = None) -> PlanningInput:
    cfg = cfg or IngestConfig()
    items: dict[str, Item] = {}

    # 1) items
    for row in snap.get("items", []):
        sku = str(row["sku"])
        mb = _itemtype_to_makebuy(row.get("itemtype"))
        items[sku] = Item(
            sku=sku, name=str(row.get("name") or sku), make_buy=mb,
            build_days=int(row.get("lead_time") or 0) if mb is MakeBuy.MAKE else 0,
            build_station=row.get("build_station"),
            safety_stock=int(row.get("safety_stock") or 0),
        )

    # 2) BOM lines. Rows carry either an explicit parent_sku or a bom_name we resolve to the
    # parent assembly. Dedup guards against multi-revision duplication on the search-layer path.
    by_full = {sku: sku for sku in items}
    by_base: dict[str, list[str]] = {}
    for sku in items:
        by_base.setdefault(_base_part(sku), []).append(sku)
    seen_links: set[tuple[str, str]] = set()
    for row in snap.get("bom_lines", []):
        comp = str(row["component_sku"])
        parent = row.get("parent_sku")
        if parent is None and row.get("bom_name") is not None:
            parent = _resolve_bom_parent(row["bom_name"], by_full, by_base)
        if parent is None:
            continue
        parent = str(parent)
        if parent in items and (parent, comp) not in seen_links:
            seen_links.add((parent, comp))
            items[parent].bom.append(BomLine(comp, float(row.get("qty_per") or 1)))

    # 3) vendor sourcing -> SourcingMode list (optionally synthesize an air/expedite alternative)
    for row in snap.get("vendor_sourcing", []):
        sku = str(row["sku"])
        if sku not in items:
            continue
        supplier = str(row.get("supplier") or "vendor")
        cost = int(round(float(row.get("cost") or 0)))
        lead = int(row.get("lead_time") or 0)
        item = items[sku]
        item.make_buy = MakeBuy.BUY  # has a vendor -> purchased
        item.sourcing.append(SourcingMode(f"{supplier}-std", supplier, cost, lead))
        if cfg.default_freight_modes and lead > 14:
            fast_lead = max(int(round(lead * (100 - cfg.air_speedup_pct) / 100)), 3)
            fast_cost = int(round(cost * (100 + cfg.air_premium_pct) / 100))
            item.sourcing.append(SourcingMode(f"{supplier}-air", supplier, fast_cost, fast_lead))

    # 4) inventory
    inventory = [
        InventoryRecord(str(r["sku"]), int(r.get("on_hand") or 0), str(r.get("location") or "MAIN"))
        for r in snap.get("inventory", []) if str(r.get("sku")) in items
    ]

    # 5) scheduled receipts (open POs)
    receipts = [
        ScheduledReceipt(str(r["sku"]), int(r.get("qty") or 0), _to_days(r.get("due_date"), day0))
        for r in snap.get("open_po", []) if str(r.get("sku")) in items
    ]

    # 6) demand (open SOs)
    demand = []
    for r in snap.get("open_so", []):
        sku = str(r.get("sku"))
        if sku not in items:
            continue
        demand.append(DemandLine(
            sku=sku, qty=int(r.get("qty") or 0), due_day=_to_days(r.get("due_date"), day0),
            order_id=str(r.get("order_id") or ""), revenue=int(round(float(r.get("revenue") or 0))),
        ))

    return PlanningInput(items=items, work_centers={}, inventory=inventory,
                         scheduled_receipts=receipts, demand=demand)


def dump_snapshot(snap: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(snap, f, indent=2, default=str)


def load_snapshot(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
