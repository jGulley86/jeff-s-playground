"""Lead-time uncertainty: safety time, rolling-horizon replanning, and robustness simulation.

Research §6: at high utilization / high variability, planning against AVERAGE lead times is fragile.
Two levers:
  * Safety time  — plan against a service-level PERCENTILE lead time (mean + z*sigma), so procurement
    is released early enough to absorb normal supplier variability. (Preferred over safety stock when
    you can forecast need dates well — research §6.)
  * Rolling horizon — re-plan over a moving window as actuals arrive, committing only the near term.

`simulate_service_level` quantifies how often a plan actually hits its dates when lead times are
drawn from their distributions, so you can choose a planning service level with eyes open.
"""

from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field

from .model import PlanningInput, SourcingMode
from .safety_stock import z_for_service_level
from .scheduler import ScheduleResult, schedule


def robust_lead_time(mean_days: float, stdev_days: float, service_level: float) -> int:
    """Percentile lead time = mean + z(service_level) * sigma, rounded up (safety time)."""
    z = z_for_service_level(service_level)
    return max(int(round(mean_days + z * stdev_days)), 0)


def robustify(pin: PlanningInput, service_level: float = 0.95) -> PlanningInput:
    """Return a copy of the plan whose sourcing lead times are inflated to the service-level
    percentile, so the schedule builds in safety time against supplier lead-time variability."""
    out = copy.deepcopy(pin)
    for item in out.items.values():
        new_modes = []
        for m in item.sourcing:
            new_modes.append(SourcingMode(
                label=m.label, supplier=m.supplier, cost_per_unit=m.cost_per_unit,
                lead_time_days=robust_lead_time(m.lead_time_days, m.lead_time_stdev, service_level),
                max_qty=m.max_qty, moq=m.moq, lead_time_stdev=m.lead_time_stdev,
            ))
        item.sourcing = new_modes
    return out


@dataclass
class RobustnessReport:
    samples: int
    planning_service_level: float
    overall_on_time_rate: float
    per_order_on_time: dict[str, float] = field(default_factory=dict)
    mean_tardiness: float = 0.0
    p95_tardiness: int = 0


def simulate_service_level(pin: PlanningInput, planning_service_level: float = 0.95,
                           samples: int = 30, seed: int = 0,
                           time_limit_s: float = 4.0) -> RobustnessReport:
    """Monte Carlo: build a safety-time plan, then draw ACTUAL lead times from each mode's
    distribution and re-plan each scenario, recording how often each order still hits its date.

    Interpretation: this is the achievable service level assuming you re-plan optimally as actuals
    land (an optimistic but realistic upper bound for a shop that replans). Raising the planning
    service level (more safety time) trades cost/earliness for a higher realized on-time rate.
    """
    rng = random.Random(seed)
    robust_pin = robustify(pin, planning_service_level)

    on_time_counts: dict[str, int] = {}
    seen: dict[str, int] = {}
    tardiness_samples: list[int] = []

    for _ in range(samples):
        scen = copy.deepcopy(robust_pin)
        # Draw actual lead times from the ORIGINAL (mean, sigma); keep the safety-time plan's choices
        # honest by perturbing the lead actually experienced.
        orig = {it.sku: {m.label: m for m in pin.items[it.sku].sourcing} for it in pin.items.values()}
        for item in scen.items.values():
            drawn = []
            for m in item.sourcing:
                base = orig.get(item.sku, {}).get(m.label)
                mean = base.lead_time_days if base else m.lead_time_days
                sigma = base.lead_time_stdev if base else m.lead_time_stdev
                actual = max(int(round(rng.gauss(mean, sigma))), 0) if sigma > 0 else mean
                drawn.append(SourcingMode(m.label, m.supplier, m.cost_per_unit, actual,
                                          m.max_qty, m.moq, m.lead_time_stdev))
            item.sourcing = drawn
        res: ScheduleResult = schedule(scen, time_limit_s)
        for d in res.demand_results:
            seen[d.order_id] = seen.get(d.order_id, 0) + 1
            if d.tardiness == 0:
                on_time_counts[d.order_id] = on_time_counts.get(d.order_id, 0) + 1
            tardiness_samples.append(d.tardiness)

    per_order = {oid: on_time_counts.get(oid, 0) / n for oid, n in seen.items()}
    overall = (sum(on_time_counts.values()) / sum(seen.values())) if seen else 1.0
    tardiness_samples.sort()
    p95 = tardiness_samples[int(0.95 * (len(tardiness_samples) - 1))] if tardiness_samples else 0
    mean_t = sum(tardiness_samples) / len(tardiness_samples) if tardiness_samples else 0.0
    return RobustnessReport(
        samples=samples, planning_service_level=planning_service_level,
        overall_on_time_rate=overall, per_order_on_time=per_order,
        mean_tardiness=mean_t, p95_tardiness=p95,
    )


# --------------------------------------------------------------------------------------------------
# Rolling-horizon replanning
# --------------------------------------------------------------------------------------------------

@dataclass
class RollingResult:
    as_of_day: int
    committed: list[str]          # order_ids committed (inside the freeze fence) this cycle
    schedule: ScheduleResult


def rolling_horizon(pin: PlanningInput, cycle_days: int = 30, freeze_fence_days: int = 14,
                    cycles: int = 3, service_level: float = 0.95,
                    time_limit_s: float = 6.0) -> list[RollingResult]:
    """Re-plan every `cycle_days`, committing (freezing) any order whose build starts within the
    freeze fence so the near-term plan is stable (mitigates MRP nervousness — research §6).

    This is a lightweight scaffold: each cycle re-solves the (safety-time) plan as-of a day and marks
    which orders are now frozen. Wire live actuals/receipts updates between cycles in production.
    """
    results: list[RollingResult] = []
    robust = robustify(pin, service_level)
    for c in range(cycles):
        as_of = c * cycle_days
        res = schedule(robust, time_limit_s)
        committed = [
            b.uid.split("/")[0]
            for b in res.builds
            if b.start <= as_of + freeze_fence_days
        ]
        results.append(RollingResult(as_of_day=as_of, committed=sorted(set(committed)),
                                      schedule=res))
    return results
