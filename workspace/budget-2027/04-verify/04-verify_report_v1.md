# Verifier report v1 — VERDICT: PASS
Independent scripts (not builder's): check1/2/3.py in session scratchpad/verify/ (ephemeral).

| Check | Result | Evidence |
|---|---|---|
| Opens cleanly, cached values present | PASS | openpyxl + LibreOffice convert OK; 12 sheets. Excel itself untested. |
| Formulas intact | PASS | Formula counts match source per sheet (COO P&L 3320, FO 2104, FE 2104, PO 2072, CO 2068, PE 2057, drivers match); DeploySum 515→498 = frozen external cells |
| Full recalc reproduces cache | PASS | 27,680 cells, 0 diffs >0.01 |
| No new #REF!/#NAME?/#VALUE! | PASS | Errors only in DeploySum (#REF! 463, #N/A 35) and hidden Prod Payroll (#REF! 796), identical to SD source |
| COO P&L = FO+PO+CO+FE+PE | PASS | Rows 9–132, B:N and U:AG, 2,807 cells, max diff 3e-8 |
| FO/FE = SD book | PASS | 0 mismatches (3371/3372 cells); driver tabs 0 mismatches |
| PO/CO/PE = COO book | PASS | 0 mismatches |
| COO P&L changed only on FO/FE-fed rows | PASS | diffs only in U:AG/AJ on rows 29-31,37,44-49,52-56,63,64,67-69,73-75,116,117,132,137,139-141; no 2026 diffs |
| 2026 FO/FE differences flagged | PASS | 0 differences B:N |
| Issues list complete | PASS | I-01..I-25 with severity, location, action |
| Headline: AG132 -11,851,351.34; N132 -899,222.05; AG63 8,833,208.99; AG16 0; FO NI -7,347,499.60; FE NI -1,320,147.57 | PASS | |
| 427 external-link cells frozen | PASS | 0 residual [1] formulas, no externalLink part |
| I-01, I-07, I-08, I-16 | PASS | PO N12 6,363,078 / N13 85,861 / N15 975,000 → AG 0; dep N19+N20+N22 ≈1.75M → 0; +5000 U28/Y28/AD28, +15000 U38/U42; 101 rows $27,804.02 |

Notes: Collation Notes holds text copies of error codes (not errors). External workbook not verifiable (accepted). 2027 NI is cost-only because revenue = 0.
