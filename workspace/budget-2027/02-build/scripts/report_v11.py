"""v11 notes (md) and Collation Notes (JSON for cnotes_v6.render): corrections pass on v10 (handoff 2026-10-10).

Usage:
  python3 -I report_v11.py V10_MD CN10_JSON V10_XLSX LO_VERSION_TXT HVALS_JSON OUT_NOTES_JSON OUT_MD [CHECKS_JSON]

- V10_MD / CN10_JSON: the v10 notes and the v10 Collation Notes (cnotes_v6.py extract, round trip byte-identical).
  Everything is carried verbatim except the six fixes of the v11 handoff; every edit is anchored on the exact v10 text
  and asserts exactly one occurrence, so the build stops if the v10 text is not what this script expects.
- HVALS_JSON ('-' = pass A): the LibreOffice-recalculated values of the new live check formulas (Collation Notes
  H78:H81), from hvals_v11.py. Pass A uses 0.0 placeholders (the stage build that LibreOffice then recalculates).
- CHECKS_JSON ('-' = before the checks): analyze_v11.py output; pass 2 fills the computed diff / recalc numbers into
  the md. The Collation Notes JSON NEVER depends on CHECKS_JSON, so pass 1 and pass 2 give byte-identical notes JSON.
- F1 root cause closed by construction: this script reads no file properties, no clock and no dates - only the v10 md,
  the v10 Collation Notes, the workbook bytes (sha256 + 6 cached figures) and the recalculated H values. Two runs on
  the same inputs are byte-identical (run_build_v11.sh builds twice and compares).
- No name is read or written; the added text quotes department totals only (no per-person amounts).
"""
import sys, os, json, hashlib, copy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

(V10MD, CN10, V10X, LOV, HVALS, OUTJ, OUTMD) = sys.argv[1:8]
CHECKS = sys.argv[8] if len(sys.argv) > 8 else "-"

md = open(V10MD, encoding="utf-8").read()
cn = json.load(open(CN10))
lov = open(LOV, encoding="utf-8").read().strip()
H = json.load(open(HVALS)) if HVALS != "-" else {"H78": 0.0, "H79": 0.0, "H80": 0.0, "H81": 0.0}
AN = json.load(open(CHECKS)) if CHECKS != "-" else None
V10SHA = hashlib.sha256(open(V10X, "rb").read()).hexdigest()

# ---- the six fixes, shared text -------------------------------------------------------------------------------
FALSE_SENT = "the SD book's properties show 2026-10-09 (a re-save, not the model date)"
FIX_SENT = ("the SD workbook carries no document properties, so its save date cannot be read from the file; "
            "the model's as-of date is unknown (v11 correction, full-sweep F1)")
HCCOO_NOTE = ("HC-COO is the unedited roster roll-up of the HC tabs - it still lists the material handler (PO HC r20) "
              "under PO and holds no logistics seats, so HC-COO's CO payroll (748,768) intentionally differs from the "
              "CO P&L 6610-6640 (1,147,260), which adds the Logistics&WH model less LOG-01 (user decision 2026-10-10).")
BANNER_NOTE = ("the in-book 'Logistics&WH Payroll' tab is an unedited copy of the SD model; its banner (A2) still says "
               "the payroll 'rolls up to Production Operations'. Superseded: the cost is booked in Central Operations "
               "(CO 6610-6640) per the user decision of 2026-10-10 (I-17 RESOLVED). The tab itself is deliberately not "
               "edited (it stays value-identical to the SD input).")
PREC_NOTE = ("the I-05 burden ((5,715)) and the O7 rate-base ((899)) items are computed on the 9-person current-staff "
             "base carried from v9. On the v10 8-person base (PO HC r20 in CO since v10) each moves by well under $1k "
             "- immaterial at this precision; the carried figures are kept.")
