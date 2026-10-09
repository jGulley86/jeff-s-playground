# Brief v4 — fourth input: COO HC & PL workfile (scope for v6, after v5)

## New input
`00-brief/inputs/COO_HC_and_PL_workfile.xlsx` (last modified 2026-10-07). Same P&L layout as the COO book, plus employee-level headcount tabs FO HC, PO HC, CO HC, FE HC and PE HC, and a COO HC roll-up. Each dept P&L payroll row is a formula pulling from its HC tab (e.g. PO!U33 = 'PO HC'!M67).
Taxes and benefits are a % of salary, per dept. The raise is 3% in Oct-27.
Hidden tab "Claude Log" is not relevant.

## Orchestrator pre-scan (facts)
- Version vs COO book (_2, modified 2026-10-09):
  - 2026 (N): identical on all rows.
  - FO and CO: identical.
  - PO payroll and PE payroll: identical. PO non-payroll 2027 lines are 0 in the workfile and filled in _2 (444k COGS + 172k opex). PE opex is 0 in the workfile and 85k in _2.
  - So _2 is the later P&L version.
  - FE 6610–6640 differs: workfile 908,980 vs _2 752,002.
- Rosters (2027 salary, per HC tabs):
  - FO: 16 people, 1,088,252 (= the COO book's old FO 5510).
  - PO: 9 people (team leads, production techs, material handling lead, material handler, associates), 525,311, flat through 2027 with no hires.
  - CO: 5 people (one starts Oct-26), 528,452.
  - FE: 7 people plus an open "Field Engineer" row with no salary. Includes Head of Service Delivery at 205,000/yr (matches the user's figure) and Field Engineer Manager from Dec-26 at 140k.
  - PE: 9 people, 1,078,020. One row is marked "transfer?" (Head of Production and Delivery, 225k).
- SD Fld Eng Budget roster vs FE HC: same people and salaries, except that SD adds a 75k Field Engineer (likely the open row) and an Aug-27 CS Specialist hire.
  - Burden rates differ: SD uses 6.8% tax / 16.4% benefits; FE HC uses 4.07% / 7.22%.

## Questions this input can now answer
1. I-28 (CO/PE vs FE SG&A overlap): rosters exist, so check for any person in more than one roster (FE HC, CO HC, PE HC, SD Fld Eng Budget, SD Fld Ops Payroll, SD Logistics&WH Payroll, SD Prod Payroll). Compare by title + salary + start month. Names may be used inside scripts, but never printed in notes or chat.
2. I-05 / I-17: PO 5100 = 9 current staff, flat. Do the Prod Payroll and Logistics&WH models include those same 9 (overlap), so that the true increment is model total minus overlap? Quantify the net ramp cost that PO lacks.
3. FO: does SD Fld Ops Payroll's current staff match FO HC's 16? Is SD's 3.24M = current 16 + ramp hires? Split it.
4. FE: SD burden rates vs FE HC actual rates. Quantify the difference. Not a budget change unless the user decides.
5. PE "transfer?" row: flag it.

## Scope (v6)
- Analysis and reconciliation, plus the HC tabs brought into the workbook as supporting tabs (read-only, provenance).
- Do not replace _2 P&L values with workfile values. _2 is newer; the payroll for PO/CO/PE is identical anyway.
- No budget value changes except by user decision.

## Open question for the user
Confirm that _2 is the latest P&L. Recommended: yes.
