# Critic review v8 — 2 BLOCKING, 7 OPTIONAL
Scope items 1 (XLOOKUP → INDEX/MATCH), 3 (PO 5100 = (1−B131)×v7) and 5 (diff confined) PASS. Headline, bridge, scenario and range arithmetic all tie.

## BLOCKING
- B1 The Sep–Dec 26 treatment is inconsistent, and in the booked case it double counts.
  - Sep-26 labour (90,851) is excluded "because it is in the PO run rate", but the run rate holds no labour, so the stated reason is false. The same wording appears in Depreciation Schedule A161 and B209.
  - With B131 = B132 = 1, the current 9 staff's Oct–Dec 26 labour is capitalised into the 2027 vintages, while the 2026 PO forecast (J:M) already expenses it. That is a double hit (est. ~20k of the 48,621 depreciation).
  - The Q4-26 ramp hires are in no 2026 book, so this creates an opening asset that does not exist.
  - Fix: one rule for all Sep–Dec 26 labour. Either B132 = 0 (2026 labour stays a 2026 cost), or capitalise it net of PO!J33:M35. Correct the labels and restate.
- B2 Idle-month labour is flagged but never quantified.
  - Jan-27 has no builds: expensing its labour (140,751) gives ≈ (126,900) net.
  - Oct-26 has no builds: ≈ (10,900) less 2027 depreciation.
  - Net ≈ (116,000). Paired with the scope sensitivity, this turns the contribution negative.
  - Fix: add a caveat row, and include it in the bounds, the sign-flip statement and I-40.

## OPTIONAL
1. "65k/8k holds no production labour" is stated with no source. Restore the "already in unit cost" upside (up to +153,038) and give it an owner.
2. Headline: state that this is a reclassification. CapEx needs +2.59M (+0.38M from Q4-26). Dec-27 balance sheet: 2,171,148 in service (net) and 650,571 not yet in service.
3. Call the 650,571 "PP&E not yet placed in service (CIP)", not inventory.
4. Footnote that the YoY change is not like-for-like (a policy change).
5. Conclusion should list I-10 and I-41.
6. Recompute the LB2 components under B131 = 0, or footnote them.
7. Current 9 are removed at HC rates (652,820) but capitalised at model rates (630,504): a 22,316 gap. State it.
