"""Tests for safety-stock / ROP / EOQ formulas (iteration 5)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.safety_stock import (
    economic_order_quantity, recommend_policy, reorder_point,
    safety_stock_combined, safety_stock_demand_variability, z_for_service_level,
)


def test_z_scores_match_standard_table():
    assert abs(z_for_service_level(0.95) - 1.645) < 0.01
    assert abs(z_for_service_level(0.975) - 1.96) < 0.01
    assert abs(z_for_service_level(0.90) - 1.282) < 0.01


def test_safety_stock_demand_variability():
    # SS = Z * sigma_D * sqrt(LT) = 1.645 * 10 * sqrt(16) = 65.8
    ss = safety_stock_demand_variability(1.645, 10, 16)
    assert abs(ss - 65.8) < 0.5


def test_combined_formula_lead_time_dominates():
    # When sigma_L is large, the D^2*sigma_L^2 term should dominate the buffer.
    only_demand = safety_stock_demand_variability(1.645, 2, 84)
    combined = safety_stock_combined(1.645, avg_demand=5, demand_stdev=2,
                                     lead_time_days=84, lead_time_stdev=14)
    assert combined > only_demand * 2


def test_reorder_point():
    # ROP = avg_demand*LT + SS = 5*84 + 100 = 520
    assert reorder_point(5, 84, 100) == 520


def test_eoq():
    # EOQ = sqrt(2*D*S/H) = sqrt(2*1000*50/2) = sqrt(50000) ~ 223.6
    assert abs(economic_order_quantity(1000, 50, 2) - 223.6) < 0.5


def test_recommend_policy_uses_combined_when_lead_varies():
    pol = recommend_policy("X", avg_demand_per_day=5, demand_stdev=2,
                           lead_time_days=84, lead_time_stdev=14, service_level=0.95)
    assert pol.safety_stock > 0 and pol.reorder_point > pol.safety_stock


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
