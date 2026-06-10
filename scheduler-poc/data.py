"""Sample problem data for the integrated-scheduler proof of concept.

Everything here is hard-coded for demonstration. In production this module would be replaced by a
SuiteQL extract from NetSuite (see section 9 of ../docs/production-scheduler-research.md) feeding the
same dataclasses.

Time unit: integer DAYS. Day 0 = "today" (the planning start).
Money unit: dollars (integers, to keep CP-SAT in integer arithmetic).
"""

from dataclasses import dataclass, field


# --------------------------------------------------------------------------------------------------
# Master data
# --------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class WorkCenter:
    name: str
    # capacity = number of jobs that can run in parallel. 1 = a single machine (NoOverlap).
    capacity: int = 1


@dataclass(frozen=True)
class SourcingMode:
    """One way to buy one material: a (supplier, freight) option.

    This is the §7.1 'lead time is a decision variable' idea: the same material has several modes,
    each with its own cost and lead time. The solver picks exactly one per (job, material).
    """
    label: str            # e.g. "VendorA-ocean"
    cost_per_unit: int    # dollars/unit, INCLUDING freight/expedite premium baked in
    lead_time_days: int   # days from order to material-on-hand
    max_qty: int          # supplier capacity ceiling for this mode (units available to us)


@dataclass(frozen=True)
class Material:
    name: str
    modes: tuple[SourcingMode, ...]   # the sourcing menu for this material


@dataclass(frozen=True)
class Operation:
    work_center: str   # which work center this operation runs on
    duration: int      # processing days (already = setup + run*qty, pre-computed)


@dataclass
class Job:
    """A customer order to build something."""
    name: str
    due_date: int                      # day the customer wants it
    tardiness_penalty_per_day: int     # $/day late (the §7.5 wⱼ; also models lost-goodwill cost)
    revenue: int                       # order value, for profit reporting
    operations: list[Operation]        # sequential routing (op[i] before op[i+1])
    # materials this job consumes: {Material: quantity_required}
    materials: dict[str, int] = field(default_factory=dict)


# --------------------------------------------------------------------------------------------------
# The shop: two work centers, each a single machine.
# --------------------------------------------------------------------------------------------------

WORK_CENTERS = {
    "MACHINING": WorkCenter("MACHINING", capacity=1),
    "ASSEMBLY":  WorkCenter("ASSEMBLY",  capacity=1),
}


# --------------------------------------------------------------------------------------------------
# Materials and their sourcing menus.
#
# ALLOY_X is the interesting one: a long-lead specialty raw material. It has
#   - VendorA-ocean : cheap, slow (84 d)
#   - VendorA-air   : same supplier, air freight: pricier, much faster (21 d)
#   - VendorB-prem  : alternate supplier, expensive, medium lead (35 d), LIMITED capacity
# FASTENERS is a commodity: always on hand effectively (lead time 2 d, one cheap mode).
# --------------------------------------------------------------------------------------------------

MATERIALS = {
    "ALLOY_X": Material(
        name="ALLOY_X",
        modes=(
            SourcingMode("VendorA-ocean", cost_per_unit=100, lead_time_days=84, max_qty=500),
            SourcingMode("VendorA-air",   cost_per_unit=140, lead_time_days=21, max_qty=500),
            SourcingMode("VendorB-prem",  cost_per_unit=185, lead_time_days=35, max_qty=80),
        ),
    ),
    "FASTENERS": Material(
        name="FASTENERS",
        modes=(
            SourcingMode("Local-stock", cost_per_unit=2, lead_time_days=2, max_qty=100000),
        ),
    ),
}


# --------------------------------------------------------------------------------------------------
# Scenarios. Each is a list of jobs to schedule. The horizon bounds the planning window (days).
#
# We deliberately reuse the same physical job (a "Widget" needing 50 units of ALLOY_X) at three
# different due dates to show the three behaviors from the research doc §7.6.
# --------------------------------------------------------------------------------------------------

def _widget(name: str, due_date: int) -> Job:
    return Job(
        name=name,
        due_date=due_date,
        tardiness_penalty_per_day=500,   # $500/day late — steep enough to justify expediting
        revenue=40000,
        operations=[
            Operation("MACHINING", duration=10),
            Operation("ASSEMBLY",  duration=5),
        ],
        materials={"ALLOY_X": 50, "FASTENERS": 200},
    )


@dataclass
class Scenario:
    title: str
    description: str
    horizon: int
    jobs: list[Job]


SCENARIOS = [
    Scenario(
        title="1. Comfortable due date",
        description=(
            "Customer wants the Widget in 120 days. There is plenty of slack, so the model should "
            "pick the CHEAPEST sourcing (VendorA-ocean @ $100, 84-day lead) and still finish on time."
        ),
        horizon=200,
        jobs=[_widget("Widget-Comfortable", due_date=120)],
    ),
    Scenario(
        title="2. Rush date (feasible but expensive)",
        description=(
            "Customer wants the SAME Widget in 45 days. Ocean (84 d) can't make it. The model should "
            "CHOOSE to pay a premium — air freight (21 d, +$40/unit) or VendorB (35 d) — because the "
            "premium is cheaper than 39 days of tardiness penalty. This is the 'yes, but it costs "
            "more' quote."
        ),
        horizon=200,
        jobs=[_widget("Widget-Rush", due_date=45)],
    ),
    Scenario(
        title="3. Impossible date (genuinely infeasible on time)",
        description=(
            "Customer wants the Widget in 20 days. The fastest material option is air freight at "
            "21 days, then 15 days of production on top. No combination hits 20 days. The model "
            "still returns the CHEAPEST-total plan and reports the earliest achievable date and the "
            "unavoidable tardiness — i.e. 'no, the earliest I can do is day N'."
        ),
        horizon=200,
        jobs=[_widget("Widget-Impossible", due_date=20)],
    ),
]