HF = {  # live check formulas (no leading '='; cnotes_v6.render adds none)
    "H78": "CO!AG67-'HC-CO'!Z67-('Logistics&WH Payroll'!S43-'Logistics&WH Payroll'!S34+'Logistics&WH Payroll'!S46)",
    "H79": "CO!AG68-'HC-CO'!Z68-('Logistics&WH Payroll'!S44-'Logistics&WH Payroll'!S34*'Logistics&WH Payroll'!$B$5)",
    "H80": "CO!AG69-'HC-CO'!Z69-('Logistics&WH Payroll'!S45-'Logistics&WH Payroll'!S34*'Logistics&WH Payroll'!$B$6)",
    "H81": "SUM(H78:H80)",
}


def sub1(text, old, new, where):
    n = text.count(old)
    assert n == 1, f"{where}: anchor found {n} times (expected 1): {old[:80]!r}"
    return text.replace(old, new)


# ---- workbook figures quoted by the added text (read, not typed) ----------------------------------------------
import openpyxl
wv = openpyxl.load_workbook(V10X, data_only=True)
ag132 = wv["COO P&L"]["AG132"].value
z70 = wv["HC-CO"]["Z70"].value
co_total = wv["CO"]["AG67"].value + wv["CO"]["AG68"].value + wv["CO"]["AG69"].value
assert round(ag132, 2) == 159136.40, ag132
assert round(z70) == 748768 and round(co_total) == 1147260, (z70, co_total)
assert f"{round(z70):,}" == "748,768" and f"{round(co_total):,}" == "1,147,260"  # the totals the reader note quotes

# ================================================================ Collation Notes JSON =========================
cn = copy.deepcopy(cn)
S = cn["sections"]
assert cn["title"] == "2027 COO Budget - Collation Notes (build v10, draft for review)"
cn["title"] = "2027 COO Budget - Collation Notes (build v11, draft for review)"

# geometry guard: section 4's table data rows must sit at sheet rows 78-81 (column H = col 8 = the check column),
# and nothing inserted at or above section 4 (the fixes below only edit text there), so H78:H81 keep their address.
r = 3
rows4 = None
for i, sec in enumerate(S):
    r += 1 + len(sec.get("lines", []))
    t = sec.get("table")
    if t:
        r += 1
        if i == 4:
            rows4 = list(range(r, r + len(t["rows"])))
        r += len(t["rows"]) + len(t.get("after", []))
    r += 1
assert rows4 == [78, 79, 80, 81], rows4

# fix 1 (F1): Issues I-38 evidence cell
t23 = S[23]["table"]
assert S[23]["heading"].startswith("Issues (v10)")
r38 = t23["rows"][37]
assert r38[0] == "I-38"
r38[4] = sub1(r38[4], FALSE_SENT, FIX_SENT, "CN I-38 evidence")

# fix 3 (H78:H81 live formulas) + a line note in section 4
t4 = S[4]["table"]
assert t4["header"][7] == "Check (must be 0)"
for k, key in enumerate(("H78", "H79", "H80", "H81")):
    old = t4["rows"][k][7]
    assert isinstance(old, float) and old == 0.0, (key, old)
    t4["rows"][k][7] = {"f": HF[key], "v": float(H[key])}
S[4]["lines"][0] += (" v11: the 'Check (must be 0)' column (H78:H81) holds live formulas (CO!AG67:AG69 less "
                     "'HC-CO'!Z67:Z69 less 'Logistics&WH Payroll' S43:S45 net of LOG-01 row 34, + S46 new-hire cost "
                     "on 6610; H81 = SUM(H78:H80)); previously static values. Cached values are the LibreOffice "
                     "recalculation of this workbook.")

# fix 6b (precision note, written INTO the two caveat rows so no row above H78:H81 shifts)
t3 = S[3]["table"]
assert t3["rows"][8][0] == "I-05 burden (O1), capitalised"
assert t3["rows"][9][0] == "Rate base of the current 9 (critic v8 O7)"
for k in (8, 9):
    t3["rows"][k][2] += (" v11 precision note: computed on the 9-person current-staff base carried from v9; on the "
                         "v10 8-person base (PO HC r20 in CO) it moves by well under $1k - immaterial; the carried "
                         "figure is kept.")

