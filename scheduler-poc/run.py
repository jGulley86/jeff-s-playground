"""aps — top-level orchestrator / CLI.

Ties the whole engine together: load data -> MRP purchasing plan -> finite-capacity schedule with
cost-aware sourcing -> safety-stock recommendations -> optional rush-order quote.

Examples:
    python run.py                          # full report on the seed dataset
    python run.py --snapshot ns.json       # load a live NetSuite snapshot (see connectors/netsuite)
    python run.py --quote SLIPBOT-V3:2@45  # quote 2 SlipBots wanted by day 45
    python run.py --service-level 0.97     # safety stock at a 97% service level
"""

from __future__ import annotations

import argparse

from aps.connectors.netsuite import load_snapshot, planning_input_from_snapshot
from aps.model import DemandLine, MakeBuy, PlanningInput
from aps.mrp import run_mrp
from aps.promising import quote_rush_order
from aps.safety_stock import recommend_policy
from aps.scheduler import schedule
from aps.seed import build_seed


def load(args) -> PlanningInput:
    if args.snapshot:
        pin = planning_input_from_snapshot(load_snapshot(args.snapshot))
        if not pin.work_centers:
            print("  (note: snapshot has no work centers; builds run unconstrained. "
                  "Add routings/stations to enable finite capacity.)")
        return pin
    return build_seed()


def section(title: str) -> None:
    print(f"\n{'=' * 84}\n{title}\n{'-' * 84}")


def report_mrp(pin: PlanningInput) -> None:
    section("MRP — TIME-PHASED PURCHASING / BUILD PLAN")
    result = run_mrp(pin)
    print(f"{'SKU':<16}{'kind':<6}{'qty':>5}  {'release':>8}  {'receipt':>8}  flag")
    for o in sorted(result.planned_orders, key=lambda o: (o.release_day, o.sku)):
        flag = "  <-- LATE: expedite/re-source" if o.late_release else ""
        kind = "MAKE" if o.kind is MakeBuy.MAKE else "BUY"
        print(f"{o.sku:<16}{kind:<6}{o.qty:>5}  {o.release_day:>8}  {o.receipt_day:>8}{flag}")
    if result.shortages:
        print(f"  {len(result.shortages)} shortage(s) need expediting — see the scheduler's sourcing choices.")


def report_schedule(pin: PlanningInput):
    section("FINITE-CAPACITY SCHEDULE  (on-time first, then cheapest sourcing)")
    res = schedule(pin)
    print(f"status={res.status}  total_tardiness={res.total_tardiness}d  "
          f"sourcing_cost=${res.total_cost:,}\n")
    print("  Promise dates:")
    for d in res.demand_results:
        v = "ON TIME" if d.tardiness == 0 else f"LATE {d.tardiness}d"
        print(f"    {d.order_id:<8} {d.qty}x {d.sku:<12} due {d.due_day:>4} -> done {d.completion_day:>4}  [{v}]")
    print("\n  Sourcing decisions:")
    for s in sorted(res.sourcing, key=lambda s: s.sku):
        exp = "  *EXPEDITE*" if ("air" in s.mode_label.lower() or "prem" in s.mode_label.lower()) else ""
        print(f"    {s.sku:<14} x{s.qty:<3} {s.mode_label:<18} lead {s.lead_time_days:>3}d  ${s.cost:,}{exp}")
    return res


def report_safety_stock(pin: PlanningInput, service_level: float) -> None:
    section(f"SAFETY-STOCK RECOMMENDATIONS  (service level {service_level:.0%})")
    # Rough average daily demand from total demand over the horizon.
    total_qty = sum(d.qty for d in pin.demand) or 1
    horizon = max(pin.horizon_days, 1)
    print(f"{'SKU':<16}{'lead':>5}{'sigmaLT':>8}{'SS':>6}{'ROP':>6}")
    for sku, item in pin.items.items():
        if item.make_buy is not MakeBuy.BUY or not item.sourcing:
            continue
        mode = item.default_mode()
        # crude per-day demand proxy; in production derive from demand history / forecast
        avg_demand = (total_qty / horizon)
        pol = recommend_policy(
            sku, avg_demand_per_day=max(avg_demand, 0.1),
            demand_stdev=max(item.demand_stdev, 0.5),
            lead_time_days=mode.lead_time_days, lead_time_stdev=mode.lead_time_stdev,
            service_level=service_level,
        )
        print(f"{sku:<16}{mode.lead_time_days:>5}{mode.lead_time_stdev:>8.1f}"
              f"{pol.safety_stock:>6}{pol.reorder_point:>6}")
    print("  (lead-time variability sigmaLT drives most of the buffer for long-lead parts.)")


def report_quote(pin: PlanningInput, spec: str, baseline) -> None:
    # spec format: SKU:QTY@DAY
    sku_qty, _, day = spec.partition("@")
    sku, _, qty = sku_qty.partition(":")
    rush = DemandLine(sku=sku, qty=int(qty or 1), due_day=int(day or 30), order_id="RUSH-CLI",
                      revenue=0, tardiness_penalty_per_day=2000)
    section(f"RUSH-ORDER QUOTE  ({rush.qty}x {rush.sku} by day {rush.due_day})")
    print(quote_rush_order(pin, rush, baseline=baseline).summary())


def main() -> None:
    ap = argparse.ArgumentParser(description="Integrated production scheduler")
    ap.add_argument("--snapshot", help="path to a NetSuite snapshot JSON")
    ap.add_argument("--service-level", type=float, default=0.95)
    ap.add_argument("--quote", help="rush order to quote, format SKU:QTY@DAY (e.g. SLIPBOT-V3:2@45)")
    ap.add_argument("--no-mrp", action="store_true")
    args = ap.parse_args()

    pin = load(args)
    print(f"Loaded plan: {len(pin.items)} items, {len(pin.demand)} demand lines, "
          f"horizon {pin.horizon_days}d.")
    if not args.no_mrp:
        report_mrp(pin)
    baseline = report_schedule(pin)
    report_safety_stock(pin, args.service_level)
    if args.quote:
        report_quote(pin, args.quote, baseline)
    print()


if __name__ == "__main__":
    main()
