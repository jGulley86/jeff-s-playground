"""Material Requirements Planning: BOM explosion + gross-to-net + lead-time offsetting.

This is the deterministic planning core (research §4). It turns independent demand for finished
goods into time-phased planned orders for every make/buy item below them, netting against on-hand
inventory, scheduled receipts, and safety stock, and offsetting each planned order's release date by
that item's lead time (build_days for MAKE items, sourcing lead time for BUY items).

Algorithm (classic low-level-code MRP):
  1. Compute each item's low-level code (deepest position in any BOM).
  2. Process items shallow->deep. For each item:
       a. aggregate gross requirements by day,
       b. net against projected on-hand (on-hand + receipts - safety stock) walking time forward,
       c. emit planned order RECEIPTS where projected balance would dip below safety stock
          (lot-sized),
       d. offset each receipt back by lead time to get the planned order RELEASE,
       e. for MAKE items, explode each release into child gross requirements at the release day
          (children must be on hand when the build starts).
  3. A release day < 0 means standard lead times can't meet the due date -> flagged as a shortage
     (the signal that triggers expediting / the sourcing optimizer in scheduler.py).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from math import ceil

from .model import Item, MakeBuy, PlanningInput


@dataclass(frozen=True)
class PlannedOrder:
    sku: str
    qty: int
    release_day: int       # when to release (order/start). May be < 0 => infeasible w/ std lead time
    receipt_day: int       # when it must be available (= the need date)
    kind: MakeBuy
    lead_time_days: int
    late_release: bool = False   # True if release_day < 0 (standard lead time misses the due date)


@dataclass
class MrpResult:
    planned_orders: list[PlannedOrder] = field(default_factory=list)
    # per-item gross requirements after explosion, for reporting/debug: sku -> [(day, qty), ...]
    gross_requirements: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    shortages: list[PlannedOrder] = field(default_factory=list)   # orders with late_release

    def orders_for(self, sku: str) -> list[PlannedOrder]:
        return [o for o in self.planned_orders if o.sku == sku]


def low_level_codes(items: dict[str, Item]) -> dict[str, int]:
    """Deepest depth at which each sku appears in any BOM (0 = only ever a top-level/finished good)."""
    codes: dict[str, int] = {sku: 0 for sku in items}

    def visit(sku: str, depth: int, seen: frozenset[str]) -> None:
        if sku in seen:
            raise ValueError(f"BOM cycle detected at {sku}")
        codes[sku] = max(codes.get(sku, 0), depth)
        item = items.get(sku)
        if item and item.make_buy is MakeBuy.MAKE:
            for line in item.bom:
                visit(line.component, depth + 1, seen | {sku})

    for sku, item in items.items():
        if item.make_buy is MakeBuy.MAKE:
            for line in item.bom:
                visit(line.component, 1, frozenset({sku}))
    return codes


def _lot_size(qty: int, multiple: int) -> int:
    if multiple <= 1:
        return qty
    return ceil(qty / multiple) * multiple


def run_mrp(pin: PlanningInput) -> MrpResult:
    result = MrpResult()
    codes = low_level_codes(pin.items)

    # Gross requirements accumulate as we explode parents. Seed with independent demand.
    gross: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for d in pin.demand:
        gross[d.sku][d.due_day] += d.qty

    # Process items shallow -> deep so a parent's planned releases are exploded before we net a child.
    for sku in sorted(pin.items, key=lambda s: codes.get(s, 0)):
        item = pin.items[sku]
        reqs = gross.get(sku, {})
        if not reqs:
            continue

        result.gross_requirements[sku] = sorted(reqs.items())
        lead = item.default_lead_time()

        # ---- gross-to-net, walking time forward ----
        # Build a day-ordered event timeline: receipts add supply, requirements consume it.
        receipts_by_day: dict[int, int] = defaultdict(int)
        for r in pin.receipts_for(sku):
            receipts_by_day[r.due_day] += r.qty

        available = pin.on_hand(sku)
        ss = item.safety_stock
        days = sorted(set(reqs) | set(receipts_by_day))

        for day in days:
            available += receipts_by_day.get(day, 0)
            demand_today = reqs.get(day, 0)
            available -= demand_today
            if available < ss:
                shortfall = ss - available
                order_qty = _lot_size(shortfall, item.lot_size)
                release_day = day - lead
                po = PlannedOrder(
                    sku=sku,
                    qty=order_qty,
                    release_day=release_day,
                    receipt_day=day,
                    kind=item.make_buy,
                    lead_time_days=lead,
                    late_release=release_day < 0,
                )
                result.planned_orders.append(po)
                if po.late_release:
                    result.shortages.append(po)
                available += order_qty

                # Explode a MAKE order into child demand at the RELEASE day (build-start).
                if item.make_buy is MakeBuy.MAKE:
                    for line in item.bom:
                        child_qty = int(ceil(order_qty * line.qty_per))
                        gross[line.component][max(release_day, 0)] += child_qty

    return result
