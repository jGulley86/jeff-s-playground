"""Tests for the HTML report generator (iteration 10)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.connectors.writeback import build_writeback
from aps.mrp import run_mrp
from aps.report import render_html
from aps.scheduler import schedule
from aps.seed import build_seed


def test_report_renders_html_with_key_sections():
    pin = build_seed()
    sched = schedule(pin)
    wb = build_writeback(pin, sched, run_mrp(pin))
    h = render_html(pin, sched, wb, title="Test Report")
    assert h.startswith("<!doctype html>")
    for token in ("Gantt", "Promise dates", "Sourcing decisions", "Exceptions", "Makespan"):
        assert token in h
    # demand orders appear
    for d in sched.demand_results:
        assert d.order_id in h


def test_report_escapes_and_handles_no_exceptions():
    pin = build_seed()
    sched = schedule(pin)
    h = render_html(pin, sched, writeback=None, title="No WB")
    assert "No exceptions" in h  # writeback omitted -> clean message
    assert "<script>" not in h   # nothing injected


def test_report_marks_late_orders_red():
    # Force a late order and confirm the 'late' class shows up.
    from aps.model import BomLine, DemandLine, Item, MakeBuy, PlanningInput, SourcingMode, WorkCenter
    fg = Item("FG", "F", MakeBuy.MAKE, build_days=5, build_station="S", bom=[BomLine("PART", 1)])
    part = Item("PART", "P", MakeBuy.BUY,
                sourcing=[SourcingMode("air", "V", 160, 10, max_qty=100)])
    pin = PlanningInput(items={"FG": fg, "PART": part}, work_centers={"S": WorkCenter("S", 1)},
                        demand=[DemandLine("FG", 1, due_day=5, order_id="RUSH",
                                           tardiness_penalty_per_day=1000)], horizon_days=100)
    sched = schedule(pin)
    h = render_html(pin, sched, build_writeback(pin, sched))
    assert "LATE" in h and "late" in h


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
