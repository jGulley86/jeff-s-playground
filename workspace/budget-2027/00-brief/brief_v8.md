# Brief v8 — ingest user HC edits (v14 build, on top of v12+v13)
New input: `00-brief/inputs/USER_EDIT_FINAL_v4_HC.xlsx` — the user's copy of FINAL_v4, edited and saved in Microsoft Excel (Mac). Excel "repair" stripped the patched formulas there (PO 33–35 etc. show #REF!), so it is an EDIT SOURCE only, never a base. Lift the user's edits; apply to the clean v12/v13 chain.

## User edits found (orchestrator diff, titles only)
- HC-CO: r18 title set to "Facilities Manager" (the 110k employee); ADD Material Handler 49,920 Sep-26 (moved from HC-PO r20); ADD MH Team Lead 57,554 Sep-26; ADD Material Flow Supervisor 85,000 Nov-26 (r35); ADD Applications Engineer 85,000 Nov-26 (r36). New roster 2027 salary 860,846.
- HC-PO: Material Handler row removed (moved to CO); ADD Production Manager 125,000 Oct-26. Roster 2027 salary 600,954; totals shifted to r66 (row structure edited).
- HC-FE: ADD Associate Field Robotics Engineer 75,000 Sep-26 (= the Fld Eng Budget r15 person; the I-28 duplicate).
- HC-PE: ADD Purchasing Analyst 85,000 Jan-27; Launch Planner 75,000 Nov-26; Quality Engineer 100,000 Dec-26; Manufacturing Engineer 110,000 Dec-26; Strategic Sourcing Lead 120,000 Oct-26. Roster 2027 salary 1,571,695 (+493,675).
- CO U98/U106 blocks: user typed 2,000/6,500 monthly constants (= brief_v7 request; v13 implements natively; do NOT copy the constants).
- Other sheet diffs in their file are Excel re-save artifacts or #REF! damage; ignore.

## Open user decisions (asked 2026-10-12; do not build v14's ambiguous parts without answers)
1. Wire PE 6610–6640 to HC-PE roster totals (like CO)? Recommended yes.
2. CO MH + TL: keep on roster and exclude logistics seats MH-01 + TL-01 from the CO logistics add-on (extend the LOG-01 exclusion)? Recommended yes.
3. PO Production Manager: expense to PO 6610 (recommended) or capitalise into production labour (supervisor double-count risk vs the model ratio)?
4. Remove the FE Associate from FO's current-staff count (+78,529), resolving I-28? Recommended yes.

## v14 scope (once answered)
- Re-apply the roster edits to the clean base by VALUE-EQUIVALENT insertion (keep our sheet structure; do not import Excel-shifted rows wholesale). HC-PO r20 subtraction in PO 5110–5140 must be re-anchored after the MH move (base stays 590,317.51).
- Apply decisions 1–4; recompute HC-COO roll-up; full engine save (v12 technique); diff confined; standard suite; verifier.

## User answers (2026-10-12) — build decisions
1. YES: wire PE 6610–6640 to HC-PE roster totals (PE HC rates D6/D7, 3% Oct-27 raise mechanics as on the tab).
2. "We are backfilling Servando, so the Material Flow Supervisor should be included."
   Orchestrator interpretation (state in notes; one formula term to flip if wrong): the MFS hire (85k, Nov-26, HC-CO r35) IS the realized backfill that the logistics model carries as seat MH-02 "Material Handler (backfill for Servando…)". Therefore:
   - keep ALL user roster adds on HC-CO (MH, TL, MFS, AppEng) — they flow via HC-CO totals;
   - the CO logistics add-on now excludes, by formula, the seats realized on the roster: LOG-01 (already), MH-01, TL-01, and MH-02;
   - seats still added from the model: INV-01, MH-03, MH-04, TL-02, MH-06 (+ their new-hire costs; MH-02's 2026 hire cost does not touch 2027 — verify).
3. PO Production Manager (125k, Oct-26): EXPENSE to PO 6610–6640 at PO HC rates. He must NOT enter the capitalised labour base. PO 5110–5140 B131 base stays the 8 production staff = 590,317.51/yr (MH moved to CO): rewrite the formulas off the embedded-constants-minus-r20 form onto a live 8-person basis that survives the roster edit; HC-PO gets the PM row added and the MH row removed, totals back at rows 67–70 (our structure, not the user's shifted rows).
4. YES: Fld Ops Payroll B11 14 → 13 (FE Associate out of FO's count; +78,529 incl. the 5330 knock-on). He stays in Fld Eng Budget and on HC-FE. He remains listed on HC-FO (roster snapshot; feeds nothing) — add a reader note, I-28 → RESOLVED.

## Build packaging
v13 (single build, on top of v12) = brief_v7 (CO!S98=24000, S106=78000) + this brief. Then verifier, critic sanity on the CO de-dup logic, final package v5.
