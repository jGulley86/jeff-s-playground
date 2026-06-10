"""Tests for the finite-capacity scheduler + cost-aware sourcing (iteration 2)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.model import (
    BomLine, DemandLine, InventoryRecord, Item, MakeBuy, PlanningInput, SourcingMode, WorkCenter,
)
from aps.scheduler import expand_demand, schedule
from aps.seed import build_seed


def _two_mode_case(due_day: int) -> PlanningInput:
    """FG built from one purchased PART that has a cheap-slow (ocean) and pricey-fast (air) mode."""
    fg = Item(sku="FG", name="Finished", make_buy=MakeBuy.MAKE, build_days=5, build_station="S",
              bom=[BomLine("PART", 1)])
    part = Item(sku="PART", name="Part", make_buy=MakeBuy.BUY, sourcing=[
        SourcingMode("ocean", "V", cost_per_unit=100, lead_time_days=60, max_qty=100),
        SourcingMode("air", "V", cost_per_unit=160, lead_time_days=10, max_qty=100),
    ])
    return PlanningInput(
        items={"FG": fg, "PART": part},
        work_centers={"S": WorkCenter("S", 1)},
        demand=[DemandLine("FG", qty=1, due_day=due_day, order_id="SO",
                           tardiness_penalty_per_day=1000)],
        horizon_days=300,
    )


def test_relaxed_date_uses_cheapest_mode():
    # Due day 120: ocean (60d) + build (5d) fits easily -> pick the cheap ocean mode.
    res = schedule(_two_mode_case(due_day=120))
    assert res.total_tardiness == 0
    assert res.sourcing[0].mode_label == "ocean"


def test_rush_date_forces_expedite():
    # Due day 20: ocean can't make it; model must CHOOSE air to stay on time.
    res = schedule(_two_mode_case(due_day=20))
    assert res.total_tardiness == 0, "should hit the date via expedite"
    assert res.sourcing[0].mode_label == "air"
    assert res.sourcing[0].lead_time_days == 10


def test_impossible_date_minimizes_tardiness():
    # Due day 5: even air (10d) + build (5d) = 15 can't hit day 5. Returns feasible plan, reports lateness.
    res = schedule(_two_mode_case(due_day=5))
    assert res.feasible
    assert res.total_tardiness > 0
    # earliest achievable completion = air(10) + build(5) = day 15 -> 10 days late
    assert res.demand_results[0].completion_day == 15
    assert res.demand_results[0].tardiness == 10


def test_inventory_netting_avoids_tasks():
    # If on-hand fully covers demand, there are no procurement tasks.
    fg = Item(sku="FG", name="Finished", make_buy=MakeBuy.MAKE, build_days=5, build_station="S",
              bom=[BomLine("PART", 1)])
    part = Item(sku="PART", name="Part", make_buy=MakeBuy.BUY,
                sourcing=[SourcingMode("ocean", "V", 100, 60, max_qty=100)])
    pin = PlanningInput(
        items={"FG": fg, "PART": part}, work_centers={"S": WorkCenter("S", 1)},
        inventory=[InventoryRecord("FG", 5)],
        demand=[DemandLine("FG", qty=5, due_day=30, order_id="SO")], horizon_days=100,
    )
    tasks = expand_demand(pin)
    assert not tasks, "demand fully covered by on-hand FG should produce no tasks"


def test_seed_schedule_is_on_time_and_cheapest():
    res = schedule(build_seed())
    assert res.feasible and res.total_tardiness == 0
    # all relaxed -> every chosen mode should be the cheapest (ocean/std), none air
    assert all("air" not in s.mode_label for s in res.sourcing)


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
