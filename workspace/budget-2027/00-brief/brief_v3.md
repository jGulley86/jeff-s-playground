# Brief v3 — user decision: Option 3 (revenue + depreciation)
User instruction (2026-10-09): "Go with option 3. Depreciation is linear. 7 years on SlipLifts and 10 years on Trays."

## Scope for v3 build (starts from v2)
A. DeploySum refresh, as in brief_v2 items 1–2.
B. Revenue: put 2027 monthly recognized revenue from new DeploySum (row 39, Jan–Dec 27) into the 2027 budget.
   - Assumption to label: it goes to PO 4100 Subscription/Platform Fees, because PO holds all 2026 revenue. 4500 and 4900 stay 0 unless the source splits them.
   - Use formulas that reference DeploySum cells, not pasted numbers.
C. Depreciation: straight-line, SlipLift 7 yrs (84 months), SlipTray 10 yrs (120 months), no salvage.
   - Build a visible "Depreciation Schedule" tab with input cells (life, unit cost, start convention, GL mapping) and monthly calcs. PO depreciation rows link to it.
   - Unit cost comes from the DeploySum notes (row 46 text) and/or CapEx ÷ units. Reconcile the two and report any gap; never guess.
   - In-service = go-live month (DeploySum rows 19/20 units going live). Depreciation starts in the go-live month (full-month convention, labelled; the user may change it).
   - Existing fleet (in service before Jan-27, including Sep–Dec 26 go-lives): it must not be double-counted against the 2026 run rate. Use the PO 2026 monthly depreciation (rows 19–22, B:M) to show what the existing fleet runs at. Carry it as a separate, labelled input line.
   - Units deployed Sep–Dec 26 are either in that run rate already or added explicitly; show which and why.
   - GL mapping is an assumption to label: SlipLift → 5011. SlipTray → choose between 5012 SlipCarrier and 5020 Peripherals based on the 2026 history, and flag the choice. SlipBot 5010: none built in 2027; existing SlipBot depreciation is handled per the existing-fleet rule above.
D. Notes: headline shows full 2027 Net Income (now with revenue and depreciation), the cost-only view, and the 2026 comparison. Update I-01 and I-07 to resolved-by-assumption and add the new assumptions to the issues/assumptions list.

## Unchanged
- No changes to FO/FE/CO/PE values, or to PO non-revenue, non-depreciation lines.
- Every other v1/v2 rule still applies.
