# Supply & Demand Planner (SlipOS mock)

Rebuild of the `/mocks/demand-planner` page. The old mock ("Robot Availability", kept in
`legacy/`) was a sales-only calculator over hard-coded spreadsheet outputs. This version
is one page that Sales, Production, Supply Chain and leadership can all work from, built
to what was asked for in the 2026-09-03 mock review, Jeff's 8/4 vision page, and the
Demand Planner PRD (2026-08-05).

## What changed and why

| Complaint / requirement | What the page now does |
| --- | --- |
| Too many screens; need one calendar view like the spreadsheet | One grid: every deployment as a pill on its week, then per product **Build plan → Deployable inventory**, with month rollups underneath. Sticky first column, horizontal scroll, "now" column highlighted. |
| Sales: "I need X lifts + Y trays — when?" then reserve it | Ask panel at the top. Forward (quantity → earliest go-live week) and reverse (date → biggest configuration). **Place soft hold** puts the deal on the calendar as a proposed soft hold; **Copy customer promise** gives the rep the text. |
| Levels of "locked in" in one visual language | Five typed stages, one hue, decreasing solidity: PO in hand (solid) → Contract signed → Negotiation (dashed) → Soft hold (dotted) → Early estimate (faint, never counted). |
| Soft commitments that flag collisions so Sales picks | Soft holds count in coverage (toggle). When hard + negotiation demand is covered but holds push a product negative, a **collision** signal names the competing holds and hands the decision to Sales. |
| Reps promising the same robots | Holds land in a **review queue** (Planner accepts / amends / rejects) and are visible to everyone on the grid immediately. |
| Turned-away demand evaporates in hallway conversations | **Demand-gap log**: when the offered date is later than the customer needs (or nothing is promisable), the rep logs it in one click. |
| Production keys actuals; plan-vs-actual visible | Supply detail rows (actuals, returns/catch-up) per week. Past weeks show actual/plan when they differ. Plan-vs-actual for the last 4 weeks in the governance card. "Mark supply inputs keyed" stamps freshness. |
| Supply chain: when do we buy? | **Material release** signal: contract/PO deployments inside the material lead time that haven't been released, with a one-click release. |
| Governance: named versions, Jeff approves, typed reasons, off-cycle flagged and counted | Editing any future build cell creates a **draft**. Approval requires the six things Jeff listed (delta preview, consensus number, coverage with buffer state, capacity signal green/acknowledged, plan-vs-actual, typed reason) and is **blocked** when supply inputs are older than 7 days or a capacity red is unacknowledged. Approving mints `P-YYYY-MM-DD` (`-OC` when off-cycle), records what it supersedes, and writes the ledger. Off-cycle approvals this quarter are counted; three triggers a constraint review. |
| Negative cells were the only alarm | **Signals** each carry an owner: shortfall (Manufacturing), collision (Sales), over-capacity (Leadership, needs ack), cap breach (Finance), stale supply inputs, review queue (Planner), material release (Supply Chain), missing actuals. |
| Weekly cadence lives in people's heads | Cadence strip (Mon demand refresh → Tue supply check → Wed consensus → Thu publish) highlights today. **Copy weekly pack** produces the Thursday publication text. |

## The model (one week convention)

```
ending[t] = ending[t-1] + build[t] + adjust[t] − demand[t]
build[t]  = keyed actual for past weeks, else the plan (draft if one exists)
demand[t] = deployments at t whose stage is counted (PO, contract, negotiation, soft — toggles)
ATP[w]    = min over t ∈ [w, w+protect] of ending[t]  − buffer, ignoring weeks already < 0
```

"Build" means units completing (deployable) in that week. Weeks that are already negative
are an existing shortfall owned by the plan owner; they do not block a promise, they make it
**conditional** (the answer says by how much it deepens the gap). Nothing is promisable in a
week whose balance is itself negative.

## Data

Seeded from the *Demand Forecast and Fulfillment Confirmation* workbook (2026 Demand
Forecast sheet, plan as of week of Jun 29, 2026). Everything is editable in the UI. State
autosaves to the browser (`localStorage`) and can be exported/imported as JSON from
**Assumptions & data**. **Reset to seed** restores the workbook numbers.

Because the seed plan is from June and today is September, the page opens with real
signals: heavy trays go −10 in late December, light trays −14 from October (no light-tray
builds planned), finished goods break the $1M cap in November, supply inputs are stale.
Those are the workbook's facts, not bugs.

## Files

- `SupplyDemandPlanner.jsx` — the component. Same shape as the old mock (default export,
  imports `react` and `recharts`), so it drops into the SlipOS mocks route unchanged.
- `standalone.html` — self-contained build (React + Recharts inlined). Open it in a browser.
- `build.mjs`, `package.json` — `npm install && npm run build` regenerates `standalone.html`.
- `legacy/RobotInventory_v1.jsx` — the previous mock, for reference.

## Deliberately not built

CRM sync, MES/WMS actuals, MRP and named ramp scenarios are deferred by the PRD to later
phases; the deployment record already carries the fields they will populate (`source`,
`materialReleased`, actuals per week). Site-readiness checklists live in the Deployment
Manager and are represented here only as the lead-time parameter.
