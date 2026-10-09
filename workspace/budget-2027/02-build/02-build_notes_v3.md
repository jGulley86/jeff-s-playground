# 02-build notes v3 - 2027 COO budget collation

Output: `02-build/02-build_COO_2027_Budget_Collated_v3.xlsx` (v1 and v2 files are unchanged)  
Scripts: `02-build/scripts/` - v3 entry point `run_build_v3.sh` (build_v3.py, recalc.sh, analyze_v3.py, report_v3.py). It starts from the delivered v2 workbook; `run_build_v2.sh` still reproduces v2 and `run_build.sh` reproduces v1.  
Inputs (read-only): `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `a3264ef4305e1e7da7c8cf7efbcd5407556aba56e85d50375f9ece711199e9b4`; `Service_Delivery_PL_worksheets.xlsx` sha256 `fedee8d16eb7db72d2745e77a7c6441057b4229131c52d25c944dbb5b858a466`; **new** `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `645e31303dcbbbd6279152aeaa8e5e61dffa0984f1f6116d671408011166fceb`  
Briefs: `00-brief/brief_v2.md`, `00-brief/brief_v3.md` (user decision 2026-10-09: Option 3, straight-line, SlipLift 7 yrs, SlipTray 10 yrs, 'Trays = carriers').  
Recalculation engine: LibreOffice 24.2.7.2 420(Build:2) (headless, recalc on load).

## Headline

| Line | COO P&L row | 2026 (N) | 2027 v3 (AG) | Change | % | 2027 v2 (AG) |
|---|---|---:|---:|---:|---:|---:|
| Revenue | 16 | 7,423,940 | 15,563,646 | 8,139,706 | 110% | 0 |
| COGS | 63 | 4,478,016 | 12,152,017 | 7,674,002 | 171% | 8,833,209 |
|   of which depreciation (in COGS) | 19-22 | 1,788,097 | 3,318,808 | 1,530,712 | 86% | 0 |
| Gross Profit | 64 | 2,945,924 | 3,411,628 | 465,704 | 16% | (8,833,209) |
| Opex | 116 | 3,929,957 | 3,018,142 | (911,815) | -23% | 3,018,142 |
| Net Ordinary Income | 117 | (984,033) | 393,486 | 1,377,519 | 140% | (11,851,351) |
| Net Other Income | 131 | 84,811 | 0 | (84,811) | -100% | 0 |
| **Net Income** | 132 | (899,222) | 393,486 | 1,292,708 | 144% | (11,851,351) |

- **Full 2027 Net Income (COO P&L AG132): 393,486** vs 2026 (899,222). This includes 2027 revenue of 15,563,646 (orchestrator assumption: all to 4100) and depreciation of 3,318,808.
- **Cost-only view:** total COO cost (COGS + Opex, AG63 + AG116) 15,170,160 vs 2026 8,407,973 (change 6,762,187, 80%). Excluding depreciation: 11,851,351 vs 2026 6,619,876. The v2 cost total was 11,851,351, so the only cost change from v2 is the new depreciation, 3,318,808.
- 2027 gross margin (AG65) 21.9%. The 2027 Net Income is now complete in scope, but it rests on the assumptions below. Three need a user decision: SlipBot run rate (I-32), Q4-26 go-lives (I-31) and peripherals (I-33).
- Checks: COO P&L roll-up 2936 cells, 0 off by more than $1 (max 4.9e-08); FO/FE/CO/PE vs v2 **0 formula and 0 value diffs** (CO 39 and PE 3 cells differ by < 1e-9 from LibreOffice recalculation order; no input changed); revenue tie (0.00); depreciation recompute max diff 3.8e-10; new errors **0**; externalLink parts **0**; defined names 8,965.
- Issues: 3 HIGH, 11 MED, 19 LOW (v2: 6 HIGH, 7 MED, 16 LOW).

## Changes from v2

| # | Area | What v3 did | Where |
|---|---|---|---|
| 1 | DeploySum refresh | Rows 3-49 replaced from the 9/30/26 resolved file, mapped by label. The new file has no ARR row, so new rows 39-49 go to rows 40-50 and row 39 (ARR) is kept empty. 410 '[1]' cells stored as cached values (formula text on Collation Notes); 88 internal formulas kept. The 17 v2 'stale external-link value' comments on B17:R17 were removed. | DeploySum!A3:R50 |
| 2 | Tie-out | Live check of rows 16-21 against split rows 54-64, every month: all 0, 'Tie-out rows 16-21 vs 54-64: OK'. | DeploySum!A69:R76 |
| 3 | '$000s' labels | 13 labels relabelled to '$', each with a comment quoting the source label (I-30). | DeploySum col A |
| 4 | Revenue | PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27). PO!R12 = 'Manual'; note in PO!AI12. 4500/4900 unchanged (0). | PO row 12 |
| 5 | Depreciation | New visible tab 'Depreciation Schedule': inputs, existing-fleet lines, vintage calc by month (12 go-live months x lifts/trays/peripherals), output by GL, memo checks. PO!U19:AF22 link to output rows 79-82; PO!R19:R22 = 'Manual'; notes in PO!AI19:AI22. | 'Depreciation Schedule'; PO rows 19-22 |
| 6 | Collation Notes | Rebuilt for v3 (assumptions, live headline, issues, external-formula list). | Collation Notes |
| 7 | Row visibility | DeploySum rows 3-49 follow the 9/30/26 file: v2 hidden [30, 32, 33, 34, 35, 36, 40, 41, 42] -> v3 [41, 42]. Recognized revenue (row 40) is visible because it now feeds PO. | DeploySum |

Issue-level changes (severity v2 -> v3):

| ID | v2 | v3 | Change |
|---|---|---|---|
| I-01 | HIGH | MED | Resolved by assumption (revenue linked to DeploySum); residual 4500/4900 question. HIGH -> MED. |
| I-03 | HIGH | LOW | Resolved: DeploySum refreshed from the 9/30/26 resolved file; 0 errors. HIGH -> LOW. |
| I-04 | HIGH | LOW | Typed drivers now tie to resolved rows 16-21 (live check). HIGH -> LOW. |
| I-05 | LOW | MED | Prod Payroll now partly computes; lift payroll 2027 far above PO 5100. LOW -> MED. |
| I-07 | HIGH | MED | Resolved by assumption (Depreciation Schedule); open parts split to I-31..I-33. HIGH -> MED. |
| I-11 | MED | MED | Evidence refreshed with v3 values. |
| I-20 | LOW | LOW | DeploySum hidden rows now follow the 9/30/26 file. |
| I-23 | LOW | LOW | Row 65 now shows a 2027 margin. |
| I-25 | LOW | LOW | DeploySum errors gone; Prod Payroll error code now #NAME?. |
| I-30 | new | LOW | New in v3. |
| I-31 | new | LOW | New in v3. |
| I-32 | new | HIGH | New in v3. |
| I-33 | new | MED | New in v3. |

All other v2 issues are carried unchanged (FO, FE, CO, PE and the PO non-revenue, non-depreciation lines did not change).

## Completion criteria

| Criterion | Result |
|---|---|
| COO P&L = FO+PO+CO+FE+PE on all cells | 2936 additive cells (rows 9-141, B:N and U:AG; ratio formulas excluded), 0 failures, max abs diff 4.9e-08. Check row 133 max abs 1.7e-10. |
| FO/FE/CO/PE and untouched PO rows: 0 diffs vs v2 | FO, FE, CO, PE: 0 formula / 0 value diffs (table below). PO: formula changes only in rows 12, 19-22 (R, U:AF, AI); value changes only in those rows, their subtotals (14, 16, 37, 63, 64, 117, 132) and the AH '% of total revenue' column. PO formula changes outside the edited rows: 0. COO P&L formula changes: 0. |
| PO row 12 2027 = DeploySum Jan-Dec 27 recognized revenue within $1 | PO!U12:AF12 sum 15,563,645.54; 9/30/26 file F39:Q39 sum 15,563,645.54, R39 15,563,645.54; diff (0.00). |
| Depreciation recomputes by hand for a sampled month | Jun-27 shown below; Python recompute of all 48 GL-months from raw inputs: max diff 3.8e-10. |
| 0 new errors (excluding resolved DeploySum cells); 0 externalLink parts | New errors 0. Resolved: DeploySum 498, Prod Payroll 366. externalLink parts 0, externalReference elements 0. |
| Every assumption registered | Assumptions register below (A-01..A-21), each with its source or 'user-confirmed' / 'orchestrator assumption' / 'builder assumption'. |

## Depreciation schedule summary

Tab `Depreciation Schedule` (visible, after DeploySum). Method: straight-line, no salvage, full month of depreciation from the go-live month (input B13 = 0; set 1 to start the month after). New units = DeploySum rows 19/20 (units going live), Jan-Dec 27. Existing fleet = PO Dec-26 monthly run rate, carried flat. Output = SUMIF by GL over all calc lines, then PO!U19:AF22.

**Inputs**

