"""Finite-capacity production scheduler with cost-aware sourcing (iteration 2).

Where mrp.py gives the time-phased *purchasing* view, this module gives the *execution* view: it
explodes each demand line into a tree of production tasks (build tasks for MAKE items, procurement
tasks for BUY items), nets against on-hand inventory, then uses OR-Tools CP-SAT to:

  * schedule build tasks on finite-capacity stations (NoOverlap / Cumulative),
  * respect BOM precedence (a parent build can't start until its children are done),
  * CHOOSE a sourcing mode per purchased part (supplier x freight) — the "lead time is a decision
    variable" pattern (research §7.7) — so the model expedites only when it has to,
  * gate each build's start on its materials being available.

Objective is LEXICOGRAPHIC, on-time first (per the project decision):
    Phase A: minimize total tardiness of finished-good demand.
    Phase B: holding tardiness at its best value, minimize total sourcing/expedite cost.

So the schedule hits customer dates whenever physically possible, and among all on-time plans picks
the cheapest sourcing — and when a date is physically impossible, it gets as close as it can and the
result reports the unavoidable tardiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil

from ortools.sat.python import cp_model

from .model import Item, MakeBuy, PlanningInput, SourcingMode


# --------------------------------------------------------------------------------------------------
# Task graph (built from demand by explosion + netting)
# --------------------------------------------------------------------------------------------------

@dataclass
class Task:
    uid: str                 # unique id, e.g. "SO-1001/SLIPBOT-V3"
    sku: str
    qty: int
    kind: MakeBuy
    children: list[str] = field(default_factory=list)   # uids of prerequisite tasks
    station: str | None = None                          # MAKE only
    build_days: int = 0                                 # MAKE only
    modes: list[SourcingMode] = field(default_factory=list)  # BUY only
    # demand linkage (finished-good tasks only):
    due_day: int | None = None
    tardiness_penalty_per_day: int = 0
    order_id: str = ""


def expand_demand(pin: PlanningInput) -> dict[str, Task]:
    """Explode every demand line into a task tree, netting against on-hand inventory.

    Returns {uid: Task}. One build/procurement task per (item, demand-line) — build time is a fixed
    per-product duration, so quantity scales cost/material but not the number of build tasks.
    """
    tasks: dict[str, Task] = {}
    available = {r.sku: pin.on_hand(r.sku) for r in pin.inventory}
    for sku in pin.items:
        available.setdefault(sku, 0)

    def consume(sku: str, qty: int) -> int:
        """Take as much as possible from on-hand; return the remaining NET quantity to produce/buy."""
        take = min(available.get(sku, 0), qty)
        available[sku] = available.get(sku, 0) - take
        return qty - take

    def explode(order_id: str, sku: str, qty: int) -> str | None:
        """Create a task for (sku, qty) and its subtree. Returns the task uid, or None if covered."""
        net = consume(sku, qty)
        if net <= 0:
            return None  # fully covered by inventory -> available immediately, no task needed
        item = pin.items[sku]
        uid = f"{order_id}/{sku}"
        # If the same (order, sku) appears twice, merge quantities.
        if uid in tasks:
            tasks[uid].qty += net
            return uid

        if item.make_buy is MakeBuy.MAKE:
            task = Task(uid=uid, sku=sku, qty=net, kind=MakeBuy.MAKE,
                        station=item.build_station, build_days=item.build_days)
            tasks[uid] = task
            for line in item.bom:
                child_uid = explode(order_id, line.component, int(ceil(net * line.qty_per)))
                if child_uid:
                    task.children.append(child_uid)
        else:
            task = Task(uid=uid, sku=sku, qty=net, kind=MakeBuy.BUY, modes=list(item.sourcing))
            tasks[uid] = task
        return uid

    # Process demand earliest-due first so scarce inventory is allocated to the most urgent orders.
    for d in sorted(pin.demand, key=lambda d: d.due_day):
        root = explode(d.order_id or d.sku, d.sku, d.qty)
        if root:
            tasks[root].due_day = d.due_day
            tasks[root].tardiness_penalty_per_day = d.tardiness_penalty_per_day
            tasks[root].order_id = d.order_id
    return tasks


# --------------------------------------------------------------------------------------------------
# CP-SAT scheduling
# --------------------------------------------------------------------------------------------------

@dataclass
class SourcingChoice:
    uid: str
    sku: str
    qty: int
    mode_label: str
    supplier: str
    lead_time_days: int
    cost: int
    ready_day: int


@dataclass
class BuildSlot:
    uid: str
    sku: str
    station: str
    start: int
    end: int


@dataclass
class DemandResult:
    order_id: str
    sku: str
    qty: int
    due_day: int
    completion_day: int
    tardiness: int


@dataclass
class ScheduleResult:
    status: str
    total_tardiness: int
    total_cost: int
    demand_results: list[DemandResult] = field(default_factory=list)
    sourcing: list[SourcingChoice] = field(default_factory=list)
    builds: list[BuildSlot] = field(default_factory=list)
    feasible: bool = True


def _build_model(pin: PlanningInput, tasks: dict[str, Task]):
    model = cp_model.CpModel()
    H = pin.horizon_days

    start = {}      # uid -> start var
    end = {}        # uid -> end var
    presences = {}  # uid -> [presence literals] for BUY tasks
    cost_terms = []
    station_intervals: dict[str, list] = {wc: [] for wc in pin.work_centers}
    station_demands: dict[str, list[int]] = {wc: [] for wc in pin.work_centers}

    # Pass 1: create start/end vars for every task (so precedence can reference any child).
    for uid in tasks:
        start[uid] = model.new_int_var(0, H, f"s_{uid}")
        end[uid] = model.new_int_var(0, H, f"e_{uid}")

    # Pass 2: add per-task constraints (sourcing choice, build intervals, precedence).
    for uid, t in tasks.items():
        s, e = start[uid], end[uid]

        if t.kind is MakeBuy.BUY:
            # Choose exactly one sourcing mode; end = start + chosen lead time; add its landed cost.
            lits = []
            lead_terms = []
            for i, m in enumerate(t.modes):
                p = model.new_bool_var(f"p_{uid}_{m.label}")
                lits.append(p)
                if t.qty > m.max_qty:
                    model.add(p == 0)               # supplier can't supply this quantity
                order_qty = max(t.qty, m.moq)
                cost_terms.append(p * (order_qty * m.cost_per_unit))
                lead_terms.append(p * m.lead_time_days)
            model.add_exactly_one(lits)
            presences[uid] = lits
            model.add(e == s + sum(lead_terms))
        else:
            # MAKE: fixed-duration build on a finite-capacity station.
            iv = model.new_interval_var(s, t.build_days, e, f"iv_{uid}")
            if t.station in station_intervals:
                station_intervals[t.station].append(iv)
                station_demands[t.station].append(1)
            # Precedence: can't start until every child task is complete.
            for c in t.children:
                model.add(s >= end[c])

    # Finite capacity per build station.
    for wc_name, wc in pin.work_centers.items():
        ivs = station_intervals[wc_name]
        if not ivs:
            continue
        if wc.capacity == 1:
            model.add_no_overlap(ivs)
        else:
            model.add_cumulative(ivs, station_demands[wc_name], wc.capacity)

    # Tardiness on finished-good (demand) tasks.
    tardiness_terms = []
    tardiness_vars = {}
    for uid, t in tasks.items():
        if t.due_day is not None:
            tard = model.new_int_var(0, H, f"tard_{uid}")
            model.add_max_equality(tard, [end[uid] - t.due_day, 0])
            tardiness_vars[uid] = tard
            tardiness_terms.append(tard)

    return model, start, end, presences, cost_terms, tardiness_terms, tardiness_vars


def schedule(pin: PlanningInput, time_limit_s: float = 15.0) -> ScheduleResult:
    tasks = expand_demand(pin)
    model, start, end, presences, cost_terms, tardiness_terms, tardiness_vars = _build_model(pin, tasks)

    total_tardiness = model.new_int_var(0, pin.horizon_days * max(len(tardiness_terms), 1), "total_tard")
    model.add(total_tardiness == (sum(tardiness_terms) if tardiness_terms else 0))
    total_cost = model.new_int_var(0, 10**9, "total_cost")
    model.add(total_cost == (sum(cost_terms) if cost_terms else 0))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s / 2

    # ---- Phase A: minimize tardiness (on-time first) ----
    model.minimize(total_tardiness)
    st = solver.solve(model)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return ScheduleResult(status=solver.status_name(st), total_tardiness=-1,
                              total_cost=-1, feasible=False)
    best_tardiness = int(solver.value(total_tardiness))

    # ---- Phase B: hold tardiness at best, minimize cost ----
    model.add(total_tardiness <= best_tardiness)
    model.minimize(total_cost)
    solver2 = cp_model.CpSolver()
    solver2.parameters.max_time_in_seconds = time_limit_s / 2
    st2 = solver2.solve(model)
    sol = solver2 if st2 in (cp_model.OPTIMAL, cp_model.FEASIBLE) else solver
    status_name = solver2.status_name(st2) if st2 in (cp_model.OPTIMAL, cp_model.FEASIBLE) \
        else solver.status_name(st)

    return _extract(pin, tasks, sol, start, end, presences, tardiness_vars, status_name)


def _extract(pin, tasks, sol, start, end, presences, tardiness_vars, status_name) -> ScheduleResult:
    res = ScheduleResult(status=status_name, total_tardiness=0, total_cost=0)
    for uid, t in tasks.items():
        if t.kind is MakeBuy.BUY:
            for i, m in enumerate(t.modes):
                if sol.value(presences[uid][i]) == 1:
                    order_qty = max(t.qty, m.moq)
                    cost = order_qty * m.cost_per_unit
                    res.total_cost += cost
                    res.sourcing.append(SourcingChoice(
                        uid=uid, sku=t.sku, qty=t.qty, mode_label=m.label, supplier=m.supplier,
                        lead_time_days=m.lead_time_days, cost=cost, ready_day=int(sol.value(end[uid])),
                    ))
        else:
            res.builds.append(BuildSlot(
                uid=uid, sku=t.sku, station=t.station or "?",
                start=int(sol.value(start[uid])), end=int(sol.value(end[uid])),
            ))
        if t.due_day is not None:
            tard = int(sol.value(tardiness_vars[uid]))
            res.total_tardiness += tard
            res.demand_results.append(DemandResult(
                order_id=t.order_id, sku=t.sku, qty=t.qty, due_day=t.due_day,
                completion_day=int(sol.value(end[uid])), tardiness=tard,
            ))
    res.builds.sort(key=lambda b: b.start)
    res.demand_results.sort(key=lambda d: d.due_day)
    return res
