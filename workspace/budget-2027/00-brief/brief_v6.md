# Brief v6 — Logistics & Warehouse payroll moves to Central Operations (v10 build)
User (2026-10-10):
- "The WH and logistics numbers should hit central operations, along with [named CO employee]."
- The named employee makes $110,000 annually.
- "Yes, the material handler should move to CO."

New uploads:
- COO_HC_and_PL_workfile: byte-identical to the existing input.
- Service_Delivery_PL_worksheets: re-uploaded and saved as `inputs/Service_Delivery_PL_worksheets_v2.xlsx`. The orchestrator diff found 0 value differences; the only content differences are array-formula object identity. The Logistics&WH Payroll tab is unchanged.
- The Google Sheet link could not be read in this session. The user's screenshot shows the CO HC roster: 4 current employees plus an empty row. The named employee is not on it and is not in any input.

## Scope (v10, from v9)
1. **Bring in the Logistics&WH Payroll tab.** Copy it from the SD book into the workbook, cell by cell with styles. Its formulas must resolve in-book: it references Fld Ops Payroll and Prod Payroll, which are both present.
2. **Book the logistics model in CO.** CO 6610/6630/6640, 2027 months U:AF, = the existing CO values + the Logistics&WH model by seat, as formulas.
   - Salaries go to 6610, payroll taxes to 6630, benefits to 6640.
   - New-hire cost goes to the most appropriate existing CO line; state which one.
   - EXCLUDE seat LOG-01 (Logistics Manager). That person is already on CO HC r17 and is already inside CO's 6610–6640.
   - The material handler seat MH-01 (= PO HC r20) moves to CO through this model, as the user confirmed.
3. **Remove the material handler from PO so they are not counted twice.**
   - The PO 5110–5140 base used by the B131 switch must drop MH-01's PO HC cost. In the booked case PO 5100 is already 0; the B131=0 sensitivity must not double count.
   - Prod Payroll (capitalised labour) counts current staff by number only. Leave the model unchanged, but update I-41 / the 9-vs-7 overlap discussion: one of PO's 9 is now in CO.
4. **Add the new CO employee.**
   - Annual salary 110,000 (user-confirmed).
   - Assumption, to label: current employee in seat for all of 2027, Jan–Dec 27.
   - Use CO HC rates (D6/D7 tax and benefits) and the CO 3% raise from Oct-27, consistent with the CO roster.
   - Add the person as a new row on HC-CO in the empty current-employee row, so CO's roster total and P&L flow from it. Alternatively, add a clearly labelled line feeding CO 6610–6640. State which.
   - The name may appear on HC-CO, as it does for the other employees. It must NOT appear in the notes md or chat.
5. **Resolve issues.**
   - I-17 → RESOLVED (user decision): booked in CO.
   - Recompute the headline, caveat table, range and sign-flip.
   - The PO/CO payroll reconciliation tables must reflect the move.
6. **Diff vs v9.** Prove it is confined to: the new Logistics&WH tab; HC-CO (new row); CO rows 67–69 U:AF and their subtotals; the PO B131-base cells for 5110–5140; the COO P&L roll-up; Collation Notes. 0 changes in 2026 columns.
