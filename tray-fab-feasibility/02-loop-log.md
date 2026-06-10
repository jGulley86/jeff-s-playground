# Loop Log — 25 Self-Correcting Loops

Issues are numbered I-nn (cumulative, never deleted — see `03-registers.md` for final state).
Assumptions are A-nn; human inputs are H-nn. Confidence is for the overall plan, 1–10.

---

## Loop 1 of 25 — Scope and baseline (Breadth)

**Issues identified:**
- I-01: "Light Tray" is ambiguous — NetSuite has 106997 LIGHT TRAY ($6,593.75) but the uploaded package is 107455 WOOD TRAY. Which family does the 10/month apply to?
- I-02: Fabrication scope boundary unclear — heavy decks are painted steel panels and DeckOver non-skid is applied somewhere; wood decking is lumber. What exactly hands off to assembly?
- I-03: No takt definition yet.

**Resolutions:**
- I-01 → Resolved: treat Wood Tray 107455 as the light family (it is the released package supplied; 106997 appears superseded). Logged A-1 and H-1 (Jeff to confirm).
- I-02 → Resolved: in-scope = steel weldments, steel piece parts, and their powder/prep, ending at coated, inspected steel handed to assembly. Heavy steel decks are fab parts; DeckOver application and lumber decking stay with assembly (current practice per BoM — DeckOver Paint is a tray-level BoM line consumed at assembly). Logged A-2.
- I-03 → Resolved: 20 working days/month → takt = 1 heavy tray/day and 1 wood tray every 2 days; fab plans to a daily drumbeat of 1 heavy weldment + 0.5 wood tray steel set.

**Algorithm pass:** *Question:* who owns the requirement that fab must replicate the vendor's full scope (cut→form→weld→coat)? Nobody internally — it's inherited from how the vendor quotes. Scope is negotiable per process step. *Delete:* in-house finishing (powder booth + oven for 16-ft parts) — deleted; outsource powder coat. *Simplify:* treat the two tray families as one shared routing with different work content. *Accelerate:* nothing yet — too early.

**Constraint check:** drum provisionally = the weld cell (most labor-dense step). All later equipment decisions must subordinate to it.

Loop 1 of 25 complete. Resolved: I-01..I-03. Open: none carried. Assumptions added: A-1, A-2. Confidence: 2/10.

---

## Loop 2 of 25 — Cutting technology and routing skeleton (Breadth)

**Issues identified:**
- I-04: Tube cutting method undecided — 25 tube pieces/heavy tray with laser-cut locating cut-outs ("fitment of tubes into cut-outs defines positional tolerance," note 11). A saw cannot make those features.
- I-05: No routing exists per family.
- I-06: Weld content per heavy tray unquantified — everything downstream depends on it.

**Resolutions:**
- I-04 → Resolved: three options — (a) tube laser ($450–900K used), (b) saw + CNC plasma coping (~$120K, slower, dross cleanup), (c) buy laser-cut tube kits from a service center. At 20/month (≈ 21,000 lb tube/mo) a tube laser is idle >80% of the time. Choose (c): buy cut kits. Capex avoided; revisit at 2× volume (I-04 stays linked to stress loop 19).
- I-05 → Resolved: first-draft routings written into plan §1 (receive → kit verify → fixture fit/tack → weldout → inspect/straighten → outsource powder → final QA → handoff).
- I-06 → Partially resolved: placeholder 1,500 weld-inches/heavy weldment, flagged for hard calculation in depth phase (reopened as I-20 in Loop 9).

**Algorithm pass:** *Question:* challenge "fab must cut its own steel" — rejected; cut kits are a commodity in the Atlanta market. *Delete:* tube laser purchase — deleted before it was ever bought. *Simplify:* one kit P/N per weldment rev (single PO line, single receipt). *Accelerate:* none.

**Constraint check:** drum = weld cell. Buying kits protects the drum (no upstream machine downtime can starve it if kits carry 2-week buffer).

Loop 2 of 25 complete. Resolved: I-04, I-05; I-06 partial. Open: I-06. Assumptions added: A-3 (kit pricing ≈ 1.9× material, basis: regional service-center quotes pattern). Confidence: 3/10.

---

## Loop 3 of 25 — Staffing first pass (Breadth)

**Issues identified:**
- I-07: No headcount model.
- I-08: Welder qualification requirements undefined (drawing invokes fillet sizes/tolerances but no AWS code reference found on the weldment drawing).
- I-09: Atlanta-area wage basis missing.

**Resolutions:**
- I-07 → Resolved (draft): 3 welders + 1 working fab lead + 1 ops tech (kitting/QA/material), single shift. Hard math deferred to Loop 14.
- I-08 → Resolved: adopt AWS D1.1 structural code as internal standard (industry default for structural carbon-steel tube/plate weldments rated for payload); welders qualified to D1.1 fillet + groove on 1/8" wall tube; WPS/PQR written by a contract CWI. Logged H-2 (engineering to confirm code/spec intent — drawings don't call a code explicitly).
- I-09 → Resolved: Norcross/Atlanta market — MIG fabricator-welder $24–29/hr, working fab lead $36–40/hr, fab ops tech $22–26/hr (basis: 2025–26 metro Atlanta fabrication postings; loaded factor 1.35). Logged A-4.

**Algorithm pass:** *Question:* does fab need its own supervisor, or can it report to the existing production manager? Challenged — kept a *working* lead, deleted a non-working supervisor layer. *Delete:* dedicated QA inspector role — deleted; lead + ops tech carry inspection with a contract CWI for setup (partially added back in Loop 22). *Simplify:* one shift only; overtime is the surge mechanism. *Accelerate:* none.

**Constraint check:** drum = weld cell → staffing subordinates: the only roles added are those that keep welders welding (kitting, inspection, material moves done by ops tech, not welders).

Loop 3 of 25 complete. Resolved: I-07 (draft), I-08, I-09. Open: I-06. Assumptions: A-4. Confidence: 3/10.

---

## Loop 4 of 25 — Facility first pass (Breadth)

