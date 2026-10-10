# 02-build notes v8 - 2027 COO budget collation

> **CONFIDENTIAL – contains named compensation data (HC-* tabs); restrict distribution.** The workbook's HC-* tabs hold employee names and salaries; share the workbook and these notes only with people cleared to see compensation. In this file per-person amounts for identified employees are rounded to the nearest $5k (shown with '~') or aggregated. Rounding does not change an amount that is already a multiple of $5k, so some unique-role salaries (one person per role) still appear at their exact value; the Collation Notes sheet keeps exact figures. A department total compared across versions can also reveal one person's cost.

## Decisions pending

Decision #1 is RESOLVED (user-confirmed 2026-10-10: production labour is capitalised) and booked in v8. 9 decisions remain open: #2-#9 as in v7 (#6 reworded now that the production ramp is capitalised) and #10, new, on the scope of the policy (I-40). The budget carries the 'current treatment' column. Effects are on the 2027 COO contribution, each on its own.

| # | Decision (user) | Issue | Current treatment in the budget | Alternatives: effect on 2027 COO contribution (+ raises, ( ) lowers) | Who |
|---|---|---|---|---|---|
| 1 | RESOLVED (user-confirmed 2026-10-10: 'production labor is capitalized. Use the same formula as the file has.'). Production labour: expensed, or capitalised into the unit cost? | I-05 (RESOLVED), I-23, I-40 | Booked in v8: all Prod Payroll labour is capitalised (model 2027 2,592,894, the 9 current staff included) and depreciated by the Depreciation Schedule logic: 5011 +118,078, 5012 +34,961; PO 5110-5140 2027 = 0 (v7 652,820). Contribution 638,814 (v7 139,032). | Resolved. The scope (current staff, Oct-Dec 26 labour) is Decision #10. | User (resolved) |
| 2 | SlipBot fleet status (5010 depreciation) | I-32 | Carried flat at the PO Dec-26 run rate 112,797.85/month = 1,353,574 in 2027 (builder assumption, A-17). | Fully depreciated or retired from Jan-27: +1,353,574. Continue the 2026 decline ((3,541)/month, Jan-Sep 26) from the Sep-26 level in Jan-27: +276,164 (actuals Jan-Aug only, (1,945)/month: +151,680). Same decline also running through Oct-Dec 26, floored at 0: +403,624 (actuals-only slope: +221,687). Ongoing at the run rate: 0. Related: the 5020 base of 8,212/month (Jan-26, before any SlipLift depreciation) may end with the SlipBots: up to +98,543. | User, with PO/Finance (fixed-asset register) |
| 3 | Q4-26 go-lives: PO run rate or DeploySum | I-31 | Inside the PO Dec-26 run rate: PO steps up for 15 lifts / 53 trays (DeploySum: 18 / 67). | Sep-26 run rate + DeploySum Oct-Dec 26 vintages: (39,057). If PO's Dec-26 step-up (3 lifts, 12 trays) is Jan-27 units already in the Jan-27 vintage and PO's Oct/Nov counts are right: +37,457. Keep as is: 0. | User, after the PO owner says what the Q4-26 step-ups are |
| 4 | SlipLift peripherals: GL and useful life | I-33 | 5020 Robot Peripherals, 84 months: 63,836 of 2027 depreciation (builder assumption, A-10/A-11). | GL 5011 instead of 5020: 0 (moves 63,836 from PO row 22 to row 20). Life 60 months: (25,534). Life 120 months: +19,151. | User |
| 5 | Revenue split across 4100 / 4500 / 4900 | I-01 (A-02, A-03) | All 15,563,646 of plan revenue on 4100; 4500 and 4900 = 0 (orchestrator assumption). | Split the plan revenue across the three lines: 0 (classification only; gross margin unchanged). Budget implementation / one-time revenue in addition to the plan: not determinable (2026 4500 + 4900: 1,060,861). | User / Finance |
| 6 | Warehouse payroll (Logistics&WH) and the material-handling roles | I-17, I-41 | v8: the Prod Payroll model (ramp and current 9) is in the budget as capitalised labour (Decision #1). The Logistics&WH model is not: PO 5110-5140 held the 9 current PO HC staff, now 0 (capitalised). | Add the 7 new Logistics&WH seats: (336,530); deduplicated at the 9-overlap (398,492) (MH-01 then a new seat); at the 7-overlap the 2 material-handling roles also stay expensed: (471,093) (I-41). Keep as is: 0. (The Prod Payroll ramp is no longer an expense: Decision #1.) | User, with the PO owner |
| 7 | One person probably costed in both FO and FE | I-28 | Probably costed twice (name match only; title and salary differ; likely FO->FE move): one of the 14 current techs in Fld Ops Payroll and Fld Eng Budget row 15. | Remove from FO (B11 14 -> 13): +78,529 (payroll +78,198, 5330 +331). Remove from FE (row 15): +~95,000. Pro rata if the move happens mid-year. | SD / FO owners |
| 8 | FE payroll tax and benefit rates | I-34 | SD field rates 6.8% / 16.4% on FE salaries. | FE HC (T&B) rates 4.069% / 7.223%: +109,539. Keep: 0. Caveat: the HC T&B tax rates are below the 7.65% employer FICA and unverified (I-37); with the FE tax rate at 7.65%: +76,600. | User / Finance |
| 9 | PE 'transfer?' row (Head of Production and Delivery) | I-35 | In PE 6610-6640 for all of 2027 (~255,000). | Leaves COO from Jan-27: +~255,000. Moves within COO: 0 (budget it once, on the receiving department). Stays: 0. | PE owner |
| 10 | Scope of the capitalisation policy: are the 9 current production staff and the Oct-Dec 26 model labour (in the Jan-Feb 27 go-lives) capitalised too? 2026 expensed COO 5100 production labour, so the 2026 policy may have been partial. | I-40 | Both capitalised (brief v5 primary case): 'Depreciation Schedule'!B131 = 1, B132 = 1. | Current 9 expensed (sensitivity): (601,118) -> 37,696. Oct-Dec 26 labour not capitalised: +48,621 -> 687,435. Both: (572,877) -> 65,936. Each is one switch on the Depreciation Schedule; the workbook recalculates. | User / Finance |

Why #10 (I-40): brief v5 reads the policy as covering the whole Prod Payroll model, the 9 current staff included, but the 2026 books expensed production labour (COO 5100 208,574 in 2026: PO 197,323, PE 11,473) next to credits that fit a capitalised-labour credit (PO 6000 (309,871), PE 5140 (56,264); I-23). So the 2026 policy may have been partial. DeploySum labels the unit costs 'Unit cost (CapEx)' (A47); v8 adds the labour on top of those costs.

## Headline: 2027 COO contribution

| Line | COO P&L row | 2026 (N) | 2027 v8 (AG) | Change | % | 2027 v7 (AG) | v8 - v7 |
|---|---|---:|---:|---:|---:|---:|---:|
| Revenue (company recognized revenue, 9/30/26 sales plan) | 16 | 7,423,940 | 15,563,646 | 8,139,706 | 110% | 15,563,646 | 0 |
| COGS (COO departments) | 63 | 4,478,016 | 11,652,235 | 7,174,220 | 160% | 12,152,017 | (499,782) |
|   of which depreciation (in COGS) | 19-22 | 1,788,097 | 3,471,846 | 1,683,750 | 94% | 3,318,808 | 153,038 |
| Gross Profit | 64 | 2,945,924 | 3,911,410 | 965,486 | 33% | 3,411,628 | 499,782 |
| Opex (COO departments) | 116 | 3,929,957 | 3,272,597 | (657,361) | -17% | 3,272,597 | 0 |
| COO contribution before other income (workbook label 'Net Ordinary Income') | 117 | (984,033) | 638,814 | 1,622,847 | n/m | 139,032 | 499,782 |
| Net Other Income | 131 | 84,811 | 0 | (84,811) | -100% | 0 | 0 |
| **COO contribution (workbook label 'Net Income')** | 132 | (899,222) | 638,814 | 1,538,036 | n/m | 139,032 | 499,782 |

- **2027 COO contribution (COO P&L AG132): 638,814** (v7 139,032, +499,782). The change is exactly PO 5110-5140 removed (652,820, now capitalised) less the depreciation of the capitalised labour (153,038: 5011 118,078, 5012 34,961). Revenue 15,563,646 (all to 4100); COGS + Opex 14,924,832.
- Issues: 4 HIGH, 15 MED, 20 LOW open; 2 RESOLVED. v8 resolves I-05, adds I-40 (HIGH) and I-41 (MED), and updates I-07, I-11, I-14, I-17, I-23, I-25, I-37 and I-38.

**Headline caveat: resolved (Decision #1, user-confirmed 2026-10-10): production labour is capitalised. The whole Prod Payroll model (2,592,894 for 2027: ramp and the current 9) is budgeted as capitalised labour and reaches 2027 only as depreciation (153,038); the FO ramp (2,618,543) stays an operating cost (field labour). Both follow the same 9/30/26 deployment plan. The contribution moves from 139,032 to 638,814: PO 5110-5140 (652,820) leaves the P&L and 153,038 of labour depreciation enters 5011/5012. Scope sensitivity (current 9 expensed, ramp only capitalised): 37,696.**

### Caveats on the headline (read before using the figure)

(1) What the figure is. The bottom line, 638,814, is a **COO contribution**: the company's recognized revenue (15,563,646, all of it) less the costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: 14,924,832). Costs outside COO (for example sales, G&A, R&D) are not in this workbook, so it is **not company Net Income**. The workbook row keeps its GL label 'Net Income' (COO P&L!A132) because v4 and v5 change no label on the P&L tabs; the notes and Collation Notes call it 'COO contribution'.

(2) What the revenue is. 2027 revenue is the 9/30/26 sales plan's recognized revenue (DeploySum row 40, static cached values, A-24), not signed contracts. It includes unsigned and forecast bookings: Sep-Dec 26 bookings of 3,544,300 include 2,264,000 of unsigned forecast at 100% (DeploySum note 5, A49: bookings are gross ACV), and all 29,452,766 of FY27 bookings are forecast (new logos 24,016,000, expansion 5,436,766). 7,618,410 (49%) of 2027 revenue is above the Dec-26 exit rate x 12 (7,945,236), so it depends on go-lives that have not happened yet.

(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. Production labour is capitalised (Decision #1); the **scope alternatives** (Decision #10) are rows here, as are the I-17 readings with the capitalised Prod Payroll (9 by count, 7 by role). The v7 rows for 'I-05 expensed', 'capitalised on top' and 'inside the unit cost' are removed: the policy is decided.

| Item | Direction | What could happen | Effect on 2027 COO contribution | Contribution after this item alone | Source cells |
|---|---|---|---:|---:|---|
| Decision #1 scope: current 9 expensed (sensitivity, not booked) | downside | If only the ramp is capitalised and the 9 current PO staff stay expensed, PO 5110-5140 returns to its v7 amount (652,820), 2027 capitalised labour falls to 1,962,389 and its 2027 depreciation to 101,336 (booked: 153,038). Recalculated with the workbook switch 'Depreciation Schedule'!B131 = 0. | (601,118) | 37,696 | 'Depreciation Schedule'!B131:B132; PO!U33:AF35 |
| Decision #1 scope: Oct-Dec 26 labour not capitalised | upside | 2026 expensed production labour (COO 5100 208,574 in 2026), so the Oct-Dec 26 model labour in the Jan-Feb 27 go-lives (381,863) may not be capitalisable. Without it 2027 labour depreciation is 104,417. Switch B132 = 0. | +48,621 | 687,435 | 'Depreciation Schedule'!B132; rows 143-145 (B:E) |
| Decision #1 scope: both alternatives | downside | Current 9 expensed and no Oct-Dec 26 labour capitalised (B131 = 0, B132 = 0), recalculated. | (572,877) | 65,936 | 'Depreciation Schedule'!B131:B132; PO!U33:AF35 |
| I-41 (7-overlap): material-handling roles stay expensed | downside | PO 5110-5140 = 0 also removes the 2 material-handling roles (PO HC r16 Material Handling Team Lead, r20 Material Handler). On the 7-of-9 role reading they are warehouse staff (Logistics&WH), not production labour, so their cost stays an expense: the 2 people together at PO HC rates. | (134,563) | 504,251 | 'HC-PO'!C16:Z16, C20:Z20, D6:D7; PO!U33:AF35 |
| I-05 burden (O1), capitalised | downside | The ramp at PO HC burden rates (+141,924 of 2027 cost, v7 O1) is now capitalised, so only its depreciation reaches 2027 (pro rata: 4.03% of 2027 payroll is depreciated in 2027 under the booked method without Oct-Dec 26 labour). | (5,715) | 633,098 | Prod Payroll!B6:C7, H6:H7; 'HC-PO'!D6:D7 |
| Run rate: 2026 go-lives carry no labour | downside | The existing-fleet run rate (PO Dec-26) holds no labour. Under the same policy the Sep-26 model labour (90,851) sits in the Nov-26 go-lives: 12 months of 2027 depreciation. Earlier 2026 go-lives: not determinable (no 2026 labour by build month before Sep-26). | (12,074) | 626,740 | 'Depreciation Schedule'!B152, B154, row 161; PO!M20:M21 |
| I-17 | downside | Logistics & warehouse seats (SD model, not carried) that no HC roster holds: 7 seats, net of the 2 seats that are already on CO HC r17 and PO HC r20 (210,912 of the model's 547,441). | (336,530) | 302,284 | SD Logistics&WH Payroll!S51 less LOG-01 and MH-01 (not carried) |
| I-17 deduplicated, 9-overlap | downside | On the 9-of-9 count reading PO HC r20 is one of Prod Payroll's 9 current staff, now capitalised; Logistics&WH seat MH-01 (r20 by name) is then a new seat (+~60,000). | (398,492) | 240,321 | SD Logistics&WH Payroll MH-01; Prod Payroll B9:C9 |
| I-17 + I-41, 7-overlap | downside | The 7 Logistics&WH seats plus the 2 material-handling roles staying expensed (I-41); no seat counted twice. | (471,093) | 167,721 | as above |
| I-10 | downside | FO/FE lines with 2026 spend budgeted at 0 for 2027 (5920 software, 6610 SG&A salaries, 7200 contractors); effect if they continue at the 2026 level. | (384,425) | 254,389 | FO!N58, N67, N91; FE!N91 (AG = 0) |
| I-26 | RESOLVED | RESOLVED (user-confirmed 2026-10-09): Head of Service Delivery salary 205,000/year entered in v5 and now inside the headline (2027 cost ~255,000: salary ~205,000 + payroll tax ~15,000 + benefits ~35,000; v4 contribution was 393,486). No remaining exposure. | 0 (now in the headline) | 638,814 | Fld Eng Budget!B21 = 205,000 |
| I-28 | upside | Probable duplicate (name match only; title and salary differ; likely FO->FE move): FO HC r15 Field Technician = Fld Eng Budget r15 Field Engineer. Remove from FO (Fld Ops Payroll B11 14 -> 13), recalculated: payroll +78,198 and +331 on 5330 (Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11); supervisor headcount unchanged. Pro rata if the move happens mid-year. | +78,529 | 717,343 | Fld Ops Payroll!B11, rows 20-24; Fld Maint Budget!B29 |
| I-28 | upside | Same person: remove from FE instead (Fld Eng Budget row 15, at SD burden rates). Pro rata if the move happens mid-year. (per-person amount rounded to $5k) | +~95,000 | ~735,000 | Fld Eng Budget!B15; rows 61, 69-70 |
| I-31 | two-way | Shortfall if DeploySum's Q4-26 go-lives are right (3 lifts, 14 trays more than PO's run rate). | (39,057) | 599,757 | PO!J20:M21; DeploySum!C19:E20 |
| I-31 | two-way | Double count if PO's Dec-26 step-up (3 lifts, 12 trays; DeploySum Dec-26 go-lives 0) is Jan-27 units (20 lifts, 60 trays go live Jan-27, built Nov-26). Excludes the 5020 Dec step (+12,300 more if it is the same units). | +37,457 | 676,271 | PO!L20:M21; DeploySum!E19:F20 |
| I-32 | upside | SlipBot fleet fully depreciated or retired from Jan-27 (5010 = 0). | +1,353,574 | 1,992,388 | PO!M19; 'Depreciation Schedule'!B21 |
| I-32 | upside | Trend alternative: 5010 keeps falling at the 2026 rate (141,122 Jan-26 -> 112,798 Sep-26, (3,541)/month). | +276,164 | 914,978 | PO!B19, J19, M19 |
| I-32 | upside | Trend alternative continued from Sep-26: the same (3,541)/month decline also runs through Oct-Dec 26, so Jan-27 starts 4 months below Sep-26 (98,636 in Jan-27, 59,689 in Dec-27; floored at 0, 0 months at the floor). | +403,624 | 1,042,438 | PO!B19, J19, M19 |
| I-33 | two-way | Peripherals life 60 months instead of 84 (a longer life, e.g. 120 months, gives the opposite sign). | (25,534) | 613,279 | 'Depreciation Schedule'!B11 |
| I-34 | upside | FE payroll tax and benefits at the FE HC rates (4.069% / 7.223%) instead of the SD rates (6.8% / 16.4%) on the same FE salary base. | +109,539 | 748,353 | Fld Eng Budget!B22:B23; 'HC-FE'!D6:D7; FE!AG68:AG69 |
| I-34 with FE tax at 7.65% | upside | The HC T&B tax rates are below the 7.65% employer FICA and unverified (I-37). If FE payroll tax cannot be below 7.65%, the 6630 part of I-34 (+25,120) goes and the SD 6.8% is short: upside benefits only. | +76,600 | 715,413 | 'HC-FE'!D6:D7; Fld Eng Budget!B22:B23 |
| I-37 | downside | CO and PE payroll tax uses the HC T&B rates (CO 5.22%, PE 3.57%), below 7.65%; at 7.65% on every salary dollar (upper bound). v8: PO's part (v7 21,081) is gone: PO production payroll is capitalised at the model's own rates. | (56,801) | 582,013 | 'HC-CO'!D6; 'HC-PE'!D6; CO!AG68; PE!AG68 |
| I-37 | downside | FO and FE payroll tax uses the SD field rate 6.8%, also below 7.65% (same upper-bound basis; FO salary base 3,100,031 incl. the ramp, FE 919,884). | (34,169) | 604,644 | Fld Ops Payroll!B7; Fld Eng Budget!B22 |
| I-35 | upside | PE HC r22 Head of Production and Delivery ('transfer?') leaves COO from Jan-27. 0 if the role moves to another COO department and is budgeted there once. (per-person amount rounded to $5k) | +~255,000 | ~895,000 | 'HC-PE'!A22, Z22; PE!AG67:AG69 |
| I-36 | upside | The Aug-27 Customer Support Specialist hire on Fld Eng Budget (not on FE HC) is not approved. | +33,967 | 672,781 | Fld Eng Budget!B19:C19, row 65 |
| I-39 | upside | FE HC r35 Field Engineer Manager is an open seat (HC-FE 'Open Positions'), not an employee; COO book _2 leaves it out and Fld Eng Budget r20 costs it from Jan-27. If the seat stays open all of 2027 (salary + SD burden). | +173,774 | 812,587 | 'HC-FE'!B34:F35; Fld Eng Budget!A20:C20, row 66 |
| A-14 | upside | Depreciation convention: mid-month in the go-live month instead of a full month (new units and, from v8, their capitalised labour: +12,578 of it). | +149,995 | 788,809 | 'Depreciation Schedule'!B13 |
| A-14 | upside | Depreciation convention: start the month after go-live (B13 = 1), recalculated; of which capitalised labour +25,157. | +299,990 | 938,803 | 'Depreciation Schedule'!B13 = 1 |
| A-22 | downside | Revenue rests on unsigned / forecast bookings (Sep-Dec 26 includes 2,264,000 unsigned at 100%). Revenue effect not determinable from the workbook. | n/d | n/d | DeploySum!A49 (note 5), row 40 |

**Sign-flip statement (computed, v8):** with production labour capitalised the 2027 COO contribution is 638,814 (v7 139,032). No single quantified item turns it negative: the largest single downsides leave 37,696 (scope sensitivity: current 9 expensed), 167,721 (I-17 + I-41 at the 7-overlap), 240,321 (I-17 deduplicated, 9-overlap) and 254,389 (I-10). Pairs that turn it negative: the sensitivity (current 9 expensed) + I-17 deduplicated (9-overlap) (360,797); the sensitivity (current 9 expensed) + I-17 (298,834); the sensitivity (current 9 expensed) + I-10 (346,729); the sensitivity (current 9 expensed) + I-31 shortfall (1,361); I-17 + I-41 (7-overlap) + I-10 (216,704); I-17 deduplicated (9-overlap) + I-10 (144,104); I-17 + I-10 (82,141). Upside: I-32 can add up to 1,353,574 (contribution 1,992,388); the trend alternative adds 276,164 (914,978), or 403,624 (1,042,438) if the decline also ran through Oct-Dec 26. Policy scope: without the Oct-Dec 26 labour +48,621 (687,435). Smaller: A-14 +149,995 to +299,990, I-28 +78,529 to +~95,000, I-34 +109,539, I-35 up to +~255,000, I-36 +33,967, I-39 up to +173,774. With costs held fixed, revenue 638,814 (4.1%) below plan also takes the contribution to zero.

**Range (v8):** asymmetric by construction, as in v7. Lower bound 1, booked policy, all quantified downsides (I-17 + I-41 at the 7-overlap, the more adverse reading; I-10; I-31 shortfall; I-05 burden capitalised; run-rate labour): (273,550). Lower bound 2, the same under the scope sensitivity (current 9 expensed; I-17 deduplicated at the 9-overlap, the more adverse reading there): (802,068). Upper end, I-32 in full only: 1,992,388. I-37 (unverified upper bound) is not in the range. v7 range: (2,723,481) to 1,492,606 (with production labour expensed).

| Bound | What it adds to the headline | 2027 COO contribution |
|---|---|---:|
| Lower bound 1 (booked policy, all quantified downsides) | I-17 + I-41 (7-overlap); I-10; I-31 shortfall; I-05 burden capitalised; run-rate labour | (273,550) |
| Lower bound 2 (scope sensitivity: current 9 expensed) | sensitivity; I-17 deduplicated (9-overlap); I-10; I-31 shortfall; I-05 burden; run-rate labour | (802,068) |
| Point estimate | - | 638,814 |
| Upper end | I-32 in full only | 1,992,388 |

**Conclusion:** capitalising production labour (Decision #1) moves the 2027 COO contribution from 139,032 to 638,814, and with it the sign question: no single quantified item now turns it negative, but two together can (the pairs listed above). Treat 638,814 as a point estimate inside (273,550) to 1,992,388 (lower bound 2 with the current staff expensed: (802,068)) until Decisions #10, #6 and #2 (I-40, I-17, I-32) are answered.

## Changes from v7

| Item | Point | What v8 did | Where |
|---|---|---|---|
| Policy | Decision #1 RESOLVED | Production labour capitalised (user-confirmed 2026-10-10); primary case: all Prod Payroll labour incl. the current 9 (brief v5). | Decisions pending #1; I-05 |
| Prod Payroll | XLOOKUP not evaluated by LibreOffice | 16 cells (B48:Q48) -> INDEX/MATCH equivalent; no other model cell edited. Model errors 430 -> 0; 2027 2,592,893.90 = Python replica (diff 4.7e-10). | Prod Payroll!B48:Q48 |
| Depreciation Schedule | Capitalised-labour block | New sections 8-10 (rows 128-216): labour by build month, per unit, by go-live vintage, by GL, memo; switches B131 / B132; rows 1-126 unchanged. | 'Depreciation Schedule'!A128:S216 |
| PO 5011 / 5012 | Labour depreciation booked | +118,078 / +34,961 (formulas: section 4 + section 9). | PO!U20:AF21 |
| PO 5110-5140 | Capitalised | 652,820 -> 0: formulas =(1 - B131) x the v7 amount, labelled CAPITALISED in column AI. | PO!U33:AF35, AI33:AI35 |
| Headline | Contribution | 139,032 -> 638,814 (+499,782 = 5100 removed 652,820 less labour depreciation 153,038). | COO P&L!AG132 |
| Caveats | Recomputed | Expensed / capitalised-on-top / inside-unit-cost rows removed (resolved); scope alternatives (I-40), material-handling roles (I-41), run-rate labour, I-05 burden added; A-14 and I-37 recomputed; carried rows act on the new headline. Sign-flip and range recomputed. | Headline caveats |
| Issues | Updated | I-05 RESOLVED; I-40 (HIGH) and I-41 (MED) new; I-07, I-11, I-14, I-17, I-23, I-25, I-37, I-38 updated. | Issues (v8) |
| Decisions pending | Updated | #1 RESOLVED; #6 reworded (warehouse payroll); #10 new (scope of the policy). | Decisions pending |
| Privacy | Wording | v7's wording that every per-person amount in the md is rounded is withdrawn: salaries that are $5k multiples are unchanged by the $5k rounding, so some unique-role salaries appear exactly (counted in the completion criteria). | banner; completion criteria |

The verifier's v7 note (privacy wording) is addressed in the banner. v7's own changes from v6 are listed in `02-build_notes_v7.md` and still apply.

## Production labour: capitalised (Decision #1 RESOLVED)

User, 2026-10-10: 'production labor is capitalized. Use the same formula as the file has.' Brief v5 reads 'the file's formula' as the SD Prod Payroll model for the labour and the existing Depreciation Schedule logic for the capitalisation. v8 books the primary case: **all production payroll in the model is capitalised, including the 9 current PO staff**, and PO 5110-5140 2027 goes to 0 (formulas, labelled CAPITALISED in PO column AI). The sensitivity (only the ramp capitalised, the current 9 expensed) is shown, not booked.

### 1. Prod Payroll computes in the workbook (XLOOKUP replaced)

LibreOffice does not evaluate XLOOKUP, so v7's Prod Payroll showed #NAME? in 430 cells (tray and supervisor rows) and v6/v7 evaluated it in a scratch copy (A-28). v8 replaces only the 16 XLOOKUP cells of row 48 ('staffing tier used, trays/week') with an equivalent that LibreOffice and Excel both evaluate: the smallest tier >= x (exact match, else the next tier up), or MAX(tiers) if x is above every tier. On the ascending, unique tier row B20:O20 (checked), MATCH(x, r, 1) is the position of the largest tier <= x, and ISNA(MATCH(x, r, 0)) adds 1 when x is not itself a tier; below the first tier IFERROR gives 0 + 1. No other Prod Payroll cell is edited.

| Cell | Old formula (v7) | New formula (v8) | x = MAX(C8, trays/week) | Tier v8 (LibreOffice) | Tier v7 scratch (SMALL/COUNTIF) | Tier Python replica |
|---|---|---|---|---|---|---|
| B48 | `=_xlfn.xlookup(MAX($C$8,B47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,B47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,B47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,B47),$B$20:$O$20,0))))` | 10.00 | 10 | 10 | 10 |
| C48 | `=_xlfn.xlookup(MAX($C$8,C47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,C47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,C47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,C47),$B$20:$O$20,0))))` | 10.00 | 10 | 10 | 10 |
| D48 | `=_xlfn.xlookup(MAX($C$8,D47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,D47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,D47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,D47),$B$20:$O$20,0))))` | 14.00 | 20 | 20 | 20 |
| E48 | `=_xlfn.xlookup(MAX($C$8,E47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,E47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,E47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,E47),$B$20:$O$20,0))))` | 10.00 | 10 | 10 | 10 |
| F48 | `=_xlfn.xlookup(MAX($C$8,F47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,F47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,F47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,F47),$B$20:$O$20,0))))` | 10.00 | 10 | 10 | 10 |
| G48 | `=_xlfn.xlookup(MAX($C$8,G47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,G47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,G47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,G47),$B$20:$O$20,0))))` | 21.50 | 30 | 30 | 30 |
| H48 | `=_xlfn.xlookup(MAX($C$8,H47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,H47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,H47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,H47),$B$20:$O$20,0))))` | 13.77 | 20 | 20 | 20 |
| I48 | `=_xlfn.xlookup(MAX($C$8,I47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,I47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,I47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,I47),$B$20:$O$20,0))))` | 22.87 | 30 | 30 | 30 |
| J48 | `=_xlfn.xlookup(MAX($C$8,J47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,J47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,J47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,J47),$B$20:$O$20,0))))` | 16.48 | 20 | 20 | 20 |
| K48 | `=_xlfn.xlookup(MAX($C$8,K47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,K47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,K47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,K47),$B$20:$O$20,0))))` | 19.83 | 20 | 20 | 20 |
| L48 | `=_xlfn.xlookup(MAX($C$8,L47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,L47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,L47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,L47),$B$20:$O$20,0))))` | 27.55 | 30 | 30 | 30 |
| M48 | `=_xlfn.xlookup(MAX($C$8,M47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,M47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,M47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,M47),$B$20:$O$20,0))))` | 27.55 | 30 | 30 | 30 |
| N48 | `=_xlfn.xlookup(MAX($C$8,N47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,N47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,N47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,N47),$B$20:$O$20,0))))` | 37.10 | 40 | 40 | 40 |
| O48 | `=_xlfn.xlookup(MAX($C$8,O47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,O47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,O47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,O47),$B$20:$O$20,0))))` | 32.97 | 40 | 40 | 40 |
| P48 | `=_xlfn.xlookup(MAX($C$8,P47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,P47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,P47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,P47),$B$20:$O$20,0))))` | 42.70 | 50 | 50 | 50 |
| Q48 | `=_xlfn.xlookup(MAX($C$8,Q47),$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)` | `=IF(MAX($C$8,Q47)>MAX($B$20:$O$20),MAX($B$20:$O$20),INDEX($B$20:$O$20,IFERROR(MATCH(MAX($C$8,Q47),$B$20:$O$20,1),0)+ISNA(MATCH(MAX($C$8,Q47),$B$20:$O$20,0))))` | 49.68 | 50 | 50 | 50 |

**Proof (model totals within $1 of the Python replica):** the replica rebuilds the whole model from its input cells (grids, rates, raise, absence, DeploySum builds) with no cached model value.

| Prod Payroll 2027 (S41 / S62 / S79 / S81) | v8 workbook (LibreOffice) | Python replica (from input cells) | Difference |
|---|---:|---:|---:|
| lift | 1,622,423.15 | 1,622,423.15 | -2.3e-09 |
| tray | 729,177.00 | 729,177.00 | -4.7e-10 |
| sup | 241,293.75 | 241,293.75 | 0.0e+00 |
| total | 2,592,893.90 | 2,592,893.90 | 4.7e-10 |

Every month of rows 41, 62, 79 and 81 (Sep-26..Dec-27): max difference replica vs v8 4.7e-10; v7 scratch (SMALL/COUNTIF) vs v8 0.0e+00. Prod Payroll errors: v7 430, v8 0. The handoff's verified figures hold: 2027 2,592,893.90 (lift 1,622,423.15, tray 729,177.00, supervisors 241,293.75); the 9 current staff at model rates 630,504.48; builds 2027 312 lifts / 1,355 trays, of which live in 2027 222 / 952.

### 2. Method (Depreciation Schedule sections 8-10, rows 128-216)

1. Labour by build month: Prod Payroll rows 41 (lift), 62 (tray), 79 (supervisors), Sep-26..Dec-27, same columns B:Q (rows 137-140).
2. Capitalised share: all of it (B131 = 1). With B131 = 0 the model's own cost of the current staff (rows 141-142, same cost formula at 7 lift + 2 tray, no hires) is left out and PO 5110-5140 returns to its v7 amount.
3. Supervisors to lifts / trays pro rata to the month's lift : tray labour (A-37, v7 A-32 by month).
4. Labour per unit built = the month's labour / units built that month (DeploySum rows 24/25). Oct-26 and Jan-27 build nothing; their labour waits and joins the next build month (A-38).
5. Each unit's labour joins its go-live vintage 2 months later (B133; check B134 = 0: DeploySum go-lives equal the builds 2 months earlier in every 2027 month) and is depreciated exactly like the unit: full month from go-live (+B13), 84 months lifts (5011), 120 months trays (5012), salvage B12 (A-39). Peripherals (5020) carry no labour.
6. Sep-Dec 26 model months (A-40): Sep-26 builds go live Nov-26 (a 2026 vintage inside the PO run rate, so its labour, 90,851, is not added; see the run-rate row in the caveats); Oct-26 rolls into Nov-26; the Nov-26 and Dec-26 builds are the Jan-27 and Feb-27 go-lives and carry the Oct-Dec 26 labour (381,863; switch B132).
7. Builds for 2028 go-lives (Nov-Dec 27) carry 650,571 of labour with no 2027 depreciation (CIP / inventory, A-41).
8. Output: section 9 rows 193/194 by GL, added to PO rows 20/21 (U:AF). Section 4 (rows 79-82) is unchanged and still shows the units only; row 197 = total.

### 3. Labour per unit, by build month

| Build month | Prod Payroll (row 81) | Capitalised: lifts (row 147) | Capitalised: trays (row 148) | Lifts built | Trays built | Lift labour pooled (row 152) | Tray labour pooled (row 154) | Labour per lift (row 156) | Labour per tray (row 157) | Go-live |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sep-26 | 90,851 | 69,733 | 21,118 | 9 | 32 | 69,733 | 21,118 | 7,748 | 660 | Nov-26 |
| Oct-26 | 81,851 | 62,902 | 18,949 | 0 | 0 | 0 | 0 | 0 | 0 | Dec-26 |
| Nov-26 | 155,879 | 112,625 | 43,254 | 20 | 60 | 175,527 | 62,203 | 8,776 | 1,037 | Jan-27 |
| Dec-26 | 144,133 | 104,709 | 39,425 | 8 | 24 | 104,709 | 39,425 | 13,089 | 1,643 | Feb-27 |
| Jan-27 | 140,751 | 102,249 | 38,503 | 0 | 0 | 0 | 0 | 0 | 0 | Mar-27 |
| Feb-27 | 181,250 | 121,669 | 59,581 | 22 | 86 | 223,918 | 98,083 | 10,178 | 1,141 | Apr-27 |
| Mar-27 | 175,250 | 118,761 | 56,489 | 14 | 61 | 118,761 | 56,489 | 8,483 | 926 | May-27 |
| Apr-27 | 175,250 | 118,761 | 56,489 | 20 | 98 | 118,761 | 56,489 | 5,938 | 576 | Jun-27 |
| May-27 | 176,685 | 119,735 | 56,950 | 18 | 73 | 119,735 | 56,950 | 6,652 | 780 | Jul-27 |
| Jun-27 | 178,120 | 120,709 | 57,411 | 22 | 85 | 120,709 | 57,411 | 5,487 | 675 | Aug-27 |
| Jul-27 | 212,417 | 151,569 | 60,848 | 28 | 122 | 151,569 | 60,848 | 5,413 | 499 | Sep-27 |
| Aug-27 | 202,828 | 143,772 | 59,056 | 28 | 122 | 143,772 | 59,056 | 5,135 | 484 | Oct-27 |
| Sep-27 | 240,150 | 160,893 | 79,257 | 34 | 159 | 160,893 | 79,257 | 4,732 | 498 | Nov-27 |
| Oct-27 | 259,621 | 182,382 | 77,240 | 36 | 146 | 182,382 | 77,240 | 5,066 | 529 | Dec-27 |
| Nov-27 | 318,497 | 215,701 | 102,796 | 42 | 183 | 215,701 | 102,796 | 5,136 | 562 | Jan-28 |
| Dec-27 | 332,074 | 233,043 | 99,031 | 48 | 220 | 233,043 | 99,031 | 4,855 | 450 | Feb-28 |

### 4. Capitalised labour: 2027 total, depreciated in 2027 vs carried into 2028

| Item | Value | Depreciation Schedule cell |
|---|---:|---|
| Production payroll 2027 (Prod Payroll!S81) = capitalised labour from 2027 payroll | 2,592,894 | B201, B202 |
|   into 2027 go-lives (Feb-Oct 27 builds; Jan-27 rolls into Feb-27): depreciated from go-live | 1,942,323 | B203 |
|   into 2028 go-lives (Nov-Dec 27 builds): CIP / inventory at Dec-27, no 2027 depreciation | 650,571 | B204 |
|   waiting for a build at Dec-27 | 0 | B205 |
| Oct-Dec 26 model labour into the Jan-Feb 27 go-lives (Nov-Dec 26 builds; Oct-26 rolls into Nov-26) | 381,863 | B208 |
| Sep-26 model labour in the Nov-26 go-lives (2026 vintage, inside the PO run rate; not added) | 90,851 | B209 |
| Depreciable labour in the 2027 go-live vintages (2027 + Oct-Dec 26 labour) | 2,324,186 | B210 |
| 2027 depreciation of capitalised labour (5011 / 5012) | 153,038 (118,078 / 34,961) | R195 (rows 193-194) |
| Capitalised labour in service at Dec-27, net of 2027 depreciation | 2,171,148 | B213 |
| Average labour per unit built in 2027: lift / tray | 5,735 (8.8% of 65,000) / 593 (7.4% of 8,000) | B215:B216 |

So of the **2,592,894 of 2027 production payroll capitalised**, 1,942,323 sits in units that go live in 2027 and are depreciated from go-live, and **650,571 is carried into 2028 go-lives** (CIP / inventory at Dec-27). The 2027 vintages also carry 381,863 of Oct-Dec 26 labour. 2027 depreciation of the labour: **153,038** (5011 118,078, 5012 34,961).

| Line | v7 | v8 | Change |
|---|---:|---:|---:|
| 5010 | 1,353,574 | 1,353,574 | 0 |
| 5011 | 1,248,196 | 1,366,273 | +118,078 |
| 5012 | 418,898 | 453,859 | +34,961 |
| 5020 | 298,140 | 298,140 | 0 |
| 5110 (PO row 33) | 525,310 | 0 | (525,310) |
| 5130 (PO row 34) | 19,105 | 0 | (19,105) |
| 5140 (PO row 35) | 108,404 | 0 | (108,404) |
| 2027 COO contribution (COO P&L AG132) | 139,032 | 638,814 | +499,782 |

### 5. Hand recompute of one month: Jun-27

Vintages in service in Jun-27 under the full-month rule: Jan-Jun 27 go-lives (Mar-27 has none). Labour per unit from the build month (table above).

| Go-live vintage | Built | Lifts | Labour per lift | 5011 per month | Trays | Labour per tray | 5012 per month |
|---|---|---:|---:|---:|---:|---:|---:|
| Jan-27 | Nov-26 | 20 | 8,776.35 | 20 x 8,776.35 / 84 = 2,089.61 | 60 | 1,036.72 | 60 x 1,036.72 / 120 = 518.36 |
| Feb-27 | Dec-26 | 8 | 13,088.59 | 8 x 13,088.59 / 84 = 1,246.53 | 24 | 1,642.69 | 24 x 1,642.69 / 120 = 328.54 |
| Apr-27 | Feb-27 | 22 | 10,178.10 | 22 x 10,178.10 / 84 = 2,665.69 | 86 | 1,140.50 | 86 x 1,140.50 / 120 = 817.36 |
| May-27 | Mar-27 | 14 | 8,482.94 | 14 x 8,482.94 / 84 = 1,413.82 | 61 | 926.05 | 61 x 926.05 / 120 = 470.74 |
| Jun-27 | Apr-27 | 20 | 5,938.06 | 20 x 5,938.06 / 84 = 1,413.82 | 98 | 576.42 | 98 x 576.42 / 120 = 470.74 |
| **Hand total Jun-27** |  |  |  | **8,829.48** |  |  | **2,605.74** |
| Workbook: PO!Z20 / Z21 v8 - v7 |  |  |  | 8,829.48 |  |  | 2,605.74 |

Hand vs workbook: max difference 6.4e-11 (also = 'Depreciation Schedule'!K193 8,829.48 and K194 2,605.74). The whole block is also rebuilt in Python from the replica payroll: max difference 3.3e-09 over every row of sections 8-10.

### 6. Sensitivity (current 9 expensed) and the other scope alternatives

| Case | 2027 payroll capitalised | 2027 labour depreciation | PO 5110-5140 2027 (expense) | 2027 COO contribution | vs booked |
|---|---:|---:|---:|---:|---:|
| Booked (primary): all Prod Payroll labour capitalised, incl. the current 9 and Oct-Dec 26 labour | 2,592,894 | 153,038 | 0 | 638,814 | - |
| Sensitivity (shown, not booked): only the ramp capitalised; the current 9 stay expensed | 1,962,389 | 101,336 | 652,820 | 37,696 | (601,118) |
| Alternative: Oct-Dec 26 labour not capitalised | 2,592,894 | 104,417 | 0 | 687,435 | +48,621 |
| Both alternatives | 1,962,389 | 73,095 | 652,820 | 65,936 | (572,877) |
| v7 headline (labour not capitalised; ramp not budgeted) | - | 0 | 652,820 | 139,032 | (499,782) |

Each case is a LibreOffice recalculation of a scratch copy of v8 with the switch changed (scen_v8.py), checked against the Python replica (difference < 1e-6). The sensitivity books PO 5110-5140 at the v7 amount (652,820, the PO HC roster) and capitalises the ramp only: 2027 labour 1,962,389, depreciation 101,336, contribution **37,696** ((601,118) vs booked).

### 7. Bridge from v7's verified 64,735

| Step | 2027 depreciation | Note |
|---|---:|---|
| v7 'capitalised on top' (ramp only; annual average per unit built in 2027; 2027 labour only) | 64,735 | v7 figure, reproduced |
| + the current 9 (whole model, v7 method) | +21,754 | = 86,490 |
| + labour per unit by build month, zero-build months rolled forward (A-38) | +17,927 | = 104,417 (= switch B132 = 0) |
| + Oct-Dec 26 labour in the Jan-Feb 27 go-lives (A-40) | +48,621 | = 153,038 (booked) |
| Sensitivity on the same method (ramp only, monthly, incl. Oct-Dec 26 ramp labour) | 101,336 | v7 method 64,735; difference +36,601 |

v7's method (ramp only, annual average labour per unit built in 2027, 2027 labour only) is reproduced exactly (64,735.34). v8 keeps its parts (model split, supervisors pro rata, 2-month lag, Depreciation Schedule rules) and applies them by build month, as brief v5 asks: early builds carry more labour per unit (Nov-26 to Feb-27: up to 13,089 per lift) and are in service longer in 2027, so the monthly method depreciates more in 2027 than the annual average.

### 8. Interactions not booked

- **Material-handling roles (I-41).** PO 5110-5140 = 0 removes the 2 material-handling roles too. On the 7-of-9 role reading they are warehouse staff and their cost (134,563 together at PO HC rates) should stay an expense.
- **Logistics&WH (I-17).** Unchanged as an expense (336,530); deduplicated with the capitalised Prod Payroll 398,492 (9-overlap) or 471,093 (7-overlap, with I-41).
- **Existing-fleet run rate.** The PO Dec-26 run rate carries no labour; the Sep-26 labour in the Nov-26 go-lives would add 12,074 of 2027 depreciation (earlier 2026 go-lives not determinable).
- **2026 columns.** PO and COO P&L 2026 (B:N) are unchanged: 2026 still expenses its 5100 production labour (I-40). The Prod Payroll Sep-Dec 26 model columns now compute (they were #NAME? for trays and supervisors); they are model months, not P&L 2026 columns.

## Prod Payroll overlap: 9 by count vs 7 by role (B2)

v8 note: with production labour capitalised, the overlap no longer changes an expensed ramp. It decides two things: whether the 2 material-handling roles belong in the capitalised labour at all (7 reading: no, I-41, 134,563) and how I-17 is deduplicated (398,492 at 9, 471,093 at 7). The v7 text below (I-05 as an expensed net increment) is history.

Prod Payroll has no names or titles. Its 'current staff on payroll (Sep-26)' is 7 lift + 2 tray = 9, which equals the PO HC headcount. But PO HC's 9 are 7 production staff and 2 material-handling roles (1 Material Handling Team Lead, 1 Material Handler). Both material-handling roles are tied to the Logistics&WH model: PO HC r20 is seat MH-01 by name, and seat MH-02 backfills PO HC r16. v6 used the count match only.

| Reading | Who overlaps | I-05 net | I-17 net | I-05 + I-17 |
|---|---|---:|---:|---|
| 9 of 9 by count (v6) | all 9 PO HC people = Prod Payroll's 9 current staff (7 lift + 2 tray, no names in the model) | 1,962,389 | 336,530 | 2,298,919 as shipped in v6: PO HC r20 taken out twice (in I-05 by count, in I-17 as MH-01 by name). Deduplicated, MH-01 counts as a new seat: 2,360,882 |
| 7 of 9 by role (critic B2) | the 7 production staff (2 Team Lead, 2 Senior Production Technician, 1 Production Technician, 2 Production Associate) are Prod Payroll current staff; r20 Material Handler = MH-01 (name) and r16 Material Handling Team Lead (backfilled by MH-02) belong with Logistics&WH | 2,102,502 (+140,112: 2 model seats at 70,056 each) | 336,530 | 2,439,031 (no seat taken out twice) |

**Which seats v6 subtracted twice.** v6's combined 2,298,919 is I-05 + I-17 as computed separately. I-05 takes all 9 PO HC people out of Prod Payroll by count, PO HC r20 included. I-17 takes PO HC r20 out of Logistics&WH again, as seat MH-01 by name, so one person is subtracted twice. One person fills one seat. Keeping the count match (9 reading), MH-01 is an unfilled seat and comes back into I-17: 2,360,882 (+~60,000). On the 7 reading, r20 is MH-01 and r16 sits with Logistics&WH, so Prod Payroll's 9 current seats hold the 7 production staff plus 2 seats no roster fills. Those 2 seats are costed at the model's average current cost per head (70,056; 69,992 lift, 70,280 tray; A-34): I-05 2,102,502 and combined 2,439,031, with nothing subtracted twice. PO HC r16 itself stays budgeted in PO all of 2027 under both readings (I-17: if r16 leaves the role MH-02 backfills, PO HC is overstated).

## Other v7 checks (critic v6 O1-O8, verifier V1; v7 figures)

v8 note: O1 (I-05 at PO HC burden rates, +141,924) is now capitalised: 2027 effect (5,715) (caveat row). O7's range is replaced by the v8 range. The rest is unchanged.

| Item | Point | Finding | Source |
|---|---|---|---|
| O1 | I-05 at PO HC burden rates | PO HC 24.3% of salary vs the model's 15.6%: +141,924; ramp 2,104,313 (9-overlap) | 'HC-PO'!D6:D7; Prod Payroll B6:C7, H6:H7 |
| O2 | SD models may be older than the roster | Prod Payroll Sep-Dec 26 hires 15 (Sep-26: 3 lift, 1 tray, 1 sup; Nov-26: 6 lift, 3 tray, 1 sup); Logistics&WH TL-01 Material Handling Team Lead Dec-26, MH-02 Material Handler Oct-26; none on the HC rosters (workfile saved 2026-10-07). Question: when were the models last updated? (I-38) | Prod Payroll rows 31, 52, 71; HC tabs |
| O3 | FO/FE person | Probable duplicate (name match only; title/salary differ; likely FO->FE move); upside pro rata to the months after the move (about 6,544 per month on the FO side) | I-28; Decision #7 |
| O4 / V1 | I-28 FO side with knock-ons | Fld Ops Payroll B11 14 -> 13, LibreOffice recalculation: +78,529.08 = payroll +78,198.12 + 5330 +330.96 (Fld Maint Budget!B29); supervisor headcount unchanged (True); after 217,561 (v6: +78,198, 217,230) | scen_v7.py; COO P&L!AG46, AG52:AG54 |
| O5 | FE HC r35 is an open seat | 'Open Positions' (HC-FE row 34), no employee; A-29 amended (start relaxed); _2 excludes it, SD costs it from Jan-27: up to +173,774 (I-39) | 'HC-FE'!B34:F35; Fld Eng Budget r20 |
| O6 | HC T&B tax rates below FICA | all five below 7.65% (3.57%-6.85%); PO/CO/PE up to (77,882); I-34 +76,600 if FE tax at 7.65% (I-37) | 'HC-*'!D6 |
| O7 | Range asymmetry | lower bound 1 (2,723,481) (9-overlap (2,645,332)); lower bound 2 (excl. I-05) (620,980); I-05 capitalised on top (690,337); upper 1,492,606 | Sign-flip statement |
| O8 | Privacy | CONFIDENTIAL banner (md and Collation Notes); per-person amounts rounded to $5k in the md (A-35); no per-person CSV written in v7; scratch name lists deleted | md; Collation Notes; run_build_v7.sh |

| Dept | HC T&B tax rate | Below 7.65%? | Rate used in the budget | 2027 tax gap at 7.65% (upper bound) |
|---|---:|---|---|---:|
| FO | 6.847% | yes | SD 6.8% | 26,350 |
| PO | 3.637% | yes | HC rate | 21,081 |
| CO | 5.221% | yes | HC rate | 12,834 |
| FE | 4.069% | yes | SD 6.8% | 7,819 |
| PE | 3.571% | yes | HC rate | 43,967 |

The tax-gap column is the 2027 salary base times (7.65% less the rate used); PO, CO and PE on the HC salaries (77,882 together), FO and FE on the SD salary base. It ignores the Social Security wage base, which lowers the true rate for salaries above it, so it is an upper bound (I-37, A-31).

## Payroll reconciliation

v8 note: PO 5110-5140 2027 is now 0 (capitalised; I-05 RESOLVED). The reconciliation below (v6/v7) compares the PO HC roster (652,820, the amount removed from PO and restored by the sensitivity) with the SD models; for Prod Payroll the 'net increment not in the budget' no longer applies, because the whole model is in the budget as capitalised labour (2,592,894 for 2027). Logistics&WH stays outside (I-17, I-41).

Sources: the HC tabs of `COO_HC_and_PL_workfile.xlsx` (now HC-FO ... HC-COO in the workbook; one row per person, 2027 = columns M:X), the P&L payroll lines of the v6 workbook (= v5), the COO book _2, and the SD payroll models (Fld Ops Payroll, Fld Eng Budget and Prod Payroll in the workbook; Logistics&WH Payroll in the SD book, not carried). People are identified by roster + row + title; names were used only inside recon_v6.py to match people. v7: per-person amounts are rounded to the nearest $5k in this file (A-35). 'Current' = on payroll before 2027 and on an HC roster; 'ramp' = hires the SD models add. All amounts are 2027 (Jan-Dec), salary + payroll tax + benefits unless stated.

### Summary by department

| Dept | GL | HC roster: people, 2027 total | v6 P&L line (= v5) | COO book _2 | SD model 2027 | Current staff in the SD model | Ramp in the SD model | Overlaps found | Net increment not in the budget |
|---|---|---|---|---|---|---|---|---|---|
| FO | 5510-5540 | 16; 1,341,298 | 3,957,239 | 1,341,298 | Fld Ops Payroll 3,957,239 | 16 = FO HC 16; 1,338,696 | 2,618,543 | FO HC r15 also on Fld Eng Budget r15 (I-28) | 0 (the SD model is the budget) |
| PO | 5110-5140 | 9; 652,820 | 652,820 | 652,820 | Prod Payroll 2,592,894; Logistics&WH 547,441 | Prod Payroll 9 (count) 630,504; Logistics&WH 2 seats 210,912 | Prod Payroll 1,962,389; Logistics&WH 336,530 | 9 of 9 in Prod Payroll by count, or 7 of 9 by role (B2); r20 = Logistics&WH MH-01 (name); r16 backfilled by MH-02 | 2,360,882 (9, deduplicated) or 2,439,031 (7); v6 summed 2,298,919, which takes r20 out twice |
| CO | 6610-6640 | 5; 618,961 | 618,961 | 618,961 | none (r17 is Logistics&WH LOG-01) | - | - | r17 = Logistics&WH LOG-01 (name) | 0 |
| FE | 6610-6640 | 7 + 1 open row; 908,980 | 1,133,298 | 752,002 | Fld Eng Budget 1,133,298 | 7 of 7 matched (6 people by name, 1 open seat r35 by title + salary) | Aug-27 hire 33,967 (I-36) | Fld Eng Budget r15 = FO HC r15 (I-28) | 0 (the SD model is the budget) |
| PE | 6610-6640 | 9; 1,211,637 | 1,211,637 | 1,211,637 | none | - | - | none; r22 'transfer?' (I-35) | 0 |

HC roster vs P&L line, monthly: PO, CO and PE 2027 P&L payroll equal their HC rows 67-69 in every month (max difference: PO 0.00, CO 0.00, PE 0.00). FO and FE P&L come from the SD models (I-02); the COO book _2 equals FO HC exactly and equals FE HC less the Field Engineer Manager row.

### FO: Fld Ops Payroll (FO 5510-5540) split into current staff and ramp

| Block (Fld Ops Payroll rows) | Who | Salary | New-hire cost | Payroll tax | Benefits | Total 2027 | Headcount Jan-27 -> Dec-27 |
|---|---|---:|---:|---:|---:|---:|---|
| Current techs (20-24) | 14 = FO HC field technicians 14 (count; model average 63,000) | 888,615 | 0 | 60,426 | 145,733 | 1,094,774 | 14 -> 14 |
| Management & coordination (76-80) | FO HC r21 Operations Coordinator, r25 Field Maintenance Manager (name + salary) | 197,989 | 0 | 13,463 | 32,470 | 243,922 | 2 -> 2 |
| **Current staff (= FO HC 16)** |  | 1,086,604 | 0 | 73,889 | 178,203 | **1,338,696** | 16 -> 16 |
| New-logo techs (26-35) | ramp | 1,605,030 | 110,000 | 109,142 | 263,225 | 2,087,397 | 5 -> 58 |
| Expansion techs (37-47) | ramp | 257,722 | 20,000 | 17,525 | 42,266 | 337,514 | 0 -> 10 |
| Floaters (49-60) | ramp (switch M14 = No) | 0 | 0 | 0 | 0 | 0 | 0 -> 0 |
| Incremental supervisors (62-73) | ramp | 150,675 | 8,000 | 10,246 | 24,711 | 193,632 | 0 -> 4 |
| **Ramp hires** |  | 2,013,428 | 138,000 | 136,913 | 330,202 | **2,618,543** | 5 -> 72 |
| **Total = FO 5510 + 5530 + 5540** |  | 3,100,031 | 138,000 | 210,802 | 508,405 | **3,957,239** |  |

FO ramp headcount Jan..Dec 27: 5, 5, 10, 13, 18, 23, 30, 37, 44, 54, 63, 72. FO 5510 3,238,031 = salaries + new-hire cost (rows 21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77); the split ties to FO!U52:AF54 in every month (checked to 1e-6).

Reconciliation with the COO book's old FO (5510 1,088,252 = FO HC salary; 5510-5540 1,341,298 = FO HC total): the SD current-staff block has salary 1,086,604 ((1,648)) and total 1,338,696 ((2,602)). The coordinator and manager match to the dollar (2 people, combined 2027 salary 197,988.86, differences 0.00 and 0.00). The techs differ only because the model uses 14 x 63,000 = 882,000 where FO HC has 883,636 (2027 with the Oct-27 raise: 888,615 vs 890,263), and the burden rates differ slightly (SD 6.8% / 16.4%, FO HC 6.847% / 16.405%). So the old FO was the current 16 only; the SD build = the same 16 + 2,618,543 of ramp hires. One of the 14 techs (FO HC r15) is also costed on Fld Eng Budget r15 (I-28).

### PO: PO HC vs Prod Payroll and Logistics&WH Payroll (I-05, I-17)

PO 5110-5140 (652,820) is exactly PO HC: 9 current staff (2 Team Lead, 1 Material Handling Team Lead, 2 Senior Production Technician, 1 Production Technician, 1 Material Handler, 2 Production Associate); headcount every 2027 month 9 (min) to 9 (max), no hires, raise from Oct-27 like every roster.

**How many of the 9 appear in the SD models?** Prod Payroll: **9 of 9 by headcount** (its 'current staff on payroll (Sep-26)' is 7 lift + 2 tray = 9, 0 supervisors; the model has no names or titles, so this is a count match, not a person match). Logistics&WH: **1 of 9 by name** (PO HC r20 Material Handler = seat MH-01); PO HC r16 Material Handling Team Lead is named as the person seat MH-02 backfills (from Oct-26), but r16 stays on PO HC through Dec-27. The Logistics&WH model also holds CO HC r17 Field Logistics Manager (seat LOG-01, by name). If the 9 are Prod Payroll's current staff, PO HC r20 sits in both SD models, and the 'Both models' column below, as summed in v6, takes r20 out twice (inside I-05 by count, inside I-17 as MH-01). See 'Prod Payroll overlap: 9 by count vs 7 by role' for the two readings and the deduplicated figures (B2).

|  | PO HC / PO 5110-5140 | Prod Payroll (SD) | Logistics&WH Payroll (SD, not carried) | Both models |
|---|---:|---:|---:|---:|
| Model 2027 total | - | 2,592,894 (lift 1,622,423, tray 729,177, supervisors 241,294) | 547,441 | 3,140,335 |
| People already on an HC roster | 9 (652,820) | 9 current staff (count): model cost 630,504 | 2 seats: MH-01 (PO HC r20) ~60,000, LOG-01 (CO HC r17) ~150,000 | 841,416 |
| **Net increment (ramp) not in the budget** | 0 | **1,962,389** (I-05) | **336,530** (I-17): 7 seats | **2,298,919** (r20 out twice; deduplicated 2,360,882 / 2,439,031, B2) |
| Ramp headcount Jan-27 -> Dec-27 | 0 -> 0 | 15 -> 45 | 2 -> 7 | 17 -> 52 |
| Gross gap vs PO 5100 (model total - 652,820) | - | 1,940,074 | n/a (different team) | - |

Net increment = model total less the model's own cost of the people already on HC rosters (A-27), so it is the cost of the ramp hires at the model's rates. The model costs the 9 current staff at 630,504, 22,315 below PO 5100 (652,820): average salary 57,200.05 vs 57,933.33, and different burden (model tax 7.5%, benefits 7.5% lift / 8.0% tray, plus the monthly absence coverage of Prod Payroll rows 33/54; PO HC 3.64% / 20.64%). That difference is not part of the net increment. Ramp cost by component: salary 1,591,611, absence coverage 85,268, payroll tax 125,766, benefits 121,745, new-hire cost 38,000. The model already has 9 lift, 4 tray and 2 supervisor hires in Sep-Dec 26, so 2027 opens with 15 ramp staff. None of these 15, nor Logistics&WH TL-01 (Dec-26) and MH-02 (Oct-26), is on the HC rosters (workfile saved 2026-10-07): the models may predate the roster (I-38).

**Net ramp by month (2027)**

| Row | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | 2027 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Prod Payroll ramp headcount | 15 | 21 | 21 | 21 | 21 | 21 | 25 | 25 | 31 | 34 | 42 | 45 |  |
| Prod Payroll ramp cost | 89,063 | 129,562 | 123,562 | 123,562 | 124,535 | 125,509 | 159,345 | 150,217 | 188,461 | 206,382 | 264,783 | 277,410 | 1,962,389 |
| Logistics&WH new seats (headcount) | 2 | 3 | 4 | 4 | 4 | 5 | 7 | 7 | 7 | 7 | 7 | 7 |  |
| Logistics&WH new seats cost | 10,464 | 16,392 | 21,517 | 20,517 | 20,517 | 26,642 | 38,106 | 36,106 | 36,106 | 36,721 | 36,721 | 36,721 | 336,530 |
| **Net ramp headcount, both** | 17 | 24 | 25 | 25 | 25 | 26 | 32 | 32 | 38 | 41 | 49 | 52 |  |
| **Net ramp cost, both** | 99,527 | 145,953 | 145,078 | 144,078 | 145,052 | 152,151 | 197,450 | 186,323 | 224,567 | 243,103 | 301,504 | 314,131 | **2,298,919** (9 reading as summed in v6; see B2) |
| Prod Payroll total headcount (incl. the 9) | 24 | 30 | 30 | 30 | 30 | 30 | 34 | 34 | 40 | 43 | 51 | 54 |  |
|   of which lift / tray / supervisors (Dec-27) | 35 / 15 / 4 |  |  |  |  |  |  |  |  |  |  |  |  |

**Logistics&WH seats**

| Seat | Team | Start | Annual base | 2027 cost (model rates) | On an HC roster? | In net increment |
|---|---|---|---:|---:|---|---|
| LOG-01 Logistics Manager | Central Operations | on payroll | 120,000 | ~150,000 | CO HC r17 Field Logistics Manager (name) | no |
| INV-01 Inventory Control Specialist | Inventory control | Feb-27 | 48,000 | 55,652 | no | yes |
| TL-01 Material Handling Team Lead | Receiving & putaway | Dec-26 | 52,000 | 64,544 | title only: PO HC r16 Material Handling Team Lead (salary ~60,000, start Sep-26) | yes |
| TL-02 Material Handling Team Lead | Kitting & line replenishment | Jul-27 | 52,000 | 33,032 | title only: PO HC r16 Material Handling Team Lead (salary ~60,000, start Sep-26) | yes |
| MH-01 Material Handler | Receiving & putaway | on payroll | ~50,000 | ~60,000 | PO HC r20 Material Handler (name) | no |
| MH-02 Material Handler | Receiving & putaway | Oct-26 | ~50,000 | ~60,000 | backfills PO HC r16 Material Handling Team Lead; title only: PO HC r20 Material Handler (salary ~50,000, start Sep-26; already matched by name to another seat) | yes |
| MH-06 Material Handler | Receiving & putaway | Jul-27 | ~50,000 | 31,751 | title only: PO HC r20 Material Handler (salary ~50,000, start Sep-26; already matched by name to another seat) | yes |
| MH-03 Material Handler | Kitting & line replenishment | Mar-27 | ~50,000 | 52,712 | title only: PO HC r20 Material Handler (salary ~50,000, start Sep-26; already matched by name to another seat) | yes |
| MH-04 Material Handler | Kitting & line replenishment | Jun-27 | ~50,000 | 36,876 | title only: PO HC r20 Material Handler (salary ~50,000, start Sep-26; already matched by name to another seat) | yes |

Seats the model's own check block excludes: LOG-02 (Logistics&WH Payroll!A55; = FO HC r21 Operations Coordinator, budgeted in FO) and MH-05 (A56; in no model, I-27). Model rates: tax 6.8%, benefits 16.4%; Python replica of the seat costs vs the SD cached values: max difference 3.3e-06.

### CO

CO 6610-6640 (618,961) = CO HC: 5 people (4 current, 1 new hire), CO HC rates 5.22% / 11.91%. No SD model; CO HC r17 Field Logistics Manager is also seat LOG-01 of the not-carried Logistics&WH model (excluded from the I-17 net). Net increment 0.

### FE: FE HC vs Fld Eng Budget (FE 6610-6640)

| Fld Eng Budget row | Salary | Start (SD) | FE HC row | Match | Start (HC) | 2027 salary SD | 2027 salary HC | Difference |
|---|---:|---|---|---|---|---:|---:|---:|
| r13 Field Engineer | ~100,000 | Jan-27 | r14 Senior Field Robotics Engineer | name | Sep-26 | ~100,000 | ~100,000 | 0.00 |
| r14 Field Engineer | ~70,000 | Jan-27 | r15 Associate Field Robotics Engineer | name | Sep-26 | ~75,000 | ~75,000 | 0.00 |
| r15 Field Engineer | 75,000 | Jan-27 | - | not on FE HC; same name as FO HC r15 Field Technician | - | ~75,000 | - | ~75,000 |
| r16 Field Engineer | 70,000 | Jan-27 | r19 Associate Field Robotics Engineer | name | Sep-26 | ~70,000 | ~70,000 | 0.00 |
| r17 Customer Support Manager | 160,000 | Jan-27 | r17 Customer Support Manager | name | Sep-26 | ~160,000 | ~160,000 | 0.00 |
| r18 Customer Support Specialist | 65,000 | Jan-27 | r18 Customer Support Specialist | name | Sep-26 | ~65,000 | ~65,000 | 0.00 |
| r19 Customer Support Specialist | 65,000 | Aug-27 | - | not on FE HC | - | 27,570.83 | - | 27,570.83 |
| r20 Field Engineering Manager | 140,000 | Jan-27 | r35 Field Engineer Manager | title + salary (open seat, start relaxed; A-29) | Dec-26 | 141,050.00 | 141,050.00 | 0.00 |
| r21 Head of Service Delivery | 205,000 | Jan-27 | r16 Head of Service Delivery | name | Sep-26 | ~205,000 | ~205,000 | 0.00 |
| Total |  |  |  |  |  | 919,884.37 | 816,751.03 | 103,133.33 |

FE HC r41 'Field Engineer' (new-hire block) has no name, salary or start (0 in FE HC); it may be the seat for Fld Eng Budget r15. FE HC r35 Field Engineer Manager sits under 'Open Positions' (HC-FE row 34) with no employee: it is an open seat, not a person, so its match with Fld Eng Budget r20 is seat-to-seat (A-29 amended). The COO book _2 leaves it out, FE HC starts it in Dec-26 and Fld Eng Budget costs it from Jan-27 (I-39). Start months: FE HC has every current person in seat from Sep-26 (the open Field Engineer Manager seat from Dec-26) and Fld Eng Budget starts everyone in Jan-27; for the matched people the 2027 monthly salary is identical (max difference 0.00), so the start months have no 2027 effect. COO book FE 6610 675,701 = FE HC 816,751 less FE HC r35 Field Engineer Manager (141,050).

**Burden rates (I-34)**

| FE 2027 | Salary base | 6630 payroll tax | 6640 benefits | Total burden |
|---|---:|---:|---:|---:|
| Budget: SD rates 6.8% / 16.4% | 919,884 | 62,552 | 150,861 | 213,413 |
| At FE HC rates 4.069% / 7.223% | 919,884 | 37,432 | 66,442 | 103,874 |
| **Difference (budget higher)** |  | +25,120 | +84,419 | **+109,539** |

On the matched people only (816,751 of salary) the difference is +97,258. FE HC's own burden on its 816,751 is 33,235 + 58,993.

### PE

PE 6610-6640 (1,211,637) = PE HC: 9 people, PE HC rates 3.57% / 8.82%. No SD model. PE HC r22 Head of Production and Delivery is marked 'transfer?' in column A: 2027 cost ~255,000 (salary ~225,000, tax ~10,000, benefits ~20,000), on no other roster (I-35).

### Duplicate scan across all rosters (I-28)

Rosters compared: FE HC, CO HC, PE HC, PO HC, FO HC, SD Fld Eng Budget, SD Fld Ops Payroll (named rows), SD Logistics&WH (seats), SD Prod Payroll (anonymous counts). Rule (A-29): name where present, otherwise title + salary + start; one-to-one. Names are not shown.

| Person A | Person B | Match basis | Classification |
|---|---|---|---|
| FO HC r15 Field Technician | Fld Eng Budget r15 Field Engineer | name | PROBABLE DUPLICATE (name match only; title and salary differ; likely FO->FE move) across P&L sources: FO 5510-5540 (Fld Ops Payroll current techs, by count) and FE 6610-6640 (Fld Eng Budget) |
| FO HC r21 Operations Coordinator | Fld Ops Payroll r76 Operations Coordinator | name | same person, one P&L source (FO 5510-5540 via Fld Ops Payroll) |
| FO HC r25 Field Maintenance Manager | Fld Ops Payroll r77 Manager | name | same person, one P&L source (FO 5510-5540 via Fld Ops Payroll) |
| PO HC r20 Material Handler | Logistics&WH MH-01 Material Handler | name | duplicate if the Logistics&WH model is adopted (model not carried); excluded from the I-17 net increment |
| CO HC r17 Field Logistics Manager | Logistics&WH LOG-01 Logistics Manager | name | duplicate if the Logistics&WH model is adopted (model not carried); excluded from the I-17 net increment |
| FE HC r14 Senior Field Robotics Engineer | Fld Eng Budget r13 Field Engineer | name | same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |
| FE HC r15 Associate Field Robotics Engineer | Fld Eng Budget r14 Field Engineer | name | same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |
| FE HC r16 Head of Service Delivery | Fld Eng Budget r21 Head of Service Delivery | name | same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |
| FE HC r17 Customer Support Manager | Fld Eng Budget r17 Customer Support Manager | name | same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |
| FE HC r18 Customer Support Specialist | Fld Eng Budget r18 Customer Support Specialist | name | same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |
| FE HC r19 Associate Field Robotics Engineer | Fld Eng Budget r16 Field Engineer | name | same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |
| FE HC r35 Field Engineer Manager | Fld Eng Budget r20 Field Engineering Manager | title + salary (start Dec-26 vs Jan-27) | same seat (open position, no employee; start month relaxed, A-29), one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |

Head of Service Delivery: FE HC r16 and Fld Eng Budget r21 only; CO HC / PE HC name matches 0, title matches 0; nearest title: PE HC r22 Head of Production and Delivery (different name and salary). No person appears on two HC tabs. Anonymous rows: Fld Ops Payroll's 14 current techs = the 14 FO HC field technicians (count); Prod Payroll's 9 current staff = PO HC 9 (count), or 7 by role (B2).

### Roster-to-P&L map

`02-build/02-build_roster_map_v6.csv` (no names): 47 roster rows (FO 16, PO 9, CO 5, FE 8, PE 9); each is mapped to exactly one P&L source (unmapped: 0). The FE HC r41 open row maps to no cost. 13 rows carry a flag in 'also_in' (model overlaps, the FO/FE duplicate, the PE 'transfer?' row, the open FE row). The CSV is v6's and is unchanged; v7 writes no per-person CSV.

## HC tabs added to the workbook (v6; unchanged in v7 and v8)

| Tab | From (workfile) | Cells | Formulas | Part |
|---|---|---|---|---|
| HC-FO | FO HC | 1,604 | 873 | xl/worksheets/sheet14.xml |
| HC-PO | PO HC | 1,610 | 873 | xl/worksheets/sheet15.xml |
| HC-CO | CO HC | 1,604 | 873 | xl/worksheets/sheet16.xml |
| HC-FE | FE HC | 1,604 | 873 | xl/worksheets/sheet17.xml |
| HC-PE | PE HC | 1,605 | 873 | xl/worksheets/sheet18.xml |
| HC-COO | COO HC | 1,050 | 829 | xl/worksheets/sheet19.xml |

Placed after Fld Eng Budget, in the order of the handoff. Copied cell by cell at the XML level with values, formulas (shared formulas kept), cached values, styles, column widths, row heights, frozen panes, data validations and cell notes. Sheet references re-pointed ('PO HC'! -> 'HC-PO'!, ...); HC-COO reads only the other five HC tabs. Shared strings were inlined (sharedStrings.xml untouched). Styles: 92 cell formats, 24 fonts, 8 fills, 5 borders and 4 number formats appended to styles.xml (existing entries unchanged, so no existing cell changes format); 7 theme colours resolved to RGB because the workfile theme (Aptos) differs from v5's. The hidden 'Claude Log' tab and the workfile P&L tabs were not copied (_2 stays the P&L source).

External links stored as values (A-30): each dept HC tab reads its payroll tax and benefits rates (D6:D7) from an external T&B workbook ([1], not supplied). The 10 cells keep the workfile's cached values. v7 (O6): every stored tax rate (D6) is below the 7.65% employer FICA, so these rates are unverified (I-37):

| Tab | Cell | Original formula (text) | Stored value |
|---|---|---|---|
| HC-FO | D6 | `INDEX('[1]T&B'!$S$13:$S$122,MATCH("FO",'[1]T&B'!$R$13:$R$122,0))` | 6.847091% |
| HC-FO | D7 | `INDEX('[1]T&B'!$T$13:$T$122,MATCH("FO",'[1]T&B'!$R$13:$R$122,0))` | 16.405371% |
| HC-PO | D6 | `INDEX('[1]T&B'!$S$13:$S$122,MATCH("PO",'[1]T&B'!$R$13:$R$122,0))` | 3.636890% |
| HC-PO | D7 | `INDEX('[1]T&B'!$T$13:$T$122,MATCH("PO",'[1]T&B'!$R$13:$R$122,0))` | 20.636269% |
| HC-CO | D6 | `INDEX('[1]T&B'!$S$13:$S$122,MATCH("CO",'[1]T&B'!$R$13:$R$122,0))` | 5.221456% |
| HC-CO | D7 | `INDEX('[1]T&B'!$T$13:$T$122,MATCH("CO",'[1]T&B'!$R$13:$R$122,0))` | 11.905805% |
| HC-FE | D6 | `INDEX('[1]T&B'!$S$13:$S$122,MATCH("FE",'[1]T&B'!$R$13:$R$122,0))` | 4.069207% |
| HC-FE | D7 | `INDEX('[1]T&B'!$T$13:$T$122,MATCH("FE",'[1]T&B'!$R$13:$R$122,0))` | 7.222909% |
| HC-PE | D6 | `INDEX('[1]T&B'!$S$13:$S$122,MATCH("PE",'[1]T&B'!$R$13:$R$122,0))` | 3.571466% |
| HC-PE | D7 | `INDEX('[1]T&B'!$T$13:$T$122,MATCH("PE",'[1]T&B'!$R$13:$R$122,0))` | 8.823233% |

Checks (v6, unchanged in v7 and v8): HC tabs copied byte for byte from v7; v8 recalculation of the HC tabs: errors 0, cached vs recalculated max difference 4.9e-09 over 3,432 cells.

## Head of Service Delivery salary (I-26, resolved in v5)

- Input: Fld Eng Budget!B21 = 205,000 (annual salary, user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). This is the only typed input that changed; no formula, label or other cell was edited.
- How the model treats it: row 67 uses the same formula as the other roster rows (=IF(B$58>=$C$21,$B$21/12*(1+IF(B$58>=$B$25,$B$24,0)),0)). Start month C21 = 2027-01-01, so all 12 months of 2027 are paid: 17,083.33/month Jan-Sep, then +3% (Fld Eng Budget!B24 = Fld Ops Payroll M5 = Prod Payroll M5) from 2027-10-01 (B25 = Fld Ops Payroll M6 = Prod Payroll M6) = 17,595.83/month for 3 months. No raise-eligibility test applies on this tab (I-29); the salary is treated as the Dec-26 rate.
- Burden: payroll taxes 6.8% (B22 = Fld Ops Payroll B7) and benefits 16.4% (B23 = Fld Ops Payroll B8), applied to the salary rows total (rows 69-70).
- 2027 cost of the role: salary ~205,000 + payroll tax ~15,000 + benefits ~35,000 = ~255,000.
- FE 2027 (AG): 6610 713,347 -> 919,884 (+~205,000); 6630 48,508 -> 62,552 (+~15,000); 6640 116,989 -> 150,861 (+~35,000). FE Total - Expense 931,334 -> 1,185,788. COO P&L rows 67-69 move by the same amounts.
- 2027 COO contribution (COO P&L AG132): 393,486 (v4) -> 139,032 (v5), (~255,000). 2026 FE 6610 was 850,615; FE 6610 2027 is now 919,884 (8% vs 2026; v4 -16%).
- v6: the HC rosters confirm the person is on FE HC r16 (205,000, in seat from Sep-26) and nowhere else; Fld Eng Budget starts the row in Jan-27, which gives the same 2027 cost.

## Build and sources

Output: `02-build/02-build_COO_2027_Budget_Collated_v8.xlsx` and this file (v1-v7 files unchanged; no v8 CSV).  
Scripts: `02-build/scripts/` - v8 entry point `run_build_v8.sh`: build_v8.py stage1 (formula edits on v7) -> recalc.sh (LibreOffice full recalculation) -> patches_v8.py (static downstream trace with deps_v5.py; values of the edited cells and their downstream set only; stops if anything else moves > 1e-6) -> build_v8.py final -> scen_v8.py + recalc.sh (switch scenarios) -> prodpay_v6.py, recon_v6.py, scen_v7.py, figures_v7.py on v7 (carried v7 figures) -> figures_v8.py -> cnotes_v6.py (v7 Collation Notes) -> report_v8.py pass 1 -> build_v8.py final with Collation Notes -> diff_versions.py v7 -> v8, recalc.sh, analyze_v8.py -> report_v8.py pass 2 (JSON must equal pass 1) -> privacy_v6.py (names) and paylist_v8.py (per-person amounts) -> scratch name lists deleted. `run_build_v7.sh` ... `run_build.sh` still reproduce v7 ... v1.  
Inputs (read-only): `COO_HC_and_PL_workfile.xlsx` sha256 `01eca67dc1ce297717ede0880974540b7be4ad6003f3db27ad5f2769daac9cc3`; `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `a3264ef4305e1e7da7c8cf7efbcd5407556aba56e85d50375f9ece711199e9b4`; `Service_Delivery_PL_worksheets.xlsx` sha256 `fedee8d16eb7db72d2745e77a7c6441057b4229131c52d25c944dbb5b858a466`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `645e31303dcbbbd6279152aeaa8e5e61dffa0984f1f6116d671408011166fceb`.  
Recalculation engine: LibreOffice 24.2.7.2 420(Build:2).  
Base: v7 workbook sha256 `cb2d831a10b067e35c668d52ece619b0c156f2af5e22b66a65f2a055d8d11554`.

## Completion criteria (v8)

| Criterion | Result |
|---|---|
| COO P&L = sum of the departments | Every COO P&L GL row, 2027 months U:AF and AG: max |COO - (FO + PO + CO + FE + PE)| 2.8e-09 over 1,287 cells; check row 133 (AG) 0.0e+00. |
| 0 new errors; Prod Payroll computes | Errors v7 -> v8: Prod Payroll {'#NAME?': 430} -> none; new errors 0; LibreOffice recalculation of v8 vs stored values: 1212 cells differ, max 9.3e-09, non-numeric mismatches 0. |
| Diff confined to the allowed areas | diff_versions.py v7 -> v8: 1120 formula and 1928 value differences, all inside the allowed areas (classified below): outside 0; 2026 columns (B:N) of the P&L tabs changed 0; sheets with differences COO P&L, Depreciation Schedule, PO, Prod Payroll. |
| Package | 57 of 62 v7 parts byte-identical; changed: xl/worksheets/sheet4.xml, xl/worksheets/sheet2.xml, xl/worksheets/sheet1.xml, xl/worksheets/sheet11.xml, xl/worksheets/sheet9.xml; added / removed 0 / 0; external links 0. |
| Hand recompute of one month | Jun-27 labour depreciation by hand = PO!Z20 / Z21 (v8 - v7): max difference 6.4e-11. |
| XLOOKUP replacement proof | 16 cells; tiers identical to the v7 scratch and the replica; model totals vs replica max 2.3e-09 (< $1). |
| Every figure computed by script | figures_v8.py, figures_v7.py, recon_v6.py, scen_v7/v8.py; report_v8.py types no figure. |
| Collation Notes live formulas | 32 formulas; recalc vs stored max diff 3.9e-08, text mismatches 0; first section is the CONFIDENTIAL banner: True. |
| No names | privacy_v6.py on the md, the Collation Notes JSON and sheet: 46 full names, 89 tokens checked in 3 files; hits 0. The return message is checked the same way. |
| Per-person amounts in the md | paylist_v8.py: 454 per-person amounts (636 forms) checked in 1 files; exact hits 0; coincidental equal numbers in non-people md sections (not changed) 1; $5k-multiple per-person amounts that rounding leaves exact and that appear: 7 (of 9 such amounts). Those $5k-multiple amounts are unique-role salaries that the $5k rounding cannot hide (banner). |

## Depreciation schedule summary

Tab `Depreciation Schedule` (visible, after DeploySum). Method: straight-line, no salvage, full month of depreciation from the go-live month (input B13 = 0; set 1 to start the month after). New units = DeploySum rows 19/20 (units going live), Jan-Dec 27. Existing fleet = PO Dec-26 monthly run rate, carried flat. Output = SUMIF by GL over all calc lines, then PO!U19:AF22. v8: PO rows 20/21 also add section 9 (capitalised production labour, rows 193/194); section 4 itself is unchanged.

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

**Depreciation by GL, existing vs new units vs capitalised labour (v8)**

| GL | 2026 (PO N) | Existing: Dec-26 run rate /month | Existing 2027 | New 2027 go-lives (units): 2027 | Capitalised labour (v8): 2027 | Total 2027 | Jan-27 /month | Dec-27 /month |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5010 SlipBot (PO row 19) | 1,492,329 | 112,797.85 | 1,353,574 | 0 | 0 | 1,353,574 | 112,797.85 | 112,797.85 |
| 5011 SlipLift (PO row 20) | 100,360 | 20,444.90 | 245,339 | 1,002,857 | 118,078 | 1,366,273 | 38,010.70 | 233,191.75 |
| 5012 SlipCarrier (SlipTray) (PO row 21) | 36,993 | 6,502.64 | 78,032 | 340,867 | 34,961 | 453,859 | 11,021.00 | 81,431.39 |
| 5020 Robot Peripherals (PO row 22) | 158,415 | 19,525.33 | 234,304 | 63,836 | 0 | 298,140 | 20,510.45 | 31,839.32 |
| **Total** | 1,788,097 | 159,270.72 | 1,911,249 | 1,407,560 | 153,038 | 3,471,846 | 182,340.00 | 459,260.32 |

Monthly per unit: SlipLift 65,000/84 = 773.81; SlipTray 8,000/120 = 66.67; peripherals 4,137.50/84 = 49.26.

**Hand recompute, sampled month Jun-27** (go-lives Jan-Jun 27 in service under the full-month rule: 84 lifts = 20+8+0+22+14+20; 329 trays = 60+24+0+86+61+98):

| GL | Existing run rate | New units | Capitalised labour (v8; section 5 of the labour section) | Hand total | Workbook PO!Z (Jun-27) |
|---|---:|---|---:|---:|---:|
| 5010 | 112,797.85 | none | none | 112,797.85 | 112,797.85 |
| 5011 | 20,444.90 | 84 x 65,000 / 84 = 65,000.00 | 8,829.48 | 94,274.38 | 94,274.38 |
| 5012 | 6,502.64 | 329 x 8,000 / 120 = 21,933.33 | 2,605.74 | 31,041.71 | 31,041.71 |
| 5020 | 19,525.33 | 84 x 4,137.50 / 84 = 4,137.50 | none | 23,662.83 | 23,662.83 |

**Existing fleet: PO 2026 monthly depreciation (rows 19-22; B:I actual, J:M forecast)**

| GL | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep F | Oct F | Nov F | Dec F | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5010 SlipBot | 141,122 | 122,212 | 126,630 | 128,215 | 133,969 | 133,969 | 127,510 | 127,510 | 112,798 | 112,798 | 112,798 | 112,798 | 1,492,329 |
| 5011 SlipLift | 0 | 0 | 1,678 | 3,263 | 3,263 | 11,653 | 7,458 | 9,836 | 8,838 | 15,802 | 18,123 | 20,445 | 100,360 |
| 5012 SlipCarrier (SlipTray) | 0 | 0 | 0 | 1,791 | 3,125 | 4,796 | 3,294 | 3,909 | 2,969 | 4,903 | 5,703 | 6,503 | 36,993 |
| 5020 Robot Peripherals | 8,212 | 10,914 | 10,939 | 13,556 | 13,556 | 13,770 | 8,509 | 8,592 | 14,867 | 17,475 | 18,500 | 19,525 | 158,415 |

Do J:M step up with the Sep-Dec 26 go-lives (DeploySum B:E)? Partly. DeploySum has Sep 0, Oct 9, Nov 9, Dec 0 lifts and Sep 0, Oct 35, Nov 32, Dec 0 trays. The PO forecast steps up by exact multiples of the DeploySum unit cost over the user's lives: 5011 by 9, 3, 3 lifts x 65,000/84 (Oct/Nov/Dec) and 5012 by 29, 12, 12 trays x 8,000/120. So the forecast already holds Q4-26 go-lives at the same costs and lives, but fewer of them: October lifts match; the rest do not. 5020's steps (2,608.33, 1,025.00, 1,025.00) are not whole multiples of the DeploySum peripheral cost, so their basis is unknown. 5010 is flat Sep-Dec at 112,797.85.

**Treatment: rely on the run rate (builder decision; two-way risk, I-31).** Oct-Dec 26 go-lives are not added explicitly. Why: the run rate is PO's own forecast and already contains Q4-26 step-ups priced like the schedule; adding DeploySum's Q4 units on top would count the 15 lifts and 53 trays already in it twice. The risk runs both ways. If DeploySum's Q4 counts are right, the run rate is short 3 lifts / 14 trays (39,057 for 2027; memo in schedule section 5). If PO's Dec-26 step-up (3 lifts, 12 trays; DeploySum has no Dec-26 go-lives) is units that DeploySum places in Jan-27, they are also in the Jan-27 vintage: 37,457 counted twice. PO owner to confirm; user decision (Decisions pending #3).

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

v8: the DeploySum CapEx (and the 65,000 / 4,137.50 / 8,000 unit costs) holds no production labour. The capitalised labour is added on top per vintage: 2,324,186 in the 2027 go-lives (depreciable cost of the 2027 go-lives incl. labour 27,896,561), 650,571 in the builds for 2028 go-lives.

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
| A-15 | Units built in 2027 for 2028 go-lives are not depreciated in 2027. v8: their capitalised labour (650,571) is not depreciated either (A-41). | CapEx 9,446,375 excluded | 'Depreciation Schedule' section 7 | follows A-14 (not in service) |
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
| A-26 | Head of Service Delivery annual salary (current employee), entered in v5 | 205,000/year in B21; model: full year from 2027-01-01, +3% from 2027-10-01, tax 6.8%, benefits 16.4%: 2027 cost ~255,000 | Fld Eng Budget!B21 -> rows 67-71, 78-80 -> FE rows 67-69 | user-confirmed 2026-10-09 ('Head of Service delivery salary is $205k annually'); treatment = existing workbook logic |
| A-27 | Net increment of an SD payroll model = model 2027 total less the model's own cost of the people already on an HC roster (same model rates) | I-05 1,962,389; I-17 336,530 | Prod Payroll; SD Logistics&WH Payroll | builder definition (v6, handoff: 'model total minus the overlap already in PO') |
| A-28 | Prod Payroll tray and supervisor rows evaluated by replacing XLOOKUP (match_mode 1) with an equivalent SMALL/COUNTIF formula in a scratch copy only. v8: the 16 XLOOKUP cells are replaced in the workbook by an INDEX/MATCH equivalent (Prod Payroll!B48:Q48): tiers and model totals identical to the scratch method; the scratch copy is no longer needed. | model 2027 2,592,894; Python replica agrees to 5e-10 | Prod Payroll!B48:Q48 (v8: replaced in the workbook) | builder method (v6) |
| A-29 | Person match: name where present (all tokens of the shorter name in the longer, same first token); otherwise title + salary + start; one-to-one. v7: start month relaxed for FE HC r35, an open seat ('Open Positions', no employee), matched seat-to-seat with Fld Eng Budget r20 (HC Dec-26, SD Jan-27; I-39). | 12 pairs; anonymous model rows (Prod Payroll current staff, Fld Ops Payroll current techs) matched by headcount only | recon_v6.py | handoff rule |
| A-30 | HC tab tax/benefit rates (D6:D7) linked to an external T&B workbook are kept as the workfile's cached values | 10 cells | 'HC-*'!D6:D7 | builder (as DeploySum in v3) |
| A-31 | Employer FICA reference rate 7.65% (6.2% Social Security + 1.45% Medicare), used only to test the HC T&B tax rates (I-37) | PO/CO/PE gap up to 77,882; FO/FE up to 34,169 | figures_v7.py | statutory rates; wage base not modelled (upper bound) |
| A-32 | Capitalised case (Decision #1): ramp split to lifts and trays from the model (lift / tray ramp = model total less its current-staff cost); supervisors allocated pro rata to the lift : tray ramp cost. v8: superseded for the booked figure by A-36..A-41; reproduced as the bridge check (64,735). | lift 1,291,250, tray 671,139 (supervisors 65.8% to lifts); check with the model-total split: depreciation 65,458 vs 64,735 | Prod Payroll rows 41, 62, 79 | builder assumption (v7, handoff fallback shown) |
| A-33 | Capitalised case: 2027 ramp labour spread evenly over the units built in 2027; units go live 2 months after build; depreciation per the Depreciation Schedule (full month from go-live, 84 / 120 months); units built Nov-Dec 27 (2028 go-lives) carry labour but no 2027 depreciation. v8: superseded for the booked figure by A-36..A-41; reproduced as the bridge check (64,735). | units built 312 lifts / 1355 trays; live in 2027 222 / 952; depreciation 64,735 (9) / 69,357 (7) | DeploySum rows 19-20, 24-25, 33-34; 'Depreciation Schedule' rows 38-62 | builder assumption (v7); lag checked on the DeploySum rows (DeploySum note 1) |
| A-34 | 7-overlap reading (B2): the 2 Prod Payroll current seats no PO HC production person fills are costed at the model's average current cost per head; capitalised case keeps the 9-overlap lift / tray mix | +140,112 (139,984 to 140,560 as tray or lift seats) | Prod Payroll B9, C9, H10; 'HC-PO'!C14:C22 | builder assumption (v7) |
| A-35 | md privacy: per-person amounts for identified employees rounded to the nearest $5k ('~'); Collation Notes keeps exact figures (restricted workbook) | md only | paylist_v7.py | critic v6 O8 / handoff |
| A-36 | Production labour capitalised (Decision #1 RESOLVED): every Prod Payroll cost row (rows 41, 62, 79) is capitalised into the units built that month; the current staff are included (switch B131 = 1) | 2027 2,592,894; 2027 depreciation 153,038 | 'Depreciation Schedule'!B131, rows 137-149 | user-confirmed 2026-10-10; scope per brief v5 (orchestrator); Finance to confirm (I-40) |
| A-37 | Supervisors are allocated to lifts and trays pro rata to the month's lift : tray capitalised labour (v7 A-32, now by month) | 2027 supervisors 241,294: 166,821 to lifts | 'Depreciation Schedule'!row 146 | builder (v7 A-32 carried to monthly) |
| A-38 | Labour per unit = the build month's capitalised labour / units built that month; a month with no units built (Oct-26, Jan-27) rolls its labour into the next build month (work in progress) | Oct-26 81,851 into Nov-26 builds; Jan-27 140,751 into Feb-27 builds | 'Depreciation Schedule'!rows 152-157 | builder assumption (v8); Finance to confirm idle-month treatment (I-40) |
| A-39 | Build-to-go-live lag 2 months (DeploySum note 1); labour joins the vintage cost at go-live and is depreciated like the unit (full month from go-live + B13, 84 / 120 months, salvage B12) | lag check 0 (DeploySum go-lives = builds 2 months earlier, every 2027 month) | 'Depreciation Schedule'!B133:B134, rows 165-189 | DeploySum note 1; Depreciation Schedule logic (brief v5) |
| A-40 | Sep-Dec 26 model months: Sep-26 builds go live Nov-26 (2026 vintage, inside the PO run rate; not added); Oct-26 has no builds and rolls into Nov-26; the Nov-Dec 26 builds go live Jan-Feb 27 and carry the Oct-Dec 26 labour (switch B132 = 1) | 381,863 into Jan-Feb 27; 90,851 in the Nov-26 go-lives (not added) | 'Depreciation Schedule'!B132, rows 159-161, B207:B209 | builder assumption (brief v5: state how) |
| A-41 | Builds for 2028 go-lives (Nov-Dec 27) carry labour that is not depreciated in 2027: CIP / inventory at Dec-27 | 650,571 | 'Depreciation Schedule'!row 160, B204 | follows A-14 / A-15 |


A-22..A-25 are new in v4; A-26 is new in v5; A-27..A-30 are new in v6; A-36..A-41 are new in v8 and A-15, A-28, A-32, A-33 were amended in v8; A-31..A-35 are new in v7 and A-29 was amended in v7 (critic O5); A-14, A-17, A-18 and A-19 were edited in v4 (critic O1, O3, O4); A-17 also shows the N3 trend case in v5.

## DeploySum refresh and tie-out (v3 build; unchanged in v4-v8)

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

## v7 -> v8 diff

`diff_versions.py` (exact: formulas as text, cached values with no tolerance) on every sheet present in both files except Collation Notes:

| Sheet | Cells | Formula diffs | Value diffs |
|---|---:|---:|---:|
| COO P&L | 3,530 | 0 | 235 |
| FO | 3,581 | 0 | 0 |
| PO | 3,634 | 65 | 222 |
| CO | 3,582 | 0 | 0 |
| FE | 3,582 | 0 | 0 |
| PE | 3,590 | 0 | 0 |
| DeploySum | 901 | 0 | 0 |
| Depreciation Schedule | 2,253 | 1039 | 1039 |
| Fld Ops Payroll | 1,165 | 0 | 0 |
| Prod Payroll | 1,173 | 16 | 432 |
| Fld Maint Budget | 1,012 | 0 | 0 |
| Fld Eng Budget | 740 | 0 | 0 |
| HC-FO | 1,071 | 0 | 0 |
| HC-PO | 1,056 | 0 | 0 |
| HC-CO | 1,039 | 0 | 0 |
| HC-FE | 1,046 | 0 | 0 |
| HC-PE | 1,051 | 0 | 0 |
| HC-COO | 948 | 0 | 0 |
| **Total** | 34,954 | 1120 | 1928 |

Where the differences are (analyze_v8.py; every changed cell is an edited cell or in the static downstream trace of the edits):

| Sheet | Area | Formula diffs | Value diffs | Allowed by the handoff as |
|---|---|---:|---:|---|
| COO P&L | roll-up of the PO rows and subtotals (U:AF, AG, AH, AJ; incl. ratio rows 65, 141 and check row 133) | 0 | 235 | the COO P&L roll-up |
| PO | U20:AF21 (5011 / 5012, 2027 months) | 24 | 24 | PO rows 20/21 and 33-35 (2027 months), their subtotals |
| PO | subtotals and ratios of those rows (AG / AH / AJ; rows 36, 37, 63, 64, 117, 132, 137-142) | 0 | 157 | PO rows 20/21 and 33-35 (2027 months), their subtotals |
| PO | AI20:AI21, AI33:AI35 (notes: 'capitalised') | 5 | 5 | PO rows 20/21 and 33-35 (2027 months), their subtotals |
| PO | U33:AF35 (5110-5140, 2027 months) | 36 | 36 | PO rows 20/21 and 33-35 (2027 months), their subtotals |
| Depreciation Schedule | rows 128-216 (new sections 8-10) | 1039 | 1039 | new rows / blocks on the Depreciation Schedule |
| Prod Payroll | B48:Q48 (the 16 XLOOKUP cells) | 16 | 16 | Prod Payroll XLOOKUP cells (and the model cells they feed) |
| Prod Payroll | rows 49-81 (cells fed by row 48: tray, supervisor and total rows) | 0 | 416 | Prod Payroll XLOOKUP cells (and the model cells they feed) |

Outside the allowed areas: **0** cells. 2026 columns (B:N) of COO P&L, FO, PO, CO, FE, PE: **0** changed. Cells outside the edits and their trace that LibreOffice moved by floating-point noise only were not written (max 9.3e-09, 1212 cells, kept at their v7 bytes).

Package: 57 of 62 v7 parts byte-identical; changed: xl/worksheets/sheet4.xml, xl/worksheets/sheet2.xml, xl/worksheets/sheet1.xml, xl/worksheets/sheet11.xml, xl/worksheets/sheet9.xml.

## Error scan

| Sheet | v7 | v8 |
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
| Prod Payroll | {'#NAME?': 430} | none |
| Fld Maint Budget | none | none |
| Fld Eng Budget | none | none |
| HC-FO | none | none |
| HC-PO | none | none |
| HC-CO | none | none |
| HC-FE | none | none |
| HC-PE | none | none |
| HC-COO | none | none |

New errors in v8: **0**. Prod Payroll's 430 #NAME? cells of v7 are gone (XLOOKUP replaced, A-28).

## Package

Parts 62 (v7 62); `xl/externalLinks/*` **0**; defined names 8,965 (v7: 8,965).

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
| 14 | HC-FO | visible |
| 15 | HC-PO | visible |
| 16 | HC-CO | visible |
| 17 | HC-FE | visible |
| 18 | HC-PE | visible |
| 19 | HC-COO | visible |

## Severity scale

HIGH = blocks sign-off or > $250k impact; MED = $50k-250k or needs owner confirmation; LOW = < $50k or hygiene.

Applied in this order: (1) HIGH if the item blocks sign-off or its $ impact computed from the workbook is > $250k; (2) MED if that impact is $50k-250k; (3) MED if the impact cannot be determined from the workbook and an owner must confirm; (4) otherwise LOW (impact < $50k, $0, or hygiene). 'Impact' is the amount the item could move the 2027 budget, read from cells; where only an exposure (the amount resting on the item) is known, it is shown but not used as the impact.

## Issues (v8)

Severity per the scale above. Open: 4 HIGH, 15 MED, 20 LOW; 2 RESOLVED. v8: I-05 RESOLVED by policy (production labour capitalised); I-40 (HIGH, scope of the policy) and I-41 (MED, material-handling roles) are new; I-07, I-11, I-14, I-17, I-23, I-25, I-37 and I-38 are updated. No other severity changed.

| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |
|---|---|---|---|---|---|---|---|
| I-01 | MED | PO!U12:AF12; PO!R12; PO!U13:AF13; PO!U15:AF15; DeploySum!F40:Q40 | Resolved by assumption in v3. 2027 revenue is now budgeted: PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27; row 39 in the 9/30/26 file), all to 4100 Subscription/Platform Fees (orchestrator assumption). PO!R12 set to 'Manual'. Still open: 4500 Implementation Fees and 4900 One-Time Revenue stay 0 in 2027, and the source does not say whether recognized revenue includes them. | PO!AG12 = 15,563,645.54; DeploySum FY27 recognized revenue (9/30/26 file R39) = 15,563,645.54; difference (0.00). 2026: 4500 85,861, 4900 975,000. Cross-check Sep-Dec 26: DeploySum recognized revenue 2,527,326 vs PO 4100 forecast (PO!J12:M12) 2,486,929 (difference 40,396), so the 4100 mapping is consistent with how PO forecasts 2026. | not determinable (2026 4500+4900 = 1,060,861) | impact not determinable; owner confirmation needed | Finance/PO owner to confirm the 4100 mapping and whether 2027 implementation or one-time revenue should be budgeted on 4500/4900. |
| I-02 | HIGH | FO!AG63; FO!AG116; FE!AG63; FE!AG116; COO P&L!AG132 | Replacing FO and FE with the SD versions adds 6,828,802 to 2027 COO cost (COGS + Opex). The SD build is much heavier than the COO book's FO/FE. (v4: restated in cost terms; the earlier evidence quoted 2027 Net Income from before revenue was budgeted.) | FO cost (AG63 + AG116): COO book 1,341,298 -> SD 7,347,500; FE: COO book 752,002 -> SD 1,574,602; together 2,093,300 -> 8,922,101. With the COO book's FO/FE, the 2027 COO contribution would be 6,967,834 instead of 139,032. Drivers: FO!N52 876,692 -> AG52 3,238,031; FO!N47 255,704 -> AG47 1,519,865; FO!N29 57,182 -> AG29 765,000. | (6,828,802) on the contribution | impact (6,828,802) | COO and SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off. |
| I-03 | LOW | DeploySum!A3:R49 (Collation Notes lists the formulas) | Resolved in v3. DeploySum rows 3-49 now hold the resolved values from 2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx. The 410 cells that link to the external workbook '[1]' are stored as that file's cached values; their formula text is on Collation Notes. The links are still not live (the [1] workbook was not supplied), so the next plan update needs a new resolved export. | DeploySum errors: v2 {'#REF!': 463, '#N/A': 35}, v3 none (498 resolved). Every mapped cell B:R equals the 9/30/26 cached value (mismatches: 0). New-file sha256 645e31303dcbbbd6... | 0 | hygiene | Refresh DeploySum from a new resolved export when the plan changes. Keep the row map (ARR row 39 kept). |
| I-04 | LOW | DeploySum!B53:R66; DeploySum!A69:R76 (v3 check block) | The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (rows 53-66) are still typed values. v3 adds a live check: they now tie to the resolved rows 16-21 in every month Sep-26..FY27. So the FO/FE drivers are consistent with the 9/30/26 plan; they are just not linked. | 16+17 vs 54+57+60: FY 67 vs 67, max monthly diff 0; 18 vs 64: FY 67 vs 67, max monthly diff 0; 19 vs 55+58+61: FY 250 vs 250, max monthly diff 0; 20 vs 56+59+62: FY 1,036 vs 1,036, max monthly diff 0; 21 vs 63: FY 0 vs 0, max monthly diff 0. DeploySum!A76 = 'Tie-out rows 16-21 vs 54-64: OK'. | 0 | hygiene | Optional: replace rows 54-64 with formulas (or document the source) so they update with the plan. |
| I-05 | RESOLVED | Prod Payroll!B24:S81 (hidden); Prod Payroll!S41, S62, S79, S81; PO!AG33:AG36; 'HC-PO'!B14:Z22, Z67:Z70; 'Depreciation Schedule'!A128:S216; PO!U20:AF21 | RESOLVED by policy in v8 (Decision #1, user-confirmed 2026-10-10: production labour is capitalised). The whole Prod Payroll model is in the budget as capitalised labour: 2,592,894 for 2027 (lift 1,622,423, tray 729,177, supervisors 241,294; the 9 current staff 630,504 at model rates, the ramp 1,962,389). PO 5110-5140 2027 = 0 (formulas, labelled capitalised; v7 652,820), and the labour reaches 2027 only as depreciation of the units it builds: 153,038 (5011 118,078, 5012 34,961). Remaining exposure = depreciation only, plus the policy scope (I-40) and the material-handling roles (I-41). Was (v7, HIGH): the 1,962,389 net ramp was not in the budget and its treatment was open. | Prod Payroll computes in the workbook (16 XLOOKUP cells replaced, A-28): S81 2,592,893.90; Python replica from the input cells, max monthly difference 4.7e-10. 2027 labour 2,592,894 = into 2027 go-lives 1,942,323 + into 2028 go-lives (CIP / inventory) 650,571; Oct-Dec 26 labour into the Jan-Feb 27 go-lives 381,863; depreciable labour in the 2027 vintages 2,324,186, 2,171,148 net at Dec-27. Average labour per unit built in 2027: lift 5,735 (8.8% of 65,000), tray 593 (7.4% of 8,000). | (153,038) depreciation (in the headline) and +652,820 PO 5110-5140 removed: +499,782 vs v7 | resolved (was HIGH); scope exposure in I-40 | None for I-05. Finance: confirm the scope (I-40, Decision #10). PO owner: the material-handling roles (I-41). SD owner: the model date (I-38). |
| I-06 | LOW | Fld Maint Budget!B30 (comment); Fld Ops Payroll!B11; FO!AG44; FO!AG52 | MeLi contractor double count: quantified at $0 in the current cells. The CONFIRM comment on Fld Maint Budget!B30 says Fld Ops Payroll includes MeLi in '21 all-in techs', but Fld Ops Payroll!B11 = 14 ('Current site techs on payroll (Sep-26) - Domestic Only') and Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11 = 21. So MeLi techs are costed in 5310 only. The comment describes an earlier state and is stale (Fld Maint Budget!A143 records the correction). | FO 5310 (FO!AG44 = 575,268) = MeLi techs in role 346,920 + Merida contractors 123,900 + MeLi supervisor 104,448 (Fld Maint Budget rows 70-72 x B10/B11; row 84 = 575,268). FO 5510 current techs: Fld Ops Payroll!F20:Q20 = 14 each month (formula =$B$11); current-tech payroll 2027 1,094,774. | 0 | impact 0 | SD owner to confirm and delete the stale CONFIRM comment on Fld Maint Budget!B30. |
| I-07 | MED | PO!U19:AF22; 'Depreciation Schedule'!A1:S126; COO P&L!AG19:AG22 | Resolved by assumption in v3. 2027 depreciation is now budgeted from the new 'Depreciation Schedule' tab: straight-line, SlipLift 84 months, SlipTray 120 months, no salvage, full month from the go-live month. Existing fleet = PO Dec-26 run rate, carried flat (builder assumption, A-17). New units = DeploySum 2027 go-lives (rows 19/20). PO!R19:R22 set to 'Manual'. The open parts are logged separately: I-31 (Q4-26 go-lives), I-32 (existing-fleet run rates, SlipBot) and I-33 (peripherals). | 2027 depreciation 3,318,808 (2026 1,788,097): existing fleet 1,911,249, new 2027 go-lives 1,407,560. By GL: 5010 SlipBot 1,353,574; 5011 SlipLift 1,248,196; 5012 SlipCarrier (SlipTray) 418,898; 5020 Robot Peripherals 298,140. Python recompute from raw inputs vs workbook, all 48 GL-months: max diff 3.78e-10. v8: + capitalised production labour 153,038 (5011 118,078, 5012 34,961; 'Depreciation Schedule' sections 8-9): 2027 depreciation 3,471,846. | not determinable (component decisions in I-31..I-33) | impact not determinable; owner confirmation needed | PO owner/Finance to confirm the run-rate approach against the fixed-asset register, and resolve I-31..I-33. |
| I-08 | LOW | PO!U28; PO!Y28; PO!AD28; PO!U38; PO!U42 | Typed plugs are added onto the driver formula in 2027 month cells (+15,000, +5,000). They are not visible in the method columns R:T. | PO!U28 +5,000; PO!Y28 +5,000; PO!AD28 +5,000; PO!U38 +15,000; PO!U42 +15,000. Total plugs 45,000. | 45,000 | impact 45,000 | PO owner to move these amounts into a documented input (column S or a manual row), or remove them. |
| I-09 | LOW | PE!W74:AF74; PE!W76 | Typed numbers overwrite the driver formula in some 2027 months (manual overrides inside a formula row). | PE!W74=1,500, PE!X74=1,500, PE!Y74=2,000, PE!Z74=2,000, PE!AA74=2,500, PE!AB74=2,500, PE!AC74=3,000, PE!AD74=3,000, PE!AE74=3,500, PE!AF74=4,000, PE!W76=300. Total typed 25,800. | 25,800 | impact 25,800 | PE owner to confirm the overrides, or set the row method to Manual. |
| I-10 | MED | FO!AG58; FO!AG67; FO!AG91; FE!AG91; FO!AG116 | FO/FE lines with material 2026 spend have 2027 = 0, and FO Total Expense (SG&A) is 0 for 2027. Fld Maint Budget!A99 says: 'Not budgeted here: 6100 Travel and 7550 Tools ($0 by design – field travel books to 5050/5360, field tools to 5330); new-hire onboarding (covered by the $2K new-hire cost in Fld Ops Payroll B9). Out of scope: 5920, 7200, 8600.' | FO!AG58 5920 - Software - COGS: 2026 119,260 -> 2027 0; FO!AG67 6610 - Salaries and Wages - SG&A: 2026 50,575 -> 2027 0; FO!AG91 7200 - Contractors: 2026 59,734 -> 2027 0; FE!AG91 7200 - Contractors: 2026 154,857 -> 2027 0; FO!N116 217,242 -> AG116 0. 2026 total of these lines 384,425. | not determinable (2026 base 384,425) | impact not determinable; owner confirmation needed | SD owner to confirm whether these costs stop in 2027 or are budgeted elsewhere. |
| I-11 | MED | COO P&L!AG12; COO P&L!AG52; COO P&L!AG19; COO P&L!AG47 (+ variance table) | 98 rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k (v3 values; list below). | v3 values: 98 rows (v2: 98). Largest COO P&L GL moves: COO P&L!N12 6,363,078 -> AG12 15,563,646; COO P&L!N52 887,966 -> AG52 3,238,031; COO P&L!N47 319,694 -> AG47 1,554,365; COO P&L!N20 100,360 -> AG20 1,248,196. v8: 99 rows (regenerated: 0 added, 23 changed, 1 removed; production labour capitalised). | not determinable | impact not determinable; owner confirmation needed | Each dept owner to comment on their rows in the variance table. |
| I-12 | MED | Fld Maint Budget!B8; Fld Maint Budget!B78:M78; FO!AG46 | Site setup kit cost is flagged as a placeholder (Fld Maint Budget!D8: 'PLACEHOLDER – update when the kit list is priced (Spare Parts, Tool Kits, 5S for'). It feeds FO 5330. | Fld Maint Budget!B8 = 4,500 $/new site; 'Site setup kits' 2027 (B78:M78) = 274,500. FO!N46 23,121 -> AG46 288,069. | not determinable (exposure 274,500) | impact not determinable; owner confirmation needed | SD owner to price the kit list and replace B8. |
| I-13 | MED | Fld Ops Payroll!M11; Fld Ops Payroll!B12; Fld Ops Payroll!M14 | Two Fld Ops Payroll drivers are marked 'Placeholder' in the author's notes: site techs per floater (M11) and the share of expansion go-lives needing a tech (B12). M11 currently has no effect because the floater switch M14 = 'No' (floater payroll 2027 = 0). B12 drives expansion-tech payroll. | M11 = 40, B12 = 0.6, M14 = 'No'. Expansion tech payroll 2027 (Fld Ops Payroll!F47:Q47) = 337,514. | not determinable (exposure 337,514) | impact not determinable; owner confirmation needed | SD owner to confirm or replace B12; M11 matters only if M14 is set to Yes. |
| I-14 | MED | Prod Payroll!M7; Prod Payroll!B9; Prod Payroll!A33; Fld Ops Payroll!B9; Old Draft!B142 (SD, not carried) | More placeholder inputs: Prod Payroll new-hire cost, current headcount and absence factors (no budget effect while Prod Payroll is broken), and the Fld Ops Payroll new-hire cost per tech, which hidden Old Draft!B142 says overlaps an onboarding line. v8: Prod Payroll now computes and drives the budget (capitalised labour, I-05), so these placeholders (M7 new-hire cost, B9 / C9 current staff, the absence factors) now move 5011 / 5012 depreciation. | Fld Ops Payroll!B9 = 2,000; new-hire cost in FO 2027 (Fld Ops Payroll rows 34, 46, 59, 72, F:Q) = 138,000. Old Draft!B142: '7. Onboarding: 10 new hires Jan – Sep. The $2,000 Fld Ops Payroll placeholder (B9) overlaps this line; replace it with the actual cost here '. | not determinable (exposure 138,000) | impact not determinable; owner confirmation needed | SD owner to confirm B9 (and that onboarding is not also budgeted elsewhere). |
| I-15 | LOW | Fld Maint Budget!B12 (comment); Fld Maint Budget!B11; Fld Ops Payroll!H11; Fld Ops Payroll!E12 | The CONFIRM comment on Fld Maint Budget!B12 says Fld Ops Payroll shows 0 current supervisors; it now shows H11 = 1 ('Current supervisors counted toward ratio (Sep-26) – [name; FO HC r25 Field Maintenance Manager]'), and E12 says 'Ratio = domestic techs only. MeLi contract supervisor budgeted in Fld Maint Budget B11.'. The MeLi contract supervisor (5310) and the domestic manager (5510) are different people, so there is no double count; the comment is stale. | MeLi supervisor in 5310 2027 = 104,448 (Fld Maint Budget!B11 = 8,704/month x B12 = 1). FO HC r25 Field Maintenance Manager (Fld Ops Payroll row 77) 2027 = ~120,000; incremental supervisors (row 73) 2027 = 193,632. | 0 | impact 0 | SD owner to confirm and delete the stale comment. |
| I-16 | LOW | Fld Maint T&E Data!M5:M388 (SD, hidden, not carried) | 101 T&E transactions are flagged 'Reclass needed' = Yes, totalling $27,804.02; booked GL differs from budget GL. 2 are tagged 'AI suggested' and 17 have tag basis 'Assumed'. If FO 2026 actuals were pulled on booked GL, these sit on the wrong 2026 lines; totals are unaffected, and no formula in the output reads this sheet. | Top booked->budget GL pairs: 5050->5360 x34, 6100->5360 x16, 5360->5050 x14, 7550->5330 x12, 6100->5050 x8. | 27,804 | impact 27,804 | Finance to post the reclasses (or confirm none are needed). |
| I-17 | HIGH | Logistics&WH Payroll!A14:S51 (SD, not carried); PO!AG33:AG36; 'HC-PO'!B16:C20; 'HC-CO'!B17:C17 | The SD Logistics & Warehouse payroll model (547,441 for 2027, referenced by no formula) names two people who are already on HC rosters: its Logistics Manager seat (LOG-01) is CO HC r17 Field Logistics Manager (costed in CO 6610-6640; the model's own note classifies the seat as Central Operations) and its first Material Handler seat (MH-01) is PO HC r20 Material Handler (costed in PO 5110-5140). Net of those two seats (210,912 at model rates), the model adds 336,530 that no roster or P&L line carries: 7 seats (INV-01, TL-01, TL-02, MH-02, MH-06, MH-03, MH-04), all hires from Oct-26 on. MH-02 is described as the backfill for PO HC r16 Material Handling Team Lead, who stays on PO HC for all of 2027. v7 (B2): v6's combined I-05 + I-17 (2,298,919) took PO HC r20 out twice (inside I-05 by count, inside I-17 as MH-01 by name). Deduplicated: 2,360,882 (9-overlap; MH-01 then counts as a new seat, +~60,000) or 2,439,031 (7-overlap). Logistics&WH seats TL-01 (Dec-26) and MH-02 (Oct-26) are dated before the roster file and are not on it (I-38). v8 (production labour capitalised): I-17 stays an expensed cost (warehouse, not production). Deduplicated against the capitalised Prod Payroll: 398,492 at the 9-overlap (MH-01 then a new seat); 471,093 at the 7-overlap, incl. the 2 material-handling roles that PO 5110-5140 = 0 removes (I-41). | Seats (2027 cost at model rates, start): LOG-01 Logistics Manager ~150,000 (on payroll); INV-01 Inventory Control Specialist 55,652 (Feb-27); TL-01 Material Handling Team Lead 64,544 (Dec-26); TL-02 Material Handling Team Lead 33,032 (Jul-27); MH-01 Material Handler ~60,000 (on payroll); MH-02 Material Handler ~60,000 (Oct-26); MH-06 Material Handler 31,751 (Jul-27); MH-03 Material Handler 52,712 (Mar-27); MH-04 Material Handler 36,876 (Jun-27). Net seats headcount Jan..Dec 27: 2, 3, 4, 4, 4, 5, 7, 7, 7, 7, 7, 7. The two overlapping people cost 204,109 on their HC rosters (already in the budget). Seats the model itself excludes: LOG-02 (= FO HC r21, budgeted in FO) and MH-05 (in no model, I-27). PO HC r16 2027 cost ~70,000 at PO rates. | (336,530) on the contribution (net); v5 showed the gross 547,441 | impact 336,530 (> $250k) | PO owner to confirm the warehouse team plan. If adopted, add the 7 new seats (336,530), not the model total. Confirm whether PO HC r16 leaves the role MH-02 backfills; if so PO HC is overstated by up to ~70,000. |
| I-18 | LOW | Fld Ops Payroll!B10; Fld Ops Payroll!B15; Fld Ops Payroll!B16 | The hiring horizon ends at Dec-27 (DeploySum row 54). Hires for Jan-28 go-lives use an Oct-Dec 27 average default rather than a forecast (documented by the author). | B10 = 1; B15 = =ROUND(AVERAGE(DeploySum!O54:Q54),0) = 7; B16 = =ROUND(AVERAGE(DeploySum!O57:Q57),0) = 2; cell notes on B10/B15/B16. | not determinable | hygiene | Overwrite B15/B16 if a 2028 go-live forecast exists. |
| I-19 | LOW | FE!U30:AF75 (rows 30-31, 67-69, 74-75); Fld Eng Budget rows 28-33, 85-91 | FE and Fld Eng Budget link in both directions: Fld Eng Budget reads FE 2026 columns, and FE 2027 rows read Fld Eng Budget. LibreOffice recalculated with no errors (no cell-level circularity), but the structure is easy to break. | Fld Eng Budget has 68 references to FE; FE has 84 references to Fld Eng Budget. | not determinable | hygiene | Check Fld Eng Budget before editing the FE 2026 columns it reads. |
| I-20 | LOW | SD sheets Prod Payroll, Old Draft, Fld Maint T&E Data (hidden); DeploySum!A41:A42 (hidden rows 41-42) | SD has 3 hidden sheets; Prod Payroll is carried and kept hidden, the others are not carried (FO/FE do not depend on them). DeploySum row visibility for rows 3-49 now follows the 9/30/26 file. | Hidden in output: ['Prod Payroll']. DeploySum hidden rows v2 [30, 32, 33, 34, 35, 36, 40, 41, 42] -> v3 [41, 42] (rows 30, 32-36 and recognized revenue row 40 are now visible, as in the 9/30/26 file). | not determinable | hygiene | None, unless reviewers want Old Draft / T&E Data in the pack. |
| I-21 | LOW | Fld Maint T&E Data!Q26 (SD) | Old Draft dependence is contained: 1 cell(s) outside Old Draft read it, none in the FO/FE chain, so the output has 0 references to it. | SD Fld Maint T&E Data: 1 cell(s) e.g. Q26: ='Old Draft'!B28*'Old Draft'!B23. SD dependency map: Old Draft -> {'Fld Maint T&E Data': 458, 'Fld Ops Payroll': 131, 'DeploySum': 112}. | not determinable | hygiene | None for the budget. Consider deleting Old Draft once the reference is re-pointed. |
| I-22 | LOW | COO P&L!A23:A24, B27, B37 (same rows on FO, PO, CO, FE, PE) | Rows 23 and 24 carry the same label ('5025 - Freight and Delivery - Production (Summary)'). Row 23 is an empty header; row 24 holds postings inside row 27 (=SUM(B24:B26)). Row 37 (=B19+B22+B27+B28+B29+B30+B31+B36+B20+B21) covers every direct child of its section, so nothing is skipped today, but anything typed on row 23 would be left out. | Subtotal scan on 6 sheets: 0 skipped lines with values. Non-empty cells on row 23 by tab: {COO P&L: 0, FO: 0, PO: 0, CO: 0, FE: 0, PE: 0}. COO P&L dept-sum formulas omitting a dept: 0. | not determinable | hygiene | Optionally relabel row 23 as a header, or lock it. |
| I-23 | LOW | COO P&L!B65:M65; COO P&L!C141 | COO P&L row 65 (labelled 'Expense') holds an unlabelled gross-margin % formula (=IFERROR(B64/B16,"")). With 2027 revenue now budgeted, it shows a 2027 margin (AG65 = 21.9%). Row 141 shows an extreme ratio for Feb-26 caused by negative 2026 payroll postings. | COO P&L!C141 = -14.33 (ratio). PO!N67 (308,059) -> AG67 0; PE!N35 (56,264) -> AG35 0. | not determinable | hygiene | Label row 65. Finance to explain the negative 2026 payroll postings in PO 6610 and PE 5140. v7: the PO 6610 and PE 5140 credits are also evidence for Decision #1 (production labour capitalised, B1); Finance's answer settles both. v8: Decision #1 is resolved (capitalised); the 2026 credits now bear on the 2026 policy and the scope (I-40). |
| I-24 | LOW | Workbook defined names (xl/workbook.xml <definedNames>, workbook scope, no cell); list in 02-build_pruned_names_v2.csv | The COO book carries 14,310 legacy defined names from an old template. None is used by any formula, data validation, conditional format, chart or other name. v2 pruned the 5,345 unused names whose target is #REF! (5,330) or external-looking (15); 8,965 remain (string/array constants and plain values). | Before 14,310, after 8,965. Usage scan covered cell formulas, data validations, conditional formats, charts, print areas/titles and other names (counts in the notes file). Names referenced: 0 from parts, 0 from other names. Pruned names still referenced: 0. | not determinable | hygiene | Optional: purge the remaining constant-valued legacy names in Name Manager. |
| I-25 | LOW | Prod Payroll!B24:S81; DeploySum!A1 (notes) | Side effects of moving from Google Sheets to xlsx: threaded comments become plain notes (text kept); Google's '#ERROR!' has no Excel equivalent; LibreOffice saves error constants as '=#REF!' formulas. v3: DeploySum no longer has errors; Prod Payroll's remaining errors are now #NAME? (LibreOffice has no XLOOKUP), not #REF!. v8: Prod Payroll's XLOOKUP cells are replaced by an INDEX/MATCH equivalent (A-28), so LibreOffice evaluates the whole model. | Errors v2 -> v3: DeploySum {'#REF!': 463, '#N/A': 35} -> none; Prod Payroll {'#REF!': 796} -> {'#NAME?': 430}. New errors: 0. v8: Prod Payroll errors 430 -> 0. | not determinable | hygiene | None; disclosed for reviewers. |
| I-26 | RESOLVED | Fld Eng Budget!B21; Fld Eng Budget!B67:M67; FE!AG67 | RESOLVED (user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). v5 enters 205,000 in Fld Eng Budget!B21, the designated input cell. Was (v4, MED): 'Head of Service Delivery – [name]' (FE HC r16) had no salary entered, so FE 6610 carried $0 for this current employee. | Fld Eng Budget!B21 = 205,000; row 67 uses the roster formula of rows 59-66 (=IF(B$58>=$C$21,$B$21/12*(1+IF(B$58>=$B$25,$B$24,0)),0)...): start 2027-01-01 (C21) so 12 months paid, 17,083.33/month, +3% from 2027-10-01 (B24, B25) for 3 months (17,595.83/month): 2027 salary ~205,000; payroll tax 6.8% (B22) ~15,000; benefits 16.4% (B23) ~35,000; total ~255,000. FE!AG67 713,347 -> 919,884. | (~255,000) on the contribution (in the v5 headline) | resolved; was MED (owner confirmation) | None. v6: the Head of Service Delivery is on FE HC r16 and Fld Eng Budget r21 only, not on CO HC or PE HC (I-28). |
| I-27 | LOW | Logistics&WH Payroll!B56 (SD, not carried); FO!U52:AF52 | Logistics&WH Payroll excludes MH-05 ('Less: MH-05 Material Handler, logistics support (counted on the FO tab)'), but FO 5510 2027 (FO!U52) sums only Fld Ops Payroll rows 21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77, none of which is an MH-05 seat; 'MH-05' appears nowhere outside Logistics&WH Payroll. So this seat is in neither model. | Logistics&WH Payroll!B56 = -38,133 (deduction of MH-05's 2027 base pay, before burden). FO!U52 = ='Fld Ops Payroll'!F21+'Fld Ops Payroll'!F31+'Fld Ops Payroll'!F43+'Fld Ops Payroll'!F56+'Fld Ops Payroll'!F69+'Fld Ops Payroll'!F76+'Fld Ops Payroll'!F77+'Fld Ops Payroll'!F34+'Fld Ops Payroll'!F46+'Fld Ops Payroll'!F59+'Fld Ops Payroll'!F72. MH-05 mentions elsewhere: none. | 38,133 base pay missing (before burden) | impact 38,133 | SD/PO owners to decide where MH-05 is budgeted and add it. |
| I-28 | MED | 'HC-FO'!B15:D15; Fld Eng Budget!A15:C15, row 61; Fld Ops Payroll!B11; 'HC-FE'!B41:D41; 'HC-CO'; 'HC-PE' | v6 answers the person-level question with the HC rosters. Every person on FE HC, CO HC, PE HC, PO HC, FO HC, SD Fld Eng Budget, SD Fld Ops Payroll, SD Logistics&WH and SD Prod Payroll was compared by name where present, otherwise by title + salary + start (A-29). CO and PE: no person on the FE roster is on CO HC or PE HC (0 name matches, 0 title + salary matches). The Head of Service Delivery is on FE HC r16 and Fld Eng Budget r21 only (nearest title elsewhere: PE HC r22 Head of Production and Delivery, a different person at a different salary; I-35). One person is probably costed twice in the budget (name match only; title and salary differ; likely FO->FE move): Fld Eng Budget r15 Field Engineer (75,000, 'current employee') has the same full name as FO HC r15 Field Technician (~70,000), one of the 14 current techs Fld Ops Payroll costs by count (B11 = 14). FE HC has no salary for this person; its r41 'Field Engineer' row is open (no name, salary or start). | FE side 2027: salary ~75,000, with SD burden ~95,000. FO side, recalculated with Fld Ops Payroll B11 14 -> 13 (v7): +78,529 = payroll 78,198 (one current tech at model rates, salary 63,472.50) + 331 on 5330 (Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11); supervisor headcount unchanged in every month. v6 stated 78,198 (payroll only). Pair scan: 9 same-person pairs inside one P&L source (FE HC <-> Fld Eng Budget 7, FO HC <-> Fld Ops Payroll 2); 1 duplicate across P&L sources; 2 with the not-carried Logistics&WH model (I-17). Roster-to-P&L map: 02-build_roster_map_v6.csv (no names). | +78,529 to +~95,000 (budget overstated by one person if the duplicate is confirmed; pro rata if the move happens mid-year) | impact ~95,000 ($50k-250k) | SD / FO owners: confirm whether this person moved from FO to FE. Then remove them from one side (Fld Ops Payroll B11 14 -> 13, or Fld Eng Budget row 15) and, if the move is real, give FE HC r41 the salary and start month. No budget value changed in v6 or v7. |
| I-29 | LOW | Prod Payroll!M9; Fld Ops Payroll!M7; Fld Eng Budget!B59 (row formula); PO!AD33; PO!AD34; PO!AD35; CO!AD67; CO!AD68; CO!AD69; PE!AD67; PE!AD68; PE!AD69 | Raise timing is consistent (same % and month everywhere), but the eligibility rule is not: Fld Ops Payroll and Logistics&WH Payroll exclude staff hired in the months before the raise (Prod Payroll!M9), while Fld Eng Budget and the typed PO/CO/PE payroll rows apply the raise to the whole row. | Prod Payroll!M5 = 0.03, M6 = 2027-10-01, M9 = 6. Steps found in typed rows: PO!AD33 3.00%; PO!AD34 3.00%; PO!AD35 3.00%; CO!AD67 3.00%; CO!AD68 3.00%; CO!AD69 3.00%; PE!AD67 3.00%; PE!AD68 3.00%; PE!AD69 3.00%; FE!AD67 3.00%; FE!AD68 3.00%; FE!AD69 3.00%. | not determinable | hygiene | Payroll owners to confirm whether the eligibility rule should apply to all departments. |
| I-30 | LOW | DeploySum!A2, A7, A9, A11, A13, A29, A30, A35, A38, A39, A40, A41, A42 | The source labels say '$000s', but the values are whole dollars. v3 relabelled the 13 cells to '$' (A2 text: 'Dollars in $ (relabelled in v3; the source said $000s)'). Each cell has a comment quoting the original label, so the change is visible, not silent. | E.g. DeploySum!R13 total bookings 29,452,766 and R29 Production CapEx 32,410,900 are dollars: CapEx = units x unit cost in dollars (section 'Unit-cost reconciliation'), and recognized revenue is the same order as PO's 2026 revenue in dollars. | 0 | hygiene | Plan owner to fix the labels in the source (Revenue Roll-up / Deploy) so the next export is right. |
| I-31 | LOW | 'Depreciation Schedule'!A88:D97; PO!J20:M22; DeploySum!C19:E20 | Oct-Dec 26 go-lives are carried in the PO Dec-26 run rate, not added explicitly. The risk runs both ways. (a) Shortfall: PO steps up for 15 lifts and 53 trays in Q4-26, DeploySum has 18 and 67; if DeploySum is right the budget is short 39,057. (b) Possible double count: PO's Dec-26 step-up (3 lifts, 12 trays) has no DeploySum Dec-26 go-live. If these are units DeploySum places in Jan-27 (20 lifts, 60 trays, built Nov-26), they sit in both the run rate and the Jan-27 vintage: 37,457 too much. If (b) holds and DeploySum's Q4 counts are right, the gross Q4 shortfall is 76,514 and the net is still (39,057). The 5020 step-ups cannot be reproduced from DeploySum's peripheral cost. | PO 5011 monthly step-ups Oct/Nov/Dec: 6,964.29, 2,321.43, 2,321.43 = 9, 3, 3 lifts x 65,000/84. 5012: 1,933.33, 800.00, 800.00 = 29, 12, 12 trays x 8,000/120. 5020: 2,608.33, 1,025.00, 1,025.00 = 52.95, 20.81, 20.81 peripheral sets at 4,137.50/84 (not whole). DeploySum Oct/Nov/Dec lifts [9, 9, 0], trays [35, 32, 0]. Dec-26 step-ups with no DeploySum Dec-26 go-live: 3 lifts x 773.81 + 12 trays x 66.67 = 3,121.43/month, 37,457 for 2027. Gap not budgeted: 3 lifts + 14 trays = 3,254.76/month, 39,057 for 2027 (plus up to 10,639 if Q4-26 lift peripherals are not in 5020). | (39,057) to +37,457 (5020 Dec step: up to +12,300 more) | impact 39,057 (< $50k) | PO owner to say what the Oct/Nov/Dec-26 step-ups on PO rows 20-22 are (which go-lives, which month). Then the user chooses: keep the PO run rate (current), or Sep-26 run rate + DeploySum Oct-Dec 26 vintages. Do not do both. |
| I-32 | HIGH | 'Depreciation Schedule'!B21:B24; PO!M19:M22; PO!U19:AF19 | Existing-fleet depreciation is carried flat at the PO Dec-26 run rate for all 12 months of 2027. The flat carry is a builder assumption (A-17): the brief asked for the PO 2026 monthly depreciation as the existing-fleet input, not for a flat carry. The workbook has no asset register, so it cannot show whether any of these assets reach the end of their life, or are retired, in 2027. The largest line is 5010 SlipBot: 112,797.85/month = 1,353,574 in 2027. Whether the SlipBot fleet is fully depreciated, retired or ongoing is not in the files. DeploySum note 4 says no SlipBots are built and existing bots are redeployed, which suggests the fleet is in use. 5020's run rate basis is also unknown (I-31). Trend alternative: 5010 fell through 2026 (141,122 Jan -> 112,798 Sep, (3,541)/month); continuing that decline through 2027 from the Sep-26 level lowers depreciation by 276,164 (151,680 on the Jan-Aug actuals trend, (1,945)/month); if the decline also runs through Oct-Dec 26 (floored at 0) it lowers it by 403,624 (221,687 on the actuals trend). The 5020 base (8,212 in Jan-26, when 5011 was 0) predates SlipLift depreciation, so it is probably SlipBot-related and may share the SlipBot end-of-life risk (98,543 for 2027 at that rate). | Dec-26 run rates (PO!M): 5010 112,797.85, 5011 20,444.90, 5012 6,502.64, 5020 19,525.33; 2027 existing total 1,911,249. 5010 2026 actuals Jan-Aug 141,122.35 -> 127,510.00, forecast Sep-Dec flat 112,797.85; 2026 total 1,492,329. | up to +1,353,574 (5010 = 0); trend +276,164 (continued from Sep-26: +403,624); 5020 base up to +98,543 | impact 1,353,574 | USER DECISION: confirm SlipBot fleet status (fully depreciated / retired / ongoing / declining as in 2026) and the end-of-life month for any existing asset group. Change the section 2 input on the schedule if the run rate stops. |
| I-33 | MED | 'Depreciation Schedule'!B7, B11, B16; PO!U22:AF22 | SlipLift peripherals (4,137.50 per lift, from DeploySum CapEx) are depreciated on 5020 Robot Peripherals over 84 months. Both the GL and the life are builder assumptions: the user gave lives for SlipLifts and SlipTrays only. 5020 was chosen because PO's 2026 forecast books 5011 at exactly $65,000/84 per lift, so PO keeps peripherals out of 5011. | 2027 new-peripheral depreciation 63,836 (Dec-27 12,313.99/month). Moving it to 5011 changes the GL split only, not the total. A different life changes the amount in proportion (e.g. 60 months: 89,370). | 63,836 | impact 63,836 | User to confirm the peripherals GL (5020 or 5011) and life; both are input cells. |
| I-34 | MED | Fld Eng Budget!B22:B23; Fld Ops Payroll!B7:B8; 'HC-FE'!D6:D7; FE!AG68:AG69 | Payroll tax and benefits on FE salaries use the SD field rates (6.8% / 16.4%, Fld Eng Budget!B22:B23 = Fld Ops Payroll!B7:B8). FE HC uses the FE rates from the T&B file, 4.069% / 7.223% ('HC-FE'!D6:D7, stored as values, A-30). On the 2027 FE salary base 919,884 the budget carries 6630 62,552 and 6640 150,861; at FE HC rates they would be 37,432 and 66,442. Not changed in v6 (no budget change without a user decision). v7 (O6): every HC T&B tax rate (3.57%-6.85%) is below the 7.65% employer FICA, so the T&B rates are unverified (I-37); the 6630 part of the upside may not exist. | Difference 2027: 6630 +25,120, 6640 +84,419, total +109,539 more in the budget than at FE HC rates (on the matched people only, 816,751 of salary: +97,258). Other departments: FO HC rates 6.847% / 16.405% are within 0.047 points of the SD rates; PO, CO and PE payroll already use their HC rates. | +109,539 if the FE HC rates are right; +76,600 if the FE tax rate is at least 7.65% | impact 109,539 ($50k-250k) | User / Finance: choose the FE burden rates (FE HC T&B rates or the SD field rates). If FE HC, set Fld Eng Budget B22:B23 to the FE rates. |
| I-35 | MED | 'HC-PE'!A22:Z22; PE!AG67:AG69 | PE HC r22 Head of Production and Delivery (225,000, Sep-26 to Dec-27) is marked 'transfer?' in column A. The row is costed in PE 6610-6640 for all of 2027 (PE 2027 payroll equals PE HC). The person is on no other roster (0 name and 0 title matches), so there is no double count today. If the transfer happens, the cost leaves PE, and leaves COO if the receiving department is outside the five COO departments. | 2027 cost: salary ~225,000 + payroll tax ~10,000 (3.57%) + benefits ~20,000 (8.82%) = ~255,000. The HC tabs have Transfers In/Out blocks (rows 51-64) for such moves; none is filled. | up to +~255,000 (leaves COO from Jan-27); 0 if it moves within COO and is budgeted once | impact not determinable; owner confirmation needed (exposure ~255,000) | PE owner to confirm the transfer, the month and the receiving department; record it in the Transfers Out / In blocks so it is budgeted once. |
| I-36 | LOW | Fld Eng Budget!A15:C15, A19:C19; 'HC-FE'!B41:F41; FE!AG67 | Fld Eng Budget costs two rows that FE HC does not: r15 Field Engineer 75,000 (the same person as FO HC r15; I-28) and r19 Customer Support Specialist, a new hire from Aug-27 at 65,000 (links to r18). FE HC instead has an open 'Field Engineer' row (r41) with no salary or start. Together the two rows explain the whole gap between FE HC salary 816,751 and the budget's FE 6610 919,884. Start months differ for every matched person (HC Sep-26; Fld Eng Budget Jan-27), with no 2027 effect. v7: the Field Engineer Manager row (FE HC r35, Dec-26) is an open seat, not a person (I-39). | Gap 103,133 = r15 ~75,000 + r19 27,570.83. Matched people: 2027 monthly salary identical (max difference 0.00). The COO book's FE 6610 (675,701) is FE HC less FE HC r35 Field Engineer Manager (141,050, from Dec-26). | +33,967 if the Aug-27 hire is not approved (salary 27,571 + SD burden) | impact 33,967 (< $50k) | FE owner to confirm the Aug-27 Customer Support Specialist hire and add it to FE HC if approved; the r15 row is handled under I-28. |
| I-37 | MED | 'HC-FO'!D6; 'HC-PO'!D6; 'HC-CO'!D6; 'HC-FE'!D6; 'HC-PE'!D6; PO!AG34; CO!AG68; PE!AG68; Fld Ops Payroll!B7; Fld Eng Budget!B22 | The HC T&B employer payroll tax rates (A-30, stored values) are all below the 7.65% employer FICA (6.2% Social Security + 1.45% Medicare): FO 6.847%, PO 3.637%, CO 5.221%, FE 4.069%, PE 3.571%. A rate below 7.65% is possible only if salaries above the Social Security wage base pull the average down, and the rates would normally also carry unemployment taxes. They are unverified. PO, CO and PE payroll tax in the budget uses these rates, so it may be under-budgeted; FO and FE use the SD rate 6.8%, also below 7.65%. FE's I-34 upside rests on the FE rate. v8: PO production payroll is capitalised (PO 5110-5140 = 0), so PO's part is no longer an expensed P&L risk; the model's own 7.5% applies. | At 7.65% on every 2027 salary dollar (upper bound): PO +21,081, CO +12,834, PE +43,967 = +77,882 of tax; FO +26,350 and FE +7,819 against the SD 6.8%. I-34 at an FE tax rate of 7.65%: +76,600 instead of +109,539. | up to (56,801) CO/PE (v7 (77,882) incl. PO 21,081); up to (34,169) FO/FE | impact 56,801 ($50k-250k) | Finance: confirm what the T&B tax rates include (FICA, FUTA/SUTA, wage-base caps) and the rate to budget per department. Then reset 'HC-*'!D6 and, if needed, Fld Ops Payroll!B7 / Fld Eng Budget!B22. |
| I-38 | MED | Prod Payroll!B31:E31, B52:E52, B71:E71; Logistics&WH Payroll (SD, not carried) TL-01, MH-02; 'HC-PO' | The SD payroll models hire people before 2027 that the HC rosters do not show: Prod Payroll 15 (Sep-26: 3 lift, 1 tray, 1 sup; Nov-26: 6 lift, 3 tray, 1 sup) and Logistics&WH TL-01 Material Handling Team Lead (Dec-26), MH-02 Material Handler (Oct-26). None of them is on an HC roster; the workfile was last saved 2026-10-07, so at least the Sep-26 hires should be on it if they happened. The models may be older than the roster. v8: the model now drives the budget (capitalised labour and its depreciation), so its date matters more: its Sep-Dec 26 hires set the Oct-Dec 26 labour in the Jan-Feb 27 vintages (381,863). | Workfile saved 2026-10-07 (file properties); the SD book's properties show 2026-10-09 (a re-save, not the model date). The models' Sep-Dec 26 hires set the 2027 opening ramp (Prod Payroll: 15 ramp staff in Jan-27). | not determinable | impact not determinable; owner confirmation needed | SD / PO owners: when were Prod Payroll and Logistics&WH Payroll last updated? Were the Sep-Dec 26 hires made, deferred or dropped? Refresh the models before Decision #6. |
| I-39 | MED | 'HC-FE'!B34:F35; Fld Eng Budget!A20:C20, row 66; FE!AG67 | FE HC r35 Field Engineer Manager sits under 'Open Positions' (HC-FE row 34) with no employee: it is an open seat, not a person (v6 called it a matched person). The match with Fld Eng Budget r20 Field Engineering Manager is seat-to-seat on title + salary with the start month relaxed (A-29 amended). The sources disagree on whether the seat is filled: the COO book _2 leaves it out (FE 6610 = FE HC less r35), FE HC starts it in Dec-26, Fld Eng Budget costs it from Jan-27. | 2027 cost in the budget (salary + SD burden): 173,774; COO book _2 gap vs FE HC: 141,050 of salary. | up to +173,774 if the seat stays open all of 2027 | impact 173,774 ($50k-250k) | FE owner: is the Field Engineer Manager seat filled, and from when? Set Fld Eng Budget!C20 to the start month. |
| I-40 | HIGH | 'Depreciation Schedule'!B131:B132, rows 141-149; PO!U33:AF35; COO P&L!N36 | Scope of the capitalisation policy (Decision #10). The user confirmed that production labour is capitalised; brief v5 reads the policy as covering the whole Prod Payroll model, including the 9 current PO staff (PO 5110-5140), and v8 also capitalises the Oct-Dec 26 model labour into the Jan-Feb 27 go-lives it builds. The 2026 books point to a partial policy: COO 5100 production labour of 208,574 was expensed in 2026 (PO 197,323, PE 11,473), next to credits that fit a capitalised-labour credit (PO 6000 (309,871), PE 5140 (56,264); I-23). Idle-capacity labour (months with no builds roll into the next build, A-38) may also have to be expensed under the inventory rules. | Current 9 expensed ('Depreciation Schedule'!B131 = 0; ramp only capitalised): contribution 37,696 ((601,118)); 2027 labour depreciation 101,336. Oct-Dec 26 labour not capitalised (B132 = 0): +48,621. Both: (572,877). Labour in zero-build months rolled forward: Oct-26 81,851, Jan-27 140,751. | (601,118) if the current 9 stay expensed; +48,621 if the Oct-Dec 26 labour is not capitalised | impact 601,118 (> $250k) | Finance: confirm that the policy covers the current production staff, the Oct-Dec 26 labour and idle months; set 'Depreciation Schedule'!B131 / B132 to match (the workbook recalculates PO and the depreciation). |
| I-41 | MED | PO!U33:AF35; 'HC-PO'!B16:Z16, B20:Z20; Logistics&WH MH-01, MH-02 | PO 5110-5140 = 0 removes all 9 PO HC people from the expense, including the 2 material-handling roles (r16 Material Handling Team Lead, r20 Material Handler). Prod Payroll's 9 current staff match PO HC 9 by count only; on the 7-of-9 role reading (v7 B2) the 2 are warehouse staff tied to Logistics&WH (r20 = MH-01 by name; MH-02 backfills r16), so their cost is not production labour and would stay an expense. | The 2 people together at PO HC rates: 134,563 (2027 salary x (1 + 3.64% + 20.64%)). The 2 Prod Payroll seats they would leave stay in the model and are capitalised. | (134,563) on the 7-overlap reading; 0 on the 9 reading | impact 134,563 ($50k-250k) | PO owner: are r16 / r20 production or warehouse staff? If warehouse, budget them outside the capitalised labour (keep their PO HC cost in 5110-5140 or move it to 5350 Warehouse). |

### Variance scan: rows with |AG-N| > $50k and > 50% (regenerated from the v8 workbook; the generator first reproduces the v7 table exactly)

'%' = (AG - N) / N; 'n/m' where N is zero or negative, or AG is negative while N is positive. Rows new in v5: FE 69 6640 - Benefits - SG&A; FE 140 Benefits. No rows dropped. v8: 0 rows added, 23 changed, 1 removed (production labour capitalised).

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
| PO | 20 | 5011 - SlipLift Depreciation | 100,360 | 1,366,273 | 1,265,914 | 1261% |
| PO | 21 | 5012 - SlipCarrier Depreciation | 36,993 | 453,859 | 416,866 | 1127% |
| PO | 22 | 5020 - Robot Peripherals Depreciation | 158,415 | 298,140 | 139,724 | 88% |
| PO | 27 | Total - 5025 - Freight and Delivery - Production (Summary) | 57,197 | 0 | (57,197) | -100% |
| PO | 33 | 5110 - Salaries and Wages - Production | 137,080 | 0 | (137,080) | -100% |
| PO | 35 | 5140 - Benefits - Production | 54,271 | 0 | (54,271) | -100% |
| PO | 36 | Total - 5100 - Labor Expense - Production | 197,323 | 0 | (197,323) | -100% |
| PO | 37 | Total - 5000 - Robot Production and Deployment | 2,111,917 | 3,559,700 | 1,447,783 | 69% |
| PO | 38 | 5015 - Supplies and Materials | 2,839 | 101,250 | 98,411 | 3467% |
| PO | 42 | 5201 - Inventory Adjustments | 22,000 | 75,000 | 53,000 | 241% |
| PO | 63 | Total - Cost Of Sales | 2,361,338 | 3,915,922 | 1,554,583 | 66% |
| PO | 64 | Gross Profit | 5,062,601 | 11,647,724 | 6,585,123 | 130% |
| PO | 67 | 6610 - Salaries and Wages - SG&A | (308,059) | 0 | 308,059 | n/m |
| PO | 73 | Total - 6000 - Labor Expense - SG&A | (309,871) | 0 | 309,871 | n/m |
| PO | 98 | 7700 - Inventory Obsolescence-old | 636,000 | 0 | (636,000) | -100% |
| PO | 116 | Total - Expense | 461,703 | 171,650 | (290,053) | -63% |
| PO | 117 | Net Ordinary Income | 4,600,898 | 11,476,074 | 6,875,175 | 149% |
| PO | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| PO | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| PO | 132 | Net Income | 4,685,709 | 11,476,074 | 6,790,364 | 145% |
| PO | 137 | Salaries and Wages | (159,704) | 0 | 159,704 | n/m |
| PO | 140 | Benefits | 51,491 | 0 | (51,491) | -100% |
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
| COO P&L | 20 | 5011 - SlipLift Depreciation | 100,360 | 1,366,273 | 1,265,914 | 1261% |
| COO P&L | 21 | 5012 - SlipCarrier Depreciation | 36,993 | 453,859 | 416,866 | 1127% |
| COO P&L | 22 | 5020 - Robot Peripherals Depreciation | 158,415 | 298,140 | 139,724 | 88% |
| COO P&L | 24 | 5025 - Freight and Delivery - Production (Summary) | 50,108 | 0 | (50,108) | -100% |
| COO P&L | 27 | Total - 5025 - Freight and Delivery - Production (Summary) | 62,008 | 0 | (62,008) | -100% |
| COO P&L | 29 | 5040 - Freight & Delivery - Deployment | 85,214 | 765,000 | 679,786 | 798% |
| COO P&L | 30 | 5050 - Travel - Deployment | 94,810 | 392,987 | 298,177 | 314% |
| COO P&L | 33 | 5110 - Salaries and Wages - Production | 202,457 | 0 | (202,457) | -100% |
| COO P&L | 36 | Total - 5100 - Labor Expense - Production | 208,574 | 0 | (208,574) | -100% |
| COO P&L | 37 | Total - 5000 - Robot Production and Deployment | 2,305,147 | 4,759,868 | 2,454,721 | 106% |
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
| COO P&L | 63 | Total - Cost Of Sales | 4,478,016 | 11,652,235 | 7,174,220 | 160% |
| COO P&L | 91 | 7200 - Contractors | 214,591 | 0 | (214,591) | -100% |
| COO P&L | 98 | 7700 - Inventory Obsolescence-old | 636,000 | 0 | (636,000) | -100% |
| COO P&L | 106 | 8600 - Repairs and Maintenance | 51,212 | 0 | (51,212) | -100% |
| COO P&L | 117 | Net Ordinary Income | (984,033) | 638,814 | 1,622,847 | n/m |
| COO P&L | 121 | 9150 - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 122 | Total - Other Income | 104,811 | 0 | (104,811) | -100% |
| COO P&L | 131 | Net Other Income | 84,811 | 0 | (84,811) | -100% |
| COO P&L | 132 | Net Income | (899,222) | 638,814 | 1,538,036 | n/m |
| COO P&L | 137 | Salaries and Wages | 3,264,812 | 5,764,388 | 2,499,575 | 77% |
| COO P&L | 139 | Payroll Taxes | 210,079 | 339,448 | 129,369 | 62% |
| COO P&L | 140 | Benefits | 471,094 | 817,299 | 346,204 | 73% |

## Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; v8: payroll rows regenerated)

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
| 137 | Salaries and Wages | 3,238,031 |  | 528,452 | 919,884 | 1,078,020 | 5,764,388 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 = 0 in 2027, capitalised in v8: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |
| 139 | Payroll Taxes | 210,802 |  | 27,593 | 62,552 | 38,501 | 339,448 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 = 0 in 2027, capitalised in v8: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |
| 140 | Benefits | 508,405 |  | 62,916 | 150,861 | 95,116 | 817,299 | n/a (memo total) | $0 | Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 = 0 in 2027, capitalised in v8: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above). |

Result: 0 likely double counts on the same GL row. Unclear rows are logged as I-28. v6: the HC rosters answer the person-level question for rows 67-69 (no FE person on CO HC or PE HC); the one person costed twice sits on two different GL rows (FO 5510 and FE 6610), see I-28. Cross-row overlaps found while tracing: none between FO payroll and Logistics&WH (FO HC r21 Operations Coordinator is excluded from Logistics&WH, Logistics&WH Payroll!B55, and costed in Fld Ops Payroll row 76: 2027 ~75,000); one seat in neither model (MH-05, I-27); the current employee with no salary in v4 (I-26) has a salary from v5 (Fld Eng Budget!B21 = 205,000).

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

Rates and timing only: other sheets read only these typed raise inputs from Prod Payroll, never a headcount or cost cell, except the v8 capitalised-labour block on the Depreciation Schedule (rows 137-140 read Prod Payroll rows 41, 62, 79, 81; rows 141-142 read its rate inputs). v8: Prod Payroll computes in full (0 errors; XLOOKUP replaced, A-28) and reaches the budget only as capitalised-labour depreciation (PO 5011 / 5012). PO 5110-5140 2027 (PO!U33:AF35) are formulas = 0 (capitalised), and FO 5510 shares no headcount source with Prod Payroll: no double count through Prod Payroll.

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
| PO | 33 | 5110 - Salaries and Wages - Production | False (v8: formula = 0, capitalised) | none (0 all year) |
| PO | 34 | 5130 - Payroll Taxes - Production | False (v8: formula = 0, capitalised) | none (0 all year) |
| PO | 35 | 5140 - Benefits - Production | False (v8: formula = 0, capitalised) | none (0 all year) |
| CO | 67 | 6610 - Salaries and Wages - SG&A | True | AD: 3.00% |
| CO | 68 | 6630 - Payroll Taxes - SG&A | True | AD: 3.00% |
| CO | 69 | 6640 - Benefits - SG&A | True | AD: 3.00% |
| PE | 67 | 6610 - Salaries and Wages - SG&A | True | AD: 3.00% |
| PE | 68 | 6630 - Payroll Taxes - SG&A | True | AD: 3.00% |
| PE | 69 | 6640 - Benefits - SG&A | True | AD: 3.00% |
| FE | 67 | 6610 - Salaries and Wages - SG&A | False | AB: 7.34%, AD: 3.00% |
| FE | 68 | 6630 - Payroll Taxes - SG&A | False | AB: 7.34%, AD: 3.00% |
| FE | 69 | 6640 - Benefits - SG&A | False | AB: 7.34%, AD: 3.00% |

9 of 12 payroll rows step by Prod Payroll!M5 (3.00%) in month 10 of 2027 (Prod Payroll!M6; v8: PO 5110-5140 are 0, capitalised); the raise inputs on Fld Ops Payroll / Fld Eng Budget / Logistics&WH are all links to those cells, so % and month are consistent. FE's other step is the new hire 'Customer Support Specialist – New hire' starting 2027-08-01. Rule difference: eligibility (Prod Payroll!M9) is applied in Fld Ops Payroll (`=F20*$B$6/12+IF(F$19>=$M$6,MIN(F20,INDEX($B20:$Q20,IFERROR(M...`) and Logistics&WH, but not in Fld Eng Budget (`=IF(B$58>=$C$13,$B$13/12*(1+IF(B$58>=$B$25,$B$24,0)),0)`) or the typed rows: I-29.

### Logistics & Warehouse payroll and MeLi

- Logistics&WH Payroll 2027 (S51) 547,441; Sep-Dec 26 (R51) 92,495. Components 2027: Base salaries 440,293; Payroll taxes 29,940; Benefits 72,208; New-hire cost 5,000. Formulas referencing the sheet in either book: 0.
- PO 2027 (v8: production labour capitalised): 5110 - Salaries and Wages - Production 0; 5130 - Payroll Taxes - Production 0; 5140 - Benefits - Production 0; Total - 5100 - Labor Expense - Production 0 (v7 652,820; 2026 197,323); 5350 - Warehouse 0 (2026 3,341). See I-17, I-41.
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
- D1 (v6): Patch the v5 package, do not round-trip it. The HC tabs are transplanted at the XML level; every v5 part except workbook.xml, its rels, [Content_Types].xml, styles.xml (append only) and Collation Notes keeps its bytes, so the v5 -> v6 diff on the existing sheets is exactly 0.
- D2 (v6): HC tabs keep the workfile's own formulas and cached values; sheet references are renamed to the new tab names. The 10 T&B rate links are external and are stored as values (A-30), as DeploySum's external links were in v3. Theme colours are resolved to RGB because the two workbooks have different themes.
- D3 (v6): COO book _2 stays the P&L source (brief v4); the workfile's P&L tabs are not imported. PO, CO and PE payroll are identical anyway; FO and FE come from the SD models.
- D4 (v6): Net increment = model total less the model's own cost of the people already on HC rosters (A-27). Both sides use the model's rates, so the net is the ramp alone. The model-vs-PO HC cost difference on the same 9 people ((22,315)) is shown, not netted.
- D5 (v6): The Logistics Manager seat (LOG-01) is taken out of the I-17 net although it overlaps CO, not PO: the model's own note classifies it as Central Operations and the person is on CO HC.
- D6 (v6): Prod Payroll's 9 current staff are matched to the 9 PO HC people by headcount only (the model has no names or titles); stated as a count match.
- D7 (v6): The Field Engineer Manager is matched on title + salary although the start month differs (HC Dec-26; Fld Eng Budget!D20 calls its Jan-27 a placeholder); the 2027 cost is identical. Matching is one-to-one: a person matched by name is not matched again on title + salary (this keeps the four new Material Handler seats from matching PO HC r20, who is seat MH-01).
- D8 (v6): The FO/FE duplicate person (I-28) is not resolved in the budget (no budget change); both resolutions are quantified.
- D9 (v6): The range keeps v5's convention (lower end = quantified downsides added; upper end = I-32 full only) so v5 and v6 compare; the new upsides are listed, not added.
- D10 (v6): Carried v5 text that quoted employee names (I-15, I-26, one cross-department line) is rewritten with dept + title + roster row; the meaning is unchanged.
- D11 (v6): A roster-to-P&L map is written as a CSV with no names (roster, row, title, salary, start, P&L source, flags); per-person salaries appear there because the match rule uses them. The notes quote per-person amounts only where a finding needs them (I-28, I-35, the FO/FE and PO match evidence).
- D1 (v7): Notes and presentation only. build_v7.py copies every v6 part byte for byte and renders only the Collation Notes part, so no budget cell can move.
- D2 (v7): Decision #1 (expensed or capitalised) is placed first and v6's decisions are renumbered #2-#9, as the handoff asked; cross-references in carried text were updated.
- D3 (v7): Capitalised case = depreciation only, by the existing Depreciation Schedule logic. The lift / tray split is derived from the model (lift and tray ramp), so the handoff's fallback split is shown as a check, not used. Supervisors are allocated pro rata to the lift : tray ramp, labelled as an assumption (A-32). Labour is spread per unit built in 2027 (A-33). A third case, labour already inside the 65,000 / 8,000 unit cost (effect 0), is shown because the handoff's question names that unit cost.
- D4 (v7): 7-overlap: the 2 Prod Payroll current seats that no PO HC production person fills are costed at the model's average current cost per head; the lift-only / tray-only range is shown (A-34). The deduplicated 9-overlap combined figure adds MH-01 back, because the name match (r20 = MH-01) is firmer than the count match.
- D5 (v7): Lower bound 1 now uses the deduplicated 7-overlap combined figure (the most adverse consistent reading); lower bound 2 excludes I-05; the upper end keeps v6's convention (I-32 only) so the versions compare. I-37 is not added to the range because the rates are unverified and the figure is an upper bound.
- D6 (v7): The I-28 FO side is computed by LibreOffice recalculation of a scratch copy with Fld Ops Payroll B11 reduced by one (scen_v7.py), so every knock-on (Fld Maint Budget!B29 -> 5330; the supervisor ratio, unchanged) is included.
- D7 (v7): Privacy. Per-person amounts for identified employees are rounded to $5k in the md only (paylist_v7.py). The Collation Notes sheet keeps exact figures because the same workbook holds the named HC tabs, and it carries the CONFIDENTIAL banner. A planned hire (Fld Eng Budget r19, I-36) and open seats (FE HC r35, I-39) are not people and stay exact. No per-person CSV is written in v7; the scratch name lists of the v6 and v7 builds are deleted after the build.
- D8 (v7): The O6 test uses the statutory 7.65% (A-31) and ignores the Social Security wage base, so the gaps are upper bounds; Finance is asked for the real rates.
- D1 (v8): Patch, do not round-trip (v5 method). Stage 1 = v7 + the formula edits; LibreOffice recalculates it in full; values are written only for the edited cells and their static downstream trace (deps_v5.py), and the build stops if any other cell moves by more than 1e-6. Every other cell keeps its v7 bytes.
- D2 (v8): XLOOKUP is replaced by IF / INDEX / MATCH / ISNA (brief v5: INDEX/MATCH, 'next tier up, else max'), not v6's SMALL/COUNTIF: MATCH compares numbers directly, while COUNTIF("<"&x) turns a decimal x into text. Proven equal three ways (v7 scratch, Python replica, model totals).
- D3 (v8): The capitalised labour is the Prod Payroll model ('the file's formula', brief v5), not the PO HC roster: the current 9 are capitalised at the model's rates (630,504), and their PO HC cost (652,820) leaves PO. The 22,315 difference between the two costings goes with it.
- D4 (v8): PO 5110-5140 2027 = (1 - B131) x the v7 amount, not a bare 0: the formula gives 0 when capitalised, keeps the v7 amount visible, and makes the sensitivity a single switch. Column AI labels the rows CAPITALISED.
- D5 (v8): Labour per unit by build month (brief v5 item 2) instead of v7's annual average; months with no builds roll forward (A-38). The bridge shows the effect of each change from v7's 64,735.
- D6 (v8): The Oct-Dec 26 labour is included where its builds go live in 2027 (brief v5), with a switch (B132); the Sep-26 labour is not added because its units went live in 2026 (inside the PO run rate); it is shown as a caveat row.
- D7 (v8): The new block sits below the existing schedule (rows 128+); section 4 (rows 79-82) is not edited, so the labour depreciation is added at PO rows 20/21 (an allowed area) and row 197 gives the total.
- D8 (v8): Caveats: the v7 expensed / capitalised-on-top / inside-unit-cost rows are dropped (policy decided). Lower bound 1 uses the booked policy, lower bound 2 the scope sensitivity; each uses the more adverse I-17 reading consistent with it. Upper end unchanged in kind (I-32 only).
- D9 (v8): Privacy. The md keeps v7's $5k rounding; the banner now says that $5k-multiple salaries stay exact (paylist_v8.py counts them). No per-person CSV is written; the scratch name lists are deleted after the build.

## Not done / limits

- The external workbook '[1]' is still not available: DeploySum holds the 9/30/26 cached values, not live links.
- No fixed-asset register was supplied, so existing-fleet depreciation is a run rate, not an asset-by-asset schedule. End-of-life dates are unknown (I-32).
- Not opened in Microsoft Excel. Prod Payroll's XLOOKUP rows show #NAME? in LibreOffice 24.2 and may evaluate in Excel (untested). (v8: replaced by INDEX/MATCH; evaluates in LibreOffice.)
- No change made in v3 to FO, FE, CO, PE, or to PO lines other than 12 and 19-22 (and their subtotals/ratios); v5 changes only Fld Eng Budget!B21 (FE payroll and its totals recalculate). 4500/4900 stay 0 by assumption.
- v2 limits on page setup, sheet-scoped names and Google-specific parts still apply.
- v4: revenue effect of unsigned/forecast bookings and the revenue-vs-go-live timing (A-22, A-25) cannot be quantified from the workbook; the Revenue Roll-up and 2026 Exist New tabs of the plan were not supplied.
- v5: the explanatory text on the Depreciation Schedule tab (B17/D17, D21, row 19 heading) was not edited; it is superseded by A-17, A-18, A-19 and I-31 (Collation Notes line, N1).
- v5: the workbook could not confirm the Head of Service Delivery is not also inside CO or PE typed SG&A payroll; v6 confirms it from the HC rosters (I-28). The salary is the current rate, raised from Oct-27 like the rest of the roster.
- v5: not opened in Microsoft Excel; Excel will show the stored values until it recalculates (they match a LibreOffice recalculation).
- v6: no budget value was changed. The payroll findings (I-05, I-17, I-28, I-34, I-35, I-36) are exposures and decisions for the owners and the user.
- v6: Prod Payroll has no names or titles, so its overlap with PO HC is a headcount match; Fld Ops Payroll's 14 current techs are matched to FO HC the same way.
- v6: the HC tabs' T&B rates are the workfile's cached values (the T&B workbook was not supplied). The HC tabs are provenance only: no budget cell reads them.
- v6: not opened in Microsoft Excel. The HC tabs keep the workfile's formulas and were recalculated in LibreOffice with 0 errors; the Prod Payroll tray / supervisor figures come from the scratch evaluation (A-28), not from cells in this workbook (which still show #NAME? in LibreOffice).
- v6: whether the FO/FE person moved departments, whether the PE row transfers, and which burden rates FE should use are owner questions; the notes quantify each answer.
- v7: no budget value was changed. Decision #1, the 7-overlap reading, the T&B rates (I-37), the model date (I-38) and the open FE seat (I-39) are questions for the user, Finance and the owners; the notes quantify each answer.
- v7: the capitalised case is an approximation at the budget's level of detail (labour per unit built, depreciation by go-live vintage). It does not model a cost roll per build month, the capitalisation of the current staff already in PO 5110-5140, or the 2026 labour in the Jan-Feb 27 go-lives. (v8: superseded - v8 rolls the cost per build month, capitalises the current staff and includes the Oct-Dec 26 labour.)
- v7: the SD book's file date is a re-save, so the models' own update date cannot be read from the files (I-38).
- v8: not opened in Microsoft Excel. The new formulas use standard functions (INDEX, MATCH, ISNA, IFERROR, SUMIF, SUMPRODUCT, EOMONTH, YEAR).
- v8: idle months (no builds) are capitalised into the next build month (A-38); inventory rules may require abnormal idle-capacity labour to be expensed. Finance to confirm (I-40); not quantified separately beyond the Oct-26 and Jan-27 amounts in I-40.
- v8: the existing-fleet run rate (PO Dec-26 forecast) carries no labour for 2026 go-lives; only the Sep-26 part is quantified (caveat row).
- v8: 2026 columns are untouched, so 2026 still expenses its 5100 production labour; whether 2026 should also be restated is outside this budget (I-40).
- v8: the Depreciation Schedule's text at A2 ('Section 4 feeds PO rows 19-22') predates v8 and was not edited (rows 1-126 are outside the allowed areas); Collation Notes records it.
