# SlipLift Production Scheduler

A self-contained, finite-capacity production scheduling tool for SlipLift assembly.
Everything — data, scheduling engine, and UI — lives in a single `index.html` with no
external dependencies, so it can be hosted anywhere and embedded directly in the MES.

## What it does

- **Finite-capacity scheduling.** Every SlipLift in the weekly build plan expands into its
  118 MBOM operations (bench subassembly ops run in parallel across bench seats; main-line
  ops run in sequence per robot across stations). Trays, recurring base load (field parts,
  QC rework, ECO retrofits), and discrete work chunks (MeLi bins, battery refurb, Slip Mini, …)
  compete for the same technician pool. Dispatching is earliest-due-date.
- **Calendar-aware.** Weekends and holidays are skipped; PTO is pro-rated; MBOM touch times
  are divided by the labor-efficiency factor; workdays are shrunk by direct-labor utilization.
  The math reproduces the tops-down headcount workbook exactly (673.2 effective hrs/head,
  91.6 h per SlipLift at 80 % efficiency).
- **Bottleneck alerts.** Flags capacity shortfalls (heads), main-line station rate limits,
  bench-seat rate limits, late units, and the 26-tray forecast gap.
- **Technician assignment.** A named roster with roles (Any / Bench / Line / Support); the
  dispatcher assigns every task to a specific eligible technician round-robin. The Technicians
  tab shows per-tech utilization, an hours-per-tech-per-week load board, a who-does-what week
  detail, and a task-level assignments CSV export.
- **Fully editable.** Build plan (including a bulk set/add/scale editor across any week range),
  operations, roster, workforce, calendar, recurring load, and work chunks are all editable in
  the UI; the schedule recomputes live (~150 ms). Edits persist in the browser (localStorage),
  and scenarios can be shared via JSON export/import.
- **MES hand-off.** `Export schedule CSV` produces a dispatch list (unit, bench start, line
  start, completion, on-time status) plus the weekly load/capacity table.

## Data sources (seeded into the file)

| Source | What was taken |
|---|---|
| `mbom_tree_260805_1436_ET_edited.xlsx` › `operations_all` | 118 operations, touch minutes per robot, Bench/Main split, sequence |
| `BOY_Manufacturing_Headcount_TopsDown.xlsx` (Jeff, 8/4/2026) | Horizon (22 wks from 8/3), 10 techs, 85 % utilization, holidays, PTO, tray hours, recurring load, work chunks, forecast gap |
| Demand forecast summary (via headcount workbook) | 42 SlipLifts (3/wk tapering to 2/wk), 75 heavy trays (~10/wk through wk of 9/21) |

The weekly SlipLift/tray split is a seeded assumption — adjust it to the live forecast in the
Build Plan tab. The SharePoint demand-forecast file wasn't reachable from this environment;
when the real weekly numbers differ, type them in or import them via JSON.

## Deploying / embedding in the MES

1. Host `index.html` on anything that serves static files (internal web server, SharePoint
   page, or the MES's web-content widget).
2. Embed with `<iframe src="https://your-host/production-scheduler/index.html" style="width:100%;height:100%;border:0">`.
3. State is per-browser (localStorage). To share a scenario, use **Export data JSON** →
   **Import data JSON**.

## Updating for a new MBOM revision

Edit operations in the Operations tab, or regenerate the `SEED_OPS` block in `index.html`
from a fresh `operations_all` export (columns: phase, seq, name, min/each, min/robot, qty,
type M/B) and reload with **Reset to seed data**.

## Engine model, in brief

- Time unit: *effective minutes* — `hours/day × utilization × PTO-factor` per tech-day.
- Task duration: MBOM minutes ÷ labor efficiency (trays/recurring/chunks use their planning
  hours as-is).
- Resources: technician pool, main-line stations (1 robot each, ops serial per robot),
  bench seats. A configurable WIP lead time (default 2 weeks) models work already in flight
  before week 1.
- Constraint: bench subassemblies for a robot must finish before its line install starts
  (toggle in Assumptions).
