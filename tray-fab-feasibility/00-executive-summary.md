# Executive Summary — In-House Tray Fabrication (Loop 50 + 100-simulation update)

**Recommendation: HYBRID, lean-staged configuration — proceed through three gates.**
Weld the Heavy Tray weldment (106900) and Wood Tray legs in-house from purchased
laser-cut tube and formed-sheet kits; outsource powder coat; keep buying steel decks,
heavy legs, wood-tray piece parts, and hardware. No cutting, forming, or coating
equipment at current volume.

**100-simulation update (2026-06-11, `07-capital-efficiency-simulation.md`):** Monte
Carlo across demand, quotes, hours, steel, wages, and failure modes retired the original
$504K equipment plan — it never won in 100 worlds. The winning configuration (**C,
lean-staged**) buys the same 22/mo capacity for **$268K** (modular fixture, 2-ton mobile
gantries, 2 pulse MIGs, trigger-based hiring) plus a **$75K pre-engineered upgrade kit
ordered only when demand sustains >20/mo**: median 5-yr NPV ≈ **$1.0M**, cash trough
≈ **−$430K**, payback ≈ 23 months, NPV-positive in 89% of worlds, lowest regret of any
strategy. Renegotiating with TEEMS (6–12% off, no build) remains the pre-priced floor —
100% safe, but a median ~$540K left on the table.

**The decision is the gates, not a forecast.** Three sequential commitments, each with
pre-written exit criteria and a capped downside:

| Gate | When | Proceed only if | Capital at risk if stopped |
|---|---|---|---|
| **G-1** | Now | 24-month committed forecast ≥ 18 heavy/mo; insurance read (H-16) acceptable; leadership attention available M0–M6 | ~$0 |
| **G-2** | ~M1 | Real kit + powder quotes give contribution ≥ $1,800/unit | ≈ $50K |
| **G-3** | ~M5 | 3 first articles pass quality AND measured hours ≤ 19/unit | ≈ $400K (net of resale) |

Fallback at any gate: renegotiate TEEMS to $4,800–5,000/weldment using this should-cost
model — a successful outcome, not a failure.

## What the evidence shows (NetSuite, drawings, market data — not assumptions)

- **Current buy price is $5,577.84** (PO10309, 5/19/26), single-sourced to TEEMS
  Fabrication. The R02→R03 revision opened at +12.4% and settled at +6.8% — with three
  revisions in four months, rev churn is a measured recurring tax.
- **Demand is real:** heavy-tray work orders run 21–22/month, scheduled through late July,
  with surge weeks of 10 and a 14-tray single-site batch (Denton). Wood tray has 3 work
  orders ever — the plan does not depend on it.
- **The buy path has a ceiling:** TEEMS's demonstrated throughput is ~24–26/month —
  parity with demand today. Growth forces a second-source qualification either way.
- **Lead time:** measured 3.0–6.5 weeks PO-to-receipt today vs. ~7–11 days in-house.

## The numbers (cash basis, Loop-49 audited)

| Metric | Value (configuration C) |
|---|---|
| Make variable cost / weldment | $3,352 (kits $2,035 + powder $425 + labor $667 + consumables/CoQ) |
| Contribution / weldment | **$2,226** |
| Net cash savings at 20/mo | **≈ +$185K/yr** (lower fixed base than the $504K plan) |
| Cash breakeven volume | ≈ 12–13 heavy/mo |
| Capex / cash trough | **$268K (+$75K trigger kit)** / median trough ≈ **−$430K** |
| 5-yr NPV (100 sims) | median **+$1.0M**, P10 −$8K, 89% of worlds positive |
| Median payback | ≈ 23 months |
| Team / space / SOP | **3.5 FTE day one (lead + 2 welders + contract CWI), triggers for the rest** · 6,500 SF (+3,000 reserved) at 1275 Oakbrook · month 7 |

Stated plainly: **at flat current volume this is roughly NPV-neutral — the project is
justified by the growth path, the vendor capacity wall, the rev-churn tax, and the
lead-time position.** That is why G-1 demands a committed forecast rather than treating
today's 22/month as sufficient.

## Top 5 risks & mitigations

1. **Structural liability moves in-house (R-11)** — broker review before G-1 ($15–25K/yr
   budgeted), serial-level traceability (welder/WPS/heat/lot — near zero cost), UT spot
   checks, PE design-margin memo, field-incident runbook (which today's vendor-welded
   fleet needs anyway).
2. **Kit quotes come back high** — G-2 floor ($1,800 contribution) catches it at ~$50K
   exposure; fallback is renegotiation armed with the model.
3. **Weld hours run over** — G-3 measures actual hours on first articles before the vendor
   winds down; staged response: overtime → 4th welder; survives +30% hours.
4. **Ramp or first-article failure** — TEEMS at full rate through M6, callable frame
   agreement after; 10-unit bridge stock during transition; platen fallback if the fixture
   slips.
5. **TEEMS reacts badly** — sequenced negotiation: they keep ~$320K/yr of deck/edge-guard
   work plus formed-kit first right; decks pre-quoted to kit processors as the hedge.

## Next 10 actions

1. Jeff: G-1 — commit or decline the 24-month volume view (H-11); everything sequences
   from this.
2. Insurance broker: product-liability delta for in-house structural welding (H-16).
3. Landlord + Gwinnett fire marshal: hot-work occupancy at Oakbrook (H-4), week 1.
4. RFQ cut kits + deck second-sourcing to two Atlanta processors (H-7); RFQ powder, two
   vendors, 16-ft parts (H-5) → feeds G-2.
5. Lock TEEMS R03 pricing on a 90-day blanket *before* any announcement, then hold the
   sequenced conversation (keep-scope offer + frame agreement).
6. Engineering: weld code confirmation (H-2), note-14 weld review (H-6), tolerance note
   (H-13), design-margin memo (H-14).
7. Verify Oakbrook bay: clear height, 480V spare capacity, slab (H-3/H-8/H-9).
8. Start fixture design in-house; dual-quote the build; pre-order steel at 60% design.
9. Post the fab-lead role; engage the contract CWI.
10. Decide purchase vs. lease for capex (H-10) once G-2 passes.

Full detail: `01-feasibility-plan.md` (12 sections) · `02-loop-log.md` +
`05-loop-log-26-50.md` (50 loops) · `03-registers.md` (104 issues, assumptions, human
inputs, gates) · `04-data-basis.md` (sources incl. PO/WO history) ·
`06-financial-model.md` (monthly cash, NPV/IRR, regret).