# fix 5 (banner pointer) + the AI33:AI35 status, in 'Workbook text superseded'
assert S[7]["heading"] == "Workbook text superseded by these notes"
S[7]["lines"][3] = sub1(S[7]["lines"][3],
                        "PO!AI33:AI35 (v8/v9 notes) were not edited (the v10 diff is confined to PO!U33:AF35 there); "
                        "the 5110-5140 base is now 'the v7 amount less PO HC r20'.",
                        "PO!AI33:AI35 (v8/v9 notes) were not edited in v10 (its diff is confined to PO!U33:AF35 "
                        "there); v11 updates AI33:AI35 to the v10 wording - B131 = 0 restores the v7 amount LESS "
                        "HC-PO r20, which moved to CO (user decision 2026-10-10). Text only; values unchanged.",
                        "CN superseded-text v10 line")
S[7]["lines"].append("v11: " + BANNER_NOTE)

# fix 6a (scope the B:N claim) + v11 base line, in 'Source and build'
assert S[8]["heading"] == "Source and build"
S[8]["lines"][0] = sub1(S[8]["lines"][0], "no 2026 column (B:N) of the P&L tabs changes.",
                        "no 2026 column (B:N) of the six P&L sheets (COO P&L, FO, PO, CO, FE, PE) changes - scoped in "
                        "v11: HC-CO r18's inputs/months (B18:E18, M18:N18) and the HC-COO roll-up's 2027 columns M:N "
                        "changed by design (2027/roster data, not 2026).", "CN source line B:N")
S[8]["lines"][1] = sub1(S[8]["lines"][1], "Full notes: 02-build/02-build_notes_v10.md.",
                        "Full notes: 02-build/02-build_notes_v11.md.", "CN full-notes pointer")
S[8]["lines"].append("v11 (corrections pass, handoff 2026-10-10): base = the v10 collated workbook; edits = this "
                     "sheet (regenerated) and PO!AI33:AI35 (text). 0 value changes on any other cell (every other "
                     "zip part is byte-identical); COO P&L!AG132 = 159,136.40, unchanged. See 'Changes from v10 "
                     "(v11)' below.")

# fix 4 (HC-COO reader note) in 'Payroll reconciliation'
assert S[19]["heading"].startswith("Payroll reconciliation (v10)")
S[19]["lines"].append("Reader note (v11): " + HCCOO_NOTE)

# the 'Changes from v10 (v11)' section, inserted after 'Source and build' (below row 81, so H78:H81 do not move)
S.insert(9, {
    "heading": "Changes from v10 (v11): corrections pass - six documentation fixes, no value changes (handoff 2026-10-10)",
    "lines": ["v11 fixes one false sentence (full-sweep F1) and five documentation items (v10 verifier notes 1-3 and "
              "5-7). No budget value changes: the v10 -> v11 diff is confined to this sheet (regenerated) and "
              "PO!AI33:AI35 (text); COO P&L!AG132 = 159,136.40 (cached value byte-identical to v10). Root cause of "
              "F1: the v7 report chain read the SD book's '.modified' document property; the file has no "
              "docProps/core.xml, so openpyxl returned the run time, and the sentence was carried v7 -> v10. "
              "report_v11.py reads no file properties, no clock and no dates, so the v11 build is not date-dependent. "
              "The workfile's 2026-10-07 save date is real and kept."],
    "table": {"header": ["#", "Fix", "Where"], "rows": [
        ["1", "F1 (false statement): the I-38 evidence no longer claims a save date read from the SD book's document "
              "properties (reported as a 2026-10-09 re-save in v7-v10) - the SD workbook carries no document "
              "properties, so its save date cannot be read from the file; the model's as-of date is unknown.",
         "Issues I-38 (Evidence); md I-38 row"],
        ["2", "PO!AI33:AI35 notes updated: B131 = 0 restores the v7 amount LESS HC-PO r20, which moved to CO (user "
              "decision 2026-10-10); 5110-5140 B131 base 652,820 -> 590,318. Text only; the cells' values and the "
              "U:AF formulas are unchanged.", "PO!AI33:AI35"],
        ["3", "The 'Check (must be 0)' cells are live formulas computing the check from the workbook (previously "
              "static values); cached values = LibreOffice recalculation.", "This sheet, H78:H81"],
        ["4", "Reader note: " + HCCOO_NOTE, "'Payroll reconciliation' lines; md"],
        ["5", "Pointer: " + BANNER_NOTE, "'Workbook text superseded' lines; md"],
        ["6", "Precision wording: the '0 changes in 2026 B:N' claim is scoped to the six P&L sheets (HC-CO r18 "
              "inputs/months and HC-COO M:N changed by design), and " + PREC_NOTE,
         "'Source and build' line; caveat rows (sheet rows 45-46); md"],
    ], "after": []},
})

