"""Iteration 4 demo: quote three rush orders against the committed SlipBot plan.

    python run_quote.py
"""

from __future__ import annotations

from aps.model import DemandLine
from aps.promising import quote_rush_order
from aps.scheduler import schedule
from aps.seed import build_seed


def main() -> None:
    pin = build_seed()
    baseline = schedule(pin)
    print("\nCOMMITTED BASELINE")
    print("=" * 78)
    for d in baseline.demand_results:
        print(f"  {d.order_id}: {d.qty}x {d.sku} due {d.due_day} -> done {d.completion_day} "
              f"({'on time' if d.tardiness == 0 else f'{d.tardiness}d late'})")
    print(f"  baseline sourcing cost: ${baseline.total_cost:,}")

    scenarios = [
        ("comfortable", DemandLine("SLIPBOT-V3", 2, due_day=200, order_id="RUSH-A",
                                   revenue=80000, tardiness_penalty_per_day=2000)),
        ("rush (expedite)", DemandLine("SLIPBOT-V3", 2, due_day=80, order_id="RUSH-B",
                                       revenue=120000, tardiness_penalty_per_day=3000)),
        ("near-impossible", DemandLine("SLIPBOT-V3", 2, due_day=45, order_id="RUSH-C",
                                       revenue=120000, tardiness_penalty_per_day=3000)),
    ]
    for label, rush in scenarios:
        print(f"\n{'=' * 78}\nRUSH SCENARIO: {label}\n{'-' * 78}")
        q = quote_rush_order(pin, rush, baseline=baseline)
        print(q.summary())
    print()


if __name__ == "__main__":
    main()
