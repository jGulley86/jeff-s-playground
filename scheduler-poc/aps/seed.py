"""Sample dataset — a simplified multi-level SlipBot bill of materials.

This is a stand-in for live NetSuite + Drive data (wired in iteration 3). It exercises every feature:
multi-level MAKE BOMs, long-lead purchased parts with air/ocean sourcing alternatives, on-hand
inventory, an in-flight scheduled receipt, and customer demand with due dates + tardiness penalties.

Quantities/lead times are illustrative, not SlipRobotics' real figures.
"""

from __future__ import annotations

from .model import (
    BomLine, DemandLine, InventoryRecord, Item, MakeBuy, PlanningInput,
    ScheduledReceipt, SourcingMode, WorkCenter,
)


def build_seed() -> PlanningInput:
    items: dict[str, Item] = {}

    def make(sku, name, build_days, station, bom, **kw):
        items[sku] = Item(sku=sku, name=name, make_buy=MakeBuy.MAKE,
                           build_days=build_days, build_station=station,
                           bom=[BomLine(c, q) for c, q in bom], **kw)

    def buy(sku, name, modes, **kw):
        items[sku] = Item(sku=sku, name=name, make_buy=MakeBuy.BUY, sourcing=modes, **kw)

    # ---- Finished good ----
    make("SLIPBOT-V3", "SlipBot V3 Autonomous Lift", build_days=10, station="FINAL-ASSY",
         bom=[("DRIVE-MODULE", 1), ("CHASSIS", 1), ("WHEEL-ASSY", 4), ("BATTERY-PACK", 1)])

    # ---- Sub-assemblies (MAKE) ----
    make("DRIVE-MODULE", "Drive Module", build_days=5, station="SUB-ASSY",
         bom=[("MOTOR", 2), ("CONTROLLER-PCB", 1)])
    make("CHASSIS", "Welded Chassis", build_days=4, station="WELD",
         bom=[("ALLOY-FRAME", 1)], lot_size=1)

    # ---- Purchased parts (BUY) with sourcing menus (supplier x freight) ----
    buy("ALLOY-FRAME", "Aluminum Frame Extrusion",
        modes=[
            SourcingMode("FrameCo-ocean", "FrameCo", cost_per_unit=900, lead_time_days=84,
                         max_qty=500, lead_time_stdev=10),
            SourcingMode("FrameCo-air", "FrameCo", cost_per_unit=1300, lead_time_days=21,
                         max_qty=500, lead_time_stdev=4),
            SourcingMode("FrameAlt-prem", "FrameAlt", cost_per_unit=1700, lead_time_days=35,
                         max_qty=60, lead_time_stdev=6),
        ], safety_stock=2, demand_stdev=1.5)

    buy("CONTROLLER-PCB", "Motion Controller PCB (single-source)",
        modes=[
            # Single, backlogged supplier — no faster mode. This is the "genuinely infeasible" case.
            SourcingMode("ChipCo-std", "ChipCo", cost_per_unit=450, lead_time_days=112,
                         max_qty=200, lead_time_stdev=21),
        ], safety_stock=3, demand_stdev=2.0)

    buy("BATTERY-PACK", "LiFePO4 Battery Pack",
        modes=[
            SourcingMode("CellCo-ocean", "CellCo", cost_per_unit=1200, lead_time_days=56,
                         max_qty=300, lead_time_stdev=7),
            SourcingMode("CellCo-air", "CellCo", cost_per_unit=1550, lead_time_days=18,
                         max_qty=300, lead_time_stdev=3),
        ], safety_stock=2, demand_stdev=1.0)

    buy("MOTOR", "BLDC Drive Motor",
        modes=[
            SourcingMode("MotorWorks-ocean", "MotorWorks", cost_per_unit=300, lead_time_days=45,
                         max_qty=2000, lead_time_stdev=5),
            SourcingMode("MotorWorks-air", "MotorWorks", cost_per_unit=380, lead_time_days=14,
                         max_qty=2000, lead_time_stdev=2),
        ], safety_stock=8, demand_stdev=3.0)

    buy("WHEEL-ASSY", "Heavy-duty Wheel Assembly",
        modes=[
            SourcingMode("WheelPro-stock", "WheelPro", cost_per_unit=140, lead_time_days=10,
                         max_qty=10000, lead_time_stdev=2),
        ], safety_stock=20, demand_stdev=6.0)

    # ---- Work centers (finite-capacity build stations) ----
    work_centers = {
        "FINAL-ASSY": WorkCenter("FINAL-ASSY", capacity=2),
        "SUB-ASSY":   WorkCenter("SUB-ASSY", capacity=2),
        "WELD":       WorkCenter("WELD", capacity=1),
    }

    # ---- Inventory on hand ----
    inventory = [
        InventoryRecord("WHEEL-ASSY", 60),
        InventoryRecord("MOTOR", 12),
        InventoryRecord("ALLOY-FRAME", 3),
        InventoryRecord("BATTERY-PACK", 2),
        InventoryRecord("CONTROLLER-PCB", 4),
        InventoryRecord("SLIPBOT-V3", 1),
    ]

    # ---- In-flight supply ----
    scheduled_receipts = [
        ScheduledReceipt("CONTROLLER-PCB", qty=10, due_day=40),
        ScheduledReceipt("BATTERY-PACK", qty=8, due_day=30),
    ]

    # ---- Independent demand (customer orders) ----
    demand = [
        DemandLine("SLIPBOT-V3", qty=5, due_day=120, order_id="SO-1001",
                   revenue=200000, tardiness_penalty_per_day=2000),
        DemandLine("SLIPBOT-V3", qty=3, due_day=160, order_id="SO-1002",
                   revenue=120000, tardiness_penalty_per_day=1500),
    ]

    return PlanningInput(
        items=items, work_centers=work_centers, inventory=inventory,
        scheduled_receipts=scheduled_receipts, demand=demand, horizon_days=400,
    )
