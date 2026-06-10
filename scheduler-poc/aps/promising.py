"""Order promising / rush-quote engine (research §8).

Answers the make-to-order question: "A customer wants N units of X by day D — can I do it, what does it
cost, and what does it displace?" Implements the APS sandbox 'test-plan' pattern:

  1. Solve the committed baseline (existing demand only).
  2. Insert the rush order into a COPY of the plan and re-solve.
  3. Compare: achievable completion day, on-time vs requested date, incremental sourcing/expedite
     cost, and which existing orders get pushed later (displaced).
  4. Give an accept/reject recommendation using an Order-Acceptance-and-Scheduling profit test
     (§8.4): profit = revenue - rush tardiness penalty - incremental cost - displacement penalties.

This reuses the same finite-capacity + cost-aware-sourcing scheduler, so a quote automatically
accounts for build times, material lead times, and the option to expedite.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field

from .model import DemandLine, PlanningInput
from .scheduler import ScheduleResult, schedule


@dataclass
class Displacement:
    order_id: str
    sku: str
    baseline_completion: int
    new_completion: int

    @property
    def days_later(self) -> int:
        return self.new_completion - self.baseline_completion


@dataclass
class Quote:
    rush_order_id: str
    sku: str
    qty: int
    requested_day: int
    achievable_day: int
    on_time: bool
    tardiness: int
    incremental_cost: int                 # expedite/freight premium vs baseline
    expedited_parts: list[str] = field(default_factory=list)
    displacements: list[Displacement] = field(default_factory=list)
    # accept/reject economics
    revenue: int = 0
    rush_penalty: int = 0
    displacement_penalty: int = 0
    profit: int = 0
    recommend_accept: bool = False
    feasible: bool = True

    def summary(self) -> str:
        verdict = "ON TIME" if self.on_time else f"LATE by {self.tardiness}d (earliest day {self.achievable_day})"
        rec = "ACCEPT" if self.recommend_accept else "DECLINE"
        lines = [
            f"Quote for {self.rush_order_id}: {self.qty}x {self.sku}, requested day {self.requested_day}",
            f"  feasibility : {verdict}",
            f"  expedite    : {', '.join(self.expedited_parts) if self.expedited_parts else 'none'}"
            f"  (+${self.incremental_cost:,})",
        ]
        if self.displacements:
            lines.append("  displaces   :")
            for d in self.displacements:
                lines.append(f"      {d.order_id} ({d.sku}) slips {d.days_later}d "
                             f"({d.baseline_completion} -> {d.new_completion})")
        else:
            lines.append("  displaces   : nothing")
        lines += [
            f"  economics   : revenue ${self.revenue:,} - rush penalty ${self.rush_penalty:,} "
            f"- displacement ${self.displacement_penalty:,} - expedite ${self.incremental_cost:,}",
            f"                = profit ${self.profit:,}",
            f"  RECOMMENDATION: {rec}",
        ]
        return "\n".join(lines)


def _completions(res: ScheduleResult) -> dict[str, int]:
    return {d.order_id: d.completion_day for d in res.demand_results}


def quote_rush_order(pin: PlanningInput, rush: DemandLine,
                     baseline: ScheduleResult | None = None,
                     time_limit_s: float = 15.0) -> Quote:
    """Produce a promise/accept-reject quote for a rush order against the committed plan."""
    baseline = baseline or schedule(pin, time_limit_s)
    base_completions = _completions(baseline)

    pin2 = copy.deepcopy(pin)
    pin2.demand.append(rush)
    with_rush = schedule(pin2, time_limit_s)

    q = Quote(rush_order_id=rush.order_id or rush.sku, sku=rush.sku, qty=rush.qty,
              requested_day=rush.due_day, achievable_day=rush.due_day, on_time=True,
              tardiness=0, incremental_cost=0, revenue=rush.revenue)

    if not with_rush.feasible:
        q.feasible = False
        q.recommend_accept = False
        return q

    # Rush order outcome
    rush_res = next((d for d in with_rush.demand_results
                     if d.order_id == (rush.order_id or rush.sku)), None)
    if rush_res:
        q.achievable_day = rush_res.completion_day
        q.tardiness = rush_res.tardiness
        q.on_time = rush_res.tardiness == 0

    # Incremental cost (expedite premium) and which parts got expedited
    q.incremental_cost = max(with_rush.total_cost - baseline.total_cost, 0)
    base_modes = {s.uid: s.mode_label for s in baseline.sourcing}
    for s in with_rush.sourcing:
        if "air" in s.mode_label.lower() or "prem" in s.mode_label.lower():
            if base_modes.get(s.uid) != s.mode_label:
                q.expedited_parts.append(f"{s.sku}:{s.mode_label}")

    # Displacement of existing committed orders
    for oid, new_c in _completions(with_rush).items():
        if oid == (rush.order_id or rush.sku):
            continue
        base_c = base_completions.get(oid)
        if base_c is not None and new_c > base_c:
            sku = next((d.sku for d in with_rush.demand_results if d.order_id == oid), "?")
            q.displacements.append(Displacement(oid, sku, base_c, new_c))

    # ---- OAS profit test (§8.4) ----
    q.rush_penalty = q.tardiness * rush.tardiness_penalty_per_day
    # displacement penalty = each displaced order's own per-day penalty x days slipped
    pen_by_order = {d.order_id: d.tardiness_penalty_per_day for d in pin.demand}
    q.displacement_penalty = sum(
        d.days_later * pen_by_order.get(d.order_id, 0) for d in q.displacements
    )
    q.profit = q.revenue - q.rush_penalty - q.displacement_penalty - q.incremental_cost
    q.recommend_accept = q.profit > 0
    return q
