"""v13 build: brief_v7 (CO 7700/8600 inputs) + brief_v8 as amended (user HC roster merge, decisions 1-4), on v12.

Stage 1 (cell edits, openpyxl; the deliverable is produced later by ONE full LibreOffice recalc + engine save of the
stage-2 file, so no package patching of saved parts is involved):
  A. CO!S98 = 24000, CO!S106 = 78000 (R stays 'Even' -> U:AF = S/12).
  B. Roster edits re-applied into OUR sheet structure (names copied from the user's file at run time; they are never
     written to any script, JSON, md or stdout):
       HC-CO: C18 title 'Facilities Manager'; r19 Material Handler 49,920 Sep-26 (= MH-01, moved from HC-PO r20);
              r20 Material Handling Team Lead 57,554 Sep-26 END-DATED Nov-26 (the user's F20 value - their file ends
              the row in 2026, so its 2027 cost is 0); r35 Material Flow Supervisor 85,000 Nov-26;
              r36 Applications Engineer 85,000 Nov-26 (open positions, no names in the user's file).
       HC-PO: r20 blanked (B/C/D cleared; E/F/G/H keep the template's empty-row prefills);
              r41 Production Manager 125,000 Oct-26 (New Hires block = the user's r40 after their row deletion).
       HC-FE: r20 Associate Field Robotics Engineer 75,000 Sep-26 (the Fld Eng Budget r15 person, I-28).
       HC-PE: r35 Purchasing Analyst 85,000 Jan-27; r36 Launch Planner 75,000 Nov-26; r37 Quality Engineer 100,000
              Dec-26; r38 Manufacturing Engineer 110,000 Dec-26; r41 Strategic Sourcing Lead 120,000 Oct-26.
  C. Decision 1: PE!U67:AF69 typed constants -> live links 'HC-PE'!M67:X69 (+ AI notes).
  D. Decision 2: CO!U67:AF69 logistics add-on excludes BY FORMULA the roster-realized seats: LOG-01 (row 34, already),
     TL-01 (row 36), MH-01 (row 38), MH-02 (row 39); + AI notes. Collation Notes H78:H80 check formulas extended the
     same way (H81 = SUM unchanged).
  E. Decision 3: PO!U67:AF69 = the Production Manager as live links to 'HC-PO'!M41:X41 x (1, D6, D7) (+ AI notes).
     He is NOT in the capitalised labour base.
  F. Decision 4: Fld Ops Payroll!B11 = 13 (I-28 resolved; FE Associate out of FO's tech count).
  G. PO!U33:AF35 re-anchored: (1 - B131) x SUM('HC-PO'!M14:M33) x (1, D6, D7) + the idle rows 226-228. The current-
     employee block (rows 14-33) is the live 8-production-staff basis; the PM (r41, New Hires) is outside it by
     construction. B131 = 0 base unchanged at 590,317.51/yr. (+ AI33:AI35 notes.)

Stage 2 (Collation Notes text/number updates, applied after the stage-1 file has been fully recalculated and measured
by figures_v13.py): in-place updates of the stale current-state cells + the v13 block appended below row 810.

Usage:
  python3 -I build_v13.py stage1 V12_XLSX USER_XLSX OUT_XLSX OUT_SPEC_JSON
  python3 -I build_v13.py stage2 STAGE1_XLSX FIGURES_JSON OUT_XLSX
No clock, no file properties, no dates are read (F1 rule).
"""
import sys, json, datetime, os, zipfile
import openpyxl
from openpyxl.utils import get_column_letter


def pin_coreprops(ref_xlsx, out_xlsx):
    """openpyxl force-stamps docProps/core.xml 'modified' with the wall clock at save (openpyxl.writer.excel), which
    would make the build date-dependent (F1 rule) and the two passes differ. Replace the script-written
    INTERMEDIATE's core.xml with the reference file's bytes (zip-level, fixed entry date). The deliverable itself is
    the later LibreOffice engine save, which carries docProps unchanged (v12-proven), so the shipped docProps stay
    v12's - no XML is spliced into any engine-saved part."""
    core = zipfile.ZipFile(ref_xlsx).read("docProps/core.xml")
    tmp = out_xlsx + ".tmp"
    with zipfile.ZipFile(out_xlsx) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for info in zi.infolist():
            if info.filename == "docProps/core.xml":
                zo.writestr(zipfile.ZipInfo("docProps/core.xml", date_time=(1980, 1, 1, 0, 0, 0)), core)
            else:
                zo.writestr(info, zi.read(info.filename))
    os.replace(tmp, out_xlsx)

LW = "'Logistics&WH Payroll'"
P27 = [get_column_letter(c) for c in range(21, 33)]    # U..AF  P&L 2027 months
H27 = [get_column_letter(c) for c in range(13, 25)]    # M..X   HC 2027 months
L27 = [get_column_letter(c) for c in range(6, 18)]     # F..Q   Logistics / Depreciation 2027 months
D = datetime.datetime


