"""v14 notes: generated from the v13 notes by ASSERTED in-place replacements plus the 'Changes from v13 (v14)'
section. Each replacement must match exactly once (exit on any drift); the output is then self-checked for banned
stale strings and required new strings, and cross-checked against the pass's sweep results. No clock, no file
properties, no dates are read (F1 rule); all content is deterministic, so the two passes are byte-identical.

Usage:
  python3 -I report_v14.py V13_MD SWEEP_PRE_JSON OUT_MD
"""
import sys, json

V13MD, SWEEPJ, OUT = sys.argv[1:4]

NEW_SECTION = """## Changes from v13 (v14): documentation corrections only - no value changes

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

"""

R = [  # (old, new) - each must occur exactly once in the v13 md
 ("# 02-build notes v13 - 2027 COO budget collation (CO 7700/8600 inputs + the user's HC roster merge, decisions 1-4)",
  "# 02-build notes v14 - 2027 COO budget collation (documentation corrections on v13; all v13 figures unchanged)"),
 ("\n## Changes from v12 (v13)\n",
  "\n" + NEW_SECTION + "\n## Changes from v12 (v13)\n"),
 ("| Gross Profit | 64 | 2,945,924 | 4,038,561 | 1,092,637 | 37% | 4,038,561 | 0 |",
  "| Gross Profit | 64 | 2,945,924 | 4,038,561 | 1,092,637 | 37% | 3,960,032 | 78,529 |"),
 ("additions - ten hires/moves (4 CO, 5 PE, 1 PO) plus",
  "additions - 11 hires/moves (4 CO, 5 PE, 1 PO, 1 FE; count and scope as defined in the conclusion) plus"),
 ("(iii) The Material Handling Team Lead's CO roster row is end-dated Nov-26 (the user's file), so neither CO nor "
  "any PO expense line carries that role in 2027 while seat TL-01 is excluded - a deliberate one-cell flip if wrong "
  "(I-41/A-47).",
  "(iii) The Material Handling Team Lead's CO roster row is end-dated Nov-26 (the user's file), so neither CO nor "
  "any PO expense line carries that role in 2027 while seat TL-01 is excluded. v14: the previously advertised "
  "one-cell flip (HC-CO F20 = Dec-27) is NOT a complete fix - it adds ~70,000 of CO expense while the role stays "
  "inside the capitalised labour (HC-PO r16 in the B131 base; the Prod Payroll model counts by number), carrying it "
  "twice; and if the person in fact left at Nov-26, the B131 = 0 base, LB2 and the by-number model all carry a "
  "departed person (I-41/A-47)."),
 ("brief v8: the HC roster merge - 4 CO adds, 5 PE adds, the PO Production Manager, the FE Associate, I-28 resolved)",
  "brief v8: the HC roster merge - 11 hires/moves: 4 CO, 5 PE, 1 PO (the Production Manager), 1 FE (the Associate; "
  "roster row only - he was already costed in FE), counted as roster rows added on the four HC tabs, the HC-CO r18 "
  "title edit and HC-PO r20 blanking not among them, the CO Team Lead row carrying no 2027 cost; I-28 resolved)"),
 ("and the PO owner answers the restated I-41 (the Team Lead's Nov-26 end date and seat TL-01).",
  "and the PO owner answers the restated I-41 three-way (left at Nov-26 / warehouse / production - Collation Notes "
  "H381)."),
 ("One cell flips it: HC-CO F20 = Dec-27 costs the person in CO (+~70,000 at CO HC rates). Restated as I-41.",
  "v14 (critic v13 B1): HC-CO F20 = Dec-27 ALONE is not a complete fix - it costs the person in CO (+~70,000 at CO "
  "HC rates) while r16 stays in the 8-person B131 base and the by-number Prod Payroll model keeps capitalising the "
  "role: carried twice (expense + robot cost), asset overstated ~70k. And if the person actually LEFT at Nov-26 "
  "(the backfill reading), r16, the live B131 = 0 base (590,317.51 - it falls by the r16 cost, ~70,000, without "
  "that row), lower bound 2 and the by-number model all carry a departed person: the B131 = 0 scenario "
  "((1,205,750.10)) and LB2 ((1,714,922)) are ~70,000 too negative, and on the 9-of-9 reading the capitalised "
  "asset is ~70,056 too high (2027 depreciation 2,821). Exact figures on the Collation Notes I-41/A-47 rows. "
  "Restated as I-41."),
 ("so HC-COO's roster-level FO+FE payroll counts him twice while the P&L costs him once, in FE. HC-COO 2027 total "
  "payroll 5,855,984 (v12 4,863,502).",
  "so HC-COO's roster-level FO+FE payroll counts him twice while the P&L costs him once, in FE. v14 (critic v13 "
  "O1): the Material Handling Team Lead is likewise double-listed - HC-PO r16 (Sep-26..Dec-27) and HC-CO r20 "
  "(Sep-26..Nov-26) - so HC-COO's roster-level payroll and headcount count that person twice in Sep-Nov-26 "
  "(2026-side columns only); from Dec-26 and for all of 2027 the HC-CO row costs 0, so 2027 is unaffected. HC-COO "
  "2027 total payroll 5,855,984 (v12 4,863,502)."),
 ("The CO 6610-6640 composition (roster + in-seats = P&L) ties to < $0.01 per GL (build assertion + live H78:H81).",
  "The CO 6610-6640 composition (roster + in-seats = P&L) ties to < $0.01 per GL (build assertion + live H78:H81).\n"
  "\n"
  "v14 (critic v13 O2) - the MH-02 <-> Material Flow Supervisor swap is asymmetric: the seat goes OUT at the "
  "model's cost (~60,000 at model rates - exact on the Collation Notes seat table), while the realized hire comes "
  "IN on the roster at 85,000 salary + CO HC burden (100,304.86 of 2027 cost); net ~ +38,300 of cost inside the "
  "(71,048.29) B+D term. The asymmetry is the price of realizing the backfill seat at a higher salary and CO HC "
  "rates (the swap itself is user-confirmed, A-46)."),
 ("| I-41 | MED | **Restated.** The Material Handling Team Lead: HC-PO r16 (Sep-26..Dec-27, inside the capitalised "
  "base) AND HC-CO r20 (Sep-26..Nov-26, 2027 cost 0 - the user's file value, A-47). Booked: PO expenses 0 "
  "(capitalised), CO excludes seat TL-01 as roster-realized -> no 2027 expense line carries the role: (~70,000) if "
  "it should stay an expense (7-of-9 reading). 0 if the end date is right and the Material Flow Supervisor (in CO) "
  "is the replacement. Under B131 = 0 the role is expensed inside PO 5110-5140 (and the exposure is 0 there). "
  "One-cell alternative: HC-CO F20 = Dec-27 books the person in CO (+~70,000). PO owner to confirm. |",
  "| I-41 | MED | **Restated in v13; completed in v14 (critic v13 B1).** The Material Handling Team Lead: HC-PO "
  "r16 (Sep-26..Dec-27, inside the capitalised base and - by headcount - the by-number Prod Payroll model) AND "
  "HC-CO r20 (Sep-26..Nov-26, 2027 cost 0 - the user's file value, A-47). Booked: PO expenses 0 (capitalised), CO "
  "excludes seat TL-01 as roster-realized -> no 2027 expense line carries the role. Three branches: (1) warehouse "
  "role, person stays (7-of-9 reading): (~70,000) should stay an expense; flipping HC-CO F20 = Dec-27 ALONE books "
  "+~70,000 in CO while the capitalised side keeps the role (r16 in the B131 base; the model counts by number) - "
  "carried twice, asset overstated ~70k. (2) Person left at Nov-26 (the backfill reading): r16, the live B131 = 0 "
  "base (590,317.51; ~70,000 lower without r16), LB2 and the by-number model carry a departed person - the B131 = "
  "0 scenario ((1,205,750.10)) and LB2 ((1,714,922)) are ~70,000 too negative; on the 9-of-9 reading the asset is "
  "70,056 too high (2027 depreciation 2,821). (3) Production role, stays: booked treatment right. Under B131 = 0 "
  "the role is expensed inside PO 5110-5140. PO owner to answer the three-way (Collation Notes H381). |"),
 ("| MH-02 excluded from the CO add-on ((~60,000)); if wrong, one formula term per CO row flips it back (+ that "
  "amount) |",
  "| MH-02 excluded from the CO add-on ((~60,000)); if wrong, flip it back by deleting the -'Logistics&WH "
  "Payroll'!<col>39 term in each of the 12 month columns U:AF of CO row 67 and the row-39 term inside the "
  "bracketed subtraction on rows 68/69 (x B5/B6 there), and co-edit the H78:H80 check formulas on the Collation "
  "Notes sheet (their S39 terms); flipping back ADDS that ~60,000 of 2027 cost - the contribution falls by it "
  "(v14, critic v13 O3) |"),
 ("| one cell to flip (HC-CO F20 = Dec-27: +~70,000 CO cost) |",
  "| HC-CO F20 = Dec-27 books +~70,000 of CO cost but leaves the role in the capitalised labour; if the person "
  "left at Nov-26, r16 and the B131 = 0 base carry a departed person (both: I-41, v14) |"),
 ("## Error scan and suite (all green)",
  "## Error scan and suite (all green; re-run on v14)"),
 ("- 0 error caches in v13 and in its LibreOffice recalculation; 0 '#REF!' anywhere in stored formulas (the user's "
  "severed-reference incident cannot recur from this file); 0 shared formulas in the package.",
  "- 0 error caches in v14 and in its LibreOffice recalculation; 0 #REF! in formulas, caches and names - 6 "
  "historical text mentions of '#REF!' remain on the Collation Notes sheet (cells E343, D364, D365, E365; records "
  "of the v2/v3 error cleanups) - and the user's severed-reference incident cannot recur from this file; 0 shared "
  "formulas in the package (wording rescoped in v14 per verifier v13)."),
 ("- A full LibreOffice recalculation of v13 reproduces its own cache (numeric <= 1e-6); the deliverable is "
  "value-identical to the recalculated stage-1 content outside the Collation Notes sheet, so the figures and "
  "scenarios below hold for the shipped file.",
  "- A full LibreOffice recalculation of v14 reproduces its own cache (numeric <= 1e-6); the deliverable is "
  "value-identical to v13 outside the Collation Notes sheet (diff-asserted), so the v13 figures and scenarios "
  "below hold for the shipped file."),
 ("- Collation Notes: the 32 live headline formulas (C21:F28) are unchanged from v12; H78:H81 (the CO de-dup "
  "check) cache and recalculate to 0.",
  "- Collation Notes: the 32 live headline formulas (C21:F28) are unchanged (identical in v12, v13 and v14); "
  "H78:H81 (the CO de-dup check) formulas are v13's and cache and recalculate to 0."),
 ("## Completion criteria (v13)",
  "## Completion criteria (v13, as shipped; v14's own criteria are in the 'Changes from v13 (v14)' section)"),
 ("| No severed refs anywhere | 0 #REF! in formulas and caches (v13 and its recalc) |",
  "| No severed refs | 0 #REF! in formulas, caches and names (v13 and its recalc; re-proven on v14); 6 historical "
  "text mentions on Collation Notes (wording rescoped in v14) |"),
 ("Output: `02-build/02-build_COO_2027_Budget_Collated_v13.xlsx` and this file (v1-v12 files unchanged; no v13 "
  "CSV).",
  "Output (v13): `02-build/02-build_COO_2027_Budget_Collated_v13.xlsx` and `02-build_notes_v13.md` (v1-v12 files "
  "unchanged; no v13 CSV). Output (v14): `02-build/02-build_COO_2027_Budget_Collated_v14.xlsx` and this file - the "
  "v14 pipeline is in the 'Changes from v13 (v14)' section."),
 ("- The Material Handling Team Lead's 2027 treatment rests on the user's Nov-26 end date (A-47/I-41): one cell "
  "(HC-CO F20) flips it if wrong.",
  "- The Material Handling Team Lead's 2027 treatment rests on the user's Nov-26 end date (A-47/I-41): the PO "
  "owner's three-way answer (left at Nov-26 / warehouse and staying / production) decides the fix. HC-CO F20 = "
  "Dec-27 alone only adds the CO expense; the capitalised side (B131 base, by-number model) needs its own edit in "
  "two of the three branches (v14, critic v13 B1)."),
 ("- 05-final packaging (FINAL_v5) is the orchestrator's step after verification, not part of this build.",
  "- Pending user answers (verifier v13; NOT acted on in v14 - no number changed): (1) PO!R24:R26 production "
  "freight (5025/5026/5027) is 'YOY Growth' in the user's edited file vs 'Even'/0 carried since v1; carrying it "
  "would add 60,056.60 of 2027 COGS (AG132 about (706,810)). (2) HC-PE!A22 'transfer?' flag is blank in the user's "
  "file; no number changes either way, and I-35's ~255,000 upside rests on it.\n"
  "- 05-final packaging (FINAL_v5) is the orchestrator's step after verification, not part of this build."),
]

