# 02-build notes v2 - 2027 COO budget collation

Output: `02-build/02-build_COO_2027_Budget_Collated_v2.xlsx`  
Pruned-name log: `02-build/02-build_pruned_names_v2.csv`  
Scripts: `02-build/scripts/` - v2 entry point `run_build_v2.sh` (build.py --mark-frozen-zeros, prune_names.py, recalc.sh, analyze.py, analyze_v2.py, pkgscan.py, diff_versions.py, report.py). `run_build.sh` still reproduces v1 (it calls the frozen `report_v1.py`).  
Inputs (read-only): `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `a3264ef4305e1e7da7c8cf7efbcd5407556aba56e85d50375f9ece711199e9b4`; `Service_Delivery_PL_worksheets.xlsx` sha256 `fedee8d16eb7db72d2745e77a7c6441057b4229131c52d25c944dbb5b858a466`  
Recalculation engine: LibreOffice 24.2.7.2 420(Build:2) (from `soffice --version`); openpyxl 3.1.5; Python 3.13.16.

## Headline

- **Total 2027 COO cost (COGS + Opex, COO P&L AG63 + AG116): 11,851,351** vs 2026 8,407,973 (N63 + N116), change 3,443,378 (41%). Before the FO/FE swap the COO book showed 5,277,004 for 2027.
  - COGS 2027 8,833,209 (2026 4,478,016); Opex 2027 3,018,142 (2026 3,929,957).
- 2027 Net Income (AG132) (11,851,351) is **incomplete**: 2027 revenue is 0 (2026 7,423,940, I-01) and 2027 depreciation is 0 (2026 1,788,097, I-07). Do not present it as a result.
- New formula errors introduced by the merge: **0**. COO P&L roll-up: 2911 cells checked, 0 off by more than $1 (max abs diff 0.0000); check row 133 max abs = 0.000000.
- v1 vs v2: 26,388 cells on 11 budget/driver sheets compared; **0 formula and 0 value differences**. Only comments were added (17).
- Package: 0 externalLink parts; defined names 14,310 -> 8,965.
- Issues: 6 HIGH, 7 MED, 16 LOW (scale below). Cross-department overlap: 0 likely double counts, 3 unclear rows (I-28).

## Changes from v1

| Item | Critic finding | What v2 did |
|---|---|---|
| B1 | Freeze of DeploySum [1] cells described as 'as instructed'. | Reworded everywhere (Method, I-03, D2, Collation Notes): frozen per orchestrator handoff; a declared deviation from brief criterion 1 because the linked workbook was not supplied and the SD file has no externalLink part (SD package externalLink parts: 0). Original formulas remain listed on Collation Notes. |
| B2 | No-external-link claim vs I-24 external .xls names; clean open unproven. | Package inspected (section 'Package and defined names'): externalLink parts 0, <externalReference> elements 0, chart parts 0. The 15 'external' names were quoted string/array constants, not links. Name usage scanned across cell formulas, data validations, conditional formats, charts, print areas/titles and other names: 0 uses. Pruned 5,345 unused #REF!/external-looking names (logged, 02-build_pruned_names_v2.csv); definedNames 14,310 -> 8,965. |
| B3 | Cross-department double counting unchecked. | Added 'Cross-department overlap' table: 9 GL rows (+3 memo rows) with 2+ depts non-zero in 2027, each traced: 5 legitimate, 1 likely legitimate, 3 unclear, 0 likely double counts. Prod Payroll trace: rates/timing only. New issues I-26..I-29. |
| O1 | Hard-coded claims in report.py. | report.py rewritten: every number/fact comes from analysis JSON; LibreOffice version read from `soffice --version` ('LibreOffice 24.2.7.2 420(Build:2)'). v1 report kept as report_v1.py for v1 reproduction only. |
| O2 | Logistics&WH: quantify vs PO. | I-17: 547,441 2027 vs PO 5100 652,820; re-rated to HIGH. Also found MH-05 gap (I-27). |
| O3 | Quantify MeLi double count. | I-06: $0 in current cells (Fld Ops Payroll!B11 = 14, domestic only); 5310 breakdown given; comment stale; re-rated to LOW. |
| O4 | Downgrade I-05. | I-05 re-rated to LOW: Prod Payroll supplies only typed rate/timing inputs. |
| O5 | Downgrade I-16. | I-16 re-rated to LOW. |
| O6 | Headline should lead with total COO cost. | Headline now leads with 2027 COGS + Opex 11,851,351 vs 2026 8,407,973; Net Income labelled incomplete (no revenue, no depreciation). |
| O7 | sheet!cell everywhere; define severities. | Every issue has a sheet!cell (or the workbook <definedNames> location for I-24); severity scale and tie-break rule stated; each issue shows the basis used. Counts: {'HIGH': 6, 'LOW': 16, 'MED': 7}. |
| O8 | 'Untouched' wording. | Replaced by 'values and formulas unchanged (verified); formatting re-saved by LibreOffice'. |
| O9 | Limits not stated. | Limits listed (page setup/print settings, sheet-scoped names, Excel not used, Google parts) in 'Not done / limits'. |
| O10 | Stale zeros look like data; raise-timing check. | Cell comments added on 17 frozen non-error cells (B17:R17 on DeploySum): 'stale external-link value – not real data'. Raise-timing consistency check done (section 'Raise timing'); one rule difference logged as I-29. |

Issue-level changes (severity v1 -> v2):

| ID | v1 | v2 | Change |
|---|---|---|---|
| I-01 | HIGH | HIGH | Unchanged |
| I-02 | HIGH | HIGH | Unchanged |
| I-03 | HIGH | HIGH | Wording: 'as instructed' replaced by the declared-deviation statement (B1). |
| I-04 | HIGH | HIGH | Unchanged |
| I-05 | HIGH | LOW | O4: $0 budget impact; it supplies typed rate/timing inputs only. Severity HIGH -> LOW. |
| I-06 | HIGH | LOW | Quantified (O3): overlap $0 in current cells; comment stale. Severity HIGH -> LOW. |
| I-07 | HIGH | HIGH | Unchanged |
| I-08 | MED | LOW | Total plugs quantified. Severity MED -> LOW. |
| I-09 | LOW | LOW | Unchanged |
| I-10 | MED | MED | Unchanged |
| I-11 | MED | MED | Location now sheet!cell (O7). |
| I-12 | MED | MED | Unchanged |
| I-13 | MED | MED | Unchanged |
| I-14 | LOW | MED | Stated scale applied: impact not determinable, owner confirmation needed. Severity LOW -> MED. |
| I-15 | MED | LOW | Quantified: $0 overlap; comment stale. Severity MED -> LOW. |
| I-16 | MED | LOW | O5: < $50k and 2026 line mapping only. Severity MED -> LOW. |
| I-17 | MED | HIGH | Quantified (O2): possible understatement of PO. Severity MED -> HIGH. |
| I-18 | LOW | LOW | Unchanged |
| I-19 | LOW | LOW | Unchanged |
| I-20 | LOW | LOW | Location now sheet!cell (O7). |
| I-21 | LOW | LOW | Unchanged |
| I-22 | LOW | LOW | Unchanged |
| I-23 | LOW | LOW | Unchanged |
| I-24 | LOW | LOW | Partly fixed in v2 (B2): logged prune of #REF!/external-looking names. |
| I-25 | LOW | LOW | Unchanged |
| I-26 | new | MED | New in v2. |
| I-27 | new | LOW | New in v2. |
| I-28 | new | MED | New in v2. |
| I-29 | new | LOW | New in v2. |

## Severity scale

HIGH = blocks sign-off or > $250k impact; MED = $50k-250k or needs owner confirmation; LOW = < $50k or hygiene.

Applied in this order: (1) HIGH if the item blocks sign-off or its $ impact computed from the workbook is > $250k; (2) MED if that impact is $50k-250k; (3) MED if the impact cannot be determined from the workbook and an owner must confirm; (4) otherwise LOW (impact < $50k, $0, or hygiene). 'Impact' is the amount the item could move the 2027 budget, read from cells; where only an exposure (the amount resting on the item) is known, it is shown but not used as the impact.

## Method

1. **Base = COO book**, loaded with formulas (openpyxl). Its `FO` and `FE` tabs were deleted and rebuilt in the same positions (tab 2 and 5 of the COO book).
2. **Copied cell by cell from the SD book**: value or formula (array formulas re-created), font, fill, border, alignment, number format, protection, hyperlinks, notes; merged ranges; column widths/hidden/outline; row heights/hidden; freeze panes, gridlines, zoom, tab colour, sheet state; data validations; conditional formats.
3. **Dependency closure** of SD `FO`/`FE` formulas: FO, FE, Fld Maint Budget, Fld Ops Payroll, Fld Eng Budget, DeploySum, Prod Payroll. SD defined names: 1 (_xlnm._FilterDatabase@Fld Maint T&E Data; sheet-scoped, not carried; see limits).
4. **External links (declared deviation)**: 427 DeploySum formula cells reference `[1]` (2026 Exist New, Deploy, Deploy Detail, Expansion, New Sales, Revenue Roll-up). They were frozen to the SD cached values **per orchestrator handoff; this is a declared deviation from brief criterion 1 because the linked workbook was not supplied and the SD file has no externalLink part** (SD package externalLink parts: 0). Cached values: {'#ERROR!': 175, '#REF!': 202, '0': 17, '#N/A': 33}. Google `#ERROR!` has no Excel equivalent and was stored as `#REF!`. Every cell and its original formula is on the `Collation Notes` sheet and summarised in the appendix. Apart from these, formulas in source = formulas in output on every sheet (sheets with a different count: none).
5. **COO P&L, PO, CO, PE: values and formulas unchanged (verified); formatting re-saved by LibreOffice.** COO P&L formulas reference `FO!`/`FE!` by name, so they pick up the new tabs.
6. **v2 additions**: cell comments on the 17 frozen non-error cells ('stale external-link value – not real data'); logged prune of unused #REF!/external-looking defined names (`prune_names.py`, XML-level, only `xl/workbook.xml` rewritten).
7. **Recalculated** with headless LibreOffice 24.2.7.2 420(Build:2) using a private profile set to always recalculate on load; reloaded with `data_only=True` and compared every cell with the source cached values. The delivered file is the LibreOffice-recalculated file.

## Package and defined names (B2)

Final package `02-build_COO_2027_Budget_Collated_v2.xlsx`: 37 parts.

