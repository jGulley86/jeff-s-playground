# 02-build notes v1 - 2027 COO budget collation

Output: `02-build/02-build_COO_2027_Budget_Collated_v1.xlsx`  
Scripts: `02-build/scripts/` (build.py, recalc.sh, analyze.py, report.py, run_build.sh)  
Inputs (read-only): `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `a3264ef4305e1e7da7c8cf7efbcd5407556aba56e85d50375f9ece711199e9b4`; `Service_Delivery_PL_worksheets.xlsx` sha256 `fedee8d16eb7db72d2745e77a7c6441057b4229131c52d25c944dbb5b858a466`

## Headline

- COO P&L 2027 Net Income (AG132): before **(5,277,004)**, after **(11,851,351)** (change (6,574,348)).
- COO P&L 2026 Net Income (N132): before (899,222), after (899,222). The FO/FE 2026 columns are identical in both books, so 2026 does not move.
- 2027 revenue is still 0 (I-01). The 2027 P&L is cost-only.
- New formula errors introduced by the merge: **0**. COO P&L roll-up check: 2911 cells checked, 0 off by more than $1 (max abs diff 0.0000). COO P&L 'check' row 133 max abs = 0.000000.

## Method

1. **Base = COO book**, loaded with formulas (openpyxl). I deleted the `FO` and `FE` tabs and created new `FO` / `FE` tabs in the same positions (2nd and 5th).
2. **Copied cell by cell from the SD book** (`copy_worksheet` cannot cross workbooks): value or formula (array formulas re-created with the same ref), font, fill, border, alignment, number format, protection, hyperlinks, notes; merged ranges; column widths/hidden/outline; row heights/hidden; freeze panes, gridlines, zoom, tab colour, sheet state; data validations; conditional formats (with their dxf styles).
3. **Dependency closure**: I parsed every formula in SD `FO` and `FE` for sheet references and followed them recursively. The closure is FO, FE, Fld Maint Budget, Fld Ops Payroll, Fld Eng Budget, DeploySum, Prod Payroll (DeploySum and Prod Payroll are reached only indirectly). The SD book has no defined names other than a filter range on the T&E sheet, which is not carried, so no names needed copying. A token scan of every output formula found 0 uses of the COO book's defined names (see I-24).
4. **External links**: 427 DeploySum formula cells reference `[1]` (an external workbook that was not supplied, and the xlsx contains no externalLink part). Each was replaced by its SD cached value: {'#ERROR!': 175, '#REF!': 202, '0': 17, '#N/A': 33}. Google's `#ERROR!` has no Excel equivalent and was stored as `#REF!`. Each cell is listed in the `Collation Notes` sheet (cell, original formula, cached value, stored value) and summarised in the appendix below. No other formula was turned into a value.
5. **COO P&L, PO, CO, PE untouched.** COO P&L formulas reference `FO!`/`FE!` by name, so they pick up the new tabs.
6. **Collation Notes** sheet added at the front, with source, method, live headline formulas, the issues list, and the external-cell list.
7. **Recalculated** with headless LibreOffice 24.2 (`soffice --headless --convert-to xlsx`), using a private profile set to always recalculate on load. I then reloaded with `data_only=True` and checked every cell against the source cached values. The delivered file is the LibreOffice-recalculated file, so cached values are present.

## Sheets in the output and why

| # | Sheet | From | State | Why |
|---|---|---|---|---|
| 1 | Collation Notes | new | visible | Summary of source, method and issues (required) |
| 2 | COO P&L | COO book | visible | Roll-up; unchanged |
| 3 | FO | SD book | visible | Replaces COO FO (newer, fuller build) |
| 4 | PO | COO book | visible | Unchanged |
| 5 | CO | COO book | visible | Unchanged |
| 6 | FE | SD book | visible | Replaces COO FE (newer, fuller build) |
| 7 | PE | COO book | visible | Unchanged |
| 8 | DeploySum | SD book | visible | FO/FE dependency via Fld Ops Payroll, Fld Maint Budget, Fld Eng Budget, Prod Payroll |
| 9 | Fld Ops Payroll | SD book | visible | Direct FO dependency (FO rows 52-54) |
| 10 | Prod Payroll | SD book | hidden | Indirect: Fld Ops Payroll!M5:M7 read Prod Payroll!M5, M6, M9 |
| 11 | Fld Maint Budget | SD book | visible | Direct FO dependency (FO rows 29, 30, 44-49) |
| 12 | Fld Eng Budget | SD book | visible | Direct FE dependency (FE rows 30, 31, 67-69, 74, 75) |

