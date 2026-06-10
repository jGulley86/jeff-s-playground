"""Tests for NetSuite plan write-back + exceptions (iteration 9)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.connectors.writeback import NetSuiteWriter, build_writeback
from aps.model import (
    BomLine, DemandLine, Item, MakeBuy, PlanningInput, SourcingMode, WorkCenter,
)
from aps.mrp import run_mrp
from aps.scheduler import schedule
from aps.seed import build_seed


def test_writeback_builds_work_and_purchase_orders():
    pin = build_seed()
    sched = schedule(pin)
    plan = build_writeback(pin, sched, run_mrp(pin))
    assert plan.work_orders, "expected work orders for MAKE builds"
    assert plan.purchase_orders, "expected purchase orders for sourcing choices"
    # every PO carries vendor + item + qty
    for po in plan.purchase_orders:
        assert po["item"] and po["vendor"] and po["quantity"]


def test_dry_run_does_not_send():
    pin = build_seed()
    plan = build_writeback(pin, schedule(pin))
    out = NetSuiteWriter(dry_run=True).commit(plan)
    assert out["dry_run"] is True
    assert out["purchase_orders"] == plan.purchase_orders


def test_commit_calls_create_record_when_live():
    pin = build_seed()
    plan = build_writeback(pin, schedule(pin))
    sent = []

    def fake_create(record_type, payload):
        sent.append((record_type, payload))
        return {"id": f"{record_type}-{len(sent)}"}

    out = NetSuiteWriter(create_record=fake_create, dry_run=False).commit(plan)
    assert len(out["work_orders"]) == len(plan.work_orders)
    assert len(out["purchase_orders"]) == len(plan.purchase_orders)
    assert len(sent) == len(plan.work_orders) + len(plan.purchase_orders)


def test_exceptions_flag_late_and_expedite():
    # Tight due date forces both expedite and (if still impossible) late exceptions.
    fg = Item("FG", "F", MakeBuy.MAKE, build_days=5, build_station="S", bom=[BomLine("PART", 1)])
    part = Item("PART", "P", MakeBuy.BUY, sourcing=[
        SourcingMode("ocean", "V", 100, 60, max_qty=100),
        SourcingMode("air", "V", 160, 10, max_qty=100),
    ])
    pin = PlanningInput(items={"FG": fg, "PART": part}, work_centers={"S": WorkCenter("S", 1)},
                        demand=[DemandLine("FG", 1, due_day=12, order_id="RUSH",
                                           tardiness_penalty_per_day=1000)], horizon_days=200)
    plan = build_writeback(pin, schedule(pin))
    kinds = {e.kind for e in plan.exceptions}
    assert "expedite" in kinds, "air sourcing should raise an expedite exception"


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