**Issues identified:**
- I-10: Footprint by function unknown; 15.5-ft, 1,179-lb weldments need defined handling.
- I-11: Crane vs. forklift vs. gantry undecided; ceiling height at 1275 Oakbrook unverified.
- I-12: Does the Oakbrook lease/landlord permit welding (hot work) occupancy?

**Resolutions:**
- I-10 → Resolved (draft): 9,000 SF within 1275 Oakbrook: receiving/raw 1,500; kitting 500; 2 heavy weld cells 1,600; small-weldment cell 400; inspect/rework 600; powder out/in staging 800; WIP 1,200; aisles 2,400. Detailed load calcs deferred (Loop 13).
- I-11 → Resolved: freestanding 5-ton gantry crane runs over the weld cells + 5K-lb forklift for everything else. Avoids building-structure dependency. H-3: confirm Oakbrook clear height ≥ 18 ft in the fab bay.
- I-12 → Logged H-4 (lease use clause, landlord consent, insurance rider). Cannot be resolved internally; risk R-3 opened.

**Algorithm pass:** *Question:* challenge the assumption that fab must be at Oakbrook — it could lease cheap nearby flex space; kept at Oakbrook for shared management/forklifts/receiving (and the building is already being evaluated at 43,790 SF). *Delete:* building bridge crane — deleted in favor of freestanding gantries (no structural reinforcement, no landlord work). *Simplify:* powder staging combined with shipping dock area (shared dock door). *Accelerate:* none.

**Constraint check:** drum = weld cell; facility spend concentrates there (gantry coverage, fume capture, fixtures). No spend on cutting/forming space — consistent with kit strategy.

Loop 4 of 25 complete. Resolved: I-10 (draft), I-11. Open: I-06, I-12(H-4). Assumptions: A-5 (Oakbrook fab allocation at $10/SF loaded). Confidence: 4/10.

---

## Loop 5 of 25 — Quality and EHS first pass (Breadth)

**Issues identified:**
- I-13: No incoming/in-process/final inspection plan.
- I-14: Weld fume exposure control undefined (A36/ER70S-6 → manganese fume; OSHA action levels).
- I-15: First-article method for a 15.5-ft weldment with ±0.02 two-place tolerances undefined.

**Resolutions:**
- I-13 → Resolved: incoming = kit count + MTR check + spot dimensional on 5 features/kit; in-process = fillet gauge checks per joint class + 100% visual per D1.1 Table 6.1 acceptance; final = fixture-based go/no-go on interface features (foot mounts, lifting interfaces, deck tabs) + powder thickness check (2–3 mil per drawing block).
- I-14 → Resolved: source-capture fume guns or extraction arms at each cell + ambient ventilation; baseline industrial-hygiene survey in month 1 of production for Mn (OSHA PEL 5 mg/m³ ceiling; ACGIH TLV 0.02 mg/m³ respirable — design to the stricter), PAPR welding helmets if sampling exceeds. Costed in capex.
- I-15 → Resolved: the weld fixture itself is the master gauge — fixture certified once by a laser-tracker service (~$8K), then first articles measured on-fixture + critical free-state dims with a rented FARO arm. Avoids buying a CMM (ties to Delete in Loop 12).

**Algorithm pass:** *Question:* does every weldment need full dimensional layout? No — only first articles and after fixture changes; production uses interface go/no-go. *Delete:* in-house blast cabinet — deleted; the powder vendor owns surface prep (their standard process includes wash/blast). *Simplify:* one inspection traveler per tray serial, shared QA form across both families. *Accelerate:* none.

**Constraint check:** drum = weld cell. Inspection happens off-drum (ops tech inspects while welders start the next unit); fixture-as-gauge avoids a measurement queue at the drum.

Loop 5 of 25 complete. Resolved: I-13..I-15. Open: I-06, I-12. Confidence: 4/10.

---

## Loop 6 of 25 — Consumables + financial skeleton (Breadth)

**Issues identified:**
- I-16: Consumables unquantified.
- I-17: No make-vs-buy financial model exists.
- I-18: Powder-coat outsource price for a 16-ft, 1,179-lb weldment unknown.

**Resolutions:**
- I-16 → Resolved: per heavy weldment — ~39 lb deposited weld metal → ~45 lb wire @ $1.60/lb = $72; shielding gas (C25) ≈ $30; tips/nozzles/abrasives/anti-spatter ≈ $28 → ≈ $130/heavy unit; ≈ $10 per wood leg. Basis: deposition math (Loop 9) + catalog pricing.
- I-17 → Resolved (skeleton): annual model built — buy baseline $1.88M vs. make (hybrid) draft $1.7M; structure in plan §9, numbers hardened Loops 11–17.
- I-18 → Resolved as estimate: $425/heavy weldment (basis: $0.30–0.40/lb batch powder for large parts, Atlanta market, plus 16-ft handling premium); $12/leg batch rate. Logged H-5 — get two real quotes; parts this long exceed some vendors' ovens.

**Algorithm pass:** *Question:* challenge DeckOver as a fab cost — confirmed assembly-side (BoM places it at tray level), excluded. *Delete:* flat laser and press brake — deleted; formed sheet parts (cosmetic plates, bent supports, leg-hole bent sheets) arrive in the kits. *Simplify:* consumables on vendor-managed inventory (VMI) bin program — no purchasing labor. *Accelerate:* none.

**Constraint check:** drum = weld cell; nothing purchased this loop touches non-drum capacity.

Loop 6 of 25 complete. Resolved: I-16, I-17 (skeleton), I-18 (estimate). Open: I-06, I-12. Assumptions: A-6 (powder pricing). Confidence: 5/10.

---

## Loop 7 of 25 — Throughput & constraint draft (Breadth)

**Issues identified:**
- I-19: Drum capacity vs. load not yet computed; buffer and rope undefined.

**Resolutions:**
- I-19 → Resolved (draft): weld-cell load ≈ 445 hr/mo vs. ≈ 490 hr/mo capacity (3 welders + lead at 50%) → 91% drum utilization. Buffer: 5 working days of kits ahead of the drum (≈ 5 heavy + 3 wood kit-sets). Rope: kit releases (PO call-offs) are triggered by drum completions, not by forecast — a kanban of 7 heavy kit-sets total in the loop. Detail hardened in Loop 10.

