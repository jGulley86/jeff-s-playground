# 02-build notes v5 - 2027 COO budget collation

## Decisions pending

Four user decisions are open. The builder has not resolved them; the budget carries the 'current treatment' column. Effects are on the 2027 COO contribution, each on its own.

| # | Decision (user) | Issue | Current treatment in the budget | Alternatives: effect on 2027 COO contribution (+ raises, ( ) lowers) | Who |
|---|---|---|---|---|---|
| 1 | SlipBot fleet status (5010 depreciation) | I-32 | Carried flat at the PO Dec-26 run rate 112,797.85/month = 1,353,574 in 2027 (builder assumption, A-17). | Fully depreciated or retired from Jan-27: +1,353,574. Continue the 2026 decline ((3,541)/month, Jan-Sep 26) from the Sep-26 level in Jan-27: +276,164 (actuals Jan-Aug only, (1,945)/month: +151,680). Same decline also running through Oct-Dec 26, floored at 0: +403,624 (actuals-only slope: +221,687). Ongoing at the run rate: 0. Related: the 5020 base of 8,212/month (Jan-26, before any SlipLift depreciation) may end with the SlipBots: up to +98,543. | User, with PO/Finance (fixed-asset register) |
| 2 | Q4-26 go-lives: PO run rate or DeploySum | I-31 | Inside the PO Dec-26 run rate: PO steps up for 15 lifts / 53 trays (DeploySum: 18 / 67). | Sep-26 run rate + DeploySum Oct-Dec 26 vintages: (39,057). If PO's Dec-26 step-up (3 lifts, 12 trays) is Jan-27 units already in the Jan-27 vintage and PO's Oct/Nov counts are right: +37,457. Keep as is: 0. | User, after the PO owner says what the Q4-26 step-ups are |
| 3 | SlipLift peripherals: GL and useful life | I-33 | 5020 Robot Peripherals, 84 months: 63,836 of 2027 depreciation (builder assumption, A-10/A-11). | GL 5011 instead of 5020: 0 (moves 63,836 from PO row 22 to row 20). Life 60 months: (25,534). Life 120 months: +19,151. | User |
| 4 | Revenue split across 4100 / 4500 / 4900 | I-01 (A-02, A-03) | All 15,563,646 of plan revenue on 4100; 4500 and 4900 = 0 (orchestrator assumption). | Split the plan revenue across the three lines: 0 (classification only; gross margin unchanged). Budget implementation / one-time revenue in addition to the plan: not determinable (2026 4500 + 4900: 1,060,861). | User / Finance |

v5 enters one user-confirmed input: the Head of Service Delivery's annual salary, 205,000, in Fld Eng Budget!B21 (resolves I-26). Everything else that moved is downstream recalculation. The 2027 COO contribution falls from 393,486 (v4) to **139,032** ((254,454)). Diff vs v4: 1 input cell, 425 downstream value changes, 0 changes outside the downstream set, 0 formula changes; see 'v4 -> v5 diff'.

## Headline: 2027 COO contribution

| Line | COO P&L row | 2026 (N) | 2027 v5 (AG) | Change | % | 2027 v4 (AG) | v5 - v4 |
|---|---|---:|---:|---:|---:|---:|---:|
| Revenue (company recognized revenue, 9/30/26 sales plan) | 16 | 7,423,940 | 15,563,646 | 8,139,706 | 110% | 15,563,646 | 0 |
| COGS (COO departments) | 63 | 4,478,016 | 12,152,017 | 7,674,002 | 171% | 12,152,017 | 0 |
|   of which depreciation (in COGS) | 19-22 | 1,788,097 | 3,318,808 | 1,530,712 | 86% | 3,318,808 | 0 |
| Gross Profit | 64 | 2,945,924 | 3,411,628 | 465,704 | 16% | 3,411,628 | 0 |
| Opex (COO departments) | 116 | 3,929,957 | 3,272,597 | (657,361) | -17% | 3,018,142 | 254,454 |
| COO contribution before other income (workbook label 'Net Ordinary Income') | 117 | (984,033) | 139,032 | 1,123,065 | n/m | 393,486 | (254,454) |
| Net Other Income | 131 | 84,811 | 0 | (84,811) | -100% | 0 | 0 |
| **COO contribution** (workbook label 'Net Income') | 132 | (899,222) | 139,032 | 1,038,254 | n/m | 393,486 | (254,454) |

- **2027 COO contribution (COO P&L AG132): 139,032** vs 2026 (899,222). Change 1,038,254; % n/m (2026 base negative). It includes 2027 plan revenue of 15,563,646 (all to 4100, orchestrator assumption) and depreciation of 3,318,808. v4: 393,486.
- Cost-only view: total COO cost (COGS + Opex, AG63 + AG116) 15,424,614 vs 2026 8,407,973 (change 7,016,641, 83%). Excluding depreciation: 12,105,806 vs 2026 6,619,876.
- 2027 gross margin 21.9% (unchanged: the new cost is Opex). '%' is 'n/m' where the 2026 base is zero or negative or the sign flips: COO contribution before other income (workbook label 'Net Ordinary Income'); COO contribution (workbook label 'Net Income').
- Issues: 3 HIGH, 10 MED, 19 LOW open; 1 RESOLVED (I-26, v5).

### Caveats on the headline (read before using the figure)

(1) What the figure is. The bottom line, 139,032, is a **COO contribution**: the company's recognized revenue (15,563,646, all of it) less the costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: 15,424,614). Costs outside COO (for example sales, G&A, R&D) are not in this workbook, so it is **not company Net Income**. The workbook row keeps its GL label 'Net Income' (COO P&L!A132) because v4 and v5 change no label on the P&L tabs; the notes and Collation Notes call it 'COO contribution'.

(2) What the revenue is. 2027 revenue is the 9/30/26 sales plan's recognized revenue (DeploySum row 40, static cached values, A-24), not signed contracts. It includes unsigned and forecast bookings: Sep-Dec 26 bookings of 3,544,300 include 2,264,000 of unsigned forecast at 100% (DeploySum note 5, A49: bookings are gross ACV), and all 29,452,766 of FY27 bookings are forecast (new logos 24,016,000, expansion 5,436,766). 7,618,410 (49%) of 2027 revenue is above the Dec-26 exit rate x 12 (7,945,236), so it depends on go-lives that have not happened yet.