| Input | Value | Cell | Source |
|---|---:|---|---|
| SlipLift unit cost | 65,000.00 | B6 | DeploySum!A46 note 3: 'SlipLift $65,000' |
| SlipLift peripherals per lift | 4,137.50 | B7 | Derived: (R29 32,410,900 - R25 1,355 x 8,000) / R24 312 - 65,000. Note 3 prints '$4,138' (TEXT format rounds to whole dollars). |
| SlipTray unit cost | 8,000.00 | B8 | DeploySum!A46 note 3: 'SlipTray $8,000' |
| SlipLift life | 84 months | B9 | user-confirmed (7 years) |
| SlipTray life | 120 months | B10 | user-confirmed (10 years) |
| Peripherals life | 84 months (=B9) | B11 | builder assumption (I-33) |
| Salvage | 0% | B12 | user-confirmed / brief v3 |
| Start delay after go-live month | 0 | B13 | brief v3 convention (labelled input) |
| GL SlipLift / SlipTray / peripherals | 5011 / 5012 / 5020 | B14:B16 | user-confirmed / user-confirmed / builder assumption |

**Units (DeploySum, 9/30/26)**: 2027 go-lives 250 SlipLifts and 1,036 SlipTrays (R19/R20; = SD rows 55+58+61 and 56+59+62). By month (Jan..Dec 27): lifts [20, 8, 0, 22, 14, 20, 18, 22, 28, 28, 34, 36]; trays [60, 24, 0, 86, 61, 98, 73, 85, 122, 122, 159, 146]. Unit-months in service in 2027: lifts 1,296, trays 5,113. No SlipBots go live or are built (rows 21/26 = 0; note 4).

**Depreciation by GL, existing vs new**

| GL | 2026 (PO N) | Existing: Dec-26 run rate /month | Existing 2027 | New 2027 go-lives: 2027 | New: Dec-27 /month | Total 2027 | Jan-27 /month | Dec-27 /month |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5010 SlipBot (PO row 19) | 1,492,329 | 112,797.85 | 1,353,574 | 0 | 0.00 | 1,353,574 | 112,797.85 | 112,797.85 |
| 5011 SlipLift (PO row 20) | 100,360 | 20,444.90 | 245,339 | 1,002,857 | 193,452.38 | 1,248,196 | 35,921.09 | 213,897.28 |
| 5012 SlipCarrier (SlipTray) (PO row 21) | 36,993 | 6,502.64 | 78,032 | 340,867 | 69,066.67 | 418,898 | 10,502.64 | 75,569.31 |
| 5020 Robot Peripherals (PO row 22) | 158,415 | 19,525.33 | 234,304 | 63,836 | 12,313.99 | 298,140 | 20,510.45 | 31,839.32 |
| **Total** | 1,788,097 | 159,270.72 | 1,911,249 | 1,407,560 | 274,833.04 | 3,318,808 | 179,732.03 | 434,103.76 |

Monthly per unit: SlipLift 65,000/84 = 773.81; SlipTray 8,000/120 = 66.67; peripherals 4,137.50/84 = 49.26.

**Hand recompute, sampled month Jun-27** (go-lives Jan-Jun 27 in service under the full-month rule: 84 lifts = 20+8+0+22+14+20; 329 trays = 60+24+0+86+61+98):

| GL | Existing run rate | New units | Hand total | Workbook PO!Z (Jun-27) |
|---|---:|---|---:|---:|
| 5010 | 112,797.85 | none | 112,797.85 | 112,797.85 |
| 5011 | 20,444.90 | 84 x 65,000 / 84 = 65,000.00 | 85,444.90 | 85,444.90 |
| 5012 | 6,502.64 | 329 x 8,000 / 120 = 21,933.33 | 28,435.97 | 28,435.97 |
| 5020 | 19,525.33 | 84 x 4,137.50 / 84 = 4,137.50 | 23,662.83 | 23,662.83 |

**Existing fleet: PO 2026 monthly depreciation (rows 19-22; B:I actual, J:M forecast)**

| GL | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep F | Oct F | Nov F | Dec F | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5010 SlipBot | 141,122 | 122,212 | 126,630 | 128,215 | 133,969 | 133,969 | 127,510 | 127,510 | 112,798 | 112,798 | 112,798 | 112,798 | 1,492,329 |
| 5011 SlipLift | 0 | 0 | 1,678 | 3,263 | 3,263 | 11,653 | 7,458 | 9,836 | 8,838 | 15,802 | 18,123 | 20,445 | 100,360 |
| 5012 SlipCarrier (SlipTray) | 0 | 0 | 0 | 1,791 | 3,125 | 4,796 | 3,294 | 3,909 | 2,969 | 4,903 | 5,703 | 6,503 | 36,993 |
| 5020 Robot Peripherals | 8,212 | 10,914 | 10,939 | 13,556 | 13,556 | 13,770 | 8,509 | 8,592 | 14,867 | 17,475 | 18,500 | 19,525 | 158,415 |

Do J:M step up with the Sep-Dec 26 go-lives (DeploySum B:E)? Partly. DeploySum has Sep 0, Oct 9, Nov 9, Dec 0 lifts and Sep 0, Oct 35, Nov 32, Dec 0 trays. The PO forecast steps up by exact multiples of the DeploySum unit cost over the user's lives: 5011 by 9, 3, 3 lifts x 65,000/84 (Oct/Nov/Dec) and 5012 by 29, 12, 12 trays x 8,000/120. So the forecast already holds Q4-26 go-lives at the same costs and lives, but fewer of them: October lifts match; the rest do not. 5020's steps (2,608.33, 1,025.00, 1,025.00) are not whole multiples of the DeploySum peripheral cost, so their basis is unknown. 5010 is flat Sep-Dec at 112,797.85.

**Decision: rely on the run rate.** Oct-Dec 26 go-lives are not added explicitly, so there is no double count. Why: the run rate is PO's own forecast and already contains Q4-26 step-ups priced like the schedule. Adding DeploySum's Q4 units on top would double count the 15 lifts and 53 trays already in it. The 3-lift / 14-tray shortfall vs DeploySum (39,057 for 2027) is shown as a memo (schedule section 5) and logged as I-31 for a user decision.

**SlipBot 5010:** carried at the Dec-26 run rate 112,797.85/month = 1,353,574 for 2027 (2026: 1,492,329). This carries the run rate through 2027 as instructed; it is not evidence that the fleet is still depreciating. Fleet status is unknown: **user to confirm** whether it is fully depreciated, retired or ongoing (I-32).

## Unit-cost reconciliation

CapEx ÷ units to build does not give a single per-unit price because CapEx is a two-product sum: **CapEx = SlipLifts to build x (65,000 + 4,137.50) + SlipTrays to build x 8,000**. Deployment freight ($5,000 per deployment, note 3) is expensed on its own row (30) and is not in CapEx. The DeploySum formula for row 35 (`=B33*([1]Deploy!$B$7+[1]Deploy!$B$14)+B34*[1]Deploy!$B$8`) has the same structure: lift cost + peripherals, plus tray cost. The note's '$4,138' is 4,137.50 rounded by `TEXT(...,"$#,##0")`.

| Production month | Lifts | Trays | CapEx (row 29) | CapEx ÷ all units | Lifts x 69,137.50 + trays x 8,000 | Residual | Residual using note's $4,138 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sep-26 | 9 | 32 | 878,237.50 | 21,420.43 | 878,237.50 | 0.00 | (4.50) |
| Oct-26 | 0 | 0 | 0.00 |  | 0.00 | 0.00 | 0.00 |
| Nov-26 | 20 | 60 | 1,862,750.00 | 23,284.38 | 1,862,750.00 | 0.00 | (10.00) |
| Dec-26 | 8 | 24 | 745,100.00 | 23,284.38 | 745,100.00 | 0.00 | (4.00) |
| Jan-27 | 0 | 0 | 0.00 |  | 0.00 | 0.00 | 0.00 |
| Feb-27 | 22 | 86 | 2,209,025.00 | 20,453.94 | 2,209,025.00 | 0.00 | (11.00) |
| Mar-27 | 14 | 61 | 1,455,925.00 | 19,412.33 | 1,455,925.00 | 0.00 | (7.00) |
| Apr-27 | 20 | 98 | 2,166,750.00 | 18,362.29 | 2,166,750.00 | 0.00 | (10.00) |
| May-27 | 18 | 73 | 1,828,475.00 | 20,093.13 | 1,828,475.00 | 0.00 | (9.00) |
| Jun-27 | 22 | 85 | 2,201,025.00 | 20,570.33 | 2,201,025.00 | 0.00 | (11.00) |
| Jul-27 | 28 | 122 | 2,911,850.00 | 19,412.33 | 2,911,850.00 | 0.00 | (14.00) |
| Aug-27 | 28 | 122 | 2,911,850.00 | 19,412.33 | 2,911,850.00 | 0.00 | (14.00) |
| Sep-27 | 34 | 159 | 3,622,675.00 | 18,770.34 | 3,622,675.00 | 0.00 | (17.00) |
| Oct-27 | 36 | 146 | 3,656,950.00 | 20,093.13 | 3,656,950.00 | 0.00 | (18.00) |
| Nov-27 | 42 | 183 | 4,367,775.00 | 19,412.33 | 4,367,775.00 | 0.00 | (21.00) |
| Dec-27 | 48 | 220 | 5,078,600.00 | 18,950.00 | 5,078,600.00 | 0.00 | (24.00) |

