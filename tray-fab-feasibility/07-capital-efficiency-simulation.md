# Capital-Efficiency Simulation — 100 Monte Carlo Runs

Run 2026-06-11 (`sim/simulate.py`, seed 20260611, output in `sim/results.txt`).
Goal: same project, but **incredibly smart with money** — find the capital strategy that
wins across uncertainty, not just in the base case, and translate it into a concrete
machine list, shop build-out, and hiring sequence.

## 1. Method

100 stochastic world-draws (common random numbers — every strategy faces the identical
world), 60-month horizon, monthly cash vs. the continue-buying baseline. Stochastic
inputs, all anchored to the data basis: demand growth (median +10%/yr, lognormal, capped
0.65–1.9, starting at the evidenced 21/mo), 15% recession shock (−40% for 12 mo), kit
quotes (tri $1,850/$2,035/$2,550), true weld hours (tri 14.5/16.5/22 + learning curve),
powder (tri $350/$425/$550), steel index walk (8%/yr vol on 60% of kit), buy-price
escalation (2–5%/yr), revision events (Poisson 2/yr; fixture-block cost in-house),
wage inflation (3–5%), hiring lag (1–3 mo), FA failure (15–30% by fixture quality,
+2 mo and $40K), used-equipment repair events, insurance delta ($15–25K/yr),
wood-tray ramp realization (10–100% of plan), negotiation success (70% at 6–12%).
Calibration check: in flat worlds, strategy B reproduces the Loop-49 deterministic P&L.

Five strategies, each a complete capital + staffing policy:

| | Capex | Fixture | Handling | Day-1 crew | Capacity | Upgrade path |
|---|---|---|---|---|---|---|
| **A ultra-lean** | $225K | certified platens + manual layout | mobile gantries | lead + 2 welders | 18/mo | none |
| **C lean-staged** | $268K | modular hard fixture | 2-ton mobile gantries | lead + 2 welders, triggers | 22/mo | +$75K kit → 27/mo |
| **B base (Loop-25 plan)** | $504K | custom hard fixture | 5-ton gantry runways | 5 FTE | 22/mo | +$45K → 27/mo |
| **D capacity-forward** | $660K | hard fixture + tack jig | 5-ton runways | 6 FTE | 27/mo | +$60K → 40/mo |
| **E renegotiate-only** | ~$0 | — | — | — | — | — |

## 2. Results (100 simulations)

```
strategy         meanNPV     P10     P50     P90   %>0  trough50  trough10 payback50
A_ultra_lean         486      77     515     871   91%      -361      -445        24
C_lean_staged        855      -8    1012    1595   89%      -431      -521        23
B_base               320    -869     562    1232   72%      -731     -1112        33
D_capacity_fwd       369   -1361     608    1883   62%      -931     -1745        35
E_renegotiate        520     154     398     987  100%       -15       -15         4

Wins (best NPV on the same world-draw):       Regret vs best choice (median / P90, $K):
  A_ultra_lean       8 /100                     A_ultra_lean      559 / 1221
  C_lean_staged     40 /100                     C_lean_staged     125 /  733
  B_base             0 /100                     B_base            743 / 1198
  D_capacity_fwd    31 /100                     D_capacity_fwd    622 / 1682
  E_renegotiate     21 /100                     E_renegotiate     543 / 1340

Median NPV ($K) by realized demand-growth regime (n = 31/18/32/19):
strategy           shrink <1.0   flat 1.0-1.1   grow 1.1-1.35   fast >1.35
A_ultra_lean              178            656             662          492
C_lean_staged              99           1142            1240         1091
B_base                   -718            617             875          745
D_capacity_fwd          -1225            154            1169         1757
E_renegotiate             284            357             671          876
```

## 3. What the simulation says