(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. Items can overlap (I-05 and I-17 both concern production payroll), so do not add them without the owners' answers.

| Item | Direction | What could happen | Effect on 2027 COO contribution | Contribution after this item alone | Source cells |
|---|---|---|---:|---:|---|
| I-17 | downside | Logistics & warehouse payroll (SD model) is not in PO 5100; if PO's typed production payroll excludes the warehouse team, PO is understated. | (547,441) | (408,409) | SD Logistics&WH Payroll!S47 (not carried) |
| I-05 | downside | Production payroll model 'Total lift payroll' 1,622,423 vs PO 5100 typed 652,820; gap if the model is right (lift payroll only; tray and supervisor rows do not compute in LibreOffice). May overlap I-17. | (969,603) | (830,571) | Prod Payroll!S41; PO!AG36 |
| I-10 | downside | FO/FE lines with 2026 spend budgeted at 0 for 2027 (5920 software, 6610 SG&A salaries, 7200 contractors); effect if they continue at the 2026 level. | (384,425) | (245,393) | FO!N58, N67, N91; FE!N91 (AG = 0) |
| I-26 | RESOLVED | RESOLVED (user-confirmed 2026-10-09): Head of Service Delivery salary 205,000/year entered in v5 and now inside the headline (2027 cost 254,454: salary 206,538 + payroll tax 14,045 + benefits 33,872; v4 contribution was 393,486). No remaining exposure. | 0 (now in the headline) | 139,032 | Fld Eng Budget!B21 = 205,000 |
| I-31 | two-way | Shortfall if DeploySum's Q4-26 go-lives are right (3 lifts, 14 trays more than PO's run rate). | (39,057) | 99,975 | PO!J20:M21; DeploySum!C19:E20 |
| I-31 | two-way | Double count if PO's Dec-26 step-up (3 lifts, 12 trays; DeploySum Dec-26 go-lives 0) is Jan-27 units (20 lifts, 60 trays go live Jan-27, built Nov-26). Excludes the 5020 Dec step (+12,300 more if it is the same units). | +37,457 | 176,489 | PO!L20:M21; DeploySum!E19:F20 |
| I-32 | upside | SlipBot fleet fully depreciated or retired from Jan-27 (5010 = 0). | +1,353,574 | 1,492,606 | PO!M19; 'Depreciation Schedule'!B21 |
| I-32 | upside | Trend alternative: 5010 keeps falling at the 2026 rate (141,122 Jan-26 -> 112,798 Sep-26, (3,541)/month). | +276,164 | 415,196 | PO!B19, J19, M19 |
| I-32 | upside | Trend alternative continued from Sep-26: the same (3,541)/month decline also runs through Oct-Dec 26, so Jan-27 starts 4 months below Sep-26 (98,636 in Jan-27, 59,689 in Dec-27; floored at 0, 0 months at the floor). | +403,624 | 542,656 | PO!B19, J19, M19 |
| I-33 | two-way | Peripherals life 60 months instead of 84 (a longer life, e.g. 120 months, gives the opposite sign). | (25,534) | 113,498 | 'Depreciation Schedule'!B11 |
| A-14 | upside | Depreciation convention: mid-month in the go-live month instead of a full month. | +137,417 | 276,448 | 'Depreciation Schedule'!B13 |
| A-14 | upside | Depreciation convention: start the month after go-live. | +274,833 | 413,865 | 'Depreciation Schedule'!B13 = 1 |
| A-22 | downside | Revenue rests on unsigned / forecast bookings (Sep-Dec 26 includes 2,264,000 unsigned at 100%). Revenue effect not determinable from the workbook. | n/d | n/d | DeploySum!A49 (note 5), row 40 |

**Sign-flip statement (computed from the table):** The 2027 COO contribution of 139,032 changes sign on I-05 alone (139,032 - 969,603 = (830,571)) or I-17 alone (139,032 - 547,441 = (408,409)) or I-10 alone (139,032 - 384,425 = (245,393)). I-31 alone leaves 99,975. Together, I-17 + I-05 take it to (1,378,013) (if they do not overlap; the PO owner must say). I-10 with the I-31 shortfall gives (284,450). All quantified downsides together (I-17, I-05, I-10, I-31 shortfall): (1,801,495). Upside: I-32 can add up to 1,353,574 (contribution 1,492,606); the trend alternative adds 276,164 (415,196), or 403,624 (542,656) if the decline also ran through Oct-Dec 26. With costs held fixed, revenue 139,032 (0.9%) below plan also takes the contribution to zero. Conclusion: the sign of the 2027 COO contribution is not established by this budget. Treat 139,032 as a point estimate inside a range from (1,801,495) to 1,492,606 (illustrative extremes of quantified items; excludes I-02, A-22; lower end assumes no I-05/I-17 overlap; lower end = all four quantified downsides added: I-17, I-05, I-10, I-31 shortfall; upper end = I-32 full only, the other upsides A-14, I-31 double count and I-33 are not added) until I-17, I-05 and I-32 are answered.

## Changes from v4

| Item | Point | What v5 did | Where |
|---|---|---|---|
| I-26 | Head of Service Delivery salary (user-confirmed 2026-10-09) | Fld Eng Budget!B21 = 205,000. Existing row-67 mechanics apply (full year from 2027-01-01, +3% from 2027-10-01, tax 6.8%, benefits 16.4%): FE 6610 +206,538, 6630 +14,045, 6640 +33,872; COO contribution 393,486 -> 139,032 ((254,454)). I-26 marked RESOLVED. | Fld Eng Budget!B21; FE / COO P&L rows 67-69 and subtotals (recalculated); I-26; caveat table; Headline |
| Recalc | Downstream values | 425 cached values recalculated, all downstream of B21 by static trace (COO P&L 159, FE 137, Fld Eng Budget 129); 0 formulas changed. | v4 -> v5 diff |
| Sign flip | Recomputed on the new contribution | v4: 393,486 flipped on I-05 or I-17 alone; range (1,547,040) to 1,747,060. v5: 139,032 flips on I-05 or I-17 or I-10 alone; range (1,801,495) to 1,492,606. | Sign-flip statement |
| N1 | Depreciation Schedule tab text conflicts with A-17/A-19 and I-31 | Collation Notes line added: the tab text at B17 (with D17), D21 and the row 19 heading is superseded by A-17, A-18, A-19 and I-31. Tab text not edited (only B21 may change in v5). | Collation Notes 'Workbook text superseded'; Depreciation schedule summary |
| N2 | Sign-flip range is illustrative | Range labelled 'illustrative extremes of quantified items; excludes I-02, A-22; lower end assumes no I-05/I-17 overlap', with what each end includes. | Sign-flip statement (md and Collation Notes) |
| N3 | I-32 trend understated if the decline ran through Oct-Dec 26 | New case: decline continued from Sep-26, floored at 0: +403,624 (vs +276,164 starting from the Sep-26 level in Jan-27; actuals-only slope +221,687). | Caveat table; Decisions pending #1; I-32; A-17 |
| Carried tables | Recomputed from the v5 workbook | Variance scan: 2 rows added, 5 changed, 0 removed; cross-department overlap: 6 rows changed; raise-step table: 3 rows changed; I-02 and I-28 FE amounts refreshed. Each generator reproduces the v4 table exactly from v4 first. | Variance scan; Cross-department checks; I-02; I-28 |

No critic v4 item was declined. N1 is handled by a superseding note rather than by editing the tab text, because the v5 brief allows only Fld Eng Budget!B21 to change. v4's own changes from v3 (critic v3 B1, O1-O8) are listed in `02-build_notes_v4.md` and still apply.

## Head of Service Delivery salary (I-26, resolved in v5)

- Input: Fld Eng Budget!B21 = 205,000 (annual salary, user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). This is the only typed input that changed; no formula, label or other cell was edited.
- How the model treats it: row 67 uses the same formula as the other roster rows (=IF(B$58>=$C$21,$B$21/12*(1+IF(B$58>=$B$25,$B$24,0)),0)). Start month C21 = 2027-01-01, so all 12 months of 2027 are paid: 17,083.33/month Jan-Sep, then +3% (Fld Eng Budget!B24 = Fld Ops Payroll M5 = Prod Payroll M5) from 2027-10-01 (B25 = Fld Ops Payroll M6 = Prod Payroll M6) = 17,595.83/month for 3 months. No raise-eligibility test applies on this tab (I-29); the salary is treated as the Dec-26 rate.
- Burden: payroll taxes 6.8% (B22 = Fld Ops Payroll B7) and benefits 16.4% (B23 = Fld Ops Payroll B8), applied to the salary rows total (rows 69-70).
- 2027 cost of the role: salary 206,538 + payroll tax 14,045 + benefits 33,872 = 254,454.
- FE 2027 (AG): 6610 713,347 -> 919,884 (+206,538); 6630 48,508 -> 62,552 (+14,045); 6640 116,989 -> 150,861 (+33,872). FE Total - Expense 931,334 -> 1,185,788. COO P&L rows 67-69 move by the same amounts.
- 2027 COO contribution (COO P&L AG132): 393,486 (v4) -> 139,032 (v5), (254,454). 2026 FE 6610 was 850,615; FE 6610 2027 is now 919,884 (8% vs 2026; v4 -16%).

