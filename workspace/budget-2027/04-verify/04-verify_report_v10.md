# Verifier report v10 — VERDICT: PASS
Own scripts (scratch verify10/, since deleted). Workspace untouched (sha256 pre/post identical). No names in report.

## Confirmed (all to the cent unless noted)
- **Headline:** AG132 = 159,136.40; tie 687,435.11 − 398,492.42 − 129,806.29 holds; CO delta = AG132 delta.
- **CO 2027:** 6610 963,670.09; 6630 55,098.30; 6640 128,491.55; total 1,147,259.93. Independent Python recompute from the raw workfile/SD inputs matches all 36 GL-months to 4.4e-11.
- **New CO employee (HC-CO r18):** 129,806.29 (salary 110,825.00 at Jan-27 start + 3% Oct raise; CO HC rates). Live-linkage probes (salary → 120k; start → Feb-27) move CO exactly as expected.
- **Logistics less LOG-01:** 398,492.42, recomputed per seat from the SD inputs; LOG-01 (148,948.80) matches HC-CO r17 by name and salary; new-hire 5,000 flows to 6610; the in-book tab is cell-identical to the SD source (0 errors, cross-sheet inputs resolve in-book; live-linkage probe on Fld Ops Payroll B7 works).
- **PO base:** 652,819.95 → 590,317.51; drop = HC-PO r20 loaded 62,502.44; booked PO 5110–5140 stay 0; B131=0 recalc reproduces the 8-person base exactly.
- **Diff vs v9:** 79 formula + 565 value changes, all confined as claimed (incl. HC-COO values-only deviation, every delta = the new employee's amounts); 0 changes in 2026 B:N on the six P&L sheets; comments/merges/formats/names (8,965) unchanged; no external links.
- **Integrity:** full recalc 35,837 cells, 0 diffs >1e-6; COO P&L = Σ depts (max 5.0e-8); 0 error cells.
- **Scenarios:** B131=0 → (399,860); B135=0 → 32,228; both → (480,264); B132=1 → 98,441; B132=1+B131=0 → (433,274); I-10 alone → (225,288); idle+I-41 → (39,833); idle+I-31 → (6,829). LB1 (469,929); LB2 (909,032); UB 1,512,711. Only the two listed pairs flip the sign. All 31 exposure-table rows tie.
- **Privacy:** the new employee's name is in HC-CO B18 only; md/Collation Notes/CSVs have 0 name hits.

## Non-blocking notes (routed to the v11 notes pass)
1. PO!AI33:AI35 text stale ("restores the v7 amount" — now less r20).
2. Collation Notes H78:H81 check cells are static values (live recompute = 0).
3. HC-COO still lists r20 under PO and has no logistics seats, so HC-COO CO payroll (748,768) ≠ CO P&L (1,147,260) by design — add a reader note.
4. On the 9-of-9 reading MH-01 is also inside the capitalised labour count (+2,821 upside; already disclosed as I-41).
5. O7 (899) and I-05 burden (5,715) items carried from v9; on the 8-person base they move by well under $1k.
6. The in-book Logistics tab banner still says "rolls up to Production Operations" (unedited SD copy); cost is booked in CO per the user decision.
7. "0 changes in 2026 B:N" should be scoped to the six P&L sheets (HC-CO r18 inputs and HC-COO M:N change by design).
8. The tab was copied from the SD re-upload (cell-identical to the original).

Not verifiable: Excel engine; that the seat/roster name matches are the same real people (name+salary match; one title differs); the chat-sourced 110,000 / Jan-27 instruction (implemented as specified; whether the person is on 2026 payroll is unknown and disclosed).