Not carried over (no FO/FE dependency): `Logistics&WH Payroll` (no formula anywhere references it, see I-17), `Old Draft` (hidden, see I-21), `Fld Maint T&E Data` (hidden, see I-16). All three were still scanned.

## Formula preservation

| Sheet | Formulas in source | Formulas in output | External cells -> cached value |
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

Note: in DeploySum the output count (498) = 88 internal formulas kept + 410 error constants that LibreOffice saves as `=#REF!`/`=#N/A` formulas. The other 17 external cells had a cached value of 0 and are stored as the number 0.

## Reconciliation (source cached vs output recalculated)

Source = SD book for FO/FE, COO book for PO/CO/PE. N = 2026 total, AG = 2027 total.

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

| Sheet | Cells compared | Value mismatches | Max abs numeric diff | New errors | Errors cleared | Error code changed (still error) |
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
| Net Income | 132 | AG | (5,277,004) | (11,851,351) | (6,574,348) |

Roll-up integrity: for every COO P&L row 9-132 (except ratio row 65) and 137-140, across B:N and U:AG, COO P&L = FO+PO+CO+FE+PE. 2911 cells checked, 0 failures, max abs diff 0.000000.

## Error scan (#REF!, #NAME?, #VALUE!, #DIV/0!, #N/A, Google #ERROR!)

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

No cell that was a value in the source is an error in the output (new errors = 0). The DeploySum and Prod Payroll errors were already there in the SD book (I-03, I-05). All #DIV/0!/#VALUE!/#NAME? counts are 0.

## Issues