## Build and sources

Output: `02-build/02-build_COO_2027_Budget_Collated_v5.xlsx` (v1-v4 files unchanged)  
Scripts: `02-build/scripts/` - v5 entry point `run_build_v5.sh`: build_v5.py (stage 1: v4 package with only B21 set) -> recalc.sh (LibreOffice full recalculation of stage 1) -> deps_v5.py (static trace of every formula downstream of B21) -> patches_v5.py (recalculated values of downstream cells that changed; anything that changed outside the trace stops the build) -> build_v5.py (stage 2: v4 package + B21 + those cached values) -> figures_v5.py -> report_v5.py -> build_v5.py (final, with Collation Notes) -> diff_versions.py, recalc.sh and analyze_v5.py (checks). Every zip part other than the three patched sheets and Collation Notes is copied byte for byte from v4. `run_build_v4.sh` ... `run_build.sh` still reproduce v4 ... v1.  
Inputs (read-only): `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `a3264ef4305e1e7da7c8cf7efbcd5407556aba56e85d50375f9ece711199e9b4`; `Service_Delivery_PL_worksheets.xlsx` sha256 `fedee8d16eb7db72d2745e77a7c6441057b4229131c52d25c944dbb5b858a466`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `645e31303dcbbbd6279152aeaa8e5e61dffa0984f1f6116d671408011166fceb`; user answer 2026-10-09 (B21).  
Reviews: critic `03-review/03-review_critic_v4.md` (N1-N3); verifier `04-verify/04-verify_report_v3.md` (v3 PASS).  
Recalculation engine: LibreOffice 24.2.7.2 420(Build:2) (used to compute the downstream values and to check the result).

## Completion criteria (v5)

| Criterion | Result |
|---|---|
| Only input diff is Fld Eng Budget!B21 = 205,000 | Input (non-formula) cells changed: 1 (Fld Eng Budget!B21). Formulas changed: 0 (diff_versions.py reports 1 'formula diff' because it compares cell contents and B21 went from empty to a typed number). Comments changed: 0 / 0 / 0. |
| Value changes only downstream of B21 | 425 value diffs, all in the static downstream set ({'COO P&L': 159, 'FE': 137, 'Fld Eng Budget': 129}); outside the set: 0. Recalc noise left at v4 values outside the set: 40 cells, max 9.9e-08 (< 1e-6, not a change). |
| Cached values are what the formulas give | LibreOffice recalculation of v5 vs its stored values, every sheet except Collation Notes: 40 cells differ, max 9.9e-08; non-numeric mismatches 0. |
| COO P&L = sum of the departments | 2,936 COO P&L cells checked (rows 12 onward, columns B:N and U:AG, ratio rows and columns excluded): max |COO - (FO+PO+CO+FE+PE)| 4.9e-08; failures 0. |
| 0 new errors | New errors vs v4: 0. |
| I-26 shows RESOLVED | Issues table Sev = RESOLVED; caveat table row 'RESOLVED'; Collation Notes text check: True. |
| N1-N3 addressed | N1 line on Collation Notes: True; N2 range label: True; N3 trend case: True. |
| Collation Notes live formulas | 32 formulas; LibreOffice recalc vs stored values: max diff 3.9e-08, text mismatches 0. |
| Figures recompute from the final file | figures_v5.py on the final v5 = on stage 2: True. |
| No stale v4 numbers | v4 values of every recalculated cell and every changed figure (>= 1,000) searched in this file outside 'Changes from v4' and 'Head of Service Delivery salary': 0 hits (148 numbers checked). |

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

**Treatment: rely on the run rate (builder decision; two-way risk, I-31).** Oct-Dec 26 go-lives are not added explicitly. Why: the run rate is PO's own forecast and already contains Q4-26 step-ups priced like the schedule; adding DeploySum's Q4 units on top would count the 15 lifts and 53 trays already in it twice. The risk runs both ways. If DeploySum's Q4 counts are right, the run rate is short 3 lifts / 14 trays (39,057 for 2027; memo in schedule section 5). If PO's Dec-26 step-up (3 lifts, 12 trays; DeploySum has no Dec-26 go-lives) is units that DeploySum places in Jan-27, they are also in the Jan-27 vintage: 37,457 counted twice. PO owner to confirm; user decision (Decisions pending #2).

**SlipBot 5010:** carried at the Dec-26 run rate 112,797.85/month = 1,353,574 for 2027 (2026: 1,492,329). The flat carry is a builder assumption (A-17), not evidence that the fleet is still depreciating. 5010 fell through 2026 ((3,541)/month Jan-Sep); continuing that trend would lower 2027 by 276,164, or by 403,624 if the decline also ran through Oct-Dec 26 (floored at 0). Fleet status is unknown: **user to confirm** whether it is fully depreciated, retired or ongoing (I-32).

Depreciation Schedule tab text superseded (critic v4 N1): the explanatory text at 'Depreciation Schedule'!B17 ('In run rate', with its note in D17: 'Never both'), D21 and the row 19 heading ('... carried flat') predates the v4 review and is replaced by A-17, A-18, A-19 and I-31 on this sheet: the flat carry is a builder assumption (A-17, A-19), and the Q4-26 treatment is a two-way risk awaiting the PO owner (A-18, I-31), not a settled 'never both' rule. The tab text was not edited, so that no cell other than Fld Eng Budget!B21 changes in v5.

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

Revenue basis (A-22, A-24, A-25): plan figures, not contracts. Sep-Dec 26 bookings 3,544,300 include 2,264,000 unsigned at 100%; FY27 bookings 29,452,766 are forecast. DeploySum!F40:Q40 hold static values (12 of 12). Dec-26 exit rate 662,103/month x 12 = 7,945,236; the other 7,618,410 of 2027 revenue depends on 2027 go-lives.

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
| A-14 | In-service = go-live month (DeploySum rows 19/20); full month of depreciation in that month | start delay 0; sensitivity: 1-month delay lowers 2027 depreciation by 274,833; mid-month convention lowers it by 137,417 | 'Depreciation Schedule'!B13 | brief v3 convention (orchestrator; labelled; user may change) |
| A-15 | Units built in 2027 for 2028 go-lives are not depreciated in 2027 | CapEx 9,446,375 excluded | 'Depreciation Schedule' section 7 | follows A-14 (not in service) |
| A-16 | Existing fleet = PO Dec-26 monthly run rate | 159,270.72/month | 'Depreciation Schedule'!B21:B24 = PO!M19:M22 | orchestrator instruction (handoff) |
| A-17 | Existing run rates stay flat all of 2027 (no end-of-life, retirement or disposal) | 1,911,249; trend alternative on 5010 +276,164 to the contribution (+403,624 if the decline also ran through Oct-Dec 26) | 'Depreciation Schedule' rows 33-36 | builder assumption: no asset register in the files (I-32) |
| A-18 | Oct-Dec 26 go-lives covered by the PO run rate, not added explicitly; the risk runs both ways | (39,057) if DeploySum's Q4 counts are right; +37,457 if PO's Dec-26 step-ups are Jan-27 units | 'Depreciation Schedule'!B17, section 5 | builder decision between the brief's two options; PO owner to confirm what the step-ups are (I-31) |
| A-19 | SlipBot 5010 continues at the Dec-26 run rate; no new SlipBots | 1,353,574 | 'Depreciation Schedule'!B21 | builder assumption (flat carry, A-17); status user to confirm (I-32); no builds per DeploySum note 4 |
| A-20 | '$000s' labels on DeploySum hold dollars; relabelled to '$' with comments | 13 labels | DeploySum col A | orchestrator instruction; evidence in I-30 |
| A-21 | ARR row (39) kept empty to keep the SD row map | no data | DeploySum row 39 | brief v2 item 1 |
| A-22 | Revenue includes unsigned and forecast bookings, taken at 100% | Sep-Dec 26 bookings 3,544,300 incl. 2,264,000 unsigned; FY27 bookings 29,452,766 all forecast | DeploySum!A49 (note 5); DeploySum rows 7-13, 40 | source: 9/30/26 sales plan; no probability weighting applied (builder: taken as given) |
| A-23 | Existing-fleet base is the PO Dec-26 forecast, not an actual | 159,270.72/month (PO!M19:M22; Sep-Dec 26 are forecast columns J:M; actuals run to Aug-26) | 'Depreciation Schedule'!B21:B24 | builder note (PO 2026 file); refresh when Q4-26 actuals close |
| A-24 | DeploySum F40:Q40 (2027 revenue) are static cached values from the 9/30/26 file, not live links | 12 of 12 months static; PO!U12:AF12 link to them (formulas) | DeploySum!F40:Q40 -> PO!U12:AF12 | build v3 (external workbook [1] not supplied); a plan change needs a new resolved export |
| A-25 | Revenue start timing vs go-live: revenue follows the plan's own recognition timing; depreciation starts in the go-live month (A-14) | not determinable: the workbook cannot show whether revenue starts in the go-live month | DeploySum row 40 vs rows 19/20; 'Depreciation Schedule'!B13 | builder note; plan owner to confirm (Revenue Roll-up not supplied) |
| A-26 | Head of Service Delivery annual salary (current employee), entered in v5 | 205,000/year in B21; model: full year from 2027-01-01, +3% from 2027-10-01, tax 6.8%, benefits 16.4%: 2027 cost 254,454 | Fld Eng Budget!B21 -> rows 67-71, 78-80 -> FE rows 67-69 | user-confirmed 2026-10-09 ('Head of Service delivery salary is $205k annually'); treatment = existing workbook logic |

A-22..A-25 are new in v4; A-26 is new in v5; A-14, A-17, A-18 and A-19 were edited in v4 (critic O1, O3, O4); A-17 also shows the N3 trend case in v5.

## DeploySum refresh and tie-out (v3 build; unchanged in v4 and v5)

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

## v4 -> v5 diff

`diff_versions.py` (exact: formulas as text, cached values with no tolerance) on every sheet present in both files except Collation Notes:

| Sheet | Cells | Formula diffs | Value diffs |
|---|---:|---:|---:|
| COO P&L | 3,530 | 0 | 159 |
| FO | 3,581 | 0 | 0 |
| PO | 3,631 | 0 | 0 |
| CO | 3,582 | 0 | 0 |
| FE | 3,582 | 0 | 137 |
| PE | 3,590 | 0 | 0 |
| DeploySum | 901 | 0 | 0 |
| Depreciation Schedule | 1,214 | 0 | 0 |
| Fld Ops Payroll | 1,165 | 0 | 0 |
| Prod Payroll | 1,173 | 0 | 0 |
| Fld Maint Budget | 1,012 | 0 | 0 |
| Fld Eng Budget | 740 | 1 | 130 |
| **Total** | 27,701 | 1 | 426 |

The one 'formula diff' is Fld Eng Budget!B21 (empty -> 205,000, a typed input: diff_versions.py compares cell contents). Cells whose formula text changed: 0.

Classification of the 426 value diffs: input cells 1 (Fld Eng Budget!B21); formula cells downstream of B21 425; anything else 0. Static trace: 490 formula cells can depend on B21 ({'Fld Eng Budget': 129, 'FE': 170, 'COO P&L': 182, 'Collation Notes': 9}); 56 of them did not change value; the Collation Notes ones are regenerated. Of the recalculated downstream cells, 2 moved by <= 1e-6 only. Recalculation noise outside the trace (left at the v4 value, not a change): 40 cells, max abs 9.9e-08, sheets {'COO P&L': 20, 'PO': 20}.

Comments added / removed / changed: 0 / 0 / 0. Sheets only in v4 / only in v5: none / none. Package: 34 of 38 parts byte-identical to v4; changed: xl/worksheets/sheet6.xml, xl/worksheets/sheet13.xml, xl/worksheets/sheet2.xml, xl/worksheets/sheet1.xml; added: none; removed: none.

## Error scan

| Sheet | v4 | v5 |
|---|---|---|
| COO P&L | none | none |
| FO | none | none |
| PO | none | none |
| CO | none | none |
| FE | none | none |
| PE | none | none |
| DeploySum | none | none |
| Depreciation Schedule | none | none |
| Fld Ops Payroll | none | none |
| Prod Payroll | {'#NAME?': 430} | {'#NAME?': 430} |
| Fld Maint Budget | none | none |
| Fld Eng Budget | none | none |

New errors in v5: **0**. Prod Payroll's #NAME? cells are the XLOOKUP rows LibreOffice cannot evaluate (I-05, I-25).

## Package

Parts 38; `xl/externalLinks/*` **0**; defined names 8,965 (v4: 8,965).

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

## Issues (v5)

Severity per the scale above. v5: I-26 RESOLVED (user-confirmed salary entered); I-32 adds the N3 trend case; I-02 and I-28 quote the recalculated FE amounts. v4 changed the text of I-02 (O6), I-05 (B1), I-07 and I-32 (O2, O3) and I-31 (O1). No other severity changed.

| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |
|---|---|---|---|---|---|---|---|
| I-01 | MED | PO!U12:AF12; PO!R12; PO!U13:AF13; PO!U15:AF15; DeploySum!F40:Q40 | Resolved by assumption in v3. 2027 revenue is now budgeted: PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27; row 39 in the 9/30/26 file), all to 4100 Subscription/Platform Fees (orchestrator assumption). PO!R12 set to 'Manual'. Still open: 4500 Implementation Fees and 4900 One-Time Revenue stay 0 in 2027, and the source does not say whether recognized revenue includes them. | PO!AG12 = 15,563,645.54; DeploySum FY27 recognized revenue (9/30/26 file R39) = 15,563,645.54; difference (0.00). 2026: 4500 85,861, 4900 975,000. Cross-check Sep-Dec 26: DeploySum recognized revenue 2,527,326 vs PO 4100 forecast (PO!J12:M12) 2,486,929 (difference 40,396), so the 4100 mapping is consistent with how PO forecasts 2026. | not determinable (2026 4500+4900 = 1,060,861) | impact not determinable; owner confirmation needed | Finance/PO owner to confirm the 4100 mapping and whether 2027 implementation or one-time revenue should be budgeted on 4500/4900. |
| I-02 | HIGH | FO!AG63; FO!AG116; FE!AG63; FE!AG116; COO P&L!AG132 | Replacing FO and FE with the SD versions adds 6,828,802 to 2027 COO cost (COGS + Opex). The SD build is much heavier than the COO book's FO/FE. (v4: restated in cost terms; the earlier evidence quoted 2027 Net Income from before revenue was budgeted.) | FO cost (AG63 + AG116): COO book 1,341,298 -> SD 7,347,500; FE: COO book 752,002 -> SD 1,574,602; together 2,093,300 -> 8,922,101. With the COO book's FO/FE, the 2027 COO contribution would be 6,967,834 instead of 139,032. Drivers: FO!N52 876,692 -> AG52 3,238,031; FO!N47 255,704 -> AG47 1,519,865; FO!N29 57,182 -> AG29 765,000. | (6,828,802) on the contribution | impact (6,828,802) | COO and SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off. |
| I-03 | LOW | DeploySum!A3:R49 (Collation Notes lists the formulas) | Resolved in v3. DeploySum rows 3-49 now hold the resolved values from 2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx. The 410 cells that link to the external workbook '[1]' are stored as that file's cached values; their formula text is on Collation Notes. The links are still not live (the [1] workbook was not supplied), so the next plan update needs a new resolved export. | DeploySum errors: v2 {'#REF!': 463, '#N/A': 35}, v3 none (498 resolved). Every mapped cell B:R equals the 9/30/26 cached value (mismatches: 0). New-file sha256 645e31303dcbbbd6... | 0 | hygiene | Refresh DeploySum from a new resolved export when the plan changes. Keep the row map (ARR row 39 kept). |
| I-04 | LOW | DeploySum!B53:R66; DeploySum!A69:R76 (v3 check block) | The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (rows 53-66) are still typed values. v3 adds a live check: they now tie to the resolved rows 16-21 in every month Sep-26..FY27. So the FO/FE drivers are consistent with the 9/30/26 plan; they are just not linked. | 16+17 vs 54+57+60: FY 67 vs 67, max monthly diff 0; 18 vs 64: FY 67 vs 67, max monthly diff 0; 19 vs 55+58+61: FY 250 vs 250, max monthly diff 0; 20 vs 56+59+62: FY 1,036 vs 1,036, max monthly diff 0; 21 vs 63: FY 0 vs 0, max monthly diff 0. DeploySum!A76 = 'Tie-out rows 16-21 vs 54-64: OK'. | 0 | hygiene | Optional: replace rows 54-64 with formulas (or document the source) so they update with the plan. |
| I-05 | MED | Prod Payroll!B24:S81 (hidden); Prod Payroll!S41; PO!AG33:AG36 | The production payroll model now partly computes. It reads DeploySum rows 4, 24, 25, 27 and 28, which v3 resolved. Errors fell from 796 to 430. The remaining 430 are #NAME?: 16 cells use _xlfn.xlookup (row 48), which LibreOffice 24.2.7.2 does not support, and the rest are in rows 49-81 below them (#NAME? propagates). Excel may evaluate them; not tested. It still feeds no budget value: FO/FE/CO/PE show 0 diffs and PO payroll rows are typed. Now that it computes, 'Total lift payroll' 2027 is far above PO's typed production labour. | Prod Payroll!S41 'Total lift payroll' (F:Q = Jan-Dec 27) = 1,622,423; tray (row 62), supervisor (row 79) and total (row 81) are still #NAME? in LibreOffice. PO 'Total - 5100 - Labor Expense - Production' AG36 = 652,820 (typed rows 33-35). Gap: 1,622,423 - 652,820 = 969,603 (lift payroll only). If the model is right and PO 5100 is the whole production payroll, the 2027 COO contribution falls by at least this gap, which on its own turns it negative ((830,571)). May overlap I-17. Cells read from Prod Payroll by other sheets: typed raise inputs only (M5, M6, M9), unchanged. | not determinable (exposure 969,603: lift payroll model 1,622,423 vs PO 5100 652,820) | impact not determinable; owner confirmation needed | PO owner to say which production payroll is right: the typed PO 5110-5140, or this model (open it in Excel to evaluate the XLOOKUP rows). See also I-17. |
| I-06 | LOW | Fld Maint Budget!B30 (comment); Fld Ops Payroll!B11; FO!AG44; FO!AG52 | MeLi contractor double count: quantified at $0 in the current cells. The CONFIRM comment on Fld Maint Budget!B30 says Fld Ops Payroll includes MeLi in '21 all-in techs', but Fld Ops Payroll!B11 = 14 ('Current site techs on payroll (Sep-26) - Domestic Only') and Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11 = 21. So MeLi techs are costed in 5310 only. The comment describes an earlier state and is stale (Fld Maint Budget!A143 records the correction). | FO 5310 (FO!AG44 = 575,268) = MeLi techs in role 346,920 + Merida contractors 123,900 + MeLi supervisor 104,448 (Fld Maint Budget rows 70-72 x B10/B11; row 84 = 575,268). FO 5510 current techs: Fld Ops Payroll!F20:Q20 = 14 each month (formula =$B$11); current-tech payroll 2027 1,094,774. | 0 | impact 0 | SD owner to confirm and delete the stale CONFIRM comment on Fld Maint Budget!B30. |
| I-07 | MED | PO!U19:AF22; 'Depreciation Schedule'!A1:S126; COO P&L!AG19:AG22 | Resolved by assumption in v3. 2027 depreciation is now budgeted from the new 'Depreciation Schedule' tab: straight-line, SlipLift 84 months, SlipTray 120 months, no salvage, full month from the go-live month. Existing fleet = PO Dec-26 run rate, carried flat (builder assumption, A-17). New units = DeploySum 2027 go-lives (rows 19/20). PO!R19:R22 set to 'Manual'. The open parts are logged separately: I-31 (Q4-26 go-lives), I-32 (existing-fleet run rates, SlipBot) and I-33 (peripherals). | 2027 depreciation 3,318,808 (2026 1,788,097): existing fleet 1,911,249, new 2027 go-lives 1,407,560. By GL: 5010 SlipBot 1,353,574; 5011 SlipLift 1,248,196; 5012 SlipCarrier (SlipTray) 418,898; 5020 Robot Peripherals 298,140. Python recompute from raw inputs vs workbook, all 48 GL-months: max diff 3.78e-10. | not determinable (component decisions in I-31..I-33) | impact not determinable; owner confirmation needed | PO owner/Finance to confirm the run-rate approach against the fixed-asset register, and resolve I-31..I-33. |
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
| I-26 | RESOLVED | Fld Eng Budget!B21; Fld Eng Budget!B67:M67; FE!AG67 | RESOLVED (user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). v5 enters 205,000 in Fld Eng Budget!B21, the designated input cell. Was (v4, MED): 'Head of Service Delivery – Rasheen Henry' had no salary entered, so FE 6610 carried $0 for this current employee. | Fld Eng Budget!B21 = 205,000; row 67 uses the roster formula of rows 59-66 (=IF(B$58>=$C$21,$B$21/12*(1+IF(B$58>=$B$25,$B$24,0)),0)...): start 2027-01-01 (C21) so 12 months paid, 17,083.33/month, +3% from 2027-10-01 (B24, B25) for 3 months (17,595.83/month): 2027 salary 206,538; payroll tax 6.8% (B22) 14,045; benefits 16.4% (B23) 33,872; total 254,454. FE!AG67 713,347 -> 919,884. | (254,454) on the contribution (in the v5 headline) | resolved; was MED (owner confirmation) | None. Confirm at sign-off that the Head of Service Delivery is not also budgeted on CO or PE (I-28). |
| I-27 | LOW | Logistics&WH Payroll!B56 (SD, not carried); FO!U52:AF52 | Logistics&WH Payroll excludes MH-05 ('Less: MH-05 Material Handler, logistics support (counted on the FO tab)'), but FO 5510 2027 (FO!U52) sums only Fld Ops Payroll rows 21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77, none of which is an MH-05 seat; 'MH-05' appears nowhere outside Logistics&WH Payroll. So this seat is in neither model. | Logistics&WH Payroll!B56 = -38,133 (deduction of MH-05's 2027 base pay, before burden). FO!U52 = ='Fld Ops Payroll'!F21+'Fld Ops Payroll'!F31+'Fld Ops Payroll'!F43+'Fld Ops Payroll'!F56+'Fld Ops Payroll'!F69+'Fld Ops Payroll'!F76+'Fld Ops Payroll'!F77+'Fld Ops Payroll'!F34+'Fld Ops Payroll'!F46+'Fld Ops Payroll'!F59+'Fld Ops Payroll'!F72. MH-05 mentions elsewhere: none. | 38,133 base pay missing (before burden) | impact 38,133 | SD/PO owners to decide where MH-05 is budgeted and add it. |
| I-28 | MED | CO!AG67:AG69; PE!AG67:AG69; FE!AG67:AG69; Fld Eng Budget!A13:A21 | SG&A payroll (6610/6630/6640) is non-zero on CO, FE and PE. FE is built from a named roster on Fld Eng Budget; CO and PE are typed monthly amounts with no roster, so the workbook cannot confirm that no person on the FE roster is also inside CO or PE. | row 67: CO 528,452, FE 919,884, PE 1,078,020; row 68: CO 27,593, FE 62,552, PE 38,501; row 69: CO 62,916, FE 150,861, PE 95,116. 2027 months typed (no formula): CO yes, PE yes, FE no (formulas). FE roster: Fld Eng Budget!A13:A21. | not determinable (no CO/PE roster) | impact not determinable; owner confirmation needed | CO and PE owners to confirm their SG&A payroll rosters exclude the people on Fld Eng Budget!A13:A21. |
| I-29 | LOW | Prod Payroll!M9; Fld Ops Payroll!M7; Fld Eng Budget!B59 (row formula); PO!AD33; PO!AD34; PO!AD35; CO!AD67; CO!AD68; CO!AD69; PE!AD67; PE!AD68; PE!AD69 | Raise timing is consistent (same % and month everywhere), but the eligibility rule is not: Fld Ops Payroll and Logistics&WH Payroll exclude staff hired in the months before the raise (Prod Payroll!M9), while Fld Eng Budget and the typed PO/CO/PE payroll rows apply the raise to the whole row. | Prod Payroll!M5 = 0.03, M6 = 2027-10-01, M9 = 6. Steps found in typed rows: PO!AD33 3.00%; PO!AD34 3.00%; PO!AD35 3.00%; CO!AD67 3.00%; CO!AD68 3.00%; CO!AD69 3.00%; PE!AD67 3.00%; PE!AD68 3.00%; PE!AD69 3.00%; FE!AD67 3.00%; FE!AD68 3.00%; FE!AD69 3.00%. | not determinable | hygiene | Payroll owners to confirm whether the eligibility rule should apply to all departments. |
| I-30 | LOW | DeploySum!A2, A7, A9, A11, A13, A29, A30, A35, A38, A39, A40, A41, A42 | The source labels say '$000s', but the values are whole dollars. v3 relabelled the 13 cells to '$' (A2 text: 'Dollars in $ (relabelled in v3; the source said $000s)'). Each cell has a comment quoting the original label, so the change is visible, not silent. | E.g. DeploySum!R13 total bookings 29,452,766 and R29 Production CapEx 32,410,900 are dollars: CapEx = units x unit cost in dollars (section 'Unit-cost reconciliation'), and recognized revenue is the same order as PO's 2026 revenue in dollars. | 0 | hygiene | Plan owner to fix the labels in the source (Revenue Roll-up / Deploy) so the next export is right. |
| I-31 | LOW | 'Depreciation Schedule'!A88:D97; PO!J20:M22; DeploySum!C19:E20 | Oct-Dec 26 go-lives are carried in the PO Dec-26 run rate, not added explicitly. The risk runs both ways. (a) Shortfall: PO steps up for 15 lifts and 53 trays in Q4-26, DeploySum has 18 and 67; if DeploySum is right the budget is short 39,057. (b) Possible double count: PO's Dec-26 step-up (3 lifts, 12 trays) has no DeploySum Dec-26 go-live. If these are units DeploySum places in Jan-27 (20 lifts, 60 trays, built Nov-26), they sit in both the run rate and the Jan-27 vintage: 37,457 too much. If (b) holds and DeploySum's Q4 counts are right, the gross Q4 shortfall is 76,514 and the net is still (39,057). The 5020 step-ups cannot be reproduced from DeploySum's peripheral cost. | PO 5011 monthly step-ups Oct/Nov/Dec: 6,964.29, 2,321.43, 2,321.43 = 9, 3, 3 lifts x 65,000/84. 5012: 1,933.33, 800.00, 800.00 = 29, 12, 12 trays x 8,000/120. 5020: 2,608.33, 1,025.00, 1,025.00 = 52.95, 20.81, 20.81 peripheral sets at 4,137.50/84 (not whole). DeploySum Oct/Nov/Dec lifts [9, 9, 0], trays [35, 32, 0]. Dec-26 step-ups with no DeploySum Dec-26 go-live: 3 lifts x 773.81 + 12 trays x 66.67 = 3,121.43/month, 37,457 for 2027. Gap not budgeted: 3 lifts + 14 trays = 3,254.76/month, 39,057 for 2027 (plus up to 10,639 if Q4-26 lift peripherals are not in 5020). | (39,057) to +37,457 (5020 Dec step: up to +12,300 more) | impact 39,057 (< $50k) | PO owner to say what the Oct/Nov/Dec-26 step-ups on PO rows 20-22 are (which go-lives, which month). Then the user chooses: keep the PO run rate (current), or Sep-26 run rate + DeploySum Oct-Dec 26 vintages. Do not do both. |
| I-32 | HIGH | 'Depreciation Schedule'!B21:B24; PO!M19:M22; PO!U19:AF19 | Existing-fleet depreciation is carried flat at the PO Dec-26 run rate for all 12 months of 2027. The flat carry is a builder assumption (A-17): the brief asked for the PO 2026 monthly depreciation as the existing-fleet input, not for a flat carry. The workbook has no asset register, so it cannot show whether any of these assets reach the end of their life, or are retired, in 2027. The largest line is 5010 SlipBot: 112,797.85/month = 1,353,574 in 2027. Whether the SlipBot fleet is fully depreciated, retired or ongoing is not in the files. DeploySum note 4 says no SlipBots are built and existing bots are redeployed, which suggests the fleet is in use. 5020's run rate basis is also unknown (I-31). Trend alternative: 5010 fell through 2026 (141,122 Jan -> 112,798 Sep, (3,541)/month); continuing that decline through 2027 from the Sep-26 level lowers depreciation by 276,164 (151,680 on the Jan-Aug actuals trend, (1,945)/month); if the decline also runs through Oct-Dec 26 (floored at 0) it lowers it by 403,624 (221,687 on the actuals trend). The 5020 base (8,212 in Jan-26, when 5011 was 0) predates SlipLift depreciation, so it is probably SlipBot-related and may share the SlipBot end-of-life risk (98,543 for 2027 at that rate). | Dec-26 run rates (PO!M): 5010 112,797.85, 5011 20,444.90, 5012 6,502.64, 5020 19,525.33; 2027 existing total 1,911,249. 5010 2026 actuals Jan-Aug 141,122.35 -> 127,510.00, forecast Sep-Dec flat 112,797.85; 2026 total 1,492,329. | up to +1,353,574 (5010 = 0); trend +276,164 (continued from Sep-26: +403,624); 5020 base up to +98,543 | impact 1,353,574 | USER DECISION: confirm SlipBot fleet status (fully depreciated / retired / ongoing / declining as in 2026) and the end-of-life month for any existing asset group. Change the section 2 input on the schedule if the run rate stops. |
| I-33 | MED | 'Depreciation Schedule'!B7, B11, B16; PO!U22:AF22 | SlipLift peripherals (4,137.50 per lift, from DeploySum CapEx) are depreciated on 5020 Robot Peripherals over 84 months. Both the GL and the life are builder assumptions: the user gave lives for SlipLifts and SlipTrays only. 5020 was chosen because PO's 2026 forecast books 5011 at exactly $65,000/84 per lift, so PO keeps peripherals out of 5011. | 2027 new-peripheral depreciation 63,836 (Dec-27 12,313.99/month). Moving it to 5011 changes the GL split only, not the total. A different life changes the amount in proportion (e.g. 60 months: 89,370). | 63,836 | impact 63,836 | User to confirm the peripherals GL (5020 or 5011) and life; both are input cells. |

### Variance scan: rows with |AG-N| > $50k and > 50% (recomputed from the v5 workbook)

'%' = (AG - N) / N; 'n/m' where N is zero or negative, or AG is negative while N is positive. Rows new in v5: FE 69 6640 - Benefits - SG&A; FE 140 Benefits. No rows dropped.

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
| FO | 64 | Gross Profit | (1,967,580) | (7,347,500) | (5,379,919) | n/m |
| FO | 67 | 6610 - Salaries and Wages - SG&A | 50,575 | 0 | (50,575) | -100% |
| FO | 73 | Total - 6000 - Labor Expense - SG&A | 53,891 | 0 | (53,891) | -100% |
| FO | 91 | 7200 - Contractors | 59,734 | 0 | (59,734) | -100% |
| FO | 116 | Total - Expense | 217,242 | 0 | (217,242) | -100% |
| FO | 117 | Net Ordinary Income | (2,184,823) | (7,347,500) | (5,162,677) | n/m |
| FO | 132 | Net Income | (2,184,823) | (7,347,500) | (5,162,677) | n/m |
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
| PO | 67 | 6610 - Salaries and Wages - SG&A | (308,059) | 0 | 308,059 | n/m |
| PO | 73 | Total - 6000 - Labor Expense - SG&A | (309,871) | 0 | 309,871 | n/m |
| PO | 98 | 7700 - Inventory Obsolescence-old | 636,000 | 0 | (636,000) | -100% |
| PO | 116 | Total - Expense | 461,703 | 171,650 | (290,053) | -63% |
| PO | 117 | Net Ordinary Income | 4,600,898 | 10,976,292 | 6,375,394 | 139% |
| PO | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| PO | 132 | Net Income | 4,685,709 | 10,976,292 | 6,290,582 | 134% |
| PO | 137 | Salaries and Wages | (159,704) | 525,310 | 685,014 | n/m |
| PO | 140 | Benefits | 51,491 | 108,404 | 56,914 | 111% |
| FE | 30 | 5050 - Travel - Deployment | 87,455 | 346,633 | 259,178 | 296% |
| FE | 37 | Total - 5000 - Robot Production and Deployment | 99,214 | 388,814 | 289,600 | 292% |
| FE | 63 | Total - Cost Of Sales | 115,989 | 388,814 | 272,825 | 235% |
| FE | 64 | Gross Profit | (115,989) | (388,814) | (272,825) | n/m |
| FE | 69 | 6640 - Benefits - SG&A | 80,480 | 150,861 | 70,381 | 87% |
| FE | 91 | 7200 - Contractors | 154,857 | 0 | (154,857) | -100% |
| FE | 140 | Benefits | 80,480 | 150,861 | 70,381 | 87% |
| PE | 33 | 5110 - Salaries and Wages - Production | 65,377 | 0 | (65,377) | -100% |
| PE | 35 | 5140 - Benefits - Production | (56,264) | 0 | 56,264 | n/m |
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
| COO P&L | 35 | 5140 - Benefits - Production | (1,993) | 108,404 | 110,397 | n/m |
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
| COO P&L | 117 | Net Ordinary Income | (984,033) | 139,032 | 1,123,065 | n/m |
| COO P&L | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| COO P&L | 132 | Net Income | (899,222) | 139,032 | 1,038,254 | n/m |
| COO P&L | 137 | Salaries and Wages | 3,264,812 | 6,289,698 | 3,024,886 | 93% |
| COO P&L | 139 | Payroll Taxes | 210,079 | 358,553 | 148,474 | 71% |
| COO P&L | 140 | Benefits | 471,094 | 925,703 | 454,609 | 97% |

## Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5)

### Cross-department overlap

Every COO P&L GL row (label 'NNNN - ...') and the payroll memo rows 137-140 were checked: 103 rows, of which 12 have 2 or more departments non-zero in 2027 (AG). Each was traced to its driver cells.

| Row | Line | FO | PO | CO | FE | PE | COO P&L AG | Classification | Amount at risk | Driver trace |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 30 | 5050 - Travel - Deployment | 46,354 |  |  | 346,633 |  | 392,987 | Legitimate split (documented) | $0 | FO!U30 = ='Fld Maint Budget'!B90 (tech deployment travel = new sites x Fld Maint Budget!B6 0.3 x B5 2,533/trip; D6: 'FE travels every deployment (FE sheet); techs supplement where FE is short'). FE!U30 = ='Fld Eng Budget'!B74 (FE travel per weighted deployment; Fld Eng Budget!B6 = 1: 'Source: user-provided. 100% stays on the FE tab until a decision on moving deployment trav'). Fld Eng Budget!B2: 'Technician deployment travel sits on Fld Maint Budget.' Different people (techs vs field engineers). |
| 47 | 5340 - Spare Parts | 1,519,865 | 34,500 |  |  |  | 1,554,365 | Likely legitimate split | $0 | FO!U47 = ='Fld Maint Budget'!B94: spares run rate from FO-dept actuals only (Fld Maint Budget!D16: 'FO tab 5340 actuals, Jan–Jul 26 average ($147,799 ÷ 7)'), grown with SlipLifts in field. PO: PO input method 'Even', annual input S = 30000, with later months multiplied by a ramp row (PO!AF47 = =IF($R47="Manual","",IFERROR(IF($R47="YOY Growth",$N47*(1+$T47)/12,$S47/12),""))*AF146). Both depts booked 5340 in 2026 (N: FO 255,704, PO 63,637); FO's base excludes PO's spend. |
| 67 | 6610 - Salaries and Wages - SG&A |  |  | 528,452 | 919,884 | 1,078,020 | 2,526,356 | Unclear (person level) | not determinable; rows involved: CO 528,452, PE 1,078,020 | FE!U67 = ='Fld Eng Budget'!B78; Fld Eng Budget!B78 = =B68, B68 = =SUM(B59:B67) (named roster A13:A21). CO and PE U:AF are typed monthly amounts with no roster. All three booked 6610 in 2026 (CO 533,086, FE 850,615, PE 1,048,172). See I-28. |
| 68 | 6630 - Payroll Taxes - SG&A |  |  | 27,593 | 62,552 | 38,501 | 128,646 | Unclear (person level) | not determinable; rows involved: CO 27,593, PE 38,501 | Follows 6610: FE!U68 = ='Fld Eng Budget'!B79, Fld Eng Budget!B69 = =B68*$B$22; CO/PE typed. See I-28. |
| 69 | 6640 - Benefits - SG&A |  |  | 62,916 | 150,861 | 95,116 | 308,894 | Unclear (person level) | not determinable; rows involved: CO 62,916, PE 95,116 | Follows 6610: FE!U69 = ='Fld Eng Budget'!B80, Fld Eng Budget!B70 = =B68*$B$23; CO/PE typed. See I-28. |
| 74 | 6100 - Travel |  |  |  | 45,235 | 26,500 | 71,735 | Legitimate split | $0 | FE!U74 = ='Fld Eng Budget'!B76 (FE non-deployment travel: FE-tab 2026 run rate + buffer). PE: PE input method 'Even', annual input S = 6000 (plus typed overrides, I-09). Separate departments' own travel; both booked 6100 in 2026 (FE 35,010, PE 2,235). |
| 93 | 7500 - Facility Expenses |  | 5,750 |  |  | 9,380 | 15,130 | Legitimate split | $0 | PO: PO input method 'Even', annual input S = 5000; PE: PE input method 'Even', annual input S = 8400. Separate dept inputs; both booked this GL in 2026 (PO 530, PE 3,148). |
| 95 | 7550 - Tools and Equipment |  | 29,900 |  |  | 36,180 | 66,080 | Legitimate split | $0 | PO: PO input method 'Even', annual input S = 26000; PE: PE input method 'Even', annual input S = 32400. Separate dept inputs; both booked this GL in 2026 (PO 5,059, PE 21,705). |
| 99 | 8100 - Technology |  | 20,000 |  |  | 5,400 | 25,400 | Legitimate split | $0 | PO: PO input method 'Even', annual input S = 20000; PE: PE input method 'Even', annual input S = 5400. Separate dept inputs; both booked this GL in 2026 (PO 13,648, PE 3,093). |
| 137 | Salaries and Wages | 3,238,031 | 525,310 | 528,452 | 919,884 | 1,078,020 | 6,289,698 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 typed and unlinked: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |
| 139 | Payroll Taxes | 210,802 | 19,105 | 27,593 | 62,552 | 38,501 | 358,553 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 typed and unlinked: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |
| 140 | Benefits | 508,405 | 108,404 | 62,916 | 150,861 | 95,116 | 925,703 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 typed and unlinked: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |

Result: 0 likely double counts on the same GL row. Unclear rows are logged as I-28. Cross-row overlaps found while tracing: none between FO payroll and Logistics&WH (Rebecca is excluded from Logistics&WH, Logistics&WH Payroll!B55, and costed in Fld Ops Payroll row 76: 2027 77,089); one seat in neither model (MH-05, I-27); the current employee with no salary in v4 (I-26) has a salary from v5 (Fld Eng Budget!B21 = 205,000).

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

Rates and timing only: other sheets read only these typed raise inputs from Prod Payroll, never a headcount or cost cell. Prod Payroll now partly computes (v3 resolved DeploySum): 'Total lift payroll' S41 = 1,622,423, but 430 cells are errors (#NAME? 430; XLOOKUP rows that LibreOffice cannot evaluate, see I-05), out of 899 formulas. PO 5110-5140 2027 (PO!U33:AF35) are typed values with no link to any tab, so PO AG33 525,310 and FO 5510 share no headcount source: no double count through Prod Payroll. The open question is the reverse: the model's lift payroll exceeds PO 5100 (652,820) by 969,603 (I-05).

### Raise timing consistency

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
| FE | 67 | 6610 - Salaries and Wages - SG&A | False | AB: 7.34%, AD: 3.00% |
| FE | 68 | 6630 - Payroll Taxes - SG&A | False | AB: 7.34%, AD: 3.00% |
| FE | 69 | 6640 - Benefits - SG&A | False | AB: 7.34%, AD: 3.00% |

12 of 12 payroll rows step by Prod Payroll!M5 (3.00%) in month 10 of 2027 (Prod Payroll!M6); the raise inputs on Fld Ops Payroll / Fld Eng Budget / Logistics&WH are all links to those cells, so % and month are consistent. FE's other step is the new hire 'Customer Support Specialist – New hire' starting 2027-08-01. Rule difference: eligibility (Prod Payroll!M9) is applied in Fld Ops Payroll (`=F20*$B$6/12+IF(F$19>=$M$6,MIN(F20,INDEX($B20:$Q20,IFERROR(M...`) and Logistics&WH, but not in Fld Eng Budget (`=IF(B$58>=$C$13,$B$13/12*(1+IF(B$58>=$B$25,$B$24,0)),0)`) or the typed rows: I-29.

### Logistics & Warehouse payroll and MeLi

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
- D1 (v4): Patch, do not round-trip. v4 copied the v3 package and rewrote only the Collation Notes part; LibreOffice re-saves change cached values in the last floating-point digit.
- D2 (v4): Collation Notes strings are written as inline strings, and existing v3 cell styles are reused, so sharedStrings.xml and styles.xml stay byte-identical (the v3 notes strings remain in sharedStrings.xml, unused).
- D3 (v4): Formula cells on Collation Notes store values computed by the figures script; the analyze script checks them against a LibreOffice recalculation.
- D4 (v4): '% change' = n/m when the base is zero or negative or the new value is negative with a positive base; the live formula returns text ('n/m' or e.g. '110%') so no new number format is needed.
- D5 (v4): The workbook's 'Net Income' label (COO P&L!A132 and dept tabs) is not renamed; the notes and Collation Notes use 'COO contribution'.
- D6 (v4): Exposures are shown one at a time against the headline and not netted, because I-05 and I-17 may overlap; combined figures are shown with that caveat.
- D7 (v4): The I-32 trend alternative uses the Jan->Sep-26 slope (critic's basis, Sep is the first forecast month) and also shows the Jan->Aug actuals-only slope; each is floored so 5010 cannot go negative.
- D8 (v4): Decisions pending are presented, not resolved; the budget keeps the v3 treatment.
- D1 (v5): Recalculate with LibreOffice, keep only downstream changes. Stage 1 (v4 + B21) is fully recalculated; a static trace of all formulas lists every cell that can depend on B21; only those cells take the recalculated value (when it differs). Every other cell keeps its v4 bytes, so the v4 -> v5 diff shows exactly the input and its consequences; the build stops if any cell outside the trace moves by more than 1e-6.
- D2 (v5): The salary is entered as the annual figure the user gave (205,000) in the designated input cell; the model's own row-67 logic applies unchanged (full year from the C21 start month Jan-27, the tab-wide 3% raise from Oct-27, the tab's tax and benefit rates). No new logic was added. Read as the current (Dec-26) salary, consistent with the other roster rows.
- D3 (v5): Workbook text cells that the salary makes out of date are left as they are (only B21 may change). Fld Eng Budget!D21 still says 'Enter annual salary in B21' (now done); the Depreciation Schedule text is superseded by a Collation Notes line (N1).
- D4 (v5): N2 label used as given, plus what each end contains, because the upper end is I-32 alone and does not add the other quantified upsides (A-14, I-31 double count, I-33).
- D5 (v5): N3 case continues the Jan->Sep-26 slope through Oct-Dec 26, so Jan-27 is 4 slope steps below Sep-26; effect = flat carry (12 x Dec-26 run rate) less the trend path, each month floored at 0. The Dec-26 run rate equals the Sep-26 level in the PO forecast (checked).
- D6 (v5): Tables carried from v2/v3 that quote workbook values (variance scan, cross-department overlap, raise steps) are regenerated from the v5 workbook by generators that first reproduce the v4 tables exactly from v4.

## Not done / limits

- The external workbook '[1]' is still not available: DeploySum holds the 9/30/26 cached values, not live links.
- No fixed-asset register was supplied, so existing-fleet depreciation is a run rate, not an asset-by-asset schedule. End-of-life dates are unknown (I-32).
- Not opened in Microsoft Excel. Prod Payroll's XLOOKUP rows show #NAME? in LibreOffice 24.2 and may evaluate in Excel (untested).
- No change made in v3 to FO, FE, CO, PE, or to PO lines other than 12 and 19-22 (and their subtotals/ratios); v5 changes only Fld Eng Budget!B21 (FE payroll and its totals recalculate). 4500/4900 stay 0 by assumption.
- v2 limits on page setup, sheet-scoped names and Google-specific parts still apply.
- v4: revenue effect of unsigned/forecast bookings and the revenue-vs-go-live timing (A-22, A-25) cannot be quantified from the workbook; the Revenue Roll-up and 2026 Exist New tabs of the plan were not supplied.
- v5: the explanatory text on the Depreciation Schedule tab (B17/D17, D21, row 19 heading) was not edited; it is superseded by A-17, A-18, A-19 and I-31 (Collation Notes line, N1).
- v5: the workbook cannot confirm the Head of Service Delivery is not also inside CO or PE typed SG&A payroll (I-28 open); the salary is assumed to be the current rate, raised from Oct-27 like the rest of the roster.
- v5: not opened in Microsoft Excel; Excel will show the stored values until it recalculates (they match a LibreOffice recalculation).
