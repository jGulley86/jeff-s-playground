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