**Algorithm pass:** *Question:* is 91% drum utilization acceptable? Challenged — TOC says the drum should run hot but 91% with no proven cycle times is optimistic; flagged R-5 (ramp risk) and kept overtime as protective capacity. *Delete:* attempted to delete the second heavy weld fixture from the capex list — deleted (one fixture, one-piece flow; tack and weldout on the same fixture). Watch: may return at higher volume. *Simplify:* weldment flows through exactly one cell (no transfer between tack and weldout stations) — fewer crane moves, less distortion risk. *Accelerate:* none yet.

**Constraint check:** drum = the single heavy weldment fixture/cell, explicitly now (not just "welders"). Welders flex to the small-weldment cell when the fixture is occupied by tack-up.

Loop 7 of 25 complete. Resolved: I-19 (draft). Open: I-06, I-12. Confidence: 5/10.

---

## Loop 8 of 25 — Timeline, risk register, first recommendation (Breadth — all sections drafted)

**Issues identified:**
- I-20: (reopens I-06 formally) Weld inches still a placeholder.
- I-21: Weldment component weights sum to ≈1,287 lb vs. 1,179 lb drawing total — 9% discrepancy.
- I-22: No supplier wind-down/overlap plan; single-source risk during transition.

**Resolutions:**
- I-20 → Carried to Loop 9 (depth phase begins).
- I-21 → Resolved: drawing CAD total (1,178.672 lb) governs for handling/powder math; the discrepancy is attributed to rev-level quantity changes in the extracted parts list (e.g., item 17 added at R02 may overlap item 10 usage). Material purchasing uses the kit BoM, so the error does not propagate to cost. Documented in data basis.
- I-22 → Resolved: keep the incumbent vendor live through qualification: months 1–6 vendor at full rate, month 7 vendor 50%, months 8–9 vendor as paid standby (2 units/mo), then PO-on-demand. Risk R-6 logged with this mitigation.

**Algorithm pass:** *Question:* challenge the implicit requirement to in-source both families simultaneously — rejected as a requirement; heavy weldment is 81% of the addressable spend and goes first; wood-tray steel piece parts stay purchased indefinitely (only wood legs come in-house, as drum filler). *Delete:* wood-tray bracket/plate fabrication — deleted permanently from scope. *Simplify:* implementation now has one critical path: fixture design → build → first article. *Accelerate:* order long-lead fixture steel at design 60% release.

All 12 sections now have a complete first draft. Make/Buy/Hybrid draft recommendation: **Hybrid** (weld in-house from purchased cut kits; outsource powder; keep buying decks, small parts, heavy legs).

**Constraint check:** drum = heavy weldment fixture. Vendor-overlap plan exists specifically to protect the drum during its least reliable period (ramp).

Loop 8 of 25 complete. Resolved: I-21, I-22. Open: I-20, I-12. Confidence: 5/10.

---

## Loop 9 of 25 — Weld content hardened (Depth)

**Issues identified:**
- I-23: Joint-by-joint weld length never computed (closes I-20).
- I-24: Drawing note 14 ("all tube welded all-around at all joints") is a major cost driver — is it structurally necessary everywhere?
- I-25: Weld deposition assumptions (rate, operating factor) unstated.

**Resolutions:**
- I-23 → Resolved by joint count: tube-to-tube all-around joints — 8× B3 (4×2: 12 in/joint-end ×2 ends) = 192 in; 4× B4 (5×2: 14 in ×2) = 112 in; ~6 joints of 6×3 members (18 in ×2) = 216 in; 5 small 4×2 joints = 120 in → tube ≈ 640 in. Plates: lifting 2×40=80; foot mounts 8×30=240; center reinforcement stitch 2×120=240; cosmetic stitch ≈100; tabs 8×8=64; bent supports 6×10=60 → plate ≈ 784 in. **Total ≈ 1,425 weld-inches**, rounded to 1,450 for planning. Deposited metal at 0.25" fillet ≈ 0.027 lb/in → ≈ 39 lb/weldment.
- I-24 → Cannot be resolved internally: logged H-6 — engineering review of note 14; converting non-structural joints to stitch welds could cut 15–20% of arc time. Plan does NOT bank these savings.
- I-25 → Resolved: pulse-MIG spray, 9 lb/hr deposition, 40% arc-on operating factor in fixtured work (basis: AWS/Lincoln semi-automatic benchmarks for fixtured weldments) → 39 lb ÷ 9 ÷ 0.40 ≈ **10.8 hr weldout**; + fit/tack 4.5 hr (two-person 2.25 hr) + grind/touch/straighten 1.2 hr → **16.5 weld-dept hr/heavy weldment**.

**Algorithm pass:** *Question:* note 14 challenged (above, H-6). *Delete:* attempted to delete the straightening step — kept (1,179-lb frame with quarter symmetry will move when welded; deleting it would surface as first-article failure). This is the loop where deletion failed honestly. *Simplify:* weld sequence documented once in the WPS travel sheet (balanced, quarter-symmetric sequence to control distortion). *Accelerate:* evaluated robotic/cobot weldout — rejected at 20/mo (fixturing investment > labor saved; and per the Algorithm, do not automate joints that H-6 may delete).

**Constraint check:** drum load recomputed with 16.5 hr: heavy 330 hr + wood legs 75 hr + 10% rework/FA allowance ≈ 445 hr/mo. Holds.

Loop 9 of 25 complete. Resolved: I-23, I-25; I-24 → H-6. Open: I-12. Confidence: 6/10.

---

## Loop 10 of 25 — Cycle times & utilization model (Depth)

**Issues identified:**
- I-26: Non-weld cycle times (receiving, kitting, inspection, load/unload) unmodeled.
- I-27: Daily schedule doesn't prove 1 heavy/day is achievable on one fixture.
- I-28: Wood-leg weld time is a guess.