BANNED = ["ten hires/moves", "13 hires/moves", "| 4,038,561 | 0 |", "0 '#REF!' anywhere", "No severed refs anywhere",
          "One cell flips it:", "one cell to flip (HC-CO F20", "one formula term per CO row flips it back",
          "would be (2,289,154)", "-> (399,860)", "a deliberate one-cell flip if wrong"]
REQUIRED = ["Changes from v13 (v14)", "3,960,032", "(3,095,044)", "(706,810)", "sweep_v14.py", "100,304.86",
            "11 hires/moves", "left at Nov-26", "Three branches", "6 historical text mentions"]

EXPECTED_SWEEP = sorted({
    "E17:399,860", "E17:32,228", "E17:480,264", "E17:98,441", "A32:2,289,154", "A33:13 hires",
    "A35:A35-stale", "A35:A35-stale2", "C43:319,393", "C43:74,099", "C43:54,703", "C47:398,492",
    "C60:15,525", "C60:2,715", "C60:43,967", "C61:3,100,031", "C323:77,882", "C323:34,169", "C336:19,396",
    "F357:398,492", "D377:62,207", "E377:21,081", "E377:12,834", "E377:43,967", "E377:77,882", "E377:26,350",
    "F377:62,207", "F377:34,169", "G377:62,207", "D380:399,860", "A873:10 user-approved [whole-sheet]"})

text = open(V13MD, encoding="utf-8").read()
for old, new in R:
    k = text.count(old)
    assert k == 1, f"replacement anchor not unique (count {k}): {old[:80]!r}"
    text = text.replace(old, new)
for b in BANNED:
    assert b not in text, f"banned string still present: {b!r}"
for r in REQUIRED:
    assert r in text, f"required string missing: {r!r}"
sweep = json.load(open(SWEEPJ))
got = sorted(set(sweep["disallowed"]))
assert got == sorted(EXPECTED_SWEEP), f"sweep pass-1 findings differ from the documented list: {got}"
assert len(got) == 31, f"sweep pass-1 count {len(got)} != 31"
open(OUT, "w", encoding="utf-8").write(text)
print(f"report_v14: {len(R)} asserted replacements on the v13 notes; sweep pass-1 findings (31) cross-checked -> {OUT}")
