# In-House Tray Fabrication Feasibility — Standing Plan (Loop 25 state)

Slip Robotics steel tray fabrication, evaluated 2026-06-10. Volumes: **20 Heavy Trays
(106901-R02) + 10 Wood/Light Trays (107455-R01) per month**. Scope: fabrication only —
receiving, cutting, forming, welding, surface prep/coating, fab QA. Assembly excluded.
All sources in `04-data-basis.md`; derivations in `02-loop-log.md`; open items in
`03-registers.md`.

**Architecture decided (hybrid):** buy laser-cut tube kits and formed-sheet kits; weld
the heavy weldment (106900) and wood-tray leg weldments (107508) in-house; outsource
powder coat; keep buying steel decks, heavy legs (106911), and all wood-tray steel piece
parts. Sections below describe that plan.

---

## 1. Process flow & routing

**Heavy Tray weldment (1/working day):**

| Op | Step | Resource | Time (hr) |
|---|---|---|---|
| 10 | Receive kit-set (tube kit + plate kit, batch of 5), MTR + count + 5-pt dim check | Ops tech | 0.8/unit |
| 20 | Stage kit at cell; fixture load | Welder pair + gantry | 0.6 |
| 30 | Fit & tack in fixture (quarter-symmetric sequence) | Welder pair | 2.25 elapsed (4.5 labor) |
| 40 | Weldout, paired both sides, pulse-MIG ER70S-6, 0.25" fillets (~1,450 weld-in, ~39 lb deposited) | Welder pair | ~6.0 elapsed (10.8 labor) |
| 50 | Unload; straighten as needed; 100% visual per D1.1 + fillet gauge; traveler | Welder + lead | 1.2 |
| 60 | Stage for powder; ship 2×/wk, 5/load | Ops tech | 0.25 |
| 70 | Outsourced powder coat RAL 9003 (incl. vendor prep/blast) | Vendor | ≤5 working days TAT |
| 80 | Receive; coating thickness + final interface go/no-go on gauge points; handoff to assembly | Ops tech | 0.7 |

Weld-department content: **16.5 labor-hr/unit**. Fixture occupancy ≈ 8.5 hr/day → 1/day with slack.

**Wood Tray (steel scope, 0.5/day):** legs (6/tray) welded in-house on a small fixture —
1.25 hr/leg including handling; batch-powdered with heavy loads. Beams, brackets, plates,
bent sheets remain purchased; lumber decking is assembly scope.

## 2. Equipment list

| Item | Spec | Qty | New/Used | Cost | Lead | Footprint / utilities |
|---|---|---|---|---|---|---|
| Heavy weldment fixture | 16-ft certified fixture, hydraulic clamps, Slip-owned design | 1 | New build | $85K | 10–14 wk | 20×8 ft |
| Leg/small fixtures | Wood-leg + spares | 1 set | New | $18K | 6 wk | 8×4 ft |
| Tack jig (added at 2× volume only) | Pre-stage jig | (1) | New | ($30K) | 8 wk | deferred |
| Pulse MIG welders | 450A class, .045 wire | 4 (3+1 spare) | New | $38K | stock | 22 kVA peak ea |
| Fume extraction | 3 source-capture arms 1,000 CFM + ambient roof fan 8,000 CFM | 1 sys | New | $58K | 8 wk | 15 kVA |
| Gantry cranes | Freestanding 5-ton, 2 runs over weld cells | 2 | Used/refurb | $88K | 8–10 wk | 10 kVA |
| Tilt/rotate weldment cart | 2-ton positioner cart | 1 | New | $14K | 6 wk | — |
| Weld tables/platens | Certified platens (also fixture fallback) | 2 | Used | $32K | 4 wk | — |
| QA | Fillet gauges, fixture laser-tracker cert, FARO rental mo 4–6 | — | — | $27K | — | — |
| Facility prep | 480V/250A feeder + drops, air piping, 25 HP compressor, lighting, screens, cantilever racks | — | — | $78K | 6–8 wk | — |
| Install/rigging/contingency | 15% | — | — | $66K | — | — |
| **Total capex** | | | | **$504K** | max 14 wk | |

