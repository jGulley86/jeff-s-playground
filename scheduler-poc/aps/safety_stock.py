"""Safety stock, reorder point, and EOQ (research §4C).

Implements the standard statistical formulas so planning parameters can be COMPUTED from demand and
lead-time variability rather than guessed. Per the research note, lead-time variability (sigma_L)
often dominates, so the combined formula is the recommended default for purchased long-lead parts.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import NormalDist


def z_for_service_level(service_level: float) -> float:
    """Z-score for a cycle service level, e.g. 0.95 -> ~1.645."""
    service_level = min(max(service_level, 0.5), 0.999999)
    return NormalDist().inv_cdf(service_level)


def safety_stock_demand_variability(z: float, demand_stdev: float, lead_time_days: float) -> float:
    """SS = Z * sigma_D * sqrt(LT)  (demand varies, lead time fixed)."""
    return z * demand_stdev * sqrt(max(lead_time_days, 0))


def safety_stock_combined(z: float, avg_demand: float, demand_stdev: float,
                          lead_time_days: float, lead_time_stdev: float) -> float:
    """SS = Z * sqrt(LT*sigma_D^2 + D^2*sigma_L^2)  (both demand and lead time vary)."""
    return z * sqrt(lead_time_days * demand_stdev**2 + (avg_demand**2) * (lead_time_stdev**2))


def reorder_point(avg_demand: float, lead_time_days: float, safety_stock: float) -> float:
    """ROP = average demand during lead time + safety stock."""
    return avg_demand * lead_time_days + safety_stock


def economic_order_quantity(annual_demand: float, order_cost: float, holding_cost: float) -> float:
    """EOQ = sqrt(2*D*S/H)."""
    if holding_cost <= 0:
        return 0.0
    return sqrt(2 * annual_demand * order_cost / holding_cost)


@dataclass
class StockingPolicy:
    sku: str
    service_level: float
    z: float
    avg_demand_per_day: float
    lead_time_days: float
    lead_time_stdev: float
    demand_stdev: float
    safety_stock: int
    reorder_point: int


def recommend_policy(sku: str, avg_demand_per_day: float, demand_stdev: float,
                     lead_time_days: float, lead_time_stdev: float = 0.0,
                     service_level: float = 0.95) -> StockingPolicy:
    """Compute a recommended safety stock + reorder point for one item.

    Uses the combined formula when lead time varies (the realistic case for long-lead purchased
    parts), otherwise the demand-variability-only formula.
    """
    z = z_for_service_level(service_level)
    if lead_time_stdev > 0:
        ss = safety_stock_combined(z, avg_demand_per_day, demand_stdev, lead_time_days, lead_time_stdev)
    else:
        ss = safety_stock_demand_variability(z, demand_stdev, lead_time_days)
    ss_i = int(round(ss))
    rop = reorder_point(avg_demand_per_day, lead_time_days, ss_i)
    return StockingPolicy(
        sku=sku, service_level=service_level, z=round(z, 3),
        avg_demand_per_day=avg_demand_per_day, lead_time_days=lead_time_days,
        lead_time_stdev=lead_time_stdev, demand_stdev=demand_stdev,
        safety_stock=ss_i, reorder_point=int(round(rop)),
    )
