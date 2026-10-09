"""v2 analysis: cross-department overlap, driver traces, raise timing, quantifications for the critic items.

Usage:
  python3 -I analyze_v2.py COO_BOOK SD_BOOK OUT_XLSX_RECALCULATED EXTREFS_JSON RESULT_V2_JSON

Reads only. Every number written to RESULT_V2_JSON is read or summed from workbook cells; nothing is typed in.
"""
import sys, re, json, datetime, collections
import openpyxl
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.utils import get_column_letter, column_index_from_string

COO_PATH, SD_PATH, OUT_PATH, EXT_JSON, RES_JSON = sys.argv[1:6]
DEPTS = ["FO", "PO", "CO", "FE", "PE"]
M27 = [get_column_letter(i) for i in range(21, 33)]          # dept tabs U..AF = Jan..Dec 27
DRV27 = [get_column_letter(i) for i in range(6, 18)]          # Fld Ops Payroll / Logistics&WH F..Q = Jan..Dec 27
FMB27 = [get_column_letter(i) for i in range(2, 14)]          # Fld Maint / Fld Eng Budget B..M = Jan..Dec 27
ERR_RE = re.compile(r"^(#(NULL!|DIV/0!|VALUE!|REF!|NAME\?|NUM!|N/A|ERROR!|CALC!|SPILL!)|Err:\d+)$")


def ftext(v):
    if isinstance(v, ArrayFormula):
        return v.text
    if isinstance(v, str) and v.startswith("="):
        return v
    return None


def num(v):
    if isinstance(v, bool):
        return None
    return float(v) if isinstance(v, (int, float)) else None


