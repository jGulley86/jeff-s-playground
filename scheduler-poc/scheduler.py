"""Integrated production scheduler — proof of concept.

A CP-SAT model that jointly:
  * schedules each job's operations on finite-capacity work centers (NoOverlap), and
  * CHOOSES how to source each raw material (supplier x freight mode), where each mode has its own
    cost and lead time, and the lead time gates when production can start.

Objective (research doc §7.5):
    minimize  Σ material cost (qty x chosen mode cost)  +  Σ weightⱼ x tardinessⱼ

The "lead time is a decision variable" pattern (§7.1/§7.7) is implemented with one boolean presence
literal per sourcing mode and `add_exactly_one`, so the solver pays a freight/expedite premium only
when doing so beats the tardiness penalty — and when no mode can hit the date, it returns the
cheapest plan and reports the unavoidable tardiness (the "earliest I can do is day N" quote).

Run:  python scheduler.py
"""

from __future__ import annotations

from ortools.sat.python import cp_model

import data


def solve_scenario(scenario: data.Scenario) -> None:
    model = cp_model.CpModel()
    H = scenario.horizon

    # Bookkeeping we read back after solving.
    mode_presence: dict[tuple[str, str, int], cp_model.IntVar] = {}  # (job, material, mode_idx) -> bool
    material_cost_terms: list[cp_model.LinearExpr] = []
    job_completion: dict[str, cp_model.IntVar] = {}
    job_tardiness: dict[str, cp_model.IntVar] = {}
    job_first_op_start: dict[str, cp_model.IntVar] = {}
    job_material_ready: dict[str, cp_model.IntVar] = {}
    # intervals per work center, to enforce finite capacity
    wc_intervals: dict[str, list] = {wc: [] for wc in data.WORK_CENTERS}
    wc_demands: dict[str, list[int]] = {wc: [] for wc in data.WORK_CENTERS}
    # per-job op schedule for reporting: job -> list[(wc, start_var, end_var)]
    job_ops_report: dict[str, list[tuple[str, cp_model.IntVar, cp_model.IntVar]]] = {}

    for job in scenario.jobs:
        # ---- Sourcing decision per material: pick exactly one mode -------------------------------
        material_lead_vars: list[cp_model.IntVar] = []
        for mat_name, qty in job.materials.items():
            material = data.MATERIALS[mat_name]
            presences = []
            for m_idx, mode in enumerate(material.modes):
                p = model.new_bool_var(f"{job.name}__{mat_name}__{mode.label}")
                mode_presence[(job.name, mat_name, m_idx)] = p
                presences.append(p)
                # A mode that can't supply the required quantity cannot be chosen (supplier capacity).
                if qty > mode.max_qty:
                    model.add(p == 0)
                # Material cost contribution when this mode is chosen.
                material_cost_terms.append(p * (mode.cost_per_unit * qty))
            model.add_exactly_one(presences)

            # Chosen lead time for this material = Σ presence * lead_time (exactly one term is active).
            lead_var = model.new_int_var(0, H, f"{job.name}__{mat_name}__lead")
            model.add(
                lead_var
                == sum(presences[i] * material.modes[i].lead_time_days
                       for i in range(len(material.modes)))
            )
            material_lead_vars.append(lead_var)

        # Material-ready day for the job = the slowest material to arrive (the bottleneck, §8.3).
        material_ready = model.new_int_var(0, H, f"{job.name}__material_ready")
        model.add_max_equality(material_ready, material_lead_vars)
        job_material_ready[job.name] = material_ready

        # ---- Operations: sequential routing on finite-capacity work centers ----------------------
        prev_end = None
        ops_report: list[tuple[str, cp_model.IntVar, cp_model.IntVar]] = []
        for op_idx, op in enumerate(job.operations):
            start = model.new_int_var(0, H, f"{job.name}__op{op_idx}__start")
            end = model.new_int_var(0, H, f"{job.name}__op{op_idx}__end")
            interval = model.new_interval_var(start, op.duration, end,
                                              f"{job.name}__op{op_idx}__iv")
            wc_intervals[op.work_center].append(interval)
            wc_demands[op.work_center].append(1)
            ops_report.append((op.work_center, start, end))

            if op_idx == 0:
                # Production can't start until the materials have arrived.
                model.add(start >= material_ready)
                job_first_op_start[job.name] = start
            else:
                model.add(start >= prev_end)  # precedence within the routing
            prev_end = end

        job_ops_report[job.name] = ops_report

        # ---- Completion & tardiness --------------------------------------------------------------
        completion = model.new_int_var(0, H, f"{job.name}__completion")
        model.add(completion == prev_end)
        job_completion[job.name] = completion

        tardiness = model.new_int_var(0, H, f"{job.name}__tardiness")
        model.add_max_equality(tardiness, [completion - job.due_date, 0])
        job_tardiness[job.name] = tardiness

    # ---- Finite capacity per work center ---------------------------------------------------------
    for wc_name, wc in data.WORK_CENTERS.items():
        intervals = wc_intervals[wc_name]
        if not intervals:
            continue
        if wc.capacity == 1:
            model.add_no_overlap(intervals)
        else:
            model.add_cumulative(intervals, wc_demands[wc_name], wc.capacity)

    # ---- Objective: material/freight cost + tardiness penalty (§7.5) ------------------------------
    tardiness_cost_terms = [
        job.tardiness_penalty_per_day * job_tardiness[job.name] for job in scenario.jobs
    ]
    model.minimize(sum(material_cost_terms) + sum(tardiness_cost_terms))

    # ---- Solve -----------------------------------------------------------------------------------
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.solve(model)

    _report(scenario, solver, status, mode_presence, job_completion, job_tardiness,
            job_material_ready, job_ops_report)