**Resolutions:**
- I-26 → Resolved: per heavy unit — receive/kit verify 0.8 hr; fixture load/unload (crane) 0.6 hr; final inspect + traveler 0.7 hr; powder logistics (load truck, receive back) 0.5 hr → 2.6 ops-tech hr/unit (ops tech capacity 160 hr/mo vs. load 20×2.6 + wood 10×1.5 = 67 hr → ops tech also runs receiving and VMI; OK).
- I-27 → Resolved: fixture timeline — day 1: 0700 kit staged, two welders tack (2.25 hr), weldout split across both welders' stations? No — one fixture: tack 0700–0915, weldout 0915–1700 (one welder 10.8 arc-adjusted hr exceeds one shift) → resolved by pairing: weldout shared by 2 welders on opposite sides (balanced welding also controls distortion) → 10.8 ÷ 1.8 effective ≈ 6 hr elapsed → unit off fixture by ~1530, straighten/inspect off-line. One fixture sustains 1/day with 1.5 hr slack. Third welder runs wood legs + relief.
- I-28 → Resolved: wood leg weldment (107508): small fixture, ~8 lb-class part, est. 35 weld-in → 0.75 hr weld + 0.5 hr handling = 1.25 hr/leg → 75 hr/mo at 60 legs. Basis: scaled from heavy-leg analog (106911 at $79.71 vendor price implies <1.5 hr shop content).

**Algorithm pass:** *Question:* must straightening be a separate station? Yes (off-drum by design). *Delete:* deck fabrication permanently deleted from any future phase list (painted decks at $72–137 are efficient vendor parts; in-housing them would add a laser+brake+paint chain for ~$590/tray of low-margin content). *Simplify:* two-welder paired weldout becomes the standard method (also halves distortion risk). *Accelerate:* paired weldout is itself the acceleration; no automation.

**Constraint check:** drum = the single heavy fixture, proven at 1/day with slack. Capex stays subordinated: still one fixture.

Loop 10 of 25 complete. Resolved: I-26..I-28. Open: I-12. Confidence: 6/10.

---

## Loop 11 of 25 — Material & kit cost build-up (Depth)

**Issues identified:**
- I-29: Kit prices are a single multiplier assumption (A-3) — needs a bottom-up check.
- I-30: Scrap/yield unmodeled.
- I-31: Wood-tray steel weight never estimated (affects nothing big — bound it).

**Resolutions:**
- I-29 → Resolved bottom-up: tube kit — 1,007 lb + 8% drop = 1,088 lb @ $0.72/lb A500 = $783 material; tube-laser time ≈ 1.6 hr @ $165/hr = $264; handling/pack/margin ≈ $310 → **$1,360/kit**. Plate/formed kit — 181 lb + 15% skeleton = 208 lb @ $0.62 = $129; laser 0.9 hr @ $150 = $135; 22 bends @ $4 = $88; margin ≈ $95 → **$447/kit**. Close to A-3's 1.9× check ($1,807 vs $1,790). H-7: validate with two real quotes (Metals & Services, Ryerson Advanced Processing, or similar Atlanta processors).
- I-30 → Resolved: 2% weldment scrap/rework-to-scrap in year 1 (one lost unit per 50), falling to 0.5%; carried as $26/unit year-1 adder. In-process rework already in the 10% drum allowance.
- I-31 → Resolved as bound: wood-tray steel ≈ 450 lb ± 30% (two ~15-ft 4×2 tubes ≈ 145 lb + 12 brackets ≈ 100 lb + legs 6×~20 lb + sheet parts) — only used for handling/forklift sizing, not cost (those parts stay purchased). A-7 logged.

**Algorithm pass:** *Question:* why 8% tube drop? Because kits nest per-tray; challenged → nesting across 5-tray batches cuts drop to ~5%; adopted (kit PO releases in batches of 5, still consumed 1/day from buffer — rope unchanged). *Delete:* attempted to delete the plate/formed kit vendor (fold into tube vendor) — kept two vendors quoted but will award both scopes to one processor if pricing holds (simplification, not deletion). *Simplify:* single combined kit-set P/N per tray rev (tube + plate on one skid). *Accelerate:* batch nesting (above) — a real cost acceleration that only made sense after deletion of in-house cutting.

**Constraint check:** drum unaffected; kit batching of 5 respects the 5-day buffer exactly.

Loop 11 of 25 complete. Resolved: I-29..I-31. Open: I-12. Assumptions: A-7. Confidence: 6/10.

---

## Loop 12 of 25 — Per-tray cost build-up & breakeven (Depth)

**Issues identified:**
- I-32: No unit economics table; breakeven volume unknown.
- I-33: Labor rate loading factor unstated in math.
- I-34: Capex amortization policy unset.

**Resolutions:**
- I-32 → Resolved — heavy weldment make cost: kits $1,807 + powder $425 + consumables $130 + scrap adder $26 + direct weld labor 16.5 hr × $35.10 = $579 + ops-tech share 2.6 hr × $33.75 = $88 → **variable ≈ $3,055** vs. buy $5,221 → **contribution $2,166/unit**. Fixed pool (lead $107K, facility $150K, maintenance/cal/PPE $20K, fixtures+equip amortization $64K) ≈ $341K/yr → **breakeven ≈ 158 heavy-equivalent units/yr ≈ 13/mo** (wood legs contribute ~$3K/yr net — ignored in breakeven).
- I-33 → Resolved: 1.35 loading (FICA, GA SUTA, workers comp class 3365 ~$4–6/100, health, PTO) — stated everywhere as "loaded."
- I-34 → Resolved: 7-yr straight line on $450K equipment/fixtures (fixtures 5-yr); blended $64K/yr.

**Algorithm pass:** *Question:* challenge the $5,221 buy price as the comparison basis — is it stable? It's a real repeated PO price (avg = last). Kept, but steel-spike sensitivity assigned to Loop 24. *Delete:* FARO arm purchase ($75K) — deleted; rent one for first-article months (~$4K/mo × 2) and rely on certified fixture + interface gauges thereafter. *Simplify:* unit-economics table becomes the single source for all financial sections (no parallel models). *Accelerate:* none.

