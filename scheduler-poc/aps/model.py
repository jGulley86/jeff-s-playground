"""Core domain model for the integrated production scheduler.

These dataclasses are the single source of truth that every layer speaks:
  * connectors/ populate them from NetSuite + Google Drive,
  * mrp.py consumes them to compute time-phased material requirements,
  * scheduler.py turns planned work into a finite-capacity schedule,
  * promising.py answers rush-order quotes.

Design notes (see ../../docs/production-scheduler-research.md):
  * Time is integer DAYS. Day 0 = the planning anchor ("today").
  * Money is integer dollars (keeps CP-SAT in integer arithmetic).
  * BUILD TIME is modeled as a fixed per-product duration (`Item.build_days`) per the project
    decision — the production lead time once all materials are on hand. Finer operation-level
    routings can be layered in later without changing callers.
  * SOURCING is a menu of modes per purchased item (supplier x freight), each with its own cost and
    lead time — this is the "lead time is a decision variable" idea (research §7.1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class MakeBuy(str, Enum):
    MAKE = "make"   # produced in-house (has a build_days + BOM)
    BUY = "buy"     # purchased (has sourcing modes / lead time)


@dataclass(frozen=True)
class SourcingMode:
    """One way to buy one purchased item: a (supplier, freight) option.

    cost_per_unit INCLUDES any freight/expedite premium so the optimizer compares true landed cost.
    """
    label: str             # e.g. "VendorA-ocean", "VendorA-air"
    supplier: str          # vendor name / NetSuite vendor id
    cost_per_unit: int     # landed $/unit incl. freight
    lead_time_days: int    # order -> on-hand
    max_qty: int = 10**9   # supplier capacity ceiling for this mode (units)
    moq: int = 0           # minimum order quantity
    lead_time_stdev: float = 0.0  # day-to-day variability, for safety-stock math (iter 5)


@dataclass(frozen=True)
class BomLine:
    """One component of a parent item's bill of materials."""
    component: str   # child Item.sku
    qty_per: float   # quantity of component per 1 unit of parent


@dataclass(frozen=True)
class Operation:
    """One routing step of a MAKE item (iteration 6).

    Duration of the operation for an order of size `qty` = setup_days + ceil(run_days_per_unit*qty).
    setup is incurred once per order; run scales with quantity (research §2).
    """
    name: str
    work_center: str
    setup_days: int = 0
    run_days_per_unit: float = 0.0

    def duration(self, qty: int) -> int:
        from math import ceil
        return self.setup_days + ceil(self.run_days_per_unit * max(qty, 1))


@dataclass
class Item:
    """A part: either MAKE (built in-house) or BUY (purchased)."""
    sku: str
    name: str
    make_buy: MakeBuy

    # --- MAKE attributes ---
    build_days: int = 0                       # fixed build duration (fallback when no routing)
    build_station: str | None = None          # station used when no routing is defined
    bom: list[BomLine] = field(default_factory=list)
    routing: list[Operation] = field(default_factory=list)  # operation-level routing (iter 6)

    # --- BUY attributes ---
    sourcing: list[SourcingMode] = field(default_factory=list)

    # --- planning parameters (apply to both) ---
    safety_stock: int = 0
    lot_size: int = 1                          # round planned orders up to a multiple of this
    demand_stdev: float = 0.0                  # for safety-stock math (iter 5)

    def default_mode(self) -> SourcingMode | None:
        """The preferred (standard) sourcing mode = lowest landed cost. None for MAKE items."""
        if self.make_buy is MakeBuy.BUY and self.sourcing:
            return min(self.sourcing, key=lambda m: m.cost_per_unit)
        return None

    def default_lead_time(self) -> int:
        """Lead time used by plain MRP: the preferred (cheapest) sourcing mode, or build time.

        Using the cheapest (not fastest) mode means MRP plans realistically and surfaces genuine
        shortages, which the scheduler's sourcing optimizer then resolves by expediting (research §7).
        """
        mode = self.default_mode()
        if mode:
            return mode.lead_time_days
        return self.nominal_build_days()

    def nominal_build_days(self, qty: int = 1) -> int:
        """Build lead time for MRP: sum of routing op durations if routed, else build_days."""
        if self.routing:
            return sum(op.duration(qty) for op in self.routing)
        return self.build_days


@dataclass(frozen=True)
class WorkCenter:
    """A finite-capacity build station. capacity = number of parallel builds (1 = single line)."""
    name: str
    capacity: int = 1


@dataclass(frozen=True)
class InventoryRecord:
    """On-hand position for an item (optionally per location)."""
    sku: str
    on_hand: int
    location: str = "MAIN"


@dataclass(frozen=True)
class ScheduledReceipt:
    """An open PO / work order already in flight: supply arriving on a known day."""
    sku: str
    qty: int
    due_day: int


@dataclass(frozen=True)
class DemandLine:
    """Independent demand for a finished good: a customer order or forecast bucket."""
    sku: str
    qty: int
    due_day: int
    order_id: str = ""
    revenue: int = 0
    tardiness_penalty_per_day: int = 0   # $/day late; also encodes lateness/goodwill cost


@dataclass
class PlanningInput:
    """The complete bundle of master + transactional data the engine plans against."""
    items: dict[str, Item] = field(default_factory=dict)
    work_centers: dict[str, WorkCenter] = field(default_factory=dict)
    inventory: list[InventoryRecord] = field(default_factory=list)
    scheduled_receipts: list[ScheduledReceipt] = field(default_factory=list)
    demand: list[DemandLine] = field(default_factory=list)
    horizon_days: int = 365

    # ---- convenience accessors ----
    def on_hand(self, sku: str) -> int:
        return sum(r.on_hand for r in self.inventory if r.sku == sku)

    def receipts_for(self, sku: str) -> list[ScheduledReceipt]:
        return sorted((r for r in self.scheduled_receipts if r.sku == sku), key=lambda r: r.due_day)

    def item(self, sku: str) -> Item:
        return self.items[sku]
