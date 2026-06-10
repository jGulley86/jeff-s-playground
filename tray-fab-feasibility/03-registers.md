# Cumulative Registers (Loop 25 state)

## Issues Register

All 67 issues raised across the 25 loops, with final disposition. Full narrative in
`02-loop-log.md` (loop where each was raised/resolved).

| # | Issue | Disposition |
|---|---|---|
| I-01 | "Light Tray" ambiguity (106997 vs 107455) | Resolved L1 (Wood Tray = light family); confirm via H-1 |
| I-02 | Fab scope boundary (decks, DeckOver, lumber) | Resolved L1: coated steel handoff; DeckOver + lumber = assembly |
| I-03 | Takt undefined | Resolved L1: 1 heavy/day, 0.5 wood/day |
| I-04 | Tube cutting method | Resolved L2: buy laser-cut kits; revisit >50/mo |
| I-05 | No routings | Resolved L2 (plan §1) |
| I-06 | Weld content unquantified | Resolved via I-20/I-23 (L9): 1,450 weld-in, 39 lb, 16.5 hr |
| I-07 | No headcount model | Resolved L3 draft → L14 final: 5 FTE |
| I-08 | Weld code/quals undefined | Resolved L3: AWS D1.1 internal standard; H-2 confirm |
| I-09 | Wage basis | Resolved L3 (A-4) |
| I-10 | Footprint unknown | Resolved L4 → L13: 9,000 SF nominal / 7,500 min |
| I-11 | Crane strategy | Resolved L4: freestanding gantries + forklift; H-3 ceiling |
| I-12 | Landlord/hot-work permission | Closed into I-63 (L23); action lives as H-4 |
| I-13 | Inspection plan missing | Resolved L5 (plan §5) |
| I-14 | Weld fume controls | Resolved L5: source capture + IH survey to ACGIH TLV |
| I-15 | FA method for 15.5-ft weldment | Resolved L5: fixture-as-gauge + FARO rental |
| I-16 | Consumables unquantified | Resolved L6: $130/heavy, $10/leg |
| I-17 | No financial model | Resolved L6 skeleton → L12/L16/L17 final |
| I-18 | Powder outsource price unknown | Estimated L6 ($425 incl freight); H-5 quotes |
| I-19 | Drum/buffer/rope undefined | Resolved L7 → L10: fixture drum, 5-day kit buffer, kanban rope |
| I-20 | Weld inches placeholder | Resolved L9 (= I-23) |
| I-21 | Parts-list weight sum ≠ drawing total (9%) | Resolved L8: drawing governs; kit BoM governs cost |
| I-22 | No supplier wind-down plan | Resolved L8: overlap M1–M9 + frame agreement |
| I-23 | Joint-by-joint weld math | Resolved L9: 1,425→1,450 weld-in |
| I-24 | Note 14 all-around welds = cost driver | Converted to H-6 (engineering review); savings not banked |
| I-25 | Deposition basis unstated | Resolved L9: 9 lb/hr, 40% op factor |
| I-26 | Non-weld cycle times | Resolved L10: 2.6 ops-tech hr/unit |
| I-27 | 1/day on one fixture unproven | Resolved L10: paired weldout, 8.5 hr occupancy |
| I-28 | Wood-leg weld time guess | Resolved L10: 1.25 hr/leg |
| I-29 | Kit price = naive multiplier | Resolved L11 bottom-up ($1,360 + $447); H-7 quotes |
| I-30 | Scrap unmodeled | Resolved L11: 2%→0.5%, $26/unit yr-1 |
| I-31 | Wood steel weight unknown | Bounded L11 (A-7, handling only) |
| I-32 | No unit economics/breakeven | Resolved L12: contribution $2,166; breakeven 13/mo |
| I-33 | Loading factor unstated | Resolved L12: 1.35 |
| I-34 | Amortization policy | Resolved L12: 7-yr equip / 5-yr fixtures, $64K/yr |
| I-35 | Electrical demand | Resolved L13: 115 kVA, 250A feeder; H-8 |
| I-36 | Air & ventilation | Resolved L13: 100 CFM air; capture + 8,000 CFM ambient |
| I-37 | Floor/gantry loads | Resolved L13: 12 kip/leg; H-9 slab check |
| I-38 | Headcount vs load reconcile | Resolved L14: 445/490 hr, 5 FTE |
| I-39 | Hiring ramp/training | Resolved L14 (plan §10) |
| I-40 | Absenteeism/turnover | Resolved L14: 150 hr productive, 20% turnover budgeted |
| I-41 | Capex consolidation | Resolved L15: $504K |
| I-42 | Equipment leads vs timeline | Resolved L15: max 14 wk; 4 wk float |
| I-43 | New vs used policy | Resolved L15 |
| I-44 | ±30% sensitivity | Resolved L16 (plan §9 table) |
| I-45 | Cash curve | Resolved L16: −$610K trough M6; payback 3.1 yr / <2 yr growth |
| I-46 | Lease vs buy capex | Resolved L16: purchase base case; lease option to Jeff (H-10) |
| I-47 | Cost of quality | Resolved L17: $190 yr-1 → $95 steady per unit |
| I-48 | Heavy legs make-or-buy | Resolved L17: BUY (vendor $79.71 beats internal ≈$85) |
| I-49 | Powder logistics | Resolved L17: 2×/wk, 5/load, $72/unit freight folded in |
| I-50 | Fixed-cost coverage at −40% | Resolved L18: hibernation path; volume gate G-1 |
| I-51 | Reversibility | Resolved L18: ~$200K net capex at risk after resale; frame agreement return path |
| I-52 | Drum at 2× volume | Resolved L19: second shift, then tack jig ($30K re-add) |
| I-53 | Tube laser at 2× | Resolved L19: still buy kits; revisit >50/mo |
| I-54 | Powder capacity at 2× | Resolved L19: dual-source vendors at launch |
| I-55 | Lead single-point dependence | Resolved L20: documented system + CWI backstop + deputy |
| I-56 | Welder funnel thin | Resolved L20: 3-layer mitigation; worst case +6–8 wk, $35K |
| I-57 | Fixture lead-time slip | Resolved L21: dual-quote + in-house platen fallback (0.7/day) |
| I-58 | Gantry slip | Resolved L21: rental bridge ($2.2K/mo) |
| I-59 | FA distortion risk | Resolved L22: sequence/restraint + pre/post-powder measurement |
| I-60 | Disposition authority | Resolved L22: CWI (weld) + MRB-lite (dimensional) |
| I-61 | FA failure burns overlap window | Resolved L22: decision tree, $40K contingency |
| I-62 | Finish-booth permit block | Resolved L23: non-event — powder outsourced by design |
| I-63 | Hot-work occupancy at Oakbrook | Resolved L23: consent + fire-marshal path; flex-space fallback |
| I-64 | Gas storage limits | Resolved L23: manifold ≤3,000 SCF per NFPA 55 |
| I-65 | Steel +25% make exposure | Resolved L24: +$228/unit |
| I-66 | Steel +25% buy behavior | Resolved L24: vendor +$330–420; net favorable to make |
| I-67 | Kit contract structure | Resolved L24: index-priced, no margin-on-material |