**Constraint check:** drum = heavy fixture. Note: breakeven (13/mo) < plan (20/mo) < fixture capacity (22/mo) — the economics close precisely because the drum is well-utilized; any capex that adds non-drum capacity worsens breakeven. Flagged and held.

Loop 12 of 25 complete. Resolved: I-32..I-34. Open: I-12. Confidence: 7/10.

---

## Loop 13 of 25 — Facility load calcs (Depth)

**Issues identified:**
- I-35: Electrical demand unsized.
- I-36: Compressed air & ventilation CFM unsized.
- I-37: Floor loading & gantry foundations unchecked.

**Resolutions:**
- I-35 → Resolved: 4× 450A pulse MIG @ ~22 kVA peak, 60% duty, diversity 0.6 → 53 kVA; gantry hoists 10; compressor (25 HP) 20; fume/ventilation fans 15; lighting/misc 15 → **≈ 115 kVA demand → 480V/200A feeder, spec 250A for headroom**. H-8: confirm Oakbrook spare service capacity.
- I-36 → Resolved: air — guns/tools/grinders ≈ 60 CFM peak → 25 HP rotary screw (~100 CFM) with dryer. Ventilation — 3 source-capture arms @ 1,000 CFM + ambient weld-area exchange ≈ 8,000 CFM roof fan; makeup air interlocked. Welding area separated by weld screens, not walls (fire watch line-of-sight).
- I-37 → Resolved: 1,179-lb part + 3,000-lb fixture + gantry point loads ≈ 12 kip/leg → standard 6" industrial slab OK with 18"×18" base plates; verify slab thickness via core or drawings (H-9). Raw/kit storage on cantilever racks: 5-tray kit batch ≈ 6,500 lb/bay — standard.

**Algorithm pass:** *Question:* is 9,000 SF actually needed? Re-measured: cells+inspection+kitting are 5,100 SF; storage/WIP/aisles flex with the building — could compress to 7,500 SF if Oakbrook space is tight. Plan keeps 9,000 nominal / 7,500 minimum. *Delete:* dedicated rework bay — deleted; straightening happens at the inspection table with the gantry. *Simplify:* one gas manifold (bulk-mix C25 cylinders banked) instead of per-station cylinders — fewer changeouts, steadier mix. *Accelerate:* none.

**Constraint check:** drum protected by facility design: gantry coverage and fume capture sized for simultaneous paired weldout; power sized so adding a 4th active station (stress case) needs no service change.

Loop 13 of 25 complete. Resolved: I-35..I-37. Open: I-12. Confidence: 7/10.

---

## Loop 14 of 25 — Staffing math finalized (Depth)

**Issues identified:**
- I-38: Headcount vs. load never reconciled after cycle-time hardening.
- I-39: Hiring ramp and training plan missing.
- I-40: Absenteeism/turnover allowance missing.

**Resolutions:**
- I-38 → Resolved: monthly load — heavy weld 330 hr, wood legs 75 hr, rework/FA 40 hr → 445 hr vs. capacity: 3 welders × 150 productive hr = 450 + lead 40 = 490 → 91% planned, 99% without lead. Verdict: 3 welders is correct *only* with a welding lead. Headcount: 3 welders, 1 working lead, 1 ops tech = **5.0 FTE**; loaded payroll ≈ $396K/yr.
- I-39 → Resolved: hire lead at month 2 (joins fixture design reviews); welders 1–2 at month 3 (weld coupons, D1.1 quals, build leg fixtures); welder 3 at month 5; qualification builds months 4–5; rate by month 7. Training: contract CWI runs WPS/PQR + qual testing (~$15K).
- I-40 → Resolved: 150 productive hr/mo per welder already nets out PTO/indirect (8%); turnover assumption 20%/yr for welders (Atlanta market) → budget 1 requalification cycle/yr ($5K) and keep coupon-test pipeline warm (R-7).

**Algorithm pass:** *Question:* challenge "welders must be AWS-certified" hires — relaxed: hire for fit-up skill and test internally to D1.1; certification is produced, not purchased (widens labor pool, lowers wage pressure). *Delete:* material-handler role — confirmed deleted (ops tech + welders self-serve with gantry/forklift; forklift shared with existing operations). *Simplify:* one wage band per role, posted. *Accelerate:* lead hired early enough to co-design fixtures — converts ramp learning into design, not rework.

**Constraint check:** drum = fixture + paired welders; the org chart has exactly one purpose — keep the fixture cycling daily. No headcount exists that doesn't feed the drum.

Loop 14 of 25 complete. Resolved: I-38..I-40. Open: I-12. Confidence: 7/10.

---

## Loop 15 of 25 — Capex finalized (Depth)

**Issues identified:**
- I-41: Capex list never consolidated after the deletions.
- I-42: Equipment lead times unverified against the timeline.
- I-43: New-vs-used policy unstated.

**Resolutions:**
- I-41 → Resolved — capex (plan §2 table): heavy weldment fixture $85K; leg fixtures $18K; weld tables/positioner $32K; 4 pulse-MIG $38K; fume extraction $58K; 2-leg 5-ton gantry runs $88K; tilt/rotate weldment cart $14K; QA (gauges, fixture certification, rentals) $27K; facility prep (power drops, air piping, lighting, screens, racks) $78K; install/rigging/contingency 15% $66K → **total $504K** (vs. $640K pre-deletion draft; deletions: bridge crane, FARO, blast cabinet, lasers, brake).
- I-42 → Resolved: nothing on the list exceeds 14-week lead (fixture build is the longest at 10–14 wks); gantry 8–10 wks; MIGs stock. Timeline (M7 rate) holds with 4 weeks of float.
- I-43 → Resolved: buy new for welders/fume (warranty, parts); used/refurb acceptable for gantry and tables (−30%, already priced).

**Algorithm pass:** *Question:* challenge the tilt/rotate cart — owner is welder ergonomics + the 0.25 fillet quality in position; kept (flat/horizontal welding is faster and is part of the 9 lb/hr basis). *Delete:* second set of leg fixtures — deleted (legs single-fixture, 60/mo is 4 days of work). *Simplify:* all stations identical (same gun, same liner, same consumables SKU). *Accelerate:* pre-order fixture steel at 60% design (4 weeks saved on critical path — accepted from Loop 8).