Max |residual| with 4,137.50: 0.00 in every month. With the note's rounded $4,138 the gap is $0.50 per lift ((174.50) over Sep-26..Dec-27). Using the note's figure would overstate 2027 depreciable cost by 125.00 (250 lifts x $0.50); the schedule uses the reconciling 4,137.50. Handoff examples: Sep-26 9 x 69,137.50 + 32 x 8,000 = 878,237.50; Nov-26 20 x 69,137.50 + 60 x 8,000 = 1,862,750.

Depreciable cost of 2027 go-lives = 250 x 69,137.50 + 1,036 x 8,000 = 25,572,375. CapEx bridge: FY27 CapEx 32,410,900 - CapEx for 2028 go-lives 9,446,375 + Nov-Dec 26 builds for Jan-Feb 27 go-lives 2,607,850 = 25,572,375 (difference 0). Builds for 2028 go-lives (90 lifts, 403 trays) are not in service in 2027, so they are not depreciated.

## Revenue

| Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | 2027 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PO!U12:AF12 = DeploySum!F40:Q40 | 783,428 | 821,920 | 807,746 | 907,122 | 997,376 | 1,116,046 | 1,231,592 | 1,379,626 | 1,561,857 | 1,751,627 | 1,975,163 | 2,230,141 | 15,563,646 |

Every cell is a formula (`=DeploySum!F40` ... `=DeploySum!Q40`). 2026 revenue (PO N16) 7,423,940: 4100 6,363,078, 4500 85,861, 4900 975,000. Sep-Dec 26 cross-check: DeploySum recognized revenue 570,292, 632,828, 662,103, 662,103 vs PO 4100 forecast 531,107, 626,941, 651,941, 676,941.

## Assumptions register

| ID | Assumption | Value / effect | Where | Source |
|---|---|---|---|---|
| A-01 | 2027 revenue = DeploySum recognized revenue Jan-Dec 27 | 15,563,646 | PO!U12:AF12 <- DeploySum!F40:Q40 | DeploySum 9/30/26 (row 39 in that file) |
| A-02 | All 2027 revenue maps to 4100 Subscription/Platform Fees | 4100 = 100% | PO row 12 | orchestrator assumption (brief v3) |
| A-03 | 4500 Implementation and 4900 One-Time revenue stay 0 in 2027 | 0 | PO rows 13, 15 (unchanged) | orchestrator assumption (brief v3: source does not split them) |
| A-04 | Straight-line depreciation, no salvage | salvage 0% | 'Depreciation Schedule'!B12 | user-confirmed 2026-10-09 |
| A-05 | SlipLift useful life | 84 months | 'Depreciation Schedule'!B9 | user-confirmed 2026-10-09 |
| A-06 | SlipTray useful life | 120 months | 'Depreciation Schedule'!B10 | user-confirmed 2026-10-09 |
| A-07 | SlipLift unit cost | 65,000 | 'Depreciation Schedule'!B6 | source: DeploySum!A46 note 3 |
| A-08 | SlipTray unit cost | 8,000 | 'Depreciation Schedule'!B8 | source: DeploySum!A46 note 3 |
| A-09 | SlipLift peripherals cost per lift | 4,137.50 | 'Depreciation Schedule'!B7 (formula) | source: derived from DeploySum R29/R24/R25; reconciles every month (note shows $4,138 rounded) |
| A-10 | Peripherals life = SlipLift life | 84 months | 'Depreciation Schedule'!B11 | builder assumption (I-33) |
| A-11 | Peripherals GL | 5020 Robot Peripherals | 'Depreciation Schedule'!B16 | builder assumption (I-33); alternative 5011 |
| A-12 | SlipLift GL | 5011 SlipLift Depreciation | 'Depreciation Schedule'!B14 | user-confirmed (handoff) |
| A-13 | SlipTray GL | 5012 SlipCarrier Depreciation | 'Depreciation Schedule'!B15 | user-confirmed 2026-10-09 ('Trays = carriers') |
| A-14 | In-service = go-live month (DeploySum rows 19/20); full month of depreciation in that month | start delay 0; sensitivity: 1-month delay lowers 2027 by 274,833 | 'Depreciation Schedule'!B13 | brief v3 convention (orchestrator; labelled; user may change) |
| A-15 | Units built in 2027 for 2028 go-lives are not depreciated in 2027 | CapEx 9,446,375 excluded | 'Depreciation Schedule' section 7 | follows A-14 (not in service) |
| A-16 | Existing fleet = PO Dec-26 monthly run rate | 159,270.72/month | 'Depreciation Schedule'!B21:B24 = PO!M19:M22 | orchestrator instruction (handoff) |
| A-17 | Existing run rates stay flat all of 2027 (no end-of-life, retirement or disposal) | 1,911,249 | 'Depreciation Schedule' rows 33-36 | builder assumption: no asset register in the files (I-32) |
| A-18 | Oct-Dec 26 go-lives covered by the run rate, not added explicitly | memo gap 39,057 | 'Depreciation Schedule'!B17, section 5 | builder decision between the handoff's two options (I-31) |
| A-19 | SlipBot 5010 continues at the Dec-26 run rate; no new SlipBots | 1,353,574 | 'Depreciation Schedule'!B21 | orchestrator instruction to carry; status user to confirm (I-32); no builds per DeploySum note 4 |
| A-20 | '$000s' labels on DeploySum hold dollars; relabelled to '$' with comments | 13 labels | DeploySum col A | orchestrator instruction; evidence in I-30 |
| A-21 | ARR row (39) kept empty to keep the SD row map | no data | DeploySum row 39 | brief v2 item 1 |

## DeploySum refresh and tie-out

Row map (by label; verified: every label in the new file matches the mapped row after the '$000s' relabel, mismatches 0): new rows 1-38 -> same rows; new rows 39-49 -> rows 40-50. Row 39 'ARR - end of period' has no counterpart; B39:R39 cleared, comment on A39. Value check: every mapped cell B:R equals the 9/30/26 cached value (mismatches 0).

