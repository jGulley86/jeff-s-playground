# Integrated Production Scheduler — Proof of Concept

A small, runnable demonstration of the genuinely novel part of the system described in
[`../docs/production-scheduler-research.md`](../docs/production-scheduler-research.md): a
**finite-capacity production schedule that chooses how to source each raw material** (which
supplier / freight mode), trading off **material + freight/expedite cost against tardiness
penalties**, using Google OR-Tools CP-SAT.

It implements the model from **§7.5 (objective) + §7.7 (CP-SAT alternative-interval pattern)** and
shows the three behaviors you asked about:

1. **Standard sourcing** — cheapest supplier/ocean freight when the due date is comfortable.
2. **Feasible-but-expensive** — when a customer wants it faster, the solver *chooses* to pay an air
   freight premium or a more expensive alternate supplier because that's cheaper than the tardiness
   penalty.
3. **Genuinely infeasible** — single backlogged supplier, no faster mode, due date physically
   unreachable → the model reports it can't hit the date and quotes the earliest it *can*.

> This is a teaching/scoping PoC, not production code. Time is modeled in **days** as integers.
> Data is hard-coded in `data.py`. There is no NetSuite connection here — see §9 of the research
> doc for the extraction layer that would feed `data.py`.

## What it models

- **Jobs** (customer orders): each has a quantity, a due date, and a per-day tardiness penalty
  (`weight`), plus a revenue figure so you can see profit.
- **Operations**: each job routes through one or more **work centers**; operations are sequential
  (precedence) and a work center does one operation at a time (`NoOverlap` = finite capacity).
- **Materials**: each job consumes raw materials. Each material has several **sourcing modes**
  (supplier × freight), each with a `cost_per_unit`, a `lead_time_days`, and a capacity limit.
- **The coupling**: a job's first operation cannot start until its materials have arrived. The
  chosen sourcing mode's lead time sets that material-available date — so picking air freight lets
  production start sooner, at higher cost.

## Objective (matches §7.5 of the research doc)

```
minimize   Σ material cost (qty × chosen mode cost_per_unit)
         + Σ freight/expedite premium (baked into mode cost)
         + Σ weightⱼ × tardinessⱼ
```

Exactly one sourcing mode is chosen per (job, material) via `add_exactly_one`. The material-available
date is wired to the job's start. The solver pays a premium only when it beats the tardiness penalty.

## Run it

```bash
cd scheduler-poc
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scheduler.py
```

You'll see three scenarios printed back-to-back (comfortable due date, rush date, impossible date)
with the chosen sourcing mode per material, the schedule, the cost breakdown, and the
promise-date verdict.

## Files

- `data.py` — the sample problem (work centers, jobs, operations, materials, sourcing modes,
  scenarios). Edit this to model your own shop.
- `scheduler.py` — the CP-SAT model + solver + a readable report. This is the load-bearing file.
- `requirements.txt` — just `ortools`.

## Where this slots into the full system

This PoC is step 3–4 of the build sequence in §5 of the research doc. In production you would:

- Replace `data.py` with a **SuiteQL extract** from NetSuite (§9) → items, BOMs, routings, work
  centers, inventory, open POs, and **per-vendor lead time + cost** (which you must pull yourself —
  see §9.3).
- Add **MRP gross-to-net + multi-level BOM explosion** (§4) upstream to turn finished-good demand
  into the per-material requirements this model consumes.
- Wrap the solver in the **sandbox "test plan"** pattern (§8.2) for live rush-order quoting.
