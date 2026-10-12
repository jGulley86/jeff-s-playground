# Brief v7 — user additions to CO (v13 build, applied on top of v12)
User (2026-10-12): "add $2,000 per month in GL 7700 in CO; Add $6,500 per month in GL 8600 in CO".

## Orchestrator pre-scan (v11 state)
- CO row 98 = "7700 - Inventory Obsolescence-old": 2026 N = 0; 2027 = 0 (R="Even", S=0). Label carries an "-old" suffix; it is the only 7700 row.
- CO row 106 = "8600 - Repairs and Maintenance": 2026 N = 30,775.16; 2027 = 0 (R="Even", S=0).
- Template mechanics: with R="Even", U:AF = $S/12. So the native change is two INPUT cells, no formula edits:
  - CO!S98 = 24000  → U98:AF98 = 2,000/month, AG98 = 24,000
  - CO!S106 = 78000 → U106:AF106 = 6,500/month, AG106 = 78,000
- Expected downstream: CO Total Expense +102,000; contribution AG132 159,136.40 → 57,136.40; COO P&L rows 98/106/116/117/132 move identically.

## Scope (v13, from v12 once v12 lands)
1. Set the two S cells; leave R/T untouched; LibreOffice full recalc + engine save (same Excel-safe serialization as v12).
2. Diff vs v12 confined to: CO S98/S106 inputs + their U:AG/AH/AJ rows + CO subtotals (116/117/132, ratio rows) + COO P&L roll-up + Collation Notes. 0 changes to 2026 columns.
3. Notes: record both additions as user-confirmed (2026-10-12); flag (a) the 7700 label "-old" suffix for the user to confirm it is the intended account, (b) 8600 2027 = 78,000 vs 2026 30,775 (+153%, > the variance-scan threshold) as user-directed; update headline, caveat table, range, sign-flip (I-10 alone now −327k…; recompute by script).
4. Standard suite + verifier pass.