## Assumptions Register

| # | Assumption | Basis |
|---|---|---|
| A-1 | Wood Tray 107455-R01 is the "Light Tray" family for the 10/mo plan | Supplied data package; 106997 appears superseded |
| A-2 | Fab handoff = coated, inspected steel; DeckOver paint and lumber decking are assembly scope | BoM placement of 101450 and lumber at tray level |
| A-3 | Cut-kit pricing ≈ 1.9× raw material | Cross-checked bottom-up in L11 (machine-rate build-up) |
| A-4 | Atlanta wages: welder $24–29, lead $38, ops tech $25; ×1.35 loading | 2025–26 metro postings; GA comp class 3365 |
| A-5 | Fab space at 1275 Oakbrook ≈ $10/SF loaded ($7.50 + $2.50 NNN) | Repo decision-analysis tool inputs |
| A-6 | Powder coat $425/heavy weldment incl. freight; $12/leg batch | $0.30–0.40/lb large-part market rate + handling premium |
| A-7 | Wood-tray steel ≈ 450 lb ± 30% | Member-by-member estimate; affects handling only |
| A-8 | Wood beams ≈ $185 ea purchased (price missing in NetSuite) | Tube length × market rate; ~$740/tray |

## Human Inputs Needed (only Jeff / the company can answer)

| # | Input | Why it matters |
|---|---|---|
| H-1 | Confirm Wood Tray = the 10/mo light family (vs 106997) | Scopes the second routing |
| H-2 | Engineering: confirm AWS D1.1 (or other code) intent for tray weldments | Quals, WPS, inspection acceptance |
| H-3 | Oakbrook clear height in proposed fab bay (≥18 ft needed) | Gantry selection |
| H-4 | Landlord consent for welding occupancy + insurance rider | Site decision, week-1 action |
| H-5 | Two real powder quotes for 16-ft/1,179-lb parts (+ second source) | $102K/yr line; vendor ovens may not fit |
| H-6 | Engineering review of drawing note 14 (all-around welds everywhere) | 15–20% arc-time upside, not banked |
| H-7 | Two real cut-kit quotes (tube + formed sheet) from Atlanta processors | Largest make-side cost ($437K/yr) |
| H-8 | Oakbrook spare electrical capacity (need ~250A at 480V) | Facility prep cost/schedule |
| H-9 | Slab thickness/condition in fab bay (gantry 12 kip point loads) | Foundation cost |
| H-10 | Purchase vs lease preference for the $504K capex | Cash trough −$610K vs −$280K |
| H-11 | Committed 24-month tray forecast tied to fleet plans | The volume gate G-1 — the decision hinge |
| H-12 | Staffing-agency read on Atlanta welder market depth (incl. 2nd shift) | R-7 |
| H-13 | Engineering: weldment-specific tolerance note (loosen non-interface dims) | Highest-leverage FA risk reducer |

## Volume gate

**G-1:** commit capital only with a credible 24-month forecast ≥ 18 heavy-equivalent
trays/month. Below 14/mo flat: use the should-cost model to renegotiate the purchased
weldment price (target $4,400–4,600) instead of building.