def _report(scenario, solver, status, mode_presence, job_completion, job_tardiness,
            job_material_ready, job_ops_report) -> None:
    print("=" * 90)
    print(scenario.title)
    print("-" * 90)
    print(scenario.description)
    print()

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"  No solution found (status={solver.status_name(status)}).")
        print()
        return

    total_material_cost = 0
    for job in scenario.jobs:
        print(f"  JOB: {job.name}   (due day {job.due_date}, revenue ${job.revenue:,})")

        # Sourcing decisions
        for mat_name, qty in job.materials.items():
            material = data.MATERIALS[mat_name]
            for m_idx, mode in enumerate(material.modes):
                if solver.value(mode_presence[(job.name, mat_name, m_idx)]) == 1:
                    line_cost = mode.cost_per_unit * qty
                    total_material_cost += line_cost
                    print(f"    material {mat_name:<10} x{qty:<4} -> {mode.label:<14} "
                          f"lead {mode.lead_time_days:>3}d  ${mode.cost_per_unit}/u  "
                          f"= ${line_cost:,}")

        ready = solver.value(job_material_ready[job.name])
        print(f"    materials ready (slowest): day {ready}")

        # Schedule
        for i, (wc, s, e) in enumerate(job_ops_report[job.name]):
            print(f"    op{i} {wc:<10} day {solver.value(s):>3} -> {solver.value(e):>3}")

        completion = solver.value(job_completion[job.name])
        tardiness = solver.value(job_tardiness[job.name])
        print(f"    completion: day {completion}")
        if tardiness == 0:
            print(f"    VERDICT: ON TIME (due day {job.due_date}). Promise it.")
        else:
            print(f"    VERDICT: CANNOT hit day {job.due_date}. Earliest achievable = day "
                  f"{completion} ({tardiness} days late).")
        print()

    tardiness_cost = sum(
        job.tardiness_penalty_per_day * solver.value(job_tardiness[job.name])
        for job in scenario.jobs
    )
    print(f"  COST BREAKDOWN")
    print(f"    material + freight/expedite : ${total_material_cost:,}")
    print(f"    tardiness penalty           : ${tardiness_cost:,}")
    print(f"    -------------------------------------------")
    print(f"    total (objective)           : ${total_material_cost + tardiness_cost:,}")
    print(f"    solver status               : {solver.status_name(status)}"
          f"  ({solver.wall_time:.2f}s)")
    print()


def main() -> None:
    print()
    print("INTEGRATED PRODUCTION SCHEDULER — PROOF OF CONCEPT")
    print("Cost-aware sourcing (supplier/freight choice) + finite-capacity scheduling")
    print("See ../docs/production-scheduler-research.md sections 7 & 8.")
    print()
    for scenario in data.SCENARIOS:
        solve_scenario(scenario)


if __name__ == "__main__":
    main()