json.dump(cn, open(OUTJ, "w"), indent=1, ensure_ascii=False)

# ================================================================ md ===========================================
# fix 1 (F1)
md = sub1(md, FALSE_SENT, FIX_SENT, "md I-38 evidence")

# title
md = sub1(md, "# 02-build notes v10 - 2027 COO budget collation",
          "# 02-build notes v11 - 2027 COO budget collation (corrections pass on v10; figures unchanged)", "md title")

# fix 6b: pointers in the two caveat rows + note (b) under the table
md = sub1(md, "Carried from v9: Prod Payroll and the labour block unchanged. | (5,715)",
          "Carried from v9: Prod Payroll and the labour block unchanged. 9-person base; see note (b) below the table. "
          "| (5,715)", "md I-05 burden row")
md = sub1(md, "Carried from v9: Prod Payroll and PO HC rates unchanged (the model still costs 9 current staff). | (899)",
          "Carried from v9: Prod Payroll and PO HC rates unchanged (the model still costs 9 current staff). 9-person "
          "base; see note (b) below the table. | (899)", "md O7 row")
md = sub1(md, "\n\n**Sign-flip statement (computed, v10):",
          "\n\n(b) Precision note (v11): " + PREC_NOTE + "\n\n**Sign-flip statement (computed, v10):", "md note (b)")

# fix 5 (banner pointer), before the New-hire paragraph of the Logistics section
md = sub1(md, "\n\n**New-hire cost.**",
          "\n\n**Tab banner (v11).** The" + BANNER_NOTE[3:] + "\n\n**New-hire cost.**", "md banner note")

# fix 3: note under the md check table (the sheet counterpart H78:H81 is now live)
md = sub1(md, "The HC-CO roster's 5 existing people equal the v9 typed values in every month (the old constants were "
          "HC-CO rows 67-69).",
          "The HC-CO roster's 5 existing people equal the v9 typed values in every month (the old constants were "
          "HC-CO rows 67-69). v11: on the Collation Notes sheet the 'Check (must be 0)' cells (H78:H81) are live "
          "formulas (CO!AG67:AG69 less 'HC-CO'!Z67:Z69 less 'Logistics&WH Payroll' S43:S45 net of LOG-01 row 34, + "
          "S46 new-hire cost on 6610; H81 = SUM(H78:H80)); the 0.00s here are their recalculated values.",
          "md check-table note")

# fix 4 (HC-COO reader note), before the 9-vs-7 paragraph
md = sub1(md, "\n\n**9 by count vs 7 by role (I-41), updated.**",
          "\n\n**Reader note (v11).** " + HCCOO_NOTE + "\n\n**9 by count vs 7 by role (I-41), updated.**",
          "md HC-COO note")

# fix 6a (scope the 2026 B:N claim)
md = sub1(md, "2026 columns (B:N) of COO P&L / FO / PO / CO / FE / PE: 0 changes.",
          "2026 columns (B:N): 0 changes on the six P&L sheets (COO P&L, FO, PO, CO, FE, PE) - the sheets where B:N "
          "are the 2026 columns; HC-CO r18's inputs/months (B18:E18, M18:N18) and the HC-COO roll-up's 2027 columns "
          "M:N changed by design (2027/roster data, not 2026; v11 scope note).", "md diff B:N")
md = sub1(md, "| Diff confined (v9 -> v10) | outside the allowed areas 0; 2026 columns 0; HC-COO roll-up reported separately |",
          "| Diff confined (v9 -> v10) | outside the allowed areas 0; 2026 columns (B:N) of the six P&L sheets 0 "
          "(HC-CO r18 inputs/months and HC-COO M:N changed by design - 2027/roster data; v11 scope note); HC-COO "
          "roll-up reported separately |", "md criteria B:N")