| v3 row | Label | '[1]' cells stored as values | Example original formula |
|---:|---|---:|---|
| 3 | (row 3 tie-out text) | 1 | `="Tie-out to Deploy Detail (bookings $, deployments, production): "&IF(AND(SUMPRODUCT(ABS(` |
| 4 | (month-end dates) | 16 | `='[1]Revenue Roll-up'!D17` |
| 6 | New logos – deals booked (#) | 17 | `='[1]Revenue Roll-up'!D51` |
| 7 | New logos – bookings ($) | 17 | `='[1]Revenue Roll-up'!D50` |
| 8 | Expansion – deals booked (#) | 17 | `='[1]Revenue Roll-up'!D65` |
| 9 | Expansion – bookings ($) | 17 | `='[1]Revenue Roll-up'!D64` |
| 10 | Existing & forecast contracts – booked (#) | 16 | `=COUNTIF('[1]Deploy Detail'!K21:K62,">0")` |
| 11 | Existing & forecast contracts – bookings ($) | 17 | `='[1]Deploy Detail'!K63` |
| 16 | SlipLift deployments (#) | 17 | `=COUNTIFS('[1]2026 Exist New'!$U$9:$U$50,"Yes",'[1]2026 Exist New'!$E$9:$E$50,"SlipLift",'` |
| 17 | SlipBot deployments (#) | 17 | `=COUNTIFS('[1]2026 Exist New'!$U$9:$U$50,"Yes",'[1]2026 Exist New'!$E$9:$E$50,"SlipBot",'[` |
| 19 | SlipLifts going live (units) | 17 | `=[1]Deploy!D47` |
| 20 | SlipTrays going live (units) | 17 | `=[1]Deploy!D48` |
| 21 | SlipBots going live (units) | 17 | `=[1]Deploy!D49` |
| 24 | SlipLifts to build | 17 | `=[1]Deploy!D53` |
| 25 | SlipTrays to build | 17 | `=[1]Deploy!D54` |
| 26 | SlipBots to build | 17 | `=[1]Deploy!D55` |
| 29 | Production CapEx ($) | 17 | `=[1]Deploy!D68` |
| 30 | Deployment freight – expensed ($) | 17 | `=[1]Deploy!D69` |
| 33 | SlipLifts built for 2028 go-lives | 16 | `=SUMIFS('[1]Deploy Detail'!$G$225:$G$236,'[1]Deploy Detail'!$E$225:$E$236,B$4,'[1]Deploy D` |
| 34 | SlipTrays built for 2028 go-lives | 16 | `=SUMIFS('[1]Deploy Detail'!$H$225:$H$236,'[1]Deploy Detail'!$E$225:$E$236,B$4,'[1]Deploy D` |
| 35 | CapEx for 2028 go-lives – estimate ($) | 17 | `=B33*([1]Deploy!$B$7+[1]Deploy!$B$14)+B34*[1]Deploy!$B$8` |
| 38 | CARR – end of period ($) | 17 | `='[1]Revenue Roll-up'!D24` |
| 40 | Recognized revenue ($) | 17 | `='[1]Revenue Roll-up'!D38` |
| 41 | Billings ($) | 17 | `='[1]Revenue Roll-up'!D40` |
| 42 | Deferred revenue – end of period ($) | 17 | `='[1]Revenue Roll-up'!D45` |
| 45 | 1. Timing: bookings go live 3 months after booking (new logos & expans | 1 | `="1. Timing: bookings go live "&'[1]Deploy Detail'!B8&" months after booking (new logos & ` |
| 46 | 2. Deal size: new-logo deal = 4 SlipLifts + 12 SlipTrays ($316,000); e | 1 | `="2. Deal size: new-logo deal = "&[1]Deploy!B18&" SlipLifts + "&[1]Deploy!B19&" SlipTrays ` |
| 47 | 3. Unit cost (CapEx): SlipLift $65,000 + $4,138 peripherals, SlipTray  | 1 | `="3. Unit cost (CapEx): SlipLift "&TEXT([1]Deploy!B7,"$#,##0")&" + "&TEXT([1]Deploy!B14,"$` |
| 48 | 4. SlipBots: none are built – returned/existing bots are redeployed (i | 1 | `="4. SlipBots: "&IF([1]Deploy!B17="Y","none are built – returned/existing bots are redeplo` |
| 49 | 5. Sep–Dec 26 bookings include unsigned forecast of $2,264,000 (Arconi | 1 | `="5. Sep–Dec 26 bookings include unsigned forecast of "&TEXT(SUMIFS('[1]2026 Exist New'!$P` |

Total external cells stored as values: 410. Comments removed: 17 (DeploySum!B17, DeploySum!C17, DeploySum!D17, ...). Comments added: 13 (the relabels and A39).

**Tie-out rows 16-21 vs 54-64** (live in DeploySum!A69:R76):

| Check | FY27 top | FY27 split | Sep-Dec 26 top | Sep-Dec 26 split | Max abs monthly diff (B:R) |
|---|---:|---:|---:|---:|---:|
| 16+17 vs 54+57+60 | 67 | 67 | 4 | 4 | 0 |
| 18 vs 64 | 67 | 67 | 4 | 4 | 0 |
| 19 vs 55+58+61 | 250 | 250 | 18 | 18 | 0 |
| 20 vs 56+59+62 | 1,036 | 1,036 | 67 | 67 | 0 |
| 21 vs 63 | 0 | 0 | 0 | 0 | 0 |

Status cell DeploySum!A76: 'Tie-out rows 16-21 vs 54-64: OK'. FY27: deployments 67, SlipLifts 250 = 212+30+8, SlipTrays 1,036 = 636+375+25, matching the orchestrator pre-scan.

## v2 -> v3 diff

`analyze_v3.py`: formulas compared exactly, cached values exactly except numeric differences <= 1e-6 (recalculation-order float noise, counted separately).

| Sheet | Cells | Formula diffs | Value diffs | Float-noise cells (max) |
|---|---:|---:|---:|---:|
| COO P&L | 3,530 | 0 | 288 | 23 (1.0e-09) |
| FO | 3,581 | 0 | 0 | 0 (0.0e+00) |
| PO | 3,631 | 70 | 285 | 3 (1.0e-09) |
| CO | 3,582 | 0 | 0 | 39 (9.9e-10) |
| FE | 3,582 | 0 | 0 | 0 (0.0e+00) |
| PE | 3,590 | 0 | 0 | 3 (1.0e-10) |
| DeploySum | 918 | 533 | 621 | 0 (0.0e+00) |
| Fld Ops Payroll | 1,165 | 0 | 0 | 0 (0.0e+00) |
| Prod Payroll | 1,173 | 0 | 798 | 0 (0.0e+00) |
| Fld Maint Budget | 1,012 | 0 | 0 | 0 (0.0e+00) |
| Fld Eng Budget | 739 | 0 | 0 | 0 (0.0e+00) |

New sheet: Depreciation Schedule. Collation Notes was rebuilt (not compared).

PO rows with any change:

| Row | Line | Columns | Class |
|---:|---|---|---|
| 12 | 4100 - Subscription/Platform Fees | R, U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AI, AJ | edited line |
| 13 | 4500 - Implementation Fees | AH | edited line |
| 14 | Total - 4000 - Sales | U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AJ | subtotal / derived |
| 15 | 4900 - One-Time Revenue | AH | edited line |
| 16 | Total - Income | U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AJ | subtotal / derived |
| 19 | 5010 - SlipBot Depreciation | R, U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AI, AJ | edited line |
| 20 | 5011 - SlipLift Depreciation | R, U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AI, AJ | edited line |
| 21 | 5012 - SlipCarrier Depreciation | R, U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AI, AJ | edited line |
| 22 | 5020 - Robot Peripherals Depreciation | R, U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AI, AJ | edited line |
| 37 | Total - 5000 - Robot Production and Deployment | U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AJ | subtotal / derived |
| 63 | Total - Cost Of Sales | U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AJ | subtotal / derived |
| 64 | Gross Profit | U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AJ | subtotal / derived |
| 117 | Net Ordinary Income | U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AJ | subtotal / derived |
| 132 | Net Income | U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF, AG, AH, AJ | subtotal / derived |
| 93 rows | every other PO line | AH only | AH '% Total Rev' = AG/AG$16; blank in v2 because 2027 revenue was 0 |

Rows 13 and 15 change only in AH. Their budget values (U:AF) are unchanged, at 0. PO formula changes outside rows 12 and 19-22: 0. COO P&L: 0 formula changes; value changes on 108 rows; outside the revenue/depreciation chain (rows 12-16, 19-22, 37, 63-65, 117, 132) only column AH changed (checked: 0 exceptions).

DeploySum: 533 formula / 621 value diffs are the refresh (rows 3-50) and the new check block (rows 69-76). Prod Payroll: 0 formula diffs and 798 value diffs, because it reads DeploySum rows 4/24/25/27/28 (I-05). Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget read only DeploySum rows 53-66, and show 0 diffs.

## Error scan

| Sheet | v2 | v3 |
|---|---|---|
| COO P&L | none | none |
| FO | none | none |
| PO | none | none |
| CO | none | none |
| FE | none | none |
| PE | none | none |
| DeploySum | {'#REF!': 463, '#N/A': 35} | none |
| Depreciation Schedule | none | none |
| Fld Ops Payroll | none | none |
| Prod Payroll | {'#REF!': 796} | {'#NAME?': 430} |
| Fld Maint Budget | none | none |
| Fld Eng Budget | none | none |

New errors (a cell that is an error in v3 but not in v2): **0**. Prod Payroll's remaining 430 errors were errors in v2 too; the code changed from #REF! to #NAME? because the DeploySum inputs now resolve and LibreOffice then reaches the 16 XLOOKUP cells (row 48), which it does not support; the other #NAME? cells are below them.

## Package

Final package: 38 parts; `xl/externalLinks/*` **0**; `<externalReference>` 0; defined names 8,965 (v2: 8,965; none added or removed).

## Sheets in the output

| # | Sheet | State |
|---|---|---|
| 1 | Collation Notes | visible |
| 2 | COO P&L | visible |
| 3 | FO | visible |
| 4 | PO | visible |
| 5 | CO | visible |
| 6 | FE | visible |
| 7 | PE | visible |
| 8 | DeploySum | visible |
| 9 | Depreciation Schedule | visible |
| 10 | Fld Ops Payroll | visible |
| 11 | Prod Payroll | hidden |
| 12 | Fld Maint Budget | visible |
| 13 | Fld Eng Budget | visible |

## Severity scale

HIGH = blocks sign-off or > $250k impact; MED = $50k-250k or needs owner confirmation; LOW = < $50k or hygiene.

Applied in this order: (1) HIGH if the item blocks sign-off or its $ impact computed from the workbook is > $250k; (2) MED if that impact is $50k-250k; (3) MED if the impact cannot be determined from the workbook and an owner must confirm; (4) otherwise LOW (impact < $50k, $0, or hygiene). 'Impact' is the amount the item could move the 2027 budget, read from cells; where only an exposure (the amount resting on the item) is known, it is shown but not used as the impact.

## Issues (v3)

Severity per the scale above. 'Basis' shows which rule set the rating. v2 rows not listed under 'Issue-level changes' are carried verbatim.

| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |
|---|---|---|---|---|---|---|---|
| I-01 | MED | PO!U12:AF12; PO!R12; PO!U13:AF13; PO!U15:AF15; DeploySum!F40:Q40 | Resolved by assumption in v3. 2027 revenue is now budgeted: PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27; row 39 in the 9/30/26 file), all to 4100 Subscription/Platform Fees (orchestrator assumption). PO!R12 set to 'Manual'. Still open: 4500 Implementation Fees and 4900 One-Time Revenue stay 0 in 2027, and the source does not say whether recognized revenue includes them. | PO!AG12 = 15,563,645.54; DeploySum FY27 recognized revenue (9/30/26 file R39) = 15,563,645.54; difference (0.00). 2026: 4500 85,861, 4900 975,000. Cross-check Sep-Dec 26: DeploySum recognized revenue 2,527,326 vs PO 4100 forecast (PO!J12:M12) 2,486,929 (difference 40,396), so the 4100 mapping is consistent with how PO forecasts 2026. | not determinable (2026 4500+4900 = 1,060,861) | impact not determinable; owner confirmation needed | Finance/PO owner to confirm the 4100 mapping and whether 2027 implementation or one-time revenue should be budgeted on 4500/4900. |
| I-02 | HIGH | COO P&L!AG132; FO!AG132; FE!AG132 | Replacing FO and FE with the SD versions moves 2027 COO Net Income by (6,574,348). The SD build is much heavier than the COO book's FO/FE. | COO P&L!AG132 before (5,277,004), after (11,851,351). FO!AG132 COO book (1,341,298) -> SD (7,347,500); FE!AG132 COO book (752,002) -> SD (1,320,148). Drivers: FO!N52 876,692 -> AG52 3,238,031; FO!N47 255,704 -> AG47 1,519,865; FO!N29 57,182 -> AG29 765,000. | (6,574,348) | impact (6,574,348) | COO and SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off. |
| I-03 | LOW | DeploySum!A3:R49 (Collation Notes lists the formulas) | Resolved in v3. DeploySum rows 3-49 now hold the resolved values from 2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx. The 410 cells that link to the external workbook '[1]' are stored as that file's cached values; their formula text is on Collation Notes. The links are still not live (the [1] workbook was not supplied), so the next plan update needs a new resolved export. | DeploySum errors: v2 {'#REF!': 463, '#N/A': 35}, v3 none (498 resolved). Every mapped cell B:R equals the 9/30/26 cached value (mismatches: 0). New-file sha256 645e31303dcbbbd6... | 0 | hygiene | Refresh DeploySum from a new resolved export when the plan changes. Keep the row map (ARR row 39 kept). |
| I-04 | LOW | DeploySum!B53:R66; DeploySum!A69:R76 (v3 check block) | The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (rows 53-66) are still typed values. v3 adds a live check: they now tie to the resolved rows 16-21 in every month Sep-26..FY27. So the FO/FE drivers are consistent with the 9/30/26 plan; they are just not linked. | 16+17 vs 54+57+60: FY 67 vs 67, max monthly diff 0; 18 vs 64: FY 67 vs 67, max monthly diff 0; 19 vs 55+58+61: FY 250 vs 250, max monthly diff 0; 20 vs 56+59+62: FY 1,036 vs 1,036, max monthly diff 0; 21 vs 63: FY 0 vs 0, max monthly diff 0. DeploySum!A76 = 'Tie-out rows 16-21 vs 54-64: OK'. | 0 | hygiene | Optional: replace rows 54-64 with formulas (or document the source) so they update with the plan. |
| I-05 | MED | Prod Payroll!B24:S81 (hidden); Prod Payroll!S41; PO!AG33:AG36 | The production payroll model now partly computes. It reads DeploySum rows 4, 24, 25, 27 and 28, which v3 resolved. Errors fell from 796 to 430. The remaining 430 are #NAME?: 16 cells use _xlfn.xlookup (row 48), which LibreOffice 24.2.7.2 does not support, and the rest are in rows 49-81 below them (#NAME? propagates). Excel may evaluate them; not tested. It still feeds no budget value: FO/FE/CO/PE show 0 diffs and PO payroll rows are typed. Now that it computes, 'Total lift payroll' 2027 is far above PO's typed production labour. | Prod Payroll!S41 'Total lift payroll' (F:Q = Jan-Dec 27) = 1,622,423; tray (row 62), supervisor (row 79) and total (row 81) are still #NAME? in LibreOffice. PO 'Total - 5100 - Labor Expense - Production' AG36 = 652,820 (typed rows 33-35). Cells read from Prod Payroll by other sheets: typed raise inputs only (M5, M6, M9), unchanged. | not determinable (exposure: lift payroll alone 1,622,423 vs PO 5100 652,820) | impact not determinable; owner confirmation needed | PO owner to say which production payroll is right: the typed PO 5110-5140, or this model (open it in Excel to evaluate the XLOOKUP rows). See also I-17. |
| I-06 | LOW | Fld Maint Budget!B30 (comment); Fld Ops Payroll!B11; FO!AG44; FO!AG52 | MeLi contractor double count: quantified at $0 in the current cells. The CONFIRM comment on Fld Maint Budget!B30 says Fld Ops Payroll includes MeLi in '21 all-in techs', but Fld Ops Payroll!B11 = 14 ('Current site techs on payroll (Sep-26) - Domestic Only') and Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11 = 21. So MeLi techs are costed in 5310 only. The comment describes an earlier state and is stale (Fld Maint Budget!A143 records the correction). | FO 5310 (FO!AG44 = 575,268) = MeLi techs in role 346,920 + Merida contractors 123,900 + MeLi supervisor 104,448 (Fld Maint Budget rows 70-72 x B10/B11; row 84 = 575,268). FO 5510 current techs: Fld Ops Payroll!F20:Q20 = 14 each month (formula =$B$11); current-tech payroll 2027 1,094,774. | 0 | impact 0 | SD owner to confirm and delete the stale CONFIRM comment on Fld Maint Budget!B30. |
| I-07 | MED | PO!U19:AF22; 'Depreciation Schedule'!A1:S126; COO P&L!AG19:AG22 | Resolved by assumption in v3. 2027 depreciation is now budgeted from the new 'Depreciation Schedule' tab: straight-line, SlipLift 84 months, SlipTray 120 months, no salvage, full month from the go-live month. Existing fleet = PO Dec-26 run rate, carried flat. New units = DeploySum 2027 go-lives (rows 19/20). PO!R19:R22 set to 'Manual'. The open parts are logged separately: I-31 (Q4-26 go-lives), I-32 (existing-fleet run rates, SlipBot) and I-33 (peripherals). | 2027 depreciation 3,318,808 (2026 1,788,097): existing fleet 1,911,249, new 2027 go-lives 1,407,560. By GL: 5010 SlipBot 1,353,574; 5011 SlipLift 1,248,196; 5012 SlipCarrier (SlipTray) 418,898; 5020 Robot Peripherals 298,140. Python recompute from raw inputs vs workbook, all 48 GL-months: max diff 3.78e-10. | not determinable (component decisions in I-31..I-33) | impact not determinable; owner confirmation needed | PO owner/Finance to confirm the run-rate approach against the fixed-asset register, and resolve I-31..I-33. |
| I-08 | LOW | PO!U28; PO!Y28; PO!AD28; PO!U38; PO!U42 | Typed plugs are added onto the driver formula in 2027 month cells (+15,000, +5,000). They are not visible in the method columns R:T. | PO!U28 +5,000; PO!Y28 +5,000; PO!AD28 +5,000; PO!U38 +15,000; PO!U42 +15,000. Total plugs 45,000. | 45,000 | impact 45,000 | PO owner to move these amounts into a documented input (column S or a manual row), or remove them. |
| I-09 | LOW | PE!W74:AF74; PE!W76 | Typed numbers overwrite the driver formula in some 2027 months (manual overrides inside a formula row). | PE!W74=1,500, PE!X74=1,500, PE!Y74=2,000, PE!Z74=2,000, PE!AA74=2,500, PE!AB74=2,500, PE!AC74=3,000, PE!AD74=3,000, PE!AE74=3,500, PE!AF74=4,000, PE!W76=300. Total typed 25,800. | 25,800 | impact 25,800 | PE owner to confirm the overrides, or set the row method to Manual. |
| I-10 | MED | FO!AG58; FO!AG67; FO!AG91; FE!AG91; FO!AG116 | FO/FE lines with material 2026 spend have 2027 = 0, and FO Total Expense (SG&A) is 0 for 2027. Fld Maint Budget!A99 says: 'Not budgeted here: 6100 Travel and 7550 Tools ($0 by design – field travel books to 5050/5360, field tools to 5330); new-hire onboarding (covered by the $2K new-hire cost in Fld Ops Payroll B9). Out of scope: 5920, 7200, 8600.' | FO!AG58 5920 - Software - COGS: 2026 119,260 -> 2027 0; FO!AG67 6610 - Salaries and Wages - SG&A: 2026 50,575 -> 2027 0; FO!AG91 7200 - Contractors: 2026 59,734 -> 2027 0; FE!AG91 7200 - Contractors: 2026 154,857 -> 2027 0; FO!N116 217,242 -> AG116 0. 2026 total of these lines 384,425. | not determinable (2026 base 384,425) | impact not determinable; owner confirmation needed | SD owner to confirm whether these costs stop in 2027 or are budgeted elsewhere. |
| I-11 | MED | COO P&L!AG12; COO P&L!AG52; COO P&L!AG19; COO P&L!AG47 (+ variance table) | 98 rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k (v3 values; list below). | v3 values: 98 rows (v2: 98). Largest COO P&L GL moves: COO P&L!N12 6,363,078 -> AG12 15,563,646; COO P&L!N52 887,966 -> AG52 3,238,031; COO P&L!N47 319,694 -> AG47 1,554,365; COO P&L!N20 100,360 -> AG20 1,248,196. | not determinable | impact not determinable; owner confirmation needed | Each dept owner to comment on their rows in the variance table. |
| I-12 | MED | Fld Maint Budget!B8; Fld Maint Budget!B78:M78; FO!AG46 | Site setup kit cost is flagged as a placeholder (Fld Maint Budget!D8: 'PLACEHOLDER – update when the kit list is priced (Spare Parts, Tool Kits, 5S for'). It feeds FO 5330. | Fld Maint Budget!B8 = 4,500 $/new site; 'Site setup kits' 2027 (B78:M78) = 274,500. FO!N46 23,121 -> AG46 288,069. | not determinable (exposure 274,500) | impact not determinable; owner confirmation needed | SD owner to price the kit list and replace B8. |
| I-13 | MED | Fld Ops Payroll!M11; Fld Ops Payroll!B12; Fld Ops Payroll!M14 | Two Fld Ops Payroll drivers are marked 'Placeholder' in the author's notes: site techs per floater (M11) and the share of expansion go-lives needing a tech (B12). M11 currently has no effect because the floater switch M14 = 'No' (floater payroll 2027 = 0). B12 drives expansion-tech payroll. | M11 = 40, B12 = 0.6, M14 = 'No'. Expansion tech payroll 2027 (Fld Ops Payroll!F47:Q47) = 337,514. | not determinable (exposure 337,514) | impact not determinable; owner confirmation needed | SD owner to confirm or replace B12; M11 matters only if M14 is set to Yes. |
| I-14 | MED | Prod Payroll!M7; Prod Payroll!B9; Prod Payroll!A33; Fld Ops Payroll!B9; Old Draft!B142 (SD, not carried) | More placeholder inputs: Prod Payroll new-hire cost, current headcount and absence factors (no budget effect while Prod Payroll is broken), and the Fld Ops Payroll new-hire cost per tech, which hidden Old Draft!B142 says overlaps an onboarding line. | Fld Ops Payroll!B9 = 2,000; new-hire cost in FO 2027 (Fld Ops Payroll rows 34, 46, 59, 72, F:Q) = 138,000. Old Draft!B142: '7. Onboarding: 10 new hires Jan – Sep. The $2,000 Fld Ops Payroll placeholder (B9) overlaps this line; replace it with the actual cost here '. | not determinable (exposure 138,000) | impact not determinable; owner confirmation needed | SD owner to confirm B9 (and that onboarding is not also budgeted elsewhere). |
| I-15 | LOW | Fld Maint Budget!B12 (comment); Fld Maint Budget!B11; Fld Ops Payroll!H11; Fld Ops Payroll!E12 | The CONFIRM comment on Fld Maint Budget!B12 says Fld Ops Payroll shows 0 current supervisors; it now shows H11 = 1 ('Current supervisors counted toward ratio (Sep-26) – Isaiah'), and E12 says 'Ratio = domestic techs only. MeLi contract supervisor budgeted in Fld Maint Budget B11.'. The MeLi contract supervisor (5310) and the domestic manager (5510) are different people, so there is no double count; the comment is stale. | MeLi supervisor in 5310 2027 = 104,448 (Fld Maint Budget!B11 = 8,704/month x B12 = 1). Isaiah (Fld Ops Payroll row 77) 2027 = 120,900; incremental supervisors (row 73) 2027 = 193,632. | 0 | impact 0 | SD owner to confirm and delete the stale comment. |
| I-16 | LOW | Fld Maint T&E Data!M5:M388 (SD, hidden, not carried) | 101 T&E transactions are flagged 'Reclass needed' = Yes, totalling $27,804.02; booked GL differs from budget GL. 2 are tagged 'AI suggested' and 17 have tag basis 'Assumed'. If FO 2026 actuals were pulled on booked GL, these sit on the wrong 2026 lines; totals are unaffected, and no formula in the output reads this sheet. | Top booked->budget GL pairs: 5050->5360 x34, 6100->5360 x16, 5360->5050 x14, 7550->5330 x12, 6100->5050 x8. | 27,804 | impact 27,804 | Finance to post the reclasses (or confirm none are needed). |
| I-17 | HIGH | Logistics&WH Payroll!S51 (SD, not carried); PO!AG33:AG36 | The SD Logistics & Warehouse payroll model ('Warehouse and logistics team payroll that rolls up to Production Operations, sized from th...') totals 547,441 for 2027 but is referenced by 0 formulas in either book. PO 2027 production labour (rows 33-35) is typed with no link, so the workbook cannot show whether warehouse payroll is inside it. If it is not, PO 2027 is understated by up to 547,441. | Logistics&WH Payroll 2027 (F51:Q51) = 547,441: Base salaries 440,293; Payroll taxes 29,940; Benefits 72,208; New-hire cost 5,000; Dec-27 headcount 9. PO 2027: 5110 - Salaries and Wages - Production 525,310; 5130 - Payroll Taxes - Production 19,105; 5140 - Benefits - Production 108,404; Total - 5100 - Labor Expense - Production 652,820. Logistics&WH 2027 = 84% of PO 5100 total and 104% of PO 5110 salaries. PO 5350 Warehouse AG48 = 0; FO 5350 AG48 = 36,000 (Fld Maint Budget warehouse rent line). | up to 547,441 | impact 547,441 | PO owner to confirm whether PO 5110-5140 include the warehouse team. If not, link PO to this model (it would then need to be carried into the workbook). |
| I-18 | LOW | Fld Ops Payroll!B10; Fld Ops Payroll!B15; Fld Ops Payroll!B16 | The hiring horizon ends at Dec-27 (DeploySum row 54). Hires for Jan-28 go-lives use an Oct-Dec 27 average default rather than a forecast (documented by the author). | B10 = 1; B15 = =ROUND(AVERAGE(DeploySum!O54:Q54),0) = 7; B16 = =ROUND(AVERAGE(DeploySum!O57:Q57),0) = 2; cell notes on B10/B15/B16. | not determinable | hygiene | Overwrite B15/B16 if a 2028 go-live forecast exists. |
| I-19 | LOW | FE!U30:AF75 (rows 30-31, 67-69, 74-75); Fld Eng Budget rows 28-33, 85-91 | FE and Fld Eng Budget link in both directions: Fld Eng Budget reads FE 2026 columns, and FE 2027 rows read Fld Eng Budget. LibreOffice recalculated with no errors (no cell-level circularity), but the structure is easy to break. | Fld Eng Budget has 68 references to FE; FE has 84 references to Fld Eng Budget. | not determinable | hygiene | Check Fld Eng Budget before editing the FE 2026 columns it reads. |
| I-20 | LOW | SD sheets Prod Payroll, Old Draft, Fld Maint T&E Data (hidden); DeploySum!A41:A42 (hidden rows 41-42) | SD has 3 hidden sheets; Prod Payroll is carried and kept hidden, the others are not carried (FO/FE do not depend on them). DeploySum row visibility for rows 3-49 now follows the 9/30/26 file. | Hidden in output: ['Prod Payroll']. DeploySum hidden rows v2 [30, 32, 33, 34, 35, 36, 40, 41, 42] -> v3 [41, 42] (rows 30, 32-36 and recognized revenue row 40 are now visible, as in the 9/30/26 file). | not determinable | hygiene | None, unless reviewers want Old Draft / T&E Data in the pack. |
| I-21 | LOW | Fld Maint T&E Data!Q26 (SD) | Old Draft dependence is contained: 1 cell(s) outside Old Draft read it, none in the FO/FE chain, so the output has 0 references to it. | SD Fld Maint T&E Data: 1 cell(s) e.g. Q26: ='Old Draft'!B28*'Old Draft'!B23. SD dependency map: Old Draft -> {'Fld Maint T&E Data': 458, 'Fld Ops Payroll': 131, 'DeploySum': 112}. | not determinable | hygiene | None for the budget. Consider deleting Old Draft once the reference is re-pointed. |
| I-22 | LOW | COO P&L!A23:A24, B27, B37 (same rows on FO, PO, CO, FE, PE) | Rows 23 and 24 carry the same label ('5025 - Freight and Delivery - Production (Summary)'). Row 23 is an empty header; row 24 holds postings inside row 27 (=SUM(B24:B26)). Row 37 (=B19+B22+B27+B28+B29+B30+B31+B36+B20+B21) covers every direct child of its section, so nothing is skipped today, but anything typed on row 23 would be left out. | Subtotal scan on 6 sheets: 0 skipped lines with values. Non-empty cells on row 23 by tab: {COO P&L: 0, FO: 0, PO: 0, CO: 0, FE: 0, PE: 0}. COO P&L dept-sum formulas omitting a dept: 0. | not determinable | hygiene | Optionally relabel row 23 as a header, or lock it. |
| I-23 | LOW | COO P&L!B65:M65; COO P&L!C141 | COO P&L row 65 (labelled 'Expense') holds an unlabelled gross-margin % formula (=IFERROR(B64/B16,"")). With 2027 revenue now budgeted, it shows a 2027 margin (AG65 = 21.9%). Row 141 shows an extreme ratio for Feb-26 caused by negative 2026 payroll postings. | COO P&L!C141 = -14.33 (ratio). PO!N67 (308,059) -> AG67 0; PE!N35 (56,264) -> AG35 0. | not determinable | hygiene | Label row 65. Finance to explain the negative 2026 payroll postings in PO 6610 and PE 5140. |
| I-24 | LOW | Workbook defined names (xl/workbook.xml <definedNames>, workbook scope, no cell); list in 02-build_pruned_names_v2.csv | The COO book carries 14,310 legacy defined names from an old template. None is used by any formula, data validation, conditional format, chart or other name. v2 pruned the 5,345 unused names whose target is #REF! (5,330) or external-looking (15); 8,965 remain (string/array constants and plain values). | Before 14,310, after 8,965. Usage scan covered cell formulas, data validations, conditional formats, charts, print areas/titles and other names (counts in the notes file). Names referenced: 0 from parts, 0 from other names. Pruned names still referenced: 0. | not determinable | hygiene | Optional: purge the remaining constant-valued legacy names in Name Manager. |
| I-25 | LOW | Prod Payroll!B24:S81; DeploySum!A1 (notes) | Side effects of moving from Google Sheets to xlsx: threaded comments become plain notes (text kept); Google's '#ERROR!' has no Excel equivalent; LibreOffice saves error constants as '=#REF!' formulas. v3: DeploySum no longer has errors; Prod Payroll's remaining errors are now #NAME? (LibreOffice has no XLOOKUP), not #REF!. | Errors v2 -> v3: DeploySum {'#REF!': 463, '#N/A': 35} -> none; Prod Payroll {'#REF!': 796} -> {'#NAME?': 430}. New errors: 0. | not determinable | hygiene | None; disclosed for reviewers. |
| I-26 | MED | Fld Eng Budget!B21; Fld Eng Budget!B67:M67; FE!AG67 | 'Head of Service Delivery – Rasheen Henry' has no salary entered, so FE 6610 carries $0 for this current employee. The source note says: 'Source: user-provided. Current employee, in seat now. Enter annual salary in B21'. | Fld Eng Budget!B21 = None; row 67 2027 = 0; FE!AG67 = 713,347 excludes it. | not determinable (salary not in workbook) | impact not determinable; owner confirmation needed | SD owner to enter the salary in Fld Eng Budget!B21 (or confirm it is budgeted in another dept). |
| I-27 | LOW | Logistics&WH Payroll!B56 (SD, not carried); FO!U52:AF52 | Logistics&WH Payroll excludes MH-05 ('Less: MH-05 Material Handler, logistics support (counted on the FO tab)'), but FO 5510 2027 (FO!U52) sums only Fld Ops Payroll rows 21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77, none of which is an MH-05 seat; 'MH-05' appears nowhere outside Logistics&WH Payroll. So this seat is in neither model. | Logistics&WH Payroll!B56 = -38,133 (deduction of MH-05's 2027 base pay, before burden). FO!U52 = ='Fld Ops Payroll'!F21+'Fld Ops Payroll'!F31+'Fld Ops Payroll'!F43+'Fld Ops Payroll'!F56+'Fld Ops Payroll'!F69+'Fld Ops Payroll'!F76+'Fld Ops Payroll'!F77+'Fld Ops Payroll'!F34+'Fld Ops Payroll'!F46+'Fld Ops Payroll'!F59+'Fld Ops Payroll'!F72. MH-05 mentions elsewhere: none. | 38,133 base pay missing (before burden) | impact 38,133 | SD/PO owners to decide where MH-05 is budgeted and add it. |
| I-28 | MED | CO!AG67:AG69; PE!AG67:AG69; FE!AG67:AG69; Fld Eng Budget!A13:A21 | SG&A payroll (6610/6630/6640) is non-zero on CO, FE and PE. FE is built from a named roster on Fld Eng Budget; CO and PE are typed monthly amounts with no roster, so the workbook cannot confirm that no person on the FE roster is also inside CO or PE. | row 67: CO 528,452, FE 713,347, PE 1,078,020; row 68: CO 27,593, FE 48,508, PE 38,501; row 69: CO 62,916, FE 116,989, PE 95,116. 2027 months typed (no formula): CO yes, PE yes, FE no (formulas). FE roster: Fld Eng Budget!A13:A21. | not determinable (no CO/PE roster) | impact not determinable; owner confirmation needed | CO and PE owners to confirm their SG&A payroll rosters exclude the people on Fld Eng Budget!A13:A21. |
| I-29 | LOW | Prod Payroll!M9; Fld Ops Payroll!M7; Fld Eng Budget!B59 (row formula); PO!AD33; PO!AD34; PO!AD35; CO!AD67; CO!AD68; CO!AD69; PE!AD67; PE!AD68; PE!AD69 | Raise timing is consistent (same % and month everywhere), but the eligibility rule is not: Fld Ops Payroll and Logistics&WH Payroll exclude staff hired in the months before the raise (Prod Payroll!M9), while Fld Eng Budget and the typed PO/CO/PE payroll rows apply the raise to the whole row. | Prod Payroll!M5 = 0.03, M6 = 2027-10-01, M9 = 6. Steps found in typed rows: PO!AD33 3.00%; PO!AD34 3.00%; PO!AD35 3.00%; CO!AD67 3.00%; CO!AD68 3.00%; CO!AD69 3.00%; PE!AD67 3.00%; PE!AD68 3.00%; PE!AD69 3.00%; FE!AD67 3.00%; FE!AD68 3.00%; FE!AD69 3.00%. | not determinable | hygiene | Payroll owners to confirm whether the eligibility rule should apply to all departments. |
| I-30 | LOW | DeploySum!A2, A7, A9, A11, A13, A29, A30, A35, A38, A39, A40, A41, A42 | The source labels say '$000s', but the values are whole dollars. v3 relabelled the 13 cells to '$' (A2 text: 'Dollars in $ (relabelled in v3; the source said $000s)'). Each cell has a comment quoting the original label, so the change is visible, not silent. | E.g. DeploySum!R13 total bookings 29,452,766 and R29 Production CapEx 32,410,900 are dollars: CapEx = units x unit cost in dollars (section 'Unit-cost reconciliation'), and recognized revenue is the same order as PO's 2026 revenue in dollars. | 0 | hygiene | Plan owner to fix the labels in the source (Revenue Roll-up / Deploy) so the next export is right. |
| I-31 | LOW | 'Depreciation Schedule'!A88:D97; PO!J20:M22; DeploySum!C19:E20 | Oct-Dec 26 go-lives are carried in the PO Dec-26 run rate (not added explicitly, so there is no double count). The PO forecast steps up for Q4-26 go-lives, but by fewer units than the 9/30/26 DeploySum: it covers 15 lifts and 53 trays, against DeploySum's 18 lifts and 67 trays. The 5020 step-ups cannot be reproduced from DeploySum's peripheral cost. | PO 5011 monthly step-ups Oct/Nov/Dec: 6,964.29, 2,321.43, 2,321.43 = 9, 3, 3 lifts x 65,000/84. 5012: 1,933.33, 800.00, 800.00 = 29, 12, 12 trays x 8,000/120. 5020: 2,608.33, 1,025.00, 1,025.00 = 52.95, 20.81, 20.81 peripheral sets at 4,137.50/84 (not whole). DeploySum Oct/Nov/Dec lifts [9, 9, 0], trays [35, 32, 0]. Gap not budgeted: 3 lifts + 14 trays = 3,254.76/month, 39,057 for 2027 (plus up to 10,639 if Q4-26 lift peripherals are not in 5020). | 39,057 (up to 49,696 with peripherals) | impact 39,057 | User/PO owner to choose: keep the PO run rate (current), or replace the Q4-26 step-ups with DeploySum's Oct-Dec 26 go-lives (Sep-26 run rate + explicit vintages). Do not do both. |
| I-32 | HIGH | 'Depreciation Schedule'!B21:B24; PO!M19:M22; PO!U19:AF19 | Existing-fleet depreciation is carried flat at the PO Dec-26 run rate for all 12 months of 2027, as the handoff instructed. The workbook has no asset register, so it cannot show whether any of these assets reach the end of their life, or are retired, in 2027. The largest line is 5010 SlipBot: 112,797.85/month = 1,353,574 in 2027. Whether the SlipBot fleet is fully depreciated, retired or ongoing is not in the files. DeploySum note 4 says no SlipBots are built and existing bots are redeployed, which suggests the fleet is in use. 5020's run rate basis is also unknown (I-31). | Dec-26 run rates (PO!M): 5010 112,797.85, 5011 20,444.90, 5012 6,502.64, 5020 19,525.33; 2027 existing total 1,911,249. 5010 2026 actuals Jan-Aug 141,122.35 -> 127,510.00, forecast Sep-Dec flat 112,797.85; 2026 total 1,492,329. | up to 1,353,574 (5010); 1,911,249 all existing lines | impact 1,353,574 | USER DECISION: confirm SlipBot fleet status (fully depreciated / retired / ongoing) and the end-of-life month for any existing asset group. Change the section 2 input on the schedule if the run rate stops. |
| I-33 | MED | 'Depreciation Schedule'!B7, B11, B16; PO!U22:AF22 | SlipLift peripherals (4,137.50 per lift, from DeploySum CapEx) are depreciated on 5020 Robot Peripherals over 84 months. Both the GL and the life are builder assumptions: the user gave lives for SlipLifts and SlipTrays only. 5020 was chosen because PO's 2026 forecast books 5011 at exactly $65,000/84 per lift, so PO keeps peripherals out of 5011. | 2027 new-peripheral depreciation 63,836 (Dec-27 12,313.99/month). Moving it to 5011 changes the GL split only, not the total. A different life changes the amount in proportion (e.g. 60 months: 89,370). | 63,836 | impact 63,836 | User to confirm the peripherals GL (5020 or 5011) and life; both are input cells. |

### Variance scan: rows with |AG-N| > $50k and > 50% (v3 values)

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
| PO | 12 | 4100 - Subscription/Platform Fees | 6,363,078 | 15,563,646 | 9,200,567 | 145% |
| PO | 13 | 4500 - Implementation Fees | 85,861 | 0 | (85,861) | -100% |
| PO | 14 | Total - 4000 - Sales | 6,448,940 | 15,563,646 | 9,114,706 | 141% |
| PO | 15 | 4900 - One-Time Revenue | 975,000 | 0 | (975,000) | -100% |
| PO | 16 | Total - Income | 7,423,940 | 15,563,646 | 8,139,706 | 110% |
| PO | 20 | 5011 - SlipLift Depreciation | 100,360 | 1,248,196 | 1,147,836 | 1144% |
| PO | 21 | 5012 - SlipCarrier Depreciation | 36,993 | 418,898 | 381,906 | 1032% |
| PO | 22 | 5020 - Robot Peripherals Depreciation | 158,415 | 298,140 | 139,724 | 88% |
| PO | 27 | Total - 5025 - Freight and Delivery - Production (Summary) | 57,197 | 0 | (57,197) | -100% |
| PO | 33 | 5110 - Salaries and Wages - Production | 137,080 | 525,310 | 388,230 | 283% |
| PO | 35 | 5140 - Benefits - Production | 54,271 | 108,404 | 54,133 | 100% |
| PO | 36 | Total - 5100 - Labor Expense - Production | 197,323 | 652,820 | 455,497 | 231% |
| PO | 37 | Total - 5000 - Robot Production and Deployment | 2,111,917 | 4,059,482 | 1,947,565 | 92% |
| PO | 38 | 5015 - Supplies and Materials | 2,839 | 101,250 | 98,411 | 3467% |
| PO | 42 | 5201 - Inventory Adjustments | 22,000 | 75,000 | 53,000 | 241% |
| PO | 63 | Total - Cost Of Sales | 2,361,338 | 4,415,704 | 2,054,365 | 87% |
| PO | 64 | Gross Profit | 5,062,601 | 11,147,942 | 6,085,341 | 120% |
| PO | 67 | 6610 - Salaries and Wages - SG&A | (308,059) | 0 | 308,059 | 100% |
| PO | 73 | Total - 6000 - Labor Expense - SG&A | (309,871) | 0 | 309,871 | 100% |
| PO | 98 | 7700 - Inventory Obsolescence-old | 636,000 | 0 | (636,000) | -100% |
| PO | 116 | Total - Expense | 461,703 | 171,650 | (290,053) | -63% |
| PO | 117 | Net Ordinary Income | 4,600,898 | 10,976,292 | 6,375,394 | 139% |
| PO | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| PO | 132 | Net Income | 4,685,709 | 10,976,292 | 6,290,582 | 134% |
| PO | 137 | Salaries and Wages | (159,704) | 525,310 | 685,014 | 429% |
| PO | 140 | Benefits | 51,491 | 108,404 | 56,914 | 111% |
| FE | 30 | 5050 - Travel - Deployment | 87,455 | 346,633 | 259,178 | 296% |
| FE | 37 | Total - 5000 - Robot Production and Deployment | 99,214 | 388,814 | 289,600 | 292% |
| FE | 63 | Total - Cost Of Sales | 115,989 | 388,814 | 272,825 | 235% |
| FE | 64 | Gross Profit | (115,989) | (388,814) | (272,825) | -235% |
| FE | 91 | 7200 - Contractors | 154,857 | 0 | (154,857) | -100% |
| PE | 33 | 5110 - Salaries and Wages - Production | 65,377 | 0 | (65,377) | -100% |
| PE | 35 | 5140 - Benefits - Production | (56,264) | 0 | 56,264 | 100% |
| COO P&L | 12 | 4100 - Subscription/Platform Fees | 6,363,078 | 15,563,646 | 9,200,567 | 145% |
| COO P&L | 13 | 4500 - Implementation Fees | 85,861 | 0 | (85,861) | -100% |
| COO P&L | 14 | Total - 4000 - Sales | 6,448,940 | 15,563,646 | 9,114,706 | 141% |
| COO P&L | 15 | 4900 - One-Time Revenue | 975,000 | 0 | (975,000) | -100% |
| COO P&L | 16 | Total - Income | 7,423,940 | 15,563,646 | 8,139,706 | 110% |
| COO P&L | 20 | 5011 - SlipLift Depreciation | 100,360 | 1,248,196 | 1,147,836 | 1144% |
| COO P&L | 21 | 5012 - SlipCarrier Depreciation | 36,993 | 418,898 | 381,906 | 1032% |
| COO P&L | 22 | 5020 - Robot Peripherals Depreciation | 158,415 | 298,140 | 139,724 | 88% |
| COO P&L | 24 | 5025 - Freight and Delivery - Production (Summary) | 50,108 | 0 | (50,108) | -100% |
| COO P&L | 27 | Total - 5025 - Freight and Delivery - Production (Summary) | 62,008 | 0 | (62,008) | -100% |
| COO P&L | 29 | 5040 - Freight & Delivery - Deployment | 85,214 | 765,000 | 679,786 | 798% |
| COO P&L | 30 | 5050 - Travel - Deployment | 94,810 | 392,987 | 298,177 | 314% |
| COO P&L | 33 | 5110 - Salaries and Wages - Production | 202,457 | 525,310 | 322,853 | 159% |
| COO P&L | 35 | 5140 - Benefits - Production | (1,993) | 108,404 | 110,397 | 5540% |
| COO P&L | 36 | Total - 5100 - Labor Expense - Production | 208,574 | 652,820 | 444,246 | 213% |
| COO P&L | 37 | Total - 5000 - Robot Production and Deployment | 2,305,147 | 5,259,650 | 2,954,503 | 128% |
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
| COO P&L | 63 | Total - Cost Of Sales | 4,478,016 | 12,152,017 | 7,674,002 | 171% |
| COO P&L | 91 | 7200 - Contractors | 214,591 | 0 | (214,591) | -100% |
| COO P&L | 98 | 7700 - Inventory Obsolescence-old | 636,000 | 0 | (636,000) | -100% |
| COO P&L | 106 | 8600 - Repairs and Maintenance | 51,212 | 0 | (51,212) | -100% |
| COO P&L | 117 | Net Ordinary Income | (984,033) | 393,486 | 1,377,519 | 140% |
| COO P&L | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| COO P&L | 132 | Net Income | (899,222) | 393,486 | 1,292,708 | 144% |
| COO P&L | 137 | Salaries and Wages | 3,264,812 | 6,083,161 | 2,818,348 | 86% |
| COO P&L | 139 | Payroll Taxes | 210,079 | 344,509 | 134,430 | 64% |
| COO P&L | 140 | Benefits | 471,094 | 891,831 | 420,737 | 89% |

## Carried from v2 (still valid: FO, FE, CO, PE and PO payroll unchanged)

### Cross-department overlap (from v2)

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

## Decisions

- D1 (v3): Built v3 from the delivered v2 workbook (openpyxl edit + LibreOffice recalc), not from the original inputs again. v2 is reproducible with run_build_v2.sh, so the chain is reproducible. This keeps every v2 cell, comment, name and format that v3 does not touch.
- D2 (v3): DeploySum row map by label: rows 1-38 same, 39-49 -> +1; the SD ARR row 39 is kept empty (brief v2 item 1). Internal formulas copied (88, identical to v2's after mapping); '[1]' formulas stored as cached values and listed on Collation Notes.
- D3 (v3): Peripherals cost = 4,137.50, derived from DeploySum CapEx, rather than the note's rounded '$4,138'. It reconciles every month to $0.00. The note's figure leaves a $0.50/lift residual.
- D4 (v3): Peripherals go to 5020 with the SlipLift life. Both are inputs and flagged for the user (I-33).
- D5 (v3): Oct-Dec 26 go-lives: rely on the PO Dec-26 run rate, never both; gap shown as memo (I-31).
- D6 (v3): Existing-fleet run rates are links (=PO!M19:M22), so they trace to the PO 2026 forecast; carried flat (I-32).
- D7 (v3): PO!R12 and R19:R22 set to 'Manual' (allowed by the row's data validation) so the method column matches the linked rows; notes in column AI.
- D8 (v3): DeploySum row visibility follows the 9/30/26 file; recognized revenue row 40 is visible because it now feeds PO.
- D9 (v3): '$000s' labels relabelled to '$' with a comment on each cell (flagged, not silent; I-30).
- D10 (v3): v2 -> v3 value comparison treats numeric differences <= 1e-6 as recalculation noise (counted and shown). All are below 1.1e-9.
- D11 (v3): Severity scale and tie-break rule unchanged from v2. The full-month convention is a brief decision, so it sits in the register with its sensitivity, not in the issues list.
- Carried from v2: D1-D9 of v2 still apply to the parts v3 did not touch.

## Not done / limits

- The external workbook '[1]' is still not available: DeploySum holds the 9/30/26 cached values, not live links.
- No fixed-asset register was supplied, so existing-fleet depreciation is a run rate, not an asset-by-asset schedule. End-of-life dates are unknown (I-32).
- Not opened in Microsoft Excel. Prod Payroll's XLOOKUP rows show #NAME? in LibreOffice 24.2 and may evaluate in Excel (untested).
- No change made to FO, FE, CO, PE, or to PO lines other than 12 and 19-22 (and their subtotals/ratios). 4500/4900 stay 0 by assumption.
- v2 limits on page setup, sheet-scoped names and Google-specific parts still apply.
