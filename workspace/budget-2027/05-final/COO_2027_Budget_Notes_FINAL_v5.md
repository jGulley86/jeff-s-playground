# 02-build notes v14 - 2027 COO budget collation (documentation corrections on v13; all v13 figures unchanged)

> **CONFIDENTIAL - contains named compensation data (HC-* tabs); restrict distribution.** The workbook's HC-* tabs hold employee names and salaries (v13 adds the user's 2026-10-12 roster entries), and the 'Logistics&WH Payroll' tab (SD copy) names seat holders; share the workbook and these notes only with people cleared to see compensation. In this file per-person amounts for identified employees are rounded to the nearest $5k (shown with '~') or aggregated; rounding does not change an amount that is already a multiple of $5k, so some unique-role salaries still appear at their exact value. The Collation Notes sheet keeps exact figures. A department total compared across versions, or a line that holds one person's cost (e.g. PO 6610-6640 in v13), can also reveal that cost.

## Changes from v13 (v14): documentation corrections only - no value changes

Handoff 2026-10-12 (orchestrator): fix the critic's v13 items (B1 blocking + O1-O4, 03-review/03-review_critic_v13.md) and the verifier's stale-text findings (04-verify/04-verify_report_v13.md). **No budget value changed: COO P&L!AG132 = (646,753.85), identical to v13.** The v13 -> v14 diff is confined to the Collation Notes sheet - 0 formula differences anywhere (H78:H81 and C21:F28 included) and 0 value differences on every other cell of all 20 sheets; comments, defined names and the six P&L sheets' 2026 columns (B:N) are identical (diff_v14.py, exit 1 on violation). Every v13 figure, bridge term and scenario value therefore holds for v14 unchanged. Technique: the v12/v13 technique - scripted openpyxl text edits on the v13 workbook (Collation Notes cells only), then ONE full LibreOffice recalculation + engine save as the deliverable.

The sections below this one are the v13 notes carried forward with the corrections applied in place (additions marked 'v14'); the table maps every change. The v13 originals (02-build_notes_v13.md and the v13 workbook) are unchanged on disk.