def jsonable(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()[:10]
    if isinstance(v, ArrayFormula):
        return v.text
    return v


coo_f = openpyxl.load_workbook(COO_PATH); coo_v = openpyxl.load_workbook(COO_PATH, data_only=True)
sd_f = openpyxl.load_workbook(SD_PATH); sd_v = openpyxl.load_workbook(SD_PATH, data_only=True)
out_f = openpyxl.load_workbook(OUT_PATH); out_v = openpyxl.load_workbook(OUT_PATH, data_only=True)
ext = json.load(open(EXT_JSON))
R = {}


def cell(book, sheet, ref):
    f, v = {"OUT": (out_f, out_v), "SD": (sd_f, sd_v), "COO": (coo_f, coo_v)}[book]
    return {"value": jsonable(v[sheet][ref].value), "formula": jsonable(ftext(f[sheet][ref].value))}


def val(book, sheet, ref):
    return cell(book, sheet, ref)["value"]


def rowsum(book, sheet, row, cols):
    return sum(num(val(book, sheet, f"{c}{row}")) or 0.0 for c in cols)


# ------------------------------------------------------------------ cells quoted by the report
CELLS = {
    "OUT": {
        "COO P&L": ["B37", "C141", "AG16", "N16"],
        "PO": ["R12", "S12", "T12", "R47", "S47", "U47", "AF47", "R93", "S93", "R95", "S95", "R99", "S99"],
        "PE": ["R74", "S74", "R93", "S93", "R95", "S95", "R99", "S99"],
        "Fld Maint Budget": ["B5", "D5", "B6", "D6", "B8", "D8", "B10", "B11", "B12", "B13", "B14", "B16", "D16",
                             "B29", "B30", "D30", "B37", "A99", "A143", "B9"],
        "Fld Ops Payroll": ["B9", "B10", "B15", "B16", "B11", "A11", "B12", "M11", "M14", "H11", "E11", "E12", "M5", "M6", "M7", "J5",
                            "J6", "J7", "J8", "H15", "E15", "H16", "E16"],
        "Fld Eng Budget": ["A21", "B21", "D21", "B2", "B6", "D6", "B24", "B25", "D24", "D25", "B103", "B100",
                           "A13", "A19", "C19", "A59", "A67", "B68", "B69", "B70", "B76", "B78", "B79", "B80", "A76"],
        "Prod Payroll": ["M5", "M6", "M7", "M9", "J5", "J6", "J7", "J9"],
        "DeploySum": ["R54", "R57", "R60", "A54", "A57", "A60"],
    },
    "SD": {
        "Logistics&WH Payroll": ["A1", "A2", "S51", "R51", "S43", "S44", "S45", "S46", "S47", "S50",
                                 "A54", "B54", "A55", "B55", "A56", "B56", "B58", "B59", "B60", "A66",
                                 "B7", "B8", "B9", "B10", "C7", "C8", "C9", "C10"],
    },
}
R["cells"] = {f"{b}:{s}!{c}": cell(b, s, c) for b, d in CELLS.items() for s, cs in d.items() for c in cs}

# ------------------------------------------------------------------ headline
hl = {}
for book in ("COO", "OUT"):
    for r in [16, 63, 116, 117, 131, 132] + list(range(17, 63)):
        for col in ("N", "AG"):
            hl[f"{book}:{r}:{col}"] = num(val(book, "COO P&L", f"{col}{r}")) or 0.0
R["headline"] = hl
# depreciation rows identified by label on COO P&L (cost rows 17-62 whose label contains 'Depreciation')
R["dep_labels"] = {r: val("OUT", "COO P&L", f"A{r}") for r in range(17, 63)
                   if "DEPRECIATION" in str(val("OUT", "COO P&L", f"A{r}") or "").upper() and not str(val("OUT", "COO P&L", f"A{r}")).startswith("Total")}

# ------------------------------------------------------------------ cross-department overlap (2027 AG)
GL_RE = re.compile(r"^\d{4} - ")
MEMO = {137: "Salaries and Wages", 138: None, 139: "Payroll Taxes", 140: "Benefits"}
ov = []
for r in range(9, 142):
    lab = (val("OUT", "COO P&L", f"A{r}") or "").strip()
    kind = "GL" if GL_RE.match(lab) else ("memo" if r in (137, 138, 139, 140) else None)
    if not kind:
        continue
    ag = {d: num(val("OUT", d, f"AG{r}")) or 0.0 for d in DEPTS}
    nz = [d for d in DEPTS if abs(ag[d]) >= 0.5]
    if len(nz) < 2:
        continue
    ov.append({"row": r, "label": lab, "kind": kind,
               "coo_pl_AG": num(val("OUT", "COO P&L", f"AG{r}")) or 0.0,
               "AG": ag, "N": {d: num(val("OUT", d, f"N{r}")) or 0.0 for d in DEPTS},
               "nonzero": nz,
               "U_formula": {d: jsonable(ftext(out_f[d][f"U{r}"].value)) or jsonable(out_f[d][f"U{r}"].value) for d in nz},
               "AF_formula": {d: jsonable(ftext(out_f[d][f"AF{r}"].value)) or jsonable(out_f[d][f"AF{r}"].value) for d in nz},
               "method": {d: [jsonable(out_f[d][f"{c}{r}"].value) for c in ("R", "S", "T")] for d in nz},
               "U_typed": {d: ftext(out_f[d][f"U{r}"].value) is None for d in nz}})
R["overlap"] = ov
R["overlap_rows_checked"] = sum(1 for r in range(9, 142)
                                if GL_RE.match((val("OUT", "COO P&L", f"A{r}") or "").strip()) or r in (137, 138, 139, 140))

# ------------------------------------------------------------------ Prod Payroll trace
SHREF = re.compile(r"'Prod Payroll'!\$?([A-Z]{1,3})\$?(\d+)")
pp_refs = []
for book, wbf in (("OUT", out_f), ("SD", sd_f)):
    for ws in wbf.worksheets:
        if ws.title == "Prod Payroll" or (book == "SD" and ws.title in out_f.sheetnames):
            continue
        for row in ws.iter_rows():
            for c in row:
                f = ftext(c.value)
                if f and "Prod Payroll" in f:
                    for m in SHREF.finditer(f):
                        tgt = f"{m.group(1)}{m.group(2)}"
                        lab_cell = f"J{m.group(2)}"
                        t = sd_f["Prod Payroll"][tgt].value
                        pp_refs.append({"book": book, "from": f"{ws.title}!{c.coordinate}", "formula": f,
                                        "target": f"Prod Payroll!{tgt}", "target_label": sd_v["Prod Payroll"][lab_cell].value,
                                        "target_is_formula": ftext(t) is not None,
                                        "value": jsonable(out_v["Prod Payroll"][tgt].value)})
R["prod_payroll_refs"] = pp_refs
# Prod Payroll calculated block: error count in output
pp_err = collections.Counter()
pp_total = 0
for row in out_v["Prod Payroll"].iter_rows():
    for c in row:
        if c.value is not None:
            pp_total += 1
            if c.data_type == "e" or (isinstance(c.value, str) and ERR_RE.match(c.value)):
                pp_err[str(c.value)] += 1
R["prod_payroll_cells"] = {"non_empty": pp_total, "errors": dict(pp_err)}
pp_f = [(c.row, c.coordinate) for row in out_f["Prod Payroll"].iter_rows() for c in row if ftext(c.value)]
def _is_err(coord):
    x = out_v["Prod Payroll"][coord]
    return x.data_type == "e" or (isinstance(x.value, str) and bool(ERR_RE.match(x.value.strip())))
pp_ok = [(r, co) for r, co in pp_f if not _is_err(co)]
R["prod_payroll_formulas"] = {"total": len(pp_f), "errors": len(pp_f) - len(pp_ok), "ok": len(pp_ok),
                              "ok_rows": sorted({r for r, _ in pp_ok}),
                              "ok_row_labels": {r: out_v["Prod Payroll"][f"A{r}"].value for r in sorted({r for r, _ in pp_ok})},
                              "total_rows": {r: {"label": out_v["Prod Payroll"][f"A{r}"].value, "S": jsonable(out_v["Prod Payroll"][f"S{r}"].value)}
                                             for r in range(1, out_v["Prod Payroll"].max_row + 1)
                                             if str(out_v["Prod Payroll"][f"A{r}"].value or "").strip().upper().startswith("TOTAL")}}
# PO production payroll rows: typed or linked?
R["po_payroll_rows"] = {r: {"label": val("OUT", "PO", f"A{r}"), "AG": num(val("OUT", "PO", f"AG{r}")) or 0.0,
                            "N": num(val("OUT", "PO", f"N{r}")) or 0.0,
                            "typed_months": sum(1 for c in M27 if ftext(out_f["PO"][f"{c}{r}"].value) is None
                                                and num(out_f["PO"][f"{c}{r}"].value) is not None),
                            "linked_months": sum(1 for c in M27 if ftext(out_f["PO"][f"{c}{r}"].value) and "!" in ftext(out_f["PO"][f"{c}{r}"].value))}
                        for r in (33, 34, 35, 36)}

# ------------------------------------------------------------------ raise timing
def steps(sheet, r):
    vals = [num(val("OUT", sheet, f"{c}{r}")) or 0.0 for c in M27]
    out = []
    for i in range(1, 12):
        if vals[i - 1] and abs(vals[i] / vals[i - 1] - 1) > 1e-6:
            out.append({"col": M27[i], "month": i + 1, "pct": vals[i] / vals[i - 1] - 1})
    return vals, out

raise_rows = []
for sheet, rows in (("PO", (33, 34, 35)), ("CO", (67, 68, 69)), ("PE", (67, 68, 69)), ("FE", (67, 68, 69))):
    for r in rows:
        if not any(num(val("OUT", sheet, f"{c}{r}")) for c in M27):
            continue
        vals, st = steps(sheet, r)
        raise_rows.append({"sheet": sheet, "row": r, "label": val("OUT", sheet, f"A{r}"),
                           "typed": all(ftext(out_f[sheet][f"{c}{r}"].value) is None for c in M27),
                           "source": jsonable(ftext(out_f[sheet][f"U{r}"].value)), "steps": st, "AG": sum(vals)})
R["raise_rows"] = raise_rows
R["raise_inputs"] = {k: cell(*k.split("|")) for k in [
    "OUT|Prod Payroll|M5", "OUT|Prod Payroll|M6", "OUT|Prod Payroll|M9",
    "OUT|Fld Ops Payroll|M5", "OUT|Fld Ops Payroll|M6", "OUT|Fld Ops Payroll|M7",
    "OUT|Fld Eng Budget|B24", "OUT|Fld Eng Budget|B25",
    "SD|Logistics&WH Payroll|B7", "SD|Logistics&WH Payroll|B8", "SD|Logistics&WH Payroll|B9"]}
# eligibility rule present in the formula?
R["raise_rule"] = {
    "Fld Ops Payroll!F21": jsonable(ftext(out_f["Fld Ops Payroll"]["F21"].value)),
    "Fld Eng Budget!B59": jsonable(ftext(out_f["Fld Eng Budget"]["B59"].value)),
    "Logistics&WH Payroll!F34": jsonable(ftext(sd_f["Logistics&WH Payroll"]["F34"].value)),
    "Logistics&WH Payroll!Y15": jsonable(ftext(sd_f["Logistics&WH Payroll"]["Y15"].value)),
}

# ------------------------------------------------------------------ Logistics & WH payroll vs PO
lwh = {"S51_2027": num(val("SD", "Logistics&WH Payroll", "S51")) or 0.0,
       "sum_F51_Q51": rowsum("SD", "Logistics&WH Payroll", 51, DRV27),
       "R51_SepDec26": num(val("SD", "Logistics&WH Payroll", "R51")) or 0.0,
       "headcount_Dec27": num(val("SD", "Logistics&WH Payroll", "Q50")) or 0.0,
       "by_component_2027": {val("SD", "Logistics&WH Payroll", f"A{r}"): rowsum("SD", "Logistics&WH Payroll", r, DRV27)
                             for r in (43, 44, 45, 46)},
       "refs_to_sheet": sum(1 for wbf in (sd_f, coo_f) for ws in wbf.worksheets for row in ws.iter_rows()
                            for c in row if ftext(c.value) and "Logistics&WH" in ftext(c.value)
                            and ws.title != "Logistics&WH Payroll"),
       "po": {r: {"label": val("OUT", "PO", f"A{r}"), "AG": num(val("OUT", "PO", f"AG{r}")) or 0.0,
                  "N": num(val("OUT", "PO", f"N{r}")) or 0.0} for r in (33, 34, 35, 36, 48)},
       "fo_5350": {"AG": num(val("OUT", "FO", "AG48")) or 0.0, "src": jsonable(ftext(out_f["FO"]["U48"].value))},
       "fo_5510_refs": jsonable(ftext(out_f["FO"]["U52"].value))}
# rows of Fld Ops Payroll the FO 5510 formula sums, with their labels (to check for an MH-05 seat)
lwh["fo_5510_rows"] = sorted({int(m.group(1)) for m in re.finditer(r"'Fld Ops Payroll'!F(\d+)", lwh["fo_5510_refs"] or "")})
lwh["fo_5510_row_labels"] = {r: val("OUT", "Fld Ops Payroll", f"A{r}") for r in lwh["fo_5510_rows"]}
lwh["mh05_mentions_outside_lwh"] = [f"{book}:{ws.title}!{c.coordinate}" for book, wbf in (("OUT", out_f), ("SD", sd_f), ("COO", coo_f))
                                    for ws in wbf.worksheets if ws.title not in ("Logistics&WH Payroll", "Collation Notes")
                                    for row in ws.iter_rows() for c in row
                                    if isinstance(c.value, str) and "MH-05" in c.value]
# Rebecca: excluded from LWH (B55) and costed in Fld Ops Payroll row 76
lwh["fop_row76"] = {"label": val("OUT", "Fld Ops Payroll", "A76"), "2027": rowsum("OUT", "Fld Ops Payroll", 76, DRV27)}
R["lwh"] = lwh

# ------------------------------------------------------------------ MeLi / 5310 decomposition
fmb = "Fld Maint Budget"
b10 = num(val("OUT", fmb, "B10")); b11 = num(val("OUT", fmb, "B11"))
meli = {"techs_in_role_cost": sum((num(val("OUT", fmb, f"{c}70")) or 0) * b10 for c in FMB27),
        "merida_cost": sum((num(val("OUT", fmb, f"{c}71")) or 0) * b10 for c in FMB27),
        "supervisor_cost": sum((num(val("OUT", fmb, f"{c}72")) or 0) * b11 for c in FMB27),
        "row84_2027": rowsum("OUT", fmb, 84, FMB27), "row91_2027": rowsum("OUT", fmb, 91, FMB27),
        "fo_AG44": num(val("OUT", "FO", "AG44")) or 0.0,
        "meli_techs_months": [num(val("OUT", fmb, f"{c}70")) for c in FMB27],
        "fop_current_techs_2027": [num(val("OUT", "Fld Ops Payroll", f"{c}20")) for c in DRV27],
        "fop_current_tech_payroll_2027": rowsum("OUT", "Fld Ops Payroll", 24, DRV27),
        "fop_B21_formula": jsonable(ftext(out_f["Fld Ops Payroll"]["B21"].value)),
        "fop_row20_formula": jsonable(ftext(out_f["Fld Ops Payroll"]["F20"].value)),
        "fop_isaiah_2027": rowsum("OUT", "Fld Ops Payroll", 77, DRV27),
        "fop_incr_supervisor_2027": rowsum("OUT", "Fld Ops Payroll", 73, DRV27)}
R["meli"] = meli

# ------------------------------------------------------------------ other quantifications used by issues
q = {}
q["fmb_kits_2027"] = rowsum("OUT", fmb, 78, FMB27)
q["fmb_kits_label"] = val("OUT", fmb, "A78")
q["fop_floater_2027"] = rowsum("OUT", "Fld Ops Payroll", 60, DRV27)
q["fop_expansion_2027"] = rowsum("OUT", "Fld Ops Payroll", 47, DRV27)
q["fop_newlogo_2027"] = rowsum("OUT", "Fld Ops Payroll", 35, DRV27)
q["feb_row67_2027"] = rowsum("OUT", "Fld Eng Budget", 67, FMB27)
q["feb_row67_label"] = val("OUT", "Fld Eng Budget", "A67")
q["fe_AG67"] = num(val("OUT", "FE", "AG67")) or 0.0
# deployment-driven FO/FE lines (rows whose 2027 months link to a driver tab)
drv_lines = []
for d in ("FO", "FE"):
    for r in range(9, 142):
        f = ftext(out_f[d][f"U{r}"].value) or ""
        if any(s in f for s in ("Fld Maint Budget", "Fld Ops Payroll", "Fld Eng Budget")):
            drv_lines.append({"sheet": d, "row": r, "AG": num(val("OUT", d, f"AG{r}")) or 0.0})
q["driver_linked_lines"] = drv_lines
q["driver_linked_total"] = sum(x["AG"] for x in drv_lines)
R["q"] = q

# PO plugs (+N appended to the driver formula) and PE typed overrides
plug_re = re.compile(r"\)\s*\+\s*(\d+(?:\.\d+)?)\s*$")
plugs = []
for r in range(9, 142):
    for c in M27:
        f = ftext(out_f["PO"][f"{c}{r}"].value)
        if f:
            m = plug_re.search(f)
            if m:
                plugs.append({"cell": f"PO!{c}{r}", "plug": float(m.group(1))})
R["po_plugs"] = plugs
over = []
for r in range(9, 142):
    kinds = {c: ftext(out_f["PE"][f"{c}{r}"].value) is not None for c in M27}
    if any(kinds.values()) and not all(kinds.values()):
        for c, isf in kinds.items():
            v = num(out_f["PE"][f"{c}{r}"].value)
            if not isf and v is not None:
                over.append({"cell": f"PE!{c}{r}", "typed": v})
R["pe_overrides"] = over

# ------------------------------------------------------------------ frozen cells
frozen = [e for e in ext["external_cells"] if not (isinstance(e["stored"], str) and e["stored"].startswith("#"))]
frozen_refs = {f"{e['sheet']}!{e['cell']}" for e in frozen}
deps = []
REF1 = re.compile(r"(?:(?:'([^']+)'|([A-Za-z][A-Za-z0-9 ]*))!)?\$?([A-Z]{1,3})\$?(\d+)")
for ws in out_f.worksheets:
    for row in ws.iter_rows():
        for c in row:
            f = ftext(c.value)
            if not f:
                continue
            for m in REF1.finditer(f):
                sh = m.group(1) or m.group(2) or ws.title
                if f"{sh}!{m.group(3)}{m.group(4)}" in frozen_refs:
                    deps.append({"cell": f"{ws.title}!{c.coordinate}", "formula": f, "value": jsonable(out_v[ws.title][c.coordinate].value)})
                    break
R["frozen"] = {"cells": [f"{e['sheet']}!{e['cell']}" for e in frozen],
               "values": dict(collections.Counter(str(e["stored"]) for e in frozen)),
               "dependents": deps,
               "dependent_values": dict(collections.Counter(str(d["value"]) for d in deps)),
               "comments_in_output": {k: (out_f[k.split("!")[0]][k.split("!")[1]].comment.text
                                          if out_f[k.split("!")[0]][k.split("!")[1]].comment else None)
                                      for k in sorted(frozen_refs)}}

# ------------------------------------------------------------------ misc facts the v1 report typed in
R["tab_positions"] = {s: out_f.sheetnames.index(s) + 1 for s in out_f.sheetnames}
R["coo_tab_positions"] = {s: coo_f.sheetnames.index(s) + 1 for s in coo_f.sheetnames}
R["deploysum_hidden_rows"] = sorted(k for k, d in out_f["DeploySum"].row_dimensions.items() if d.hidden)
ds_forms = [ftext(c.value) for row in out_f["DeploySum"].iter_rows() for c in row if ftext(c.value)]
R["deploysum_formula_mix"] = {"total": len(ds_forms),
                              "error_constant": sum(1 for f in ds_forms if re.fullmatch(r"=#(REF!|N/A|NAME\?|VALUE!|DIV/0!|NUM!|NULL!)", f)),
                              "frozen_numbers": sum(1 for e in ext["external_cells"] if isinstance(e["stored"], (int, float)))}
R["deploysum_drivers_R"] = {r: {"label": val("OUT", "DeploySum", f"A{r}"), "R": num(val("OUT", "DeploySum", f"R{r}")),
                                "R_typed": ftext(out_f["DeploySum"][f"R{r}"].value) is None} for r in (54, 57, 60)}
# formula-difference columns FO/FE (COO book vs SD book), rows 1-200, cols A:AJ
fd_cols = collections.Counter()
fd_rows = collections.defaultdict(set)
for d in ("FO", "FE"):
    for r in range(1, 201):
        for ci in range(1, 37):
            a = ftext(coo_f[d].cell(r, ci).value); b = ftext(sd_f[d].cell(r, ci).value)
            if (a or b) and a != b:
                fd_cols[get_column_letter(ci)] += 1
                fd_rows[d].add(r)
R["formula_diff_cols"] = dict(fd_cols)
R["formula_diff_rows"] = {d: sorted(v) for d, v in fd_rows.items()}
# references between FE and Fld Eng Budget
def count_refs(ws, target):
    n = 0
    for row in ws.iter_rows():
        for c in row:
            f = ftext(c.value)
            if f:
                n += len(re.findall(r"(?:'%s'|%s)!" % (re.escape(target), re.escape(target)), f))
    return n
R["fe_feb_refs"] = {"Fld Eng Budget->FE": count_refs(out_f["Fld Eng Budget"], "FE"),
                    "FE->Fld Eng Budget": count_refs(out_f["FE"], "Fld Eng Budget")}
# error totals
def err_total(wbv, sheets, typed):
    out = {}
    for s in sheets:
        n = collections.Counter()
        for row in wbv[s].iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and ERR_RE.match(v.strip()) and (not typed or c.data_type == "e"):
                    n[v] += 1
        out[s] = dict(n)
    return out
R["errors_sd"] = err_total(sd_v, ["DeploySum", "Prod Payroll"], False)
R["errors_out"] = err_total(out_v, ["DeploySum", "Prod Payroll"], True)
# page setup / print settings: source vs output for carried and COO sheets
ps = []
for s in ext["carried"] + ["COO P&L", "PO", "CO", "PE"]:
    src = sd_f[s] if s in ext["carried"] else coo_f[s]
    o = out_f[s]
    ps.append({"sheet": s, "src_orientation": src.page_setup.orientation, "out_orientation": o.page_setup.orientation,
               "src_print_area": src.print_area, "out_print_area": o.print_area,
               "src_print_titles": src.print_title_rows or src.print_title_cols, "out_print_titles": o.print_title_rows or o.print_title_cols,
               "src_fit_to_page": src.sheet_properties.pageSetUpPr.fitToPage if src.sheet_properties.pageSetUpPr else None,
               "out_fit_to_page": o.sheet_properties.pageSetUpPr.fitToPage if o.sheet_properties.pageSetUpPr else None})
R["page_setup"] = ps
R["sd_defined_names"] = {k: v.attr_text for k, v in sd_f.defined_names.items()}
R["sd_sheet_scoped_names"] = {ws.title: list(ws.defined_names.keys()) for ws in sd_f.worksheets if ws.defined_names}
# placeholder keyword counts (same scan as analyze.py)
PH = re.compile(r"PLACEHOLDER|TBD|AI suggested|assumed", re.I)
phc = collections.Counter()
for wbf in (coo_f, sd_f):
    for ws in wbf.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                t = v if isinstance(v, str) else ftext(v)
                if t and PH.search(t):
                    phc[PH.search(t).group(0).upper()] += 1
                if c.comment and PH.search(c.comment.text or ""):
                    phc[PH.search(c.comment.text).group(0).upper()] += 1
R["placeholder_keywords"] = dict(phc)
# I-10 lines: 2026 values
R["zero_2027_lines"] = [{"cell": f"{d}!AG{r}", "label": val("OUT", d, f"A{r}"), "N": num(val("OUT", d, f"N{r}")) or 0.0,
                         "AG": num(val("OUT", d, f"AG{r}")) or 0.0}
                        for d in ("FO", "FE") for r in range(9, 117)
                        if GL_RE.match((val("OUT", d, f"A{r}") or "").strip())
                        and abs(num(val("OUT", d, f"N{r}")) or 0) > 50000 and abs(num(val("OUT", d, f"AG{r}")) or 0) < 0.5]
R["versions"] = {"openpyxl": openpyxl.__version__, "python": sys.version.split()[0]}


def bbox(cells):
    if not cells:
        return None
    rs = [c[0] for c in cells]; cs = [c[1] for c in cells]
    return f"{get_column_letter(min(cs))}{min(rs)}:{get_column_letter(max(cs))}{max(rs)}"


def error_cells(wbv, sheet):
    return [(c.row, c.column) for row in wbv[sheet].iter_rows() for c in row
            if c.value is not None and (c.data_type == "e" or (isinstance(c.value, str) and ERR_RE.match(c.value.strip())))]

R["error_bbox"] = {"Prod Payroll": bbox(error_cells(out_v, "Prod Payroll")),
                   "DeploySum": bbox(error_cells(out_v, "DeploySum"))}
ext_rc = [(int(re.sub(r"[A-Z]", "", e["cell"])), column_index_from_string(re.sub(r"\d", "", e["cell"]))) for e in ext["external_cells"]]
R["ext_bbox"] = {"all": bbox(ext_rc),
                 "col_A": sorted(r for r, c in ext_rc if c == 1),
                 "grid": bbox([(r, c) for r, c in ext_rc if c > 1])}
te = sd_v["Fld Maint T&E Data"]
R["te_extent"] = {"max_row": te.max_row, "header_M4": te["M4"].value, "first_data_row": 5}
# Fld Eng Budget cells that read FE, and FE 2027 rows that read Fld Eng Budget
feb_rows = sorted({c.row for row in out_f["Fld Eng Budget"].iter_rows() for c in row
                   if ftext(c.value) and re.search(r"(?<![A-Za-z ])FE!", ftext(c.value))})
R["feb_reads_fe_rows"] = feb_rows
R["fe_reads_feb_rows"] = sorted({c.row for row in out_f["FE"].iter_rows() for c in row
                                 if ftext(c.value) and "Fld Eng Budget" in ftext(c.value)})
R["fo_reads_drivers_rows"] = {s: sorted({c.row for row in out_f["FO"].iter_rows() for c in row
                                         if ftext(c.value) and s in ftext(c.value)})
                              for s in ("Fld Maint Budget", "Fld Ops Payroll")}
R["fop_new_hire_2027"] = sum(rowsum("OUT", "Fld Ops Payroll", r, DRV27) for r in (34, 46, 59, 72))
R["fop_new_hire_rows"] = {r: val("OUT", "Fld Ops Payroll", f"A{r}") for r in (34, 46, 59, 72)}
# hidden sheets in SD book / output
R["sd_hidden_sheets"] = [ws.title for ws in sd_f.worksheets if ws.sheet_state != "visible"]
R["out_hidden_sheets"] = [ws.title for ws in out_f.worksheets if ws.sheet_state != "visible"]
# Old Draft text quoted in I-14
R["old_draft_B142"] = sd_v["Old Draft"]["B142"].value
R["sd_sheetnames"] = sd_f.sheetnames
# COO P&L rows 23/24/27 labels and row-23 emptiness on every tab
R["row23"] = {s: {"A23": val("OUT", s, "A23"), "A24": val("OUT", s, "A24"),
                  "B27": jsonable(ftext(out_f[s]["B27"].value)),
                  "row23_nonempty": sum(1 for c in range(2, 37) if out_f[s].cell(23, c).value not in (None, ""))}
              for s in ["COO P&L"] + DEPTS}
R["coo_pl_row65"] = {"A65": val("OUT", "COO P&L", "A65"), "B65": jsonable(ftext(out_f["COO P&L"]["B65"].value)),
                     "AG65": val("OUT", "COO P&L", "U65")}

json.dump(R, open(RES_JSON, "w"), indent=1, default=str)
print("overlap rows", [(o["row"], o["nonzero"]) for o in ov])
print("prod payroll refs", [(p["from"], p["target"], p["target_label"], p["target_is_formula"]) for p in pp_refs])
print("raise", [(x["sheet"], x["row"], [(s["col"], round(s["pct"], 4)) for s in x["steps"]]) for x in raise_rows])
print("lwh", lwh["S51_2027"], lwh["fo_5510_row_labels"], lwh["mh05_mentions_outside_lwh"])
print("meli", {k: v for k, v in meli.items() if not isinstance(v, list)})
print("frozen", R["frozen"]["values"], "deps", R["frozen"]["dependent_values"])
print("plugs", plugs, "overrides", sum(o["typed"] for o in over))
print("zero lines", R["zero_2027_lines"])
print("page setup diffs", [p for p in ps if p["src_orientation"] != p["out_orientation"] or p["src_print_area"] != p["out_print_area"]])
