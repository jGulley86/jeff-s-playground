# Critic review v6 — 3 BLOCKING, 8 OPTIONAL
(Saved by orchestrator from critic message. No employee names.)

## BLOCKING
- B1 Capitalisation not tested. I-05 treats the 1,962,389 production ramp as expensed. But:
  - DeploySum labels the unit costs (65,000 lift / 8,000 tray) "Unit cost (CapEx)".
  - 2026 PO 6000 SG&A labour is negative (309,871), and PE 5140 is negative too. Both are consistent with a capitalised-labour credit.
  - 2026 COO 5100 was only 208,574, so 2.6M would be a 12.5x rise.
  - Contract labour (7200, 214,591 in 2026) is another possible home.
  Fix: caveat I-05 and Decision #5 ("expensed or capitalised?"), add the 2026 base comparison, and label the lower end of the range accordingly.
- B2 The Prod Payroll overlap is matched by count only (9 of 9). The evidence points to 7: PO HC's 9 = 7 production staff + 2 material-handling roles, and those 2 are tied to Logistics&WH. If only 7 overlap, I-05 is understated by about 2 staff at model cost. Fix: drop the "no person-level overlap is left" wording, show both readings, compute the 7-overlap case, and explain which seats are subtracted twice in 2,298,919.
- B3 The asymmetry is not headlined: the FO ramp (2.62M) is in the budget, the PO ramp (1.96M) is not, and both are driven by the same deployment plan. Fix: add a headline caveat, conditional on B1.

## OPTIONAL
1. Show I-05 at PO HC burden rates (~24.3% vs the model's ~15.5%; about +140k) as a sensitivity.
2. The models hire 15 Prod staff, plus MH-02 and TL-01, in Sep–Dec 26. None of them is on the Oct-07 roster, so the models may be stale. Ask when the models were last updated.
3. Duplicate person: name match only; title and salary differ. It fits a planned FO→FE move. Reword to "probable duplicate"; the upside is partial if the move happens mid-year.
4. The FO-side +78,198 ignores knock-on effects (Fld Maint B29, supervisor ratio). Recompute with B11 = 13 in a scratch copy, or list the omitted effects.
5. FE HC r35 Field Engineer Manager is an open seat, not an employee. Amend A-29 (start month relaxed). _2 vs SD disagree on whether the seat is filled.
6. HC T&B tax rates (3.6–5.2%) are below employer FICA of 7.65%. They are unverified. The +109,539 upside may be overstated, and PO/CO/PE payroll may be under-budgeted. Ask Finance.
7. The range is built asymmetrically. State this, and optionally add a lower bound that excludes I-05.
8. Privacy: unique dept+title+salary labels in the md identify people. The workbook now holds named salary rosters for 47 people. Add a distribution caveat and round/aggregate unique-role salaries. The name list is in WORK_DIR, outside the repo (orchestrator checked: not tracked).