**Constraint check:** $504K splits: ~$310K touches the drum directly (fixtures, gantry, welders, fume, cart); $194K infrastructure/QA. No non-drum capacity purchases. Subordination holds.

Loop 15 of 25 complete. Resolved: I-41..I-43. Open: I-12. Confidence: 7/10.

---

## Loop 16 of 25 — Sensitivity, cash flow, payback (Depth)

**Issues identified:**
- I-44: ±30% volume sensitivity required but not built.
- I-45: Cash curve (capex + ramp losses) not laid out.
- I-46: Should capex be leased instead of purchased?

**Resolutions:**
- I-44 → Resolved (plan §9 table): at 14 heavy/mo net annual benefit ≈ **+$23K** (near breakeven); at 20/mo ≈ **+$165K**; at 26/mo ≈ **+$292K**; at 40/mo (2nd shift on same fixture) ≈ **+$580K**. Welder count flexes 2/3/4/6 across these points.
- I-45 → Resolved: cash low point ≈ −$610K at month 6 (capex $504K + ramp labor ahead of output + qualification builds), recovering at ~$14K/mo at plan volume → simple payback ≈ 3.1 yr from SOP at flat 20/mo; < 2 yr if volume reaches 30/mo in year 2.
- I-46 → Resolved: equipment lease quoted basis ~8.5% money factor flattens cash low point to ≈ −$280K but adds $11K/yr cost — offered as an option, not the base case. Decision is Jeff's (H-10) but base case = purchase.

**Algorithm pass:** *Question:* challenge the requirement that the project must beat the vendor on cost at *current* volume — the real decision variable is the 24-month volume trajectory + lead-time/revision agility (3 weldment revs in 4 months; vendor requote cycle eats weeks each time). Made explicit in the recommendation. *Delete:* nothing physical left to delete this loop; deleted the *standby-vendor月 payment* idea from Loop 8 — replaced with a frame agreement holding the vendor's tooling/fixtures in callable state at $0/mo (they keep our business on decks/small parts as consideration). *Simplify:* one financial table drives all scenarios. *Accelerate:* none.

**Constraint check:** drum unchanged; sensitivity confirms the drum (not demand) caps single-shift output at ~22 heavy-equiv/mo — consistent with where the second shift triggers.

Loop 16 of 25 complete. Resolved: I-44..I-46. Open: I-12. Confidence: 8/10.

---

## Loop 17 of 25 — Quality cost & final unit economics (Depth)

**Issues identified:**
- I-47: Cost of quality (rework, scrap, warranty exposure) not in unit economics.
- I-48: Heavy legs: in-house or buy — never closed with numbers.
- I-49: Powder vendor logistics (2 trips × 16-ft load) cost/time unmodeled.

**Resolutions:**
- I-47 → Resolved: year-1 CoQ ≈ $190/unit (scrap adder $26, rework labor inside the 10% drum allowance ≈ $96, CWI/IH/cal program amortized $68); steady-state ≈ $95/unit. Added to plan §9; contribution updates to $2,070 year-1, $2,170 steady.
- I-48 → Resolved with numbers: vendor $79.71/leg vs. in-house variable ≈ $74 (kit $38 + 1.0 hr labor $35 + consumables/powder $12... ≈ $85) → in-house is *worse* (−$5 to −$10/leg). **Buy heavy legs. Closed.** (Wood legs differ: $122.71 buy vs. ≈ $97 make → keep in-house as drum filler.)
- I-49 → Resolved: powder runs 2×/week, 5 weldments/load on a flatbed (16-ft parts, permitted standard load); freight ≈ $180/trip → $72/unit round trip, folded into the $425 powder estimate (now $425 incl. freight, H-5 to verify).

**Algorithm pass:** *Question:* challenge 2×/week powder cadence — daily would cut WIP but doubles freight; 2×/week keeps total powder turnaround ≤ 5 working days with a 5-unit buffer post-weld. Kept. *Delete:* heavy-leg in-house plan — deleted with math (above). The depth phase ends with scope smaller than Loop 8 drafted it: in-house = heavy weldment + wood legs only. *Simplify:* QA traveler merged with powder packing list (one document follows the serial). *Accelerate:* none.

**Constraint check:** drum load drops 60 hr/mo by deleting heavy legs (was never loaded — they were 'phase 2'); confirmed drum plan unchanged at 445/490 hr.

Loop 17 of 25 complete. Resolved: I-47..I-49. Open: I-12. Confidence: 8/10.

---

## Loop 18 of 25 — Stress: volume drops 40% (Stress test)

**Scenario:** demand falls to 12 heavy + 6 wood/mo for 12+ months.

- Issues: I-50 (fixed-cost coverage at low volume), I-51 (what is reversible?).
- Findings: contribution 144 × $2,070 ≈ $298K vs. fixed $341K → **−$43K/yr**: the project loses money below ~13.5 heavy/mo at year-1 cost levels. Welders flex to 2 (one pair), lead absorbs wood legs.
- Resolutions: I-50 → mitigation: (a) gate the project on a committed 24-month forecast ≥ 18 heavy-equiv/mo (G-1 in plan §12); (b) if the drop happens post-launch, fixed cash shrinks to ≈ $257K (sublease/return 1,500 SF, defer maintenance pool) → ≈ −$10K/yr: hibernation-capable, not fatal; fixtures/equipment retain ≈ 60% resale. I-51 → resolved: the design is reversible — vendor frame agreement (Loop 16) allows switching back within one PO cycle; capex at risk net of resale ≈ $200K.
- Risk register: R-8 (demand risk) updated with the gate and the hibernation math. Recommendation updated: hybrid stands, **with a volume gate**.

**Algorithm pass:** *Question:* is 20/mo a forecast or a commitment? — H-11 to Jeff: provide the 24-month tray forecast tied to robot fleet plans. *Delete:* at 12/mo the 3rd welder and 1,500 SF delete cleanly (proves modular cost structure). *Simplify:* scenario playbooks reduced to two triggers (sustained <16/mo → shrink; <12/mo → hibernate + revert to vendor). *Accelerate:* none.

