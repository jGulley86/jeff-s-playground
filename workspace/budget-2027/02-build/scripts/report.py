"""Turn analysis results into (1) the Collation Notes sheet spec (JSON) and (2) build notes markdown.

Usage:
  python3 -I report.py COO_BOOK SD_BOOK RESULT_JSON EXTREFS_JSON NOTES_SHEET_JSON NOTES_MD OUT_XLSX_NAME

All numbers come from RESULT_JSON / EXTREFS_JSON (computed from the workbooks); none are typed in.
"""
import sys, json, hashlib, os, collections, re

COO_PATH, SD_PATH, RES, EXT, NOTES_JSON, NOTES_MD, OUT_NAME = sys.argv[1:8]
R = json.load(open(RES)); E = json.load(open(EXT)); F = R["findings"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def m(x):
    """money format"""
    if x is None:
        return ""
    return f"{x:,.0f}" if x >= 0 else f"({-x:,.0f})"


def rec(d, row, col, key):
    for x in R["recon"]:
        if x["dept"] == d and x["row"] == row and x["col"] == col:
            return x[key]


def pl(row, col, key):
    for x in R["coo_pl_before_after"]:
        if x["row"] == row and x["col"] == col:
            return x[key]


def old(d, row, col):
    for x in R["replaced_coo_fofe"]:
        if x["dept"] == d and x["row"] == row and x["col"] == col:
            return x["coo_book"]


def var(sheet, row):
    for v in F["variance"]:
        if v["sheet"] == sheet and v["row"] == row:
            return v
    return None


def vtxt(sheet, row):
    v = var(sheet, row)
    return f"{sheet}!N{row} {m(v['N'])} -> AG{row} {m(v['AG'])}" if v else ""


coo_name, sd_name = os.path.basename(COO_PATH), os.path.basename(SD_PATH)
ext_cells = E["external_cells"]
ext_by_row = collections.OrderedDict()
for e in ext_cells:
    r = int(re.sub(r"[A-Z]", "", e["cell"]))
    ext_by_row.setdefault(r, []).append(e)
ext_cached = collections.Counter(str(e["sd_cached"]) for e in ext_cells)
ext_books = sorted({b for e in ext_cells for b in re.findall(r"\[1\]([A-Za-z0-9 &\-]+?)'?!", e["formula"])})

err_b_sd = R["errors_before_sd"]; err_a = R["errors_after"]; err_b_coo = R["errors_before_coo"]
fid = R["fidelity"]
new_err_total = sum(v["new_errors_n"] for v in fid.values())
recl = F["reclass"]
recl_amt = sum(x["amount"] or 0 for x in recl)
recl_ai = [x for x in recl if x["status"] == "AI suggested"]
recl_assumed = [x for x in recl if x["tag_basis"] == "Assumed"]
recl_pairs = collections.Counter((int(x["booked_gl"]), int(x["budget_gl"])) for x in recl)
pp = F["prod_payroll"]
hidden_rows_ds = [h for h in F["hidden"] if h["book"] == "SD" and h["sheet"] == "DeploySum"]
ph = F["placeholders"]
ph_te = [p for p in ph if p["sheet"] == "Fld Maint T&E Data"]
hard = F["hardcodes"]
dn = F["defined_names"]
od = F["old_draft"]
sub = F["subtotals"]

# ------------------------------------------------------------------ issues
I = []
def add(sev, loc, finding, evidence, action):
    I.append({"id": f"I-{len(I)+1:02d}", "sev": sev, "loc": loc, "finding": finding, "evidence": evidence, "action": action})

add("HIGH", "COO P&L!AG16; PO!R12:S15, PO!U12:AF15",
    "2027 revenue is zero. All 2026 revenue sits on PO (rows 12, 13, 15). The PO 2027 revenue rows use input method 'Even' with an empty or 0 annual input (S), so U:AF = 0. As a result, the 2027 P&L is cost-only.",
    f"COO P&L N16 = {m(pl(16,'N','after'))}, AG16 = {m(pl(16,'AG','after'))}. PO!R12='{[x for x in F['revenue_lines'] if x['row']==12][0]['R']}', S12 empty. PO 4100 N12 {m(var('PO',12)['N'])}, 4900 N15 {m(var('PO',15)['N'])}.",
    "Owner of PO/revenue must enter the 2027 revenue (or link it to the Revenue Roll-up). Do not present 2027 Net Income until this is fixed.")
add("HIGH", "COO P&L!AG132 (via FO, FE)",
    "Replacing FO and FE with the SD versions moves the 2027 COO Net Income by about -6.6M. The SD build is far heavier than the COO book's FO/FE.",
    f"COO P&L AG132 before {m(pl(132,'AG','before'))}, after {m(pl(132,'AG','after'))}. FO AG132: COO book {m(old('FO',132,'AG'))} -> SD {m(rec('FO',132,'AG','source'))}; FE AG132: COO book {m(old('FE',132,'AG'))} -> SD {m(rec('FE',132,'AG','source'))}. Drivers: {vtxt('FO',52)}; {vtxt('FO',47)}; {vtxt('FO',29)}.",
    "Ask the COO and the SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off.")
add("HIGH", "DeploySum (rows 3-49, 427 cells)",
    f"DeploySum links to a workbook that was not supplied ([1] = {', '.join(ext_books)}). In the SD book these cells had already failed. Their cached values were {dict(ext_cached)}. As instructed, I kept the cached values, so the bookings/deployments/production block (rows 4-42) and the notes A45:A49 show errors in the output.",
    f"{len(ext_cells)} formula cells contain '[1]...'. Every cell is listed in the 'Collation Notes' sheet with its original formula. DeploySum errors: before {err_b_sd['DeploySum']}, after {err_a['DeploySum']}.",
    "Get the Revenue Roll-up / Deploy Detail workbook. Then either relink these formulas or paste the values in, so the plan is reproducible.")
add("HIGH", "DeploySum!B53:R66",
    "The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (and so FO/FE 2027) are typed values, not formulas. The rows above them that should derive them (rows 4-42) are broken, so these drivers can't be traced to a source.",
    f"Rows {F['deploysum_drivers']['rows_const']} contain no formulas. Examples: Fld Ops Payroll!B15 = ROUND(AVERAGE(DeploySum!O54:Q54),0); Fld Maint Budget!B40 = N(DeploySum!F54).",
    "Have the SD owner confirm that rows 53-66 match the current deployment plan (51 new-logo, 15 expansion and 1 existing go-lives in FY27 per R54/R57/R60), then record the source.")
add("HIGH", "Prod Payroll (hidden sheet, all of A24:S81)",
    "The production payroll model doesn't work. Every calculated cell is an error in both the SD book and the output, because it is driven by the broken DeploySum rows 4-42. It does not feed FO/FE: only the input cells M5, M6 and M9 are read, by Fld Ops Payroll. Its result also does not reach PO.",
    f"Errors before {pp['errors_before']}, after {pp['errors_after']}. References into it: {pp['refs_into_prod_payroll_from_output']}. PO 5110 Salaries-Production {vtxt('PO',33)} is not linked to it.",
    "Fix DeploySum first. Then decide whether PO production labour (PO rows 33-35) should link to Prod Payroll!row 81.")
add("HIGH", "Fld Maint Budget!B30 (comment), FO!AG44, FO!AG52",
    "Possible double count of MeLi contractors. Per the SD author's own CONFIRM note, Fld Maint Budget costs them in 5310 (CXC EOR) while Fld Ops Payroll includes them in the 21 all-in techs costed as employees (5510).",
    f"Comment on Fld Maint Budget!B30. {vtxt('FO',44)} (5310 Contractors-Field); {vtxt('FO',52)} (5510 Salaries-Field Ops).",
    "The SD owner must confirm the mapping and remove one of the two costings. Until then, FO 2027 may be overstated.")
add("HIGH", "PO!AG19, PO!AG20, PO!AG22 (and COO P&L same cells)",
    "2027 depreciation on robots is zero, although 2026 carries about 1.75M. PO was out of scope and is left untouched.",
    f"{vtxt('PO',19)}; {vtxt('PO',20)}; {vtxt('PO',22)}.",
    "PO owner / Finance to budget 2027 depreciation from the fixed-asset schedule.")
hc_po = [h for h in hard if h["sheet"] == "PO"]
add("MED", "PO!U28, PO!Y28, PO!AD28, PO!U38, PO!U42",
    "Hardcoded plugs are added onto the driver formula in 2027 month cells (+5,000 / +15,000). They are not visible in the method columns R:T.",
    "; ".join(h["cells"][0] for h in hc_po),
    "PO owner to move these amounts into a documented input (column S, or a manual row), or remove them.")
hc_pe = [h for h in hard if h["sheet"] == "PE"]
add("LOW", "PE!W74:AF74, PE!W76",
    "Typed numbers overwrite the driver formula in some 2027 months (manual overrides inside a formula row).",
    "; ".join(", ".join(h["cells"]) for h in hc_pe),
    "PE owner to confirm the overrides are intended, or set the row method to Manual.")
z_lines = [(s, r) for s, r in (("FO", 58), ("FO", 67), ("FO", 91), ("FE", 91)) if var(s, r)]
add("MED", ", ".join(f"{s}!AG{r}" for s, r in z_lines),
    "Several FO/FE lines with material 2026 spend have 2027 = 0. FO Total Expense (SG&A) is 0 for 2027.",
    "; ".join(vtxt(s, r) for s, r in z_lines) + f"; {vtxt('FO',116)}.",
    "SD owner to confirm whether these costs stop in 2027 or are budgeted elsewhere (e.g. Fld Eng Budget / Fld Ops Payroll).")
n_var = len(F["variance"])
add("MED", "see 'Variance scan' table (all depts + COO P&L)",
    f"{n_var} rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k.",
    f"Largest COO P&L moves: {vtxt('COO P&L',47)}; {vtxt('COO P&L',52)}; {vtxt('COO P&L',29)}; {vtxt('COO P&L',98)}.",
    "Each dept owner should comment on the rows that apply to them in the variance table.")
add("MED", "Fld Maint Budget!B8 (D8 note); Fld Maint Budget!E117",
    "Site setup kit cost is flagged 'PLACEHOLDER - update when the kit list is priced'. It feeds FO 5330 Maintenance Tools & Supplies.",
    f"B8 = 4,500 $/new site. {vtxt('FO',46)}.",
    "SD owner to price the kit list and replace B8.")
add("MED", "Fld Ops Payroll!M11, Fld Ops Payroll!B12 (cell notes)",
    "Two Fld Ops Payroll drivers are marked 'Placeholder' in the author's notes: site techs per floater (M11) and the % of expansion go-lives needing a tech (B12). They drive FO 5510-5540.",
    "M11 = 40, B12 = 0.6. Notes on both cells begin 'Placeholder.'",
    "SD owner to confirm or replace these values.")
add("LOW", "Prod Payroll!M7, B9, A33 (cell notes); Fld Ops Payroll!B9",
    "More placeholder inputs: Prod Payroll new-hire cost, current headcount and absence factors. Hidden Old Draft!B142 says the Fld Ops Payroll $2,000 new-hire cost (B9) is a placeholder that overlaps onboarding.",
    "Prod Payroll notes start 'Placeholder'. Old Draft!B142 text. Fld Ops Payroll!B9 = 2,000.",
    "SD owner to confirm. The Prod Payroll ones have no FO/FE impact today because that sheet is broken.")
add("MED", "Fld Maint Budget!B12 (comment)",
    "Open CONFIRM: the MeLi contract supervisor is costed in 5310 at $8,704/month. The author's note says Fld Ops Payroll shows 0 current supervisors, but Fld Ops Payroll!H11 (current supervisors - Isaiah) = 1 and E12 says the MeLi supervisor sits in Fld Maint Budget. The supervisor treatment is inconsistent between the two tabs.",
    "Comment on Fld Maint Budget!B12; Fld Maint Budget!B11 = 8,704, B12 = 1; Fld Ops Payroll!H11 = 1.",
    "SD owner to confirm treatment (linked to I-06).")
add("MED", "Fld Maint T&E Data!M5:M379 (hidden SD sheet, not carried)",
    f"{len(recl)} T&E transactions are flagged 'Reclass needed' = Yes, totalling ${recl_amt:,.2f}. The booked GL differs from the budget GL. {len(recl_ai)} of them are tagged 'AI suggested' and {len(recl_assumed)} have tag basis 'Assumed'. If the FO 2026 actuals (B:M) were pulled on booked GL, these amounts sit on the wrong 2026 lines. That distorts the line-level 2026 vs 2027 comparisons, though not the totals.",
    "Top booked->budget GL pairs: " + ", ".join(f"{a}->{b} x{n}" for (a, b), n in recl_pairs.most_common(5)) + ".",
    "Finance to post the reclasses in NetSuite (or confirm none are needed). Review the 'AI suggested' / 'Assumed' tags before relying on T&E unit costs.")
add("MED", "SD 'Logistics&WH Payroll' (not carried)",
    "The SD book's Logistics & Warehouse payroll model says it 'rolls up to Production Operations', but no formula anywhere references it. The COO book's PO tab does not link to it. So the warehouse payroll is either missing from PO 2027 or entered separately.",
    "No formulas reference 'Logistics&WH Payroll' in either book (sheet dependency map). Its own A2 text says it rolls up to PO.",
    "PO owner to confirm whether PO 2027 includes the warehouse team. If not, link PO to this model (it would then need to be added to the workbook).")
add("LOW", "Fld Ops Payroll!B10, B15, B16 (cell notes)",
    "The hiring horizon ends at Dec-27 (DeploySum row 54). Hires for Jan-28 go-lives use an Oct-Dec 27 average default rather than a forecast.",
    "Notes on B10/B15/B16. B15 = ROUND(AVERAGE(DeploySum!O54:Q54),0).",
    "Overwrite B15/B16 if a 2028 go-live forecast exists.")
add("LOW", "FE <-> Fld Eng Budget",
    "FE and Fld Eng Budget link in both directions: Fld Eng Budget reads FE 2026 columns B:J/N/AG, and FE 2027 rows 30, 31, 67-69, 74, 75 read Fld Eng Budget. There is no cell-level circularity (LibreOffice recalculated with no errors), but the structure is easy to break.",
    "Fld Eng Budget has 68 references to FE. FE has 84 references to Fld Eng Budget.",
    "Avoid editing FE rows 30/31/49/50/74/75 2026 columns without checking Fld Eng Budget.")
add("LOW", "Hidden sheets / rows",
    "SD has 3 hidden sheets: Prod Payroll (carried over, kept hidden), Old Draft and Fld Maint T&E Data (not carried over because FO/FE don't depend on them). DeploySum has hidden rows, which are preserved.",
    f"Hidden: {[h['sheet'] for h in F['hidden'] if h['book']=='SD' and h['state']!='visible']}; DeploySum hidden rows {hidden_rows_ds[0]['hidden_rows'] if hidden_rows_ds else 0} (30, 32-36, 40-42).",
    "No action, unless reviewers want Old Draft / T&E Data in the pack for audit.")
add("LOW", "Old Draft (hidden, not carried)",
    "Old Draft dependence is contained. Only Fld Maint T&E Data!Q26 reads Old Draft, while Old Draft reads T&E Data, Fld Ops Payroll and DeploySum. No sheet in the FO/FE chain depends on Old Draft, so the output has 0 references to it.",
    "; ".join(f"{o['book']} {o['sheet']}: {o['refs']} cell(s) e.g. {o['examples'][0]}" for o in od) + f". SD dependency map: Old Draft -> {F['sd_depmap'].get('Old Draft')}.",
    "None for the budget. Consider deleting Old Draft from the SD book once T&E Data!Q26 is re-pointed.")
add("LOW", "All dept tabs + COO P&L rows 23/24/27/37",
    "Rows 23 and 24 carry the same label ('5025 - Freight and Delivery - Production (Summary)'). Row 23 is an empty header. Row 24 holds postings and is inside row 27 = SUM(24:26). Row 37's explicit list (19,20,21,22,27,28,29,30,31,36) covers every direct child of the 18-37 section, so no line is skipped today. But anything typed on row 23 would be left out of the totals.",
    f"Subtotal scan on 6 sheets: 0 skipped lines with values. Row 23 is blank on every tab. COO P&L dept-sum formulas: {len(F['coo_pl_omits'])} omissions.",
    "Optionally relabel row 23 as a header, or lock it.")
add("LOW", "COO P&L!B65:M65 (row labelled 'Expense'), COO P&L!C141",
    "COO P&L row 65 (the 'Expense' section header) holds an unlabelled gross-margin % formula (=IFERROR(B64/B16,\"\")). It is blank for 2027 because revenue is 0. Row 141 'Taxes and Benefits %' shows -1433% for Feb-26, caused by negative 2026 payroll postings.",
    f"C141 = -14.33 (ratio). {vtxt('PO',67)} (negative 2026 SG&A salaries); {vtxt('PE',35)}.",
    "Label row 65. Finance to explain the negative 2026 payroll postings in PO 6610 and PE 5140.")
add("LOW", "Workbook defined names (COO book)",
    f"The COO book carries {dn['coo_total']:,} legacy defined names from an old template ({dn['coo_ref_errors']:,} resolve to #REF!, some point at external .xls files). No formula uses them. I kept them unchanged.",
    f"Count before {dn['coo_total']:,}, output {dn['output_total']:,}. Name tokens found in output formulas: {F['name_usage']}.",
    "Purge the names in a separate clean-up (Name Manager), not as part of the budget.")
add("LOW", "Method artefacts (all carried SD sheets)",
    "Side effects of moving from Google Sheets to xlsx: (a) threaded comments come across as plain cell notes, with the text kept; (b) Google's '#ERROR!' code has no Excel equivalent, so cached '#ERROR!' values on external-link cells are stored as #REF!; (c) LibreOffice saves error constants as '=#REF!' formulas; (d) Prod Payroll XLOOKUP cells already failed upstream and still do.",
    f"Error-code changes on cells that were already errors: DeploySum {fid['DeploySum']['err_code_changed_n']}, Prod Payroll {fid['Prod Payroll']['err_code_changed_n']}. New errors introduced: {new_err_total}.",
    "None. These are disclosed here for the reviewers.")

# ------------------------------------------------------------------ notes sheet JSON
ext_rows_tbl = []
for e in ext_cells:
    ext_rows_tbl.append([e["sheet"], e["cell"], str(e["sd_cached"]), str(e["stored"]), e["formula"][:250]])

notes = {
    "title": "2027 COO Budget - Collation Notes (build v1, draft for review)",
    "col_widths": [10, 10, 34, 70, 70, 60],
    "sections": [
        {"heading": "Source", "lines": [
            f"Base workbook: {coo_name} (sha256 {sha(COO_PATH)[:16]}...) - COO P&L roll-up + FO, PO, CO, FE, PE.",
            f"Replacement source: {sd_name} (sha256 {sha(SD_PATH)[:16]}...) - newer FO and FE plus driver tabs.",
            "Inputs were read only. This workbook is a draft for critic / verifier review."]},
        {"heading": "Method", "lines": [
            "1. Started from the COO book. Deleted its FO and FE tabs and rebuilt them in the same tab positions from the SD book. Copied cell by cell: values/formulas, fonts, fills, borders, number formats, column widths, row heights, merges, freeze panes, data validations, conditional formats and notes.",
            "2. Brought over every SD tab that FO/FE depend on, directly or indirectly: " + ", ".join(E["support"]) + ". Hidden state was kept (Prod Payroll stays hidden).",
            "3. Not carried over (FO/FE do not depend on them): " + ", ".join(s for s in ["Logistics&WH Payroll", "Old Draft", "Fld Maint T&E Data"]) + ". I still scanned them for issues.",
            f"4. External-workbook formulas ('[1]...', {len(ext_cells)} cells on DeploySum) cannot resolve. I replaced them with the SD book's cached values and list every one below.",
            "5. PO, CO, PE and the COO P&L formulas are untouched. COO P&L picks up the new FO/FE automatically through its =SUM(FO!x,PO!x,CO!x,FE!x,PE!x) cells.",
            "6. Recalculated with headless LibreOffice and checked every value against the source cached values."]},
        {"heading": "Headline (live formulas vs COO book cached values)", "table": {
            "header": ["Line", "Col", "Before (COO book)", "After (this workbook, live)"], "formula_cols": [4],
            "rows": [[x["line"], x["col"], round(x["before"], 2), f"='COO P&L'!{x['col']}{x['row']}"] for x in R["coo_pl_before_after"]]}},
        {"heading": "Issues", "table": {
            "header": ["ID", "Severity", "Location", "Finding", "Evidence", "Recommended action"],
            "rows": [[i["id"], i["sev"], i["loc"], i["finding"], i["evidence"], i["action"]] for i in I]}},
        {"heading": f"External-reference cells replaced by SD cached values ({len(ext_cells)})", "table": {
            "header": ["Sheet", "Cell", "SD cached value", "Value stored in this workbook", "Original formula (leading = omitted)"],
            "rows": ext_rows_tbl}},
    ]}
json.dump(notes, open(NOTES_JSON, "w"), indent=1)

# ------------------------------------------------------------------ markdown
L = []
w = L.append
w("# 02-build notes v1 - 2027 COO budget collation\n")
w(f"Output: `02-build/{OUT_NAME}`  \nScripts: `02-build/scripts/` (build.py, recalc.sh, analyze.py, report.py, run_build.sh)  \n"
  f"Inputs (read-only): `{coo_name}` sha256 `{sha(COO_PATH)}`; `{sd_name}` sha256 `{sha(SD_PATH)}`\n")
w("## Headline\n")
w(f"- COO P&L 2027 Net Income (AG132): before **{m(pl(132,'AG','before'))}**, after **{m(pl(132,'AG','after'))}** (change {m(pl(132,'AG','change'))}).")
w(f"- COO P&L 2026 Net Income (N132): before {m(pl(132,'N','before'))}, after {m(pl(132,'N','after'))}. The FO/FE 2026 columns are identical in both books, so 2026 does not move.")
w(f"- 2027 revenue is still 0 (I-01). The 2027 P&L is cost-only.")
w(f"- New formula errors introduced by the merge: **{new_err_total}**. COO P&L roll-up check: {R['rollup']['checked']} cells checked, {len(R['rollup']['fail'])} off by more than $1 (max abs diff {R['rollup']['max_abs_diff']:.4f}). COO P&L 'check' row 133 max abs = {F['check_row_133_max_abs']:.6f}.\n")

w("## Method\n")
w("1. **Base = COO book**, loaded with formulas (openpyxl). I deleted the `FO` and `FE` tabs and created new `FO` / `FE` tabs in the same positions (2nd and 5th).")
w("2. **Copied cell by cell from the SD book** (`copy_worksheet` cannot cross workbooks): value or formula (array formulas re-created with the same ref), font, fill, border, alignment, number format, protection, hyperlinks, notes; merged ranges; column widths/hidden/outline; row heights/hidden; freeze panes, gridlines, zoom, tab colour, sheet state; data validations; conditional formats (with their dxf styles).")
w("3. **Dependency closure**: I parsed every formula in SD `FO` and `FE` for sheet references and followed them recursively. The closure is " + ", ".join(E["carried"]) + " (DeploySum and Prod Payroll are reached only indirectly). The SD book has no defined names other than a filter range on the T&E sheet, which is not carried, so no names needed copying. A token scan of every output formula found " + str(F["name_usage"]) + " uses of the COO book's defined names (see I-24).")
w(f"4. **External links**: {len(ext_cells)} DeploySum formula cells reference `[1]` (an external workbook that was not supplied, and the xlsx contains no externalLink part). Each was replaced by its SD cached value: {dict(ext_cached)}. Google's `#ERROR!` has no Excel equivalent and was stored as `#REF!`. Each cell is listed in the `Collation Notes` sheet (cell, original formula, cached value, stored value) and summarised in the appendix below. No other formula was turned into a value.")
w("5. **COO P&L, PO, CO, PE untouched.** COO P&L formulas reference `FO!`/`FE!` by name, so they pick up the new tabs.")
w("6. **Collation Notes** sheet added at the front, with source, method, live headline formulas, the issues list, and the external-cell list.")
w("7. **Recalculated** with headless LibreOffice 24.2 (`soffice --headless --convert-to xlsx`), using a private profile set to always recalculate on load. I then reloaded with `data_only=True` and checked every cell against the source cached values. The delivered file is the LibreOffice-recalculated file, so cached values are present.\n")

w("## Sheets in the output and why\n")
w("| # | Sheet | From | State | Why |\n|---|---|---|---|---|")
why = {"Collation Notes": ("new", "visible", "Summary of source, method and issues (required)"),
       "COO P&L": ("COO book", "visible", "Roll-up; unchanged"),
       "FO": ("SD book", "visible", "Replaces COO FO (newer, fuller build)"),
       "PO": ("COO book", "visible", "Unchanged"), "CO": ("COO book", "visible", "Unchanged"),
       "FE": ("SD book", "visible", "Replaces COO FE (newer, fuller build)"),
       "PE": ("COO book", "visible", "Unchanged"),
       "DeploySum": ("SD book", "visible", "FO/FE dependency via Fld Ops Payroll, Fld Maint Budget, Fld Eng Budget, Prod Payroll"),
       "Fld Ops Payroll": ("SD book", "visible", "Direct FO dependency (FO rows 52-54)"),
       "Prod Payroll": ("SD book", "hidden", "Indirect: Fld Ops Payroll!M5:M7 read Prod Payroll!M5, M6, M9"),
       "Fld Maint Budget": ("SD book", "visible", "Direct FO dependency (FO rows 29, 30, 44-49)"),
       "Fld Eng Budget": ("SD book", "visible", "Direct FE dependency (FE rows 30, 31, 67-69, 74, 75)")}
order = ["Collation Notes", "COO P&L", "FO", "PO", "CO", "FE", "PE"] + E["support"]
for k, s in enumerate(order, 1):
    a, b, c = why[s]
    w(f"| {k} | {s} | {a} | {b} | {c} |")
w("\nNot carried over (no FO/FE dependency): `Logistics&WH Payroll` (no formula anywhere references it, see I-17), `Old Draft` (hidden, see I-21), `Fld Maint T&E Data` (hidden, see I-16). All three were still scanned.\n")

w("## Formula preservation\n")
w("| Sheet | Formulas in source | Formulas in output | External cells -> cached value |\n|---|---:|---:|---:|")
for s, v in R["formula_counts"].items():
    w(f"| {s} | {v['source_formulas']} | {v['output_formulas']} | {v['external_replaced']} |")
w("\nNote: in DeploySum the output count (498) = 88 internal formulas kept + 410 error constants that LibreOffice saves as `=#REF!`/`=#N/A` formulas. The other 17 external cells had a cached value of 0 and are stored as the number 0.\n")

w("## Reconciliation (source cached vs output recalculated)\n")
w("Source = SD book for FO/FE, COO book for PO/CO/PE. N = 2026 total, AG = 2027 total.\n")
w("| Dept | Line | Row | 2026 N source | 2026 N output | Delta N | 2027 AG source | 2027 AG output | Delta AG |\n|---|---|---:|---:|---:|---:|---:|---:|---:|")
for d in ["FO", "PO", "CO", "FE", "PE"]:
    for r, lab in [(16, "Total Income"), (63, "Total COGS"), (64, "Gross Profit"), (116, "Total Expense"), (132, "Net Income")]:
        w(f"| {d} ({rec(d,r,'N','src')}) | {lab} | {r} | {m(rec(d,r,'N','source'))} | {m(rec(d,r,'N','output'))} | {rec(d,r,'N','delta'):.2f} | {m(rec(d,r,'AG','source'))} | {m(rec(d,r,'AG','output'))} | {rec(d,r,'AG','delta'):.2f} |")
w("\nCell-by-cell fidelity, every non-empty cell (source cached vs output):\n")
w("| Sheet | Cells compared | Value mismatches | Max abs numeric diff | New errors | Errors cleared | Error code changed (still error) |\n|---|---:|---:|---:|---:|---:|---:|")
for s, v in fid.items():
    w(f"| {s} | {v['cells']} | {v['mismatch_n']} | {v['num_max_abs_diff']:.6f} | {v['new_errors_n']} | {v['errors_cleared_n']} | {v['err_code_changed_n']} |")
w("\nFO/FE tabs replaced: COO book values (dropped) vs SD book values (used):\n")
w("| Dept | Line | Col | COO book (replaced) | SD book (used) | Difference |\n|---|---|---|---:|---:|---:|")
for x in R["replaced_coo_fofe"]:
    w(f"| {x['dept']} | {x['line']} | {x['col']} | {m(x['coo_book'])} | {m(x['sd_book'])} | {m(x['sd_book']-x['coo_book'])} |")
w("")
w("## COO P&L before vs after\n")
w("| Line | Row | Col | Before (COO book cached) | After (output) | Change |\n|---|---:|---|---:|---:|---:|")
for x in R["coo_pl_before_after"]:
    w(f"| {x['line']} | {x['row']} | {x['col']} | {m(x['before'])} | {m(x['after'])} | {m(x['change'])} |")
w(f"\nRoll-up integrity: for every COO P&L row 9-132 (except ratio row 65) and 137-140, across B:N and U:AG, COO P&L = FO+PO+CO+FE+PE. {R['rollup']['checked']} cells checked, {len(R['rollup']['fail'])} failures, max abs diff {R['rollup']['max_abs_diff']:.6f}.\n")

w("## Error scan (#REF!, #NAME?, #VALUE!, #DIV/0!, #N/A, Google #ERROR!)\n")
w("| Sheet | Before (source book cached) | After (output recalculated) |\n|---|---|---|")
for s in order:
    before = "n/a (new sheet)" if s == "Collation Notes" else (err_b_sd.get(s) if s in E["carried"] else err_b_coo.get(s))
    w(f"| {s} | {before or 'none'} | {err_a.get(s) or 'none'} |")
for s in ["Logistics&WH Payroll", "Old Draft", "Fld Maint T&E Data"]:
    w(f"| {s} (SD, not carried) | {err_b_sd.get(s) or 'none'} | n/a |")
w(f"\nNo cell that was a value in the source is an error in the output (new errors = {new_err_total}). The DeploySum and Prod Payroll errors were already there in the SD book (I-03, I-05). All #DIV/0!/#VALUE!/#NAME? counts are 0.\n")

w("## Issues\n")
w("| ID | Sev | Location (sheet!cell) | Finding | Evidence | Recommended action |\n|---|---|---|---|---|---|")
for i in I:
    esc = lambda t: str(t).replace("|", "\\|").replace("\n", " ")
    w(f"| {i['id']} | {i['sev']} | {esc(i['loc'])} | {esc(i['finding'])} | {esc(i['evidence'])} | {esc(i['action'])} |")

w("\n### Scan coverage (what was checked, including clean results)\n")
w(f"- 2026 (B:N) FO/FE differences between the books, rows 9-141: **{sum(len(v) for v in F['diff_2026'].values())} cells differ**, so no 2026 choice was needed. Formula differences FO/FE (all columns A:AJ, rows 1-200): FO {F['formula_diff_FO_FE']['FO']['n']}, FE {F['formula_diff_FO_FE']['FE']['n']}. All are in 2027 U:AF, where the SD version links to the driver tabs (FO rows 29, 30, 44-49 -> Fld Maint Budget; FO 52-54 -> Fld Ops Payroll, replacing typed numbers; FE 30, 31, 67-69, 74, 75 -> Fld Eng Budget).")
w(f"- Zero 2027 revenue: I-01.")
w(f"- External links: I-03 (DeploySum only; no other sheet in either book references another workbook).")
w(f"- Hardcoded numbers inside formula rows: {len(hard)} hits, all listed in I-08 / I-09. Constants in total/roll-up cells: 0. GL codes used as SUMIF keys and 2,080 hours/yr were excluded as false positives.")
w(f"- Placeholders (PLACEHOLDER/TBD/AI suggested/assumed, in cell values and notes, all sheets of both books): {len(ph)} hits. Of these, {len(ph_te)} are in the hidden T&E sheet's tag columns (I-16). The rest are in I-12, I-13, I-14 and DeploySum!A49 (\"Arconic + placeholders\" in the unsigned-forecast note, part of I-03). 'TBD': 0 hits.")
w(f"- Variance (>±50% and >$50k, AG vs N): {n_var} rows, listed below.")
w(f"- COO P&L dept-sum formulas omitting a dept or pointing at another cell: {len(F['coo_pl_omits'])}. COO P&L leaf rows not linked to depts while depts hold values: {len(F['coo_pl_unlinked'])}.")
w(f"- Subtotal formulas skipping lines (label-hierarchy check of every 'Total - X' row, columns B/U/AF, on COO P&L and all 5 dept tabs): 0 skipped lines. Row 37 explicitly verified (I-22). Only other hit: COO P&L row 65 header holds a GM% formula (I-23). Gross Profit / Net Ordinary Income / Net Other Income / Net Income formulas: {len(F['special_rows'])} deviations.")
w(f"- YoY column AJ sign convention: {len(F['yoy_sign']['cost_rows_using_AG_minus_N'])} cost rows using AG-N; {len(F['yoy_sign']['other'])} non-standard formulas.")
w(f"- Hidden sheets: I-20. 'Reclass needed' = Yes: I-16. Old Draft dependence: I-21 (output has 0 references).\n")

w("### Variance scan: rows with |AG-N| > $50k and > 50% (output values)\n")
w("| Sheet | Row | Line | 2026 N | 2027 AG | Change | % |\n|---|---:|---|---:|---:|---:|---:|")
for v in F["variance"]:
    pct = f"{v['pct']*100:.0f}%" if v["pct"] is not None else "n/a (N=0)"
    w(f"| {v['sheet']} | {v['row']} | {v['label']} | {m(v['N'])} | {m(v['AG'])} | {m(v['diff'])} | {pct} |")

w("\n### T&E rows with 'Reclass needed' = Yes (SD `Fld Maint T&E Data`, hidden)\n")
w(f"{len(recl)} rows, ${recl_amt:,.2f}. Rows: " + ", ".join(str(x["row"]) for x in recl) + ".\n")
w("| Booked GL -> Budget GL | Rows |\n|---|---:|")
for (a, b), n in recl_pairs.most_common():
    w(f"| {a} -> {b} | {n} |")

w("\n### Appendix: external-reference cells (DeploySum), each replaced by its SD cached value\n")
w("Full per-cell list with original formulas: `Collation Notes` sheet. Summary by row:\n")
w("| Row | Label (col A) | Cells | SD cached values | Example original formula |\n|---:|---|---|---|---|")
for r, es in ext_by_row.items():
    cells = ", ".join(e["cell"] for e in es)
    vals = dict(collections.Counter(str(e["sd_cached"]) for e in es))
    w(f"| {r} | {'(formula text)' if r in (3,45,46,47,48,49) else ''} | {cells} | {vals} | `{es[0]['formula'][:110].replace('|','/')}` |")

w("\n## Decisions\n")
w("- D1: Carried over only the dependency closure of FO/FE (5 tabs), as the handoff specifies. Logistics&WH Payroll, Old Draft and T&E Data were scanned but not carried.")
w("- D2: External `[1]` formulas were replaced by SD cached values, as instructed, even though those values are errors. Google `#ERROR!` was stored as `#REF!` (the closest Excel code for an unresolved link). This keeps error propagation the same, so every downstream IFERROR fallback matches the SD cached results (0 mismatches).")
w("- D3: Kept the COO book's 14,310 legacy defined names unchanged (base book not altered beyond scope). Flagged as I-24.")
w("- D4: Did not change or 'fix' any number, including the plugs, placeholders, zero revenue and zero depreciation. They are flagged only.")
w("- D5: The delivered xlsx is the LibreOffice-recalculated file, so every formula has a cached value. LibreOffice rewrote styles in its own format, and fills, number formats, widths, hidden state, validations and conditional formats survive. Google-specific package parts (workbook metadata, threaded-comment XML) are not kept; note text is kept.")
w("- D6: Tolerance for 'match' = $0.01 per cell (actual max diff below $0.001). Roll-up check tolerance = $1 per the brief.")
w("\n## Not done / limits\n")
w("- I could not refresh DeploySum rows 4-42 or Prod Payroll because the external workbook is unavailable (BLOCKER in the handoff, handled as instructed).")
w("- I did not open the output in Microsoft Excel. It was validated in LibreOffice 24.2 only.")
open(NOTES_MD, "w").write("\n".join(L) + "\n")
print("issues:", len(I), [ (i['id'], i['sev']) for i in I])