def money(x, dp=0):
    s = f"{abs(x):,.{dp}f}"
    return f"({s})" if x < -0.004 else s


# ----------------------------------------------------------------------------------------------- stage 1
# roster edits: (our sheet, our row) -> (user sheet, user row with the name or None, title, salary, start, end)
ROSTER = [
    ("HC-CO", 18, ("HC-CO", 18), "Facilities Manager",            None,   None,            None),  # title only
    ("HC-CO", 19, ("HC-CO", 19), "Material Handler",              49920,  D(2026, 9, 1),   None),
    ("HC-CO", 20, ("HC-CO", 20), "Material Handling Team Lead",   57554,  D(2026, 9, 1),   D(2026, 11, 1)),
    ("HC-CO", 35, None,          "Material Flow Supervisor",      85000,  D(2026, 11, 1),  None),
    ("HC-CO", 36, None,          "Applications Engineer",         85000,  D(2026, 11, 1),  None),
    ("HC-PO", 41, ("HC-PO", 40), "Production Manager",            125000, D(2026, 10, 1),  None),
    ("HC-FE", 20, ("HC-FE", 20), "Associate Field Robotics Engineer", 75000, D(2026, 9, 1), None),
    ("HC-PE", 35, None,          "Purchasing Analyst",            85000,  D(2027, 1, 1),   None),
    ("HC-PE", 36, None,          "Launch Planner",                75000,  D(2026, 11, 1),  None),
    ("HC-PE", 37, None,          "Quality Engineer",              100000, D(2026, 12, 1),  None),
    ("HC-PE", 38, None,          "Manufacturing Engineer",        110000, D(2026, 12, 1),  None),
    ("HC-PE", 41, ("HC-PE", 41), "Strategic Sourcing Lead",       120000, D(2026, 10, 1),  None),
]

AI_PO_5100 = ("v8: {gl} 2027 = 0, CAPITALISED (production labour capitalised, user-confirmed 2026-10-10); the labour "
              "reaches the P&L as 5011/5012 depreciation via 'Depreciation Schedule' sections 8-9. v9: + 'Depreciation "
              "Schedule' row {idle} (idle-month labour expensed to this GL when B135 = 0; 0 while B135 = 1, booked). "
              "v13 (user roster edits 2026-10-12): the B131 = 0 base is live = SUM('HC-PO' current-employee rows, "
              "M14:M33){rate} - the 8 production staff left after the Material Handler moved to CO (v10 decision; "
              "'HC-PO' r20 blanked in v13, replacing the embedded-constant-less-r20 form, which the user's in-Excel "
              "row deletion had severed). The Production Manager (HC-PO r41, New Hires) is NOT in this base; he is "
              "expensed in PO 6610-6640 (user decision 3, 2026-10-12). B131 = 0 base unchanged: 590,318/yr "
              "(5110 475,016 + 5130/5140 at D6/D7).")
AI_PO_66 = {
    67: "v13 (user decision 3, 2026-10-12): 6610 2027 = the Production Manager (125,000/yr, Oct-26 start, 'HC-PO' "
        "row 41, New Hires block), live link = 'HC-PO'!M41:X41; 3% raise from Oct-27 per the roster row (G41/H41). "
        "EXPENSED here; not in the capitalised production-labour base (PO 5110-5140 formulas and the Prod Payroll "
        "model do not include him). 2026 columns untouched (his Oct-Dec 26 cost is on the HC tab only).",
    68: "v13: 6630 2027 = 'HC-PO'!M41:X41 x D6 (PO HC payroll-tax rate, 3.637%).",
    69: "v13: 6640 2027 = 'HC-PO'!M41:X41 x D7 (PO HC benefits rate, 20.636%).",
}
AI_CO_66 = {
    67: "v10: 6610 2027 = 'HC-CO' row 67 (CO HC roster) + 'Logistics&WH Payroll' salaries (row 43) less excluded "
        "seats + the model's new-hire cost (row 46). v13 (user decisions 2026-10-12): excluded by formula, as "
        "realized on the HC-CO roster: LOG-01 (row 34, = HC-CO r17, since v10), MH-01 (row 38, = HC-CO r19 Material "
        "Handler, moved from HC-PO r20), TL-01 (row 36, = HC-CO r20 Material Handling Team Lead - end-dated Nov-26 "
        "in the user's file, so its 2027 roster cost is 0; see I-41), MH-02 (row 39, the backfill seat realized by "
        "the Material Flow Supervisor, HC-CO r35, user-confirmed). Seats still added from the model: INV-01, MH-03, "
        "MH-04, TL-02, MH-06 + their 5,000 of 2027 new-hire cost (the TL-01/MH-02 hire costs fall in Dec-26/Oct-26 "
        "and are not in 2027). The v13 roster adds flow through 'HC-CO' rows 67-69 at CO HC rates.",
    68: "v13: 6630 2027 = 'HC-CO' row 68 (CO HC rate D6) + 'Logistics&WH Payroll' row 44 less (rows 34 + 36 + 38 + "
        "39) x B5 (model rate 6.8%).",
    69: "v13: 6640 2027 = 'HC-CO' row 69 (CO HC rate D7) + 'Logistics&WH Payroll' row 45 less (rows 34 + 36 + 38 + "
        "39) x B6 (model rate 16.4%).",
}
AI_PE_66 = {
    67: "v13 (user decision 1, 2026-10-12): 6610 2027 = 'HC-PE' row 67, live link (replaces the typed constants; "
        "same pattern CO used pre-v10), incl. the five user-added hires of 2026-10-12: Purchasing Analyst 85,000 "
        "Jan-27 (r35), Launch Planner 75,000 Nov-26 (r36), Quality Engineer 100,000 Dec-26 (r37), Manufacturing "
        "Engineer 110,000 Dec-26 (r38), Strategic Sourcing Lead 120,000 Oct-26 (r41). 2026 columns untouched.",
    68: "v13: 6630 2027 = 'HC-PE' row 68 (PE HC payroll-tax rate D6, 3.571%; I-37 flags it as below 7.65% FICA).",
    69: "v13: 6640 2027 = 'HC-PE' row 69 (PE HC benefits rate D7, 8.823%).",
}


