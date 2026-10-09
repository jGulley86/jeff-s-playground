# Brief v1 — 2027 COO Budget Collation

## Objective
Collate the two uploaded workbooks into ONE 2027 COO budget workbook, and flag issues.

## Inputs (read-only copies)
- `00-brief/inputs/COO_Dept_PLs_2027_Budget_2.xlsx` — "COO book": `COO P&L` roll-up (=SUM of FO,PO,CO,FE,PE per cell) + dept tabs FO, PO, CO, FE, PE.
- `00-brief/inputs/Service_Delivery_PL_worksheets.xlsx` — "SD book": DeploySum, FO, FE, Fld Ops Payroll, Prod Payroll (hidden), Fld Maint Budget, Fld Eng Budget, Logistics&WH Payroll, Old Draft (hidden), Fld Maint T&E Data (hidden).

## Orchestrator pre-scan (facts, to be re-verified)
- FO and FE tabs exist in both books with identical layout (labels match rows 1–200; same formulas in AG).
- SD book's FO/FE are the fuller builds. Cached 2027 (AG) totals: FO Net Income COO book -1,341,298 vs SD -7,347,500; FE -752,002 vs -1,320,148.
- COO book cached 2027 Net Income = -5,277,004 (uses old FO/FE).
- SD book DeploySum references an external workbook `[1]Revenue Roll-up` (not supplied).
- COO P&L 2027 revenue cached = 0 (2026 revenue 7.42M).
- LibreOffice available at /usr/bin/soffice for headless recalculation.

## Approach (decided)
Base = COO book. Replace its FO and FE tabs with SD book's FO/FE, bring across SD supporting tabs that FO/FE formulas depend on (keep hidden state), so `COO P&L` rolls up the new numbers. PO, CO, PE untouched.

## Tasks / owners / order
1. builder — produce `02-build/02-build_COO_2027_Budget_Collated_v1.xlsx` + `02-build/02-build_notes_v1.md` (method, reconciliation table, issues log).
2. critic — review build vs brief (read-only). Saved to `03-review/`.
3. verifier — independently recompute reconciliation; PASS/FIX FIRST/BLOCKED. Saved to `04-verify/`.
4. orchestrator — merge into `05-final/`.
Research skipped: user supplied all sources.

## Completion criteria
- One .xlsx opening cleanly; formulas intact (not pasted values) where the source had formulas; recalculated cached values present.
- No #REF!/#NAME?/#VALUE! introduced by the merge.
- COO P&L 2027 total for every line = sum of FO+PO+CO+FE+PE 2027 for that line.
- FO and FE 2027 values in output match SD book exactly; PO/CO/PE match COO book exactly.
- 2026 actual/forecast columns: any FO/FE differences between books are flagged, not silently chosen.
- Issues list with severity, location (sheet!cell), and recommended action.

## Constraints
- Do not modify input files. Do not invent numbers; never fill gaps with estimates. No external sends.
