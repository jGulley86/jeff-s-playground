# Verifier report v8 — VERDICT: PASS
Own scripts (scratchpad/verify8/).

- **Labour depreciation from first principles:** 5011 118,077.55, 5012 34,960.51, total 153,038.06. All 12 months match.
- **Capitalised labour split:** 1,942,322.72 into 2027 go-lives; 650,571.18 carried to 2028; Oct–Dec 26 381,863.44; Sep-26 90,851.44 excluded.
- **Prod Payroll totals:** reproduced (2,592,893.90). 0 XLOOKUP cells left.
- **INDEX/MATCH vs XLOOKUP:** semantics confirmed on 16 test values (exact, between tiers, above max, below min).
- **Full recalc:** 27,876 cells, 0 mismatches. This also holds from a stripped cache.
- **Diff vs v7:** confined to the allowed areas, plus Collation Notes. 0 changes in 2026 columns.
- **PO 5110–5140 2027:** 652,819.95 → 0.
- **Contribution:** 638,813.73.
- **Sensitivities:**
  - B131 = 0 → 37,695.83
  - B132 = 0 → 687,435, with depreciation 104,417
- **Range:** (273,550) to 1,992,388; LB2 (802,068).
- **Jun-27 hand check:** matches.

Not verifiable: the Excel engine; the policy/scope choices (A-38..A-41).