| ID | Sev | Location (sheet!cell) | Finding | Evidence | Recommended action |
|---|---|---|---|---|---|
| I-01 | HIGH | COO P&L!AG16; PO!R12:S15, PO!U12:AF15 | 2027 revenue is zero. All 2026 revenue sits on PO (rows 12, 13, 15). The PO 2027 revenue rows use input method 'Even' with an empty or 0 annual input (S), so U:AF = 0. As a result, the 2027 P&L is cost-only. | COO P&L N16 = 7,423,940, AG16 = 0. PO!R12='Even', S12 empty. PO 4100 N12 6,363,078, 4900 N15 975,000. | Owner of PO/revenue must enter the 2027 revenue (or link it to the Revenue Roll-up). Do not present 2027 Net Income until this is fixed. |
| I-02 | HIGH | COO P&L!AG132 (via FO, FE) | Replacing FO and FE with the SD versions moves the 2027 COO Net Income by about -6.6M. The SD build is far heavier than the COO book's FO/FE. | COO P&L AG132 before (5,277,004), after (11,851,351). FO AG132: COO book (1,341,298) -> SD (7,347,500); FE AG132: COO book (752,002) -> SD (1,320,148). Drivers: FO!N52 876,692 -> AG52 3,238,031; FO!N47 255,704 -> AG47 1,519,865; FO!N29 57,182 -> AG29 765,000. | Ask the COO and the SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off. |
| I-03 | HIGH | DeploySum (rows 3-49, 427 cells) | DeploySum links to a workbook that was not supplied ([1] = 2026 Exist New, Deploy, Deploy Detail, Expansion, New Sales, Revenue Roll-up). In the SD book these cells had already failed. Their cached values were {'#ERROR!': 175, '#REF!': 202, '0': 17, '#N/A': 33}. As instructed, I kept the cached values, so the bookings/deployments/production block (rows 4-42) and the notes A45:A49 show errors in the output. | 427 formula cells contain '[1]...'. Every cell is listed in the 'Collation Notes' sheet with its original formula. DeploySum errors: before {'#ERROR!': 226, '#REF!': 237, '#N/A': 35}, after {'#REF!': 463, '#N/A': 35}. | Get the Revenue Roll-up / Deploy Detail workbook. Then either relink these formulas or paste the values in, so the plan is reproducible. |
| I-04 | HIGH | DeploySum!B53:R66 | The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (and so FO/FE 2027) are typed values, not formulas. The rows above them that should derive them (rows 4-42) are broken, so these drivers can't be traced to a source. | Rows [53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66] contain no formulas. Examples: Fld Ops Payroll!B15 = ROUND(AVERAGE(DeploySum!O54:Q54),0); Fld Maint Budget!B40 = N(DeploySum!F54). | Have the SD owner confirm that rows 53-66 match the current deployment plan (51 new-logo, 15 expansion and 1 existing go-lives in FY27 per R54/R57/R60), then record the source. |
| I-05 | HIGH | Prod Payroll (hidden sheet, all of A24:S81) | The production payroll model doesn't work. Every calculated cell is an error in both the SD book and the output, because it is driven by the broken DeploySum rows 4-42. It does not feed FO/FE: only the input cells M5, M6 and M9 are read, by Fld Ops Payroll. Its result also does not reach PO. | Errors before {'#REF!': 48, '#ERROR!': 748}, after {'#REF!': 796}. References into it: ["Fld Ops Payroll!M5: ='Prod Payroll'!M5", "Fld Ops Payroll!M6: ='Prod Payroll'!M6", "Fld Ops Payroll!M7: ='Prod Payroll'!M9"]. PO 5110 Salaries-Production PO!N33 137,080 -> AG33 525,310 is not linked to it. | Fix DeploySum first. Then decide whether PO production labour (PO rows 33-35) should link to Prod Payroll!row 81. |
| I-06 | HIGH | Fld Maint Budget!B30 (comment), FO!AG44, FO!AG52 | Possible double count of MeLi contractors. Per the SD author's own CONFIRM note, Fld Maint Budget costs them in 5310 (CXC EOR) while Fld Ops Payroll includes them in the 21 all-in techs costed as employees (5510). | Comment on Fld Maint Budget!B30. FO!N44 231,822 -> AG44 575,268 (5310 Contractors-Field); FO!N52 876,692 -> AG52 3,238,031 (5510 Salaries-Field Ops). | The SD owner must confirm the mapping and remove one of the two costings. Until then, FO 2027 may be overstated. |
| I-07 | HIGH | PO!AG19, PO!AG20, PO!AG22 (and COO P&L same cells) | 2027 depreciation on robots is zero, although 2026 carries about 1.75M. PO was out of scope and is left untouched. | PO!N19 1,492,329 -> AG19 0; PO!N20 100,360 -> AG20 0; PO!N22 158,415 -> AG22 0. | PO owner / Finance to budget 2027 depreciation from the fixed-asset schedule. |
| I-08 | MED | PO!U28, PO!Y28, PO!AD28, PO!U38, PO!U42 | Hardcoded plugs are added onto the driver formula in 2027 month cells (+5,000 / +15,000). They are not visible in the method columns R:T. | U28: =IF($R28="Manual","",IFERROR(IF($R28="YOY Growth",$N28*(1+$T28)/12,$S28/12),""))+5000; Y28: =IF($R28="Manual","",IFERROR(IF($R28="YOY Growth",$N28*(1+$T28)/12,$S28/12),""))+5000; AD28: =IF($R28="Manual","",IFERROR(IF($R28="YOY Growth",$N28*(1+$T28)/12,$S28/12),""))+5000; U38: =IF($R38="Manual","",IFERROR(IF($R38="YOY Growth",$N38*(1+$T38)/12,$S38/12),""))+15000; U42: =IF($R42="Manual","",IFERROR(IF($R42="YOY Growth",$N42*(1+$T42)/12,$S42/12),""))+15000 | PO owner to move these amounts into a documented input (column S, or a manual row), or remove them. |
| I-09 | LOW | PE!W74:AF74, PE!W76 | Typed numbers overwrite the driver formula in some 2027 months (manual overrides inside a formula row). | W74=1500, X74=1500, Y74=2000, Z74=2000, AA74=2500, AB74=2500, AC74=3000, AD74=3000, AE74=3500, AF74=4000; W76=300 | PE owner to confirm the overrides are intended, or set the row method to Manual. |
| I-10 | MED | FO!AG58, FO!AG67, FO!AG91, FE!AG91 | Several FO/FE lines with material 2026 spend have 2027 = 0. FO Total Expense (SG&A) is 0 for 2027. | FO!N58 119,260 -> AG58 0; FO!N67 50,575 -> AG67 0; FO!N91 59,734 -> AG91 0; FE!N91 154,857 -> AG91 0; FO!N116 217,242 -> AG116 0. | SD owner to confirm whether these costs stop in 2027 or are budgeted elsewhere (e.g. Fld Eng Budget / Fld Ops Payroll). |
| I-11 | MED | see 'Variance scan' table (all depts + COO P&L) | 98 rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k. | Largest COO P&L moves: COO P&L!N47 319,694 -> AG47 1,554,365; COO P&L!N52 887,966 -> AG52 3,238,031; COO P&L!N29 85,214 -> AG29 765,000; COO P&L!N98 636,000 -> AG98 0. | Each dept owner should comment on the rows that apply to them in the variance table. |
| I-12 | MED | Fld Maint Budget!B8 (D8 note); Fld Maint Budget!E117 | Site setup kit cost is flagged 'PLACEHOLDER - update when the kit list is priced'. It feeds FO 5330 Maintenance Tools & Supplies. | B8 = 4,500 $/new site. FO!N46 23,121 -> AG46 288,069. | SD owner to price the kit list and replace B8. |
| I-13 | MED | Fld Ops Payroll!M11, Fld Ops Payroll!B12 (cell notes) | Two Fld Ops Payroll drivers are marked 'Placeholder' in the author's notes: site techs per floater (M11) and the % of expansion go-lives needing a tech (B12). They drive FO 5510-5540. | M11 = 40, B12 = 0.6. Notes on both cells begin 'Placeholder.' | SD owner to confirm or replace these values. |
| I-14 | LOW | Prod Payroll!M7, B9, A33 (cell notes); Fld Ops Payroll!B9 | More placeholder inputs: Prod Payroll new-hire cost, current headcount and absence factors. Hidden Old Draft!B142 says the Fld Ops Payroll $2,000 new-hire cost (B9) is a placeholder that overlaps onboarding. | Prod Payroll notes start 'Placeholder'. Old Draft!B142 text. Fld Ops Payroll!B9 = 2,000. | SD owner to confirm. The Prod Payroll ones have no FO/FE impact today because that sheet is broken. |
| I-15 | MED | Fld Maint Budget!B12 (comment) | Open CONFIRM: the MeLi contract supervisor is costed in 5310 at $8,704/month. The author's note says Fld Ops Payroll shows 0 current supervisors, but Fld Ops Payroll!H11 (current supervisors - Isaiah) = 1 and E12 says the MeLi supervisor sits in Fld Maint Budget. The supervisor treatment is inconsistent between the two tabs. | Comment on Fld Maint Budget!B12; Fld Maint Budget!B11 = 8,704, B12 = 1; Fld Ops Payroll!H11 = 1. | SD owner to confirm treatment (linked to I-06). |
| I-16 | MED | Fld Maint T&E Data!M5:M379 (hidden SD sheet, not carried) | 101 T&E transactions are flagged 'Reclass needed' = Yes, totalling $27,804.02. The booked GL differs from the budget GL. 2 of them are tagged 'AI suggested' and 17 have tag basis 'Assumed'. If the FO 2026 actuals (B:M) were pulled on booked GL, these amounts sit on the wrong 2026 lines. That distorts the line-level 2026 vs 2027 comparisons, though not the totals. | Top booked->budget GL pairs: 5050->5360 x34, 6100->5360 x16, 5360->5050 x14, 7550->5330 x12, 6100->5050 x8. | Finance to post the reclasses in NetSuite (or confirm none are needed). Review the 'AI suggested' / 'Assumed' tags before relying on T&E unit costs. |
| I-17 | MED | SD 'Logistics&WH Payroll' (not carried) | The SD book's Logistics & Warehouse payroll model says it 'rolls up to Production Operations', but no formula anywhere references it. The COO book's PO tab does not link to it. So the warehouse payroll is either missing from PO 2027 or entered separately. | No formulas reference 'Logistics&WH Payroll' in either book (sheet dependency map). Its own A2 text says it rolls up to PO. | PO owner to confirm whether PO 2027 includes the warehouse team. If not, link PO to this model (it would then need to be added to the workbook). |
| I-18 | LOW | Fld Ops Payroll!B10, B15, B16 (cell notes) | The hiring horizon ends at Dec-27 (DeploySum row 54). Hires for Jan-28 go-lives use an Oct-Dec 27 average default rather than a forecast. | Notes on B10/B15/B16. B15 = ROUND(AVERAGE(DeploySum!O54:Q54),0). | Overwrite B15/B16 if a 2028 go-live forecast exists. |
| I-19 | LOW | FE <-> Fld Eng Budget | FE and Fld Eng Budget link in both directions: Fld Eng Budget reads FE 2026 columns B:J/N/AG, and FE 2027 rows 30, 31, 67-69, 74, 75 read Fld Eng Budget. There is no cell-level circularity (LibreOffice recalculated with no errors), but the structure is easy to break. | Fld Eng Budget has 68 references to FE. FE has 84 references to Fld Eng Budget. | Avoid editing FE rows 30/31/49/50/74/75 2026 columns without checking Fld Eng Budget. |
| I-20 | LOW | Hidden sheets / rows | SD has 3 hidden sheets: Prod Payroll (carried over, kept hidden), Old Draft and Fld Maint T&E Data (not carried over because FO/FE don't depend on them). DeploySum has hidden rows, which are preserved. | Hidden: ['Prod Payroll', 'Old Draft', 'Fld Maint T&E Data']; DeploySum hidden rows 9 (30, 32-36, 40-42). | No action, unless reviewers want Old Draft / T&E Data in the pack for audit. |
| I-21 | LOW | Old Draft (hidden, not carried) | Old Draft dependence is contained. Only Fld Maint T&E Data!Q26 reads Old Draft, while Old Draft reads T&E Data, Fld Ops Payroll and DeploySum. No sheet in the FO/FE chain depends on Old Draft, so the output has 0 references to it. | SD Fld Maint T&E Data: 1 cell(s) e.g. Q26: ='Old Draft'!B28*'Old Draft'!B23. SD dependency map: Old Draft -> {'Fld Maint T&E Data': 458, 'Fld Ops Payroll': 131, 'DeploySum': 112}. | None for the budget. Consider deleting Old Draft from the SD book once T&E Data!Q26 is re-pointed. |
| I-22 | LOW | All dept tabs + COO P&L rows 23/24/27/37 | Rows 23 and 24 carry the same label ('5025 - Freight and Delivery - Production (Summary)'). Row 23 is an empty header. Row 24 holds postings and is inside row 27 = SUM(24:26). Row 37's explicit list (19,20,21,22,27,28,29,30,31,36) covers every direct child of the 18-37 section, so no line is skipped today. But anything typed on row 23 would be left out of the totals. | Subtotal scan on 6 sheets: 0 skipped lines with values. Row 23 is blank on every tab. COO P&L dept-sum formulas: 0 omissions. | Optionally relabel row 23 as a header, or lock it. |
| I-23 | LOW | COO P&L!B65:M65 (row labelled 'Expense'), COO P&L!C141 | COO P&L row 65 (the 'Expense' section header) holds an unlabelled gross-margin % formula (=IFERROR(B64/B16,"")). It is blank for 2027 because revenue is 0. Row 141 'Taxes and Benefits %' shows -1433% for Feb-26, caused by negative 2026 payroll postings. | C141 = -14.33 (ratio). PO!N67 (308,059) -> AG67 0 (negative 2026 SG&A salaries); PE!N35 (56,264) -> AG35 0. | Label row 65. Finance to explain the negative 2026 payroll postings in PO 6610 and PE 5140. |
| I-24 | LOW | Workbook defined names (COO book) | The COO book carries 14,310 legacy defined names from an old template (5,330 resolve to #REF!, some point at external .xls files). No formula uses them. I kept them unchanged. | Count before 14,310, output 14,310. Name tokens found in output formulas: 0. | Purge the names in a separate clean-up (Name Manager), not as part of the budget. |
| I-25 | LOW | Method artefacts (all carried SD sheets) | Side effects of moving from Google Sheets to xlsx: (a) threaded comments come across as plain cell notes, with the text kept; (b) Google's '#ERROR!' code has no Excel equivalent, so cached '#ERROR!' values on external-link cells are stored as #REF!; (c) LibreOffice saves error constants as '=#REF!' formulas; (d) Prod Payroll XLOOKUP cells already failed upstream and still do. | Error-code changes on cells that were already errors: DeploySum 226, Prod Payroll 748. New errors introduced: 0. | None. These are disclosed here for the reviewers. |

### Scan coverage (what was checked, including clean results)

- 2026 (B:N) FO/FE differences between the books, rows 9-141: **0 cells differ**, so no 2026 choice was needed. Formula differences FO/FE (all columns A:AJ, rows 1-200): FO 132, FE 84. All are in 2027 U:AF, where the SD version links to the driver tabs (FO rows 29, 30, 44-49 -> Fld Maint Budget; FO 52-54 -> Fld Ops Payroll, replacing typed numbers; FE 30, 31, 67-69, 74, 75 -> Fld Eng Budget).
- Zero 2027 revenue: I-01.
- External links: I-03 (DeploySum only; no other sheet in either book references another workbook).
- Hardcoded numbers inside formula rows: 7 hits, all listed in I-08 / I-09. Constants in total/roll-up cells: 0. GL codes used as SUMIF keys and 2,080 hours/yr were excluded as false positives.
- Placeholders (PLACEHOLDER/TBD/AI suggested/assumed, in cell values and notes, all sheets of both books): 43 hits. Of these, 30 are in the hidden T&E sheet's tag columns (I-16). The rest are in I-12, I-13, I-14 and DeploySum!A49 ("Arconic + placeholders" in the unsigned-forecast note, part of I-03). 'TBD': 0 hits.
- Variance (>±50% and >$50k, AG vs N): 98 rows, listed below.
- COO P&L dept-sum formulas omitting a dept or pointing at another cell: 0. COO P&L leaf rows not linked to depts while depts hold values: 0.
- Subtotal formulas skipping lines (label-hierarchy check of every 'Total - X' row, columns B/U/AF, on COO P&L and all 5 dept tabs): 0 skipped lines. Row 37 explicitly verified (I-22). Only other hit: COO P&L row 65 header holds a GM% formula (I-23). Gross Profit / Net Ordinary Income / Net Other Income / Net Income formulas: 0 deviations.
- YoY column AJ sign convention: 0 cost rows using AG-N; 0 non-standard formulas.
- Hidden sheets: I-20. 'Reclass needed' = Yes: I-16. Old Draft dependence: I-21 (output has 0 references).

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

### Appendix: external-reference cells (DeploySum), each replaced by its SD cached value

Full per-cell list with original formulas: `Collation Notes` sheet. Summary by row:

| Row | Label (col A) | Cells | SD cached values | Example original formula |
|---:|---|---|---|---|
| 3 | (formula text) | A3 | {'#ERROR!': 1} | `="Tie-out to Deploy Detail (bookings $, deployments, production): "&IF(AND(SUMPRODUCT(ABS(B18:Q18-'[1]Deploy D` |
| 4 |  | B4, C4, D4, E4, F4, G4, H4, I4, J4, K4, L4, M4, N4, O4, P4, Q4 | {'#REF!': 16} | `='[1]Revenue Roll-up'!D17` |
| 6 |  | B6, C6, D6, E6, F6, G6, H6, I6, J6, K6, L6, M6, N6, O6, P6, Q6, R6 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D51` |
| 7 |  | B7, C7, D7, E7, F7, G7, H7, I7, J7, K7, L7, M7, N7, O7, P7, Q7, R7 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D50` |
| 8 |  | B8, C8, D8, E8, F8, G8, H8, I8, J8, K8, L8, M8, N8, O8, P8, Q8, R8 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D65` |
| 9 |  | B9, C9, D9, E9, F9, G9, H9, I9, J9, K9, L9, M9, N9, O9, P9, Q9, R9 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D64` |
| 10 |  | B10, C10, D10, E10, F10, G10, H10, I10, J10, K10, L10, M10, N10, O10, P10, Q10 | {'#REF!': 16} | `=COUNTIF('[1]Deploy Detail'!K21:K62,">0")` |
| 11 |  | B11, C11, D11, E11, F11, G11, H11, I11, J11, K11, L11, M11, N11, O11, P11, Q11, R11 | {'#REF!': 17} | `='[1]Deploy Detail'!K63` |
| 16 |  | B16, C16, D16, E16, F16, G16, H16, I16, J16, K16, L16, M16, N16, O16, P16, Q16, R16 | {'#ERROR!': 17} | `=COUNTIFS('[1]2026 Exist New'!$U$9:$U$50,"Yes",'[1]2026 Exist New'!$E$9:$E$50,"SlipLift",'[1]2026 Exist New'!$` |
| 17 |  | B17, C17, D17, E17, F17, G17, H17, I17, J17, K17, L17, M17, N17, O17, P17, Q17, R17 | {'0': 17} | `=COUNTIFS('[1]2026 Exist New'!$U$9:$U$50,"Yes",'[1]2026 Exist New'!$E$9:$E$50,"SlipBot",'[1]2026 Exist New'!$I` |
| 19 |  | B19, C19, D19, E19, F19, G19, H19, I19, J19, K19, L19, M19, N19, O19, P19, Q19, R19 | {'#ERROR!': 17} | `=[1]Deploy!D47` |
| 20 |  | B20, C20, D20, E20, F20, G20, H20, I20, J20, K20, L20, M20, N20, O20, P20, Q20, R20 | {'#ERROR!': 17} | `=[1]Deploy!D48` |
| 21 |  | B21, C21, D21, E21, F21, G21, H21, I21, J21, K21, L21, M21, N21, O21, P21, Q21, R21 | {'#ERROR!': 17} | `=[1]Deploy!D49` |
| 24 |  | B24, C24, D24, E24, F24, G24, H24, I24, J24, K24, L24, M24, N24, O24, P24, Q24, R24 | {'#ERROR!': 17} | `=[1]Deploy!D53` |
| 25 |  | B25, C25, D25, E25, F25, G25, H25, I25, J25, K25, L25, M25, N25, O25, P25, Q25, R25 | {'#ERROR!': 17} | `=[1]Deploy!D54` |
| 26 |  | B26, C26, D26, E26, F26, G26, H26, I26, J26, K26, L26, M26, N26, O26, P26, Q26, R26 | {'#ERROR!': 17} | `=[1]Deploy!D55` |
| 29 |  | B29, C29, D29, E29, F29, G29, H29, I29, J29, K29, L29, M29, N29, O29, P29, Q29, R29 | {'#ERROR!': 17} | `=[1]Deploy!D68` |
| 30 |  | B30, C30, D30, E30, F30, G30, H30, I30, J30, K30, L30, M30, N30, O30, P30, Q30, R30 | {'#ERROR!': 17} | `=[1]Deploy!D69` |
| 33 |  | B33, C33, D33, E33, F33, G33, H33, I33, J33, K33, L33, M33, N33, O33, P33, Q33 | {'#N/A': 16} | `=SUMIFS('[1]Deploy Detail'!$G$225:$G$236,'[1]Deploy Detail'!$E$225:$E$236,B$4,'[1]Deploy Detail'!$D$225:$D$236` |
| 34 |  | B34, C34, D34, E34, F34, G34, H34, I34, J34, K34, L34, M34, N34, O34, P34, Q34 | {'#N/A': 16} | `=SUMIFS('[1]Deploy Detail'!$H$225:$H$236,'[1]Deploy Detail'!$E$225:$E$236,B$4,'[1]Deploy Detail'!$D$225:$D$236` |
| 35 |  | B35, C35, D35, E35, F35, G35, H35, I35, J35, K35, L35, M35, N35, O35, P35, Q35, R35 | {'#ERROR!': 17} | `=B33*([1]Deploy!$B$7+[1]Deploy!$B$14)+B34*[1]Deploy!$B$8` |
| 38 |  | B38, C38, D38, E38, F38, G38, H38, I38, J38, K38, L38, M38, N38, O38, P38, Q38, R38 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D24` |
| 39 |  | B39, C39, D39, E39, F39, G39, H39, I39, J39, K39, L39, M39, N39, O39, P39, Q39, R39 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D30` |
| 40 |  | B40, C40, D40, E40, F40, G40, H40, I40, J40, K40, L40, M40, N40, O40, P40, Q40, R40 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D38` |
| 41 |  | B41, C41, D41, E41, F41, G41, H41, I41, J41, K41, L41, M41, N41, O41, P41, Q41, R41 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D40` |
| 42 |  | B42, C42, D42, E42, F42, G42, H42, I42, J42, K42, L42, M42, N42, O42, P42, Q42, R42 | {'#REF!': 17} | `='[1]Revenue Roll-up'!D45` |
| 45 | (formula text) | A45 | {'#ERROR!': 1} | `="1. Timing: bookings go live "&'[1]Deploy Detail'!B8&" months after booking (new logos & expansion); units ar` |
| 46 | (formula text) | A46 | {'#ERROR!': 1} | `="2. Deal size: new-logo deal = "&[1]Deploy!B18&" SlipLifts + "&[1]Deploy!B19&" SlipTrays ("&TEXT('[1]New Sale` |
| 47 | (formula text) | A47 | {'#ERROR!': 1} | `="3. Unit cost (CapEx): SlipLift "&TEXT([1]Deploy!B7,"$#,##0")&" + "&TEXT([1]Deploy!B14,"$#,##0")&" peripheral` |
| 48 | (formula text) | A48 | {'#ERROR!': 1} | `="4. SlipBots: "&IF([1]Deploy!B17="Y","none are built – returned/existing bots are redeployed (incl. the Meli ` |
| 49 | (formula text) | A49 | {'#N/A': 1} | `="5. Sep–Dec 26 bookings include unsigned forecast of "&TEXT(SUMIFS('[1]2026 Exist New'!$P$9:$P$50,'[1]2026 Ex` |

## Decisions

- D1: Carried over only the dependency closure of FO/FE (5 tabs), as the handoff specifies. Logistics&WH Payroll, Old Draft and T&E Data were scanned but not carried.
- D2: External `[1]` formulas were replaced by SD cached values, as instructed, even though those values are errors. Google `#ERROR!` was stored as `#REF!` (the closest Excel code for an unresolved link). This keeps error propagation the same, so every downstream IFERROR fallback matches the SD cached results (0 mismatches).
- D3: Kept the COO book's 14,310 legacy defined names unchanged (base book not altered beyond scope). Flagged as I-24.
- D4: Did not change or 'fix' any number, including the plugs, placeholders, zero revenue and zero depreciation. They are flagged only.
- D5: The delivered xlsx is the LibreOffice-recalculated file, so every formula has a cached value. LibreOffice rewrote styles in its own format, and fills, number formats, widths, hidden state, validations and conditional formats survive. Google-specific package parts (workbook metadata, threaded-comment XML) are not kept; note text is kept.
- D6: Tolerance for 'match' = $0.01 per cell (actual max diff below $0.001). Roll-up check tolerance = $1 per the brief.

## Not done / limits

- I could not refresh DeploySum rows 4-42 or Prod Payroll because the external workbook is unavailable (BLOCKER in the handoff, handled as instructed).
- I did not open the output in Microsoft Excel. It was validated in LibreOffice 24.2 only.
