# Brief v5 — user decision: production labour is capitalised (v8 build)
User (2026-10-10): "Yes, production labor is capitalized. Use the same formula as the file has." "Yes, my GitHub is private."

## Interpretation (orchestrator)
- "The file's formula" for production labour = the SD Prod Payroll model (2027 total 2,592,894; verified by independent Python replica). "The file's formula" for capitalisation = the existing Depreciation Schedule logic: straight-line, full month from go-live, 84 months SlipLift / 120 months SlipTray, go-live 2 months after build per DeploySum.
- Policy consistency: if production labour is capitalised, the current 9 PO staff (PO 5110–5140, 652,820, already inside the Prod Payroll model) are capitalised too.
  - Primary case: PO 5110–5140 2027 expense → 0. All production payroll is capitalised into unit cost and depreciated.
  - Sensitivity (shown, not booked): only the ramp is capitalised and the current 9 stay expensed.
  - Flag that 2026 actuals expensed 208,574 in 5100, so the 2026 policy may have been partial.

## Scope
1. Bring Prod Payroll into a computing state in the workbook. XLOOKUP is not evaluated by LibreOffice, so either:
   - rewrite only the XLOOKUP cells as an equivalent INDEX/MATCH ("next tier up, else max"), proven equal to the verifier replica within $1; or
   - keep XLOOKUP and justify that choice.
   Document the change cell by cell. No other change to the model.
2. Add a capitalised-labour block on the Depreciation Schedule:
   - monthly production payroll by build month, split lift/tray (supervisors pro rata, as in v7 A-32);
   - labour per unit built (by month);
   - added to the depreciable cost of each vintage at go-live;
   - depreciation into 5011 (lifts) / 5012 (trays). Peripherals are unaffected.
   - Builds for 2028 go-lives carry labour that is not depreciated in 2027 (sits in CIP/inventory); report the amount.
   - Sep–Dec 26 production labour (the model's 2026 months) feeds Jan–Feb 27 go-lives; include it where those builds go live in 2027, and say how.
3. PO 5110–5140 2027 → formulas giving 0 (or a reclass line), labelled as capitalised. Keep 2026 actuals untouched.
4. Notes:
   - Decision #1 becomes RESOLVED (user-confirmed).
   - Headline uses the capitalised case.
   - I-05 resolved by policy; remaining exposure = depreciation only.
   - Recompute the caveat table, range and sign-flip statement.
   - Remove "no exact per-person amounts" (v7 verifier) and state the disclosure honestly.
5. All other values unchanged; prove it with a diff vs v7.
