# Loop Log — Loops 26–50 (Second 25: Evidence, Depth, Adversarial Review)

Continues `02-loop-log.md`. Issue/assumption/human-input numbering continues from Loop 25
state. Phasing: Loops 26–32 replace assumptions with evidence (NetSuite transactions +
market benchmarks); Loops 33–40 build operational depth to world-class standard; Loops
41–48 attack the plan a second time, harder; Loop 49 is an independent audit pass; Loop 50
re-synthesizes.

---

## Loop 26 of 50 — Evidence: the buy price is wrong (Evidence)

**Issues identified:**
- I-68: The $5,221.32 buy baseline is stale — it is the R02 price. What is the *current* price?
- I-69: Loops 1–25 never queried actual PO history at all.
- I-70: Rev-change pricing behavior unquantified (R01→R03 churn was flagged but never costed).

**Resolutions (from NetSuite PO history, queried this loop):**
- I-68 → Resolved: PO10280 (5/11/2026) bought 106900-R03 at **$5,868.33**; PO10309 (5/19/2026) at **$5,577.84**. Current effective buy price = $5,577.84, **+6.8% over the R02 baseline** used in Loops 1–25. All economics rebase to $5,577.84 (Loop 32).
- I-69 → Resolved: full PO/receipt/work-order extract added to `04-data-basis.md` §7–9.
- I-70 → Resolved: the R03 transition initially priced at +12.4% ($5,868.33) and was negotiated down to +6.8% within 8 days. **Each revision costs a repricing event with a double-digit opening position.** This was previously a qualitative argument; it is now a measured one (~$290–647/unit per rev cycle).

**Algorithm pass:** *Question:* challenge the practice of comparing against a frozen quote — pricing must be re-pulled at decision time; added to the decision-memo checklist. *Delete:* deleted assumption A-9-to-be ("price stability") before it was born; the model now carries price as a dated input. *Simplify:* one price field, dated, sourced from the latest PO. *Accelerate:* none.

**Constraint check:** drum unchanged; buy-side facts only.

Loop 26 of 50 complete. Resolved: I-68..I-70. Confidence: 8/10 (economics provisional until Loop 32 rebase).

---

## Loop 27 of 50 — Evidence: demand is real and scheduled (Evidence)

**Issues identified:**
- I-71: The volume gate (G-1, ≥18/mo) rested entirely on a forecast Jeff hadn't provided yet. Is there transactional evidence?
- I-72: Wood-tray volume of 10/mo was taken as given — what does the system actually show?

