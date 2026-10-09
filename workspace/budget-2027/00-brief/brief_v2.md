# Brief v2 — adds third input (supersedes v1 where stated)

## New input
`00-brief/inputs/2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` contains a single sheet, DeploySum (A1:R49), as of 9/30/26. Its cached values are fully resolved, with 0 errors. It is the same sheet as the SD book's DeploySum rows 1–49, with the `[1]` links resolved.

## Orchestrator pre-scan of new input
- Columns B:Q = Sep-26..Dec-27 month-ends and R = FY2027, the same layout as SD.
- Rows 4–35 align row-for-row with SD DeploySum. In rows 38–42 the new file has no "ARR – end of period" row (SD row 39), so new rows 39–41 = SD rows 40–42 (Recognized revenue, Billings, Deferred revenue).
- Tie-out to the typed drivers that feed FO/FE (SD DeploySum rows 53–66):
  - Total deployments FY27 = 67 in both files.
  - SlipLifts 250 = 212+30+8.
  - SlipTrays 1036 = 636+375+25.
  - So the FO/FE drivers are consistent with this file, and 2027 cost numbers should not change.
- Labels say "$000s", but the values are in dollars (e.g. bookings FY27 29,452,766; CapEx 32,410,900). This is a units-label error.
- Gives 2027 recognized revenue of 15,563,646 (Jan–Dec 27, as labelled). The COO P&L 2027 revenue is 0 (I-01).
- Gives 2027 Production CapEx of 32.4M (+9.4M of builds for 2028 go-lives). PO 2027 depreciation is 0 (I-07).

## Scope change (v3 build)
1. Replace DeploySum rows 4–49 in the collated workbook with the new file's values and formulas. Keep the `[1]` formulas visible as text on Collation Notes, and store cached values from the new file. Insert or keep the ARR row so the row map stays correct. Remove the stale-link flags where the values are now resolved.
2. Add a row-by-row tie-out check of rows 16–21 against rows 54–64.
3. Do NOT populate 2027 revenue or depreciation in the COO P&L. That needs a user decision. Show a memo comparison instead.
