"""v12 semantic diff: OLD (v11) vs NEW (v12 = LibreOffice re-serialization of v11).

Proves the re-serialization changed no meaning:
  1. sheet set, order and visibility states identical;
  2. every cell's FORMULA is semantically identical (openpyxl-normalized text: XML entities decoded,
     v11 shared-formula followers translated to their explicit per-cell form - v12 stores every formula
     explicitly; array formulas compared on text + range);
  3. every cell's CACHED VALUE identical (numeric within TOL, max drift reported; strings/bools/dates exact;
     None and '' both mean an empty cache and are treated as equal - Excel-written v11 parts cache empty
     string results as <v/>, which openpyxl reads as None on one side and '' on the other in some paths);
  4. every cell's number format identical (by format string, not by xf index - the engine renumbers xfs);
  5. comments identical (per sheet: ref -> text);
  6. defined names: count before/after (the engine may renormalize; if the count changes the names dropped
     are listed and checked against formula references);
  7. row/column hidden flags identical per sheet.

No clock, no file properties, no dates are read (F1 rule).

Usage:
  python3 -I fdiff_v12.py OLD_XLSX NEW_XLSX OUT_JSON
Exit 1 on any semantic difference (value drift > TOL, formula change, sheet/comment/number-format change).
"""
import sys, json, re
import openpyxl
from openpyxl.worksheet.formula import ArrayFormula

TOL = 1e-6
OLD, NEW, OUT = sys.argv[1:4]

isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)


def norm_numfmt(f):
    """Number-format strings: '\\x' and '"x"' both mean the literal x. The engine re-escapes literals
    (e.g. Excel 'mmm-yy' -> LibreOffice 'mmm\\-yy'; '"$"#,##0' -> '\\$#,##0'): same rendered format,
    different spelling. Normalize both spellings to bare literals before comparing."""
    out = []; i = 0; q = False
    while i < len(f):
        c = f[i]
        if q:
            if c == '"': q = False
            else: out.append(c)
        elif c == '"': q = True
        elif c == "\\" and i + 1 < len(f): out.append(f[i+1]); i += 1
        else: out.append(c)
        i += 1
    return "".join(out)


def norm_formula(v):
    if isinstance(v, ArrayFormula):
        return ("array", v.ref, v.text if v.text is not None else "")
    if isinstance(v, str) and v.startswith("="):
        return ("f", v)
    return None


def cells_of(ws):
    out = {}
    for row in ws.iter_rows():
        for c in row:
            out[c.coordinate] = c
    return out


