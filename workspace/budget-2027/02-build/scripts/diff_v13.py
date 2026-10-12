"""v13 confined diff: v12 -> v13 cell-by-cell (formulas, cached values, comments) with per-sheet allowlists.

Rules (CONSTRAINTS of the v13 handoff). A violation = any difference outside them; exit 1.
  COO P&L            formulas: none. values: 2027-side columns U..AJ (21-36) only.
  CO                 formulas: S98/S106 are value cells; U67:AF69 + AI67:AI69 only. values: S98/S106; U..AJ on rows
                     67-69, 73, 98, 106, 116, 117, 132, 137-142; AI67:AI69.
  PE                 formulas: U67:AF69 + AI67:AI69. values: U..AJ on rows 67-69, 73, 116, 117, 132, 137-142; AI.
  PO                 formulas: U33:AF35, U67:AF69, AI33:AI35, AI67:AI69. values: U..AJ on rows 33-37, 67-69, 73,
                     116, 117, 132, 137-142; AI rows 33-35, 67-69.
  FO                 formulas: none. values: U..AJ only (the B11 recalc: 5330 + 5510-chain + subtotals/ratios).
  FE, HC-FO, Logistics&WH Payroll, DeploySum, Prod Payroll, Depreciation Schedule, Old sheets: nothing changes.
  Fld Ops Payroll    formulas: none. values: B11 (the one typed change) + formula cells (recalc) only.
  Fld Maint Budget   formulas: none. values: formula cells only (B29 chain).
  HC-CO/PO/FE/PE     formulas: none. values: input cells (B..F) on the listed roster rows + formula cells (recalc).
  HC-COO             formulas: none. values: formula cells only.
  Collation Notes    excluded from confinement (updated in place + v13 block); counted and reported only.
Comments: no changes anywhere. 2026 columns (B:N) of the six P&L sheets: no changes (implied by the column rules).
HC-tab differences are reported as coordinates only - never values (column B holds names).

Usage:
  python3 -I diff_v13.py V12_XLSX V13_XLSX OUT_JSON
"""
import sys, json, datetime
import openpyxl
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.utils import get_column_letter, column_index_from_string

OLD, NEW, OUT = sys.argv[1:4]
TOL = 1e-6
U, AJ, S, AI = 21, 36, 19, 35
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)

ROSTER_INPUT = {"HC-CO": {18, 19, 20, 35, 36}, "HC-PO": {20, 41}, "HC-FE": {20}, "HC-PE": {35, 36, 37, 38, 41}}
PL_ROWS = {"CO": {67, 68, 69, 73, 98, 106, 116, 117, 132, 137, 138, 139, 140, 141, 142},
           "PE": {67, 68, 69, 73, 116, 117, 132, 137, 138, 139, 140, 141, 142},
           "PO": {33, 34, 35, 36, 37, 67, 68, 69, 73, 116, 117, 132, 137, 138, 139, 140, 141, 142}}
F_ALLOWED = {"CO": {(r, c) for r in (67, 68, 69) for c in list(range(U, 33)) + [AI]},
             "PE": {(r, c) for r in (67, 68, 69) for c in list(range(U, 33)) + [AI]},
             "PO": {(r, c) for r in (33, 34, 35, 67, 68, 69) for c in list(range(U, 33)) + [AI]},
             "Collation Notes": {(78, 8), (79, 8), (80, 8)}}
FROZEN = {"FE", "HC-FO", "Logistics&WH Payroll", "DeploySum", "Prod Payroll", "Depreciation Schedule"}


def value_allowed(sheet, r, c, old_has_formula):
    if sheet == "Collation Notes":
        return True
    if sheet == "COO P&L" or sheet == "FO":
        return U <= c <= AJ
    if sheet in PL_ROWS:
        if sheet == "CO" and r in (98, 106) and c == S:
            return True
        return r in PL_ROWS[sheet] and (U <= c <= AJ or c == AI)
    if sheet in ROSTER_INPUT:
        return (r in ROSTER_INPUT[sheet] and 2 <= c <= 6) or old_has_formula
    if sheet == "Fld Ops Payroll":
        return (r, c) == (11, 2) or old_has_formula
    if sheet in ("Fld Maint Budget", "HC-COO"):
        return old_has_formula
    return False