# fix 2 is in the workbook (build_v11.py); the md 'Not done' bullet about it is resolved, the banner limit recorded
md = sub1(md, "- PO!AI33:AI35 still describe the v8/v9 formula ('the v7 amount'); the v10 base (less PO HC r20) is "
          "described here and on Collation Notes.",
          "- (resolved in v11) PO!AI33:AI35 now describe the v10 base: B131 = 0 restores the v7 amount LESS HC-PO "
          "r20, which moved to CO (user decision 2026-10-10). Still not done: the 'Logistics&WH Payroll' tab banner "
          "(A2) keeps its SD text ('rolls up to Production Operations') - the tab is an unedited SD copy by design; "
          "the pointer note (fix 5) supersedes it.", "md not-done bullet")

# ---- Changes from v10 section (before 'Changes from v9') ------------------------------------------------------
if AN:
    an_diff = (f"diff_versions.py v10 -> v11, every cell of the 6 P&L tabs and every driver / HC tab (Collation Notes "
               f"excluded; it is regenerated): {AN['diff_total']['cells']:,} cells; {AN['diff_total']['formula_diffs']} "
               f"formula and {AN['diff_total']['value_diffs']} value differences, all of them the 3 text cells "
               f"PO!AI33:AI35 (a text cell counts on both sides of that comparator); every other sheet 0 and 0; "
               f"comments added / removed / changed [0, 0, 0]; sheet set unchanged.")
    an_parts = (f"Package parts changed vs v10: {', '.join(AN['parts_changed'])} (the Collation Notes and PO parts); "
                f"parts added or removed: none. Every other part is byte-identical, so every value on every other "
                f"sheet is unchanged at the byte level, including COO P&L!AG132 = 159,136.40 (cached "
                f"{AN['ag132']['v11']:,.6f}, identical to v10).")
    an_recalc = (f"LibreOffice recalculation of the v11 file: error cells 0 (new errors 0). Stored values vs the "
                 f"recalculation: every sheet except Collation Notes max difference {AN['recalc']['max']:.1e} over "
                 f"{AN['recalc']['cells']:,} numeric cells, non-numeric differences 0; Collation Notes live formulas "
                 f"({AN['cn']['formulas']}, incl. H78:H81) max difference {AN['cn']['max']:.1e}. H78:H81 recalculated "
                 f"check values: max |check| = {AN['cn']['h_max']:.1e} (must be 0; it is, to float noise). COO P&L = "
                 f"FO + PO + CO + FE + PE on every dept-sum row: max difference {AN['sum_depts']['max']:.1e} over "
                 f"{AN['sum_depts']['rows']} rows; check row 133 max {AN['sum_depts']['row133']:.1e}.")
    an_text = (f"False sentence occurrences after the fix: md 0, workbook 0 (replacement present in both); the "
               f"workfile's 2026-10-07 date is kept. privacy_v6 hits 0; paylist exact per-person hits 0.")
else:
    an_diff = an_parts = an_recalc = an_text = "(computed in pass 2 of report_v11.py; this is the pass-1 draft)"

