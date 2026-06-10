"""Write the plan back to NetSuite: planned work orders + purchase orders, plus an exceptions list.

Transport-agnostic, mirroring the ingestion side: takes an injected `create_record(record_type,
payload) -> dict` callable, so the same code works over the NetSuite REST Record API (production) or
the NetSuite MCP connector (agent). Defaults to DRY-RUN — it builds and returns the payloads without
sending them, so you can review before anything is written to the ERP.

Record types / field names per research §9.2 — VERIFY against your account's REST metadata-catalog
before committing for real. Writing to the ERP is outward-facing and hard to undo; keep dry_run=True
until the payloads have been reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from ..model import MakeBuy, PlanningInput
from ..mrp import MrpResult
from ..scheduler import ScheduleResult

CreateRecordFn = Callable[[str, dict], dict]


@dataclass
class Exception_:
    kind: str          # "late_order" | "expedite" | "shortage"
    ref: str           # order id / sku
    detail: str
    severity: str = "warn"   # "info" | "warn" | "critical"


@dataclass
class WritebackPlan:
    work_orders: list[dict] = field(default_factory=list)      # NetSuite workOrder payloads
    purchase_orders: list[dict] = field(default_factory=list)  # NetSuite purchaseOrder payloads
    exceptions: list[Exception_] = field(default_factory=list)

    def summary(self) -> str:
        crit = sum(1 for e in self.exceptions if e.severity == "critical")
        return (f"{len(self.work_orders)} work order(s), {len(self.purchase_orders)} purchase "
                f"order(s), {len(self.exceptions)} exception(s) ({crit} critical)")


def build_writeback(pin: PlanningInput, sched: ScheduleResult,
                    mrp: MrpResult | None = None) -> WritebackPlan:
    """Turn a solved schedule into NetSuite-shaped payloads + an exceptions list."""
    plan = WritebackPlan()

    # ---- Work orders for MAKE builds ----
    for b in sched.builds:
        plan.work_orders.append({
            "recordType": "workOrder",              # VERIFY internal id
            "assemblyItem": b.sku,                   # item ref
            "quantity": next((d.qty for d in sched.demand_results
                              if d.order_id == b.uid.split("/")[0] and d.sku == b.sku), None),
            "startDate_dayOffset": b.start,          # convert to real date at send time
            "endDate_dayOffset": b.end,
            "memo": f"aps plan: {b.uid} @ {b.station}",
        })

    # ---- Purchase orders for sourcing choices ----
    for s in sched.sourcing:
        plan.purchase_orders.append({
            "recordType": "purchaseOrder",           # VERIFY internal id
            "item": s.sku,
            "vendor": s.supplier,
            "quantity": s.qty,
            "rate": (s.cost // s.qty) if s.qty else s.cost,
            "expectedReceiptDate_dayOffset": s.ready_day,
            "memo": f"aps plan: {s.mode_label} (lead {s.lead_time_days}d)",
        })
        if "air" in s.mode_label.lower() or "prem" in s.mode_label.lower():
            plan.exceptions.append(Exception_(
                "expedite", s.sku,
                f"expedited via {s.mode_label} (+premium) to hold a date — review cost", "warn"))

    # ---- Exceptions: late orders ----
    for d in sched.demand_results:
        if d.tardiness > 0:
            plan.exceptions.append(Exception_(
                "late_order", d.order_id,
                f"{d.qty}x {d.sku} due day {d.due_day} can complete only day {d.completion_day} "
                f"({d.tardiness}d late)", "critical"))

    # ---- Exceptions: MRP shortages (standard lead time misses the date) ----
    if mrp:
        for o in mrp.shortages:
            plan.exceptions.append(Exception_(
                "shortage", o.sku,
                f"need {o.qty} by day {o.receipt_day}; standard lead {o.lead_time_days}d implies "
                f"release day {o.release_day} (past) — expedite or re-source", "critical"))

    return plan


class NetSuiteWriter:
    def __init__(self, create_record: CreateRecordFn | None = None, dry_run: bool = True):
        self.create_record = create_record
        self.dry_run = dry_run

    def commit(self, plan: WritebackPlan) -> dict:
        """Send work orders + purchase orders to NetSuite. DRY-RUN returns payloads unsent."""
        if self.dry_run or self.create_record is None:
            return {"dry_run": True, "work_orders": plan.work_orders,
                    "purchase_orders": plan.purchase_orders,
                    "note": "set dry_run=False and provide create_record to write to NetSuite"}
        created = {"work_orders": [], "purchase_orders": []}
        for wo in plan.work_orders:
            created["work_orders"].append(self.create_record("workOrder", wo))
        for po in plan.purchase_orders:
            created["purchase_orders"].append(self.create_record("purchaseOrder", po))
        return created
