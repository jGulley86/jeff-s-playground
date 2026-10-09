# Verifier report v5 — VERDICT: PASS
Own scripts (scratchpad/verify5/a–d.py, ephemeral). Workspace untouched.

| Claim | Result | Evidence |
|---|---|---|
| Only input diff vs v4 = Fld Eng Budget!B21 (empty → 205000) | PASS | 0 formula changes |
| Downstream changes COO P&L 159 / FE 137 / Fld Eng Budget 129 | PASS | 130 incl. B21; other sheets 0 |
| HoSD 2027 cost: salary 206,537.50; tax 14,044.55; benefits 33,872.15; total 254,454.20 | PASS | FE AG67/68/69 919,884.37 / 62,552.14 / 150,861.04 |
| COO contribution AG132 393,486.04 → 139,031.84 | PASS | Rev, COGS unchanged; Opex +254,454 |
| Full recalc reproduces cache | PASS | forced-recalc profile; max diff 9.9e-08 |
| COO P&L = Σ depts | PASS | 3,014 cells; only ratio rows differ |
| 0 new errors | PASS | 443 error cells in both v4 and v5, identical set |
| Sign-flip: I-05 (830,571); I-17 (408,409); I-10 (245,393); all four (1,801,495); I-32 trend from Sep-26 +403,624 | PASS | |

Not re-derived: I-17 547,441 (source tab not in workbook); I-31, A-14, I-33 (unchanged from v4).