changes = f"""## Changes from v10 (v11)

Handoff 2026-10-10 (orchestrator; all rulings final): a corrections pass fixing one false sentence found by the full
v1-v9 verification sweep (F1) and five documentation items from the v10 verifier (notes 1-3 and 5-7). **No budget
value changes: the only cells that differ from v10 are the regenerated Collation Notes sheet and the three note-text
cells PO!AI33:AI35; the 2027 COO contribution (COO P&L!AG132) is unchanged at 159,136.40.** Every v10 section below
stands; where it describes the v10 build (diff, error scan, completion criteria), it still describes the v10 build.

| # | Fix | Where |
|---|---|---|
| 1 | F1 (false statement). The I-38 evidence claimed a save date read from the SD book's document properties (reported in v7-v10 as a 2026-10-09 re-save). False: the SD workbook carries no document properties (no docProps/core.xml), so its save date cannot be read from the file; the model's as-of date is unknown. The workfile's 2026-10-07 date is real and kept. | I-38 row (Evidence) in this file and on Collation Notes |
| 2 | PO!AI33:AI35 stale text. The notes now say: B131 = 0 restores the v7 amount LESS HC-PO r20, which moved to CO (user decision 2026-10-10); 5110-5140 B131 base 652,820 -> 590,318. Notes column only; no values changed. | PO!AI33:AI35 (text cells) |
| 3 | Collation Notes H78:H81. The 'Check (must be 0)' cells are now live formulas computing the check from the workbook: CO!AG67:AG69 less 'HC-CO'!Z67:Z69 less the Logistics&WH model (S43:S45 net of LOG-01 row 34, + S46 new-hire cost on 6610); H81 = SUM(H78:H80). Cached values = LibreOffice recalculation. | Collation Notes H78:H81 |
| 4 | Reader note for HC-COO: {HCCOO_NOTE} | 'Payroll reconciliation' section; Collation Notes |
| 5 | Logistics tab banner pointer: {BANNER_NOTE} | 'Logistics & Warehouse payroll' section; Collation Notes 'Workbook text superseded' |
| 6 | Precision wording. The '0 changes in 2026 B:N' claim is scoped to the six P&L sheets, noting HC-CO r18 inputs/months and HC-COO M:N changed by design; and note (b) marks that {PREC_NOTE} | diff / criteria wording; note (b) under the caveats table; Collation Notes |

**F1 root cause (fixed in the build chain):** the v7 report chain read the SD book's `.modified` document property
with openpyxl; the file has no `docProps/core.xml`, so openpyxl returned the run time, and the false sentence was then
carried verbatim v7 -> v10. `report_v11.py` reads no file properties, no clock and no dates - the v11 md and Collation
Notes derive only from the v10 md, the v10 Collation Notes, the workbook bytes and the LibreOffice-recalculated check
values, so the build is no longer date-dependent (run_build_v11.sh builds twice and requires byte-identical outputs).

### v10 -> v11 diff and checks (v11, computed)

- {an_diff}
- {an_parts}
- {an_recalc}
- {an_text}

### Completion criteria (v11)

| Criterion | Result |
|---|---|
| All six items addressed | fixes 1-6 above, applied to the md, the Collation Notes sheet and PO!AI33:AI35; presence asserted by analyze_v11.py |
| 0 value changes outside Collation Notes | the diff and the byte-identical parts above; the 3 changed PO cells are the AI33:AI35 note texts (allowed area, text only) |
| AG132 unchanged | 159,136.40 (cached value byte-identical to v10) |
| False sentence gone from md and workbook | 0 occurrences after the fix; replacement wording present in both |
| 0 new errors | LibreOffice recalculation of v11: error cells 0 |
| Two-pass build byte-identical | run_build_v11.sh runs the full pipeline twice and `cmp`s both xlsx and md |

"""
md = sub1(md, "## Changes from v9\n", changes + "## Changes from v9\n", "md changes section")

# ---- Build and sources ----------------------------------------------------------------------------------------
md = sub1(md, "Output: `02-build/02-build_COO_2027_Budget_Collated_v10.xlsx` and this file (v1-v9 files unchanged; no v10 CSV).  ",
          "Output: `02-build/02-build_COO_2027_Budget_Collated_v11.xlsx` and this file (v1-v10 files unchanged; no "
          "v11 CSV).  ", "md output line")
md = sub1(md, "Scripts: `02-build/scripts/` - v10 entry point",
          "Scripts: `02-build/scripts/` - v11 entry point `run_build_v11.sh` (runs the whole pipeline twice; both "
          "passes must be byte-identical): cnotes_v6.py extract of the v10 Collation Notes (round trip "
          "byte-identical) -> report_v11.py pass 1 (the six fixes; reads no file properties) -> build_v11.py "
          "(package patch of v10: Collation Notes regenerated + PO!AI33:AI35 text; every other zip part copied byte "
          "for byte) -> recalc.sh (full LibreOffice recalculation) -> hvals_v11.py (H78:H81 cached values from the "
          "recalculation; stops if any other cell moves > 1e-6 or any error cell appears) -> build_v11.py final -> "
          "diff_versions.py v10 -> v11, recalc.sh on the final file, analyze_v11.py (exit 1 on any failed criterion) "
          "-> recon_v11.py + names_v11.py + privacy_v6.py + paylist_v10.py (names and per-person amounts; scratch "
          "name list outside the repo, deleted) -> report_v11.py pass 2 (Collation Notes JSON must equal pass 1; "
          "writes this md). v10 entry point", "md scripts line")
