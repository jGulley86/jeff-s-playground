# SlipLift Production Scheduler

A self-contained, finite-capacity production scheduling tool for SlipLift assembly.
Everything — data, scheduling engine, and UI — lives in a single `index.html` with no
external dependencies, so it can be hosted anywhere and embedded directly in the MES.

## What it does

- **Finite-capacity scheduling.** Every SlipLift in the weekly build plan expands into its
  118 MBOM operations. Bench subassembly ops run in parallel across bench seats; main-line
  ops follow the MBOM **dependency graph** — ops not ordered by a precedence rule may run in
  parallel on the same robot up to a crew limit (default 2 techs/robot), and the robot holds
  its station from first op to last (a serial one-op-at-a-time mode is a toggle). Trays,
  recurring base load (field parts, QC rework, ECO retrofits), and discrete work chunks
  (MeLi bins, battery refurb, Slip Mini, …) compete for the same technician pool.
  Dispatching is earliest-due-date. Dependency rules are editable in the Operations tab
  (with cycle protection).
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
- **Work-in-progress tracking.** In-flight units carry their exact remaining planned hours
  from NetSuite work orders (seeded from the Master Production Plan's Weekly Capacity sheet,
  8/7/2026) and replace fresh units of their orders. Refresh by pasting rows from the
  `Weekly Capacity` or `Work Orders` sheet — the importer auto-detects either format,
  aggregates op rows per unit, and matches customers to orders.
- **Scenario planner.** What-if levers (hires by line, OT, Saturday hours, stations, bench
  seats, crew size, utilization override) rerun the full schedule without touching the saved
  plan and show baseline-vs-scenario deltas per order. A "find minimal hires" solver locates
  the smallest flexible-hire count that clears every due date and prices it against 1.5×
  overtime at the loaded labor rate; a preset applies the measured ~51% actual-pace utilization.
- **MES hand-off.** `Export schedule CSV` produces a dispatch list (unit, order, due date,
  bench start, line start, completion, on-time status) plus the weekly load/capacity table.
- **Seed-version banner.** When the embedded seed data is updated, saved browser states get a
  one-click "Load latest seed / Keep my edits" banner instead of silently going stale.

## Data sources (seeded into the file)

| Source | What was taken |
|---|---|
| `mbom_tree_260805_1436_ET_edited_1.xlsx` › `operations_all`, `dependencies` | 118 operations, touch minutes per robot, Bench/Main split, sequence, 21 main-line precedence rules |
| `BOY_Manufacturing_Headcount_TopsDown_v2.xlsx` (forecast rev 8/5/2026) | Horizon (22 wks from 8/3), holidays, PTO, tray hours, recurring load, light-tray gap |
| `Master_Production_Plan_Updated_1.xlsx` (as of 8/7/2026) | Customer orders (Home Depot, Corning, SpaceX, Mercado Libre) with handoff dates and NetSuite work-order % complete; 4 SlipLift / 3 Heavy Tray line split; 7 h + 1 h OT days; bin hours (40); special-project windows (Strip v3, 52V battery, Rebuild 3x bots, Slip Minibot) |
| 8/5 demand forecast rev (via v2 workbook §2/§7) | 42 SlipLifts, 45 heavy trays, 60 light trays — seeded as orders + build-to-stock remainder |

Demand is two-layered like the Master Production Plan: **customer orders** carry hard handoff
dates and progress-adjusted remaining work; the **weekly build plan** is build-to-stock on top,
seeded as the forecast minus order units so totals are preserved.

The tool's 85 % utilization covers meetings/5S/breaks only, because rework, chunks, and field
work are scheduled explicitly — it corresponds to the v2 workbook's "60 % build-only
utilization" convention, where that support work is folded into the other 40 %. The SharePoint
demand-forecast file wasn't reachable from this environment; when the live weekly numbers
differ, type them in (or bulk-edit) in the Build Plan tab, or import via JSON.

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
