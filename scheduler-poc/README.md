# `aps` — Integrated Production Scheduler

A working, tested in-house production scheduler for discrete (BOM-driven) manufacturing — built for
SlipBot-style build-to-order. It plans materials, schedules builds on finite capacity, **chooses how
to source each part** (supplier × freight, expediting only when it pays), answers rush-order quotes,
and recommends safety stock. Backed by the research in
[`../docs/production-scheduler-research.md`](../docs/production-scheduler-research.md).

## What it does

| Layer | Module | Purpose |
|---|---|---|
| **MRP** | `aps/mrp.py` | Multi-level BOM explosion + gross-to-net (on-hand, scheduled receipts, safety stock) + lead-time offsetting. Flags shortages. |
| **Scheduling** | `aps/scheduler.py` | OR-Tools CP-SAT: finite-capacity build stations, BOM precedence, **sourcing-mode choice**, lexicographic **on-time-first** then cheapest objective. |
| **Build times** | `aps/model.py` | Fixed per-product build duration (the production lead time once materials are on hand). |
| **Promising** | `aps/promising.py` | Rush-order quoting: achievable date, expedite premium, displaced orders, accept/decline (profit test). |
| **Safety stock** | `aps/safety_stock.py` | SS / reorder-point / EOQ from demand + lead-time variability. |
| **Routing** | `aps/model.py` (`Operation`) | Operation-level routings (setup + run/unit per station) as an alternative to fixed build time. |
| **Uncertainty** | `aps/uncertainty.py` | Safety time (percentile lead times), rolling-horizon replanning, Monte-Carlo service-level simulation. |
| **Objectives** | `aps/scheduler.py` (`ObjectiveWeights`) | Configurable cost vs on-time vs throughput weighting + `compare_objectives` what-if. |
| **Ingestion** | `aps/connectors/` | NetSuite (SuiteQL) + Google Drive → `PlanningInput`, transport-agnostic. |
| **Write-back** | `aps/connectors/writeback.py` | Schedule → NetSuite work-order/PO payloads + exceptions; dry-run by default. |
| **Report UI** | `aps/report.py` | Dependency-free HTML Gantt + promise dates + sourcing + exceptions. |
| **Orchestrator** | `run.py` | One CLI that runs the whole pipeline and prints a report. |

## Quick start

```bash
cd scheduler-poc
pip install -r requirements.txt        # ortools

python run.py                          # full report on the seed (SlipBot) dataset
python run.py --quote SLIPBOT-V3:2@45  # quote 2 SlipBots wanted by day 45
python run.py --service-level 0.97     # safety stock at 97% service level
python run.py --snapshot ns.json       # plan against a live NetSuite snapshot

# focused demos
python run_mrp.py        # MRP purchasing/build plan
python run_schedule.py   # finite-capacity schedule + sourcing
python run_quote.py      # three rush-order quotes
python run_report.py out.html   # HTML Gantt + exceptions report

# tests (no network, no pytest required)
for t in tests/test_*.py; do python "$t"; done
```

## The core idea: lead time is a decision variable

Each purchased part has a **menu of sourcing modes** (supplier × freight), each with its own landed
cost and lead time:

```
ALLOY-FRAME:  FrameCo-ocean  $900  84d
              FrameCo-air   $1300  21d   <- expedite
              FrameAlt-prem $1700  35d   <- alternate supplier
```

The scheduler picks exactly one mode per part (CP-SAT `add_exactly_one` over optional intervals) and
pays a premium **only when it's needed to hit a date** — because the objective is on-time first,
then cheapest. So:

- relaxed due date → cheapest (ocean),
- rush date → air/alternate (feasible-but-expensive),
- impossible date → minimal tardiness + the earliest achievable date is reported.

## Connecting live data

The connectors are **transport-agnostic** — they take an injected fetch function, so the same
mapping code works over the NetSuite REST/SuiteQL API (production, credential-driven) or via the
NetSuite MCP connector (an agent pulls a snapshot to JSON):

```python
from aps.connectors.netsuite import NetSuiteIngestor

def query(sql: str) -> list[dict]:
    ...  # POST to /services/rest/query/v1/suiteql (OAuth2) OR call the NetSuite MCP SuiteQL tool

pin = NetSuiteIngestor(query).build_planning_input()
```

> The NetSuite record/field internal IDs in `connectors/netsuite.py` come from research and **must be
> verified** against your account's REST metadata-catalog. Per research §9.3, NetSuite's per-vendor
> lead-time handling is limited, so we pull **raw per-vendor (cost, lead time)** rows and let our own
> optimizer choose — and we synthesize air/expedite alternatives for long-lead parts.

## Status & honest limitations

Built and tested across 5 iterations (20 tests passing). Known simplifications, by design:

- **Build time** is a fixed per-product duration, not operation-level routing (matches the chosen
  data model; finer routings can layer in without changing callers).
- One build task per (item, order) — quantity scales cost/material, not build count.
- Procurement is released as-early-as-needed; no holding-cost term yet (so JIT order release isn't
  rewarded).
- Work centers must be supplied to enable finite capacity; a NetSuite snapshot without routings
  schedules builds unconstrained until stations are added.
- Demand-rate inputs to safety stock are a horizon-average proxy; wire real forecast history for
  production.

See the research doc's confidence summary for what to verify before relying on any figure.
