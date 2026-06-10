"""Tests for configurable multi-objective scheduling (iteration 8)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.model import (
    BomLine, DemandLine, Item, MakeBuy, PlanningInput, SourcingMode, WorkCenter,
)
from aps.scheduler import ObjectiveWeights, compare_objectives, schedule


def _pin(due_day: int) -> PlanningInput:
    fg = Item("FG", "F", MakeBuy.MAKE, build_days=5, build_station="S", bom=[BomLine("PART", 1)])
    part = Item("PART", "P", MakeBuy.BUY, sourcing=[
        SourcingMode("ocean", "V", cost_per_unit=100, lead_time_days=60, max_qty=100),
        SourcingMode("air", "V", cost_per_unit=160, lead_time_days=10, max_qty=100),
    ])
    return PlanningInput(items={"FG": fg, "PART": part}, work_centers={"S": WorkCenter("S", 1)},
                         demand=[DemandLine("FG", 1, due_day=due_day, order_id="SO",
                                            tardiness_penalty_per_day=1000)], horizon_days=300)


def test_cost_priority_accepts_lateness_to_save_money():
    # Due 20: on-time needs air ($160). A cost-dominant objective prefers cheap ocean and is late.
    res = schedule(_pin(20), objective=ObjectiveWeights(tardiness=1, cost=1000, makespan=0))
    assert res.sourcing[0].mode_label == "ocean"
    assert res.total_tardiness > 0


def test_ontime_priority_pays_to_expedite():
    # Same case, on-time-dominant objective: pay for air to avoid tardiness.
    res = schedule(_pin(20), objective=ObjectiveWeights(tardiness=100000, cost=1, makespan=0))
    assert res.sourcing[0].mode_label == "air"
    assert res.total_tardiness == 0


def test_default_lexicographic_is_on_time_first():
    res = schedule(_pin(20))  # no objective -> default lexicographic
    assert res.total_tardiness == 0 and res.sourcing[0].mode_label == "air"


def test_compare_objectives_returns_tradeoff_table():
    configs = {
        "on-time": ObjectiveWeights(tardiness=100000, cost=1),
        "cost": ObjectiveWeights(tardiness=1, cost=1000),
    }
    out = compare_objectives(_pin(20), configs, time_limit_s=4)
    assert set(out) == {"on-time", "cost"}
    # on-time config should have <= tardiness and >= cost than the cost config
    assert out["on-time"].total_tardiness <= out["cost"].total_tardiness
    assert out["on-time"].total_cost >= out["cost"].total_cost
    assert out["on-time"].makespan >= 0


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
