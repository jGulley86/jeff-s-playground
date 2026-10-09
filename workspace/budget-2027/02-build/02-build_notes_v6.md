# 02-build notes v6 - 2027 COO budget collation

## Decisions pending

8 user decisions are open (4 new in v6: #5-#8). The builder has not resolved them; the budget carries the 'current treatment' column. Effects are on the 2027 COO contribution, each on its own.

| # | Decision (user) | Issue | Current treatment in the budget | Alternatives: effect on 2027 COO contribution (+ raises, ( ) lowers) | Who |
|---|---|---|---|---|---|
| 1 | SlipBot fleet status (5010 depreciation) | I-32 | Carried flat at the PO Dec-26 run rate 112,797.85/month = 1,353,574 in 2027 (builder assumption, A-17). | Fully depreciated or retired from Jan-27: +1,353,574. Continue the 2026 decline ((3,541)/month, Jan-Sep 26) from the Sep-26 level in Jan-27: +276,164 (actuals Jan-Aug only, (1,945)/month: +151,680). Same decline also running through Oct-Dec 26, floored at 0: +403,624 (actuals-only slope: +221,687). Ongoing at the run rate: 0. Related: the 5020 base of 8,212/month (Jan-26, before any SlipLift depreciation) may end with the SlipBots: up to +98,543. | User, with PO/Finance (fixed-asset register) |
| 2 | Q4-26 go-lives: PO run rate or DeploySum | I-31 | Inside the PO Dec-26 run rate: PO steps up for 15 lifts / 53 trays (DeploySum: 18 / 67). | Sep-26 run rate + DeploySum Oct-Dec 26 vintages: (39,057). If PO's Dec-26 step-up (3 lifts, 12 trays) is Jan-27 units already in the Jan-27 vintage and PO's Oct/Nov counts are right: +37,457. Keep as is: 0. | User, after the PO owner says what the Q4-26 step-ups are |
| 3 | SlipLift peripherals: GL and useful life | I-33 | 5020 Robot Peripherals, 84 months: 63,836 of 2027 depreciation (builder assumption, A-10/A-11). | GL 5011 instead of 5020: 0 (moves 63,836 from PO row 22 to row 20). Life 60 months: (25,534). Life 120 months: +19,151. | User |
| 4 | Revenue split across 4100 / 4500 / 4900 | I-01 (A-02, A-03) | All 15,563,646 of plan revenue on 4100; 4500 and 4900 = 0 (orchestrator assumption). | Split the plan revenue across the three lines: 0 (classification only; gross margin unchanged). Budget implementation / one-time revenue in addition to the plan: not determinable (2026 4500 + 4900: 1,060,861). | User / Finance |
| 5 | Production and warehouse payroll (PO 5110-5140) | I-05, I-17 | PO 5110-5140 = the 9 current PO HC staff, flat (652,820); no ramp hires. | Add the Prod Payroll ramp: (1,962,389). Add the 7 new Logistics&WH seats: (336,530). Both: (2,298,919). Keep as is: 0. (Net of the people already on PO HC and CO HC; not the model totals.) | User, with the PO owner |
| 6 | One person costed in both FO and FE | I-28 | Costed twice: one of the 14 current techs in Fld Ops Payroll and Fld Eng Budget row 15. | Remove from FO (B11 14 -> 13): +78,198. Remove from FE (row 15): +93,093. | SD / FO owners |
| 7 | FE payroll tax and benefit rates | I-34 | SD field rates 6.8% / 16.4% on FE salaries. | FE HC (T&B) rates 4.069% / 7.223%: +109,539. Keep: 0. | User / Finance |
| 8 | PE 'transfer?' row (Head of Production and Delivery) | I-35 | In PE 6610-6640 for all of 2027 (254,785). | Leaves COO from Jan-27: +254,785. Moves within COO: 0 (budget it once, on the receiving department). Stays: 0. | PE owner |

v6 changes **no budget value**. It brings the six HC tabs of the COO HC & PL workfile into the workbook as supporting tabs and reconciles every payroll source against those employee-level rosters. The 2027 COO contribution stays **139,032** (v5 139,032). What changes is the reading of it: net of the people already on PO HC, the production payroll ramp the budget does not carry is 1,962,389 (I-05), and the warehouse seats add 336,530 (I-17). Diff vs v5: 0 formula and 0 value differences on 12 existing sheets (27,701 cells); see 'v5 -> v6 diff'.

## Headline: 2027 COO contribution

| Line | COO P&L row | 2026 (N) | 2027 v6 (AG) | Change | % | 2027 v5 (AG) | v6 - v5 |
|---|---|---:|---:|---:|---:|---:|---:|
| Revenue (company recognized revenue, 9/30/26 sales plan) | 16 | 7,423,940 | 15,563,646 | 8,139,706 | 110% | 15,563,646 | 0 |
| COGS (COO departments) | 63 | 4,478,016 | 12,152,017 | 7,674,002 | 171% | 12,152,017 | 0 |
|   of which depreciation (in COGS) | 19-22 | 1,788,097 | 3,318,808 | 1,530,712 | 86% | 3,318,808 | 0 |
| Gross Profit | 64 | 2,945,924 | 3,411,628 | 465,704 | 16% | 3,411,628 | 0 |
| Opex (COO departments) | 116 | 3,929,957 | 3,272,597 | (657,361) | -17% | 3,272,597 | 0 |
| COO contribution before other income (workbook label 'Net Ordinary Income') | 117 | (984,033) | 139,032 | 1,123,065 | n/m | 139,032 | 0 |
| Net Other Income | 131 | 84,811 | 0 | (84,811) | -100% | 0 | 0 |
| **COO contribution** (workbook label 'Net Income') | 132 | (899,222) | 139,032 | 1,038,254 | n/m | 139,032 | 0 |

- **2027 COO contribution (COO P&L AG132): 139,032**, unchanged from v5. Revenue 15,563,646 (all to 4100, orchestrator assumption); COGS + Opex 15,424,614.
- Issues: 4 HIGH, 11 MED, 20 LOW open; 1 RESOLVED. v6 raises I-05 to HIGH and adds I-34 (MED), I-35 (MED) and I-36 (LOW).

### Caveats on the headline (read before using the figure)

(1) What the figure is. The bottom line, 139,032, is a **COO contribution**: the company's recognized revenue (15,563,646, all of it) less the costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: 15,424,614). Costs outside COO (for example sales, G&A, R&D) are not in this workbook, so it is **not company Net Income**. The workbook row keeps its GL label 'Net Income' (COO P&L!A132) because v4 and v5 change no label on the P&L tabs; the notes and Collation Notes call it 'COO contribution'.

(2) What the revenue is. 2027 revenue is the 9/30/26 sales plan's recognized revenue (DeploySum row 40, static cached values, A-24), not signed contracts. It includes unsigned and forecast bookings: Sep-Dec 26 bookings of 3,544,300 include 2,264,000 of unsigned forecast at 100% (DeploySum note 5, A49: bookings are gross ACV), and all 29,452,766 of FY27 bookings are forecast (new logos 24,016,000, expansion 5,436,766). 7,618,410 (49%) of 2027 revenue is above the Dec-26 exit rate x 12 (7,945,236), so it depends on go-lives that have not happened yet.

(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. v6: I-05 and I-17 are **net increments** (SD model ramp less the people already on HC rosters, A-27), so they no longer overlap; the 'I-05 + I-17' row shows both together.

| Item | Direction | What could happen | Effect on 2027 COO contribution | Contribution after this item alone | Source cells |
|---|---|---|---:|---:|---|
| I-05 | downside | Production payroll ramp (SD Prod Payroll) that PO 5110-5140 does not carry: model 2027 total 2,592,894 (lift 1,622,423, tray 729,177, supervisors 241,294) less the model's cost of the 9 current staff already in PO (630,504). Net of PO HC (v5 showed the gross lift-only gap, 969,603). | (1,962,389) | (1,823,358) | Prod Payroll!S81 (tray/supervisor rows evaluated per A-28); PO!AG33:AG36; 'HC-PO'!Z67:Z70 |
| I-17 | downside | Logistics & warehouse seats (SD model, not carried) that no HC roster holds: 7 seats, net of the 2 seats that are already on CO HC r17 and PO HC r20 (210,912 of the model's 547,441). | (336,530) | (197,498) | SD Logistics&WH Payroll!S51 less LOG-01 and MH-01 (not carried) |
| I-05 + I-17 | downside | Both payroll ramps together. No person-level overlap is left between them: the two models size different teams (production builders and supervisors vs warehouse seats) and the people already on HC rosters are taken out of each. | (2,298,919) | (2,159,887) | as above |
| I-10 | downside | FO/FE lines with 2026 spend budgeted at 0 for 2027 (5920 software, 6610 SG&A salaries, 7200 contractors); effect if they continue at the 2026 level. | (384,425) | (245,393) | FO!N58, N67, N91; FE!N91 (AG = 0) |
| I-26 | RESOLVED | RESOLVED (user-confirmed 2026-10-09): Head of Service Delivery salary 205,000/year entered in v5 and now inside the headline (2027 cost 254,454: salary 206,538 + payroll tax 14,045 + benefits 33,872; v4 contribution was 393,486). No remaining exposure. | 0 (now in the headline) | 139,032 | Fld Eng Budget!B21 = 205,000 |
| I-28 | upside | One person costed twice (FO HC r15 Field Technician = Fld Eng Budget r15 Field Engineer, same name): remove from FO (Fld Ops Payroll B11 14 -> 13; one current tech at model rates). | +78,198 | 217,230 | Fld Ops Payroll!B11, rows 20-24 |
| I-28 | upside | Same person: remove from FE instead (Fld Eng Budget row 15, 75,000 at SD burden rates). | +93,093 | 232,125 | Fld Eng Budget!B15; rows 61, 69-70 |
| I-31 | two-way | Shortfall if DeploySum's Q4-26 go-lives are right (3 lifts, 14 trays more than PO's run rate). | (39,057) | 99,975 | PO!J20:M21; DeploySum!C19:E20 |
| I-31 | two-way | Double count if PO's Dec-26 step-up (3 lifts, 12 trays; DeploySum Dec-26 go-lives 0) is Jan-27 units (20 lifts, 60 trays go live Jan-27, built Nov-26). Excludes the 5020 Dec step (+12,300 more if it is the same units). | +37,457 | 176,489 | PO!L20:M21; DeploySum!E19:F20 |
| I-32 | upside | SlipBot fleet fully depreciated or retired from Jan-27 (5010 = 0). | +1,353,574 | 1,492,606 | PO!M19; 'Depreciation Schedule'!B21 |
| I-32 | upside | Trend alternative: 5010 keeps falling at the 2026 rate (141,122 Jan-26 -> 112,798 Sep-26, (3,541)/month). | +276,164 | 415,196 | PO!B19, J19, M19 |
| I-32 | upside | Trend alternative continued from Sep-26: the same (3,541)/month decline also runs through Oct-Dec 26, so Jan-27 starts 4 months below Sep-26 (98,636 in Jan-27, 59,689 in Dec-27; floored at 0, 0 months at the floor). | +403,624 | 542,656 | PO!B19, J19, M19 |
| I-33 | two-way | Peripherals life 60 months instead of 84 (a longer life, e.g. 120 months, gives the opposite sign). | (25,534) | 113,498 | 'Depreciation Schedule'!B11 |
| I-34 | upside | FE payroll tax and benefits at the FE HC rates (4.069% / 7.223%) instead of the SD rates (6.8% / 16.4%) on the same FE salary base. | +109,539 | 248,571 | Fld Eng Budget!B22:B23; 'HC-FE'!D6:D7; FE!AG68:AG69 |
| I-35 | upside | PE HC r22 Head of Production and Delivery ('transfer?') leaves COO from Jan-27. 0 if the role moves to another COO department and is budgeted there once. | +254,785 | 393,817 | 'HC-PE'!A22, Z22; PE!AG67:AG69 |
| I-36 | upside | The Aug-27 Customer Support Specialist hire on Fld Eng Budget (not on FE HC) is not approved. | +33,967 | 172,999 | Fld Eng Budget!B19:C19, row 65 |
| A-14 | upside | Depreciation convention: mid-month in the go-live month instead of a full month. | +137,417 | 276,448 | 'Depreciation Schedule'!B13 |
| A-14 | upside | Depreciation convention: start the month after go-live. | +274,833 | 413,865 | 'Depreciation Schedule'!B13 = 1 |
| A-22 | downside | Revenue rests on unsigned / forecast bookings (Sep-Dec 26 includes 2,264,000 unsigned at 100%). Revenue effect not determinable from the workbook. | n/d | n/d | DeploySum!A49 (note 5), row 40 |

**Sign-flip statement (computed, net increments):** The 2027 COO contribution of 139,032 changes sign on I-05 alone (139,032 - 1,962,389 = (1,823,358)) or I-17 alone (139,032 - 336,530 = (197,498)) or I-10 alone (139,032 - 384,425 = (245,393)). I-31 alone leaves 99,975. Together, I-05 + I-17 (net) take it to (2,159,887). I-10 with the I-31 shortfall gives (284,450). All quantified downsides together (I-05 net, I-17 net, I-10, I-31 shortfall): (2,583,369). Upside: I-32 can add up to 1,353,574 (contribution 1,492,606); the trend alternative adds 276,164 (415,196), or 403,624 (542,656) if the decline also ran through Oct-Dec 26. New in v6 and smaller: I-28 +78,198 to +93,093, I-34 +109,539, I-35 up to +254,785, I-36 +33,967. With costs held fixed, revenue 139,032 (0.9%) below plan also takes the contribution to zero. Conclusion: the sign of the 2027 COO contribution is not established by this budget, and the production payroll question (I-05) now dominates it. Treat 139,032 as a point estimate inside a range from (2,583,369) to 1,492,606 (illustrative extremes of quantified items; excludes I-02, A-22; lower end = all four quantified downsides added: I-05 net, I-17 net, I-10, I-31 shortfall; I-05 and I-17 are net of the people already on HC rosters, so they no longer overlap; upper end = I-32 full only, the other upsides A-14, I-28, I-31 double count, I-33, I-34, I-35 and I-36 are not added) until I-05, I-17 and I-32 are answered. v5 range: (1,801,495) to 1,492,606.

## Changes from v5

| Item | Point | What v6 did | Where |
|---|---|---|---|
| HC tabs | Supporting rosters (provenance, read-only) | HC-FO, HC-PO, HC-CO, HC-FE, HC-PE, HC-COO copied cell by cell with styles from the workfile, after Fld Eng Budget; formulas re-pointed to the new tab names; 10 T&B rate links stored as values; 0 errors after recalculation. | HC-* tabs; 'HC tabs' section of the md |
| Budget values | Unchanged | 0 formula and 0 value differences vs v5 on the 12 existing sheets; contribution 139,032 (v5 139,032). | v5 -> v6 diff |
| I-05 | Production payroll, net of PO HC | MED -> HIGH. Net increment 1,962,389 (model 2,592,894 less its cost of the 9 current staff); v5 gross lift-only gap 969,603. | I-05; caveat table |
| I-17 | Warehouse payroll, net of HC overlaps | HIGH. Net 336,530 (model 547,441 less the 2 seats already on CO HC r17 and PO HC r20). | I-17; caveat table |
| I-28 | Person-level overlap check | Answered from the rosters: Head of Service Delivery not on CO or PE; 1 person costed in both FO and FE (+78,198 to +93,093). | I-28; Decisions pending #6 |
| New issues | I-34, I-35, I-36 | FE burden rates (+109,539); PE 'transfer?' row (254,785); FE roster differences (+33,967). | Issues; Decisions pending #7-8 |
| Sign flip | Recomputed with net increments | v5 range (1,801,495) to 1,492,606; v6 (2,583,369) to 1,492,606. | Sign-flip statement |
| Privacy | Employee names removed from carried text | I-15, I-26 and one cross-department line now refer to dept + title + roster row. | Issues; md |

No budget value was changed; every new figure is a reading of existing cells, the HC tabs or the SD models. v5's own changes from v4 are listed in `02-build_notes_v5.md` and still apply.

## Payroll reconciliation

Sources: the HC tabs of `COO_HC_and_PL_workfile.xlsx` (now HC-FO ... HC-COO in the workbook; one row per person, 2027 = columns M:X), the P&L payroll lines of the v6 workbook (= v5), the COO book _2, and the SD payroll models (Fld Ops Payroll, Fld Eng Budget and Prod Payroll in the workbook; Logistics&WH Payroll in the SD book, not carried). People are identified by roster + row + title; names were used only inside recon_v6.py to match people. 'Current' = on payroll before 2027 and on an HC roster; 'ramp' = hires the SD models add. All amounts are 2027 (Jan-Dec), salary + payroll tax + benefits unless stated.

### Summary by department

| Dept | GL | HC roster: people, 2027 total | v6 P&L line (= v5) | COO book _2 | SD model 2027 | Current staff in the SD model | Ramp in the SD model | Overlaps found | Net increment not in the budget |
|---|---|---|---|---|---|---|---|---|---|
| FO | 5510-5540 | 16; 1,341,298 | 3,957,239 | 1,341,298 | Fld Ops Payroll 3,957,239 | 16 = FO HC 16; 1,338,696 | 2,618,543 | FO HC r15 also on Fld Eng Budget r15 (I-28) | 0 (the SD model is the budget) |
| PO | 5110-5140 | 9; 652,820 | 652,820 | 652,820 | Prod Payroll 2,592,894; Logistics&WH 547,441 | Prod Payroll 9 (count) 630,504; Logistics&WH 2 seats 210,912 | Prod Payroll 1,962,389; Logistics&WH 336,530 | 9 of 9 in Prod Payroll (count); r20 = Logistics&WH MH-01 (name); r16 backfilled by MH-02 | 2,298,919 (I-05 1,962,389, I-17 336,530) |
| CO | 6610-6640 | 5; 618,961 | 618,961 | 618,961 | none (r17 is Logistics&WH LOG-01) | - | - | r17 = Logistics&WH LOG-01 (name) | 0 |
| FE | 6610-6640 | 7 + 1 open row; 908,980 | 1,133,298 | 752,002 | Fld Eng Budget 1,133,298 | 7 of 7 matched (6 name, 1 title + salary) | Aug-27 hire 33,967 (I-36) | Fld Eng Budget r15 = FO HC r15 (I-28) | 0 (the SD model is the budget) |
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

Reconciliation with the COO book's old FO (5510 1,088,252 = FO HC salary; 5510-5540 1,341,298 = FO HC total): the SD current-staff block has salary 1,086,604 ((1,648)) and total 1,338,696 ((2,602)). The coordinator and manager match to the dollar (77,088.86 and 120,900.00). The techs differ only because the model uses 14 x 63,000 = 882,000 where FO HC has 883,636 (2027 with the Oct-27 raise: 888,615 vs 890,263), and the burden rates differ slightly (SD 6.8% / 16.4%, FO HC 6.847% / 16.405%). So the old FO was the current 16 only; the SD build = the same 16 + 2,618,543 of ramp hires. One of the 14 techs (FO HC r15) is also costed on Fld Eng Budget r15 (I-28).

### PO: PO HC vs Prod Payroll and Logistics&WH Payroll (I-05, I-17)

PO 5110-5140 (652,820) is exactly PO HC: 9 current staff (2 Team Lead, 1 Material Handling Team Lead, 2 Senior Production Technician, 1 Production Technician, 1 Material Handler, 2 Production Associate); headcount every 2027 month 9 (min) to 9 (max), no hires, raise from Oct-27 like every roster.

**How many of the 9 appear in the SD models?** Prod Payroll: **9 of 9 by headcount** (its 'current staff on payroll (Sep-26)' is 7 lift + 2 tray = 9, 0 supervisors; the model has no names or titles, so this is a count match, not a person match). Logistics&WH: **1 of 9 by name** (PO HC r20 Material Handler = seat MH-01); PO HC r16 Material Handling Team Lead is named as the person seat MH-02 backfills (from Oct-26), but r16 stays on PO HC through Dec-27. The Logistics&WH model also holds CO HC r17 Field Logistics Manager (seat LOG-01, by name). If the 9 are Prod Payroll's current staff, PO HC r20 sits in both SD models; the net increments below take each person out once.

|  | PO HC / PO 5110-5140 | Prod Payroll (SD) | Logistics&WH Payroll (SD, not carried) | Both models |
|---|---:|---:|---:|---:|
| Model 2027 total | - | 2,592,894 (lift 1,622,423, tray 729,177, supervisors 241,294) | 547,441 | 3,140,335 |
| People already on an HC roster | 9 (652,820) | 9 current staff (count): model cost 630,504 | 2 seats: MH-01 (PO HC r20) 61,963, LOG-01 (CO HC r17) 148,949 | 841,416 |
| **Net increment (ramp) not in the budget** | 0 | **1,962,389** (I-05) | **336,530** (I-17): 7 seats | **2,298,919** |
| Ramp headcount Jan-27 -> Dec-27 | 0 -> 0 | 15 -> 45 | 2 -> 7 | 17 -> 52 |
| Gross gap vs PO 5100 (model total - 652,820) | - | 1,940,074 | n/a (different team) | - |

Net increment = model total less the model's own cost of the people already on HC rosters (A-27), so it is the cost of the ramp hires at the model's rates. The model costs the 9 current staff at 630,504, 22,315 below PO 5100 (652,820): average salary 57,200.05 vs 57,933.33, and different burden (model tax 7.5%, benefits 7.5% lift / 8.0% tray, plus the monthly absence coverage of Prod Payroll rows 33/54; PO HC 3.64% / 20.64%). That difference is not part of the net increment. Ramp cost by component: salary 1,591,611, absence coverage 85,268, payroll tax 125,766, benefits 121,745, new-hire cost 38,000. The model already has 9 lift, 4 tray and 2 supervisor hires in Sep-Dec 26, so 2027 opens with 15 ramp staff.

**Net ramp by month (2027)**

| Row | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | 2027 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Prod Payroll ramp headcount | 15 | 21 | 21 | 21 | 21 | 21 | 25 | 25 | 31 | 34 | 42 | 45 |  |
| Prod Payroll ramp cost | 89,063 | 129,562 | 123,562 | 123,562 | 124,535 | 125,509 | 159,345 | 150,217 | 188,461 | 206,382 | 264,783 | 277,410 | 1,962,389 |
| Logistics&WH new seats (headcount) | 2 | 3 | 4 | 4 | 4 | 5 | 7 | 7 | 7 | 7 | 7 | 7 |  |
| Logistics&WH new seats cost | 10,464 | 16,392 | 21,517 | 20,517 | 20,517 | 26,642 | 38,106 | 36,106 | 36,106 | 36,721 | 36,721 | 36,721 | 336,530 |
| **Net ramp headcount, both** | 17 | 24 | 25 | 25 | 25 | 26 | 32 | 32 | 38 | 41 | 49 | 52 |  |
| **Net ramp cost, both** | 99,527 | 145,953 | 145,078 | 144,078 | 145,052 | 152,151 | 197,450 | 186,323 | 224,567 | 243,103 | 301,504 | 314,131 | **2,298,919** |
| Prod Payroll total headcount (incl. the 9) | 24 | 30 | 30 | 30 | 30 | 30 | 34 | 34 | 40 | 43 | 51 | 54 |  |
|   of which lift / tray / supervisors (Dec-27) | 35 / 15 / 4 |  |  |  |  |  |  |  |  |  |  |  |  |

**Logistics&WH seats**

| Seat | Team | Start | Annual base | 2027 cost (model rates) | On an HC roster? | In net increment |
|---|---|---|---:|---:|---|---|
| LOG-01 Logistics Manager | Central Operations | on payroll | 120,000 | 148,949 | CO HC r17 Field Logistics Manager (name) | no |
| INV-01 Inventory Control Specialist | Inventory control | Feb-27 | 48,000 | 55,652 | no | yes |
| TL-01 Material Handling Team Lead | Receiving & putaway | Dec-26 | 52,000 | 64,544 | title only: PO HC r16 Material Handling Team Lead (salary 57,554, start Sep-26) | yes |
| TL-02 Material Handling Team Lead | Kitting & line replenishment | Jul-27 | 52,000 | 33,032 | title only: PO HC r16 Material Handling Team Lead (salary 57,554, start Sep-26) | yes |
| MH-01 Material Handler | Receiving & putaway | on payroll | 49,920 | 61,963 | PO HC r20 Material Handler (name) | no |
| MH-02 Material Handler | Receiving & putaway | Oct-26 | 49,920 | 61,963 | backfills PO HC r16 Material Handling Team Lead; title only: PO HC r20 Material Handler (salary 49,920, start Sep-26; already matched by name to another seat) | yes |
| MH-06 Material Handler | Receiving & putaway | Jul-27 | 49,920 | 31,751 | title only: PO HC r20 Material Handler (salary 49,920, start Sep-26; already matched by name to another seat) | yes |
| MH-03 Material Handler | Kitting & line replenishment | Mar-27 | 49,920 | 52,712 | title only: PO HC r20 Material Handler (salary 49,920, start Sep-26; already matched by name to another seat) | yes |
| MH-04 Material Handler | Kitting & line replenishment | Jun-27 | 49,920 | 36,876 | title only: PO HC r20 Material Handler (salary 49,920, start Sep-26; already matched by name to another seat) | yes |

Seats the model's own check block excludes: LOG-02 (Logistics&WH Payroll!A55; = FO HC r21 Operations Coordinator, budgeted in FO) and MH-05 (A56; in no model, I-27). Model rates: tax 6.8%, benefits 16.4%; Python replica of the seat costs vs the SD cached values: max difference 3.3e-06.

### CO

CO 6610-6640 (618,961) = CO HC: 5 people (4 current, 1 new hire), CO HC rates 5.22% / 11.91%. No SD model; CO HC r17 Field Logistics Manager is also seat LOG-01 of the not-carried Logistics&WH model (excluded from the I-17 net). Net increment 0.

### FE: FE HC vs Fld Eng Budget (FE 6610-6640)

| Fld Eng Budget row | Salary | Start (SD) | FE HC row | Match | Start (HC) | 2027 salary SD | 2027 salary HC | Difference |
|---|---:|---|---|---|---|---:|---:|---:|
| r13 Field Engineer | 98,591 | Jan-27 | r14 Senior Field Robotics Engineer | name | Sep-26 | 99,330.43 | 99,330.43 | 0.00 |
| r14 Field Engineer | 72,080 | Jan-27 | r15 Associate Field Robotics Engineer | name | Sep-26 | 72,620.60 | 72,620.60 | 0.00 |
| r15 Field Engineer | 75,000 | Jan-27 | - | not on FE HC; same name as FO HC r15 Field Technician | - | 75,562.50 | - | 75,562.50 |
| r16 Field Engineer | 70,000 | Jan-27 | r19 Associate Field Robotics Engineer | name | Sep-26 | 70,525.00 | 70,525.00 | 0.00 |
| r17 Customer Support Manager | 160,000 | Jan-27 | r17 Customer Support Manager | name | Sep-26 | 161,200.00 | 161,200.00 | 0.00 |
| r18 Customer Support Specialist | 65,000 | Jan-27 | r18 Customer Support Specialist | name | Sep-26 | 65,487.50 | 65,487.50 | 0.00 |
| r19 Customer Support Specialist | 65,000 | Aug-27 | - | not on FE HC | - | 27,570.83 | - | 27,570.83 |
| r20 Field Engineering Manager | 140,000 | Jan-27 | r35 Field Engineer Manager | title + salary | Dec-26 | 141,050.00 | 141,050.00 | 0.00 |
| r21 Head of Service Delivery | 205,000 | Jan-27 | r16 Head of Service Delivery | name | Sep-26 | 206,537.50 | 206,537.50 | 0.00 |
| Total |  |  |  |  |  | 919,884.37 | 816,751.03 | 103,133.33 |

FE HC r41 'Field Engineer' (new-hire block) has no name, salary or start (0 in FE HC); it may be the seat for Fld Eng Budget r15. Start months: FE HC has every current person in seat from Sep-26 (Field Engineer Manager from Dec-26) and Fld Eng Budget starts everyone in Jan-27; for the matched people the 2027 monthly salary is identical (max difference 0.00), so the start months have no 2027 effect. COO book FE 6610 675,701 = FE HC 816,751 less FE HC r35 Field Engineer Manager (141,050).

**Burden rates (I-34)**

| FE 2027 | Salary base | 6630 payroll tax | 6640 benefits | Total burden |
|---|---:|---:|---:|---:|
| Budget: SD rates 6.8% / 16.4% | 919,884 | 62,552 | 150,861 | 213,413 |
| At FE HC rates 4.069% / 7.223% | 919,884 | 37,432 | 66,442 | 103,874 |
| **Difference (budget higher)** |  | +25,120 | +84,419 | **+109,539** |

On the matched people only (816,751 of salary) the difference is +97,258. FE HC's own burden on its 816,751 is 33,235 + 58,993.

### PE

PE 6610-6640 (1,211,637) = PE HC: 9 people, PE HC rates 3.57% / 8.82%. No SD model. PE HC r22 Head of Production and Delivery is marked 'transfer?' in column A: 2027 cost 254,785 (salary 226,688, tax 8,096, benefits 20,001), on no other roster (I-35).

### Duplicate scan across all rosters (I-28)

Rosters compared: FE HC, CO HC, PE HC, PO HC, FO HC, SD Fld Eng Budget, SD Fld Ops Payroll (named rows), SD Logistics&WH (seats), SD Prod Payroll (anonymous counts). Rule (A-29): name where present, otherwise title + salary + start; one-to-one. Names are not shown.

| Person A | Person B | Match basis | Classification |
|---|---|---|---|
| FO HC r15 Field Technician | Fld Eng Budget r15 Field Engineer | name | DUPLICATE across P&L sources: FO 5510-5540 (Fld Ops Payroll current techs, by count) and FE 6610-6640 (Fld Eng Budget) |
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
| FE HC r35 Field Engineer Manager | Fld Eng Budget r20 Field Engineering Manager | title + salary (start Dec-26 vs Jan-27) | same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately) |

Head of Service Delivery: FE HC r16 and Fld Eng Budget r21 only; CO HC / PE HC name matches 0, title matches 0; nearest title: PE HC r22 Head of Production and Delivery (different name and salary). No person appears on two HC tabs. Anonymous rows: Fld Ops Payroll's 14 current techs = the 14 FO HC field technicians (count); Prod Payroll's 9 current staff = PO HC 9 (count).

### Roster-to-P&L map

`02-build/02-build_roster_map_v6.csv` (no names): 47 roster rows (FO 16, PO 9, CO 5, FE 8, PE 9); each is mapped to exactly one P&L source (unmapped: 0). The FE HC r41 open row maps to no cost. 13 rows carry a flag in 'also_in' (model overlaps, the FO/FE duplicate, the PE 'transfer?' row, the open FE row).

## HC tabs added to the workbook

| Tab | From (workfile) | Cells | Formulas | Part |
|---|---|---|---|---|
| HC-FO | FO HC | 1,604 | 873 | xl/worksheets/sheet14.xml |
| HC-PO | PO HC | 1,610 | 873 | xl/worksheets/sheet15.xml |
| HC-CO | CO HC | 1,604 | 873 | xl/worksheets/sheet16.xml |
| HC-FE | FE HC | 1,604 | 873 | xl/worksheets/sheet17.xml |
| HC-PE | PE HC | 1,605 | 873 | xl/worksheets/sheet18.xml |
| HC-COO | COO HC | 1,050 | 829 | xl/worksheets/sheet19.xml |

Placed after Fld Eng Budget, in the order of the handoff. Copied cell by cell at the XML level with values, formulas (shared formulas kept), cached values, styles, column widths, row heights, frozen panes, data validations and cell notes. Sheet references re-pointed ('PO HC'! -> 'HC-PO'!, ...); HC-COO reads only the other five HC tabs. Shared strings were inlined (sharedStrings.xml untouched). Styles: 92 cell formats, 24 fonts, 8 fills, 5 borders and 4 number formats appended to styles.xml (existing entries unchanged, so no existing cell changes format); 7 theme colours resolved to RGB because the workfile theme (Aptos) differs from v5's. The hidden 'Claude Log' tab and the workfile P&L tabs were not copied (_2 stays the P&L source).

External links stored as values (A-30): each dept HC tab reads its payroll tax and benefits rates (D6:D7) from an external T&B workbook ([1], not supplied). The 10 cells keep the workfile's cached values:

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

Checks: LibreOffice recalculation of v6, HC tabs: errors 0, cached vs recalculated max difference 4.9e-09 over 3,432 cells, text mismatches 0; formulas referencing a sheet outside the HC tabs 0; external references 0.

## Head of Service Delivery salary (I-26, resolved in v5)

- Input: Fld Eng Budget!B21 = 205,000 (annual salary, user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). This is the only typed input that changed; no formula, label or other cell was edited.
- How the model treats it: row 67 uses the same formula as the other roster rows (=IF(B$58>=$C$21,$B$21/12*(1+IF(B$58>=$B$25,$B$24,0)),0)). Start month C21 = 2027-01-01, so all 12 months of 2027 are paid: 17,083.33/month Jan-Sep, then +3% (Fld Eng Budget!B24 = Fld Ops Payroll M5 = Prod Payroll M5) from 2027-10-01 (B25 = Fld Ops Payroll M6 = Prod Payroll M6) = 17,595.83/month for 3 months. No raise-eligibility test applies on this tab (I-29); the salary is treated as the Dec-26 rate.
- Burden: payroll taxes 6.8% (B22 = Fld Ops Payroll B7) and benefits 16.4% (B23 = Fld Ops Payroll B8), applied to the salary rows total (rows 69-70).
- 2027 cost of the role: salary 206,538 + payroll tax 14,045 + benefits 33,872 = 254,454.
- FE 2027 (AG): 6610 713,347 -> 919,884 (+206,538); 6630 48,508 -> 62,552 (+14,045); 6640 116,989 -> 150,861 (+33,872). FE Total - Expense 931,334 -> 1,185,788. COO P&L rows 67-69 move by the same amounts.
- 2027 COO contribution (COO P&L AG132): 393,486 (v4) -> 139,032 (v5), (254,454). 2026 FE 6610 was 850,615; FE 6610 2027 is now 919,884 (8% vs 2026; v4 -16%).
- v6: the HC rosters confirm the person is on FE HC r16 (205,000, in seat from Sep-26) and nowhere else; Fld Eng Budget starts the row in Jan-27, which gives the same 2027 cost.

## Build and sources

Output: `02-build/02-build_COO_2027_Budget_Collated_v6.xlsx` (v1-v5 files unchanged) and `02-build/02-build_roster_map_v6.csv`.  
Scripts: `02-build/scripts/` - v6 entry point `run_build_v6.sh`: prodpay_v6.py (scratch copy with the Prod Payroll XLOOKUP row replaced, analysis only) -> recalc.sh -> recon_v6.py (reconciliation, roster map CSV) -> cnotes_v6.py (extracts the v5 Collation Notes, byte-exact round trip) -> build_v6.py (stage 1: v5 + HC tabs) -> report_v6.py pass 1 (Collation Notes JSON) -> build_v6.py (final) -> diff_versions.py, recalc.sh, analyze_v6.py, recon_v6.py on v6 (figures must be identical) -> report_v6.py pass 2 (JSON must equal pass 1) -> privacy_v6.py. Every v5 part other than workbook.xml, its rels, [Content_Types].xml, styles.xml (append only) and Collation Notes is copied byte for byte. `run_build_v5.sh` ... `run_build.sh` still reproduce v5 ... v1.  
Inputs (read-only): `COO_HC_and_PL_workfile.xlsx` sha256 `01eca67dc1ce297717ede0880974540b7be4ad6003f3db27ad5f2769daac9cc3` (new); `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `a3264ef4305e1e7da7c8cf7efbcd5407556aba56e85d50375f9ece711199e9b4`; `Service_Delivery_PL_worksheets.xlsx` sha256 `fedee8d16eb7db72d2745e77a7c6441057b4229131c52d25c944dbb5b858a466`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `645e31303dcbbbd6279152aeaa8e5e61dffa0984f1f6116d671408011166fceb`.  
Recalculation engine: LibreOffice 24.2.7.2 420(Build:2).  
Base: v5 workbook sha256 `fb14a92ed329a42632dd5297b6426565810e10e48b7275b7cd709c7ac9a3b6dd` (under verification in parallel when v6 was built).

## Completion criteria (v6)

| Criterion | Result |
|---|---|
| 0 value diffs on the existing sheets vs v5 | diff_versions.py on 12 sheets (27,701 cells): formula diffs 0, value diffs 0; comments added / removed / changed 0 / 0 / 0. Collation Notes regenerated (excluded). |
| Existing parts untouched | 33 of 38 v5 parts byte-identical; changed: xl/_rels/workbook.xml.rels, xl/workbook.xml, [Content_Types].xml, xl/worksheets/sheet1.xml, xl/styles.xml; styles.xml append-only: True. |
| HC tabs present with 0 errors | HC-FO, HC-PO, HC-CO, HC-FE, HC-PE, HC-COO after Fld Eng Budget: True; errors after recalculation 0; cached vs recalculated max difference 4.9e-09; external references 0; references outside the HC tabs 0. |
| HC tabs tie to the P&L | HC-PO / HC-CO / HC-PE rows 67-69 vs PO / CO / PE payroll rows, every 2027 month: max difference 3.64e-11. |
| Every roster person mapped to one P&L source, or flagged | 47 rows mapped, unmapped 0; flagged 13. |
| No new errors on existing sheets | New errors vs v5: 0. |
| Cached values are what the formulas give | LibreOffice recalculation of v6 vs stored values, existing sheets except Collation Notes: 40 cells differ, max 9.9e-08; non-numeric mismatches 0. |
| Collation Notes live formulas | 32 formulas; recalc vs stored max diff 3.9e-08, text mismatches 0. |
| Figures recompute from the final file | recon_v6.py with the v6 workbook in place of v5: identical output True. |
| No employee names in md, Collation Notes, CSV, message | privacy_v6.py on the pass-1 notes, the Collation Notes JSON and sheet, and the CSV: 46 full names, 89 tokens checked in 4 files; hits 0. It runs again on this file before it is copied; the build stops on any hit. The return message is checked the same way. |

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
| A-27 | Net increment of an SD payroll model = model 2027 total less the model's own cost of the people already on an HC roster (same model rates) | I-05 1,962,389; I-17 336,530 | Prod Payroll; SD Logistics&WH Payroll | builder definition (v6, handoff: 'model total minus the overlap already in PO') |
| A-28 | Prod Payroll tray and supervisor rows evaluated by replacing XLOOKUP (match_mode 1) with an equivalent SMALL/COUNTIF formula in a scratch copy only | model 2027 2,592,894; Python replica agrees to 5e-10 | Prod Payroll!B48:Q48 (workbook unchanged) | builder method (v6) |
| A-29 | Person match: name where present (all tokens of the shorter name in the longer, same first token); otherwise title + salary + start; one-to-one | 12 pairs; anonymous model rows (Prod Payroll current staff, Fld Ops Payroll current techs) matched by headcount only | recon_v6.py | handoff rule |
| A-30 | HC tab tax/benefit rates (D6:D7) linked to an external T&B workbook are kept as the workfile's cached values | 10 cells | 'HC-*'!D6:D7 | builder (as DeploySum in v3) |


A-22..A-25 are new in v4; A-26 is new in v5; A-27..A-30 are new in v6; A-14, A-17, A-18 and A-19 were edited in v4 (critic O1, O3, O4); A-17 also shows the N3 trend case in v5.

## DeploySum refresh and tie-out (v3 build; unchanged in v4-v6)

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

## v5 -> v6 diff

`diff_versions.py` (exact: formulas as text, cached values with no tolerance) on every sheet present in both files except Collation Notes:

| Sheet | Cells | Formula diffs | Value diffs |
|---|---:|---:|---:|
| COO P&L | 3,530 | 0 | 0 |
| FO | 3,581 | 0 | 0 |
| PO | 3,631 | 0 | 0 |
| CO | 3,582 | 0 | 0 |
| FE | 3,582 | 0 | 0 |
| PE | 3,590 | 0 | 0 |
| DeploySum | 901 | 0 | 0 |
| Depreciation Schedule | 1,214 | 0 | 0 |
| Fld Ops Payroll | 1,165 | 0 | 0 |
| Prod Payroll | 1,173 | 0 | 0 |
| Fld Maint Budget | 1,012 | 0 | 0 |
| Fld Eng Budget | 740 | 0 | 0 |
| **Total** | 27,701 | 0 | 0 |

Sheets only in v6: HC-FO, HC-PO, HC-CO, HC-FE, HC-PE, HC-COO. Sheets only in v5: none. Package: 33 of 38 v5 parts byte-identical; changed: xl/_rels/workbook.xml.rels, xl/workbook.xml, [Content_Types].xml, xl/worksheets/sheet1.xml, xl/styles.xml; added: 24 parts (6 worksheets, their rels, 6 comment parts, 6 VML drawings).

## Error scan

| Sheet | v5 | v6 |
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
| HC-FO | n/a (new) | none |
| HC-PO | n/a (new) | none |
| HC-CO | n/a (new) | none |
| HC-FE | n/a (new) | none |
| HC-PE | n/a (new) | none |
| HC-COO | n/a (new) | none |

New errors in v6: **0**. Prod Payroll's #NAME? cells are the XLOOKUP rows LibreOffice cannot evaluate (I-05, I-25; evaluated for the analysis per A-28).

## Package

Parts 62 (v5 38); `xl/externalLinks/*` **0**; defined names 8,965 (v5: 8,965).

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

## Issues (v6)

Severity per the scale above. Open: 4 HIGH, 11 MED, 20 LOW; 1 RESOLVED. v6: I-05 rewritten with the net increment and raised to HIGH; I-17 and I-28 rewritten from the HC rosters; I-34, I-35 and I-36 new; I-15 and I-26 refer to people by dept + title + roster row. No other severity changed.

| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |
|---|---|---|---|---|---|---|---|
| I-01 | MED | PO!U12:AF12; PO!R12; PO!U13:AF13; PO!U15:AF15; DeploySum!F40:Q40 | Resolved by assumption in v3. 2027 revenue is now budgeted: PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27; row 39 in the 9/30/26 file), all to 4100 Subscription/Platform Fees (orchestrator assumption). PO!R12 set to 'Manual'. Still open: 4500 Implementation Fees and 4900 One-Time Revenue stay 0 in 2027, and the source does not say whether recognized revenue includes them. | PO!AG12 = 15,563,645.54; DeploySum FY27 recognized revenue (9/30/26 file R39) = 15,563,645.54; difference (0.00). 2026: 4500 85,861, 4900 975,000. Cross-check Sep-Dec 26: DeploySum recognized revenue 2,527,326 vs PO 4100 forecast (PO!J12:M12) 2,486,929 (difference 40,396), so the 4100 mapping is consistent with how PO forecasts 2026. | not determinable (2026 4500+4900 = 1,060,861) | impact not determinable; owner confirmation needed | Finance/PO owner to confirm the 4100 mapping and whether 2027 implementation or one-time revenue should be budgeted on 4500/4900. |
| I-02 | HIGH | FO!AG63; FO!AG116; FE!AG63; FE!AG116; COO P&L!AG132 | Replacing FO and FE with the SD versions adds 6,828,802 to 2027 COO cost (COGS + Opex). The SD build is much heavier than the COO book's FO/FE. (v4: restated in cost terms; the earlier evidence quoted 2027 Net Income from before revenue was budgeted.) | FO cost (AG63 + AG116): COO book 1,341,298 -> SD 7,347,500; FE: COO book 752,002 -> SD 1,574,602; together 2,093,300 -> 8,922,101. With the COO book's FO/FE, the 2027 COO contribution would be 6,967,834 instead of 139,032. Drivers: FO!N52 876,692 -> AG52 3,238,031; FO!N47 255,704 -> AG47 1,519,865; FO!N29 57,182 -> AG29 765,000. | (6,828,802) on the contribution | impact (6,828,802) | COO and SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off. |
| I-03 | LOW | DeploySum!A3:R49 (Collation Notes lists the formulas) | Resolved in v3. DeploySum rows 3-49 now hold the resolved values from 2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx. The 410 cells that link to the external workbook '[1]' are stored as that file's cached values; their formula text is on Collation Notes. The links are still not live (the [1] workbook was not supplied), so the next plan update needs a new resolved export. | DeploySum errors: v2 {'#REF!': 463, '#N/A': 35}, v3 none (498 resolved). Every mapped cell B:R equals the 9/30/26 cached value (mismatches: 0). New-file sha256 645e31303dcbbbd6... | 0 | hygiene | Refresh DeploySum from a new resolved export when the plan changes. Keep the row map (ARR row 39 kept). |
| I-04 | LOW | DeploySum!B53:R66; DeploySum!A69:R76 (v3 check block) | The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (rows 53-66) are still typed values. v3 adds a live check: they now tie to the resolved rows 16-21 in every month Sep-26..FY27. So the FO/FE drivers are consistent with the 9/30/26 plan; they are just not linked. | 16+17 vs 54+57+60: FY 67 vs 67, max monthly diff 0; 18 vs 64: FY 67 vs 67, max monthly diff 0; 19 vs 55+58+61: FY 250 vs 250, max monthly diff 0; 20 vs 56+59+62: FY 1,036 vs 1,036, max monthly diff 0; 21 vs 63: FY 0 vs 0, max monthly diff 0. DeploySum!A76 = 'Tie-out rows 16-21 vs 54-64: OK'. | 0 | hygiene | Optional: replace rows 54-64 with formulas (or document the source) so they update with the plan. |
| I-05 | HIGH | Prod Payroll!B24:S81 (hidden); Prod Payroll!S41, S62, S79, S81; PO!AG33:AG36; 'HC-PO'!B14:Z22, Z67:Z70 | PO 5110-5140 (652,820) is the 9 current staff on PO HC, flat all year with no hires ('HC-PO' rows 14-22; PO!U33:AF35 equal 'HC-PO'!M67:X69). The production payroll model holds the same 9 as its current staff (7 lift + 2 tray on payroll Sep-26; the model has no names or titles, so the match is by headcount) and adds the hires the build plan needs. v6 evaluates the whole model, tray and supervisor rows included (A-28): 2,592,894 for 2027 (lift 1,622,423, tray 729,177, supervisors 241,294). Of that, 630,504 is the model's cost of the 9 current staff, already in PO. Net increment that PO lacks: 1,962,389 (ramp hires only). It is larger than the v5 gap (969,603) because v5 compared lift payroll only. The model also hires 9 lift, 4 tray and 2 supervisor staff in Sep-Dec 26, which PO HC does not show either. | Ramp headcount Jan..Dec 27: 15, 21, 21, 21, 21, 21, 25, 25, 31, 34, 42, 45 (plus the 9 current staff). Hires in 2027: lift 19, tray 9, supervisors 2. Ramp cost: salary 1,591,611, absence coverage 85,268, payroll tax 125,766, benefits 121,745, new-hire cost 38,000. Model cost of the 9 vs PO 5100: 630,504 vs 652,820 ((22,315): model average salary 57,200.05 vs PO HC 57,933.33; model tax 7.5%, benefits 7.5% / 8.0% plus absence coverage vs PO HC 3.64% / 20.64%). Python replica of the model vs LibreOffice: max difference 4.9e-10. | (1,962,389) on the contribution if the model is right (net of the 9 already in PO) | impact 1,962,389 (> $250k; on its own turns the contribution negative) | PO owner / user: is PO 2027 payroll the 9 current staff only (as budgeted) or the build-plan staffing in Prod Payroll? If the model is right, add the ramp (net increment), not the model total, to PO 5110-5140. Severity raised from MED (v5) because the net amount is now quantified. |
| I-06 | LOW | Fld Maint Budget!B30 (comment); Fld Ops Payroll!B11; FO!AG44; FO!AG52 | MeLi contractor double count: quantified at $0 in the current cells. The CONFIRM comment on Fld Maint Budget!B30 says Fld Ops Payroll includes MeLi in '21 all-in techs', but Fld Ops Payroll!B11 = 14 ('Current site techs on payroll (Sep-26) - Domestic Only') and Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11 = 21. So MeLi techs are costed in 5310 only. The comment describes an earlier state and is stale (Fld Maint Budget!A143 records the correction). | FO 5310 (FO!AG44 = 575,268) = MeLi techs in role 346,920 + Merida contractors 123,900 + MeLi supervisor 104,448 (Fld Maint Budget rows 70-72 x B10/B11; row 84 = 575,268). FO 5510 current techs: Fld Ops Payroll!F20:Q20 = 14 each month (formula =$B$11); current-tech payroll 2027 1,094,774. | 0 | impact 0 | SD owner to confirm and delete the stale CONFIRM comment on Fld Maint Budget!B30. |
| I-07 | MED | PO!U19:AF22; 'Depreciation Schedule'!A1:S126; COO P&L!AG19:AG22 | Resolved by assumption in v3. 2027 depreciation is now budgeted from the new 'Depreciation Schedule' tab: straight-line, SlipLift 84 months, SlipTray 120 months, no salvage, full month from the go-live month. Existing fleet = PO Dec-26 run rate, carried flat (builder assumption, A-17). New units = DeploySum 2027 go-lives (rows 19/20). PO!R19:R22 set to 'Manual'. The open parts are logged separately: I-31 (Q4-26 go-lives), I-32 (existing-fleet run rates, SlipBot) and I-33 (peripherals). | 2027 depreciation 3,318,808 (2026 1,788,097): existing fleet 1,911,249, new 2027 go-lives 1,407,560. By GL: 5010 SlipBot 1,353,574; 5011 SlipLift 1,248,196; 5012 SlipCarrier (SlipTray) 418,898; 5020 Robot Peripherals 298,140. Python recompute from raw inputs vs workbook, all 48 GL-months: max diff 3.78e-10. | not determinable (component decisions in I-31..I-33) | impact not determinable; owner confirmation needed | PO owner/Finance to confirm the run-rate approach against the fixed-asset register, and resolve I-31..I-33. |
| I-08 | LOW | PO!U28; PO!Y28; PO!AD28; PO!U38; PO!U42 | Typed plugs are added onto the driver formula in 2027 month cells (+15,000, +5,000). They are not visible in the method columns R:T. | PO!U28 +5,000; PO!Y28 +5,000; PO!AD28 +5,000; PO!U38 +15,000; PO!U42 +15,000. Total plugs 45,000. | 45,000 | impact 45,000 | PO owner to move these amounts into a documented input (column S or a manual row), or remove them. |
| I-09 | LOW | PE!W74:AF74; PE!W76 | Typed numbers overwrite the driver formula in some 2027 months (manual overrides inside a formula row). | PE!W74=1,500, PE!X74=1,500, PE!Y74=2,000, PE!Z74=2,000, PE!AA74=2,500, PE!AB74=2,500, PE!AC74=3,000, PE!AD74=3,000, PE!AE74=3,500, PE!AF74=4,000, PE!W76=300. Total typed 25,800. | 25,800 | impact 25,800 | PE owner to confirm the overrides, or set the row method to Manual. |
| I-10 | MED | FO!AG58; FO!AG67; FO!AG91; FE!AG91; FO!AG116 | FO/FE lines with material 2026 spend have 2027 = 0, and FO Total Expense (SG&A) is 0 for 2027. Fld Maint Budget!A99 says: 'Not budgeted here: 6100 Travel and 7550 Tools ($0 by design – field travel books to 5050/5360, field tools to 5330); new-hire onboarding (covered by the $2K new-hire cost in Fld Ops Payroll B9). Out of scope: 5920, 7200, 8600.' | FO!AG58 5920 - Software - COGS: 2026 119,260 -> 2027 0; FO!AG67 6610 - Salaries and Wages - SG&A: 2026 50,575 -> 2027 0; FO!AG91 7200 - Contractors: 2026 59,734 -> 2027 0; FE!AG91 7200 - Contractors: 2026 154,857 -> 2027 0; FO!N116 217,242 -> AG116 0. 2026 total of these lines 384,425. | not determinable (2026 base 384,425) | impact not determinable; owner confirmation needed | SD owner to confirm whether these costs stop in 2027 or are budgeted elsewhere. |
| I-11 | MED | COO P&L!AG12; COO P&L!AG52; COO P&L!AG19; COO P&L!AG47 (+ variance table) | 98 rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k (v3 values; list below). | v3 values: 98 rows (v2: 98). Largest COO P&L GL moves: COO P&L!N12 6,363,078 -> AG12 15,563,646; COO P&L!N52 887,966 -> AG52 3,238,031; COO P&L!N47 319,694 -> AG47 1,554,365; COO P&L!N20 100,360 -> AG20 1,248,196. | not determinable | impact not determinable; owner confirmation needed | Each dept owner to comment on their rows in the variance table. |
| I-12 | MED | Fld Maint Budget!B8; Fld Maint Budget!B78:M78; FO!AG46 | Site setup kit cost is flagged as a placeholder (Fld Maint Budget!D8: 'PLACEHOLDER – update when the kit list is priced (Spare Parts, Tool Kits, 5S for'). It feeds FO 5330. | Fld Maint Budget!B8 = 4,500 $/new site; 'Site setup kits' 2027 (B78:M78) = 274,500. FO!N46 23,121 -> AG46 288,069. | not determinable (exposure 274,500) | impact not determinable; owner confirmation needed | SD owner to price the kit list and replace B8. |
| I-13 | MED | Fld Ops Payroll!M11; Fld Ops Payroll!B12; Fld Ops Payroll!M14 | Two Fld Ops Payroll drivers are marked 'Placeholder' in the author's notes: site techs per floater (M11) and the share of expansion go-lives needing a tech (B12). M11 currently has no effect because the floater switch M14 = 'No' (floater payroll 2027 = 0). B12 drives expansion-tech payroll. | M11 = 40, B12 = 0.6, M14 = 'No'. Expansion tech payroll 2027 (Fld Ops Payroll!F47:Q47) = 337,514. | not determinable (exposure 337,514) | impact not determinable; owner confirmation needed | SD owner to confirm or replace B12; M11 matters only if M14 is set to Yes. |
| I-14 | MED | Prod Payroll!M7; Prod Payroll!B9; Prod Payroll!A33; Fld Ops Payroll!B9; Old Draft!B142 (SD, not carried) | More placeholder inputs: Prod Payroll new-hire cost, current headcount and absence factors (no budget effect while Prod Payroll is broken), and the Fld Ops Payroll new-hire cost per tech, which hidden Old Draft!B142 says overlaps an onboarding line. | Fld Ops Payroll!B9 = 2,000; new-hire cost in FO 2027 (Fld Ops Payroll rows 34, 46, 59, 72, F:Q) = 138,000. Old Draft!B142: '7. Onboarding: 10 new hires Jan – Sep. The $2,000 Fld Ops Payroll placeholder (B9) overlaps this line; replace it with the actual cost here '. | not determinable (exposure 138,000) | impact not determinable; owner confirmation needed | SD owner to confirm B9 (and that onboarding is not also budgeted elsewhere). |
| I-15 | LOW | Fld Maint Budget!B12 (comment); Fld Maint Budget!B11; Fld Ops Payroll!H11; Fld Ops Payroll!E12 | The CONFIRM comment on Fld Maint Budget!B12 says Fld Ops Payroll shows 0 current supervisors; it now shows H11 = 1 ('Current supervisors counted toward ratio (Sep-26) – [name; FO HC r25 Field Maintenance Manager]'), and E12 says 'Ratio = domestic techs only. MeLi contract supervisor budgeted in Fld Maint Budget B11.'. The MeLi contract supervisor (5310) and the domestic manager (5510) are different people, so there is no double count; the comment is stale. | MeLi supervisor in 5310 2027 = 104,448 (Fld Maint Budget!B11 = 8,704/month x B12 = 1). FO HC r25 Field Maintenance Manager (Fld Ops Payroll row 77) 2027 = 120,900; incremental supervisors (row 73) 2027 = 193,632. | 0 | impact 0 | SD owner to confirm and delete the stale comment. |
| I-16 | LOW | Fld Maint T&E Data!M5:M388 (SD, hidden, not carried) | 101 T&E transactions are flagged 'Reclass needed' = Yes, totalling $27,804.02; booked GL differs from budget GL. 2 are tagged 'AI suggested' and 17 have tag basis 'Assumed'. If FO 2026 actuals were pulled on booked GL, these sit on the wrong 2026 lines; totals are unaffected, and no formula in the output reads this sheet. | Top booked->budget GL pairs: 5050->5360 x34, 6100->5360 x16, 5360->5050 x14, 7550->5330 x12, 6100->5050 x8. | 27,804 | impact 27,804 | Finance to post the reclasses (or confirm none are needed). |
| I-17 | HIGH | Logistics&WH Payroll!A14:S51 (SD, not carried); PO!AG33:AG36; 'HC-PO'!B16:C20; 'HC-CO'!B17:C17 | The SD Logistics & Warehouse payroll model (547,441 for 2027, referenced by no formula) names two people who are already on HC rosters: its Logistics Manager seat (LOG-01) is CO HC r17 Field Logistics Manager (costed in CO 6610-6640; the model's own note classifies the seat as Central Operations) and its first Material Handler seat (MH-01) is PO HC r20 Material Handler (costed in PO 5110-5140). Net of those two seats (210,912 at model rates), the model adds 336,530 that no roster or P&L line carries: 7 seats (INV-01, TL-01, TL-02, MH-02, MH-06, MH-03, MH-04), all hires from Oct-26 on. MH-02 is described as the backfill for PO HC r16 Material Handling Team Lead, who stays on PO HC for all of 2027. | Seats (2027 cost at model rates, start): LOG-01 Logistics Manager 148,949 (on payroll); INV-01 Inventory Control Specialist 55,652 (Feb-27); TL-01 Material Handling Team Lead 64,544 (Dec-26); TL-02 Material Handling Team Lead 33,032 (Jul-27); MH-01 Material Handler 61,963 (on payroll); MH-02 Material Handler 61,963 (Oct-26); MH-06 Material Handler 31,751 (Jul-27); MH-03 Material Handler 52,712 (Mar-27); MH-04 Material Handler 36,876 (Jun-27). Net seats headcount Jan..Dec 27: 2, 3, 4, 4, 4, 5, 7, 7, 7, 7, 7, 7. The two overlapping people cost 204,109 on their HC rosters (already in the budget). Seats the model itself excludes: LOG-02 (= FO HC r21, budgeted in FO) and MH-05 (in no model, I-27). PO HC r16 2027 cost 72,061 at PO rates. | (336,530) on the contribution (net); v5 showed the gross 547,441 | impact 336,530 (> $250k) | PO owner to confirm the warehouse team plan. If adopted, add the 7 new seats (336,530), not the model total. Confirm whether PO HC r16 leaves the role MH-02 backfills; if so PO HC is overstated by up to 72,061. |
| I-18 | LOW | Fld Ops Payroll!B10; Fld Ops Payroll!B15; Fld Ops Payroll!B16 | The hiring horizon ends at Dec-27 (DeploySum row 54). Hires for Jan-28 go-lives use an Oct-Dec 27 average default rather than a forecast (documented by the author). | B10 = 1; B15 = =ROUND(AVERAGE(DeploySum!O54:Q54),0) = 7; B16 = =ROUND(AVERAGE(DeploySum!O57:Q57),0) = 2; cell notes on B10/B15/B16. | not determinable | hygiene | Overwrite B15/B16 if a 2028 go-live forecast exists. |
| I-19 | LOW | FE!U30:AF75 (rows 30-31, 67-69, 74-75); Fld Eng Budget rows 28-33, 85-91 | FE and Fld Eng Budget link in both directions: Fld Eng Budget reads FE 2026 columns, and FE 2027 rows read Fld Eng Budget. LibreOffice recalculated with no errors (no cell-level circularity), but the structure is easy to break. | Fld Eng Budget has 68 references to FE; FE has 84 references to Fld Eng Budget. | not determinable | hygiene | Check Fld Eng Budget before editing the FE 2026 columns it reads. |
| I-20 | LOW | SD sheets Prod Payroll, Old Draft, Fld Maint T&E Data (hidden); DeploySum!A41:A42 (hidden rows 41-42) | SD has 3 hidden sheets; Prod Payroll is carried and kept hidden, the others are not carried (FO/FE do not depend on them). DeploySum row visibility for rows 3-49 now follows the 9/30/26 file. | Hidden in output: ['Prod Payroll']. DeploySum hidden rows v2 [30, 32, 33, 34, 35, 36, 40, 41, 42] -> v3 [41, 42] (rows 30, 32-36 and recognized revenue row 40 are now visible, as in the 9/30/26 file). | not determinable | hygiene | None, unless reviewers want Old Draft / T&E Data in the pack. |
| I-21 | LOW | Fld Maint T&E Data!Q26 (SD) | Old Draft dependence is contained: 1 cell(s) outside Old Draft read it, none in the FO/FE chain, so the output has 0 references to it. | SD Fld Maint T&E Data: 1 cell(s) e.g. Q26: ='Old Draft'!B28*'Old Draft'!B23. SD dependency map: Old Draft -> {'Fld Maint T&E Data': 458, 'Fld Ops Payroll': 131, 'DeploySum': 112}. | not determinable | hygiene | None for the budget. Consider deleting Old Draft once the reference is re-pointed. |
| I-22 | LOW | COO P&L!A23:A24, B27, B37 (same rows on FO, PO, CO, FE, PE) | Rows 23 and 24 carry the same label ('5025 - Freight and Delivery - Production (Summary)'). Row 23 is an empty header; row 24 holds postings inside row 27 (=SUM(B24:B26)). Row 37 (=B19+B22+B27+B28+B29+B30+B31+B36+B20+B21) covers every direct child of its section, so nothing is skipped today, but anything typed on row 23 would be left out. | Subtotal scan on 6 sheets: 0 skipped lines with values. Non-empty cells on row 23 by tab: {COO P&L: 0, FO: 0, PO: 0, CO: 0, FE: 0, PE: 0}. COO P&L dept-sum formulas omitting a dept: 0. | not determinable | hygiene | Optionally relabel row 23 as a header, or lock it. |
| I-23 | LOW | COO P&L!B65:M65; COO P&L!C141 | COO P&L row 65 (labelled 'Expense') holds an unlabelled gross-margin % formula (=IFERROR(B64/B16,"")). With 2027 revenue now budgeted, it shows a 2027 margin (AG65 = 21.9%). Row 141 shows an extreme ratio for Feb-26 caused by negative 2026 payroll postings. | COO P&L!C141 = -14.33 (ratio). PO!N67 (308,059) -> AG67 0; PE!N35 (56,264) -> AG35 0. | not determinable | hygiene | Label row 65. Finance to explain the negative 2026 payroll postings in PO 6610 and PE 5140. |
| I-24 | LOW | Workbook defined names (xl/workbook.xml <definedNames>, workbook scope, no cell); list in 02-build_pruned_names_v2.csv | The COO book carries 14,310 legacy defined names from an old template. None is used by any formula, data validation, conditional format, chart or other name. v2 pruned the 5,345 unused names whose target is #REF! (5,330) or external-looking (15); 8,965 remain (string/array constants and plain values). | Before 14,310, after 8,965. Usage scan covered cell formulas, data validations, conditional formats, charts, print areas/titles and other names (counts in the notes file). Names referenced: 0 from parts, 0 from other names. Pruned names still referenced: 0. | not determinable | hygiene | Optional: purge the remaining constant-valued legacy names in Name Manager. |
| I-25 | LOW | Prod Payroll!B24:S81; DeploySum!A1 (notes) | Side effects of moving from Google Sheets to xlsx: threaded comments become plain notes (text kept); Google's '#ERROR!' has no Excel equivalent; LibreOffice saves error constants as '=#REF!' formulas. v3: DeploySum no longer has errors; Prod Payroll's remaining errors are now #NAME? (LibreOffice has no XLOOKUP), not #REF!. | Errors v2 -> v3: DeploySum {'#REF!': 463, '#N/A': 35} -> none; Prod Payroll {'#REF!': 796} -> {'#NAME?': 430}. New errors: 0. | not determinable | hygiene | None; disclosed for reviewers. |
| I-26 | RESOLVED | Fld Eng Budget!B21; Fld Eng Budget!B67:M67; FE!AG67 | RESOLVED (user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). v5 enters 205,000 in Fld Eng Budget!B21, the designated input cell. Was (v4, MED): 'Head of Service Delivery – [name]' (FE HC r16) had no salary entered, so FE 6610 carried $0 for this current employee. | Fld Eng Budget!B21 = 205,000; row 67 uses the roster formula of rows 59-66 (=IF(B$58>=$C$21,$B$21/12*(1+IF(B$58>=$B$25,$B$24,0)),0)...): start 2027-01-01 (C21) so 12 months paid, 17,083.33/month, +3% from 2027-10-01 (B24, B25) for 3 months (17,595.83/month): 2027 salary 206,538; payroll tax 6.8% (B22) 14,045; benefits 16.4% (B23) 33,872; total 254,454. FE!AG67 713,347 -> 919,884. | (254,454) on the contribution (in the v5 headline) | resolved; was MED (owner confirmation) | None. v6: the Head of Service Delivery is on FE HC r16 and Fld Eng Budget r21 only, not on CO HC or PE HC (I-28). |
| I-27 | LOW | Logistics&WH Payroll!B56 (SD, not carried); FO!U52:AF52 | Logistics&WH Payroll excludes MH-05 ('Less: MH-05 Material Handler, logistics support (counted on the FO tab)'), but FO 5510 2027 (FO!U52) sums only Fld Ops Payroll rows 21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77, none of which is an MH-05 seat; 'MH-05' appears nowhere outside Logistics&WH Payroll. So this seat is in neither model. | Logistics&WH Payroll!B56 = -38,133 (deduction of MH-05's 2027 base pay, before burden). FO!U52 = ='Fld Ops Payroll'!F21+'Fld Ops Payroll'!F31+'Fld Ops Payroll'!F43+'Fld Ops Payroll'!F56+'Fld Ops Payroll'!F69+'Fld Ops Payroll'!F76+'Fld Ops Payroll'!F77+'Fld Ops Payroll'!F34+'Fld Ops Payroll'!F46+'Fld Ops Payroll'!F59+'Fld Ops Payroll'!F72. MH-05 mentions elsewhere: none. | 38,133 base pay missing (before burden) | impact 38,133 | SD/PO owners to decide where MH-05 is budgeted and add it. |
| I-28 | MED | 'HC-FO'!B15:D15; Fld Eng Budget!A15:C15, row 61; Fld Ops Payroll!B11; 'HC-FE'!B41:D41; 'HC-CO'; 'HC-PE' | v6 answers the person-level question with the HC rosters. Every person on FE HC, CO HC, PE HC, PO HC, FO HC, SD Fld Eng Budget, SD Fld Ops Payroll, SD Logistics&WH and SD Prod Payroll was compared by name where present, otherwise by title + salary + start (A-29). CO and PE: no person on the FE roster is on CO HC or PE HC (0 name matches, 0 title + salary matches). The Head of Service Delivery is on FE HC r16 and Fld Eng Budget r21 only (nearest title elsewhere: PE HC r22 Head of Production and Delivery, a different person at a different salary; I-35). One person is costed twice in the budget: Fld Eng Budget r15 Field Engineer (75,000, 'current employee') has the same full name as FO HC r15 Field Technician (70,021), one of the 14 current techs Fld Ops Payroll costs by count (B11 = 14). FE HC has no salary for this person; its r41 'Field Engineer' row is open (no name, salary or start). | FE side 2027: salary 75,562.50, with SD burden 93,093. FO side: one current tech at model rates 78,198 (salary 63,472.50). Pair scan: 9 same-person pairs inside one P&L source (FE HC <-> Fld Eng Budget 7, FO HC <-> Fld Ops Payroll 2); 1 duplicate across P&L sources; 2 with the not-carried Logistics&WH model (I-17). Roster-to-P&L map: 02-build_roster_map_v6.csv (no names). | +78,198 to +93,093 (budget overstated by one person) | impact 93,093 ($50k-250k) | SD / FO owners: confirm whether this person moved from FO to FE. Then remove them from one side (Fld Ops Payroll B11 14 -> 13, or Fld Eng Budget row 15) and, if the move is real, give FE HC r41 the salary and start month. No budget value changed in v6. |
| I-29 | LOW | Prod Payroll!M9; Fld Ops Payroll!M7; Fld Eng Budget!B59 (row formula); PO!AD33; PO!AD34; PO!AD35; CO!AD67; CO!AD68; CO!AD69; PE!AD67; PE!AD68; PE!AD69 | Raise timing is consistent (same % and month everywhere), but the eligibility rule is not: Fld Ops Payroll and Logistics&WH Payroll exclude staff hired in the months before the raise (Prod Payroll!M9), while Fld Eng Budget and the typed PO/CO/PE payroll rows apply the raise to the whole row. | Prod Payroll!M5 = 0.03, M6 = 2027-10-01, M9 = 6. Steps found in typed rows: PO!AD33 3.00%; PO!AD34 3.00%; PO!AD35 3.00%; CO!AD67 3.00%; CO!AD68 3.00%; CO!AD69 3.00%; PE!AD67 3.00%; PE!AD68 3.00%; PE!AD69 3.00%; FE!AD67 3.00%; FE!AD68 3.00%; FE!AD69 3.00%. | not determinable | hygiene | Payroll owners to confirm whether the eligibility rule should apply to all departments. |
| I-30 | LOW | DeploySum!A2, A7, A9, A11, A13, A29, A30, A35, A38, A39, A40, A41, A42 | The source labels say '$000s', but the values are whole dollars. v3 relabelled the 13 cells to '$' (A2 text: 'Dollars in $ (relabelled in v3; the source said $000s)'). Each cell has a comment quoting the original label, so the change is visible, not silent. | E.g. DeploySum!R13 total bookings 29,452,766 and R29 Production CapEx 32,410,900 are dollars: CapEx = units x unit cost in dollars (section 'Unit-cost reconciliation'), and recognized revenue is the same order as PO's 2026 revenue in dollars. | 0 | hygiene | Plan owner to fix the labels in the source (Revenue Roll-up / Deploy) so the next export is right. |
| I-31 | LOW | 'Depreciation Schedule'!A88:D97; PO!J20:M22; DeploySum!C19:E20 | Oct-Dec 26 go-lives are carried in the PO Dec-26 run rate, not added explicitly. The risk runs both ways. (a) Shortfall: PO steps up for 15 lifts and 53 trays in Q4-26, DeploySum has 18 and 67; if DeploySum is right the budget is short 39,057. (b) Possible double count: PO's Dec-26 step-up (3 lifts, 12 trays) has no DeploySum Dec-26 go-live. If these are units DeploySum places in Jan-27 (20 lifts, 60 trays, built Nov-26), they sit in both the run rate and the Jan-27 vintage: 37,457 too much. If (b) holds and DeploySum's Q4 counts are right, the gross Q4 shortfall is 76,514 and the net is still (39,057). The 5020 step-ups cannot be reproduced from DeploySum's peripheral cost. | PO 5011 monthly step-ups Oct/Nov/Dec: 6,964.29, 2,321.43, 2,321.43 = 9, 3, 3 lifts x 65,000/84. 5012: 1,933.33, 800.00, 800.00 = 29, 12, 12 trays x 8,000/120. 5020: 2,608.33, 1,025.00, 1,025.00 = 52.95, 20.81, 20.81 peripheral sets at 4,137.50/84 (not whole). DeploySum Oct/Nov/Dec lifts [9, 9, 0], trays [35, 32, 0]. Dec-26 step-ups with no DeploySum Dec-26 go-live: 3 lifts x 773.81 + 12 trays x 66.67 = 3,121.43/month, 37,457 for 2027. Gap not budgeted: 3 lifts + 14 trays = 3,254.76/month, 39,057 for 2027 (plus up to 10,639 if Q4-26 lift peripherals are not in 5020). | (39,057) to +37,457 (5020 Dec step: up to +12,300 more) | impact 39,057 (< $50k) | PO owner to say what the Oct/Nov/Dec-26 step-ups on PO rows 20-22 are (which go-lives, which month). Then the user chooses: keep the PO run rate (current), or Sep-26 run rate + DeploySum Oct-Dec 26 vintages. Do not do both. |
| I-32 | HIGH | 'Depreciation Schedule'!B21:B24; PO!M19:M22; PO!U19:AF19 | Existing-fleet depreciation is carried flat at the PO Dec-26 run rate for all 12 months of 2027. The flat carry is a builder assumption (A-17): the brief asked for the PO 2026 monthly depreciation as the existing-fleet input, not for a flat carry. The workbook has no asset register, so it cannot show whether any of these assets reach the end of their life, or are retired, in 2027. The largest line is 5010 SlipBot: 112,797.85/month = 1,353,574 in 2027. Whether the SlipBot fleet is fully depreciated, retired or ongoing is not in the files. DeploySum note 4 says no SlipBots are built and existing bots are redeployed, which suggests the fleet is in use. 5020's run rate basis is also unknown (I-31). Trend alternative: 5010 fell through 2026 (141,122 Jan -> 112,798 Sep, (3,541)/month); continuing that decline through 2027 from the Sep-26 level lowers depreciation by 276,164 (151,680 on the Jan-Aug actuals trend, (1,945)/month); if the decline also runs through Oct-Dec 26 (floored at 0) it lowers it by 403,624 (221,687 on the actuals trend). The 5020 base (8,212 in Jan-26, when 5011 was 0) predates SlipLift depreciation, so it is probably SlipBot-related and may share the SlipBot end-of-life risk (98,543 for 2027 at that rate). | Dec-26 run rates (PO!M): 5010 112,797.85, 5011 20,444.90, 5012 6,502.64, 5020 19,525.33; 2027 existing total 1,911,249. 5010 2026 actuals Jan-Aug 141,122.35 -> 127,510.00, forecast Sep-Dec flat 112,797.85; 2026 total 1,492,329. | up to +1,353,574 (5010 = 0); trend +276,164 (continued from Sep-26: +403,624); 5020 base up to +98,543 | impact 1,353,574 | USER DECISION: confirm SlipBot fleet status (fully depreciated / retired / ongoing / declining as in 2026) and the end-of-life month for any existing asset group. Change the section 2 input on the schedule if the run rate stops. |
| I-33 | MED | 'Depreciation Schedule'!B7, B11, B16; PO!U22:AF22 | SlipLift peripherals (4,137.50 per lift, from DeploySum CapEx) are depreciated on 5020 Robot Peripherals over 84 months. Both the GL and the life are builder assumptions: the user gave lives for SlipLifts and SlipTrays only. 5020 was chosen because PO's 2026 forecast books 5011 at exactly $65,000/84 per lift, so PO keeps peripherals out of 5011. | 2027 new-peripheral depreciation 63,836 (Dec-27 12,313.99/month). Moving it to 5011 changes the GL split only, not the total. A different life changes the amount in proportion (e.g. 60 months: 89,370). | 63,836 | impact 63,836 | User to confirm the peripherals GL (5020 or 5011) and life; both are input cells. |
| I-34 | MED | Fld Eng Budget!B22:B23; Fld Ops Payroll!B7:B8; 'HC-FE'!D6:D7; FE!AG68:AG69 | Payroll tax and benefits on FE salaries use the SD field rates (6.8% / 16.4%, Fld Eng Budget!B22:B23 = Fld Ops Payroll!B7:B8). FE HC uses the FE rates from the T&B file, 4.069% / 7.223% ('HC-FE'!D6:D7, stored as values, A-30). On the 2027 FE salary base 919,884 the budget carries 6630 62,552 and 6640 150,861; at FE HC rates they would be 37,432 and 66,442. Not changed in v6 (no budget change without a user decision). | Difference 2027: 6630 +25,120, 6640 +84,419, total +109,539 more in the budget than at FE HC rates (on the matched people only, 816,751 of salary: +97,258). Other departments: FO HC rates 6.847% / 16.405% are within 0.047 points of the SD rates; PO, CO and PE payroll already use their HC rates. | +109,539 if the FE HC rates are right | impact 109,539 ($50k-250k) | User / Finance: choose the FE burden rates (FE HC T&B rates or the SD field rates). If FE HC, set Fld Eng Budget B22:B23 to the FE rates. |
| I-35 | MED | 'HC-PE'!A22:Z22; PE!AG67:AG69 | PE HC r22 Head of Production and Delivery (225,000, Sep-26 to Dec-27) is marked 'transfer?' in column A. The row is costed in PE 6610-6640 for all of 2027 (PE 2027 payroll equals PE HC). The person is on no other roster (0 name and 0 title matches), so there is no double count today. If the transfer happens, the cost leaves PE, and leaves COO if the receiving department is outside the five COO departments. | 2027 cost: salary 226,688 + payroll tax 8,096 (3.57%) + benefits 20,001 (8.82%) = 254,785. The HC tabs have Transfers In/Out blocks (rows 51-64) for such moves; none is filled. | up to +254,785 (leaves COO from Jan-27); 0 if it moves within COO and is budgeted once | impact not determinable; owner confirmation needed (exposure 254,785) | PE owner to confirm the transfer, the month and the receiving department; record it in the Transfers Out / In blocks so it is budgeted once. |
| I-36 | LOW | Fld Eng Budget!A15:C15, A19:C19; 'HC-FE'!B41:F41; FE!AG67 | Fld Eng Budget costs two rows that FE HC does not: r15 Field Engineer 75,000 (the same person as FO HC r15; I-28) and r19 Customer Support Specialist, a new hire from Aug-27 at 65,000 (links to r18). FE HC instead has an open 'Field Engineer' row (r41) with no salary or start. Together the two rows explain the whole gap between FE HC salary 816,751 and the budget's FE 6610 919,884. Start months differ for every matched person (HC Sep-26, or Dec-26 for the Field Engineer Manager; Fld Eng Budget Jan-27), with no 2027 effect. | Gap 103,133 = r15 75,562.50 + r19 27,570.83. Matched people: 2027 monthly salary identical (max difference 0.00). The COO book's FE 6610 (675,701) is FE HC less FE HC r35 Field Engineer Manager (141,050, from Dec-26). | +33,967 if the Aug-27 hire is not approved (salary 27,571 + SD burden) | impact 33,967 (< $50k) | FE owner to confirm the Aug-27 Customer Support Specialist hire and add it to FE HC if approved; the r15 row is handled under I-28. |

### Variance scan: rows with |AG-N| > $50k and > 50% (v5 workbook; unchanged in v6: 0 value diffs)

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

## Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; unchanged in v6)

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

Result: 0 likely double counts on the same GL row. Unclear rows are logged as I-28. v6: the HC rosters answer the person-level question for rows 67-69 (no FE person on CO HC or PE HC); the one person costed twice sits on two different GL rows (FO 5510 and FE 6610), see I-28. Cross-row overlaps found while tracing: none between FO payroll and Logistics&WH (FO HC r21 Operations Coordinator is excluded from Logistics&WH, Logistics&WH Payroll!B55, and costed in Fld Ops Payroll row 76: 2027 77,089); one seat in neither model (MH-05, I-27); the current employee with no salary in v4 (I-26) has a salary from v5 (Fld Eng Budget!B21 = 205,000).

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

## Not done / limits

- The external workbook '[1]' is still not available: DeploySum holds the 9/30/26 cached values, not live links.
- No fixed-asset register was supplied, so existing-fleet depreciation is a run rate, not an asset-by-asset schedule. End-of-life dates are unknown (I-32).
- Not opened in Microsoft Excel. Prod Payroll's XLOOKUP rows show #NAME? in LibreOffice 24.2 and may evaluate in Excel (untested).
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
