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
    # Items with planning attributes. `isphantom`/`leadtime`/`safetystocklevel` are item fields.
    ITEMS = """
        SELECT i.itemid AS sku, i.displayname AS name, i.itemtype AS itemtype,
               i.leadtime AS lead_time, i.safetystocklevel AS safety_stock
        FROM item i
        WHERE i.isinactive = 'F'
    """

    # Bill of materials: parent assembly -> component + quantity. Uses Advanced BoM records (§9.2);
    # adjust table/field names (bom, bomrevision, bomrevisioncomponent) to your account.
    BOM_LINES = """
        SELECT b.assembly AS parent_sku, c.item AS component_sku, c.quantity AS qty_per
        FROM bomrevisioncomponent c
        JOIN bomrevision r ON c.bomrevision = r.id
        JOIN bom b ON r.bom = b.id
        WHERE r.iscurrentrevision = 'T'
    """

    # RAW per-vendor sourcing rows (cost + purchase lead time) — the fuel for our sourcing optimizer.
    # itemvendor sublist holds per-vendor purchaseprice; vendor lead time may live on the
    # item/vendor relationship (§9.3 — verify). One row per (item, vendor).
    VENDOR_SOURCING = """
        SELECT iv.item AS sku, v.entityid AS supplier, iv.purchaseprice AS cost,
               iv.leadtime AS lead_time
        FROM itemvendor iv
        JOIN vendor v ON iv.vendor = v.id
    """

    # On-hand by location (§9.3: with Multiple Locations, read the location-level table, not item).
    INVENTORY = """
        SELECT il.item AS sku, BUILTIN.DF(il.location) AS location, il.quantityonhand AS on_hand
        FROM aggregateitemlocation il
        WHERE il.quantityonhand > 0
    """

    # Open purchase orders = scheduled receipts. mainline='F' -> line rows (§9.4).
    OPEN_PO = """
        SELECT tl.item AS sku, tl.quantity AS qty, t.duedate AS due_date
        FROM transaction t
        JOIN transactionline tl ON tl.transaction = t.id
        WHERE t.type = 'PurchOrd' AND t.status IN ('PurchOrd:B','PurchOrd:D','PurchOrd:E')
              AND tl.mainline = 'F'
    """

    # Independent demand = open sales orders (finished goods to deliver).
    OPEN_SO = """
        SELECT t.tranid AS order_id, tl.item AS sku, tl.quantity AS qty,
               t.duedate AS due_date, tl.netamount AS revenue
        FROM transaction t
        JOIN transactionline tl ON tl.transaction = t.id
        WHERE t.type = 'SalesOrd' AND t.status IN ('SalesOrd:B','SalesOrd:D','SalesOrd:E')
              AND tl.mainline = 'F'
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

    # 2) BOM lines
    for row in snap.get("bom_lines", []):
        parent, comp = str(row["parent_sku"]), str(row["component_sku"])
        if parent in items:
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