def norm_f(v):
    if isinstance(v, ArrayFormula):
        return ("array", v.ref, v.text or "")
    return v if isinstance(v, str) and v.startswith("=") else None


def norm_v(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()
    return v


of, ov = openpyxl.load_workbook(OLD), openpyxl.load_workbook(OLD, data_only=True)
nf, nv = openpyxl.load_workbook(NEW), openpyxl.load_workbook(NEW, data_only=True)
assert of.sheetnames == nf.sheetnames, "sheet set/order changed"

viol, report, cn_count = [], {}, {"formula": 0, "value": 0}
for sh in of.sheetnames:
    o_f, o_v, n_f, n_v = of[sh], ov[sh], nf[sh], nv[sh]
    rows = max(o_f.max_row, n_f.max_row)
    cols = max(o_f.max_column, n_f.max_column)
    fdiff = vdiff = 0
    cells = []
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            fo, fn = norm_f(o_f.cell(r, c).value), norm_f(n_f.cell(r, c).value)
            a, b = norm_v(o_v.cell(r, c).value), norm_v(n_v.cell(r, c).value)
            if fo is None and fn is None:
                a2 = o_f.cell(r, c).value; b2 = n_f.cell(r, c).value
                a, b = norm_v(a2) if a2 is not None else a, norm_v(b2) if b2 is not None else b
            f_changed = fo != fn
            if isnum(a) and isnum(b):
                v_changed = abs(a - b) > TOL
            else:
                v_changed = (a if a != "" else None) != (b if b != "" else None)
            if not f_changed and not v_changed:
                continue
            coord = f"{get_column_letter(c)}{r}"
            if sh == "Collation Notes":
                cn_count["formula" if f_changed else "value"] += 1
                if f_changed and (r, c) not in F_ALLOWED["Collation Notes"] and r < 812:
                    viol.append(f"Collation Notes!{coord}: formula changed outside H78:H80")
                continue
            if sh in FROZEN:
                viol.append(f"{sh}!{coord}: {'formula' if f_changed else 'value'} changed on a frozen sheet")
                continue
            if f_changed:
                if sh not in F_ALLOWED or (r, c) not in F_ALLOWED[sh]:
                    viol.append(f"{sh}!{coord}: formula changed outside the allowed set")
                fdiff += 1
            if v_changed:
                if not value_allowed(sh, r, c, fo is not None):
                    viol.append(f"{sh}!{coord}: value changed outside the allowed areas")
                vdiff += 1
            if len(cells) < 400:
                cells.append(coord)
    if fdiff or vdiff:
        report[sh] = {"formula_diffs": fdiff, "value_diffs": vdiff,
                      "cells": cells if not sh.startswith("HC-") else cells}  # coordinates only, never values
# comments
for sh in of.sheetnames:
    oc = {c.coordinate: (c.comment.text if c.comment else None) for row in of[sh].iter_rows() for c in row if c.comment}
    ncm = {c.coordinate: (c.comment.text if c.comment else None) for row in nf[sh].iter_rows() for c in row if c.comment}
    if oc != ncm:
        viol.append(f"{sh}: comments changed")
# 2026 columns of the six P&L sheets (B:N = 2-14): assert explicitly for the report
for sh in ("COO P&L", "FO", "PO", "CO", "FE", "PE"):
    for r in range(1, of[sh].max_row + 1):
        for c in range(2, 15):
            a, b = ov[sh].cell(r, c).value, nv[sh].cell(r, c).value
            same = abs(a - b) <= TOL if (isnum(a) and isnum(b)) else (a if a != "" else None) == (b if b != "" else None)
            if not same:
                viol.append(f"{sh}!{get_column_letter(c)}{r}: 2026 column changed")

out = {"violations": viol, "per_sheet": report, "collation_notes_changed_cells": cn_count,
       "names_note": "HC-tab diffs listed as coordinates only"}
json.dump(out, open(OUT, "w"), indent=1)
total_f = sum(x["formula_diffs"] for x in report.values())
total_v = sum(x["value_diffs"] for x in report.values())
print(f"diff_v13: {total_f} formula / {total_v} value diffs outside Collation Notes "
      f"(Collation Notes: {cn_count}); violations: {len(viol)}")
for v in viol[:40]:
    print("VIOLATION", v)
sys.exit(1 if viol else 0)