def lw_terms(c, kind):
    """CO 2027 formula for logistics month column c (F..Q): kind in ('sal','tax','ben')."""
    if kind == "sal":
        return f"{LW}!{c}43-{LW}!{c}34-{LW}!{c}36-{LW}!{c}38-{LW}!{c}39+{LW}!{c}46"
    row, rate = ("44", "$B$5") if kind == "tax" else ("45", "$B$6")
    return f"{LW}!{c}{row}-({LW}!{c}34+{LW}!{c}36+{LW}!{c}38+{LW}!{c}39)*{LW}!{rate}"


def stage1(v12_path, user_path, out_path, spec_path):
    wb = openpyxl.load_workbook(v12_path)
    uw = openpyxl.load_workbook(user_path, data_only=False)
    spec = []

    def setc(sheet, coord, value, kind, fmt_from=None):
        ws = wb[sheet]
        old = ws[coord].value
        ws[coord] = value
        if fmt_from is not None and ws[coord].number_format == "General":
            ws[coord].number_format = ws[fmt_from].number_format
        spec.append({"sheet": sheet, "cell": coord, "kind": kind,
                     "old": "<name>" if kind == "name" and old not in (None, "") else
                            (str(old)[:200] if old is not None else None),
                     "new": "<name from user file>" if kind == "name" else str(value)[:300]})

    # --- A. CO 7700 / 8600 inputs
    setc("CO", "S98", 24000, "input")
    setc("CO", "S106", 78000, "input")

    # --- B. roster edits (names read from the user's file only; asserted against the brief's titles/amounts)
    for sheet, row, src, title, salary, start, end in ROSTER:
        ws = wb[sheet]
        if src is not None:
            usheet, urow = src
            uname = uw[usheet].cell(row=urow, column=2).value
            assert isinstance(uname, str) and uname.strip(), f"user file {usheet} r{urow}: no name"
            ucell = uw[usheet].cell(row=urow, column=3).value
            assert ucell == title, f"user file {usheet} r{urow}: title {ucell!r} != {title!r}"
            setc(sheet, f"B{row}", uname.strip(), "name")
        if sheet == "HC-CO" and row == 18:   # title-only edit
            setc(sheet, "C18", title, "title")
            continue
        usheet, urow = src if src is not None else (sheet, row)   # open-seat rows sit at the same address
        assert uw[usheet].cell(row=urow, column=3).value == title, f"user title mismatch {sheet} r{row}"
        assert uw[usheet].cell(row=urow, column=4).value == salary, f"user salary mismatch {sheet} r{row}"
        assert uw[usheet].cell(row=urow, column=5).value == start, f"user start mismatch {sheet} r{row}"
        setc(sheet, f"C{row}", title, "title", fmt_from=f"C14")
        setc(sheet, f"D{row}", salary, "salary", fmt_from=f"D14")
        if ws[f"E{row}"].value != start:
            setc(sheet, f"E{row}", start, "start", fmt_from=f"E14")
        if end is not None:   # the user's end month (HC-CO r20: Nov-26; their file's value, disclosed)
            setc(sheet, f"F{row}", end, "end", fmt_from=f"F14")
    # user's HC-CO r20 end month must really be Nov-26 (the one roster detail taken from their file beyond the brief)
    assert uw["HC-CO"]["F20"].value == D(2026, 11, 1), "user HC-CO F20 expected Nov-26"
    # blank HC-PO r20 (Material Handler -> CO); E/F/G/H keep the template's empty-row prefills
    for col in ("B", "C", "D"):
        setc("HC-PO", f"{col}20", None, "blank")

    # --- C. PE 6610-6640 live links
    for i, (pc, hc) in enumerate(zip(P27, H27)):
        for r in (67, 68, 69):
            setc("PE", f"{pc}{r}", f"='HC-PE'!{hc}{r}", "formula")
    for r, txt in AI_PE_66.items():
        setc("PE", f"AI{r}", txt, "note")

    # --- D. CO 6610-6640 de-dup formulas
    for pc, hc, lc in zip(P27, H27, L27):
        setc("CO", f"{pc}67", f"='HC-CO'!{hc}67+{lw_terms(lc, 'sal')}", "formula")
        setc("CO", f"{pc}68", f"='HC-CO'!{hc}68+{lw_terms(lc, 'tax')}", "formula")
        setc("CO", f"{pc}69", f"='HC-CO'!{hc}69+{lw_terms(lc, 'ben')}", "formula")
    for r, txt in AI_CO_66.items():
        setc("CO", f"AI{r}", txt, "note")

    # --- E. PO 6610-6640 = Production Manager (live links to his roster row)
    for pc, hc in zip(P27, H27):
        setc("PO", f"{pc}67", f"='HC-PO'!{hc}41", "formula", fmt_from=f"{pc}33")
        setc("PO", f"{pc}68", f"='HC-PO'!{hc}41*'HC-PO'!$D$6", "formula", fmt_from=f"{pc}34")
        setc("PO", f"{pc}69", f"='HC-PO'!{hc}41*'HC-PO'!$D$7", "formula", fmt_from=f"{pc}35")
    for r, txt in AI_PO_66.items():
        setc("PO", f"AI{r}", txt, "note")

    # --- F. Fld Ops Payroll B11 = 13
    setc("Fld Ops Payroll", "B11", 13, "input")

    # --- G. PO 5110-5140 live 8-production-staff basis (+ idle rows; B135 terms stay)
    for pc, hc, lc in zip(P27, H27, L27):
        base = f"SUM('HC-PO'!{hc}14:{hc}33)"
        setc("PO", f"{pc}33", f"=(1-'Depreciation Schedule'!$B$131)*{base}+'Depreciation Schedule'!{lc}226", "formula")
        setc("PO", f"{pc}34", f"=(1-'Depreciation Schedule'!$B$131)*{base}*'HC-PO'!$D$6+'Depreciation Schedule'!{lc}227", "formula")
        setc("PO", f"{pc}35", f"=(1-'Depreciation Schedule'!$B$131)*{base}*'HC-PO'!$D$7+'Depreciation Schedule'!{lc}228", "formula")
    for r, gl, idle, rate in ((33, "5110", 226, ""), (34, "5130", 227, " x D6"), (35, "5140", 228, " x D7")):
        setc("PO", f"AI{r}", AI_PO_5100.format(gl=gl, idle=idle, rate=rate), "note")

    # --- D (check): Collation Notes H78:H80 extended for the de-dup (H81 = SUM unchanged)
    setc("Collation Notes", "H78",
         f"=CO!AG67-'HC-CO'!Z67-({LW}!S43-{LW}!S34-{LW}!S36-{LW}!S38-{LW}!S39+{LW}!S46)", "formula")
    setc("Collation Notes", "H79",
         f"=CO!AG68-'HC-CO'!Z68-({LW}!S44-({LW}!S34+{LW}!S36+{LW}!S38+{LW}!S39)*{LW}!$B$5)", "formula")
    setc("Collation Notes", "H80",
         f"=CO!AG69-'HC-CO'!Z69-({LW}!S45-({LW}!S34+{LW}!S36+{LW}!S38+{LW}!S39)*{LW}!$B$6)", "formula")

    wb.save(out_path)
    pin_coreprops(v12_path, out_path)
    json.dump({"edits": spec, "count": len(spec)}, open(spec_path, "w"), indent=1)
    print(f"stage1: {len(spec)} cell edits -> {out_path} (spec: {spec_path}; names only from the user file; docProps pinned to v12's)")


