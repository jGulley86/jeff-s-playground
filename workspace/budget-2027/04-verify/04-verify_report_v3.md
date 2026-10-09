# Verifier report v3 — VERDICT: PASS
Independent scripts (scratchpad/verify3/v.py, w.py; ephemeral). No fixes required.

| Claim | Result | Evidence |
|---|---|---|
| Headline AG: Rev 15,563,646; COGS 12,152,017; GP 3,411,628; Opex 3,018,142; NI 393,486 | PASS | cached = recalculated |
| 2026 N unchanged (NI -899,222) | PASS | 0 diffs vs v2, col N rows 9–141 |
| Depreciation by first principles, 48 GL-months | PASS | max diff 3.8e-10; 5010 1,353,574 / 5011 1,248,196 / 5012 418,898 / 5020 298,140; existing 1,911,249 + new 1,407,560 |
| Unit cost lift 65,000 + periph 4,137.50; tray 8,000 | PASS | periph derived (note prints $4,138) |
| CapEx recon Sep-26..Dec-27 | PASS | 0.0 in all 16 months |
| Depreciable cost 2027 go-lives 25,572,375 | PASS | 250×69,137.50 + 1,036×8,000 |
| Existing = 12 × source PO M19:M22 | PASS | 112,797.85 / 20,444.90 / 6,502.64 / 19,525.33 |
| No double count | PASS | new vintages reference DeploySum F:Q only; Q4-26 in run rate only; 3-lift/14-tray shortfall memo only |
| Revenue PO!U12:AF12 = DeploySum!F40:Q40 | PASS | sum 15,563,645.54 |
| FO/FE/CO/PE 0 diffs vs v2; PO only rows 12, 19–22 + subtotals + AH | PASS | |
| New budget values are formulas | PASS | 60/60; typed only labelled inputs |
| 0 externalLink parts; 0 DeploySum errors | PASS | |
| COO P&L = Σ depts | PASS | 2,988 cells; only hit is ratio row 141 (excluded) |
| Full recalc reproduces cache | PASS | 24,058 numeric cells, 0 mismatches |

Open assumptions (not calc errors): I-32 SlipBot run rate, I-33 peripherals GL/life, revenue all in 4100, existing fleet assumes no end-of-life in 2027.
