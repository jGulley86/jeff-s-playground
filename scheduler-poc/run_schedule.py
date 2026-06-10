"""Iteration 2 demo: explode demand, schedule on finite capacity, choose sourcing. on-time first.

    python run_schedule.py
"""

from __future__ import annotations

from aps.scheduler import schedule
from aps.seed import build_seed


def main() -> None:
    pin = build_seed()
    res = schedule(pin)

    print("\nINTEGRATED SCHEDULE  (on-time-first, then cheapest sourcing)")
    print("=" * 80)
    print(f"status={res.status}  total_tardiness={res.total_tardiness}d  "
          f"total_sourcing_cost=${res.total_cost:,}")

    print("\nDEMAND / PROMISE DATES")
    print("-" * 80)
    for d in res.demand_results:
        verdict = "ON TIME" if d.tardiness == 0 else f"LATE by {d.tardiness}d"
        print(f"  {d.order_id:<8} {d.sku:<12} x{d.qty:<3} due {d.due_day:>4}  "
              f"-> done {d.completion_day:>4}  [{verdict}]")

    print("\nSOURCING DECISIONS  (chosen supplier x freight per purchased part)")
    print("-" * 80)
    for s in sorted(res.sourcing, key=lambda s: s.sku):
        print(f"  {s.sku:<14} x{s.qty:<3} -> {s.mode_label:<18} lead {s.lead_time_days:>3}d  "
              f"ready day {s.ready_day:>4}  ${s.cost:,}")

    print("\nBUILD SCHEDULE  (finite-capacity stations)")
    print("-" * 80)
    for b in res.builds:
        print(f"  {b.station:<12} {b.sku:<14} day {b.start:>4} -> {b.end:>4}  ({b.uid})")
    print()


if __name__ == "__main__":
    main()