# ----------------------------------------------------------------------------------------------- stage 2
def stage2(s1_path, fig_path, out_path):
    F = json.load(open(fig_path))
    wb = openpyxl.load_workbook(s1_path)
    cn = wb["Collation Notes"]
    n = 0

    def put(coord, value):
        nonlocal n
        cn[coord] = value
        n += 1

    g = lambda k: F[k]              # number
    m0 = lambda k: money(F[k])      # formatted 0dp
    hl, hl12 = F["AG132_v13"], F["AG132_v12"]

    # ---- title and decision table
    put("A1", "2027 COO Budget - Collation Notes (build v13, draft for review)")
    put("D13", ("Booked in v10: CO 6610-6640 (2027) = CO HC roster + the Logistics&WH model less seat LOG-01. "
                "v13 (user decisions 2026-10-12): the add-on also excludes by formula the roster-realized seats "
                "MH-01 (HC-CO r19), TL-01 (HC-CO r20, end-dated Nov-26) and MH-02 (realized by the Material Flow "
                f"Supervisor backfill, HC-CO r35): logistics add-on {m0('lw_added_v12')} -> {m0('lw_added_v13')} "
                "(5 model seats + 5,000 new-hire cost); the roster adds flow via 'HC-CO' rows 67-69. "
                "See the v13 block at the bottom of this sheet."))
    put("E13", ("Resolved. I-41 restated in v13: the Material Handling Team Lead is on HC-PO r16 (in the capitalised "
                "B131 base) and on HC-CO r20 with end month Nov-26 (2027 cost 0, the user's file value); no 2027 "
                "expense line carries the role and seat TL-01 is excluded: "
                f"{money(-g('i41_effect'))} if it should stay an expense; one cell to flip (HC-CO F20 -> Dec-27, "
                f"+{m0('tl_roster_2027_cost')} CO cost) if the person should be costed in CO through 2027. "
                f"Logistics at CO HC burden rates: +{m0('burden_upside')}."))
    put("B14", ("RESOLVED (user decision 4, 2026-10-12): the FE Associate is out of FO's current-tech count "
                "(Fld Ops Payroll B11 14 -> 13). One person costed in both FO and FE (I-28)"))
    put("D14", ("Booked in v13: Fld Ops Payroll B11 = 13; he stays in Fld Eng Budget (FE 6610-6640) and on HC-FE r20 "
                "(roster); he remains LISTED on HC-FO r15 (snapshot; feeds no P&L line - reader note). "
                f"Effect +{m0('b11_effect')} (payroll +{m0('b11_payroll')}, 5330 +{m0('b11_5330')})."))
    put("E14", "Resolved; the +78,529 upside of v10-v12 is in the v13 headline.")
    put("F14", "User (resolved 2026-10-12)")

    # ---- caveat preamble
    put("A31", ("(0) v13 (user, 2026-10-12): CO adds GL 7700 24,000 and GL 8600 78,000 (brief v7); the user's HC "
                "roster edits are merged (brief v8): CO 6610-6640 "
                f"{m0('co66_v12')} -> {m0('co66_v13')} (roster adds less the de-duplicated seats), PE 6610-6640 "
                f"{m0('pe66_v12')} -> {m0('pe66_v13')} (live roster links incl. 5 new hires), PO 6610-6640 0 -> "
                f"{m0('po66_v13')} (Production Manager, expensed), FO {money(-g('b11_effect'))} (I-28 resolved). "
                f"2027 COO contribution {m0('AG132_v12')} -> {m0('AG132_v13')}."))
    put("A33", (f"(1) What the figure is. The bottom line, {m0('AG132_v13')}, is a COO contribution: the company's "
                f"recognized revenue ({m0('rev_v13')}, all of it) less the costs of the five COO departments only "
                f"(COGS + Opex of FO, PO, CO, FE, PE: {m0('cost_v13')}). Costs outside COO are not in this workbook, "
                "so it is not company Net Income. The workbook row keeps its GL label 'Net Income' (COO P&L!A132). "
                "It is NEGATIVE in v13: the user-approved 2026-10-12 additions (13 hires/moves and two CO GL lines) "
                "put 2027 COO costs above the plan's recognized revenue."))

    # ---- caveat table: D = effect (recomputed where inputs moved), E = contribution after this item alone
    for row, d_key in F["caveat_rows"]:
        if d_key is not None:
            put(f"D{row}", round(F[d_key], 2))
        dv = cn[f"D{row}"].value
        if isinstance(dv, (int, float)):
            put(f"E{row}", round(hl + dv, 2))
    put("C41", ("v13: the Material Handling Team Lead sits on HC-PO r16 (inside the capitalised B131 base, 0 expense "
                "while B131 = 1) AND on HC-CO r20 end-dated Nov-26 (2027 cost 0, the user's file value); seat TL-01 "
                "is excluded from the CO add-on as realized on the roster. So no 2027 expense line carries the role: "
                "its 2027 cost at PO HC rates if it should stay an expense. 0 if the end date is right and the "
                "Material Flow Supervisor (85,000, Nov-26, in CO) is the replacement. Flip HC-CO F20 to Dec-27 to "
                "cost the person in CO instead (one cell)."))
    put("C50", ("RESOLVED (user decision 4, 2026-10-12): B11 = 13 booked in v13; the +78,529 (payroll +78,198, 5330 "
                "+331) is in the headline. He stays in Fld Eng Budget / HC-FE; still listed on HC-FO (snapshot, "
                "feeds nothing)."))
    put("B50", "RESOLVED")
    put("D50", "0 (now in the headline)")
    put("E50", round(hl, 2))
    put("C51", ("Superseded by the user decision (remove from FO, not FE): the FE-side alternative is closed; the FE "
                "row stays budgeted (Fld Eng Budget r15; he is now also on HC-FE r20, which feeds no P&L line)."))
    put("B51", "RESOLVED")
    put("D51", "0 (decision 4)")
    put("E51", round(hl, 2))
    for row in (47, 49):
        put(f"E{row}", round(hl, 2))

    # ---- sign-flip / upside / range / conclusion
    put("A68", F["text_signflip"])
    put("A69", F["text_upside"])
    put("A70", F["text_range"])
    put("A71", F["text_conclusion"])

    # ---- CO reconciliation block (rows 74-81) + seat table (84-95)
    put("A74", ("Logistics & Warehouse payroll booked in CO (v10, I-17 RESOLVED); v13: roster-realized seats "
                "de-duplicated by formula (user decisions 2026-10-12)"))
    put("A75", ("v13: CO 6610 = 'HC-CO'!row 67 + 'Logistics&WH Payroll'!row 43 - rows 34/36/38/39 + row 46; 6630 = "
                "'HC-CO'!row 68 + row 44 - (34+36+38+39) x B5; 6640 = 'HC-CO'!row 69 + row 45 - (34+36+38+39) x B6 "
                "(2027 months U:AF <- F:Q / M:X). Excluded seats = realized on the HC-CO roster: LOG-01 (r17, v10), "
                "MH-01 (r19), TL-01 (r20, end-dated Nov-26), MH-02 (Material Flow Supervisor backfill, r35)."))
    put("A76", ("v13 roster adds on HC-CO (user, 2026-10-12): Material Handler 49,920 Sep-26 (r19); Material "
                "Handling Team Lead 57,554 Sep-26 to Nov-26 (r20; 2027 = 0); Material Flow Supervisor 85,000 Nov-26 "
                "(r35); Applications Engineer 85,000 Nov-26 (r36); r18 title set to Facilities Manager. All at CO HC "
                "rates via rows 67-69."))
    put("B77", "v12"); put("C77", "HC-CO roster (v13)"); put("D77", "roster adds v13 (in C)")
    put("E77", "Logistics&WH in-seats (5) + new-hire cost"); put("F77", "v13"); put("G77", "v13 - v12")
    for i, r in enumerate((78, 79, 80, 81)):
        put(f"B{r}", round(F["co66_v12_rows"][i], 2))
        put(f"C{r}", round(F["hcco_v13_rows"][i], 2))
        put(f"D{r}", round(F["co_adds_rows"][i], 2))
        put(f"E{r}", round(F["lw_in_rows"][i], 2))
        put(f"F{r}", round(F["co66_v13_rows"][i], 2))
        put(f"G{r}", round(F["co66_v13_rows"][i] - F["co66_v12_rows"][i], 2))
    put("G87", ("no (v13): excluded by formula - realized on HC-CO r20 Material Handling Team Lead (end-dated "
                "Nov-26 in the user's file; see I-41); Dec-26 hire cost stays in 2026"))
    put("G89", "no (v13): moved to HC-CO r19 Material Handler (roster row, CO HC rates); excluded by formula")
    put("G90", ("no (v13): realized by the Material Flow Supervisor backfill (85,000 Nov-26, HC-CO r35; "
                "user-confirmed 2026-10-12); Oct-26 hire cost stays in 2026; excluded by formula"))
    put("A94", "Total booked in CO (5 seats, v13)")
    put("E94", round(F["lw_in_sal"], 2)); put("F94", round(F["lw_added_v13"], 2))
    put("G94", f"tax {money(F['lw_in_tax'])}, benefits {money(F['lw_in_ben'])}, new-hire cost {money(F['lw_in_nh'])}")

    # ---- pointers and current-state lines further down
    put("A111", ("v13: CO!AI67:AI69 and PO!AI33:AI35 now describe the v13 formulas; PO!AI67:AI69 and PE!AI67:AI69 "
                 "notes added. The v10/v11 note-text descriptions above are superseded where they conflict."))
    v42 = cn["C42"].value
    put("C42", (v42 or "") + " v13: the person now sits on HC-CO r19 (HC-PO r20 is blank); the 9-of-9 reading and "
               "the +2,821 effect are unchanged (Prod Payroll still counts 9 by number).")
    put("A114", ("Full notes: 02-build/02-build_notes_v13.md. Figures: figures_v13.py (from the workbook, the v12 "
                 "workbook and 5 LibreOffice scenario recalculations); v13 scenario values recomputed, carried "
                 "effects marked per row."))
    put("A181", (f"v13: 5110-5140 stay 0 booked (capitalised); the contribution is {m0('AG132_v13')} "
                 "(CO/PE/PO payroll + CO 7700/8600 + I-28, see the v13 block below)."))
    put("G184", "2027 COO contribution v13"); put("H184", "vs booked v13")
    for r, key in ((185, "scen_booked"), (186, "scen_b131"), (187, "scen_b135"),
                   (188, "scen_b131_b135"), (189, "scen_b132"), (190, "scen_b132_b131")):
        put(f"G{r}", money(F[key]))
        put(f"H{r}", "-" if r == 185 else money(F[key] - hl))
    put("A191", ("v10: the B131 = 0 base excludes PO HC r20 (MH-01, booked in CO): PO 5110-5140 652,820 -> 590,318 "
                 "(5110 475,016, 5130 17,276, 5140 98,026). v13: same base, now live = SUM('HC-PO'!M14:M33) x "
                 "(1, D6, D7) - the 8 production staff; the Production Manager (r41) is outside it; recomputed "
                 f"{money(F['scen_b131_po_base'], 2)}."))
    put("C199", f"COO P&L!AG132 {m0('AG132_v13')} -> {m0('scen_b135')}")
    put("C200", f"{m0('scen_b131')} -> {m0('scen_b131_b135')}")

    # ---- payroll reconciliation block
    put("A251", ("FO: SD Fld Ops Payroll = current techs by count (B11 = 13 since v13, I-28 resolved; was 14) + "
                 "coordinator and manager + the ramp. HC-FO is a snapshot and feeds nothing; it still lists the FE "
                 "Associate (r15) who is costed in FE (Fld Eng Budget r15 / HC-FE r20) - reader note."))
    put("A252", ("PO: PO HC roster = 8 production staff (Material Handler moved to CO in v10; row blanked in v13) + "
                 "the Production Manager (r41, New Hires). PO 5110-5140 2027 = 0 (capitalised); B131 = 0 base = the "
                 "8 production staff, live SUM('HC-PO'!M14:M33) = 590,318. The PM is expensed in PO 6610-6640 "
                 f"({m0('po66_v13')} incl. burden) and is NOT in the base or the Prod Payroll model."))
    put("A253", (f"CO: CO 6610-6640 = CO HC roster {m0('hcco_total_v13')} (v12 748,768; adds: Material Handler, "
                 "MH Team Lead (2027 = 0, end-dated), Material Flow Supervisor, Applications Engineer) + "
                 f"Logistics&WH in-seats {m0('lw_added_v13')} (5 seats + hire costs; LOG-01/MH-01/TL-01/MH-02 "
                 f"excluded as roster-realized) = {m0('co66_v13')} (v12 1,147,260)."))
    put("A254", (f"PE: PE 6610-6640 = 'HC-PE' rows 67-69 live (v13, decision 1): {m0('pe66_v13')} (v12 1,211,637 "
                 "typed); 14 people incl. the 5 adds of 2026-10-12; r22 'transfer?' 254,785 still inside (I-35). "
                 "FE: budget = Fld Eng Budget (unchanged); FE HC + r15 (I-28, resolved) + Aug-27 hire (I-36); "
                 "burden +109,539 vs FE HC rates (I-34)."))
    put("A255", ("Reader note (v13): HC-COO is the roster roll-up of the HC tabs. It now shows the Material Handler "
                 "under CO only (HC-PO r20 blanked - no double listing); the FE Associate appears on BOTH HC-FO r15 "
                 "(snapshot; FO's P&L counts him no longer, B11 = 13) and HC-FE r20 (feeds nothing; FE's P&L costs "
                 "him via Fld Eng Budget r15) - so HC-COO's FO+FE roster payroll counts him twice while the P&L "
                 "costs him once, in FE. HC-COO's CO payroll "
                 f"({m0('hcco_total_v13')}) still intentionally differs from the CO P&L 6610-6640 "
                 f"({m0('co66_v13')}), which adds the de-duplicated Logistics&WH model seats."))
    recon = F["recon_table"]  # rows 257-261: [people, roster_total, g_text]
    for i, r in enumerate(range(257, 262)):
        put(f"C{r}", int(round(recon[i][0])))
        put(f"D{r}", round(recon[i][1], 2))
        put(f"G{r}", recon[i][2] if isinstance(recon[i][2], str) else round(recon[i][2], 2))

    # ---- issues register rows (I-06, I-17, I-28, I-38, I-41)
    put("D346", ("MeLi contractor double count: quantified at $0 in the current cells. The CONFIRM comment on Fld "
                 "Maint Budget!B30 says Fld Ops Payroll includes MeLi in '21 all-in techs', but Fld Ops Payroll!B11 "
                 "= 13 (v13; 'Current site techs on payroll (Sep-26) - Domestic Only') and Fld Maint Budget!B29 = "
                 "B30 + Fld Ops Payroll!B11 = 20. So MeLi techs are costed in 5310 only. The comment describes an "
                 "earlier state and is stale (Fld Maint Budget!A143 records the correction)."))
    put("E357", (f"v13 seats booked from the model (5): INV-01 {money(F['seat_INV-01'])} (Feb-27); TL-02 "
                 f"{money(F['seat_TL-02'])} (Jul-27); MH-06 {money(F['seat_MH-06'])} (Jul-27); MH-03 "
                 f"{money(F['seat_MH-03'])} (Mar-27); MH-04 {money(F['seat_MH-04'])} (Jun-27); + excluded as "
                 "roster-realized: LOG-01 (v10), MH-01, TL-01, MH-02 (v13). CO 6610-6640 check (CO - HC-CO roster - "
                 "de-duplicated model) = 0.00 (H78:H81)."))
    put("H357", ("None for the booking. Open: burden rates (A-44, +{} at CO HC rates on the remaining 5 seats); "
                 "Q4-26 hires: TL-01/MH-02 no longer booked from the model (v13); the roster now carries the "
                 "realized people (I-38 narrowed).").format(money(F["burden_upside"])))
    put("B368", "RESOLVED")
    put("D368", ("RESOLVED (user decision 4, 2026-10-12): the duplicate was real (FO -> FE move). v13 books Fld Ops "
                 "Payroll B11 = 13 (he is out of FO's current-tech count) and adds him to HC-FE r20 (75,000, "
                 "Sep-26), closing the FE HC gap (I-28/I-36). He stays costed in Fld Eng Budget r15; he remains "
                 "LISTED on HC-FO r15 (roster snapshot; feeds nothing)."))
    put("E368", (f"Booked effect, LibreOffice recalculation: +{money(F['b11_effect'], 2)} = payroll "
                 f"+{money(F['b11_payroll'], 2)} + 5330 +{money(F['b11_5330'], 2)} (Fld Maint Budget!B29 21 -> 20); "
                 "supervisor headcount unchanged in every month."))
    put("F368", f"+{m0('b11_effect')} (in the v13 headline)")
    put("G368", "resolved (user decision)")
    put("H368", "None. If the move date was mid-2026 rather than before Sep-26, the 2026 FO forecast (book data) would need checking; 2027 is right either way.")
    put("D378", ("The SD payroll models hire people before 2027 that the HC rosters did not show: Prod Payroll 15 "
                 "(Sep-26: 3 lift, 1 tray, 1 sup; Nov-26: 6 lift, 3 tray, 1 sup) and Logistics&WH TL-01 (Dec-26), "
                 "MH-02 (Oct-26). v13: TL-01 and MH-02 are no longer booked from the model - the roster realizes "
                 "them (TL-01 -> HC-CO r20, end-dated Nov-26; MH-02 -> the Material Flow Supervisor, HC-CO r35, "
                 "user-confirmed) - so I-38 is narrowed to the Prod Payroll ramp dates (they still set the "
                 "capitalised labour's 2027 opening ramp)."))
    put("D381", ("v13 restatement. The two material-handling roles of PO HC: r20 Material Handler is in CO (HC-CO "
                 "r19; v10 decision, v13 roster move completed). r16 Material Handling Team Lead stays on HC-PO "
                 "(inside the live B131 base = the 8 production staff) AND is listed on HC-CO r20 with end month "
                 "Nov-26 (2027 cost 0; the user's file value, kept per the brief). Booked (B131 = 1): PO 5110-5140 "
                 "= 0, so no expense line carries r16, and seat TL-01 is excluded from the CO add-on as realized on "
                 "the roster. On the 7-of-9 reading (r16 is warehouse staff) its cost should stay an expense: "
                 f"({money(F['i41_effect'])}). Under B131 = 0 the role is counted in PO 5110-5140. If instead the "
                 "person should be costed in CO through 2027, set HC-CO F20 = Dec-27 (one cell, "
                 f"+{m0('tl_roster_2027_cost')} of CO cost at CO HC rates)."))
    put("F381", f"({m0('i41_effect')}) (v13 restated, r16; same amount as v10; v9 (134,563) for r16 + r20)")
    put("H381", ("PO owner: is r16 production or warehouse staff, and did the person leave at Nov-26 (the user's "
                 "HC-CO end date) or stay? If warehouse and staying, budget the role outside the capitalised labour "
                 "(set HC-CO F20 = Dec-27, or keep an expense line)."))

    # ---- v13 block appended below the sheet (no insertions; existing rows keep their addresses)
    r = 812
    def line(*cells):
        nonlocal r
        for i, v in enumerate(cells):
            if v is not None:
                cn.cell(row=r, column=1 + i, value=v)
        r += 1
    for row in F["v13_block"]:
        line(*row)

    wb.save(out_path)
    pin_coreprops(s1_path, out_path)
    print(f"stage2: {n} Collation Notes cells updated in place + v13 block rows 812-{r - 1} -> {out_path} (docProps pinned)")


if __name__ == "__main__":
    if sys.argv[1] == "stage1":
        stage1(*sys.argv[2:6])
    elif sys.argv[1] == "stage2":
        stage2(*sys.argv[2:5])
    else:
        raise SystemExit("mode must be stage1 or stage2")