**Resolutions (from work-order history):**
- I-71 → Resolved: heavy-tray work orders run a steady **5/week cadence (≈21–22/month), released and scheduled through 7/27/2026**, with surge weeks of 9–10 (week of 4/24, 4/27, 6/29) and a 14-unit customer-site batch (Denton, TX deployment, 5/20). The trailing-13-week average ≈ 22/mo. **G-1's evidence threshold (≥18/mo) is met by current actuals**, though the 24-month forward commitment (H-11) is still the formal gate.
- I-72 → Resolved: only **3 wood-tray work orders exist (3/9/2026)**; wood beams (107350/107456) have never been purchased. The 10/mo wood plan is a ramp target, not a run rate. New risk **R-12**: wood volume shortfall — impact is confined to drum-filler utilization (~$20K/yr of leg savings), not gate-critical, but the wood routing should not drive any capex (it doesn't).

**Algorithm pass:** *Question:* challenged whether 20/mo was aspiration or actual — answered with transactions: actual. *Delete:* deleted the implicit dependency of project viability on wood volume (the plan now states heavy-only viability explicitly). *Simplify:* gate evidence = one query, repeatable monthly. *Accelerate:* none.

**Constraint check:** drum sized at 22/mo single shift vs. demonstrated demand 21–22/mo — tighter than the plan assumed. Protective capacity (overtime/contract welders) is not optional; it is load-bearing. Noted in §8.

Loop 27 of 50 complete. Resolved: I-71, I-72. Risks added: R-12. Confidence: 8/10.

---

## Loop 28 of 50 — Evidence: vendor structure and delivery cadence (Evidence)

**Issues identified:**
- I-73: "The vendor" was anonymous in the plan; concentration risk never named.
- I-74: Vendor delivery capacity unknown — can the buy option even support growth?
- I-75: Who makes the legs and wood parts?

**Resolutions:**
- I-73 → Resolved: heavy weldments are **single-sourced to TEEMS Fabrication** (every weldment PO). Heavy legs come from **Steel Materials, Inc.** ($79.71), wood legs from **Starflex Fabrication** ($122.71). Three fab vendors total; the big-dollar item has zero redundancy today — the in-house option *is* the second source.
- I-74 → Resolved: receipts on PO10118 (28 units) arrived 5–6/week over 5 consecutive weeks (4/6→4/30), i.e., **TEEMS's demonstrated throughput ≈ 24–26/month**, already at parity with demand. If demand doubles, the buy path needs a second vendor qualified from scratch (8–12 weeks + FA) — the same qualification work the make path does once, under Slip's control.
- I-75 → Resolved (above); piece-part vendors are unaffected by the recommendation and provide natural homes for the stay-buy scope.

**Algorithm pass:** *Question:* challenged the framing of make-vs-buy as cost-only — at 2× demand it becomes a *capacity* decision; the recommendation text updated. *Delete:* deleted the "qualify a second weldment vendor" alternative from the options list? No — kept deliberately as the comparison case in §12 (it's the honest buy-side fix and costs ~$40–80K of engineering time without capturing margin). *Simplify:* vendor map now one table. *Accelerate:* none.

**Constraint check:** drum analysis gains a twin: the *buy* path's drum is TEEMS's weld shop at ~25/mo, outside Slip's control. Stated in §8.

Loop 28 of 50 complete. Resolved: I-73..I-75. Confidence: 8/10.

---

## Loop 29 of 50 — Evidence: steel market price correction (Evidence)

**Issues identified:**
- I-76: A500 tube assumed at $0.72/lb (A-3 chain) — market check says otherwise.
- I-77: Kit cost build-up must be rebased; does the project still clear?

**Resolutions:**
- I-76 → Resolved: published service-center pricing (March 2026) for A500 Gr B rectangular tube in the relevant sizes runs **$0.85–1.00/lb** (2×4×⅛: $0.85–0.92; 2×6×⅛: $0.93–1.00). Rebase tube at **$0.90/lb**; A36 sheet/plate to $0.74/lb. Sources logged in `04-data-basis.md` §10. A-3 superseded by **A-9** (market-priced kit model).
- I-77 → Resolved: tube kit 1,088 lb × $0.90 = $979 material + cutting $264 + handling/margin $315 ≈ **$1,560** (was $1,360); plate/formed kit ≈ **$475** (was $447). Kit-set **$2,035** (+$228). Partially offset by the +$357 buy-price correction (Loop 26): net contribution moves **up** ~$130/unit. Full rebase in Loop 32.

**Algorithm pass:** *Question:* why did the original estimate miss? It used a 2024-vintage mental price. Rule added: every $/lb, $/hr, $/SF input in the model carries a date and source. *Delete:* deleted all undated numbers from the plan (each now traces to data basis). *Simplify:* kit price = (lb × indexed $/lb) + machine time + fixed adder — same formula both vendors quote against, making RFQs comparable. *Accelerate:* none.

**Constraint check:** unaffected.

Loop 29 of 50 complete. Resolved: I-76, I-77. Assumptions: A-9 (dated, sourced). Confidence: 8/10.

---

## Loop 30 of 50 — Evidence: labor market validation (Evidence)

**Issues identified:**
- I-78: A-4 wages were asserted, not sourced.
- I-79: Is the $24–29 band enough to hire D1.1-capable fitters, or is it a market-average trap?

**Resolutions:**
- I-78 → Resolved: market data (BLS OEWS 51-4121, Indeed, ZipRecruiter, Feb–Apr 2026): Atlanta welder **average $22.76–24.64/hr**; Georgia median ≈ $22.08. Sources in data basis §10.
- I-79 → Resolved: the plan's $24–29 band sits at the 60th–85th percentile — correctly positioned to hire *above-average* fitters without paying certified-pipe-welder rates. The Loop 20 escalation ceiling ($31) reaches ~90th percentile. A-4 confirmed and re-dated; R-7 probability downgraded from "high" to "medium."

**Algorithm pass:** *Question:* challenged paying 60th–85th percentile when the work is fixtured MIG — held: fit-up skill on a 186-inch frame is the actual scarce skill, and turnover costs ~$15K/seat (requal + ramp). *Delete:* deleted the night-shift premium from the base case (second shift exists only in the 2× scenario). *Simplify:* one published pay ladder (Loop 38 builds it). *Accelerate:* none.

**Constraint check:** unaffected; drum staffing cost confirmed.

Loop 30 of 50 complete. Resolved: I-78, I-79. Confidence: 8/10.

---

## Loop 31 of 50 — Evidence: lead time and working capital, measured (Evidence)

**Issues identified:**
- I-80: "6–8 week vendor lead time" was an assertion; receipts allow measurement.
- I-81: Working capital comparison (buy pipeline vs. make WIP) never computed.

**Resolutions:**
- I-80 → Resolved: PO10118 placed 3/16 → receipts 4/6, 4/10, 4/17, 4/24, 4/30: **first delivery 3.0 weeks, last 6.5 weeks** — the order book rides 3–6.5 weeks of vendor pipeline. In-house door-to-door: kit buffer 5 days + weld 1 day + powder ≤5 days ≈ **7–11 working days**, a 60–70% lead-time reduction.
- I-81 → Resolved: buy pipeline carries ~5 weeks × 5/wk × $5,578 ≈ **$140K** of open-PO/in-transit exposure; make carries kit buffer (7 sets × $2,035 = $14K) + WIP/post-weld buffer (≈8 units × ~$2,700 ≈ $22K) + consumables ≈ **$40K** — about **$100K less capital in the loop**, partially offsetting the capex in cash terms. Added to §9 and the cash model (Loop 33).

**Algorithm pass:** *Question:* is the lead-time gain worth anything in dollars? Yes — quantified as deployment-schedule risk absorbed (a Denton-style 14-tray surge currently needs 5+ weeks of notice; in-house needs ~2). Stated as strategic value, not double-counted in savings. *Delete:* nothing. *Simplify:* working-capital effect carried as a single one-time +$100K cash item at SOP. *Accelerate:* surge response documented as a playbook (overtime weekend = +3 units).

**Constraint check:** the 5-day kit buffer is confirmed as correctly sized against the measured surge pattern (max observed week = 10 units → buffer + overtime covers).

Loop 31 of 50 complete. Resolved: I-80, I-81. Confidence: 8/10.

---

## Loop 32 of 50 — Rebase: unit economics v2 (Evidence)

**Issues identified:**
- I-82: All headline numbers must be recomputed coherently with Loops 26–31 corrections.

**Resolutions — economics v2 (steady state):**
- Variable make cost/heavy weldment: kits $2,035 + powder $425 + consumables $130 + direct labor $579 + ops share $88 + CoQ $95 = **$3,352** (yr-1: $3,447 with $190 CoQ).
- Buy price: **$5,577.84** → contribution **$2,226/unit** steady ($2,131 yr-1).
- Fixed pool unchanged: $341K/yr → **breakeven 153/yr ≈ 12.8/mo**.
- Plan volume (240/yr): **+$193K/yr steady** (+$170K yr-1). At 2× (480/yr, second shift, fixed →$418K): **+$650K/yr**. At 12/mo: **−$20K/yr** (hibernation path stands).
- Buy baseline annual rebased: heavy fab-scope $6,899/tray → with wood, ≈ **$1.97M/yr** addressable.
- I-82 → Resolved; plan §9, exec summary, and registers updated. R02-based numbers retired.

**Algorithm pass:** *Question:* per Rules, this re-litigates Loop 12's resolved economics — justified explicitly by contradicting evidence (actual R03 PO price and dated steel benchmarks; both stated). *Delete:* deleted the year-1/steady-state dual bookkeeping everywhere except §9 (one table owns it). *Simplify:* all scenario rows recompute from contribution × volume − fixed; no bespoke math per scenario. *Accelerate:* none.

**Constraint check:** breakeven (12.8) < demonstrated demand (22) < drum capacity (22 single shift) — the project clears on actuals, and the drum, not demand, is the binding constraint. Unchanged conclusion, firmer ground.

Loop 32 of 50 complete. Resolved: I-82. Confidence: 9/10 on economics structure (kit quotes H-7 still the live uncertainty).

---

## Loop 33 of 50 — Monthly cash model, NPV, IRR (Depth)

**Issues identified:**
- I-83: Only a single "cash trough" number existed; no monthly model, no NPV/IRR.

**Resolutions:**
- I-83 → Resolved: monthly model M0–M24 built (`06-financial-model.md`): capex spread M1–M5, ramp labor from M2, qualification builds M4–M5, rate from M7, vendor overlap costs through M9, +$100K working-capital release at M8. Cash trough **−$612K at M6**; cumulative breakeven **M27** at flat 20/mo, **M19** on the growth path (30/mo from M13).
- 5-year NPV @ 10% discount: **+$101K flat** / **+$758K growth path**; IRR ≈ **15% flat / ≈35% growth**. The flat case clears the hurdle but thinly — consistent with the gate logic: this is a growth-justified project that doesn't lose money flat.

**Algorithm pass:** *Question:* is 10% the right hurdle for a venture-backed company? Probably low — at a 20% hurdle the flat case is NPV-negative (−$95K) and the growth case still clears (+$420K). Stated plainly in the model; the decision honestly depends on the growth view (H-11). *Delete:* nothing physical; deleted false precision — model rounds to $1K. *Simplify:* one spreadsheet-equivalent table, 14 rows. *Accelerate:* none.

**Constraint check:** cash model confirms no month requires output above drum capacity.

Loop 33 of 50 complete. Resolved: I-83. Confidence: 9/10.

---

## Loop 34 of 50 — Implementation: owners, dependencies, critical path (Depth)

**Issues identified:**
- I-84: Timeline had milestones but no owners or dependency logic.
- I-85: Decision governance undefined (who signs what, when).

**Resolutions:**
- I-84 → Resolved: plan §10 rebuilt as a dependency table: every line has an owner (Jeff, fab lead, engineering, contract CWI, vendors), duration, predecessor, and float. Critical path: **decision → fixture design (6 wk) → fixture build (12 wk) → certification (1 wk) → FA builds (4 wk) → rate ramp (6 wk) = 29 weeks ≈ M7**, with the platen-fallback bypass worth 4 weeks if the fixture build slips.
- I-85 → Resolved: three gates — **G-1** volume commitment (M0, Jeff), **G-2** quotes-confirmed re-check of economics v2 (M1, after H-5/H-7 RFQs land; kill/renegotiate if contribution <$1,800), **G-3** FA acceptance (M5, engineering + CWI; vendor overlap extends if failed). Each gate has pre-written exit criteria.

**Algorithm pass:** *Question:* who actually runs this project M0–M2 before the fab lead exists? Named explicitly: Jeff or a delegated ops engineer ~50% time (cost acknowledged in Loop 47). *Delete:* deleted the M8–M9 "project close-out review" as a milestone — folded into the monthly KPI review (Loop 35). *Simplify:* three gates instead of a stage-gate bureaucracy. *Accelerate:* RFQs (H-5/H-7) issue at M0 week 1 — they gate G-2, not equipment.

**Constraint check:** critical path runs through the fixture — the drum's tooling — as it should; nothing else is allowed to pace the project.

Loop 34 of 50 complete. Resolved: I-84, I-85. Confidence: 9/10.

---

## Loop 35 of 50 — Management operating system & KPIs (Depth)

**Issues identified:**
- I-86: No production management system defined — world-class fab shops run on a short-interval cadence, not monthly surprises.

**Resolutions:**
- I-86 → Resolved (plan §8 extension): daily 10-minute tier meeting at the drum board; KPIs: **(1) drum schedule attainment** (weldments off fixture vs. plan, target ≥95%), **(2) weld-dept hours/unit** (start 16.5, target 14.5 by M12 via learning curve), **(3) first-pass yield** (target ≥97% after FA), **(4) kit buffer days** (target 4–6), **(5) safety/IH events** (target 0), **(6) cost/unit vs. $3,352 model** (monthly). Weekly: lead reviews trend + one improvement action. Monthly: Jeff reviews the six KPIs + savings vs. plan on one page. Escalation rule: two consecutive days of missed drum attainment triggers overtime authorization automatically (pre-approved, no meeting needed).

**Algorithm pass:** *Question:* challenged adding any reporting at all — kept the minimum that protects the drum and the savings claim; six numbers, one page. *Delete:* deleted the monthly "all-hands fab review" idea; the one-pager replaces it. *Simplify:* KPI data comes from the traveler and NetSuite work orders already being created — zero new data entry. *Accelerate:* the 16.5→14.5 hr/unit learning target is the only sanctioned efficiency program; everything else waits until it's stable.

**Constraint check:** every KPI either measures the drum or protects it; none measure non-constraint busyness. Deliberate.

Loop 35 of 50 complete. Resolved: I-86. Confidence: 9/10.

---

## Loop 36 of 50 — Layout and material flow (Depth)

**Issues identified:**
- I-87: Square footage existed but no adjacency/flow layout; crane coverage unverified against flow.

**Resolutions:**
- I-87 → Resolved: block layout added to plan §4: dock → receiving/racks → kitting → [gantry run 1: weld cell A + weld cell B] → inspection/straightening (under gantry run 2) → powder staging at dock (same dock, opposite side). Flow is a U: one dock serves inbound kits and outbound/inbound powder runs. Longest crane-assisted move ≈ 80 ft; no weldment is ever forklift-carried (gantry + powered cart only); legs flow on a parallel bench lane without touching the gantry. Aisle width 12 ft for the 16-ft cart turns; checked against a 15.4-ft load envelope.

**Algorithm pass:** *Question:* two gantry runs or one long one? Two short runs beat one 120-ft run on cost and on simultaneous lift conflicts (weld cell unload + inspection lift happen daily at the same hour). *Delete:* deleted the separate powder-staging room — it's dock-side floor tape, not walls. *Simplify:* U-flow means one dock door owns all freight; receiving rules fit on one laminated page. *Accelerate:* none.

**Constraint check:** layout minimizes drum-adjacent handling: kit staged at cell the prior afternoon by ops tech; welders never leave the cell to fetch.

Loop 36 of 50 complete. Resolved: I-87. Confidence: 9/10.

---

## Loop 37 of 50 — Maintenance, spares, fixture crash recovery (Depth)

**Issues identified:**
- I-88: No PM program; the 4th MIG was "spare" without policy; fixture damage = single point of failure with no recovery plan.

**Resolutions:**
- I-88 → Resolved: PM schedule — daily welder checks (liner, tips, ground) by operators; monthly gun/feeder service by lead; quarterly gantry hoist inspection (vendor contract, $4K/yr); annual fixture re-certification (laser tracker, $8K). 4th MIG formalized as **hot spare**: identical configuration, rotated into service monthly so it is never a stale spare. Fixture crash recovery: fixture design includes replaceable locator blocks (crash damage replaces blocks, not the frame); certified platen + manual layout method (Loop 21) is the documented degraded mode at 0.7/day; spare locator set ($6K) on the shelf. All inside the existing $20K/yr maintenance pool except the spare locator set (added to capex contingency).

**Algorithm pass:** *Question:* challenged the annual fixture re-cert — kept; it underwrites the fixture-as-gauge QA strategy, which is what lets us not own a CMM. *Delete:* deleted a CMMS/software purchase — the PM program is 9 recurring calendar events; a shared calendar does it. *Simplify:* one PM checklist per asset class, on the asset. *Accelerate:* hot-spare rotation (above) — zero-cost availability.

**Constraint check:** every PM item exists to keep the drum cycling; degraded-mode output (0.7/day) is defined so a fixture event is a slowdown, not a stop.

Loop 37 of 50 complete. Resolved: I-88. Confidence: 9/10.

---

## Loop 38 of 50 — Skills ladder and retention (Depth)

**Issues identified:**
- I-89: R-7 mitigation hired people but gave them nowhere to go — turnover risk stays high without progression.

**Resolutions:**
- I-89 → Resolved: three-step ladder — **Fab 1** ($24–26): legs + tack under supervision; **Fab 2** ($26–29): heavy weldout, owns a cell; **Fab 3** ($29–31): FA welder, WPS coupons, deputy lead; lead ($38+). Step-ups by demonstrated quals (documented coupon tests + 90-day FPY record), not tenure. Cross-training matrix: every welder reaches Fab 2 on both cell types within 9 months; ops tech trains to Fab 1 (emergency relief + a retention path for that role too). Cost: built into the wage band already budgeted; the ladder changes *sequence*, not totals. Expected effect: turnover assumption improves from 20% to ~12–15% (industry pattern for laddered shops); kept 20% in the financials (conservatism noted).

**Algorithm pass:** *Question:* challenged certifying everyone on everything — no; only to Fab 2 breadth (flexibility the drum needs), Fab 3 stays selective. *Delete:* deleted external "leadership training" line for the lead — replaced with CWI-prep sponsorship (~$2.5K), which the quality system actually uses (internal CAWI by M12 reduces contract-CWI spend). *Simplify:* qual records live in the same folder as welder continuity logs D1.1 already requires — one system. *Accelerate:* internal CAWI path (above) compounds: cheaper quals, faster FA dispositions.

**Constraint check:** ladder explicitly optimizes for drum flexibility (any two welders can pair on a heavy weldout by month 9).

Loop 38 of 50 complete. Resolved: I-89. Confidence: 9/10.

---

## Loop 39 of 50 — Procurement playbook & the TEEMS conversation (Depth)

**Issues identified:**
- I-90: The kit RFQ package contents were never specified (G-2 depends on quote quality).
- I-91: The TEEMS transition was a schedule, not a negotiation strategy; retaliation risk unaddressed (becomes I-95 stress in Loop 44).

**Resolutions:**
- I-90 → Resolved: RFQ package = 106900-R03 STEP/DXF set (already in hand, drawing note 8 makes CAD authoritative for undimensioned features), per-piece tube cut list with feature counts, 5-set batch quantity, kit packaging spec (sequenced skid, piece-marked), index-pricing clause (CRU/AMM monthly, no margin-on-material), 2-week firm lead, quality flow-down (MTRs per heat, dimensional cert on 5 features/batch). Award structure: primary + secondary processor, 70/30 split year 1 (the 30% keeps the second source warm for ~$3K/yr premium).
- I-91 → Resolved: negotiation sequence with TEEMS — (1) before any announcement, lock current R03 pricing on a 90-day blanket; (2) at M0, present the split: weldments transition in-house over M1–M9, TEEMS keeps decks + edge guards (~$320K/yr) and gets first right on the formed-sheet kit scope; (3) frame agreement: callable weldment capacity at last price +5% escalator, tooling retained. TEEMS's rational play is to keep the $320K annuity; the structure gives them one.

**Algorithm pass:** *Question:* who owns supplier management after SOP? The fab lead for kits (daily), Jeff/ops for TEEMS frame (quarterly) — named. *Delete:* deleted the idea of a formal dual-award for powder (two qualified, one primary, POs flex — no split commitment needed at $110K/yr). *Simplify:* every fab PO type (kits, powder, callable weldments) reduced to three template POs with attached specs. *Accelerate:* RFQ issues M0 week 1 (gates G-2).

**Constraint check:** 70/30 processor split and the powder dual-qual both exist to protect the drum's feed; neither adds fixed cost materially.

Loop 39 of 50 complete. Resolved: I-90, I-91. Confidence: 9/10.

---

## Loop 40 of 50 — Liability, traceability, and the weld that fails in the field (Depth)

**Issues identified:**
- I-92: **In-housing shifts structural liability from TEEMS to Slip.** A tray weld failure under a loaded SlipBot on a customer dock is a injury-capable event. Never addressed in Loops 1–25. (New risk **R-11** — the most important new finding of this phase.)
- I-93: Traceability requirements undefined.
- I-94: Design margin on welds is engineering's, not fab's — but fab inherits the blame.

**Resolutions:**
- I-92 → Resolved (mitigation, not elimination): product-liability insurance review with the broker *before* G-1 (**H-16**) — manufacturing operations change the policy class; budget placeholder +$15–25K/yr added to fixed pool (fixed rises to ~$361K; breakeven moves 12.8 → 13.5/mo; scenarios updated — the project still clears).
- I-93 → Resolved: serial-level traceability already designed (traveler) — extended to: welder ID per unit, WPS rev, wire heat/lot, kit batch (→ steel heat via MTR), powder lot, FA reference. Recall scope by serial is then a query, not an investigation. Cost ≈ $0 (fields on the existing traveler).
- I-94 → Resolved: request a one-time structural review memo from engineering (or external PE) documenting weld design margins on lifting interfaces and leg attachments (**H-14**); add UT spot-check of lifting-interface welds to FA units and quarterly audit units (~$1.5K/yr contract NDT). This is cheaper than the first field incident by orders of magnitude.

**Algorithm pass:** *Question:* does outsourcing back to a vendor actually transfer this risk today? Only partially — Slip designs the weldment and deploys it; the liability argument cuts both ways and was being used selectively. Honest framing added to §12. *Delete:* nothing — this loop adds (deliberately; deletion has an order, and safety items aren't deleted to make a model prettier). *Simplify:* traceability rides existing documents. *Accelerate:* none.

**Constraint check:** UT spot checks scheduled off-drum (FA/audit units only); no inline NDT bottleneck.

Loop 40 of 50 complete. Resolved: I-92..I-94. Risks: R-11. Human inputs: H-14, H-16. Confidence: 8/10 (honest dip — R-11 is real and was missed in the first 25).

---

## Loop 41 of 50 — Adversarial: kit quotes come back +25% (Stress 2)

**Scenario:** real quotes (H-7) land at $2,545/set instead of $2,035.

- I-95: At +25% kits, contribution falls to $1,716; breakeven ≈ 17.5/mo at the new $361K fixed — **above the original 13 and uncomfortably close to demand 22**. Annual at plan: +$51K. NPV flat: negative.
- Resolution: G-2 (Loop 34) is the designed defense — it now gets a hard number: **proceed only if quoted contribution ≥ $1,800/unit** (≈ kit-set ≤ $2,460). Below that: (a) re-quote with relaxed kit spec (Slip does its own piece-marking, −$60), (b) negotiate TEEMS weldment price using the should-cost (the model shows TEEMS's implied value-add ≈ $3,540/unit against ~$1,500 of burdened internal conversion cost — a renegotiation to ~$4,800–5,000 beats a thin make), (c) park the project, keep the model as leverage. Decision tree added to §12.

**Algorithm pass:** *Question:* is the $1,800 trigger arbitrary? No — it's the contribution at which the flat-case NPV @10% crosses zero with fixed at $361K. *Delete:* nothing. *Simplify:* one number (quoted contribution) decides G-2. *Accelerate:* none.

**Constraint check:** unchanged; this is a feed-cost scenario.

Loop 41 of 50 complete. Resolved: I-95 (as a gate rule). Confidence: 8/10.

---

## Loop 42 of 50 — Adversarial: weld hours run 30% over (Stress 2)

**Scenario:** actual weld-dept content is 21.5 hr/unit, not 16.5 (estimate risk R-2 realized).

- I-96: Drum load at 20/mo becomes 430+75+40 ≈ 545 hr vs. 490 capacity → **drum breaks**; and labor cost/unit +$175.
- Resolution: staged response — (1) overtime covers to ~23/mo equivalent for ≈$4.2K/mo premium; (2) hire welder 4 (capacity 640 hr, fixed +$73K, breakeven moves to ~15.7/mo — still under demand); (3) the Loop 35 learning program plus H-6 (stitch-weld relief) become priority engineering work with a quantified target instead of nice-to-haves. Contribution at 21.5 hr ≈ $2,051 — the project survives its most likely estimating error. FA builds (3 units) will measure true hours before rate commitment — the M5 gate G-3 now also captures an *hours* reading, not just quality.

**Algorithm pass:** *Question:* why trust 16.5 at all? Because it's now bounded: vendor price implies ~30–35 burdened shop-hours total including cut/form/coat at typical fab-shop rates — 16.5 weld-only is consistent, and the FA gate measures it before the org scales. *Delete:* nothing. *Simplify:* G-3 exit criteria = quality pass AND measured hours ≤19. *Accelerate:* none (automation still loses at these volumes even at 21.5 hr).

**Constraint check:** scenario is precisely a drum-capacity event; the staged response exploits (overtime) before elevating (4th welder) — ordering preserved.

Loop 42 of 50 complete. Resolved: I-96. Confidence: 8/10.

---

## Loop 43 of 50 — Adversarial: combined downside (Stress 2)

**Scenario:** kits +15%, hours +20%, volume 16/mo, insurance at the high end — simultaneously.

- I-97: Combined: variable ≈ $3,815 → contribution $1,763; fixed $366K; 192 units/yr → **−$28K/yr**. NPV @10% ≈ −$420K. The project does not survive all four hits at once.
- Resolution: honesty over optimism — stated in §12 and the exec summary. The joint probability is low (kit and hours errors are partially independent; volume 16 contradicts current actuals of 22) but not negligible. The defense is sequencing: G-2 catches the kit price *before* capex is committed (only ~$40K of fixture-design spend is at risk at G-2), and G-3 catches hours *before* the vendor is wound down. **Maximum regret if both gates are used properly ≈ $150K** (design spend + idle prep + restart friction), vs. $612K if gates are ignored. This reframes the risk: the gates, not the forecast, are the capital protection.

**Algorithm pass:** *Question:* would a world-class operator even start with this downside? Yes — because the gate structure converts a $612K bet into three sequential ~$50–200K bets, each with an exit. That is the difference between this plan and a leap. *Delete:* nothing. *Simplify:* regret math added as three lines in §9. *Accelerate:* none.

**Constraint check:** n/a (financial scenario).

Loop 43 of 50 complete. Resolved: I-97. Confidence: 8/10.

---

## Loop 44 of 50 — Adversarial: TEEMS reacts badly (Stress 2)

**Scenario:** TEEMS, on hearing the plan, raises piece-part prices 20%, refuses the frame agreement, or cuts Slip off mid-transition.

- I-98: Exposure quantified: stay-buy scope at TEEMS ≈ decks + edge guards ≈ $320K/yr (a 20% hit = $64K/yr); a hard cutoff during M1–M6 strands up to 5 weeks of pipeline (~$140K of trays delayed, not lost).
- Resolution: (1) decks and edge guards are conventional laser/form/paint work — quotable by the kit processors; pre-quote them in the same RFQ (zero extra effort, instant second source); (2) build a 2-week finished-weldment safety stock (10 units ≈ $56K, temporary, M1–M9 only) before the announcement; (3) sequence the conversation per Loop 39 — TEEMS hears the offer (keep $320K/yr + formed-kit first right) in the same meeting as the news. Residual risk: low. R-6 updated to cover transition behavior explicitly.

**Algorithm pass:** *Question:* could we simply not tell TEEMS until qualified? Rejected — POs visibly shrink regardless; surprise maximizes retaliation. Transparency with an offer attached is the strategy. *Delete:* the temporary safety stock auto-deletes at M9 (sunset written into the plan so it doesn't become permanent inventory). *Simplify:* one RFQ covers kits + deck second-sourcing. *Accelerate:* none.

**Constraint check:** safety stock protects assembly (the customer of the drum) during the riskiest window; it is buffer, not WIP creep, and it has an expiry date.

Loop 44 of 50 complete. Resolved: I-98. Confidence: 8/10.

---

## Loop 45 of 50 — Adversarial: the upside arrives early (Stress 2)

**Scenario:** demand hits 30/mo in year 1 while wood ramps to 10/mo simultaneously (fleet growth: the Denton-style multi-site deployments become routine).

- I-99: Single-shift drum caps at 22; demand 30 → 8/mo short; TEEMS callable capacity covers ~5–6/wk but at +5% price; risk of the worst of both worlds (full fixed cost AND vendor premium).
- Resolution: trigger ladder formalized (plan §8): sustained >20/mo for 8 weeks → authorize second-shift hiring (lead time ~8 weeks, +3 welders) and the tack jig ($30K); the callable TEEMS frame bridges the 8-week hiring window. At 30/mo two-shift: +$405K/yr net; at 40/mo: +$650K. Wood at 10/mo adds 75 hr/mo of legs — absorbed by shift 2's slack. The early-upside case is the best case and needs no new analysis, only the pre-authorized triggers so nobody waits for a quarterly meeting to act.

**Algorithm pass:** *Question:* should the second fixture come before the second shift? No — shift 2 on one fixture is $30K capex vs. $115K, and the fixture is idle 16 hr/day; elevate only at >44/mo. *Delete:* nothing. *Simplify:* growth playbook = two pre-authorized triggers with owners. *Accelerate:* this loop IS the accelerate step for the whole plan — growth response time cut from ~1 quarter to ~8 weeks.

**Constraint check:** exploit (shift 2) before elevate (fixture 2) — explicitly sequenced; TEEMS frame is the buffer during elevation.

Loop 45 of 50 complete. Resolved: I-99. Confidence: 9/10.

---

## Loop 46 of 50 — Adversarial: a weld fails at a customer site (Stress 2)

**Scenario:** month 14, a leg-attachment weld cracks on a deployed tray under load. No injury — this time.

- I-100: Containment and response never scripted; in the moment, improvisation is expensive and visible to a customer.
- Resolution: response runbook added to plan §5: (1) serial → traceability query: welder, WPS, wire lot, kit batch, FA reference, sibling serials (minutes, not days); (2) containment: UT inspection of sibling-serial trays at affected sites, field-weldable repair procedure pre-written by engineering (H-14 memo covers repair quals); (3) root cause: CWI-led, 8D format, feeding the FPY KPI; (4) customer comms owned by Jeff/account team with the traceability facts in hand. Drill once during M8 (tabletop, 2 hours). The same runbook covers vendor-welded trays (most of the fleet for years) — this gap exists today regardless of the make decision, which is worth saying out loud.

**Algorithm pass:** *Question:* does this risk argue for staying with the vendor? Examined honestly: vendor welds have the same field-failure mode with *less* traceability (no serial-level welder/lot data from TEEMS today). In-house with traceability is arguably the lower-liability configuration — reversing the naive read of R-11. §12 updated. *Delete:* nothing. *Simplify:* one runbook, both sourcing modes. *Accelerate:* none.

**Constraint check:** n/a.

Loop 46 of 50 complete. Resolved: I-100. Confidence: 9/10.

---

## Loop 47 of 50 — Adversarial: management attention is the scarcest input (Stress 2)

**Scenario:** the true cost nobody budgets — Jeff's and engineering's attention M0–M9, while the core robot business is scaling.

- I-101: Opportunity cost unpriced; project failure mode "orphaned initiative" is more common than any technical failure.
- Resolution: priced and bounded — Jeff/ops-engineer at ~50% M0–M2 (gates, lease, hires), ~20% M3–M6, ~5% after the lead owns operations (M9). Engineering: ~3 weeks total (H-2, H-6, H-13, H-14 + FA dispositions). If that attention cannot be committed, **the right call is the renegotiate-don't-build branch** — stated as a first-class outcome, not a failure. Mitigations that buy attention back: the fab lead is hired *early* precisely to absorb M3+ load; the contract CWI owns the quality-system build; gates G-1/G-2/G-3 are the only mandatory Jeff touchpoints after M1.

**Algorithm pass:** *Question:* the project's real owner after M9 — named role (fab lead) with the KPI one-pager as the contract. *Delete:* deleted every recurring meeting except the daily tier (10 min, lead-run) and the monthly one-pager. *Simplify:* Jeff's total decision surface = 3 gates + 2 growth triggers + 13 H-items, most front-loaded. *Accelerate:* none.

**Constraint check:** in the implementation phase, the constraint is leadership attention, not the weld cell — the plan now subordinates to it (fewest possible decisions, front-loaded, with pre-written criteria).

Loop 47 of 50 complete. Resolved: I-101. Confidence: 9/10.

---

## Loop 48 of 50 — Adversarial: macro swings (Stress 2)

**Scenario:** recession cuts deployments 30% for 12 months; separately, tariff/freight shocks raise vendor fab pricing 15%.

- I-102: Both directions tested with economics v2: recession (14/mo) → +$8K/yr at v2 numbers (still above water, vs. −$43K in v1 — the corrected buy price helps); tariff shock → buy +$837/unit vs. make +$280 (kits are 60% material; vendor price is ~100% pass-through-able) → make advantage widens to ~$2,780/unit. The make position is counter-cyclically *protective* on cost and pro-cyclically valuable on lead time. Asymmetry noted in §12 as a genuine strategic property, not a sales line.
- Resolution: I-102 closed; sensitivity table gains both rows.

**Algorithm pass:** *Question:* does any macro path favor pure-buy? Yes, one: prolonged demand <12/mo — already the hibernation/renegotiate branch. The options map is now exhaustive. *Delete:* nothing. *Simplify:* macro rows reuse the same contribution arithmetic. *Accelerate:* none.

**Constraint check:** unchanged.

Loop 48 of 50 complete. Resolved: I-102. Confidence: 9/10.

---

## Loop 49 of 50 — Audit pass: recompute everything (Verification)

**Issues identified:**
- I-103: Two loop phases of edits risk internal inconsistency across five documents.
- I-104: **Audit finding — the contribution method double-counts welder utilization.** Loops 32–48 priced direct labor per unit (16.5 hr × $35.10) inside contribution, but the welders are salaried full-time; per-unit allocation accounts for only ~$208K of the $289K welder+ops payroll. Annual figures built from contribution × volume therefore overstate savings unless utilization is perfect. World-class discipline: the annual P&L must carry **full payroll**, not allocated hours.

**Resolutions — full restatement on a cash P&L basis (steady state, 20 heavy + 10 wood/mo):**

| | $K/yr |
|---|---|
| Avoided buy: 240 weldments × $5,577.84 + 720 wood legs × $122.71 | **1,427** |
| Kits (heavy 240 × $2,035; wood legs 720 × $48) | −523 |
| Powder (incl. freight) | −111 |
| Consumables | −38 |
| Payroll, full (3 welders + lead + ops tech, loaded) | −396 |
| Facility + utilities | −150 |
| Maintenance/cal/PPE | −20 |
| Liability insurance delta (H-16 midpoint) | −20 |
| NDT, requals, CoQ extras | −15 |
| **Net cash savings, steady** | **≈ +$155** (yr-1 ≈ +$120 with learning/CoQ) |

- Other restated headlines: **cash breakeven ≈ 15 heavy/mo** (payroll steps down at low volume; −40% case ≈ −$10K, hibernation path intact); 2× volume (two shifts) ≈ **+$525K/yr**; 30/mo ≈ **+$270K/yr**. Unit-level contribution ($2,226) remains correct *for unit decisions* (e.g., legs make-or-buy, G-2 threshold) — the error was only in multiplying it by volume for annual claims.
- Cash curve restated: trough ≈ **−$700K at M6–M7** (capex $504K + overlap-period payroll/facility ~$200K + qualification builds, partially offset by early production and the M8 working-capital release of +$100K); cumulative cash breakeven ≈ **M38 flat / ≈M25 growth path**.
- NPV (5-yr, cash basis): **≈ −$30K flat / +$310K growth path @10%** (IRR ≈ 9% / ≈22%); at a 20% venture hurdle: clearly negative flat / ≈ +$150K growth. **The flat case is NPV-neutral at best — the project is justified by the growth path and the strategic position, and the gates must say so plainly.** Exec summary and §9 rewritten accordingly.
- Gate review against restated numbers: breakeven 15 < gate 18 < demand 22 — the gate still sits correctly between viability and actuals; G-2 contribution floor ($1,800/unit) unchanged.
- Maximum-regret restated: exit at G-2 ≈ −$50K; exit at G-3 ≈ −$400K (capex + ramp spend, net of ~60% equipment resale); ignoring gates ≈ −$700K.
- Cross-document check: 00/01/03/06 now carry P&L-basis numbers; contribution-basis figures in Loops 32–48 stand as written history with this loop as the correction of record.
- I-103, I-104 → Resolved.

**Algorithm pass:** *Question:* one final challenge — is anything in the plan still owned by nobody? Sweep found one: the powder vendor relationship post-SOP — assigned to ops tech (daily logistics) + lead (quality). *Delete:* final deletion sweep found one survivor to kill: the 2-week finished-weldment safety stock had no explicit owner for its M9 sunset — owner assigned (lead), sunset confirmed. *Simplify:* exec summary rewritten to lead with the gate logic and the honest NPV split (the actual decision), not a single savings number. *Accelerate:* none — audit loops don't accelerate.

**Constraint check:** all numbers reconcile to a drum at 91% with overtime headroom; no document claims capacity the drum doesn't have. The restatement does not change the drum, the gates, or the recommendation's direction — it changes how honestly the flat case is described.

Loop 49 of 50 complete. Resolved: I-103, I-104. Confidence: 9/10.

---

## Loop 50 of 50 — Synthesis v2

The second 25 loops changed the plan in six material ways:

1. **The buy price was understated 6.8%** — current R03 POs run $5,577.84 (and opened at $5,868.33 on the rev change). Make economics improved net of the steel-price correction: contribution **$2,226/unit**.
2. **Demand is evidenced, not assumed** — work orders run 21–22/month, scheduled through late July, with surge weeks to 10. The volume gate's evidence half is satisfied today; the commitment half (H-11) remains Jeff's.
3. **The vendor picture is concrete** — TEEMS is a single source delivering ~25/month at most; at growth, the buy path hits a capacity wall that the make path removes. Wood-tray volume (3 work orders ever) is aspirational — the plan no longer leans on it.
4. **Liability and traceability were missing** (R-11) — now mitigated with insurance review (H-16), serial-level traceability at ~zero cost, UT spot checks, a PE design-margin memo (H-14), and a field-failure runbook that Slip needs *regardless* of sourcing.
5. **The financial model grew up — and got more honest.** Monthly cash to M24, NPV/IRR at two hurdle rates, working-capital release (+$100K), insurance in fixed costs, and the Loop 49 audit restatement to a full-payroll cash P&L: steady-state savings are **+$155K/yr at 20/mo** (not the contribution-method $173K), NPV ≈ **zero flat / +$310K growth @10%**, cash trough **−$700K**, and a regret analysis: with gates G-1/G-2/G-3 used properly, maximum capital at risk before each exit is ~$50K / ~$400K — the gates, not the forecast, protect the capital.
6. **The plan can now be operated, not just approved** — KPI system, PM/spares/crash-recovery, skills ladder, procurement playbook, TEEMS negotiation sequence, growth triggers, and a field-incident runbook, each with an owner.

**Recommendation (unchanged in direction, upgraded in basis and honesty): HYBRID — proceed through the three gates.** G-1 now (volume commitment + insurance read), G-2 at ~M1 (real kit/powder quotes; proceed iff contribution ≥ $1,800/unit), G-3 at ~M5 (FA quality AND measured hours ≤19). On the restated cash P&L: **+$155K/yr at today's 20/mo, +$525K/yr at 2×; NPV ≈ break-even flat / +$310K growth @10%.** The flat case alone does not justify the project at a venture hurdle rate — the committed growth path (H-11), the vendor capacity wall at ~25/mo, the measured rev-change pricing tax, and the lead-time position do. Below 15/mo or failing G-2, take the renegotiation branch armed with the should-cost model.

Final registers: I-01..I-103 all dispositioned; A-1..A-9 (two superseded, marked); H-1..H-16 open for Jeff/company. Confidence: **9/10** — the residual tenth is exactly what G-2 and G-3 are designed to retire.

Loop 50 of 50 complete.