Deleted along the way (and why): tube laser & flat laser & press brake (kits cheaper at
this volume), bridge crane (gantries avoid landlord/structural work), blast cabinet
(powder vendor preps), FARO purchase (rent for FA; fixture is the gauge), in-house powder
line (largest permit/capex risk for the least savings).

## 3. Staffing plan

| Role | Shift 1 | Wage (Atlanta, A-4) | Loaded (×1.35) | Notes |
|---|---|---|---|---|
| Fab lead (working) | 1 | $38/hr | $107K/yr | Hire month 2; welds ~25%; owns travelers, sequence, quals |
| Welder-fabricators | 3 | $24–29/hr ($26 avg) | $219K/yr | Hire-for-fitup, qualify internally to AWS D1.1 (fillet + 1/8" wall tube); months 3–5 |
| Fab ops tech | 1 | $25/hr | $70K/yr | Kitting, receiving, inspection support, powder logistics |
| **Total** | **5 FTE** | | **$396K/yr** | Supervision ratio 1:4; contract CWI for WPS/PQR/quals (~$15K setup, then monthly visits) |

Capacity: 3 welders × 150 productive hr/mo + lead 40 hr = 490 hr vs. load 445 hr (91%).
Surge = overtime, then contract welders (1.45×). Turnover assumption 20%/yr; standing
requisition + quarterly coupon-test pipeline. Second shift (+3 welders, +0.5 lead) only
at the 2× volume trigger.

## 4. Facility requirements

Location: within **1275 Oakbrook Drive (43,790 SF; $7.50 base + $2.50 NNN)** — 9,000 SF
nominal / 7,500 SF minimum, fallback to nearby flex space if landlord declines hot work.

| Function | SF |
|---|---|
| Receiving + raw/kit storage (cantilever racks, 5-kit batches) | 1,500 |
| Kitting/staging | 500 |
| Heavy weld cells (2 bays, gantry-covered) | 1,600 |
| Small-weldment (leg) cell | 400 |
| Inspection/straightening (doubles as rework) | 600 |
| Powder out/in staging at dock | 800 |
| WIP buffer (post-weld, pre/post-powder) | 1,200 |
| Aisles/forklift circulation | 2,400 |
| **Total** | **9,000** |

Requirements: clear height ≥ 18 ft over weld cells (H-3); 480V 3φ, ~115 kVA demand →
250A feeder (H-8: confirm building spare capacity); compressed air 100 CFM (25 HP screw +
dryer); weld fume: source capture at each arc + 8,000 CFM general exhaust with interlocked
makeup air; slab: gantry legs ~12 kip on 18" base plates — verify 6" slab (H-9); manifolded
C25 gas bank ≤ 3,000 SCF per NFPA 55. Fire/permits: landlord consent + Gwinnett fire-marshal
review, NFPA 51B hot-work program. No coating operations on site → no air permit, no booth.

## 5. Quality system

- **Incoming:** kit count, MTR verification (A500 Gr B / A36 or CS-B), 5-point dimensional
  spot check per kit batch; nonconforming kits rejected to processor.
- **Welding:** WPS/PQR per AWS D1.1 (H-2: engineering to confirm code intent — drawings
  specify process/filler but no code), written and qualified with contract CWI; welder quals
  on 1/8"-wall tube fillets; documented quarter-symmetric weld sequence.
- **In-process:** 100% visual to D1.1 acceptance, fillet gauges (0.25 ± 0.063 leg per note 13);
  lead audits one unit/week fully.
- **First article:** fixture certified by laser tracker (master gauge); 3 FA units measured
  on rented FARO **before and after** powder cure (oven can move residual stress); interfaces
  (foot mounts, lifting interfaces, deck tabs) gauged go/no-go in production thereafter.
- **Final:** coating thickness 2–3 mil check, serialized traveler (merged with powder packing list).
- **Calibration:** gauge/cal program ≈ $6K/yr; fixture re-cert annually or after any crash.
- H-13: request engineering relax the blanket ±.02 two-place tolerance on non-interface
  weldment dims — the single highest-leverage FA risk reducer.

## 6. EHS & compliance

- Weld fume: Mn exposure from A36/ER70S — design to ACGIH TLV 0.02 mg/m³ respirable via
  source capture; baseline IH survey month 1 of production; PAPR helmets if exceeded.
- OSHA: hot work (NFPA 51B), LOTO, crane/rigging (gantry operator training, annual hoist
  inspection), forklift certs, PPE program, hearing conservation survey.
- Fire: weld screens with line-of-sight, fire watch where required, compressed-gas storage
  per NFPA 55/IFC; no flammable-liquid coating ops on site (powder outsourced — by design).
- Workers comp class ~3365 (steel fab) priced inside the 1.35 loading.

## 7. Consumables & indirect costs

Per heavy weldment: wire 45 lb @ $1.60 = $72; C25 gas $30; tips/abrasives/anti-spatter $28
→ **$130/unit**. Wood legs ≈ $10/leg. Annual at plan volume ≈ $38K, on VMI bins.
Indirects: maintenance/cal/PPE pool $20K/yr; utilities ≈ $36K/yr incremental (in facility
line); insurance/misc $24K/yr.

## 8. Throughput & constraint analysis (TOC)

- **Drum:** the heavy weldment fixture + paired welders. Capacity 22 heavy-equiv/mo on one
  shift; load 20 + wood legs (filler, schedulable) → 91% planned utilization.
- **Buffer:** 5 working days of kit-sets ahead of the drum (7 in the loop total, released in
  processor batches of 5); post-weld buffer of ≤5 units ahead of 2×/wk powder shipments.
- **Rope:** kit call-offs are triggered by drum completions (kanban), not forecast; the
  processor holds the steel, Slip holds ~1 week.
- **Takt vs. cycle:** takt 1 heavy/day; drum cycle 8.5 hr fixture-occupancy/day → positive
  slack ~1.5 hr/day; protective capacity = overtime, then contract welders.
- Subordination: every capex line either feeds the drum or is infrastructure; cutting and
  forming capacity were deliberately **not** purchased (kits) so no non-drum machine exists
  to absorb cash or attention. At 2× volume, exploit (second shift) before elevate (tack jig
  $30K), before any new fixture.

## 9. Financials

**Unit economics, heavy weldment (steady state / year 1):**

| | Make (hybrid) | Buy |
|---|---|---|
| Tube kit (1,088 lb gross, batch-nested) | $1,360 | — |
| Plate/formed kit (208 lb gross) | $447 | — |
| Powder coat (incl. freight, 5/load) | $425 | — |
| Consumables | $130 | — |
| Direct weld labor 16.5 hr @ $35.10 | $579 | — |
| Ops-tech share 2.6 hr @ $33.75 | $88 | — |
| Cost of quality (yr-1 $190 → steady $95) | $95–190 | — |
| **Variable cost** | **$3,124–3,219** | **$5,221** |
| Contribution per unit | $2,070 (yr 1) → $2,170 | — |

Fixed pool: lead $107K + facility/utilities/insurance $150K + maintenance/cal $20K +
amortization $64K = **$341K/yr** → breakeven ≈ **13 heavy-equiv/month**.

**Annual at plan volume (240 heavy + 120 wood):** make-side total ≈ $1.72M vs. buy baseline
$1.88M → **net ≈ +$165K/yr** (wood legs ≈ +$18K of that; in-housing heavy legs was evaluated
and rejected — vendor at $79.71 beats internal cost).

**Sensitivity:**

| Scenario | Net annual benefit |
|---|---|
| −40% (12 heavy/mo) | −$43K (shrinkable to ≈ −$10K; hibernation path defined) |
| −30% (14/mo) | +$23K |
| Plan (20/mo) | +$165K |
| +30% (26/mo) | +$292K |
| 2× (40/mo, 2nd shift) | +$580K |
| Steel +25% | Make advantage widens ~$100–190/unit (vendor passes through margin-on-material; kit POs index-priced without it) |

**Capex $504K**; cash low point ≈ −$610K at month 6; simple payback 3.1 yr at flat 20/mo,
<2 yr on the growth path. Optional equipment lease flattens the cash trough to ≈ −$280K
for +$11K/yr (H-10).

## 10. Implementation timeline (decision = M0; SOP target M7)

| Month | Milestones |
|---|---|
| M0 | Decision + volume gate check (forecast ≥18/mo); landlord/fire-marshal conversations start week 1; kit + powder RFQs out (H-5, H-7) |
| M1–M2 | Fixture design (Slip-owned CAD); dual-quote fixture build; fixture steel pre-ordered at 60% design; lease/space confirmed; hire lead (M2) |
| M2–M4 | Facility prep (feeder, air, fume, racks); gantries installed; welders 1–2 hired (M3), quals + WPS/PQR with CWI; leg cell live (first revenue work: wood legs) |
| M4–M5 | Fixture delivered + laser-tracker certified; 3 first-article weldments; FARO rental; FA before/after-powder measurement |
| M5–M6 | Welder 3 hired; rate ramp 0.5/day → 1/day; vendor at full rate through M6 |
| M7 | SOP at rate; vendor to 50% |
| M8–M9 | Vendor wind-down to callable frame agreement (tooling held, $0/mo); project close-out review |

Float: ~4 weeks. No purchased machine on the critical path (longest item = fixture, with an
in-house platen fallback worth 0.7/day).

## 11. Risk register (cumulative — none deleted)

| # | Risk | Status / mitigation |
|---|---|---|
| R-1 | Light-family definition wrong (Wood vs 106997) | Open-trivial; H-1 confirm; plan robust to either |
| R-2 | Weld content estimate off (±20%) | Accepted; drum has 9% slack + overtime; re-measure at FA |
| R-3 | Landlord/AHJ blocks hot work at Oakbrook | Mitigated: early engagement + flex-space fallback (+$20K/yr) |
| R-4 | Powder vendor can't take 16-ft parts | Mitigated: dual-source at launch (H-5); worst case wet-paint alternate |
| R-5 | Ramp underperforms (cycle times optimistic) | Mitigated: vendor overlap M1–M9; contract welders; FA gate |
| R-6 | Supply gap during transition | Mitigated: overlap schedule + callable frame agreement |
| R-7 | Welder hiring/turnover | Mitigated: test-internally funnel, wage band to $31, standing pipeline, contract bridge |
| R-8 | Demand falls below breakeven (13/mo) | Mitigated: volume gate G-1 (≥18/mo committed 24-mo forecast); hibernation path; ~$200K net capex at risk after resale |
| R-9 | First-article distortion/quality failure | Mitigated: sequence control, restraint cooling, pre/post-powder FA, CWI disposition, $40K contingency; H-13 tolerance relief |
| R-10 | Steel price spike | Accepted-favorable: index-priced kits; flag absolute cost rise to product pricing |

## 12. Make / Buy / Hybrid recommendation

**Hybrid — proceed, gated.** In-house: heavy weldment + wood legs, welded from purchased
cut/formed kits, powder outsourced. Stay-buy: decks, heavy legs, wood-tray piece parts,
hardware, aluminum edge extensions.

Deciding factors: (1) the vendor weldment price ($5,221) carries ≈ $2,100/unit of
labor+margin that 16.5 hr of in-house welding captures; (2) cutting at 20/mo doesn't pay
for cutting machines — kits do; (3) powder in-house is the worst permit/capex per dollar
saved; (4) design churn (R01→R03 in 4 months) and 6–8 week vendor lead times are a growing
tax that in-house welding removes; (5) economics are volume-driven: gate on a committed
24-month forecast ≥ 18 heavy-equiv/mo (G-1). If the forecast is flat ≤ 14/mo: do not build —
instead use this model's should-cost to renegotiate the weldment price (target $4,400–4,600)
and revisit at the next volume step.
