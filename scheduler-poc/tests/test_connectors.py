"""Tests for the ingestion connectors (iteration 3). No network — fake fetchers."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aps.connectors.gdrive import DriveIngestor
from aps.connectors.netsuite import IngestConfig, planning_input_from_snapshot
from aps.model import MakeBuy


FAKE_SNAPSHOT = {
    "items": [
        {"sku": "SLIPBOT-V3", "name": "SlipBot V3", "itemtype": "Assembly", "lead_time": 10,
         "safety_stock": 0},
        {"sku": "ALLOY-FRAME", "name": "Frame", "itemtype": "InventoryItem", "safety_stock": 2},
        {"sku": "WHEEL-ASSY", "name": "Wheel", "itemtype": "InventoryItem"},
    ],
    "bom_lines": [
        {"parent_sku": "SLIPBOT-V3", "component_sku": "ALLOY-FRAME", "qty_per": 1},
        {"parent_sku": "SLIPBOT-V3", "component_sku": "WHEEL-ASSY", "qty_per": 4},
    ],
    "vendor_sourcing": [
        {"sku": "ALLOY-FRAME", "supplier": "FrameCo", "cost": 900, "lead_time": 84},
        {"sku": "WHEEL-ASSY", "supplier": "WheelPro", "cost": 140, "lead_time": 10},
    ],
    "inventory": [
        {"sku": "WHEEL-ASSY", "location": "MAIN", "on_hand": 60},
        {"sku": "ALLOY-FRAME", "location": "MAIN", "on_hand": 3},
    ],
    "open_po": [{"sku": "ALLOY-FRAME", "qty": 5, "due_date": "2026-07-01"}],
    "open_so": [{"order_id": "SO-1001", "sku": "SLIPBOT-V3", "qty": 5,
                 "due_date": "2026-09-01", "revenue": 200000}],
}


def test_snapshot_maps_items_and_bom():
    pin = planning_input_from_snapshot(FAKE_SNAPSHOT, day0="2026-06-10")
    assert pin.items["SLIPBOT-V3"].make_buy is MakeBuy.MAKE
    assert pin.items["SLIPBOT-V3"].build_days == 10
    skus = {l.component for l in pin.items["SLIPBOT-V3"].bom}
    assert skus == {"ALLOY-FRAME", "WHEEL-ASSY"}


def test_vendor_rows_become_sourcing_and_make_item_buy():
    pin = planning_input_from_snapshot(FAKE_SNAPSHOT, day0="2026-06-10")
    frame = pin.items["ALLOY-FRAME"]
    assert frame.make_buy is MakeBuy.BUY
    labels = {m.label for m in frame.sourcing}
    # std mode always; an air alternative is synthesized because lead 84 > 14
    assert "FrameCo-std" in labels and "FrameCo-air" in labels
    air = next(m for m in frame.sourcing if m.label == "FrameCo-air")
    assert air.lead_time_days < 84 and air.cost_per_unit > 900


def test_no_air_mode_for_short_lead():
    pin = planning_input_from_snapshot(FAKE_SNAPSHOT, day0="2026-06-10")
    wheel = pin.items["WHEEL-ASSY"]   # lead 10 (<=14) -> no synthesized air mode
    assert {m.label for m in wheel.sourcing} == {"WheelPro-std"}


def test_demand_and_inventory_mapped():
    pin = planning_input_from_snapshot(FAKE_SNAPSHOT, day0="2026-06-10")
    assert pin.on_hand("WHEEL-ASSY") == 60
    assert len(pin.demand) == 1 and pin.demand[0].order_id == "SO-1001"
    assert pin.demand[0].due_day > 0


def test_drive_reader_maps_forecast_and_inventory():
    sheets = {
        "forecast": [{"Model": "SLIPBOT-V3", "Units": "8", "Need Date": "2026-10-01",
                      "Order ID": "FC-1"}],
        "inv": [{"Part": "MOTOR", "On Hand": "12", "Location": "MAIN"}],
    }
    di = DriveIngestor(lambda fid, tab=None: sheets[fid])
    demand = di.demand_from_forecast("forecast", day0="2026-06-10")
    inv = di.inventory_from_sheet("inv")
    assert demand[0].sku == "SLIPBOT-V3" and demand[0].qty == 8
    assert inv[0].sku == "MOTOR" and inv[0].on_hand == 12


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
