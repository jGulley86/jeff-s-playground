# Critic review v1 — 3 BLOCKING, 10 OPTIONAL
(Saved by orchestrator from critic message.)

## BLOCKING
- B1. The notes describe freezing the 427 DeploySum external-link formulas "as instructed", but the brief has no such instruction. Brief criterion 1 is therefore unmet for those cells. Fix: present it as a declared deviation, give the reason, and point to Collation Notes for the original formulas.
  - Orchestrator ruling: partly wrong. The builder handoff did instruct freezing external refs to cached values. Fix the wording to "per orchestrator handoff; declared deviation from brief criterion 1 because the linked workbook was not supplied and there is no externalLink part".
- B2. The notes contradict themselves. The scan says there are no external links, yet I-24 says the 14,310 legacy names include external .xls pointers. Clean opening in Excel is unproven. Fix: inspect the output package (xl/externalLinks, definedNames count). Widen the usage scan to data validations, conditional formats, charts and print areas. If clean, prune the external and #REF! names in a logged step.
- B3. Cross-department double counting is unchecked. COO P&L AG30 = 392,987 vs FE AG30 = 346,633 (FO also has row 30). AG47 = 1,554,365 vs FO 1,519,865. PO AG33 production salaries 525,310 while Fld Ops Payroll reads Prod Payroll M5/M6/M9. Fix: for each 2027 GL line, a by-department table of rows where more than one dept is non-zero; trace the Prod Payroll refs; log overlaps with amounts.

## OPTIONAL
1. Hardcoded claims in report.py ("LibreOffice 24.2", "TBD 0 hits", "0 skipped lines", "all in U:AF") should be computed or removed. The version string is suspect.
2. I-17 Logistics&WH: give the cached 2027 total vs PO lines; re-rate severity.
3. I-06/I-15 MeLi double count: quantify it.
4. I-05: downgrade from HIGH (it feeds nothing).
5. I-16: downgrade to LOW.
6. Headline: lead with total 2027 COO cost; label Net Income incomplete (no revenue, no depreciation).
7. I-11/17/20/24/25 need sheet!cell; define HIGH/MED/LOW.
8. "Untouched" → "values and formulas unchanged; formatting re-saved by LibreOffice".
9. Page setup / print areas / sheet-scoped names not copied: state it as a limit.
10. DeploySum B17:R17 stale zeros look like real data: mark them. Also: raise-timing consistency check (FO payroll vs PO/CO/PE), or list it as not done.

## Criteria assessment
1 NOT MET as written (see B1/B2) · 2 MET in substance (#REF! counts rise from #ERROR! relabel + recalc; state it) · 3 MET · 4 MET · 5 MET · 6 PARTIAL
