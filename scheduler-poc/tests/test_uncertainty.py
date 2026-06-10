"""Tests for lead-time uncertainty: safety time + robustness simulation (iteration 7)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.model import (
    BomLine, DemandLine, Item, MakeBuy, PlanningInput, SourcingMode, WorkCenter,
)
from aps.uncertainty import robust_lead_time, robustify, simulate_service_level


def test_robust_lead_time_adds_safety_time():
    # mean 60, sigma 10, 95% -> 60 + 1.645*10 ~= 76
    assert robust_lead_time(60, 10, 0.95) == 76
    # zero variability -> no safety time
    assert robust_lead_time(60, 0, 0.95) == 60


def test_higher_service_level_means_more_safety_time():
    lo = robust_lead_time(60, 10, 0.90)
    hi = robust_lead_time(60, 10, 0.99)
    assert hi > lo > 60


def _variable_pin() -> PlanningInput:
    fg = Item("FG", "F", MakeBuy.MAKE, build_days=2, build_station="S", bom=[BomLine("PART", 1)])
    part = Item("PART", "P", MakeBuy.BUY, sourcing=[
        SourcingMode("v-std", "V", cost_per_unit=100, lead_time_days=30, lead_time_stdev=8),
    ])
    return PlanningInput(items={"FG": fg, "PART": part},
                         work_centers={"S": WorkCenter("S", 1)},
                         demand=[DemandLine("FG", 1, due_day=40, order_id="SO",
                                            tardiness_penalty_per_day=500)],
                         horizon_days=200)


def test_robustify_inflates_lead_times():
    pin = _variable_pin()
    r = robustify(pin, 0.95)
    assert r.items["PART"].sourcing[0].lead_time_days > pin.items["PART"].sourcing[0].lead_time_days


def test_higher_planning_service_level_improves_realized_on_time():
    pin = _variable_pin()
    # Due day 40, mean lead 30 + build 2 = 32 planned. With sigma 8, low safety time risks lateness.
    lo = simulate_service_level(pin, planning_service_level=0.50, samples=20, seed=1, time_limit_s=2)
    hi = simulate_service_level(pin, planning_service_level=0.98, samples=20, seed=1, time_limit_s=2)
    assert hi.overall_on_time_rate >= lo.overall_on_time_rate
    assert 0.0 <= lo.overall_on_time_rate <= 1.0


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