1. **C (lean-staged) is the choice.** Best median NPV ($1.01M), most wins (40/100), and —
   the decisive metric for being smart with money — **lowest regret** (median $125K vs.
   $540–740K for everything else). It is within ~$150K of the best possible choice in
   almost every world, because the $75K upgrade kit lets it become D when growth shows up.
2. **B — my own Loop-25 plan — never wins. Not once in 100 worlds.** It spends $504K to
   get the same 22/mo capacity C buys for $268K, and it staffs 5 FTE on day one where C
   staffs 3.5 and hires on triggers. The simulation retired the base plan. (Strategy B's
   honest epitaph: a good deterministic plan that pays for certainty the world doesn't offer.)
3. **D is a bet, not a plan.** It wins 31/100 — almost exclusively the fast-growth worlds
   — but its P10 is **−$1.36M** and it's NPV-positive in only 62% of worlds. If Jeff has
   firm knowledge that demand doubles (signed customer commitments, fleet plan), D's
   median in fast worlds ($1.76M) is the prize; otherwise C captures ~85% of that prize
   with ~40% of the downside.
4. **E (renegotiate) is the floor, never the ceiling.** 100% non-negative, instant payback
   — and a median $543K left on the table. It remains the correct branch if G-1 fails,
   and its existence is negotiating leverage either way.
5. **A proves the concept cheap but caps the upside** — fine if capital is truly scarce,
   but its manual-fixture quality risk (FA p=0.30, +2 hr/unit) and 18/mo ceiling cost
   ~$500K of median NPV vs. C. The $43K difference between A and C buys the modular hard
   fixture — the single highest-return $43K in the whole project.
6. **Troughs:** C's median worst-cash is **−$431K** (P10 −$521K) vs. B's −$731K (P10
   −$1.1M). Lean-staging cuts the maximum capital at risk by ~40% while *raising* expected value.

**Decision rule:** adopt **C**. Hold **E** as the pre-priced fallback at G-1/G-2. Pivot
toward **D's capacity only via C's upgrade trigger** (sustained >20/mo for 8 weeks), never
speculatively. A and B are retired.

## 4. The machine list (configuration C) — what to buy, and why

Total: **$268K** day one + **$75K pre-engineered upgrade kit** (ordered only at trigger).

| # | Item | Spec / source | New/Used | Cost | Why this and not the alternative |
|---|---|---|---|---|---|
| 1 | **Modular weldment fixture** | 5×16-ft modular tooling-table system (Siegmund/Bluco class) + machined locator blocks for 106900, hydraulic toggle clamps, laser-tracker certified | Table used/surplus OK; blocks new | $70K | The one place not to cheap out — it is the drum, the gauge, and the quality system. Modular (not a welded monolith) because the design rev'd 3× in 4 months: a rev change is new blocks (~$3–8K, 2 weeks), not a new fixture (~$85K, 12 weeks). Replaceable blocks also make crash recovery a parts swap. |
| 2 | Leg/small-part bench fixtures | wood-leg 107508 + spares, on a 5×10 used platen | New fixtures, used platen | $12K | Legs are the first revenue (M3) and the training ground for new hires before anyone touches a $5,600 weldment. |
| 3 | **Pulse-MIG welders ×2** | 350-class pulse (Miller Invision/Deltaweld or Lincoln PowerWave equiv.), .045 ER70S-6, dual-schedule | New | $18K | Pulse earns its premium on 1/8-in wall A500: burn-through control and low spatter (less grinding labor — labor is 4× the machine cost over 5 years). Two, not four: two welders on day one. |
| 4 | Backup/3rd-station MIG | 450-class CV, used (Deltaweld 452 class) | Used | $3.5K | Hot-spare philosophy at 1/3 the price; becomes station 3 at the upgrade trigger. |
| 5 | **Material handling: 2× 2-ton mobile gantries + chain hoists + powered tilt cart** | steel A-frame gantries on casters; 2-ton electric hoists; 16-ft powered weldment cart | Gantries/hoists used | $22K | The weldment weighs 1,179 lb. The base plan's 5-ton freestanding runways ($88K) were 4× oversized and needed slab work and fire-marshal review. Mobile gantries lift the same part, move to the work, need no foundations, and move out with us if the site changes. **Single biggest saving: −$66K.** |
| 6 | Fume extraction, source-capture | 2 portable HEPA source-capture units + fume-extraction guns | New (safety) | $20K | Portable beats a $58K installed system at 2–3 arcs: it follows the work, needs no ductwork permit, and relocates. Ambient roof fan ($15K) is **contingent** on the M8 industrial-hygiene survey — buy compliance when measurement says so, not before. |
| 7 | Compressed air | 25-HP rotary screw + dryer, used/refurb | Used | $12K | 60 CFM peak demand; used screw compressors are plentiful and rebuildable. |
| 8 | QA kit | fillet gauges, weld gauges, 16-ft digital tape cert'd, fixture laser-tracker certification service, FARO arm **rental** M5–M7 | Mixed | $14K | The certified fixture is the CMM. Rent precision for the 3 months it's needed (~$4K/mo) instead of owning $75K of it. |
| 9 | Benches, racks, screens | cantilever rack (24-ft tube kits), weld screens, tables | Used | $18K | Auction/used-equipment market; zero performance difference. |
| 10 | Facility prep | 2 welding circuits (100A drops), LED task lighting, air piping, striping | — | $45K | Cut from $78K by (a) negotiating landlord TI dollars (the Oakbrook model already carries $10/SF TI — use it for power), (b) no slab work (no runway foundations), (c) 6,500 SF instead of 9,000. |
| 11 | Install + contingency (~13%) | — | — | $33.5K | Includes spare locator-block set ($6K). |
| | **Day-one total** | | | **$268K** | vs. $504K base — same 22/mo capacity |
| 12 | **Upgrade kit (trigger only)** | tack/pre-stage jig, 3rd welding station outfit, 3rd gantry, ambient fan, 2nd powered cart | Mixed | $75K | Pre-engineered at M3 (drawings done, quotes held), **ordered only when demand sustains >20/mo for 8 weeks**. Takes capacity to 27/mo; second shift takes it to ~40/mo with zero additional machines. |

What we deliberately do **not** buy, at any volume below ~50/mo: tube laser ($450–900K — kits are cheaper until then), flat laser & press brake (formed parts arrive in kits), powder line ($250–400K + permits — outsource at $425/unit), bridge crane, CMM/FARO, blast cabinet, CMMS software, robotic welder (re-evaluate the leg cell with a cobot only above ~25 legs/week *and* after the H-6 weld-spec review).

## 5. Shop setup (6,500 SF inside 1275 Oakbrook, reserve the adjacent 3,000 SF)

U-flow off one dock door, built in this order:

| Wks | Build step |
|---|---|
| 1–4 | Power drops + lighting in the weld zone (landlord TI work order first — longest approval); striping; racks up; receiving lane live |
| 3–6 | Leg cell complete (platen + bench fixtures + welder 1 + portable fume) — **production-capable while the big fixture is still in build** |
| 5–10 | Modular fixture table set, leveled, blocks installed; gantries + tilt cart commissioned; weld cell A complete |
| 10–11 | Laser-tracker certification of fixture; QA bench; travelers printed |
| 12+ | Cell B floor space left **empty but powered** (the upgrade kit drops in with zero construction later) |

Zones (SF): receiving + kit racks 1,200 · kitting/staging 400 · weld cell A 800 · leg cell
400 · inspection/straightening 500 · powder out/in at dock 600 · WIP 800 · aisles 1,800.
Weldments move only by gantry + powered cart; legs flow on benches; kits staged at the
cell the afternoon before. The empty cell-B slab is the cheapest capacity option ever
purchased: $0 until the trigger fires.

## 6. Hiring plan — who, when, and the trigger for each seat

| When | Role | Cost (loaded) | Why then |
|---|---|---|---|
| M2 | **Working fab lead** ($38/hr, $107K/yr) | The only unconditional early hire. Co-designs the fixture blocks, writes WPS with the contract CWI, builds the leg cell, later runs the shop so Jeff doesn't have to. Hire for: structural-tube fab background + has trained welders. | |
| M2 (fractional) | **Contract CWI** (~$15K program) | WPS/PQR, welder qualification, FA disposition authority. Never a full-time hire at this scale. | |
| M3 | **Welder 1** (Fab 2-capable, $26–29/hr) | Quals on coupons week 1–2, then immediately productive on wood legs + the 10-unit bridge stock — revenue before the big fixture even arrives. | |
| M4 | **Welder 2** ($24–26/hr) | Paired-weldout partner for FA builds M5 and rate ramp. | |
| Trigger | **Welder 3** — hire when measured hours >17/unit at G-3 **or** demand sustains >20/mo | Don't staff for the estimate; staff for the measurement. Saves ~$73K/yr if the learning curve lands. | |
| Trigger | **Ops tech** ($70K/yr) — hire when demand sustains >24/mo or the lead logs >25% time on logistics for a month | Until then: receiving shares Slip's existing dock staff/forklift; welders self-stage with the gantry. Saves ~$70K in year 1. | |
| Trigger | **Shift-2 crew** (+3 welders, +$2.50/hr premium) — demand >20/mo for 8 wks, with the upgrade kit | Capacity to ~40/mo on the same fixture. | |

Skills ladder, quals-not-tenure (Fab 1 → 2 → 3, $24→$31), CWI-prep sponsorship for the
lead (internal CAWI by ~M12) — unchanged from Loop 38.

## 7. The ten money rules this plan follows

1. **Buy the constraint, rent everything that touches it occasionally** (fixture owned; FARO rented; CWI contracted).
2. **Capacity in options, not in steel**: empty powered floor + a pre-engineered $75K kit beats $236K of day-one machines B would have bought.
3. **Size handling to the part, not the habit** — 2-ton gantries for a 1,179-lb part, not 5-ton runways.
4. **Staff to measurements, not estimates** — welder 3 and the ops tech are hired by trigger, after G-3 measures real hours.
5. **Used iron where failure is an inconvenience** (compressor, racks, backup MIG, gantries); **new where failure stops the drum or hurts people** (pulse MIGs, fume capture, fixture blocks).
6. **Spend the landlord's money first** — TI dollars cover power and lighting before Slip capex does.
7. **Make revenue before making rate** — the leg cell earns from M3 while the fixture is still in build.
8. **Compliance on evidence** — the ambient fan waits for the IH survey; the second powder vendor is qualified on paper (free) before being needed.
9. **Every dollar has a reversal path** — modular table resells at ~55%, gantries are commodity, the lease footprint is sublettable; worst-case stranded capital ≈ $120K.
10. **Keep the floor under the project** — E (renegotiate at 6–12%) stays pre-priced and ready; it converts even a cancelled project into a six-figure win.

## 8. Updated headline vs. the Loop-50 plan

| | Loop-50 base (B) | **Simulation pick (C)** |
|---|---|---|
| Day-one capex | $504K | **$268K** (+$75K contingent) |
| Median cash trough | ≈ −$700K | **≈ −$430K** (P10 −$520K) |
| Median 5-yr NPV (100 sims) | $562K | **$1,012K** |
| P10 NPV | −$869K | **−$8K** |
| Worlds NPV-positive | 72% | **89%** |
| Median payback | 33 mo | **23 mo** |
| Capacity | 22 → 27/mo | 22 → 27/mo (same), → 40 with shift 2 |

Gates G-1/G-2/G-3, the TEEMS negotiation sequence, quality/EHS/traceability systems, and
the renegotiation fallback all carry over unchanged. The simulation changed *how much
money walks through the door on day one* — not the strategy, the gates, or the drum.