**Constraint check:** at −40% the drum is no longer the fixture (49% loaded) — the constraint moves to *cash*: fixed-cost absorption. Subordination flips: shed fixed cost, not add output.

Loop 18 of 25 complete. Resolved: I-50, I-51. Open: I-12. Confidence: 7/10 (gate added).

---

## Loop 19 of 25 — Stress: volume doubles (Stress test)

**Scenario:** 40 heavy + 20 wood/mo within 18 months.

- Issues: I-52 (drum capacity ×2), I-53 (does the kit strategy still beat owning a tube laser?), I-54 (powder vendor capacity).
- Findings & resolutions: I-52 → second shift on the *same* fixture (fixture is idle 16 hr/day): +3 welders +0.5 lead → output 40–44/mo; the Loop 7 deleted "second fixture" comes back **only** as a tack-jig ($30K) so day shift can pre-stage — a planned, acceptable re-add per the Algorithm. I-53 → at 42,000 lb tube/mo, in-house tube laser saves ≈ $390/kit but costs $650K used + operator ($95K/yr loaded): saves ≈ $187K/yr → ~3.5-yr payback, *and* it adds a non-drum machine — decision: still buy kits; revisit only above 50/mo sustained. I-54 → powder volume doubles to ~10 loads/wk equivalent — within one vendor's capacity but H-5 expands: qualify a second powder vendor at launch (dual-source from day one, trivial cost).
- Upside economics: ≈ +$580K/yr net at 40/mo; capex add ≈ $45K (tack jig + 2 stations). Payback on the whole program < 2 yr in this scenario.

**Algorithm pass:** *Question:* challenge "second shift is hard to staff" — night premium $2.50/hr priced in; Atlanta market depth adequate (H-12: confirm with a staffing agency). *Delete:* nothing; this loop legitimately re-adds the tack jig (evidence the earlier deleting was calibrated correctly). *Simplify:* second shift runs identical method (paired weldout), no new process. *Accelerate:* NOW automation earns a look: a cobot stitch-welder on the small-parts/leg cell at >25 legs/wk — deferred until H-6 (weld-spec review) lands, per the Algorithm's ordering.

**Constraint check:** drum at 2× = fixture *hours*, resolved by second shift before any new fixture — textbook subordination (exploit, then elevate).

Loop 19 of 25 complete. Resolved: I-52..I-54. Open: I-12. Confidence: 7/10.

---

## Loop 20 of 25 — Stress: key welder hires fail (Stress test)

**Scenario:** cannot fill 3 qualified welder seats by month 5; or lead quits at month 6.

- Issues: I-55 (single-point dependence on the lead), I-56 (thin Atlanta welder funnel at $24–29/hr).
- Resolutions: I-55 → lead's knowledge externalized by design: WPS, weld sequence sheets, fixture certification, and travelers are documents, not tribal knowledge; CWI contractor can backstop quals; cross-train welder #1 as deputy by month 8. I-56 → three-layer mitigation: (a) hire-for-fitup-test-internally widens funnel (Loop 14); (b) contract welders from staffing agencies bridge gaps at ~1.45× cost (≈ +$28/unit per seat-month — absorbable); (c) wage band pre-approved to $31/hr for a proven D1.1 tube welder before losing a candidate. Worst case: SOP slips 6–8 weeks; vendor overlap (Loop 8) extends at full rate — cost ≈ $35K. R-7 updated.

**Algorithm pass:** *Question:* does the plan *require* certified-from-day-one welders? No — re-affirmed: certification produced internally in week 2–3 of onboarding. *Delete:* attempted to delete the 3rd welder seat via process improvement (H-6 stitch-weld savings) — NOT taken: savings unproven; deletion rejected to protect the drum. *Simplify:* one onboarding path: coupon test → leg cell (low risk) → heavy cell pairing. *Accelerate:* standing requisition + quarterly coupon-test pipeline even when fully staffed (cheap insurance).

**Constraint check:** in this scenario the drum is welder-hours, not fixture — protective capacity = overtime + contract welders; both priced.

Loop 20 of 25 complete. Resolved: I-55, I-56. Open: I-12. Confidence: 7/10.

---

## Loop 21 of 25 — Stress: primary equipment lead time slips 6 months (Stress test)

**Scenario:** the longest-lead item (weldment fixture, 10–14 wks) slips to 9+ months, or gantry slips.

- Issues: I-57 (critical-path dependence on one fixture builder), I-58 (interim production method without gantry).
- Resolutions: I-57 → dual-quote the fixture to two builders; design owned by Slip (CAD in-house) so the package is movable; fallback: modular fixture built in-house on two certified weld platens ($28K, 6 wks) at reduced rate (0.7/day) while the hard fixture is built — SOP protected within 4 weeks of plan. I-58 → gantry slip → rent a 5-ton mobile gantry (~$2.2K/mo, stock item) — non-event. Because the kit strategy deleted all long-lead machines (lasers, brakes), **no purchased machine sits on the critical path** — this scenario is the strongest argument for the hybrid architecture; noted in recommendation.

**Algorithm pass:** *Question:* who owns fixture design — vendor or Slip? Must be Slip (engineering owns the CAD and cert procedure); made explicit in plan §5. *Delete:* nothing; verified earlier deletions are what defused this scenario. *Simplify:* fixture design package = the qualification gauge package (same document set). *Accelerate:* fixture steel pre-order at 60% design re-confirmed.

**Constraint check:** drum protected by fallback platen method; buffer (vendor overlap) covers the gap. Subordination intact.

Loop 21 of 25 complete. Resolved: I-57, I-58. Open: I-12. Confidence: 8/10.

---

## Loop 22 of 25 — Stress: first articles fail quality (Stress test)

**Scenario:** FA weldments fail flatness/interface position after powder (distortion), or weld quality rejects.

