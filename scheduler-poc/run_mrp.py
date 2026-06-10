"""Iteration 1 demo: run MRP on the seed dataset and print the time-phased plan.

    python run_mrp.py
"""

from __future__ import annotations

from aps.mrp import run_mrp
from aps.model import MakeBuy
from aps.seed import build_seed


def main() -> None:
    pin = build_seed()
    result = run_mrp(pin)

    print("\nMRP PLANNED ORDERS (release day -> receipt day)")
    print("=" * 78)
    print(f"{'SKU':<16}{'kind':<6}{'qty':>5}  {'release':>8}  {'receipt':>8}  {'lead':>5}  flag")
    print("-" * 78)
    for o in sorted(result.planned_orders, key=lambda o: (o.release_day, o.sku)):
        flag = "  <-- LATE: needs expedite" if o.late_release else ""
        kind = "MAKE" if o.kind is MakeBuy.MAKE else "BUY"
        print(f"{o.sku:<16}{kind:<6}{o.qty:>5}  {o.release_day:>8}  {o.receipt_day:>8}"
              f"  {o.lead_time_days:>5}{flag}")

    print("\nSHORTAGES (standard lead time cannot meet the due date)")
    print("-" * 78)
    if not result.shortages:
        print("  none — everything is feasible with standard sourcing.")
    for o in result.shortages:
        kind = "build" if o.kind is MakeBuy.MAKE else "buy"
        print(f"  {o.sku}: need {o.qty} by day {o.receipt_day}, but {kind} lead time is "
              f"{o.lead_time_days}d -> would have to release on day {o.release_day} (in the past). "
              f"Expedite or re-source.")
    print()


if __name__ == "__main__":
    main()
