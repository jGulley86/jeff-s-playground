# Verifier report v6 — VERDICT: FIX FIRST (one minor figure)
Own scripts (scratchpad/verify6/, ephemeral). No names in report.

CONFIRMED:
- 0 formula/value diffs vs v5 on the 12 existing sheets (227,850 cells). AG132 = 139,031.84.
- HC tabs equal the workfile, with 0 errors. D6:D7 external links are stored as values.
- Roster totals: FO 1,341,298; PO 652,820; CO 618,961; FE 908,980; PE 1,211,637. PO/CO/PE P&L tie to HC.
- Prod Payroll 2,592,894: independently re-derived in Python (lift 1,622,423; tray 729,177; supervisors 241,294).
- I-05 net 1,962,389. I-17 547,441 − 210,912 = 336,530. Combined 2,298,919.
- FO current staff 1,338,696; ramp 2,618,543.
- Duplicate person confirmed by name: Fld Eng Budget Field Engineer (75k) = HC-FO r15 (Field Technician). On no other roster.
- HoSD is on HC-FE only.
- I-28 remove-from-FE +93,093; FE burden +109,539; I-36 +33,967; PE r22 254,785.
- Range (2,583,369) to 1,492,606.
- No names in the md, Collation Notes or CSV.

FAIL (minor):
- I-28 remove-from-FO: stated +78,198 (payroll only). Fld Maint Budget!B29 also references Fld Ops Payroll!B11, so 5330 falls by a further 331. True effect +78,529, which puts the "contribution after this item" at 217,561 (stated 217,230).

NOTES:
- Prod Payroll rows 48–81 show #NAME? in the shipped file (LibreOffice lacks XLOOKUP); this does not feed the P&L.
- Logistics&WH is not in the workbook, so I-17 traces to the SD source only.
- FE "7 of 7 matched" claim not verified.
