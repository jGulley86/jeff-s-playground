"""Tests for operation-level routing (iteration 6)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.model import (
    DemandLine, Item, MakeBuy, Operation, PlanningInput, WorkCenter,
)
from aps.scheduler import schedule


def test_operation_duration_setup_plus_run():
    op = Operation("CUT", "WC1", setup_days=2, run_days_per_unit=1.0)
    assert op.duration(1) == 3      # 2 + ceil(1*1)
    assert op.duration(4) == 6      # 2 + ceil(1*4)


def test_nominal_build_days_sums_routing():
    item = Item("FG", "F", MakeBuy.MAKE, routing=[
        Operation("CUT", "WC1", 2, 1.0),
        Operation("WELD", "WC2", 1, 0.5),
    ])
    assert item.nominal_build_days(1) == 5    # (2+1) + (1+1)
    assert item.nominal_build_days(4) == 9    # (2+4) + (1+2)


def _routed_pin(due_day: int, n_orders: int = 1) -> PlanningInput:
    fg = Item("FG", "Finished", MakeBuy.MAKE, routing=[
        Operation("CUT", "WC1", setup_days=2, run_days_per_unit=1.0),
        Operation("WELD", "WC2", setup_days=1, run_days_per_unit=0.5),
    ])
    demand = [DemandLine("FG", 4, due_day=due_day, order_id=f"SO-{i}",
                         tardiness_penalty_per_day=500) for i in range(n_orders)]
    return PlanningInput(
        items={"FG": fg},
        work_centers={"WC1": WorkCenter("WC1", 1), "WC2": WorkCenter("WC2", 1)},
        demand=demand, horizon_days=300,
    )


def test_routed_build_schedules_operations_in_sequence():
    res = schedule(_routed_pin(due_day=100))
    # CUT (6d) then WELD (3d) = done day 9 for qty 4
    assert res.feasible and res.total_tardiness == 0
    assert res.demand_results[0].completion_day == 9


def test_routed_finite_capacity_serializes_two_orders():
    # Two orders, single-capacity work centers -> their CUT ops cannot overlap.
    res = schedule(_routed_pin(due_day=100, n_orders=2))
    assert res.feasible
    # Each order takes CUT=6; on a capacity-1 WC1 they serialize, so the later order finishes >= 12.
    completions = sorted(d.completion_day for d in res.demand_results)
    assert completions[1] >= 12


if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {fn.__name__}")
            traceback.print_exc()
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
