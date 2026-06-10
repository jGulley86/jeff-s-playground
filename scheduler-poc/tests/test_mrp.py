"""Tests for the MRP core (iteration 1)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.mrp import low_level_codes, run_mrp
from aps.model import (
    BomLine, DemandLine, InventoryRecord, Item, MakeBuy, PlanningInput, SourcingMode,
)
from aps.seed import build_seed


def test_low_level_codes_increase_with_depth():
    pin = build_seed()
    codes = low_level_codes(pin.items)
    assert codes["SLIPBOT-V3"] == 0          # finished good, never a component
    assert codes["DRIVE-MODULE"] == 1        # direct child of SLIPBOT-V3
    assert codes["CONTROLLER-PCB"] == 2      # child of DRIVE-MODULE
    # A part appearing at multiple depths gets the DEEPEST code:
    assert codes["ALLOY-FRAME"] == 2         # CHASSIS(1) -> ALLOY-FRAME(2)


def test_explosion_nets_against_on_hand():
    # 5 finished goods demanded, 1 on hand -> net build of 4.
    pin = build_seed()
    result = run_mrp(pin)
    first_fg = min((o for o in result.orders_for("SLIPBOT-V3")), key=lambda o: o.receipt_day)
    assert first_fg.qty == 4
    assert first_fg.kind is MakeBuy.MAKE


def test_lead_time_offsetting():
    # ALLOY-FRAME preferred (cheapest) mode is 84-day ocean; release = receipt - 84.
    pin = build_seed()
    result = run_mrp(pin)
    frame = min(result.orders_for("ALLOY-FRAME"), key=lambda o: o.receipt_day)
    assert frame.lead_time_days == 84
    assert frame.release_day == frame.receipt_day - 84


def test_rush_date_creates_shortage():
    # A near-term due date for a long-lead purchased part must flag a late release (expedite needed).
    item = Item(
        sku="WIDGET", name="Widget", make_buy=MakeBuy.MAKE, build_days=5, build_station="A",
        bom=[BomLine("LONGLEAD", 1)],
    )
    longlead = Item(
        sku="LONGLEAD", name="Long lead part", make_buy=MakeBuy.BUY,
        sourcing=[SourcingMode("V-ocean", "V", cost_per_unit=10, lead_time_days=84, max_qty=100)],
    )
    pin = PlanningInput(
        items={"WIDGET": item, "LONGLEAD": longlead},
        demand=[DemandLine("WIDGET", qty=1, due_day=20, order_id="RUSH")],
        horizon_days=200,
    )
    result = run_mrp(pin)
    assert result.shortages, "expected a shortage when 84d part is needed in 20 days"
    assert any(o.sku == "LONGLEAD" and o.release_day < 0 for o in result.shortages)


def test_safety_stock_is_respected():
    # With safety stock 8 and on-hand 12, demand of 6 dips below SS -> triggers a planned order.
    pin = build_seed()
    result = run_mrp(pin)
    motor_orders = result.orders_for("MOTOR")
    assert motor_orders, "expected MOTOR planned orders to maintain safety stock"


if __name__ == "__main__":
    # Allow running without pytest installed.
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