- `xl/externalLinks/*`: **0** parts; `<externalReference>` elements in workbook.xml: 0. Chart parts: 0. COO input externalLink parts: 0; SD input: 0.
- Package parts: `[Content_Types].xml`, `_rels/.rels`, `docProps/app.xml`, `docProps/core.xml`, `docProps/custom.xml`, `xl/_rels/workbook.xml.rels`, `xl/comments10.xml`, `xl/comments11.xml`, `xl/comments12.xml`, `xl/comments8.xml`, `xl/comments9.xml`, `xl/drawings/vmlDrawing1.vml`, `xl/drawings/vmlDrawing2.vml`, `xl/drawings/vmlDrawing3.vml`, `xl/drawings/vmlDrawing4.vml`, `xl/drawings/vmlDrawing5.vml`, `xl/sharedStrings.xml`, `xl/styles.xml`, `xl/theme/theme1.xml`, `xl/workbook.xml`, `xl/worksheets/_rels/sheet10.xml.rels`, `xl/worksheets/_rels/sheet11.xml.rels`, `xl/worksheets/_rels/sheet12.xml.rels`, `xl/worksheets/_rels/sheet8.xml.rels`, `xl/worksheets/_rels/sheet9.xml.rels`, `xl/worksheets/sheet1.xml`, `xl/worksheets/sheet10.xml`, `xl/worksheets/sheet11.xml`, `xl/worksheets/sheet12.xml`, `xl/worksheets/sheet2.xml`, `xl/worksheets/sheet3.xml`, `xl/worksheets/sheet4.xml`, `xl/worksheets/sheet5.xml`, `xl/worksheets/sheet6.xml`, `xl/worksheets/sheet7.xml`, `xl/worksheets/sheet8.xml`, `xl/worksheets/sheet9.xml`
- Defined names: COO book 14,310 -> output before prune 14,310 -> pruned 5,345 -> **final 8,965**. Final by category: {'array constant': 660, 'string constant': 8167, 'range/other': 138}. Built-in `_xlnm.*` names (print areas/titles/filters): 0. Sheet-scoped names: 0.
- Usage scan (every formula-bearing XML element in every part, plus the text of every other defined name): elements scanned {'cell': 17496, 'cf': 76, 'dv': 46} (cell = cell formulas, dv = data validations, cf = conditional formats; chart formulas would be counted as 'chart'). Names referenced from parts: 0; from other names: 0.
- Prune rule: unused AND target contains '[' or '.xls' (any case) or '#REF!'. Candidates 5,345, of which used 0; pruned 5,345 (5,330 #REF!, 15 external-looking). List: `02-build/02-build_pruned_names_v2.csv`. Re-scan of the final file: pruned names still defined 0, still referenced 0.
- The external-looking names were text, not links: `CIQWBGuid` = "Project Radar - Operating Model_v1.xlsx"; `DME_ODMALinks1` = "::ODMA\DME-MSE\London-44590=C:\TEMP\Dme\London-44590.xls"; `HTML1_1` = "[FCFF3]Sheet1!$A$1:$L$34"; `HTML10_1` = "[Daily.xls]Web!$A$1:$Q$26"; `HTML2_1` = "[WebDaily.xls]Sheet1!$A$1:$V$32"; `HTML3_1` = "[WebDaily.xls]Sheet1!$A$1:$R$32"; `HTML4_1` = "[WebDaily.xls]Sheet1!$A$1:$Q$28"; `HTML5_1` = "[WEBDAILY.XLS]Sheet1!$A$1:$Q$28"; `HTML6_1` = "[DAILY.XLS]Web!$A$1:$Q$28"; `HTML7_1` = "[DAILY.XLS]Web!$A$1:$M$28"; `HTML8_1` = "[DAILY.XLS]Web!$A$1:$M$26"; `HTML9_1` = "[DAILY.XLS]Web!$A$1:$Q$26"; `M_PlaceofPath` = "F:\GCAPPELL\VDF_Model_Backups\Education\STRA_VDF.xls"; `OO_Book_Settings_XCDestination` = "Y:\TM1WebFolder\Production Workbooks\Mfg Income Statement_x; `wrn.PRINT1.` = {"cf1.xls",#N/A,FALSE,"CF";"cfseg1.xls",#N/A,FALSE,"CF";"REV. They never created an externalLink part.
- Result: **the final package has 0 externalLink parts**, and no remaining defined name targets an external file or #REF! (remaining names meeting the prune criterion: 0). Opening in Microsoft Excel was not tested (no Excel available; see limits).

## Cross-department overlap (B3)

Every COO P&L GL row (label 'NNNN - ...') and the payroll memo rows 137-140 were checked: 103 rows, of which 12 have 2 or more departments non-zero in 2027 (AG). Each was traced to its driver cells.

| Row | Line | FO | PO | CO | FE | PE | COO P&L AG | Classification | Amount at risk | Driver trace |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 30 | 5050 - Travel - Deployment | 46,354 |  |  | 346,633 |  | 392,987 | Legitimate split (documented) | $0 | FO!U30 = ='Fld Maint Budget'!B90 (tech deployment travel = new sites x Fld Maint Budget!B6 0.3 x B5 2,533/trip; D6: 'FE travels every deployment (FE sheet); techs supplement where FE is short'). FE!U30 = ='Fld Eng Budget'!B74 (FE travel per weighted deployment; Fld Eng Budget!B6 = 1: 'Source: user-provided. 100% stays on the FE tab until a decision on moving deployment trav'). Fld Eng Budget!B2: 'Technician deployment travel sits on Fld Maint Budget.' Different people (techs vs field engineers). |
| 47 | 5340 - Spare Parts | 1,519,865 | 34,500 |  |  |  | 1,554,365 | Likely legitimate split | $0 | FO!U47 = ='Fld Maint Budget'!B94: spares run rate from FO-dept actuals only (Fld Maint Budget!D16: 'FO tab 5340 actuals, Jan–Jul 26 average ($147,799 ÷ 7)'), grown with SlipLifts in field. PO: PO input method 'Even', annual input S = 30000, with later months multiplied by a ramp row (PO!AF47 = =IF($R47="Manual","",IFERROR(IF($R47="YOY Growth",$N47*(1+$T47)/12,$S47/12),""))*AF146). Both depts booked 5340 in 2026 (N: FO 255,704, PO 63,637); FO's base excludes PO's spend. |
| 67 | 6610 - Salaries and Wages - SG&A |  |  | 528,452 | 713,347 | 1,078,020 | 2,319,819 | Unclear (person level) | not determinable; rows involved: CO 528,452, PE 1,078,020 | FE!U67 = ='Fld Eng Budget'!B78; Fld Eng Budget!B78 = =B68, B68 = =SUM(B59:B67) (named roster A13:A21). CO and PE U:AF are typed monthly amounts with no roster. All three booked 6610 in 2026 (CO 533,086, FE 850,615, PE 1,048,172). See I-28. |
| 68 | 6630 - Payroll Taxes - SG&A |  |  | 27,593 | 48,508 | 38,501 | 114,602 | Unclear (person level) | not determinable; rows involved: CO 27,593, PE 38,501 | Follows 6610: FE!U68 = ='Fld Eng Budget'!B79, Fld Eng Budget!B69 = =B68*$B$22; CO/PE typed. See I-28. |
| 69 | 6640 - Benefits - SG&A |  |  | 62,916 | 116,989 | 95,116 | 275,022 | Unclear (person level) | not determinable; rows involved: CO 62,916, PE 95,116 | Follows 6610: FE!U69 = ='Fld Eng Budget'!B80, Fld Eng Budget!B70 = =B68*$B$23; CO/PE typed. See I-28. |
| 74 | 6100 - Travel |  |  |  | 45,235 | 26,500 | 71,735 | Legitimate split | $0 | FE!U74 = ='Fld Eng Budget'!B76 (FE non-deployment travel: FE-tab 2026 run rate + buffer). PE: PE input method 'Even', annual input S = 6000 (plus typed overrides, I-09). Separate departments' own travel; both booked 6100 in 2026 (FE 35,010, PE 2,235). |
| 93 | 7500 - Facility Expenses |  | 5,750 |  |  | 9,380 | 15,130 | Legitimate split | $0 | PO: PO input method 'Even', annual input S = 5000; PE: PE input method 'Even', annual input S = 8400. Separate dept inputs; both booked this GL in 2026 (PO 530, PE 3,148). |
| 95 | 7550 - Tools and Equipment |  | 29,900 |  |  | 36,180 | 66,080 | Legitimate split | $0 | PO: PO input method 'Even', annual input S = 26000; PE: PE input method 'Even', annual input S = 32400. Separate dept inputs; both booked this GL in 2026 (PO 5,059, PE 21,705). |
| 99 | 8100 - Technology |  | 20,000 |  |  | 5,400 | 25,400 | Legitimate split | $0 | PO: PO input method 'Even', annual input S = 20000; PE: PE input method 'Even', annual input S = 5400. Separate dept inputs; both booked this GL in 2026 (PO 13,648, PE 3,093). |
| 137 | Salaries and Wages | 3,238,031 | 525,310 | 528,452 | 713,347 | 1,078,020 | 6,083,161 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 typed and unlinked: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |
| 139 | Payroll Taxes | 210,802 | 19,105 | 27,593 | 48,508 | 38,501 | 344,509 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 typed and unlinked: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |
| 140 | Benefits | 508,405 | 108,404 | 62,916 | 116,989 | 95,116 | 891,831 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 typed and unlinked: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |

Result: 0 likely double counts on the same GL row. Unclear rows are logged as I-28. Cross-row overlaps found while tracing: none between FO payroll and Logistics&WH (Rebecca is excluded from Logistics&WH, Logistics&WH Payroll!B55, and costed in Fld Ops Payroll row 76: 2027 77,089); one seat in neither model (MH-05, I-27); a current employee with no salary (I-26).

**Prod Payroll trace (what it supplies to Fld Ops Payroll):**

| Reader | Formula | Prod Payroll cell | Label | Typed input or formula | Value |
|---|---|---|---|---|---|
| Fld Ops Payroll!M5 | `='Prod Payroll'!M5` | Prod Payroll!M5 | Annual raise (% of salary) | typed input | 0.03 |
| Fld Ops Payroll!M6 | `='Prod Payroll'!M6` | Prod Payroll!M6 | Raise effective month | typed input | 2027-10-01 |
| Fld Ops Payroll!M7 | `='Prod Payroll'!M9` | Prod Payroll!M9 | Raise eligibility – min mths employed | typed input | 6 |
| Logistics&WH Payroll!B7 (SD, not carried) | `='Prod Payroll'!M5` | Prod Payroll!M5 | Annual raise (% of salary) | typed input | 0.03 |
| Logistics&WH Payroll!B8 (SD, not carried) | `='Prod Payroll'!M6` | Prod Payroll!M6 | Raise effective month | typed input | 2027-10-01 |
| Logistics&WH Payroll!B9 (SD, not carried) | `='Prod Payroll'!M9` | Prod Payroll!M9 | Raise eligibility – min mths employed | typed input | 6 |
| Logistics&WH Payroll!B10 (SD, not carried) | `='Prod Payroll'!M7` | Prod Payroll!M7 | New-hire cost – production ($) | typed input | 1000 |

Rates and timing only, no headcount and no cost: 796 of Prod Payroll's 901 formulas are errors (all payroll $ totals) and no other sheet reads any of its formulas. PO 5110-5140 2027 (PO!U33:AF35) are typed values with no link to any tab (12 of 12 months typed on row 33). So PO AG33 525,310 and FO 5510 share no headcount source; no double count through Prod Payroll.

### Raise timing consistency (O10)

| Input | Cell | Value / formula |
|---|---|---|
|  Prod Payroll | M5 | 0.03 (typed) |
|  Prod Payroll | M6 | 2027-10-01 (typed) |
|  Prod Payroll | M9 | 6 (typed) |
|  Fld Ops Payroll | M5 | 0.03 `='Prod Payroll'!M5` |
|  Fld Ops Payroll | M6 | 2027-10-01 `='Prod Payroll'!M6` |
|  Fld Ops Payroll | M7 | 6 `='Prod Payroll'!M9` |
|  Fld Eng Budget | B24 | 0.03 `='Fld Ops Payroll'!M5` |
|  Fld Eng Budget | B25 | 2027-10-01 `='Fld Ops Payroll'!M6` |
| SD (not carried) Logistics&WH Payroll | B7 | 0.03 `='Prod Payroll'!M5` |
| SD (not carried) Logistics&WH Payroll | B8 | 2027-10-01 `='Prod Payroll'!M6` |
| SD (not carried) Logistics&WH Payroll | B9 | 6 `='Prod Payroll'!M9` |

| Sheet | Row | Line | 2027 typed? | Month-on-month steps in 2027 (column: change) |
|---|---:|---|---|---|
| PO | 33 | 5110 - Salaries and Wages - Production | True | AD: 3.00% |
| PO | 34 | 5130 - Payroll Taxes - Production | True | AD: 3.00% |
| PO | 35 | 5140 - Benefits - Production | True | AD: 3.00% |
| CO | 67 | 6610 - Salaries and Wages - SG&A | True | AD: 3.00% |
| CO | 68 | 6630 - Payroll Taxes - SG&A | True | AD: 3.00% |
| CO | 69 | 6640 - Benefits - SG&A | True | AD: 3.00% |
| PE | 67 | 6610 - Salaries and Wages - SG&A | True | AD: 3.00% |
| PE | 68 | 6630 - Payroll Taxes - SG&A | True | AD: 3.00% |
| PE | 69 | 6640 - Benefits - SG&A | True | AD: 3.00% |
| FE | 67 | 6610 - Salaries and Wages - SG&A | False | AB: 9.55%, AD: 3.00% |
| FE | 68 | 6630 - Payroll Taxes - SG&A | False | AB: 9.55%, AD: 3.00% |
| FE | 69 | 6640 - Benefits - SG&A | False | AB: 9.55%, AD: 3.00% |

12 of 12 payroll rows step by Prod Payroll!M5 (3.00%) in month 10 of 2027 (Prod Payroll!M6); the raise inputs on Fld Ops Payroll / Fld Eng Budget / Logistics&WH are all links to those cells, so % and month are consistent. FE's other step is the new hire 'Customer Support Specialist – New hire' starting 2027-08-01. Rule difference: eligibility (Prod Payroll!M9) is applied in Fld Ops Payroll (`=F20*$B$6/12+IF(F$19>=$M$6,MIN(F20,INDEX($B20:$Q20,IFERROR(M...`) and Logistics&WH, but not in Fld Eng Budget (`=IF(B$58>=$C$13,$B$13/12*(1+IF(B$58>=$B$25,$B$24,0)),0)`) or the typed rows: I-29.

### Logistics & Warehouse payroll (O2) and MeLi (O3)

- Logistics&WH Payroll 2027 (S51) 547,441; Sep-Dec 26 (R51) 92,495. Components 2027: Base salaries 440,293; Payroll taxes 29,940; Benefits 72,208; New-hire cost 5,000. Formulas referencing the sheet in either book: 0.
- PO 2027: 5110 - Salaries and Wages - Production 525,310 (2026 137,080); 5130 - Payroll Taxes - Production 19,105 (2026 5,972); 5140 - Benefits - Production 108,404 (2026 54,271); Total - 5100 - Labor Expense - Production 652,820 (2026 197,323); 5350 - Warehouse 0 (2026 3,341). See I-17.
- MeLi: FO 5310 575,268 = techs in role 346,920 + Merida 123,900 + supervisor 104,448. Fld Ops Payroll costs 14 current techs per month (B11 = 14, domestic only). Overlap in current cells: $0. See I-06, I-15.

## Sheets in the output and why

| # | Sheet | From | State | Why |
|---|---|---|---|---|
| 1 | Collation Notes | new | visible | Source, method, changes, overlap table, issues, frozen-cell list |
| 2 | COO P&L | COO book | visible | Roll-up; values and formulas unchanged (verified) |
| 3 | FO | SD book | visible | Replaces COO FO |
| 4 | PO | COO book | visible | Values and formulas unchanged (verified) |
| 5 | CO | COO book | visible | Values and formulas unchanged (verified) |
| 6 | FE | SD book | visible | Replaces COO FE |
| 7 | PE | COO book | visible | Values and formulas unchanged (verified) |
| 8 | DeploySum | SD book | visible | Indirect FO/FE dependency (typed driver rows 53-66) |
| 9 | Fld Ops Payroll | SD book | visible | FO rows 52-54 |
| 10 | Prod Payroll | SD book | hidden | Indirect: Fld Ops Payroll!M5 <- Prod Payroll!M5, Fld Ops Payroll!M6 <- Prod Payroll!M6, Fld Ops Payroll!M7 <- Prod Payroll!M9 |
| 11 | Fld Maint Budget | SD book | visible | FO rows 29-30, 44-49 |
| 12 | Fld Eng Budget | SD book | visible | FE rows 30-31, 67-69, 74-75 |

Not carried (no FO/FE dependency): `Logistics&WH Payroll`, `Old Draft`, `Fld Maint T&E Data`. All were scanned.

## Formula preservation

| Sheet | Formulas in source | Formulas in output | External cells frozen |
|---|---:|---:|---:|
| FO | 2104 | 2104 | 0 |
| FE | 2104 | 2104 | 0 |
| Fld Maint Budget | 765 | 765 | 0 |
| Fld Ops Payroll | 1035 | 1035 | 0 |
| Fld Eng Budget | 560 | 560 | 0 |
| DeploySum | 515 | 498 | 427 |
| Prod Payroll | 901 | 901 | 0 |
| COO P&L | 3320 | 3320 | 0 |
| PO | 2072 | 2072 | 0 |
| CO | 2068 | 2068 | 0 |
| PE | 2057 | 2057 | 0 |

DeploySum output count (498) = 88 formulas kept + 410 error constants that LibreOffice saves as `=#REF!`/`=#N/A` formulas; 17 frozen cells are stored as numbers.

## Reconciliation (source cached vs output recalculated)

| Dept | Line | Row | 2026 N source | 2026 N output | Delta N | 2027 AG source | 2027 AG output | Delta AG |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| FO (SD) | Total Income | 16 | 0 | 0 | 0.00 | 0 | 0 | 0.00 |
| FO (SD) | Total COGS | 63 | 1,967,580 | 1,967,580 | 0.00 | 7,347,500 | 7,347,500 | -0.00 |
| FO (SD) | Gross Profit | 64 | (1,967,580) | (1,967,580) | 0.00 | (7,347,500) | (7,347,500) | 0.00 |
| FO (SD) | Total Expense | 116 | 217,242 | 217,242 | 0.00 | 0 | 0 | 0.00 |
| FO (SD) | Net Income | 132 | (2,184,823) | (2,184,823) | 0.00 | (7,347,500) | (7,347,500) | 0.00 |
| PO (COO) | Total Income | 16 | 7,423,940 | 7,423,940 | 0.00 | 0 | 0 | 0.00 |
| PO (COO) | Total COGS | 63 | 2,361,338 | 2,361,338 | -0.00 | 1,096,896 | 1,096,896 | -0.00 |
| PO (COO) | Gross Profit | 64 | 5,062,601 | 5,062,601 | -0.00 | (1,096,896) | (1,096,896) | 0.00 |
| PO (COO) | Total Expense | 116 | 461,703 | 461,703 | 0.00 | 171,650 | 171,650 | 0.00 |
| PO (COO) | Net Income | 132 | 4,685,709 | 4,685,709 | -0.00 | (1,268,546) | (1,268,546) | 0.00 |
| CO (COO) | Total Income | 16 | 0 | 0 | 0.00 | 0 | 0 | 0.00 |
| CO (COO) | Total COGS | 63 | 8,994 | 8,994 | 0.00 | 0 | 0 | 0.00 |
| CO (COO) | Gross Profit | 64 | (8,994) | (8,994) | 0.00 | 0 | 0 | 0.00 |
| CO (COO) | Total Expense | 116 | 763,946 | 763,946 | 0.00 | 618,961 | 618,961 | 0.00 |
| CO (COO) | Net Income | 132 | (772,940) | (772,940) | 0.00 | (618,961) | (618,961) | -0.00 |
| FE (SD) | Total Income | 16 | 0 | 0 | 0.00 | 0 | 0 | 0.00 |
| FE (SD) | Total COGS | 63 | 115,989 | 115,989 | 0.00 | 388,814 | 388,814 | -0.00 |
| FE (SD) | Gross Profit | 64 | (115,989) | (115,989) | 0.00 | (388,814) | (388,814) | 0.00 |
| FE (SD) | Total Expense | 116 | 1,195,806 | 1,195,806 | 0.00 | 931,334 | 931,334 | -0.00 |
| FE (SD) | Net Income | 132 | (1,311,795) | (1,311,795) | 0.00 | (1,320,148) | (1,320,148) | -0.00 |
| PE (COO) | Total Income | 16 | 0 | 0 | 0.00 | 0 | 0 | 0.00 |
| PE (COO) | Total COGS | 63 | 24,114 | 24,114 | 0.00 | 0 | 0 | 0.00 |
| PE (COO) | Gross Profit | 64 | (24,114) | (24,114) | 0.00 | 0 | 0 | 0.00 |
| PE (COO) | Total Expense | 116 | 1,291,260 | 1,291,260 | 0.00 | 1,296,197 | 1,296,197 | -0.00 |
| PE (COO) | Net Income | 132 | (1,315,374) | (1,315,374) | 0.00 | (1,296,197) | (1,296,197) | 0.00 |

Cell-by-cell fidelity, every non-empty cell (source cached vs output):

| Sheet | Cells | Value mismatches | Max abs numeric diff | New errors | Errors cleared | Error code changed |
|---|---:|---:|---:|---:|---:|---:|
| FO | 3371 | 0 | 0.000500 | 0 | 0 | 0 |
| FE | 3372 | 0 | 0.000139 | 0 | 0 | 0 |
| Fld Maint Budget | 1012 | 0 | 0.000337 | 0 | 0 | 0 |
| Fld Ops Payroll | 1165 | 0 | 0.000400 | 0 | 0 | 0 |
| Fld Eng Budget | 739 | 0 | 0.000139 | 0 | 0 | 0 |
| DeploySum | 808 | 0 | 0.000000 | 0 | 0 | 226 |
| Prod Payroll | 1173 | 0 | 0.000000 | 0 | 0 | 748 |
| PO | 3521 | 0 | 0.000444 | 0 | 0 | 0 |
| CO | 3372 | 0 | 0.000013 | 0 | 0 | 0 |
| PE | 3380 | 0 | 0.000500 | 0 | 0 | 0 |

v1 vs v2 (`diff_versions.py`, formulas and cached values, exact):

| Sheet | Cells | Formula diffs | Value diffs |
|---|---:|---:|---:|
| COO P&L | 3530 | 0 | 0 |
| FO | 3581 | 0 | 0 |
| PO | 3626 | 0 | 0 |
| CO | 3582 | 0 | 0 |
| FE | 3582 | 0 | 0 |
| PE | 3590 | 0 | 0 |
| DeploySum | 808 | 0 | 0 |
| Fld Ops Payroll | 1165 | 0 | 0 |
| Prod Payroll | 1173 | 0 | 0 |
| Fld Maint Budget | 1012 | 0 | 0 |
| Fld Eng Budget | 739 | 0 | 0 |
| **Total** | 26388 | 0 | 0 |

Comments added in v2: 17 (DeploySum!B17, DeploySum!C17, DeploySum!D17, ...); removed 0; changed 0.

FO/FE tabs replaced: COO book values (dropped) vs SD book values (used):

| Dept | Line | Col | COO book (replaced) | SD book (used) | Difference |
|---|---|---|---:|---:|---:|
| FO | Total Income | N | 0 | 0 | 0 |
| FO | Total Income | AG | 0 | 0 | 0 |
| FO | Total COGS | N | 1,967,580 | 1,967,580 | 0 |
| FO | Total COGS | AG | 1,341,298 | 7,347,500 | 6,006,202 |
| FO | Gross Profit | N | (1,967,580) | (1,967,580) | 0 |
| FO | Gross Profit | AG | (1,341,298) | (7,347,500) | (6,006,202) |
| FO | Total Expense | N | 217,242 | 217,242 | 0 |
| FO | Total Expense | AG | 0 | 0 | 0 |
| FO | Net Income | N | (2,184,823) | (2,184,823) | 0 |
| FO | Net Income | AG | (1,341,298) | (7,347,500) | (6,006,202) |
| FE | Total Income | N | 0 | 0 | 0 |
| FE | Total Income | AG | 0 | 0 | 0 |
| FE | Total COGS | N | 115,989 | 115,989 | 0 |
| FE | Total COGS | AG | 0 | 388,814 | 388,814 |
| FE | Gross Profit | N | (115,989) | (115,989) | 0 |
| FE | Gross Profit | AG | 0 | (388,814) | (388,814) |
| FE | Total Expense | N | 1,195,806 | 1,195,806 | 0 |
| FE | Total Expense | AG | 752,002 | 931,334 | 179,332 |
| FE | Net Income | N | (1,311,795) | (1,311,795) | 0 |
| FE | Net Income | AG | (752,002) | (1,320,148) | (568,146) |

## COO P&L before vs after

| Line | Row | Col | Before (COO book cached) | After (output) | Change |
|---|---:|---|---:|---:|---:|
| Total Income | 16 | N | 7,423,940 | 7,423,940 | 0 |
| Total Income | 16 | AG | 0 | 0 | 0 |
| Total COGS | 63 | N | 4,478,016 | 4,478,016 | (0) |
| Total COGS | 63 | AG | 2,438,193 | 8,833,209 | 6,395,016 |
| Gross Profit | 64 | N | 2,945,924 | 2,945,924 | (0) |
| Gross Profit | 64 | AG | (2,438,193) | (8,833,209) | (6,395,016) |
| Total Expense | 116 | N | 3,929,957 | 3,929,957 | 0 |
| Total Expense | 116 | AG | 2,838,810 | 3,018,142 | 179,332 |
| Net Income | 132 | N | (899,222) | (899,222) | (0) |
| Net Income (2027 incomplete) | 132 | AG | (5,277,004) | (11,851,351) | (6,574,348) |

Roll-up integrity: COO P&L = FO+PO+CO+FE+PE on every additive row, B:N and U:AG: 2911 cells, 0 failures, max abs diff 0.000000.

## Error scan

| Sheet | Before (source book cached) | After (output recalculated) |
|---|---|---|
| Collation Notes | n/a (new sheet) | none |
| COO P&L | none | none |
| FO | none | none |
| PO | none | none |
| CO | none | none |
| FE | none | none |
| PE | none | none |
| DeploySum | {'#ERROR!': 226, '#REF!': 237, '#N/A': 35} | {'#REF!': 463, '#N/A': 35} |
| Fld Ops Payroll | none | none |
| Prod Payroll | {'#REF!': 48, '#ERROR!': 748} | {'#REF!': 796} |
| Fld Maint Budget | none | none |
| Fld Eng Budget | none | none |
| Logistics&WH Payroll (SD, not carried) | none | n/a |
| Old Draft (SD, not carried) | none | n/a |
| Fld Maint T&E Data (SD, not carried) | none | n/a |

**#REF! counts rise: DeploySum 237 -> 463, Prod Payroll 48 -> 796.** Why: the SD book is a Google Sheets export whose cached errors include Google's `#ERROR!` (DeploySum 226, Prod Payroll 748), which Excel/LibreOffice do not have. The frozen external cells holding `#ERROR!` were stored as `#REF!`, and LibreOffice's recalculation shows every downstream failed cell as `#REF!`. The rise equals the relabelled `#ERROR!` count (DeploySum 237 + 226 = 463; Prod Payroll 48 + 748 = 796). Total error cells are unchanged (DeploySum 498 -> 498, Prod Payroll 796 -> 796), and no cell that held a value in the source is an error in the output (new errors = 0).

## Issues

Severity per the scale above. 'Basis' shows which rule set the rating.

| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |
|---|---|---|---|---|---|---|---|
| I-01 | HIGH | COO P&L!AG16; PO!R12:S15; PO!U12:AF15 | 2027 revenue is zero. The PO 2027 revenue rows use input method 'Even' with an empty or 0 annual input (S), so U:AF = 0. The 2027 P&L is cost-only, so 2027 Net Income is incomplete. | COO P&L!N16 = 7,423,940, AG16 = 0. PO!R12 = 'Even', PO!S12 = None. PO!N12 6,363,078 -> AG12 0; PO!N15 975,000 -> AG15 0. | not determinable | blocks sign-off | Owner of PO/revenue to enter 2027 revenue (or link the Revenue Roll-up). Do not present 2027 Net Income until fixed. |
| I-02 | HIGH | COO P&L!AG132; FO!AG132; FE!AG132 | Replacing FO and FE with the SD versions moves 2027 COO Net Income by (6,574,348). The SD build is much heavier than the COO book's FO/FE. | COO P&L!AG132 before (5,277,004), after (11,851,351). FO!AG132 COO book (1,341,298) -> SD (7,347,500); FE!AG132 COO book (752,002) -> SD (1,320,148). Drivers: FO!N52 876,692 -> AG52 3,238,031; FO!N47 255,704 -> AG47 1,519,865; FO!N29 57,182 -> AG29 765,000. | (6,574,348) | impact (6,574,348) | COO and SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off. |
| I-03 | HIGH | DeploySum!B4:R42; DeploySum!A3; DeploySum!A45:A49 | DeploySum links to a workbook that was not supplied ([1] = 2026 Exist New, Deploy, Deploy Detail, Expansion, New Sales, Revenue Roll-up). These 427 cells had already failed in the SD book (cached {'#ERROR!': 175, '#REF!': 202, '0': 17, '#N/A': 33}). They were frozen to the SD cached values per orchestrator handoff; this is a declared deviation from brief criterion 1 because the linked workbook was not supplied and the SD file has no externalLink part. So the bookings/deployments/production block and the notes in column A show errors. | 427 formula cells contain '[1]...'; every one is listed with its original formula on the Collation Notes sheet. SD package externalLink parts: 0. DeploySum errors: SD {'#ERROR!': 226, '#REF!': 237, '#N/A': 35}, output {'#REF!': 463, '#N/A': 35}. | not determinable | blocks sign-off | Get the Revenue Roll-up / Deploy Detail workbook; then relink these formulas or paste values so the plan is reproducible. |
| I-04 | HIGH | DeploySum!B53:R66 | The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (and so FO/FE 2027) are typed values, not formulas; the rows that should derive them are broken (I-03), so they cannot be traced to a source. | Rows [53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66] contain no formulas. FY27 totals (typed): DeploySum!R54 'New logos – deployments (#) (incl. 2026 ' = 51; DeploySum!R57 'Expansion – deployments (#)' = 15; DeploySum!R60 'Existing & forecast contracts – deployme' = 1. FO/FE 2027 lines linked to driver tabs total 8,667,647 (18 lines). | exposure 8,667,647 | blocks sign-off | SD owner to confirm rows 53-66 match the current deployment plan and record the source. |
| I-05 | LOW | Prod Payroll!B24:S81 (hidden); Fld Ops Payroll!M5:M7 | The production payroll model does not work: 796 of its 901 formulas are errors in the output (as in the SD book), including every payroll total (row 41 'Total lift payroll': S = #REF!; row 62 'Total tray payroll': S = #REF!; row 79 'Total supervisor payroll': S = #REF!; row 81 'TOTAL PRODUCTION PAYROLL (lifts + trays + supervisors)': S = #REF!). The 105 formulas that evaluate are input helpers, staffing grids and headcount rows (rows 5-7, 9, 17, 22, 29, 33, 35, 45, 50, 54, 56, 66, 69, 73). It feeds no budget value: the only cells read from it are typed rate/timing inputs, not headcount or cost. Its result does not reach PO. | Errors SD {'#REF!': 48, '#ERROR!': 748}, output {'#REF!': 796}. Cells read from it: Fld Ops Payroll!M5 <- Prod Payroll!M5 'Annual raise (% of salary)' (typed input, = 0.03); Fld Ops Payroll!M6 <- Prod Payroll!M6 'Raise effective month' (typed input, = 2027-10-01); Fld Ops Payroll!M7 <- Prod Payroll!M9 'Raise eligibility – min mths employed' (typed input, = 6). PO 5110-5140 (PO!U33:AF35) are typed values (36 typed month cells, 0 links). | 0 | impact 0 | Fix DeploySum first; then decide whether PO production labour should link to Prod Payroll (see I-17). |
| I-06 | LOW | Fld Maint Budget!B30 (comment); Fld Ops Payroll!B11; FO!AG44; FO!AG52 | MeLi contractor double count: quantified at $0 in the current cells. The CONFIRM comment on Fld Maint Budget!B30 says Fld Ops Payroll includes MeLi in '21 all-in techs', but Fld Ops Payroll!B11 = 14 ('Current site techs on payroll (Sep-26) - Domestic Only') and Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11 = 21. So MeLi techs are costed in 5310 only. The comment describes an earlier state and is stale (Fld Maint Budget!A143 records the correction). | FO 5310 (FO!AG44 = 575,268) = MeLi techs in role 346,920 + Merida contractors 123,900 + MeLi supervisor 104,448 (Fld Maint Budget rows 70-72 x B10/B11; row 84 = 575,268). FO 5510 current techs: Fld Ops Payroll!F20:Q20 = 14 each month (formula =$B$11); current-tech payroll 2027 1,094,774. | 0 | impact 0 | SD owner to confirm and delete the stale CONFIRM comment on Fld Maint Budget!B30. |
| I-07 | HIGH | PO!AG19; PO!AG20; PO!AG22; COO P&L!AG19:AG22 | 2027 depreciation is zero, while 2026 carries 1,788,097 (COO P&L rows 19, 20, 21, 22: 5010 - SlipBot Depreciation; 5011 - SlipLift Depreciation; 5012 - SlipCarrier Depreciation; 5020 - Robot Peripherals Depreciation). 2027 Net Income is therefore incomplete. PO was out of scope and is unchanged. | PO!N19 1,492,329 -> AG19 0; PO!N20 100,360 -> AG20 0; PO!N22 158,415 -> AG22 0. | not determinable | blocks sign-off | PO owner / Finance to budget 2027 depreciation from the fixed-asset schedule. |
| I-08 | LOW | PO!U28; PO!Y28; PO!AD28; PO!U38; PO!U42 | Typed plugs are added onto the driver formula in 2027 month cells (+15,000, +5,000). They are not visible in the method columns R:T. | PO!U28 +5,000; PO!Y28 +5,000; PO!AD28 +5,000; PO!U38 +15,000; PO!U42 +15,000. Total plugs 45,000. | 45,000 | impact 45,000 | PO owner to move these amounts into a documented input (column S or a manual row), or remove them. |
| I-09 | LOW | PE!W74:AF74; PE!W76 | Typed numbers overwrite the driver formula in some 2027 months (manual overrides inside a formula row). | PE!W74=1,500, PE!X74=1,500, PE!Y74=2,000, PE!Z74=2,000, PE!AA74=2,500, PE!AB74=2,500, PE!AC74=3,000, PE!AD74=3,000, PE!AE74=3,500, PE!AF74=4,000, PE!W76=300. Total typed 25,800. | 25,800 | impact 25,800 | PE owner to confirm the overrides, or set the row method to Manual. |
| I-10 | MED | FO!AG58; FO!AG67; FO!AG91; FE!AG91; FO!AG116 | FO/FE lines with material 2026 spend have 2027 = 0, and FO Total Expense (SG&A) is 0 for 2027. Fld Maint Budget!A99 says: 'Not budgeted here: 6100 Travel and 7550 Tools ($0 by design – field travel books to 5050/5360, field tools to 5330); new-hire onboarding (covered by the $2K new-hire cost in Fld Ops Payroll B9). Out of scope: 5920, 7200, 8600.' | FO!AG58 5920 - Software - COGS: 2026 119,260 -> 2027 0; FO!AG67 6610 - Salaries and Wages - SG&A: 2026 50,575 -> 2027 0; FO!AG91 7200 - Contractors: 2026 59,734 -> 2027 0; FE!AG91 7200 - Contractors: 2026 154,857 -> 2027 0; FO!N116 217,242 -> AG116 0. 2026 total of these lines 384,425. | not determinable (2026 base 384,425) | impact not determinable; owner confirmation needed | SD owner to confirm whether these costs stop in 2027 or are budgeted elsewhere. |
| I-11 | MED | COO P&L!AG12; COO P&L!AG52; COO P&L!AG19; COO P&L!AG47 (+ variance table) | 98 rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k. | Largest COO P&L GL moves: COO P&L!N12 6,363,078 -> AG12 0; COO P&L!N52 887,966 -> AG52 3,238,031; COO P&L!N19 1,492,329 -> AG19 0; COO P&L!N47 319,694 -> AG47 1,554,365. | not determinable | impact not determinable; owner confirmation needed | Each dept owner to comment on their rows in the variance table. |
| I-12 | MED | Fld Maint Budget!B8; Fld Maint Budget!B78:M78; FO!AG46 | Site setup kit cost is flagged as a placeholder (Fld Maint Budget!D8: 'PLACEHOLDER – update when the kit list is priced (Spare Parts, Tool Kits, 5S for'). It feeds FO 5330. | Fld Maint Budget!B8 = 4,500 $/new site; 'Site setup kits' 2027 (B78:M78) = 274,500. FO!N46 23,121 -> AG46 288,069. | not determinable (exposure 274,500) | impact not determinable; owner confirmation needed | SD owner to price the kit list and replace B8. |
| I-13 | MED | Fld Ops Payroll!M11; Fld Ops Payroll!B12; Fld Ops Payroll!M14 | Two Fld Ops Payroll drivers are marked 'Placeholder' in the author's notes: site techs per floater (M11) and the share of expansion go-lives needing a tech (B12). M11 currently has no effect because the floater switch M14 = 'No' (floater payroll 2027 = 0). B12 drives expansion-tech payroll. | M11 = 40, B12 = 0.6, M14 = 'No'. Expansion tech payroll 2027 (Fld Ops Payroll!F47:Q47) = 337,514. | not determinable (exposure 337,514) | impact not determinable; owner confirmation needed | SD owner to confirm or replace B12; M11 matters only if M14 is set to Yes. |
| I-14 | MED | Prod Payroll!M7; Prod Payroll!B9; Prod Payroll!A33; Fld Ops Payroll!B9; Old Draft!B142 (SD, not carried) | More placeholder inputs: Prod Payroll new-hire cost, current headcount and absence factors (no budget effect while Prod Payroll is broken), and the Fld Ops Payroll new-hire cost per tech, which hidden Old Draft!B142 says overlaps an onboarding line. | Fld Ops Payroll!B9 = 2,000; new-hire cost in FO 2027 (Fld Ops Payroll rows 34, 46, 59, 72, F:Q) = 138,000. Old Draft!B142: '7. Onboarding: 10 new hires Jan – Sep. The $2,000 Fld Ops Payroll placeholder (B9) overlaps this line; replace it with the actual cost here '. | not determinable (exposure 138,000) | impact not determinable; owner confirmation needed | SD owner to confirm B9 (and that onboarding is not also budgeted elsewhere). |
| I-15 | LOW | Fld Maint Budget!B12 (comment); Fld Maint Budget!B11; Fld Ops Payroll!H11; Fld Ops Payroll!E12 | The CONFIRM comment on Fld Maint Budget!B12 says Fld Ops Payroll shows 0 current supervisors; it now shows H11 = 1 ('Current supervisors counted toward ratio (Sep-26) – Isaiah'), and E12 says 'Ratio = domestic techs only. MeLi contract supervisor budgeted in Fld Maint Budget B11.'. The MeLi contract supervisor (5310) and the domestic manager (5510) are different people, so there is no double count; the comment is stale. | MeLi supervisor in 5310 2027 = 104,448 (Fld Maint Budget!B11 = 8,704/month x B12 = 1). Isaiah (Fld Ops Payroll row 77) 2027 = 120,900; incremental supervisors (row 73) 2027 = 193,632. | 0 | impact 0 | SD owner to confirm and delete the stale comment. |
| I-16 | LOW | Fld Maint T&E Data!M5:M388 (SD, hidden, not carried) | 101 T&E transactions are flagged 'Reclass needed' = Yes, totalling $27,804.02; booked GL differs from budget GL. 2 are tagged 'AI suggested' and 17 have tag basis 'Assumed'. If FO 2026 actuals were pulled on booked GL, these sit on the wrong 2026 lines; totals are unaffected, and no formula in the output reads this sheet. | Top booked->budget GL pairs: 5050->5360 x34, 6100->5360 x16, 5360->5050 x14, 7550->5330 x12, 6100->5050 x8. | 27,804 | impact 27,804 | Finance to post the reclasses (or confirm none are needed). |
| I-17 | HIGH | Logistics&WH Payroll!S51 (SD, not carried); PO!AG33:AG36 | The SD Logistics & Warehouse payroll model ('Warehouse and logistics team payroll that rolls up to Production Operations, sized from th...') totals 547,441 for 2027 but is referenced by 0 formulas in either book. PO 2027 production labour (rows 33-35) is typed with no link, so the workbook cannot show whether warehouse payroll is inside it. If it is not, PO 2027 is understated by up to 547,441. | Logistics&WH Payroll 2027 (F51:Q51) = 547,441: Base salaries 440,293; Payroll taxes 29,940; Benefits 72,208; New-hire cost 5,000; Dec-27 headcount 9. PO 2027: 5110 - Salaries and Wages - Production 525,310; 5130 - Payroll Taxes - Production 19,105; 5140 - Benefits - Production 108,404; Total - 5100 - Labor Expense - Production 652,820. Logistics&WH 2027 = 84% of PO 5100 total and 104% of PO 5110 salaries. PO 5350 Warehouse AG48 = 0; FO 5350 AG48 = 36,000 (Fld Maint Budget warehouse rent line). | up to 547,441 | impact 547,441 | PO owner to confirm whether PO 5110-5140 include the warehouse team. If not, link PO to this model (it would then need to be carried into the workbook). |
| I-18 | LOW | Fld Ops Payroll!B10; Fld Ops Payroll!B15; Fld Ops Payroll!B16 | The hiring horizon ends at Dec-27 (DeploySum row 54). Hires for Jan-28 go-lives use an Oct-Dec 27 average default rather than a forecast (documented by the author). | B10 = 1; B15 = =ROUND(AVERAGE(DeploySum!O54:Q54),0) = 7; B16 = =ROUND(AVERAGE(DeploySum!O57:Q57),0) = 2; cell notes on B10/B15/B16. | not determinable | hygiene | Overwrite B15/B16 if a 2028 go-live forecast exists. |
| I-19 | LOW | FE!U30:AF75 (rows 30-31, 67-69, 74-75); Fld Eng Budget rows 28-33, 85-91 | FE and Fld Eng Budget link in both directions: Fld Eng Budget reads FE 2026 columns, and FE 2027 rows read Fld Eng Budget. LibreOffice recalculated with no errors (no cell-level circularity), but the structure is easy to break. | Fld Eng Budget has 68 references to FE; FE has 84 references to Fld Eng Budget. | not determinable | hygiene | Check Fld Eng Budget before editing the FE 2026 columns it reads. |
| I-20 | LOW | SD sheets Prod Payroll, Old Draft, Fld Maint T&E Data (hidden); DeploySum!A30:A42 (hidden rows 30, 32-36, 40-42) | SD has 3 hidden sheets; Prod Payroll is carried and kept hidden, the others are not carried (FO/FE do not depend on them). DeploySum hidden rows are preserved. | Hidden in SD: ['Prod Payroll', 'Old Draft', 'Fld Maint T&E Data']; hidden in output: ['Prod Payroll']; DeploySum hidden rows: 30, 32-36, 40-42. | not determinable | hygiene | None, unless reviewers want Old Draft / T&E Data in the pack. |
| I-21 | LOW | Fld Maint T&E Data!Q26 (SD) | Old Draft dependence is contained: 1 cell(s) outside Old Draft read it, none in the FO/FE chain, so the output has 0 references to it. | SD Fld Maint T&E Data: 1 cell(s) e.g. Q26: ='Old Draft'!B28*'Old Draft'!B23. SD dependency map: Old Draft -> {'Fld Maint T&E Data': 458, 'Fld Ops Payroll': 131, 'DeploySum': 112}. | not determinable | hygiene | None for the budget. Consider deleting Old Draft once the reference is re-pointed. |
| I-22 | LOW | COO P&L!A23:A24, B27, B37 (same rows on FO, PO, CO, FE, PE) | Rows 23 and 24 carry the same label ('5025 - Freight and Delivery - Production (Summary)'). Row 23 is an empty header; row 24 holds postings inside row 27 (=SUM(B24:B26)). Row 37 (=B19+B22+B27+B28+B29+B30+B31+B36+B20+B21) covers every direct child of its section, so nothing is skipped today, but anything typed on row 23 would be left out. | Subtotal scan on 6 sheets: 0 skipped lines with values. Non-empty cells on row 23 by tab: {COO P&L: 0, FO: 0, PO: 0, CO: 0, FE: 0, PE: 0}. COO P&L dept-sum formulas omitting a dept: 0. | not determinable | hygiene | Optionally relabel row 23 as a header, or lock it. |
| I-23 | LOW | COO P&L!B65:M65; COO P&L!C141 | COO P&L row 65 (labelled 'Expense') holds an unlabelled gross-margin % formula (=IFERROR(B64/B16,"")); blank for 2027 because revenue is 0. Row 141 shows an extreme ratio for Feb-26 caused by negative 2026 payroll postings. | COO P&L!C141 = -14.33 (ratio). PO!N67 (308,059) -> AG67 0; PE!N35 (56,264) -> AG35 0. | not determinable | hygiene | Label row 65. Finance to explain the negative 2026 payroll postings in PO 6610 and PE 5140. |
| I-24 | LOW | Workbook defined names (xl/workbook.xml <definedNames>, workbook scope, no cell); list in 02-build_pruned_names_v2.csv | The COO book carries 14,310 legacy defined names from an old template. None is used by any formula, data validation, conditional format, chart or other name. v2 pruned the 5,345 unused names whose target is #REF! (5,330) or external-looking (15); 8,965 remain (string/array constants and plain values). | Before 14,310, after 8,965. Usage scan covered cell formulas, data validations, conditional formats, charts, print areas/titles and other names (counts in the notes file). Names referenced: 0 from parts, 0 from other names. Pruned names still referenced: 0. | not determinable | hygiene | Optional: purge the remaining constant-valued legacy names in Name Manager. |
| I-25 | LOW | DeploySum!A3:R49; Prod Payroll!B24:S81 | Side effects of moving from Google Sheets to xlsx: threaded comments become plain notes (text kept); Google's '#ERROR!' has no Excel equivalent, so it shows as #REF! (frozen external cells are stored as #REF!, and LibreOffice recalculation turns the downstream Google #ERROR! cells into #REF!); LibreOffice saves error constants as '=#REF!' formulas. | Error-code changes on cells that were already errors: DeploySum 226, Prod Payroll 748. Total error cells unchanged: DeploySum 498 -> 498, Prod Payroll 796 -> 796. New errors: 0. | not determinable | hygiene | None; disclosed for reviewers. |
| I-26 | MED | Fld Eng Budget!B21; Fld Eng Budget!B67:M67; FE!AG67 | 'Head of Service Delivery – Rasheen Henry' has no salary entered, so FE 6610 carries $0 for this current employee. The source note says: 'Source: user-provided. Current employee, in seat now. Enter annual salary in B21'. | Fld Eng Budget!B21 = None; row 67 2027 = 0; FE!AG67 = 713,347 excludes it. | not determinable (salary not in workbook) | impact not determinable; owner confirmation needed | SD owner to enter the salary in Fld Eng Budget!B21 (or confirm it is budgeted in another dept). |
| I-27 | LOW | Logistics&WH Payroll!B56 (SD, not carried); FO!U52:AF52 | Logistics&WH Payroll excludes MH-05 ('Less: MH-05 Material Handler, logistics support (counted on the FO tab)'), but FO 5510 2027 (FO!U52) sums only Fld Ops Payroll rows 21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77, none of which is an MH-05 seat; 'MH-05' appears nowhere outside Logistics&WH Payroll. So this seat is in neither model. | Logistics&WH Payroll!B56 = -38,133 (deduction of MH-05's 2027 base pay, before burden). FO!U52 = ='Fld Ops Payroll'!F21+'Fld Ops Payroll'!F31+'Fld Ops Payroll'!F43+'Fld Ops Payroll'!F56+'Fld Ops Payroll'!F69+'Fld Ops Payroll'!F76+'Fld Ops Payroll'!F77+'Fld Ops Payroll'!F34+'Fld Ops Payroll'!F46+'Fld Ops Payroll'!F59+'Fld Ops Payroll'!F72. MH-05 mentions elsewhere: none. | 38,133 base pay missing (before burden) | impact 38,133 | SD/PO owners to decide where MH-05 is budgeted and add it. |
| I-28 | MED | CO!AG67:AG69; PE!AG67:AG69; FE!AG67:AG69; Fld Eng Budget!A13:A21 | SG&A payroll (6610/6630/6640) is non-zero on CO, FE and PE. FE is built from a named roster on Fld Eng Budget; CO and PE are typed monthly amounts with no roster, so the workbook cannot confirm that no person on the FE roster is also inside CO or PE. | row 67: CO 528,452, FE 713,347, PE 1,078,020; row 68: CO 27,593, FE 48,508, PE 38,501; row 69: CO 62,916, FE 116,989, PE 95,116. 2027 months typed (no formula): CO yes, PE yes, FE no (formulas). FE roster: Fld Eng Budget!A13:A21. | not determinable (no CO/PE roster) | impact not determinable; owner confirmation needed | CO and PE owners to confirm their SG&A payroll rosters exclude the people on Fld Eng Budget!A13:A21. |
| I-29 | LOW | Prod Payroll!M9; Fld Ops Payroll!M7; Fld Eng Budget!B59 (row formula); PO!AD33; PO!AD34; PO!AD35; CO!AD67; CO!AD68; CO!AD69; PE!AD67; PE!AD68; PE!AD69 | Raise timing is consistent (same % and month everywhere), but the eligibility rule is not: Fld Ops Payroll and Logistics&WH Payroll exclude staff hired in the months before the raise (Prod Payroll!M9), while Fld Eng Budget and the typed PO/CO/PE payroll rows apply the raise to the whole row. | Prod Payroll!M5 = 0.03, M6 = 2027-10-01, M9 = 6. Steps found in typed rows: PO!AD33 3.00%; PO!AD34 3.00%; PO!AD35 3.00%; CO!AD67 3.00%; CO!AD68 3.00%; CO!AD69 3.00%; PE!AD67 3.00%; PE!AD68 3.00%; PE!AD69 3.00%; FE!AD67 3.00%; FE!AD68 3.00%; FE!AD69 3.00%. | not determinable | hygiene | Payroll owners to confirm whether the eligibility rule should apply to all departments. |

### Scan coverage (including clean results)

- 2026 (B:N) FO/FE differences between the books, rows 9-141: **0 cells differ**. Formula differences FO/FE (A:AJ, rows 1-200): FO 132, FE 84, in columns U:AF only (the 2027 months); rows FO 29-30, 44-49, 52-54, FE 30-31, 67-69, 74-75.
- External links: I-03 (DeploySum only; package scan above).
- Numeric literals / overrides inside formula rows: 7 hits (I-08, I-09). Constants in total/roll-up cells: 0.
- Placeholder keywords (values and notes, all sheets of both books): 43 hits, by keyword {'PLACEHOLDER': 12, 'ASSUMED': 26, 'AI SUGGESTED': 5}; 'TBD': 0. In the hidden T&E sheet: 30 (I-16).
- Variance (>50% and >$50k): 98 rows, listed below.
- COO P&L dept-sum formulas omitting a dept or misaligned: 0. Leaf rows not linked while depts hold values: 0.
- Subtotal formulas skipping lines with values: 0. Header rows carrying values: COO P&L row 65 (I-23). Gross Profit / Net Ordinary Income / Net Other Income / Net Income formula deviations: 0.
- YoY column AJ: 0 cost rows using AG-N; 0 non-standard formulas.
- Cross-department overlap: section above. Raise timing: section above.

### Variance scan: rows with |AG-N| > $50k and > 50% (output values)

| Sheet | Row | Line | 2026 N | 2027 AG | Change | % |
|---|---:|---|---:|---:|---:|---:|
| FO | 29 | 5040 - Freight & Delivery - Deployment | 57,182 | 765,000 | 707,818 | 1238% |
| FO | 37 | Total - 5000 - Robot Production and Deployment | 67,529 | 811,354 | 743,825 | 1101% |
| FO | 44 | 5310 - Contractors - Field | 231,822 | 575,268 | 343,446 | 148% |
| FO | 46 | 5330 - Maintenance Tools and Supplies | 23,121 | 288,069 | 264,949 | 1146% |
| FO | 47 | 5340 - Spare Parts | 255,704 | 1,519,865 | 1,264,161 | 494% |
| FO | 52 | 5510 - :Salaries and Wages - Field Operations | 876,692 | 3,238,031 | 2,361,340 | 269% |
| FO | 53 | 5530 - :Payroll Taxes - Field Operations | 60,890 | 210,802 | 149,912 | 246% |
| FO | 54 | 5540 - :Benefits - Field Operations | 177,696 | 508,405 | 330,709 | 186% |
| FO | 55 | Total - 5500 - Labor Expense - Field Operations | 1,115,278 | 3,957,239 | 2,841,961 | 255% |
| FO | 56 | Total - 5300 - Maintenance | 1,779,235 | 6,536,146 | 4,756,910 | 267% |
| FO | 58 | 5920 - Software - COGS | 119,260 | 0 | (119,260) | -100% |
| FO | 61 | Total - 5900 - Other COGS | 121,168 | 0 | (121,168) | -100% |
| FO | 63 | Total - Cost Of Sales | 1,967,580 | 7,347,500 | 5,379,919 | 273% |
| FO | 64 | Gross Profit | (1,967,580) | (7,347,500) | (5,379,919) | -273% |
| FO | 67 | 6610 - Salaries and Wages - SG&A | 50,575 | 0 | (50,575) | -100% |
| FO | 73 | Total - 6000 - Labor Expense - SG&A | 53,891 | 0 | (53,891) | -100% |
| FO | 91 | 7200 - Contractors | 59,734 | 0 | (59,734) | -100% |
| FO | 116 | Total - Expense | 217,242 | 0 | (217,242) | -100% |
| FO | 117 | Net Ordinary Income | (2,184,823) | (7,347,500) | (5,162,677) | -236% |
| FO | 132 | Net Income | (2,184,823) | (7,347,500) | (5,162,677) | -236% |
| FO | 137 | Salaries and Wages | 927,266 | 3,238,031 | 2,310,765 | 249% |
| FO | 139 | Payroll Taxes | 63,979 | 210,802 | 146,823 | 229% |
| FO | 140 | Benefits | 177,923 | 508,405 | 330,482 | 186% |
| PO | 12 | 4100 - Subscription/Platform Fees | 6,363,078 | 0 | (6,363,078) | -100% |
| PO | 13 | 4500 - Implementation Fees | 85,861 | 0 | (85,861) | -100% |
| PO | 14 | Total - 4000 - Sales | 6,448,940 | 0 | (6,448,940) | -100% |
| PO | 15 | 4900 - One-Time Revenue | 975,000 | 0 | (975,000) | -100% |
| PO | 16 | Total - Income | 7,423,940 | 0 | (7,423,940) | -100% |
| PO | 19 | 5010 - SlipBot Depreciation | 1,492,329 | 0 | (1,492,329) | -100% |
| PO | 20 | 5011 - SlipLift Depreciation | 100,360 | 0 | (100,360) | -100% |
| PO | 22 | 5020 - Robot Peripherals Depreciation | 158,415 | 0 | (158,415) | -100% |
| PO | 27 | Total - 5025 - Freight and Delivery - Production (Summary) | 57,197 | 0 | (57,197) | -100% |
| PO | 33 | 5110 - Salaries and Wages - Production | 137,080 | 525,310 | 388,230 | 283% |
| PO | 35 | 5140 - Benefits - Production | 54,271 | 108,404 | 54,133 | 100% |
| PO | 36 | Total - 5100 - Labor Expense - Production | 197,323 | 652,820 | 455,497 | 231% |
| PO | 37 | Total - 5000 - Robot Production and Deployment | 2,111,917 | 740,674 | (1,371,243) | -65% |
| PO | 38 | 5015 - Supplies and Materials | 2,839 | 101,250 | 98,411 | 3467% |
| PO | 42 | 5201 - Inventory Adjustments | 22,000 | 75,000 | 53,000 | 241% |
| PO | 63 | Total - Cost Of Sales | 2,361,338 | 1,096,896 | (1,264,443) | -54% |
| PO | 64 | Gross Profit | 5,062,601 | (1,096,896) | (6,159,497) | -122% |
| PO | 67 | 6610 - Salaries and Wages - SG&A | (308,059) | 0 | 308,059 | 100% |
| PO | 73 | Total - 6000 - Labor Expense - SG&A | (309,871) | 0 | 309,871 | 100% |
| PO | 98 | 7700 - Inventory Obsolescence-old | 636,000 | 0 | (636,000) | -100% |
| PO | 116 | Total - Expense | 461,703 | 171,650 | (290,053) | -63% |
| PO | 117 | Net Ordinary Income | 4,600,898 | (1,268,546) | (5,869,444) | -128% |
| PO | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| PO | 132 | Net Income | 4,685,709 | (1,268,546) | (5,954,255) | -127% |
| PO | 137 | Salaries and Wages | (159,704) | 525,310 | 685,014 | 429% |
| PO | 140 | Benefits | 51,491 | 108,404 | 56,914 | 111% |
| FE | 30 | 5050 - Travel - Deployment | 87,455 | 346,633 | 259,178 | 296% |
| FE | 37 | Total - 5000 - Robot Production and Deployment | 99,214 | 388,814 | 289,600 | 292% |
| FE | 63 | Total - Cost Of Sales | 115,989 | 388,814 | 272,825 | 235% |
| FE | 64 | Gross Profit | (115,989) | (388,814) | (272,825) | -235% |
| FE | 91 | 7200 - Contractors | 154,857 | 0 | (154,857) | -100% |
| PE | 33 | 5110 - Salaries and Wages - Production | 65,377 | 0 | (65,377) | -100% |
| PE | 35 | 5140 - Benefits - Production | (56,264) | 0 | 56,264 | 100% |
| COO P&L | 12 | 4100 - Subscription/Platform Fees | 6,363,078 | 0 | (6,363,078) | -100% |
| COO P&L | 13 | 4500 - Implementation Fees | 85,861 | 0 | (85,861) | -100% |
| COO P&L | 14 | Total - 4000 - Sales | 6,448,940 | 0 | (6,448,940) | -100% |
| COO P&L | 15 | 4900 - One-Time Revenue | 975,000 | 0 | (975,000) | -100% |
| COO P&L | 16 | Total - Income | 7,423,940 | 0 | (7,423,940) | -100% |
| COO P&L | 19 | 5010 - SlipBot Depreciation | 1,492,329 | 0 | (1,492,329) | -100% |
| COO P&L | 20 | 5011 - SlipLift Depreciation | 100,360 | 0 | (100,360) | -100% |
| COO P&L | 22 | 5020 - Robot Peripherals Depreciation | 158,415 | 0 | (158,415) | -100% |
| COO P&L | 24 | 5025 - Freight and Delivery - Production (Summary) | 50,108 | 0 | (50,108) | -100% |
| COO P&L | 27 | Total - 5025 - Freight and Delivery - Production (Summary) | 62,008 | 0 | (62,008) | -100% |
| COO P&L | 29 | 5040 - Freight & Delivery - Deployment | 85,214 | 765,000 | 679,786 | 798% |
| COO P&L | 30 | 5050 - Travel - Deployment | 94,810 | 392,987 | 298,177 | 314% |
| COO P&L | 33 | 5110 - Salaries and Wages - Production | 202,457 | 525,310 | 322,853 | 159% |
| COO P&L | 35 | 5140 - Benefits - Production | (1,993) | 108,404 | 110,397 | 5540% |
| COO P&L | 36 | Total - 5100 - Labor Expense - Production | 208,574 | 652,820 | 444,246 | 213% |
| COO P&L | 38 | 5015 - Supplies and Materials | 2,486 | 101,250 | 98,764 | 3972% |
| COO P&L | 42 | 5201 - Inventory Adjustments | 22,000 | 75,000 | 53,000 | 241% |
| COO P&L | 44 | 5310 - Contractors - Field | 231,822 | 575,268 | 343,446 | 148% |
| COO P&L | 46 | 5330 - Maintenance Tools and Supplies | 38,155 | 288,069 | 249,914 | 655% |
| COO P&L | 47 | 5340 - Spare Parts | 319,694 | 1,554,365 | 1,234,670 | 386% |
| COO P&L | 52 | 5510 - :Salaries and Wages - Field Operations | 887,966 | 3,238,031 | 2,350,065 | 265% |
| COO P&L | 53 | 5530 - :Payroll Taxes - Field Operations | 60,890 | 210,802 | 149,912 | 246% |
| COO P&L | 54 | 5540 - :Benefits - Field Operations | 178,344 | 508,405 | 330,062 | 185% |
| COO P&L | 55 | Total - 5500 - Labor Expense - Field Operations | 1,127,200 | 3,957,239 | 2,830,039 | 251% |
| COO P&L | 56 | Total - 5300 - Maintenance | 1,877,141 | 6,570,646 | 4,693,505 | 250% |
| COO P&L | 58 | 5920 - Software - COGS | 120,529 | 0 | (120,529) | -100% |
| COO P&L | 61 | Total - 5900 - Other COGS | 123,466 | 500 | (122,966) | -100% |
| COO P&L | 63 | Total - Cost Of Sales | 4,478,016 | 8,833,209 | 4,355,193 | 97% |
| COO P&L | 64 | Gross Profit | 2,945,924 | (8,833,209) | (11,779,133) | -400% |
| COO P&L | 91 | 7200 - Contractors | 214,591 | 0 | (214,591) | -100% |
| COO P&L | 98 | 7700 - Inventory Obsolescence-old | 636,000 | 0 | (636,000) | -100% |
| COO P&L | 106 | 8600 - Repairs and Maintenance | 51,212 | 0 | (51,212) | -100% |
| COO P&L | 117 | Net Ordinary Income | (984,033) | (11,851,351) | (10,867,318) | -1104% |
| COO P&L | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| COO P&L | 132 | Net Income | (899,222) | (11,851,351) | (10,952,129) | -1218% |
| COO P&L | 137 | Salaries and Wages | 3,264,812 | 6,083,161 | 2,818,348 | 86% |
| COO P&L | 139 | Payroll Taxes | 210,079 | 344,509 | 134,430 | 64% |
| COO P&L | 140 | Benefits | 471,094 | 891,831 | 420,737 | 89% |

### T&E rows with 'Reclass needed' = Yes (SD `Fld Maint T&E Data`, hidden)

101 rows, $27,804.02. Rows: 8, 9, 10, 15, 17, 20, 21, 22, 24, 25, 27, 29, 32, 33, 34, 35, 37, 39, 41, 43, 46, 47, 48, 50, 51, 52, 53, 54, 55, 56, 58, 62, 63, 66, 74, 75, 76, 79, 89, 90, 98, 104, 107, 108, 110, 111, 112, 116, 119, 120, 121, 123, 134, 139, 140, 160, 166, 167, 168, 169, 171, 172, 174, 177, 190, 191, 197, 198, 199, 201, 203, 204, 206, 224, 229, 230, 231, 232, 233, 234, 235, 236, 237, 259, 261, 269, 270, 271, 275, 289, 293, 294, 295, 296, 297, 298, 299, 303, 305, 308, 343.

| Booked GL -> Budget GL | Rows |
|---|---:|
| 5050 -> 5360 | 34 |
| 6100 -> 5360 | 16 |
| 5360 -> 5050 | 14 |
| 7550 -> 5330 | 12 |
| 6100 -> 5050 | 8 |
| 5060 -> 5370 | 7 |
| 5330 -> 5320 | 4 |
| 5025 -> 5360 | 2 |
| 8300 -> 5320 | 1 |
| 5320 -> 5050 | 1 |
| 5370 -> 5060 | 1 |
| 6110 -> 5060 | 1 |

### Appendix: external-reference cells (DeploySum), frozen to SD cached values

Full per-cell list with original formulas: `Collation Notes` sheet. Frozen non-error cells (DeploySum!B17, DeploySum!C17, DeploySum!D17, DeploySum!E17, DeploySum!F17, DeploySum!G17, DeploySum!H17, DeploySum!I17, DeploySum!J17, DeploySum!K17, DeploySum!L17, DeploySum!M17, DeploySum!N17, DeploySum!O17, DeploySum!P17, DeploySum!Q17, DeploySum!R17) carry the comment 'stale external-link value – not real data'; their only dependents (17 cells) evaluate to {'#REF!': 17}, so the zeros feed no budget value.

| Row | Cells | SD cached values | Example original formula |
|---:|---|---|---|
| 3 | A3 | {'#ERROR!': 1} | `="Tie-out to Deploy Detail (bookings $, deployments, production): "&IF(AND(SUMPRODUCT(ABS(B18:Q18-'[1]Deploy D` |
| 4 | B4, C4, D4, E4, F4, G4, H4, I4, J4, K4, L4, M4, N4, O4, P4, Q4 | {'#REF!': 16} | `='[1]Revenue Roll-up'!D17` |
| 6 | B6, C6, D6, E6, F6, G6, H6, I6, J6, K6, L6, M6, N6, O6, P6, Q6, R6 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D51` |
| 7 | B7, C7, D7, E7, F7, G7, H7, I7, J7, K7, L7, M7, N7, O7, P7, Q7, R7 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D50` |
| 8 | B8, C8, D8, E8, F8, G8, H8, I8, J8, K8, L8, M8, N8, O8, P8, Q8, R8 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D65` |
| 9 | B9, C9, D9, E9, F9, G9, H9, I9, J9, K9, L9, M9, N9, O9, P9, Q9, R9 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D64` |
| 10 | B10, C10, D10, E10, F10, G10, H10, I10, J10, K10, L10, M10, N10, O10, P10, Q10 | {'#REF!': 16} | `=COUNTIF('[1]Deploy Detail'!K21:K62,">0")` |
| 11 | B11, C11, D11, E11, F11, G11, H11, I11, J11, K11, L11, M11, N11, O11, P11, Q11, R11 | {'#REF!': 17} | `='[1]Deploy Detail'!K63` |
| 16 | B16, C16, D16, E16, F16, G16, H16, I16, J16, K16, L16, M16, N16, O16, P16, Q16, R16 | {'#ERROR!': 17} | `=COUNTIFS('[1]2026 Exist New'!$U$9:$U$50,"Yes",'[1]2026 Exist New'!$E$9:$E$50,"SlipLift",'[1]2026 Exist New'!$` |
| 17 | B17, C17, D17, E17, F17, G17, H17, I17, J17, K17, L17, M17, N17, O17, P17, Q17, R17 | {'0': 17} | `=COUNTIFS('[1]2026 Exist New'!$U$9:$U$50,"Yes",'[1]2026 Exist New'!$E$9:$E$50,"SlipBot",'[1]2026 Exist New'!$I` |
| 19 | B19, C19, D19, E19, F19, G19, H19, I19, J19, K19, L19, M19, N19, O19, P19, Q19, R19 | {'#ERROR!': 17} | `=[1]Deploy!D47` |
| 20 | B20, C20, D20, E20, F20, G20, H20, I20, J20, K20, L20, M20, N20, O20, P20, Q20, R20 | {'#ERROR!': 17} | `=[1]Deploy!D48` |
| 21 | B21, C21, D21, E21, F21, G21, H21, I21, J21, K21, L21, M21, N21, O21, P21, Q21, R21 | {'#ERROR!': 17} | `=[1]Deploy!D49` |
| 24 | B24, C24, D24, E24, F24, G24, H24, I24, J24, K24, L24, M24, N24, O24, P24, Q24, R24 | {'#ERROR!': 17} | `=[1]Deploy!D53` |
| 25 | B25, C25, D25, E25, F25, G25, H25, I25, J25, K25, L25, M25, N25, O25, P25, Q25, R25 | {'#ERROR!': 17} | `=[1]Deploy!D54` |
| 26 | B26, C26, D26, E26, F26, G26, H26, I26, J26, K26, L26, M26, N26, O26, P26, Q26, R26 | {'#ERROR!': 17} | `=[1]Deploy!D55` |
| 29 | B29, C29, D29, E29, F29, G29, H29, I29, J29, K29, L29, M29, N29, O29, P29, Q29, R29 | {'#ERROR!': 17} | `=[1]Deploy!D68` |
| 30 | B30, C30, D30, E30, F30, G30, H30, I30, J30, K30, L30, M30, N30, O30, P30, Q30, R30 | {'#ERROR!': 17} | `=[1]Deploy!D69` |
| 33 | B33, C33, D33, E33, F33, G33, H33, I33, J33, K33, L33, M33, N33, O33, P33, Q33 | {'#N/A': 16} | `=SUMIFS('[1]Deploy Detail'!$G$225:$G$236,'[1]Deploy Detail'!$E$225:$E$236,B$4,'[1]Deploy Detail'!$D$225:$D$236` |
| 34 | B34, C34, D34, E34, F34, G34, H34, I34, J34, K34, L34, M34, N34, O34, P34, Q34 | {'#N/A': 16} | `=SUMIFS('[1]Deploy Detail'!$H$225:$H$236,'[1]Deploy Detail'!$E$225:$E$236,B$4,'[1]Deploy Detail'!$D$225:$D$236` |
| 35 | B35, C35, D35, E35, F35, G35, H35, I35, J35, K35, L35, M35, N35, O35, P35, Q35, R35 | {'#ERROR!': 17} | `=B33*([1]Deploy!$B$7+[1]Deploy!$B$14)+B34*[1]Deploy!$B$8` |
| 38 | B38, C38, D38, E38, F38, G38, H38, I38, J38, K38, L38, M38, N38, O38, P38, Q38, R38 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D24` |
| 39 | B39, C39, D39, E39, F39, G39, H39, I39, J39, K39, L39, M39, N39, O39, P39, Q39, R39 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D30` |
| 40 | B40, C40, D40, E40, F40, G40, H40, I40, J40, K40, L40, M40, N40, O40, P40, Q40, R40 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D38` |
| 41 | B41, C41, D41, E41, F41, G41, H41, I41, J41, K41, L41, M41, N41, O41, P41, Q41, R41 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D40` |
| 42 | B42, C42, D42, E42, F42, G42, H42, I42, J42, K42, L42, M42, N42, O42, P42, Q42, R42 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D45` |
| 45 | A45 | {'#ERROR!': 1} | `="1. Timing: bookings go live "&'[1]Deploy Detail'!B8&" months after booking (new logos & expansion); units ar` |
| 46 | A46 | {'#ERROR!': 1} | `="2. Deal size: new-logo deal = "&[1]Deploy!B18&" SlipLifts + "&[1]Deploy!B19&" SlipTrays ("&TEXT('[1]New Sale` |
| 47 | A47 | {'#ERROR!': 1} | `="3. Unit cost (CapEx): SlipLift "&TEXT([1]Deploy!B7,"$#,##0")&" + "&TEXT([1]Deploy!B14,"$#,##0")&" peripheral` |
| 48 | A48 | {'#ERROR!': 1} | `="4. SlipBots: "&IF([1]Deploy!B17="Y","none are built – returned/existing bots are redeployed (incl. the Meli ` |
| 49 | A49 | {'#N/A': 1} | `="5. Sep–Dec 26 bookings include unsigned forecast of "&TEXT(SUMIFS('[1]2026 Exist New'!$P$9:$P$50,'[1]2026 Ex` |

## Decisions

- D1: Carried only the dependency closure of FO/FE (5 supporting tabs).
- D2: External `[1]` formulas were frozen to SD cached values per orchestrator handoff - a declared deviation from brief criterion 1 (linked workbook not supplied; SD file has no externalLink part). Google `#ERROR!` stored as `#REF!`, so downstream IFERROR fallbacks match the SD cached results.
- D3 (v2): Pruned unused defined names whose target contains '[' / '.xls' / '#REF!' (rule from the v2 handoff); kept the 8,965 constant-valued names because the rule does not cover them.
- D4: No number changed or 'fixed' (plugs, placeholders, zero revenue, zero depreciation, missing salary are flagged only). v1 vs v2 diff = 0 on every budget and driver sheet.
- D5: Delivered xlsx is the LibreOffice-recalculated file.
- D6: Match tolerance $0.01 per cell; roll-up tolerance $1 per the brief; v1-vs-v2 comparison exact.
- D7 (v2): Severity is computed from the stated scale with the tie-break rule above; each issue shows its basis.
- D8 (v2): Overlap classification uses the driver cells and the source authors' notes quoted in the table. 'Unclear' is used where the workbook has no roster or driver to compare; no amounts were estimated.
- D9 (v2): v2 entry point is `run_build_v2.sh`; `run_build.sh` reproduces v1 via the frozen `report_v1.py`.

## Not done / limits

- External workbook `[1]` unavailable: DeploySum rows with external links and Prod Payroll cannot be refreshed (accepted BLOCKER).
- Not opened in Microsoft Excel; validated with LibreOffice 24.2.7.2 420(Build:2) and by XML inspection of the package only.
- Page setup / print settings of the copied SD sheets were not copied (build copies cells, styles, dimensions, views, validations and formats only): FO orientation landscape -> portrait; FE orientation landscape -> portrait; Fld Ops Payroll orientation landscape -> portrait; DeploySum orientation landscape -> portrait, fit-to-page lost; Prod Payroll orientation landscape -> portrait. Print areas / print titles: none in the sources (`_xlnm` names in output: 0).
- Sheet-scoped defined names were not copied: SD has _xlnm._FilterDatabase@Fld Maint T&E Data (on sheet(s) not carried: Fld Maint T&E Data); COO book sheet-scoped names: none.
- Google-specific package parts are not kept (part folders in the inputs but not in the output: documenttasks, persons, threadedComments); threaded-comment text survives as plain notes.
- Raise eligibility impact (I-29), the MH-05 burden (I-27) and the Head of Service Delivery salary (I-26) are not quantified because the inputs are not in the workbook.
- Remaining constant-valued legacy names were kept (outside the prune rule).
