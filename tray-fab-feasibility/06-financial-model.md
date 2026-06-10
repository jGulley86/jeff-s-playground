# Financial Model — Cash Basis (Loop 49 restated)

Method note: unit decisions (G-2 threshold, legs make-or-buy) use **unit contribution**
($5,577.84 buy − $3,352 variable = $2,226/unit). Annual and investment decisions use the
**full-payroll cash P&L** below — welders are salaried, so allocated-hour math overstates
annual savings (Loop 49 audit finding I-104). All inputs dated and sourced in
`04-data-basis.md`.

## 1. Steady-state annual P&L at plan volume (20 heavy + 10 wood/mo)

| Line | $K/yr | Basis |
|---|---|---|
| Avoided buy — heavy weldments 240 × $5,577.84 | +1,339 | PO10309, 5/19/2026 |
| Avoided buy — wood legs 720 × $122.71 | +88 | PO10120 |
| Cut kits — heavy 240 × $2,035 | −488 | A-9 market build-up; G-2 confirms |
| Cut kits — wood legs 720 × $48 | −35 | scaled estimate |
| Powder coat (incl. freight) | −111 | A-6; H-5 confirms |
| Consumables (wire/gas/abrasives, VMI) | −38 | deposition math |
| Payroll, full (3 welders, lead, ops tech, ×1.35 loaded) | −396 | A-4, market-validated |
| Facility 9,000 SF + utilities | −150 | A-5 (Oakbrook $10/SF loaded) |
| Maintenance / calibration / PPE | −20 | PM program, Loop 37 |
| Product-liability insurance delta | −20 | H-16 placeholder midpoint |
| NDT spot checks, requals, CoQ extras | −15 | Loops 38/40 |
| **Net cash savings, steady state** | **≈ +155** | yr-1 ≈ +120 |

Capex **$504K** is separate (below). Equipment amortization is excluded here (non-cash);
it appears only in book-cost-per-tray reporting.

## 2. Volume scenarios (cash basis, payroll stepped to volume)

| Heavy volume | Staffing | Net $K/yr |
|---|---|---|
| 12/mo (−40%) | 2 welders + lead + 0.5 ops, 7,500 SF | ≈ −10 |
| 14/mo (−30%) | 2 welders + OT | ≈ −15 to +10 |
| 16/mo | 2 welders + OT | ≈ +60 |
| **20/mo (plan)** | 3 + lead + ops | **≈ +155** |
| 26/mo (+30%) | 3 + OT / 4th welder | ≈ +230 |
| 30/mo | 4–5 welders | ≈ +270 |
| 40/mo (2×, two shifts) | 6 welders + 1.5 lead + 2 ops | ≈ +525 |
| Steel +25% | any | make advantage widens ~$550/unit vs. buy (vendor passes material + margin; kits indexed without margin-on-material) |

**Cash breakeven volume ≈ 15 heavy/mo.** Gate G-1 (18/mo) sits between breakeven and
demonstrated demand (21–22/mo) with margin on both sides.

## 3. Monthly cash curve (flat 20/mo case, $K, rounded)

| Month | Capex | Opex (payroll+facility+misc) | Production margin¹ | WC release | Net | Cumulative |
|---|---|---|---|---|---|---|
| M0 | 0 | 0 | 0 | — | 0 | 0 |
| M1 | −80 | −2 | 0 | — | −82 | −82 |
| M2 | −100 | −22 | 0 | — | −122 | −204 |
| M3 | −120 | −44 | 0 | — | −164 | −368 |
| M4 | −120 | −48 | 0 | — | −168 | −536 |
| M5 | −84 | −55² | 0 | — | −139 | −675 |
| M6 | 0 | −47 | +30 (10 units) | — | −17 | −692 |
| M7 (SOP) | 0 | −47 | +60 (20 units) | — | +13 | −679 |
| M8 | 0 | −47 | +60 | +100 | +113 | −566 |
| M9–M12 | 0 | −47/mo | +60/mo | — | +13/mo | −514 at M12 |
| M13–M24 flat | 0 | −47/mo | +60/mo | — | +13/mo | −358 at M24 |
| M13–M24 growth (30/mo) | −45³ | −56/mo | +90/mo | — | ~+23/mo avg | −250 at M24 |

¹ Production margin = in-house units × (avoided buy − kits − powder − consumables) =
units × $2,988; payroll/facility are in the opex column. Vendor purchases continue for all
units not yet made in-house (M1–M6), so no savings accrue on them.
² Includes CWI program, welder quals, and 3 qualification-build kit-sets.
³ Tack jig + station adds at the growth trigger.

**Cash trough ≈ −$700K (M6–M7).** Cumulative cash breakeven ≈ **M38 flat / ≈ M25 growth**.
Optional equipment lease (~8.5% money factor) flattens the trough to ≈ −$380K for
+$11K/yr (H-10).

## 4. NPV / IRR (5-year, cash basis)

| Case | Year-1 net | Years 2–5 | NPV @10% | NPV @20% | IRR |
|---|---|---|---|---|---|
| Flat 20/mo | −$520K (incl. WC release) | +$155K/yr | **≈ −$30K** | ≈ −$250K | ≈ 9% |
| Growth (30/mo from M13) | −$520K | +$270K/yr | **≈ +$310K** | ≈ +$150K | ≈ 22% |
| 2× by year 3 | −$520K | +$270K → +$525K | ≈ +$700K | ≈ +$390K | ≈ 30% |

Read plainly: **flat-forever does not clear a venture hurdle rate; the growth path does,
comfortably.** That is why G-1 demands the 24-month volume commitment rather than treating
current demand as sufficient.

## 5. Regret analysis (what each gate protects)

| Exit point | Capital consumed | Recoverable | Max regret |
|---|---|---|---|
| Stop at G-2 (quotes bad, ~M1) | ~$80K design/deposits | ~$30K | **≈ −$50K** |
| Stop at G-3 (FA/hours fail, ~M5–6) | ~$690K | ~$290K (equipment resale ~60%, WC) | **≈ −$400K** |
| No gates, discover at M12 | ~$700K+ | ~$250K | ≈ −$450 to −700K |

The gate structure converts one $700K bet into a $50K bet, then a $350K increment — each
with pre-written exit criteria (plan §10).

## 6. Working capital

Buy pipeline today: ~5 weeks × 5/wk × $5,578 ≈ $140K in open-PO/in-transit weldments.
Make loop: 7 kit-sets ($14K) + ~8 units WIP/post-weld ($22K) + consumables ($4K) ≈ $40K.
One-time release ≈ **+$100K** at M8, included above. Temporary additions during transition:
10-unit finished-weldment safety stock (≈$56K, M1–M9 only, sunset owned by the fab lead).