| # | Item (source) | Fix | Where |
|---|---|---|---|
| 1 | B1 (critic v13, blocking) | The one-cell flip is no longer presented as a complete fix: flipping HC-CO F20 = Dec-27 ALONE books ~70,000 in CO while HC-PO r16 stays in the 8-person B131 base and the by-number Prod Payroll model keeps capitalising the role - an expense + capitalised overlap (asset overstated ~70k; the model's average is 70,056/head). New stated branch: if the person LEFT at Nov-26 (the backfill reading), r16, the live B131 = 0 base (590,317.51 - it falls by the r16 cost, ~70,000, without that row), lower bound 2 and the by-number model all carry a departed person: the B131 = 0 scenario ((1,205,750.10)) and LB2 ((1,714,922)) are ~70,000 too negative; on the 9-of-9 reading the asset is 70,056 too high (2027 depreciation 2,821). Collation Notes H381's 'budget the role outside the capitalised labour (set F20=Dec-27)' was inaccurate and is corrected to a three-way ask with accurate recipes. Exact one-person figures stay on the Collation Notes I-41/A-47 rows (banner convention). | md: headline caveat (iii), roster-merge A-47 note, I-41 issue row, A-47 assumption row, 'Not done / limits'. Collation Notes: E13, C41, D381, H381, E381, B858 |
| 2 | O1 (critic) | HC-COO double-listing inventory extended: the Team Lead person is listed on BOTH HC-PO r16 and HC-CO r20, so HC-COO's roster-level payroll and headcount count that person twice in Sep-Nov-26 (2026-side columns only); 2027 is unaffected (the HC-CO row costs 0 from Dec-26). | md: HC-COO roll-up. Collation Notes: A255 |
| 3 | O2 (critic) | The MFS <-> MH-02 swap asymmetry stated: the seat goes OUT at the model's cost (~60,000 at model rates), the realized hire comes IN at 85,000 salary + CO HC burden (100,304.86 of 2027 cost); net ~ +38,300 of cost inside the (71,048.29) B+D term (exact figures on the Collation Notes seat table and A-46 row). | md: decision 2 section. Collation Notes: G90, B857 |
| 4 | O3 (critic) | A-46 reversal recipe spelled out: delete the -'Logistics&WH Payroll'!<col>39 term in each of the 12 month columns U:AF of CO row 67 and the row-39 term inside the bracketed subtraction of rows 68/69 (x B5/B6 there); co-edit the H78:H80 check formulas on Collation Notes (their S39 terms); direction: flipping back ADDS ~60,000 of 2027 cost (exact on Collation Notes). | md: A-46 assumption row. Collation Notes: B857 |
| 5 | O4 (critic) | One hires/moves count everywhere: 11 (4 CO, 5 PE, 1 PO, 1 FE), scope = the roster rows added on the four HC tabs (the HC-CO r18 title edit and the HC-PO r20 blanking are not counted; the Material Handler's move counts once, as the CO row; the FE row feeds no P&L line; the CO Team Lead row has no 2027 cost). Replaces 'ten' (footnote (a)), the unscoped conclusion list, and Collation Notes '13'. | md: footnote (a), conclusion. Collation Notes: A33, A71, A873 |
| 6 | Verifier (md) | Headline table, Gross Profit row: the 2027 v12 column now reads 3,960,032 and the v13 - v12 change 78,529 (was 4,038,561 / 0; v13 GP 4,038,561 = v12 GP 3,960,032 + 78,529, the I-28 resolution being the only COGS change). | md headline table |
| 7 | Verifier (stale text) | Collation Notes v12-era text replaced with v13 values: E17 (scenario endpoints (1,205,750.10) / (773,662.29) / (1,286,153.81) / (707,448.94)); A32 (2026-policy contribution (3,095,044)); A35 (provenance note restated); C43 (logistics base on the 5 seats: 166,414 salaries, burden 38,608 booked vs 28,502 at CO HC rates); C47 and F357 (I-17 booked 210,023; v10-v12 (398,492) kept as marked history); C60 and issue row 377 (I-37 at 7.65%: CO 20,906 + logistics 1,415 + PE 64,102 + PM 5,054 = 91,477; FO/FE (33,630) on FO base 3,036,558 + FE 919,884); C61 (FO salary base 3,036,558); D380 (B131 = 0 sensitivity endpoint (1,205,750)); D8 (current-contribution note); C323 and C336 (same-vintage register rows, found by extending the sweep); A1 and A114 (version pointers). | Collation Notes (listed cells) |
| 8 | Verifier (#REF! wording) | '0 #REF! anywhere' claims rescoped to: 0 #REF! in formulas, caches and names; 6 historical text mentions on Collation Notes (E343, D364, D365, E365 - records of the v2/v3 error cleanups). | md error-scan + completion-criteria wording |

**Stale-value sweep (verifier instruction).** `sweep_v14.py` scans Collation Notes rows 8-71, 357 and 375-381 (plus rows 323/336, builder-extended) for the known stale values, keeping explicitly vN-marked history. Pass 1, run on v13, flagged 31 occurrences: E17 (4: 399,860 / 32,228 / 480,264 / 98,441), A32 (2,289,154), A33 ('13 hires'), A35 (2 stale provenance phrases), C43 (319,393 / 74,099 / 54,703), C47 (398,492), C60 (15,525 / 2,715 / 43,967), C61 (3,100,031), C323 (77,882 / 34,169), C336 (19,396), F357 (398,492), D377 (62,207), E377 (21,081 / 12,834 / 43,967 / 77,882 / 26,350), F377 (62,207 / 34,169), G377 (62,207), D380 (399,860), plus A873 ('10 user-approved', whole-sheet scan) - all fixed in this build. Pass 2, run on the v14 deliverable: clean (0 disallowed; the build gates on it).

**Open user items (NOT acted on - awaiting the user's answers; v14 changes no number):**
1. PO!R24:R26 production freight (5025/5026/5027) is 'YOY Growth' in the user's edited file vs 'Even'/0 carried since v1. Carrying it would add 60,056.60 of 2027 COGS; AG132 would be about (706,810) (verifier v13).
2. HC-PE!A22 'transfer?' flag is blank in the user's file. No number changes either way today; I-35's ~255,000 upside rests on that flag (verifier v13).
3. The I-41 three-way (left at Nov-26 / warehouse and staying / production) is with the PO owner (Collation Notes H381).

**Completion criteria (v14):**

| Criterion | Result |
|---|---|
| All critic v13 items (B1, O1-O4) and verifier items addressed | mapped row by row above |
| 0 value diffs outside Collation Notes; 0 formula diffs anywhere | diff_v14.py: 0 violations (Collation Notes text cells only) |
| AG132 unchanged | (646,753.85), cached and in a full recalculation |
| Suite green | suite_v14.py: figures = the verifier-confirmed v13 constants; roll-up on 2,142 SUM cells <= 1e-6; 0 error caches; recalc reproduces the cache; H78:H81 = 0; 0 shared formulas |
| Stale-value sweep clean on second pass | sweep_v14.py gate on the deliverable: 0 disallowed |
| Two-pass content-identical | run_build_v14.sh runs the pipeline twice; both passes' md byte-identical and xlsx part-identical after sorting <dataValidations> children (normcmp_v12.py; the v12-documented deviation) |
| No names / no exact per-person amounts in this file | privacy_v6 hits 0; paylist_v10 exact hits 0 (single-person amounts shown with '~') |

**Build (v14).** Entry point `scripts/run_build_v14.sh V13_XLSX V13_MD WORK_DIR OUT_DIR`: sweep_v14.py pass 1 (on v13) -> build_v14.py (the Collation Notes text edits; openpyxl; docProps pinned to v13's) -> recalc.sh = THE ENGINE SAVE (the deliverable; one full LibreOffice recalculation + save, no post-processing) -> twin save + normcmp_v12.py (determinism) -> diff_v14.py (confinement, exit 1 on violation) -> fresh recalc + suite_v14.py -> sweep_v14.py gate (pass 2, on the deliverable) -> report_v14.py (this file, generated from the v13 notes by asserted replacements and cross-checked against the sweep results) -> recon_v13.py + names_v11.py + cntext_v12.py + privacy_v6.py + paylist_v10.py (name and per-person-amount gates; scratch name list outside the repo, deleted). The whole pipeline runs twice; both passes' outputs must match as above. Base (read-only): the v13 workbook, sha256 `c03e4f6ef2b392d20e2d7cc6b88035e787253232343c011d07d04308f7216d85`, and 02-build_notes_v13.md. run_build_v13.sh ... run_build.sh still reproduce v13 ... v1. LibreOffice 24.2.7.2; Python with -I.

**Decisions (v14, builder):**

- D1 (v14): Corrections are applied IN PLACE in the carried v13 notes and Collation Notes cells (additions marked 'v14'), with the mapping table above, rather than as an errata appendix - a reader of the current file must not meet the inaccurate flip advice or a stale number in any current-state sentence; v13's own files stay untouched as the record.
- D2 (v14): The hires/moves count's scope (11 = roster rows added on the four HC tabs) includes the roster-only FE row and the zero-2027-cost CO Team Lead row, and excludes the r18 title edit and the r20 blanking: the count describes the user's roster additions, not the number of 2027 P&L cost adds (the bridge carries those in dollars).
- D3 (v14): The sweep scope was extended to register rows 323 (A-31) and 336 (A-44), which carried the same-vintage figures as the named cells; both found stale, fixed and reported. The handoff's required scope is unchanged and gates the build.
- D4 (v14): I-02's evidence cell (Collation Notes E342) still quotes the v5-era pair '6,967,834 instead of 139,032'; it is a self-dating v4/v5 comparison outside both the handoff's fix list and the sweep scope, so it is left as history and flagged here for a future pass.
- D5 (v14): Exact one-person amounts (the Team Lead's r16 cost, the F20-flip cost, the MH-02 seat cost) stay on the Collation Notes sheet per the banner convention; this file keeps the ~$5k rounding - both the r16 exposure and the flip round to ~70,000; they are two different exact amounts (PO HC rates vs CO HC rates), see the Collation Notes I-41/A-47 rows.


## Changes from v12 (v13)

Handoff 2026-10-12 (orchestrator): one build combining **brief v7** (user: "add $2,000 per month in GL 7700 in CO; Add $6,500 per month in GL 8600 in CO") and **brief v8 as amended** (the user's edited workbook `00-brief/inputs/USER_EDIT_FINAL_v4_HC.xlsx` - a reliable edit source whose roster changes are re-applied to the clean v12 chain - plus the user's four decisions of 2026-10-12). All budget changes below are user-confirmed. Technique: the v12 base is edited by script (openpyxl stage passes), then saved once, whole, by a full LibreOffice recalculation + engine save - no XML is spliced into saved parts (an unedited openpyxl round-trip + engine save of v12 was first proven semantically identical to v12: 0 formula/value/format/comment/name diffs on 253,036 cells).

| # | Change (all user-confirmed 2026-10-12) | Effect on the contribution | Cells |
|---|---|---|---|
| A | CO GL 7700 'Inventory Obsolescence-old' 2027 = 24,000 (2,000/month) and GL 8600 Repairs and Maintenance 2027 = 78,000 (6,500/month); R stays 'Even', so the two S inputs spread themselves | (102,000.00) | CO!S98, CO!S106 |
| B | Roster merge: HC-CO r18 title 'Facilities Manager'; + Material Handler ~50,000 Sep-26 (r19, = seat MH-01 moved from HC-PO r20); + Material Handling Team Lead ~60,000 Sep-26 **end-dated Nov-26** (r20; the user's file's own end month - 2027 cost 0, see I-41/A-47); + Material Flow Supervisor 85,000 Nov-26 (r35); + Applications Engineer 85,000 Nov-26 (r36). HC-PO: r20 blanked; + Production Manager 125,000 Oct-26 (r41). HC-FE: + Associate Field Robotics Engineer 75,000 Sep-26 (r20; the I-28 person). HC-PE: + Purchasing Analyst 85,000 Jan-27, Launch Planner 75,000 Nov-26, Quality Engineer 100,000 Dec-26, Manufacturing Engineer 110,000 Dec-26 (r35:r38), Strategic Sourcing Lead 120,000 Oct-26 (r41). | inside B+D, C, E below | HC-CO/PO/FE/PE input cells; names copied from the user's file at build time |
| C | Decision 1: PE 6610-6640 wired live to 'HC-PE' rows 67-69 (replacing typed constants): 1,211,637.29 -> 1,766,501.82 | (554,864.53) | PE!U67:AF69 (+AI notes) |
| B+D | Decision 2: CO 6610-6640 = 'HC-CO' rows 67-69 + the Logistics&WH model **less the roster-realized seats, by formula**: LOG-01 (since v10), MH-01, TL-01, MH-02 (the backfill seat realized by the Material Flow Supervisor, user-confirmed): 1,147,259.93 -> 1,218,308.22 | (71,048.29) | CO!U67:AF69 (+AI notes); Collation Notes H78:H81 |
| E | Decision 3: Production Manager expensed to PO 6610-6640 at PO HC rates with the 3% Oct-27 raise, live links to his roster row; NOT in the capitalised labour base or the Prod Payroll model: 0 -> ~155,000 (c) | (~155,000) (c) | PO!U67:AF69 (+AI notes) |
| F | Decision 4: Fld Ops Payroll B11 14 -> 13 (the FE Associate out of FO's tech count; he stays in Fld Eng Budget and on HC-FE; still LISTED on HC-FO r15, which feeds nothing - reader note). I-28 -> RESOLVED | +78,529.08 (payroll +78,198.12, 5330 +330.96) | Fld Ops Payroll!B11 |
| G | PO 5110-5140 re-anchored: the embedded-constants-minus-'HC-PO'!r20 formulas become a live 8-production-staff basis `(1-B131) x SUM('HC-PO'!M14:M33) x (1, D6, D7)` + the idle-month rows 226-228 (B135 terms kept). The basis survives roster edits; the PM (r41, New Hires block) is outside it by construction. B131 = 0 base recomputes 590,317.51 (= 590,317.51); booked value unchanged 0. Closes the full-sweep embedded-constants observation. | 0.00 | PO!U33:AF35 (+AI notes) |
| H | Notes + Collation Notes updated (headline, caveats, bounds, sign-flip recomputed by script; I-28 RESOLVED; I-41 restated; I-38 narrowed; I-42 added; A-46:A-48 added; YoY footnote extended) | - | this file; Collation Notes |

**Bridge from v12 (every term = the department's 2027 GL-line change; ties to the cent - asserted by `figures_v13.py`, exact terms on the Collation Notes v13 block):**

| Step | Amount |
|---|---|
| v12 contribution (COO P&L!AG132) | 159,136.40 |
| A. CO 7700 + 8600 | (102,000.00) |
| B+D. CO 6610-6640 (roster adds less de-duplicated seats) | (71,048.29) |
| C. PE 6610-6640 (live roster incl. 5 adds) | (554,864.53) |
| E. PO 6610-6640 (Production Manager) | (~155,000) (c) |
| F. Fld Ops Payroll B11 13 (I-28 resolved) | +78,529.08 |
| G. PO 5110-5140 re-anchor (booked 0 either way) | 0.00 |
| **v13 contribution** | **(646,753.85)** |

(c) One named person's cost (banner convention): rounded here, exact on the Collation Notes v13 block, which carries the full to-the-cent bridge. The sum of the exact terms equals the AG132 change to < $0.01 (build assertion).

## Headline: 2027 COO contribution

| Line | COO P&L row | 2026 (N) | 2027 v13 (AG) | Change | % | 2027 v12 (AG) | v13 - v12 |
|---|---|---|---|---|---|---|---|
| Revenue (company recognized revenue, 9/30/26 sales plan) | 16 | 7,423,940 | 15,563,646 | 8,139,706 | 110% | 15,563,646 | 0 |
| COGS (COO departments) | 63 | 4,478,016 | 11,525,085 | 7,047,069 | 157% | 11,603,614 | (78,529) |
|   of which depreciation (in COGS) | 19-22 | 1,788,097 | 3,423,225 | 1,635,128 | 91% | 3,423,225 | 0 |
| Gross Profit | 64 | 2,945,924 | 4,038,561 | 1,092,637 | 37% | 3,960,032 | 78,529 |
| Opex (COO departments) | 116 | 3,929,957 | 4,685,315 | 755,357 | 19% | 3,800,895 | 884,419 |
| COO contribution before other income ('Net Ordinary Income') | 117 | (984,033) | (646,754) | 337,280 | n/m | 159,136 | (805,890) |
| Net Other Income | 131 | 84,811 | 0 | (84,811) | -100% | 0 | 0 |
| **COO contribution ('Net Income')** | 132 | (899,222) | **(646,753.85)** | 252,468 | n/m (a) | 159,136.40 | (805,890.25) |

(a) Year on year is not like-for-like, on two counts. (1) 2026 expensed production labour, 2027 capitalises it; the policy effect carried from v10 is +2,448,290 (the labour block is untouched in v11-v13), so on the 2026 policy the 2027 contribution would be about (3,095,044). (2) The 2027 payroll now carries the user's 2026-10-12 additions - 11 hires/moves (4 CO, 5 PE, 1 PO, 1 FE; count and scope as defined in the conclusion) plus the two CO GL lines (7700/8600, little or no 2026 spend) - whose Sep-Dec 26 costs sit on the HC tabs only: the 2026 P&L columns are book data and were not restated. If any of these people (or the logistics model's 2026 hires) are on 2026 payroll, the 2026 forecast needs its own update outside this workbook's scope.

- **2027 COO contribution (COO P&L!AG132): (646,753.85)** (v12 159,136.40, change (805,890.25)). **The headline is now negative at the booked (capitalise-production-labour) policy.** The whole change is the user's 2026-10-12 additions, bridged above. Revenue 15,563,646; COGS + Opex 16,210,399.
- PO's booked COGS is unchanged (5110-5140 = 0, capitalised); the PM is Opex. CO payroll now carries two rate bases (roster at CO HC rates, 5 remaining model seats at the model's 6.8%/16.4%).
- Issues: 3 HIGH, 14 MED, 21 LOW open; 4 RESOLVED (I-05, I-17, I-26, I-28). New: I-42 (7700 label). Updated: I-06, I-17 (wiring), I-35 (PE wiring note), I-37 (recomputed), I-38 (narrowed), I-40 (base note), I-41 (restated).

**Headline caveats (new in v13):** (i) the 7700 row is labelled 'Inventory Obsolescence-old' - the only 7700 row in the book, but the '-old' suffix suggests a retired account; the user should confirm the intended account (I-42). (ii) 8600 2027 = 78,000 vs 2026 30,775 (+153%), above the variance-scan threshold - user-directed (brief v7). (iii) The Material Handling Team Lead's CO roster row is end-dated Nov-26 (the user's file), so neither CO nor any PO expense line carries that role in 2027 while seat TL-01 is excluded. v14: the previously advertised one-cell flip (HC-CO F20 = Dec-27) is NOT a complete fix - it adds ~70,000 of CO expense while the role stays inside the capitalised labour (HC-PO r16 in the B131 base; the Prod Payroll model counts by number), carrying it twice; and if the person in fact left at Nov-26, the B131 = 0 base, LB2 and the by-number model all carry a departed person (I-41/A-47).

### Caveats on the headline (read before using the figure)

(1) What the figure is. The bottom line, (646,753.85), is a **COO contribution**: the company's recognized revenue (15,563,646, all of it) less the costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: 16,210,399). Costs outside COO are not in this workbook, so it is **not company Net Income**. The workbook row keeps its GL label 'Net Income' (COO P&L!A132).

(2) What the revenue is: unchanged from v10-v12 (the 9/30/26 sales plan's recognized revenue; includes unsigned and forecast bookings - see the v10 notes section (2), still exact).

(3) Open exposures, each on its own against the headline. 'Carried from v12' = the item's inputs are outside every cell v13 changes (the v12 -> v13 diff shows 0 changes there), so the computed effect stands; the scenario switches, I-41, I-37 and the burden-rate item are recomputed on v13.

| Item | Direction | Effect | Contribution after this item alone | Basis |
|---|---|---|---|---|
| Decision #10 scope: current 8 expensed (B131 = 0 sensitivity, not booked) | downside | (558,996) | (1,205,750) | recomputed (LibreOffice scenario); PO 5110-5140 base 590,317.51 |
| I-40 idle-month labour expensed (B135 = 0, not booked) | downside | (126,908) | (773,662) | recomputed (scenario) |
| B132 = 1 (Sep-Dec 26 labour capitalised; needs a 2026 restatement) | downside | (60,695) | (707,449) | recomputed (scenario); not in the range |
| Labour already in the 65,000 / 8,000 unit cost (O1) | upside | +104,417 | (542,337) | carried from v12 |
| I-41 restated: the Team Lead role carried nowhere in 2027 expense | downside | (~70,000) | (~720,000) | recomputed; see Issues |
| MH-01 on the 9-of-9 count reading | upside | +2,821 | (643,933) | carried from v12 |
| Logistics&WH seats at CO HC burden rates (5 seats left) | upside | +10,106 | (636,648) | recomputed (v12 +19,396 on 8 seats) |
| I-05 burden (O1), capitalised | downside | (5,715) | (652,469) | carried from v12 |
| Rate base of the current staff (O7) | downside | (899) | (647,652) | carried from v12 |
| I-10 FO/FE lines at 0 | downside | (384,425) | (1,031,179) | carried from v12 |
| I-31 shortfall / double count | two-way | (39,057) / +37,457 | (685,811) / (609,297) | carried from v12 |
| I-32 SlipBot 5010 = 0 / trend / trend from Sep-26 | upside | +1,353,574 / +276,164 / +403,624 | 706,820 / (370,590) / (243,130) | carried from v12 |
| I-33 peripherals life 60 months | two-way | (25,534) | (672,288) | carried from v12 |
| I-34 FE burden at FE HC rates / with FE tax at 7.65% | upside | +109,539 / +76,600 | (537,215) / (570,154) | carried from v12 |
| I-37 payroll tax below 7.65%: CO + PE + the PM | downside | (91,477) | (738,231) | recomputed (v12 (62,207); PE roster +493,675 and the PM are new base) |
| I-37 FO and FE at the SD 6.8% | downside | (33,630) | (680,384) | recomputed (one tech out of the FO base) |
| I-35 PE 'transfer?' leaves COO | upside | ~255,000 | (~390,000) | carried from v12 (one person, rounded; the row is unchanged inside the live PE link) |
| I-36 Aug-27 FE hire not approved | upside | +33,967 | (612,787) | carried from v12 |
| I-39 FE manager seat stays open | upside | +173,774 | (472,980) | carried from v12 |
| A-14 depreciation convention (mid-month / month after) | upside | +147,903 / +295,807 | (498,851) / (350,947) | carried from v12 |
| A-22 unsigned/forecast revenue | downside | n/d | n/d | carried from v12 |
| New CO employee start month (A-43) | upside | per month later: ~10,000 | - | carried from v12 |
| I-28 | RESOLVED | 0 (booked: +78,529.08 in the headline) | (646,753.85) | user decision 4 |

Sign-flip statement (computed, v13): the headline itself is NEGATIVE: (646,754) (v12 159,136; the user-approved 2026-10-12 additions move it by (805,890)). Downsides no longer flip the sign - they deepen it (largest: the B131 = 0 scope sensitivity (558,996) -> (1,205,750); I-10 (384,425) -> (1,031,179)). Single quantified UPSIDES that make the contribution positive on their own: I-32 full +1,353,574 -> 706,820. No other single quantified item does (next largest: I-32 trend continued from Sep-26 +403,624 -> (243,130); A-14 month-after +295,807 -> (350,947)). With costs held fixed, revenue 646,754 (4.2%) ABOVE plan is needed to bring the contribution to zero.

Upside: I-32 can add up to 1,353,574 (contribution 706,820); the trend alternative adds 276,164 ((370,590)), or 403,624 ((243,130)) if the decline also ran through Oct-Dec 26. Labour already in the unit cost (O1): up to +104,417 ((542,337)). Logistics at CO HC burden rates +10,106 (v12 19,396; smaller: only 5 model seats remain in CO). MH-01 on the 9-of-9 reading +2,821. I-35 (PE transfer) +~255,000 (one person; exact in the caveat row on this sheet); I-39 +173,774; I-34 +109,539.

Range (v13): asymmetric by construction, as in v7-v12. Lower bound 1, booked policy, all quantified downsides (I-41 restated (~70,000); I-10 (384,425); I-31 shortfall (39,057); I-05 burden capitalised (5,715); rate base of the current staff (O7) (899); idle-month labour expensed (I-40) (126,908)): (1,275,819). Lower bound 2, the same under the scope sensitivity, components at B131 = 0 (sensitivity (558,996); I-10 (384,425); I-31 shortfall (39,057); I-05 burden at the B131 = 0 rate (5,286); idle-month labour at B131 = 0 (80,404); I-41 is 0 there: r16 is expensed inside PO 5110-5140): (1,714,922). Upper end, I-32 in full only: 706,820. Not in the range: I-37 (unverified upper bound, recomputed (91,477) CO/PE/PO and (33,630) FO/FE); B132 = 1 (only with a 2026 restatement); the O1, burden-rate, 9-of-9 and I-35/I-39/I-34 upsides. v12 range: (469,929) to 1,512,711 (lower bound 2 (909,032)).

| Bound | 2027 COO contribution |
|---|---|
| Lower bound 1 (booked policy, all quantified downsides) | (1,275,819) |
| Lower bound 2 (scope sensitivity, components at B131 = 0) | (1,714,922) |
| Point estimate | (646,753.85) |
| Upper end (I-32 in full only) | 706,820 |

Conclusion: the user additions of 2026-10-12 (brief v7: CO 7700 +24,000 and 8600 +78,000; brief v8: the HC roster merge - 11 hires/moves: 4 CO, 5 PE, 1 PO (the Production Manager), 1 FE (the Associate; roster row only - he was already costed in FE), counted as roster rows added on the four HC tabs, the HC-CO r18 title edit and HC-PO r20 blanking not among them, the CO Team Lead row carrying no 2027 cost; I-28 resolved) move the 2027 COO contribution from 159,136 (v12) to (646,754): NEGATIVE at the booked policy. Bridge: CO GL adds (102,000); CO payroll net (71,048); PE payroll (554,865); PO Production Manager (~155,000) (one person; exact in the v13 block below); I-28 resolution +78,529. Treat (646,754) as a point estimate inside (1,275,819) to 706,820 (lower bound 2: (1,714,922)) until Decisions #2 (I-32) and #10 (I-40) are answered, I-10 is confirmed, and the PO owner answers the restated I-41 three-way (left at Nov-26 / warehouse / production - Collation Notes H381).

## The roster merge (B): what landed where

Names were copied from the user's file into the HC tabs at build time (never into scripts, JSONs, these notes or any CSV). Titles, salaries and start months were asserted against the brief before writing. Our sheet structure is kept: the user's file had deleted HC-PO row 20, which shifted their rows; we blank r20 instead and use our row numbering (their r40 Production Manager = our r41).

| Tab | Row | Title | Annual salary | Start | End | Feeds |
|---|---|---|---|---|---|---|
| HC-CO | r18 | Facilities Manager (title set; the 110k employee of v10) | 110,000 | Jan-27 | Dec-27 | CO 6610-6640 via rows 67-69 |
| HC-CO | r19 | Material Handler (= seat MH-01, moved from HC-PO r20) | ~50,000 | Sep-26 | Dec-27 | CO 6610-6640 |
| HC-CO | r20 | Material Handling Team Lead (same person as HC-PO r16) | ~60,000 | Sep-26 | **Nov-26** | nothing in 2027 (A-47, I-41) |
| HC-CO | r35 | Material Flow Supervisor (open seat, no name; = the MH-02 backfill, A-46) | 85,000 | Nov-26 | Dec-27 | CO 6610-6640 |
| HC-CO | r36 | Applications Engineer (open seat, no name) | 85,000 | Nov-26 | Dec-27 | CO 6610-6640 |
| HC-PO | r20 | (blanked - the Material Handler moved to HC-CO r19) | - | - | - | out of the 5110-5140 base |
| HC-PO | r41 | Production Manager (New Hires block) | 125,000 | Oct-26 | Dec-27 | PO 6610-6640 (decision 3) |
| HC-FE | r20 | Associate Field Robotics Engineer (the I-28 person; = Fld Eng Budget r15) | 75,000 | Sep-26 | Dec-27 | nothing (FE P&L reads Fld Eng Budget; roster completeness) |
| HC-PE | r35 | Purchasing Analyst (open seat, no name) | 85,000 | Jan-27 | Dec-27 | PE 6610-6640 via rows 67-69 |
| HC-PE | r36 | Launch Planner (open seat, no name) | 75,000 | Nov-26 | Dec-27 | PE 6610-6640 |
| HC-PE | r37 | Quality Engineer (open seat, no name) | 100,000 | Dec-26 | Dec-27 | PE 6610-6640 |
| HC-PE | r38 | Manufacturing Engineer (open seat, no name) | 110,000 | Dec-26 | Dec-27 | PE 6610-6640 |
| HC-PE | r41 | Strategic Sourcing Lead (New Hires block) | 120,000 | Oct-26 | Dec-27 | PE 6610-6640 |

**The end-dated Team Lead row (A-47).** The user's file ends HC-CO r20 at Nov-26 (F20), so the row's 2027 cost is 0; the handoff's blocker rule says ambiguous roster details take the user's file's value, disclosed. It is internally consistent with their 'backfilling' comment (the Material Flow Supervisor starts Nov-26, seat MH-02 is the model's backfill seat) - but the same person remains on HC-PO r16, Sep-26 to Dec-27, inside the capitalised B131 base. Net effect: with TL-01 excluded and the CO row at 0, **no 2027 expense line carries the team-lead role** (booked PO expense is 0). v14 (critic v13 B1): HC-CO F20 = Dec-27 ALONE is not a complete fix - it costs the person in CO (+~70,000 at CO HC rates) while r16 stays in the 8-person B131 base and the by-number Prod Payroll model keeps capitalising the role: carried twice (expense + robot cost), asset overstated ~70k. And if the person actually LEFT at Nov-26 (the backfill reading), r16, the live B131 = 0 base (590,317.51 - it falls by the r16 cost, ~70,000, without that row), lower bound 2 and the by-number model all carry a departed person: the B131 = 0 scenario ((1,205,750.10)) and LB2 ((1,714,922)) are ~70,000 too negative, and on the 9-of-9 reading the capitalised asset is ~70,056 too high (2027 depreciation 2,821). Exact figures on the Collation Notes I-41/A-47 rows. Restated as I-41.

**Roster totals vs the user's file (completion criterion; exact equality):**

| Tab | 2027 salary total (Z67), v12 | v13 | User's file | Difference |
|---|---|---|---|---|
| HC-CO | 639,276.89 | 860,846.29 | 860,846.28 | 0.00 |
| HC-PO | 525,310.50 | 600,953.60 | 600,953.60 | 0.00 |
| HC-FE | 816,751.03 | 892,313.53 | 892,313.53 | 0.00 |
| HC-PE | 1,078,019.96 | 1,571,694.96 | 1,571,694.96 | 0.00 |

(The user's HC-PO totals sit one row higher in their file - their Excel row deletion; compared accordingly. HC-CO matches *because* r20 carries their Nov-26 end month. The user-file column shows Excel's cached floats; where the last displayed cent differs, the underlying difference is < $0.000001 and the Difference column is computed on the raw values.)

**HC-COO roll-up.** Pure formulas; recalculates. The Material Handler now appears once (HC-PO r20 blanked, HC-CO r19 filled - no double listing). Reader note: the FE Associate is listed on BOTH HC-FO r15 (snapshot; FO's P&L no longer counts him, B11 = 13) and HC-FE r20 (feeds nothing; FE's P&L costs him via Fld Eng Budget r15), so HC-COO's roster-level FO+FE payroll counts him twice while the P&L costs him once, in FE. v14 (critic v13 O1): the Material Handling Team Lead is likewise double-listed - HC-PO r16 (Sep-26..Dec-27) and HC-CO r20 (Sep-26..Nov-26) - so HC-COO's roster-level payroll and headcount count that person twice in Sep-Nov-26 (2026-side columns only); from Dec-26 and for all of 2027 the HC-CO row costs 0, so 2027 is unaffected. HC-COO 2027 total payroll 5,855,984 (v12 4,863,502). Dec-27 headcounts (HC-COO col Z): PO 9, FO 16, FE 8, PE 14, CO 9 (the end-dated Team Lead is not an active 2027 head).

**2026-side HC cells (disclosed precisely).** Adding Sep-Dec-26 starters moves the HC tabs' 2026-side columns I:L (Sep-Dec 26) on the edited rows and their totals, and HC-COO's same columns. Total Payroll (row 70) deltas by month:

| Tab | Sep-26 | Oct-26 | Nov-26 | Dec-26 |
|---|---|---|---|---|
| HC-CO | +10,490.11 | +10,490.11 | +27,083.14 | +21,465.52 |
| HC-PO | (5,169.76) | +7,775.36 | +7,775.36 | +7,775.36 |
| HC-FE | +6,955.76 | +6,955.76 | +6,955.76 | +6,955.76 |
| HC-PE | +0.00 | +11,239.47 | +18,264.14 | +37,933.21 |

The six P&L sheets' 2026 columns (B:N) are unchanged - 0 cells (diff-asserted): the 2026 P&L is book data and reads no HC tab.

## Decision 1 (C): PE 6610-6640 wired to the roster

| GL (PE, 2027) | v12 (typed) | v13 (live 'HC-PE' rows 67-69) | Change |
|---|---|---|---|
| 6610 Salaries and Wages | 1,078,019.96 | 1,571,694.96 | 493,675.00 |
| 6630 Payroll Taxes | 38,501.12 | 56,132.55 | 17,631.44 |
| 6640 Benefits | 95,116.21 | 138,674.30 | 43,558.09 |
| Total | 1,211,637.29 | 1,766,501.82 | 554,864.53 |

U67:AF69 = 'HC-PE'!M67:X69 (the same pattern CO has used since v10). The typed v12 constants equalled the then-roster to the cent, so the switch itself moves nothing; the five user adds move the roster. 2026 columns untouched. PE 2027 salary 1,571,694.96 = the handoff's expected 1,571,695 + PE HC burden at D6/D7 (3.571% / 8.823%; both below 7.65% FICA - I-37 recomputed below). The 'transfer?' row (I-35) rides inside the live link unchanged.

## Decision 2 (D): CO logistics de-dup - seat by seat (2027 $, model rates incl. 2027 new-hire cost)

CO!U67:AF69 = 'HC-CO' rows 67-69 + 'Logistics&WH Payroll' row 43 **less rows 34, 36, 38, 39** + row 46 (and the same net-of pattern x B5 / B6 on 6630/6640). The de-dup lives in CO's formulas (the Logistics&WH tab stays an unedited SD copy). Collation Notes H78:H81 check this composition live; they cache and recalculate to 0.

| Seat | In CO, v12 | In CO, v13 | 2027 cost | Why out / in |
|---|---|---|---|---|
| LOG-01 Logistics Manager | no | no | ~150,000 | = HC-CO r17 (excluded since v10) |
| MH-01 Material Handler | yes | **no** | ~60,000 | moved to HC-CO r19 (roster row at CO HC rates) |
| TL-01 Material Handling Team Lead | yes | **no** | ~65,000 | realized on HC-CO r20 (end-dated Nov-26; I-41) |
| MH-02 Material Handler (backfill seat) | yes | **no** | ~60,000 | realized by the Material Flow Supervisor (HC-CO r35; A-46, user-confirmed) |
| INV-01 Inventory Control Specialist | yes | yes | 55,652 | model seat, no roster (Feb-27) |
| MH-03 Material Handler | yes | yes | 52,712 | model seat (Mar-27) |
| MH-04 Material Handler | yes | yes | 36,876 | model seat (Jun-27) |
| TL-02 Material Handling Team Lead | yes | yes | 33,032 | model seat (Jul-27) |
| MH-06 Material Handler | yes | yes | 31,751 | model seat (Jul-27) |
| **Out in v13 (3 seats)** | | | (~190,000) | TL-01 + MH-01 + MH-02 (exact on Collation Notes) |
| **Still added from the model (5 seats)** | | | 210,022.54 | salaries 166,414.40 + tax 11,316.18 + benefits 27,291.96 + new-hire 5,000.00 |

Verified as the handoff asked: **MH-02's 1,000 hire cost sits in the model's Oct-26 column and TL-01's in Dec-26** - both outside the 2027 window, so the 2027 new-hire cost is exactly 5,000 (INV-01 Feb, MH-03 Mar, MH-04 Jun, TL-02 + MH-06 Jul), all for seats still added. The CO 6610-6640 composition (roster + in-seats = P&L) ties to < $0.01 per GL (build assertion + live H78:H81).

v14 (critic v13 O2) - the MH-02 <-> Material Flow Supervisor swap is asymmetric: the seat goes OUT at the model's cost (~60,000 at model rates - exact on the Collation Notes seat table), while the realized hire comes IN on the roster at 85,000 salary + CO HC burden (100,304.86 of 2027 cost); net ~ +38,300 of cost inside the (71,048.29) B+D term. The asymmetry is the price of realizing the backfill seat at a higher salary and CO HC rates (the swap itself is user-confirmed, A-46).

| GL (CO, 2027) | v12 | HC-CO roster v13 | of which v13 roster adds | Logistics in-seats + hire cost | v13 | v13 - v12 |
|---|---|---|---|---|---|---|
| 6610 (incl. new-hire cost) | 963,670.08 | 860,846.29 | 221,569.40 | 171,414.40 | 1,032,260.69 | 68,590.60 |
| 6630 | 55,098.30 | 44,948.71 | 11,569.15 | 11,316.18 | 56,264.89 | 1,166.59 |
| 6640 | 128,491.55 | 102,490.68 | 26,379.62 | 27,291.96 | 129,782.64 | 1,291.10 |
| Total | 1,147,259.93 | 1,008,285.68 | 259,518.17 | 210,022.54 | 1,218,308.22 | 71,048.29 |

Burden-rate caveat (A-44, updated): the 5 remaining model seats are booked at the model's 6.8% / 16.4%; at CO HC rates the contribution would be +10,106 higher (v12 +19,396 on 8 seats).

## Decision 3 (E): Production Manager expensed in PO

PO!U67:AF69 = 'HC-PO'!M41:X41 x (1, D6, D7) - live links to his roster row (125,000, Oct-26 start, New Hires block r41, 3% raise Oct-27 via the row's G/H cells). 2027: salary ~125,000, tax ~5,000, benefits ~25,000, total ~155,000 (exact on the Collation Notes v13 block). He is **not** in the capitalised labour base (PO!U33:AF35 sum rows 14:33 only; he is r41) and **not** in the Prod Payroll model (untouched). His Oct-Dec 26 cost exists on the HC tab only - no 2026 P&L change.

## Decision 4 (F): Fld Ops Payroll B11 = 13 (I-28 RESOLVED)

One typed input: B11 14 -> 13. Recalculated effect +78,529.08 on the contribution = FO 5510/5530/5540 payroll 78,198.12 lower + 5330 330.96 lower (Fld Maint Budget!B29 = B30 + B11: 21 -> 20); supervisor headcount unchanged in every month (ratio basis). Matches the v12 caveat (+78,529) and the handoff evidence. The person stays budgeted once: Fld Eng Budget r15 (FE 6610-6640) - and is now also on the HC-FE roster (r20), closing the FE HC gap that I-28/I-36 flagged. He remains LISTED on HC-FO r15: a roster snapshot that feeds no P&L line (reader note above).

## G: PO 5110-5140 re-anchor (live 8-production-staff basis)

Old (v10-v12): `(1-B131) x (embedded v7 monthly constant - 'HC-PO'!M20 x rate) + idle row` - the form whose r20 reference the user's in-Excel row deletion severed (v12 diagnosis). New (v13): `(1-B131) x SUM('HC-PO'!M14:M33) x (1, D6, D7) + idle row` - the Current Employees block itself is the basis, so the formula survives roster edits (blank rows compute empty and SUM skips them; a future current hire joins the base automatically; the PM sits in New Hires r41, outside the block). Booked value unchanged (0 while B131 = 1); B131 = 0 recomputes 590,317.51/yr = the handoff's 590,317.51 (scenario-verified on the shipped file). The idle-month B135 terms (rows 226-228) are kept. This closes the full-sweep observation about embedded constants in PO 33-35.

## Issues (v13)

Open: 3 HIGH, 14 MED, 21 LOW; 4 RESOLVED. Changed rows only (all others carried from v12's register verbatim):

| ID | Sev | Change in v13 |
|---|---|---|
| I-06 | LOW | Evidence refreshed: Fld Ops Payroll!B11 = 13 and Fld Maint Budget!B29 = 20 (was 14 / 21); the stale MeLi comment finding itself is unchanged. |
| I-17 | RESOLVED | Wiring updated: the CO add-on now excludes LOG-01 + MH-01 + TL-01 + MH-02 by formula (user decisions 2026-10-12); 5 model seats remain; H78:H81 check the composition live. |
| I-28 | **RESOLVED** | User decision 4 (2026-10-12): the duplicate was real (FO -> FE move). B11 = 13 booked (+78,529.08 in the headline); he is on HC-FE r20 now; still listed on HC-FO r15 (snapshot, feeds nothing). Residual: if the move was mid-2026, the 2026 FO forecast (book data) would need checking - 2027 is right either way. |
| I-35 | MED | PE 6610-6640 is now a live roster link, so a recorded transfer would flow automatically once HC-PE r22 is end-dated / moved; exposure unchanged (~255,000). |
| I-37 | MED | Recomputed on the v13 salary bases: CO + PE + the PM at 7.65% upper bound (91,477) (v12 (62,207); drivers: PE roster +493,675, the PM, the CO adds); FO/FE (33,630) (one tech left the FO base). Unverified upper bound; not in the range. |
| I-38 | MED | Narrowed: TL-01 and MH-02 are no longer booked from the model - the roster realizes them (HC-CO r20 end-dated / r35). Remaining: the Prod Payroll ramp dates (unchanged). |
| I-40 | HIGH | Unchanged in effect; the B131 = 0 base is now live (SUM of the current-employee block) and recomputes 590,317.51; scenario values on v13 in the caveat table. |
| I-41 | MED | **Restated in v13; completed in v14 (critic v13 B1).** The Material Handling Team Lead: HC-PO r16 (Sep-26..Dec-27, inside the capitalised base and - by headcount - the by-number Prod Payroll model) AND HC-CO r20 (Sep-26..Nov-26, 2027 cost 0 - the user's file value, A-47). Booked: PO expenses 0 (capitalised), CO excludes seat TL-01 as roster-realized -> no 2027 expense line carries the role. Three branches: (1) warehouse role, person stays (7-of-9 reading): (~70,000) should stay an expense; flipping HC-CO F20 = Dec-27 ALONE books +~70,000 in CO while the capitalised side keeps the role (r16 in the B131 base; the model counts by number) - carried twice, asset overstated ~70k. (2) Person left at Nov-26 (the backfill reading): r16, the live B131 = 0 base (590,317.51; ~70,000 lower without r16), LB2 and the by-number model carry a departed person - the B131 = 0 scenario ((1,205,750.10)) and LB2 ((1,714,922)) are ~70,000 too negative; on the 9-of-9 reading the asset is 70,056 too high (2027 depreciation 2,821). (3) Production role, stays: booked treatment right. Under B131 = 0 the role is expensed inside PO 5110-5140. PO owner to answer the three-way (Collation Notes H381). |
| I-42 | LOW (new) | The 7700 row booked with the user's 24,000 is labelled '7700 - Inventory Obsolescence-old' - the only 7700 row, but the '-old' suffix suggests a retired account. User to confirm; classification only. |

## Assumptions added in v13

| ID | Assumption | Value / effect | Where | Source |
|---|---|---|---|---|
| A-46 | The Material Flow Supervisor (85,000, Nov-26, HC-CO r35) IS the realized backfill that the logistics model carries as seat MH-02 ('backfill' seat). | MH-02 excluded from the CO add-on ((~60,000)); if wrong, flip it back by deleting the -'Logistics&WH Payroll'!<col>39 term in each of the 12 month columns U:AF of CO row 67 and the row-39 term inside the bracketed subtraction on rows 68/69 (x B5/B6 there), and co-edit the H78:H80 check formulas on the Collation Notes sheet (their S39 terms); flipping back ADDS that ~60,000 of 2027 cost - the contribution falls by it (v14, critic v13 O3) | CO!U67:AF69; 'Logistics&WH Payroll' row 39 | user 2026-10-12 ('we are backfilling [the departing employee], so the Material Flow Supervisor should be included'); orchestrator mapping |
| A-47 | HC-CO r20 (MH Team Lead) end month Nov-26 - the user's file's own value (the brief gave the salary and a Sep-26 start, no end month); 2027 cost 0; the person stays on HC-PO r16. | HC-CO F20 = Dec-27 books +~70,000 of CO cost but leaves the role in the capitalised labour; if the person left at Nov-26, r16 and the B131 = 0 base carry a departed person (both: I-41, v14) | 'HC-CO'!F20 | user's file (handoff blocker rule: take the file's value, disclose); restated as I-41 |
| A-48 | Production Manager: Oct-26 start on the roster; Oct-Dec 26 cost on the HC tab only (2026 P&L is book data, not restated); expensed all of 2027 in PO 6610-6640. | (~155,000) on the contribution | 'HC-PO'!B41:F41; PO!U67:AF69 | user decision 3 (2026-10-12); builder (2026 timing) |

A-01..A-45 are unchanged (v9/v10 registers). A-43's 'title not provided' is resolved: HC-CO r18 = Facilities Manager (user, 2026-10-12).

## v12 -> v13 diff (confinement proof)

`diff_v13.py` compares every cell of all 20 sheets (formulas and cached values) plus comments, with the handoff's allowed areas encoded as rules; **0 violations**. Changed cells outside the regenerated-in-place Collation Notes: 144 formula / 2227 value diffs:

| Sheet | Formula diffs | Value diffs | Area |
|---|---|---|---|
| COO P&L | 0 | 320 | roll-up rows 46/52-54/67-69/98/106 + subtotals/ratios, 2027 columns only |
| FO | 0 | 191 | 5330 + 5510-chain + subtotals/ratios (B11 recalc), 2027 columns only |
| PO | 72 | 163 | U33:AF35 + U67:AF69 + AI; rows 36-37; subtotals/ratios |
| CO | 36 | 183 | S98/S106; U67:AF69 + AI; rows 73/116/117/132/137-142; rows 98/106 2027 side |
| PE | 36 | 140 | U67:AF69 + AI; subtotals/ratios |
| Fld Ops Payroll | 0 | 145 | B11 + its dependent formula cells |
| Fld Maint Budget | 0 | 84 | B29 chain (formula cells only) |
| HC-PO | 0 | 109 | r20 blanked, r41 added + recalculated cells |
| HC-CO | 0 | 149 | roster input rows 18-20/35-36 + recalculated row/total cells |
| HC-FE | 0 | 88 | r20 added + recalculated cells |
| HC-PE | 0 | 165 | r35-38/41 added + recalculated cells |
| HC-COO | 0 | 490 | roll-up recalc (formula cells only) |

Collation Notes: 3 formula + 346 text/number cells updated in place (headline, decision rows, caveat table, CO block, reconciliation, issue rows, H78:H80 checks) + the v13 block appended from row 812 (no row insertions, so every existing address is stable). FE, HC-FO, Logistics&WH Payroll, DeploySum, Prod Payroll and Depreciation Schedule: **0 changes** (diff-asserted frozen). 2026 columns (B:N) of the six P&L sheets: **0 changes**. HC-tab diffs are reported as coordinates only (column B holds names). Comments: 0 changes.

## Error scan and suite (all green; re-run on v14)

- COO P&L = FO + PO + CO + FE + PE on 2142 SUM cells; max deviation 5.82e-10.
- 0 error caches in v14 and in its LibreOffice recalculation; 0 #REF! in formulas, caches and names - 6 historical text mentions of '#REF!' remain on the Collation Notes sheet (cells E343, D364, D365, E365; records of the v2/v3 error cleanups) - and the user's severed-reference incident cannot recur from this file; 0 shared formulas in the package (wording rescoped in v14 per verifier v13).
- A full LibreOffice recalculation of v14 reproduces its own cache (numeric <= 1e-6); the deliverable is value-identical to v13 outside the Collation Notes sheet (diff-asserted), so the v13 figures and scenarios below hold for the shipped file.
- Collation Notes: the 32 live headline formulas (C21:F28) are unchanged (identical in v12, v13 and v14); H78:H81 (the CO de-dup check) formulas are v13's and cache and recalculate to 0.
- Roster cross-check: all four HC Z-column totals equal the user's file's (table above, differences 0.00).

## Scenario switches (scratch copies of the shipped v13, LibreOffice full recalc; deltas = v12's, orthogonality confirmed)

| Scenario | AG132 | vs booked |
|---|---|---|
| Booked (B131 = 1, B132 = 0, B135 = 1) | (646,753.85) | - |
| B131 = 0 (current staff expensed); PO 5110-5140 base 590,317.51 | (1,205,750.10) | (558,996) |
| B135 = 0 (idle-month labour expensed) | (773,662.29) | (126,908) |
| B132 = 1 (needs a 2026 restatement) | (707,448.94) | (60,695) |
| B131 = 0 and B135 = 0 | (1,286,153.81) | (639,400) |
| B132 = 1 and B131 = 0 | (1,239,164.67) | (592,411) |

## Completion criteria (v13, as shipped; v14's own criteria are in the 'Changes from v13 (v14)' section)

| Criterion | Result |
|---|---|
| Suite green | all checks pass (suite_v13.py; summary above) |
| Bridge ties to the cent | sum of the five exact dept-level terms = AG132 change, difference < $0.01 (figures_v13.py assertion; exact terms on the Collation Notes v13 block) |
| B131 = 0 scenario still computes; its new value stated | AG132 = (1,205,750.10); PO 5110-5140 base 590,317.51 = 590,317.51 |
| Roster totals match the user's file's Z totals | all four tabs, difference 0.00 (HC-CO matches because r20 carries the user's Nov-26 end month) |
| No severed refs | 0 #REF! in formulas, caches and names (v13 and its recalc; re-proven on v14); 6 historical text mentions on Collation Notes (wording rescoped in v14) |
| Two-pass content-identical | run_build_v13.sh runs the whole pipeline twice; both passes' md byte-identical and xlsx part-identical after sorting <dataValidations> children (normcmp_v12.py; the engine's one nondeterministic element order + wall-clock zip timestamps, the v12-documented deviation). The shipped workbook is pass 1's engine save, untouched. |
| Diff confined | 0 violations (table above); frozen sheets 0 changes; 2026 P&L columns 0 changes; HC 2026-side cells disclosed |
| No names in md / CSVs (none written) / Collation Notes | privacy_v6 hits 0; paylist_v10 exact per-person hits 0 (single-person amounts shown with '~') |

## Build and sources

Output (v13): `02-build/02-build_COO_2027_Budget_Collated_v13.xlsx` and `02-build_notes_v13.md` (v1-v12 files unchanged; no v13 CSV). Output (v14): `02-build/02-build_COO_2027_Budget_Collated_v14.xlsx` and this file - the v14 pipeline is in the 'Changes from v13 (v14)' section.
Entry point `scripts/run_build_v13.sh` (the whole pipeline runs twice; the md must be byte-identical and the xlsx content-identical across passes):
build_v13.py stage1 (the A-G cell edits on v12; roster names read from the user's file only) -> recalc.sh (full LibreOffice recalculation) -> scen_v8.py x5 + recalc.sh (B131/B135/B132 single and double switches) -> figures_v13.py (every figure + tie assertions + the user-file Z cross-check) -> build_v13.py stage2 (Collation Notes in-place updates + v13 block, from the figures) -> recalc.sh = THE ENGINE SAVE (the deliverable; one full recalculation + save, no post-processing) -> diff_v13.py (confinement, exit 1 on violation) -> suite_v13.py -> scenread_v12.py on 3 re-run switches of the shipped file -> recon_v13.py + names_v11.py + cntext_v12.py + privacy_v6.py + paylist_v10.py (name and per-person-amount gates; scratch name list outside the repo, deleted) -> report_v13.py (this file). run_build_v12.sh ... run_build.sh still reproduce v12 ... v1.
Inputs (read-only): the four v12-listed sources (unchanged, sha256 in the v12 notes) plus `USER_EDIT_FINAL_v4_HC.xlsx` sha256 `02c83e1bdc230aac61e32ad194f97f3f717790122156610b03da097bd9a3e773` (roster names and the r20 end month; its severed PO formulas and typed CO constants are NOT imported - brief v8 correction).
Base: v12 workbook sha256 `b8e52e2bfdb7ba28ba53039f5cf80064b6787dfc312bf7426319b55616f854f9`. LibreOffice 24.2.7.2; Python with -I. Edit technique: openpyxl stage passes + one final LibreOffice full-recalc engine save (v12 technique; the package-patch method stays retired).

## Sections of the v12 notes not restated

Unchanged by v13 and not repeated here (02-build_notes_v12.md and the v9/v10 sections it carries): the v12 #REF! diagnosis and engine-save hardening, production-labour capitalisation mechanics, Prod Payroll model, depreciation schedule, revenue build, DeploySum tie-out, variance scan, duplicate scan, FO/FE payroll reconciliation detail, assumptions A-01..A-45, the unchanged issue rows, decisions #2-#5 and #10 (still open, unchanged effects vs the new headline shown in the caveat table). Where those sections quote the v12 contribution (159,136) or v12 wiring of CO/PE/PO payroll rows, this file supersedes them.

## Decisions (v13, builder)

- D1 (v13): Edit method - openpyxl stage passes on v12, then ONE full LibreOffice recalculation + engine save as the deliverable (the v12 technique; nothing is spliced into saved parts). Proven safe first: an unedited openpyxl round-trip + engine save of v12 semantically diffs to v12 with 0 differences (fdiff_v12.py, 253,036 cells).
- D2 (v13): The Team Lead row's Nov-26 end month is taken from the user's file (the handoff's blocker rule for roster details the brief does not pin down), which also makes every roster Z total equal the user's file exactly. Consequence (no 2027 expense line carries the role) disclosed as restated I-41 + A-47 with the one-cell flip.
- D3 (v13): HC-PO r20 is blanked, not deleted: every dependent formula (HC-PO totals, HC-COO roll-up, the new PO base) stays un-severed and row addresses stay stable - the exact failure mode of the user's in-Excel deletion cannot recur.
- D4 (v13): The PM lands in the New Hires block (r41; the user's own block, our row numbering), which keeps him outside the 5110-5140 basis BY CONSTRUCTION (the basis sums the Current Employees block M14:M33) rather than by a subtraction term.
- D5 (v13): The de-dup is implemented in CO's formulas (handoff preference); the Logistics&WH tab remains an unedited SD copy. The excluded seats are subtracted row by row so each exclusion is visible and individually reversible (A-46's one-term flip).
- D6 (v13): PO!U68:AF69 compute the PM's tax/benefits as M41 x D6/D7 directly (not via HC-PO totals, which also hold the 8 capitalised production staff), so the expensed amount is exactly one person at PO HC rates.
- D7 (v13): The Collation Notes sheet is updated in place (stale current-state cells) plus a v13 block appended below row 810; no rows are inserted, so every existing cell address (incl. the H78:H81 checks and v7-v12 historical sections, kept as records) is stable.
- D8 (v13): Caveat effects are recomputed where v13 moved their inputs (the 3 switch scenarios + 2 double switches, I-41, I-37, the burden-rate item); all other effects are carried from v12 with the diff as evidence their inputs are untouched - and the carried scenario deltas are re-verified against the recomputed ones (<= $2).
- D9 (v13): Scenarios are computed on the recalculated stage-1 content; the suite proves the deliverable value-identical outside the Collation Notes sheet, and the three single switches are re-run on the shipped file itself (B131 = 0 also re-checks the 590,317.51 base).
- D10 (v13): Names flow user-file -> workbook only; these notes, the JSONs and the return message carry none (privacy gate), and single-person amounts appear rounded ('~') with exact values kept on the Collation Notes sheet (banner convention).

## Not done / limits

- The user's Excel open-test is still the final check (validation here is LibreOffice-only, as in v12). On a clean open, PO rows 33-35 and 67-69 show values, not #REF!.
- The 2026 P&L columns are book data and were NOT restated for the Sep-Dec-26 starters (their 2026 cost is on the HC tabs only). If the new hires (or the model's 2026 logistics hires) are on 2026 payroll, the 2026 forecast needs a separate update.
- I-42: the 7700 'Inventory Obsolescence-old' label awaits the user's confirmation; the 24,000 sits on that row meanwhile.
- The Prod Payroll model still counts 9 current staff by number (brief v6: leave the model unchanged); the 9-of-9 MH-01 overlap caveat stands (+2,821).
- The 'Logistics&WH Payroll' tab banner still reads 'rolls up to Production Operations' (unedited SD copy by design; superseded note on Collation Notes).
- The Material Handling Team Lead's 2027 treatment rests on the user's Nov-26 end date (A-47/I-41): the PO owner's three-way answer (left at Nov-26 / warehouse and staying / production) decides the fix. HC-CO F20 = Dec-27 alone only adds the CO expense; the capitalised side (B131 base, by-number model) needs its own edit in two of the three branches (v14, critic v13 B1).
- The user's file's Material Handler name spelling (HC-CO r19) was copied as typed; it differs slightly from the old HC-PO r20 spelling of the same person (same role, salary and move per the brief). Not reconciled - roster hygiene for the user.
- Pending user answers (verifier v13; NOT acted on in v14 - no number changed): (1) PO!R24:R26 production freight (5025/5026/5027) is 'YOY Growth' in the user's edited file vs 'Even'/0 carried since v1; carrying it would add 60,056.60 of 2027 COGS (AG132 about (706,810)). (2) HC-PE!A22 'transfer?' flag is blank in the user's file; no number changes either way, and I-35's ~255,000 upside rests on it.
- 05-final packaging (FINAL_v5) is the orchestrator's step after verification, not part of this build.