md = sub1(md, "Base: v9 workbook sha256 `40e763a1db6b8fdc46b9bc47745cc4a6c661f86f42f319140219e8e156b7f081`. "
          "LibreOffice: LibreOffice 24.2.7.2 420(Build:2). Python run with -I. The new CO employee's name is read "
          "from a file outside the repository (run_build_v10.sh argument), never from the scripts.",
          f"Base: v10 workbook sha256 `{V10SHA}` (v10's base: v9 sha256 "
          "`40e763a1db6b8fdc46b9bc47745cc4a6c661f86f42f319140219e8e156b7f081`). "
          f"LibreOffice: {lov}. Python run with -I. v11 needs no name file (it edits no roster cell); the privacy "
          "scan reads the roster names from the workbook into a scratch list outside the repository, deleted after "
          "the build (v10: the new CO employee's name was read from a file outside the repository, never from the "
          "scripts).", "md base line")

# ---- Decisions (v11) ------------------------------------------------------------------------------------------
decisions = """## Decisions (v11, builder)

- D1 (v11): Corrections-pass method - package patch of v10 (the v4/v5 method): only the Collation Notes part is
  regenerated and the three PO!AI33:AI35 text cells replaced; every other zip part is copied byte for byte, so '0
  value changes elsewhere' holds at the byte level and is also verified cell by cell (diff_versions.py).
- D2 (v11): H78:H81 as live formulas (the handoff's preferred option): CO!AG67:AG69 - 'HC-CO'!Z67:Z69 - ('Logistics&WH
  Payroll' S43:S45 less row 34 burdened at B5/B6, + S46 new-hire cost on 6610); H81 = SUM(H78:H80). Cached values are
  taken from a full LibreOffice recalculation of the patched package, so stored values = recalculation by
  construction.
- D3 (v11): F1 root cause closed by construction: report_v11.py reads no file properties, no clock and no dates (the
  v7 chain's figures script read `.modified` on a file with no docProps/core.xml and got the run time). The v11 build
  is therefore not date-dependent; run_build_v11.sh builds twice and requires byte-identical outputs.
- D4 (v11): On the Collation Notes sheet the precision footnote (fix 6) is written into the two caveat rows (I-05
  burden, O7) rather than added as a new footnote row: a new row above the check table would shift it and the handoff
  names the check cells by address (H78:H81). The md carries a proper note (b) under its caveats table. All v11
  section/line additions on the sheet sit below row 81 for the same reason.
- D5 (v11): The HC-COO reader note quotes 748,768 ('HC-CO'!Z70, the roster total) and 1,147,260 (CO!AG67:AG69) -
  department totals, not per-person amounts, so the $5k rounding rule is not triggered; both figures are read from
  the workbook by report_v11.py, not typed.
- D6 (v11): The stale 'Not done' bullet on PO!AI33:AI35 is replaced (the item is done in v11); the unedited tab
  banner is recorded in its place as the remaining (intentional) limit. All other v10 sections are carried verbatim:
  they describe the v10 build, whose figures v11 does not change.

"""
md = sub1(md, "## Not done / limits\n", decisions + "## Not done / limits\n", "md decisions section")

open(OUTMD, "w", encoding="utf-8").write(md)
nform = sum(1 for sec in cn["sections"] for row in (sec.get("table", {}) or {}).get("rows", [])
            for v in row if isinstance(v, dict))
print(f"report_v11: notes JSON {len(cn['sections'])} sections, {nform} formula cells (H values "
      f"{'from ' + HVALS if HVALS != '-' else 'placeholder 0.0'}); md {len(md.splitlines())} lines "
      f"({'pass 2, checks filled' if AN else 'pass 1 draft'})")
