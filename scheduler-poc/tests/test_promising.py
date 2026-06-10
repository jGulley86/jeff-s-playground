"""Tests for the rush-order promising / accept-reject engine (iteration 4)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.model import (
    BomLine, DemandLine, Item, MakeBuy, PlanningInput, SourcingMode, WorkCenter,
)
from aps.promising import quote_rush_order


def _fg_with_two_modes() -> PlanningInput:
    fg = Item("FG", "Finished", MakeBuy.MAKE, build_days=5, build_station="S",
              bom=[BomLine("PART", 1)])
    part = Item("PART", "Part", MakeBuy.BUY, sourcing=[
        SourcingMode("ocean", "V", 100, 60, max_qty=100),
        SourcingMode("air", "V", 160, 10, max_qty=100),
    ])
    return PlanningInput(items={"FG": fg, "PART": part},
                         work_centers={"S": WorkCenter("S", 1)}, horizon_days=300)


def test_quote_on_time_without_expedite_accepts():
    pin = _fg_with_two_modes()
    rush = DemandLine("FG", 1, due_day=120, order_id="RUSH", revenue=50000,
                      tardiness_penalty_per_day=1000)
    q = quote_rush_order(pin, rush)
    assert q.on_time and not q.expedited_parts
    assert q.recommend_accept and q.profit > 0


def test_quote_detects_expedite():
    pin = _fg_with_two_modes()
    rush = DemandLine("FG", 1, due_day=20, order_id="RUSH", revenue=50000,
                      tardiness_penalty_per_day=1000)
    q = quote_rush_order(pin, rush)
    assert q.on_time, "should hit day 20 via air"
    assert any("air" in p for p in q.expedited_parts)
    assert q.incremental_cost > 0


def test_quote_declines_unprofitable_impossible_date():
    pin = _fg_with_two_modes()
    # Earliest possible = air(10)+build(5)=15; due 5 => 10 days late. Tiny revenue, huge penalty.
    rush = DemandLine("FG", 1, due_day=5, order_id="RUSH", revenue=1000,
                      tardiness_penalty_per_day=5000)
    q = quote_rush_order(pin, rush)
    assert not q.on_time and q.tardiness == 10
    assert q.profit < 0 and not q.recommend_accept


def test_quote_reports_displacement():
    # One station, capacity 1. An existing order and a more-urgent rush compete for it.
    fg = Item("FG", "Finished", MakeBuy.MAKE, build_days=10, build_station="S")
    pin = PlanningInput(
        items={"FG": fg}, work_centers={"S": WorkCenter("S", 1)},
        demand=[DemandLine("FG", 1, due_day=100, order_id="EXIST",
                           tardiness_penalty_per_day=500)],
        horizon_days=300,
    )
    rush = DemandLine("FG", 1, due_day=12, order_id="RUSH", revenue=50000,
                      tardiness_penalty_per_day=1000)
    q = quote_rush_order(pin, rush)
    # rush takes the station first; existing order must wait -> but due 100 has slack, may not slip.
    # Force contention: both want the early window. Rush builds days 0-10; existing 10-20, due 100.
    # No slip expected here (slack), so assert the quote is at least feasible & accepted.
    assert q.feasible and q.recommend_accept


def test_quote_displacement_forced_by_global_optimum():
    # Existing order has slack (due 100); a very urgent rush (due 5) takes the single station first
    # because that strictly lowers total tardiness -> the existing order is forced to slip.
    fg = Item("FG", "Finished", MakeBuy.MAKE, build_days=10, build_station="S")
    pin = PlanningInput(
        items={"FG": fg}, work_centers={"S": WorkCenter("S", 1)},
        demand=[DemandLine("FG", 1, due_day=100, order_id="EXIST",
                           tardiness_penalty_per_day=500)],
        horizon_days=300,
    )
    rush = DemandLine("FG", 1, due_day=5, order_id="RUSH", revenue=50000,
                      tardiness_penalty_per_day=1000)
    q = quote_rush_order(pin, rush)
    assert any(d.order_id == "EXIST" and d.days_later > 0 for d in q.displacements), \
        "slack existing order should slip when the urgent rush takes the station first"


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