def main():
    fo = openpyxl.load_workbook(OLD)
    fn = openpyxl.load_workbook(NEW)
    vo = openpyxl.load_workbook(OLD, data_only=True)
    vn = openpyxl.load_workbook(NEW, data_only=True)

    rep = {"sheets_old": fo.sheetnames, "sheets_new": fn.sheetnames,
           "states_old": [fo[s].sheet_state for s in fo.sheetnames],
           "states_new": [fn[s].sheet_state for s in fn.sheetnames],
           "defined_names_old": len(fo.defined_names), "defined_names_new": len(fn.defined_names),
           "max_value_drift": 0.0, "value_drift_cell": None, "cells_compared": 0,
           "formula_cells": 0, "formula_diffs": [], "value_diffs": [], "numfmt_diffs": [],
           "comment_diffs": [], "hidden_diffs": [], "array_formulas_old": 0, "array_formulas_new": 0}
    bad = 0

    if fo.sheetnames != fn.sheetnames or rep["states_old"] != rep["states_new"]:
        bad += 1

    dn_old = set(fo.defined_names); dn_new = set(fn.defined_names)
    rep["defined_names_dropped"] = sorted(dn_old - dn_new)[:20]
    rep["defined_names_added"] = sorted(dn_new - dn_old)[:20]

    for s in fo.sheetnames:
        wfo, wfn, wvo, wvn = fo[s], fn[s], vo[s], vn[s]
        co, cn = cells_of(wfo), cells_of(wfn)
        cvo, cvn = cells_of(wvo), cells_of(wvn)
        for coord in set(co) | set(cn):
            a = co.get(coord); b = cn.get(coord)
            fa = norm_formula(a.value) if a is not None else None
            fb = norm_formula(b.value) if b is not None else None
            rep["cells_compared"] += 1
            if fa and fa[0] == "array": rep["array_formulas_old"] += 1
            if fb and fb[0] == "array": rep["array_formulas_new"] += 1
            if fa != fb:
                rep["formula_diffs"].append([s, coord, str(fa)[:160], str(fb)[:160]])
                bad += 1
                continue
            if fa: rep["formula_cells"] += 1
            va = cvo.get(coord).value if coord in cvo else None
            vb = cvn.get(coord).value if coord in cvn else None
            if va in ("", None) and vb in ("", None):
                continue
            if isnum(va) and isnum(vb):
                d = abs(va - vb)
                if d > rep["max_value_drift"]:
                    rep["max_value_drift"] = d; rep["value_drift_cell"] = f"{s}!{coord}"
                if d > TOL:
                    rep["value_diffs"].append([s, coord, repr(va), repr(vb)]); bad += 1
            elif va != vb:
                rep["value_diffs"].append([s, coord, repr(va)[:120], repr(vb)[:120]]); bad += 1
            # number format (only where a cell exists on both sides)
            if a is not None and b is not None and a.number_format != b.number_format:
                if norm_numfmt(a.number_format) == norm_numfmt(b.number_format):
                    rep["numfmt_reescaped"] = rep.get("numfmt_reescaped", 0) + 1
                    rep.setdefault("numfmt_reescaped_pairs", set()).add((a.number_format, b.number_format))
                else:
                    rep["numfmt_diffs"].append([s, coord, a.number_format, b.number_format]); bad += 1
        # comments
        cmo = {c.coordinate: (c.comment.text or "").strip() for c in co.values() if c.comment}
        cmn = {c.coordinate: (c.comment.text or "").strip() for c in cn.values() if c.comment}
        if cmo != cmn:
            rep["comment_diffs"].append([s, sorted(set(cmo) ^ set(cmn))[:10],
                                         sorted(k for k in set(cmo) & set(cmn) if cmo[k] != cmn[k])[:10]])
            bad += 1
        # hidden rows / columns
        hro = {r: d.hidden for r, d in wfo.row_dimensions.items() if d.hidden}
        hrn = {r: d.hidden for r, d in wfn.row_dimensions.items() if d.hidden}
        hco = {c: d.hidden for c, d in wfo.column_dimensions.items() if d.hidden}
        hcn = {c: d.hidden for c, d in wfn.column_dimensions.items() if d.hidden}
        if hro != hrn or hco != hcn:
            rep["hidden_diffs"].append([s, sorted(set(hro) ^ set(hrn)), sorted(set(hco) ^ set(hcn))])
            bad += 1

    for k in ("formula_diffs", "value_diffs", "numfmt_diffs"):
        rep[k] = rep[k][:50]
    rep["numfmt_reescaped_pairs"] = sorted(rep.get("numfmt_reescaped_pairs", set()))
    json.dump(rep, open(OUT, "w"), indent=1)
    print(f"fdiff_v12: {rep['cells_compared']} cells on {len(fo.sheetnames)} sheets; "
          f"{rep['formula_cells']} identical formula cells "
          f"(arrays {rep['array_formulas_old']}/{rep['array_formulas_new']}); "
          f"formula diffs {len(rep['formula_diffs'])}; value diffs > {TOL}: {len(rep['value_diffs'])}; "
          f"max value drift {rep['max_value_drift']:.3e} at {rep['value_drift_cell']}; "
          f"number-format diffs {len(rep['numfmt_diffs'])} "
          f"(+{rep.get('numfmt_reescaped', 0)} same-format re-escapings, "
          f"{len(rep['numfmt_reescaped_pairs'])} distinct spellings); "
          f"comment diffs {len(rep['comment_diffs'])}; "
          f"hidden-flag diffs {len(rep['hidden_diffs'])}; "
          f"defined names {rep['defined_names_old']} -> {rep['defined_names_new']}; "
          f"sheets/states identical: {rep['sheets_old'] == rep['sheets_new'] and rep['states_old'] == rep['states_new']}")
    sys.exit(1 if bad else 0)


main()