- Issues: I-59 (distortion of a 15.5-ft quarter-symmetric frame), I-60 (who is qualified to disposition?), I-61 (FA failure burns the vendor-overlap window).
- Resolutions: I-59 → engineering controls already in plan (balanced paired weldout, documented sequence, straightening step, fixture restraint during cooling on unit 1–3); add: FA protocol measures *before and after* powder cure (oven at ~400°F can move residual stress) — rented FARO arm covers months 4–6 (re-adds part of the Loop 12 deletion, deliberately temporary). I-60 → contract CWI dispositions weld rejects; dimensional disposition by engineering (MRB-lite: lead + engineer). I-61 → qualification plan = 3 FA units; if unit 3 fails, decision tree: assignable-cause fix (2-wk slip) vs. fixture rework (6-wk slip, vendor overlap extends, cost ≈ $40K). Budgeted in contingency. R-9 logged.

**Algorithm pass:** *Question:* challenge ±.02 two-place default tolerance on a 186-in weldment — likely over-spec for non-interface dims; H-13: engineering to issue a weldment-specific tolerance note (interfaces tight, field dims loose). High leverage: this single drawing note moves FA pass probability more than any capex. *Delete:* nothing. *Simplify:* FA report format = production traveler + 12 added measurements (no separate FA bureaucracy). *Accelerate:* none.

**Constraint check:** FA period intentionally runs the drum at 50% (qualification builds) while the vendor still delivers — buffer working as designed.

Loop 22 of 25 complete. Resolved: I-59..I-61. Open: I-12. Confidence: 8/10.

---

## Loop 23 of 25 — Stress: landlord/permit blocks finishing (Stress test)

**Scenario:** the original worry — a finish booth is blocked. Also generalize: what *can* the landlord/AHJ block?

- Issues: I-62 (finishing permit risk), I-63 (hot-work occupancy approval at Oakbrook — this is the live version of I-12/H-4), I-64 (compressed-gas storage limits).
- Resolutions: I-62 → already structurally avoided: powder is outsourced; no spray booth, no oven, no air permit, no flammable-liquids room. Scenario is a non-event for the base plan — this was the Loop 1 deletion paying off. I-63 → welding inside an existing building requires: landlord consent (use clause), fire-marshal review (Gwinnett County), hot-work program per NFPA 51B, possibly an S-1/F-1 occupancy verification. If Oakbrook refuses → fallback: 8–10K SF light-industrial flex within 10 miles at $8–11/SF (adds ~$20K/yr and a forklift) — viability unchanged. **I-12 is hereby closed into I-63's mitigation; H-4 stays open as the action.** I-64 → manifolded C25 bank ≤ 3,000 SCF inside with compliant storage/separation per NFPA 55/IFC — routine; bulk microbulk tank outside if we outgrow it.
- R-3 updated with the fallback site path.

**Algorithm pass:** *Question:* challenge "fab must be inside the main building" — already answered: preferable, not required. *Delete:* nothing physical; deleted the *assumption* that the project's site risk is binary. *Simplify:* permit scope reduced to one review (hot work + occupancy), since coating/blast are off-site. *Accelerate:* start the landlord conversation in week 1 (it is the longest *decision* lead, not the longest *equipment* lead).

**Constraint check:** drum unaffected; site fallback adds 2–3 weeks of timeline buffer consumption, inside float.

Loop 23 of 25 complete. Resolved: I-62..I-64 (and closes I-12). Confidence: 8/10.

---

## Loop 24 of 25 — Stress: raw steel +25% (Stress test)

**Scenario:** A500/A36 prices spike 25% (tariff/cycle event) and hold for a year.

- Issues: I-65 (make-side exposure), I-66 (buy-side pass-through behavior), I-67 (contract structure for kits).
- Resolutions: I-65 → make-side material content/heavy unit ≈ $912 (in kits) → +$228/unit. I-66 → vendor weldment is ~25–30% material by value → vendor reprices +$330–420/unit (pass-through plus margin-on-material, observed industry behavior) → **make advantage widens by ~$100–190/unit in a spike**. I-67 → kit POs indexed to CRU/AMM plate & tube indices with monthly adjustment and no margin-on-material clause — locks the asymmetry in our favor. R-10 logged: steel volatility is net *favorable* to make, but absolute tray cost rises either way → flag to product pricing.
- Sensitivity table in plan §9 gains a steel-price column.

**Algorithm pass:** *Question:* challenge holding zero raw inventory — kits arrive in 5-unit batches ≈ 1 week of cover; in a spike, allow opportunistic 4-week kit pre-buys (cap: $80K working capital). *Delete:* nothing. *Simplify:* one index clause in one PO covers 84% of material exposure. *Accelerate:* none.

**Constraint check:** drum unaffected; working-capital cap set so buffer growth never starves cash needed for drum staffing.

Loop 24 of 25 complete. Resolved: I-65..I-67. Confidence: 8/10.

---

## Loop 25 of 25 — Synthesis

All sections re-read end to end; registers reconciled (no orphan issues: I-01..I-67 all resolved, accepted, or converted to H-items; H-1..H-13 open for Jeff/company; A-1..A-8 logged with bases). Final package produced:

- One-page executive summary → `00-executive-summary.md`
- Standing 12-section plan (stand-alone, current as of this loop) → `01-feasibility-plan.md`
- Registers → `03-registers.md`
- Data basis → `04-data-basis.md`

**Final recommendation: HYBRID.** Weld the heavy-tray weldment (and wood-tray legs) in-house from purchased laser-cut tube/formed-sheet kits; outsource powder coat; continue buying decks, heavy legs, and all wood-tray steel piece parts. Gate the start on a committed 24-month forecast ≥ 18 heavy-equivalent/month. Capex $504K; year-1 net ≈ +$165K/yr at 20/mo scaling to ≈ +$580K/yr at 40/mo; payback 3.1 yr flat / <2 yr on the growth path; strategic gains: lead time from ~6–8 weeks to ~5 days post-buffer, revision agility (3 revs in 4 months), and a defused single-source dependency.

Confidence: 8/10. The two numbers that most need real-world replacement before committing capital: kit quotes (H-7) and powder quotes for 16-ft parts (H-5).

Loop 25 of 25 complete.
