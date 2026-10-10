"""v11 checks. Exit 1 if any completion criterion fails.

Usage:
  python3 -I analyze_v11.py V10_XLSX V11_XLSX V11_RECALC_XLSX DIFF_JSON NOTES_JSON NOTES_MD PRIVACY_TXT PAYLIST_TXT OUT_JSON

Criteria (handoff v11):
  - diff v10 -> v11 confined to PO!AI33:AI35 (3 text cells) and the regenerated Collation Notes; 0 formula and 0 value
    differences on every other sheet; comments / sheet set unchanged; package parts changed = the PO part and the
    Collation Notes part only, none added or removed (every other part byte-identical);
  - COO P&L!AG132 unchanged: formula and cached value identical to v10; cached value rounds to 159,136.40;
  - LibreOffice recalculation of v11: 0 error cells; stored = recalculated on every sheet except Collation Notes
    (<= 1e-6, non-numeric identical); COO P&L = sum of the 5 depts; check row 133 = 0;
  - Collation Notes: every formula cell (36, incl. the new live checks H78:H81) = recalculation; H78:H81 are formulas
    and their recalculated |check| <= 1e-6; first section = CONFIDENTIAL banner;
  - the six fixes present (md + Collation Notes + PO cells); the false F1 sentence gone from the md and from every
    part of the workbook; the workfile's real 2026-10-07 date kept;
  - privacy_v6 / paylist found nothing.

The OUT_JSON carries the computed numbers report_v11.py pass 2 writes into the md; it contains no paths, no times
and no md-dependent fields, so the two runs of analyze_v11.py in one pass (on the pass-1 md and on the final md)
produce byte-identical OUT_JSONs.
"""
import sys, os, re, json, zipfile, datetime, collections
import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string as ci
from openpyxl.worksheet.formula import ArrayFormula

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_v8

V10, V11, LO11, DIFF, NJ, MD, PRIV, PAY, OUT = sys.argv[1:10]
BANNER = "CONFIDENTIAL – contains named compensation data (HC-* tabs); restrict distribution"
ERR = re.compile(r"^#(REF!|NAME\?|VALUE!|DIV/0!|N/A|NUM!|NULL!)$")
FALSE_PATS = ("a re-save, not the model date", "properties show 2026-10-09")
FIX_SENT = ("the SD workbook carries no document properties, so its save date cannot be read from the file; "
            "the model's as-of date is unknown")
CN = "Collation Notes"
fails = []
res = {}


def check(cond, msg):
    if not cond:
        fails.append(msg)


def norm(v):
    if isinstance(v, ArrayFormula):
        return ("array", v.ref, v.text)
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()
    return v


isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
f10 = openpyxl.load_workbook(V10); v10 = openpyxl.load_workbook(V10, data_only=True)
f11 = openpyxl.load_workbook(V11); v11 = openpyxl.load_workbook(V11, data_only=True)
lo = openpyxl.load_workbook(LO11, data_only=True)
d = json.load(open(DIFF))
U, AF, AG = ci("U"), ci("AF"), ci("AG")

# 1. cell diff confined to PO!AI33:AI35 (strings both sides); verified directly, not only via diff_versions
outside = []
po_cells = []
for s in f10.sheetnames:
    if s == CN:
        continue
    a_f, b_f, a_v, b_v = f10[s], f11[s], v10[s], v11[s]
    mr = max(a_f.max_row, b_f.max_row); mc = max(a_f.max_column, b_f.max_column)
    for r in range(1, mr + 1):
        for c in range(1, mc + 1):
            fa, fb = norm(a_f.cell(r, c).value), norm(b_f.cell(r, c).value)
            va, vb = norm(a_v.cell(r, c).value), norm(b_v.cell(r, c).value)
            if fa == fb and va == vb:
                continue
            coord = f"{get_column_letter(c)}{r}"
            if s == "PO" and coord in ("AI33", "AI34", "AI35") and isinstance(fa, str) and isinstance(fb, str) \
                    and not fa.startswith("=") and not fb.startswith("="):
                po_cells.append(coord)
            else:
                outside.append(f"{s}!{coord}")
check(not outside, f"changes outside PO!AI33:AI35: {outside[:10]}")
check(sorted(po_cells) == ["AI33", "AI34", "AI35"], f"PO note cells changed: {sorted(po_cells)}")
check(f10.sheetnames == f11.sheetnames and not d["sheets_only_in_new"] and not d["sheets_only_in_old"], "sheet set")
check([len(d["comments_added"]), len(d["comments_removed"]), len(d["comments_changed"])] == [0, 0, 0], "comments changed")
check(d["total"]["formula_diffs"] == 3 and d["total"]["value_diffs"] == 3
      and d["sheets"]["PO"]["formula_diffs"] == 3 and d["sheets"]["PO"]["value_diffs"] == 3
      and all(v["formula_diffs"] == 0 and v["value_diffs"] == 0 for k, v in d["sheets"].items() if k != "PO"),
      f"diff_versions totals not 3+3 on PO only: {d['total']}")
res["diff_total"] = d["total"]
res["po_cells"] = sorted(po_cells)

# 2. package parts
z10, z11 = zipfile.ZipFile(V10), zipfile.ZipFile(V11)
n10, n11 = set(z10.namelist()), set(z11.namelist())
changed = sorted(p for p in n10 & n11 if z10.read(p) != z11.read(p))
po_part, cn_part = build_v8.part_of(z11, "PO"), build_v8.part_of(z11, CN)
check(not (n10 - n11) and not (n11 - n10), "parts added/removed")
check(set(changed) == {po_part, cn_part}, f"parts changed: {changed}")
res["parts_changed"] = changed
res["parts_added"] = sorted(n11 - n10)

# 3. AG132
ag_f10, ag_f11 = f10["COO P&L"]["AG132"].value, f11["COO P&L"]["AG132"].value
ag_v10, ag_v11 = v10["COO P&L"]["AG132"].value, v11["COO P&L"]["AG132"].value
check(ag_f10 == ag_f11 and ag_v10 == ag_v11, "AG132 changed")
check(round(ag_v11, 2) == 159136.40, f"AG132 = {ag_v11}")
res["ag132"] = {"v10": ag_v10, "v11": ag_v11}

# 4. recalculation vs stored; 0 error cells
errors = []
mx = 0.0; ncells = 0; nonnum = []
for s in v11.sheetnames:
    for row in lo[s].iter_rows():
        for c in row:
            if isinstance(c.value, str) and ERR.match(c.value):
                errors.append(f"{s}!{c.coordinate}")
    if s == CN:
        continue
    a, b = v11[s], lo[s]
    for row in a.iter_rows():
        for c in row:
            x, y = c.value, b[c.coordinate].value
            if x is None and y is None:
                continue
            if isnum(x) and isnum(y):
                ncells += 1; mx = max(mx, abs(x - y))
            elif norm(x) != norm(y) and not (x in (None, "") and y in (None, "")):
                nonnum.append(f"{s}!{c.coordinate}")
check(not errors, f"error cells: {errors[:5]}")
check(mx <= 1e-6, f"stored vs recalculated max diff {mx}")
check(not nonnum, f"non-numeric stored vs recalculated differences {nonnum[:5]}")
res["recalc"] = {"max": mx, "cells": ncells, "nonnum": len(nonnum), "errors": len(errors)}

# 5. COO P&L = sum of depts (on the recalculated file)
c_f = f11["COO P&L"]
smax = 0.0; nrows = 0
for r in range(1, c_f.max_row + 1):
    fv = c_f.cell(r, U).value
    if isinstance(fv, str) and re.fullmatch(rf"=SUM\(FO!U{r},PO!U{r},CO!U{r},FE!U{r},PE!U{r}\)", fv):
        nrows += 1
        for c in list(range(U, AF + 1)) + [AG]:
            tot = sum((lo[dp].cell(r, c).value or 0) for dp in ("FO", "PO", "CO", "FE", "PE") if isnum(lo[dp].cell(r, c).value))
            v = lo["COO P&L"].cell(r, c).value
            smax = max(smax, abs((v if isnum(v) else 0) - tot))
r133 = max(abs(lo["COO P&L"].cell(133, c).value or 0) for c in range(U, AF + 1))
res["sum_depts"] = {"max": smax, "rows": nrows, "row133": r133}
check(nrows > 50 and smax < 1e-6, f"COO P&L != sum of depts ({smax})")
check(r133 < 1e-6, "check row 133")

# 6. Collation Notes: formulas = recalculation; H78:H81 live and 0; banner
cnf, cnv, cnl = f11[CN], v11[CN], lo[CN]
cnmax = 0.0; ncn = 0; cnbad = []
for row in cnf.iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("="):
            ncn += 1
            x, y = cnv[c.coordinate].value, cnl[c.coordinate].value
            if isnum(x) and isnum(y):
                cnmax = max(cnmax, abs(x - y))
            elif x != y:
                cnbad.append(c.coordinate)
hvals = []
for k in ("H78", "H79", "H80", "H81"):
    fv = cnf[k].value
    check(isinstance(fv, str) and fv.startswith("="), f"Collation Notes {k} is not a formula")
    check("'Logistics&WH Payroll'" in fv if k != "H81" else fv == "=SUM(H78:H80)", f"{k} formula: {fv}")
    hvals.append(cnl[k].value)
hmax = max(abs(v) for v in hvals if isnum(v)) if all(isnum(v) for v in hvals) else float("inf")
check(hmax <= 1e-6, f"H78:H81 recalculated checks not 0: {hvals}")
check(not cnbad and cnmax < 1e-6, f"Collation Notes formulas differ from the recalculation (max {cnmax}, bad {cnbad})")
NJd = json.load(open(NJ))
check(NJd["sections"][0]["heading"] == BANNER, "banner")
check(NJd["title"].endswith("(build v11, draft for review)"), "Collation Notes title not v11")
res["cn"] = {"formulas": ncn, "max": cnmax, "h": hvals, "h_max": hmax}
check(ncn == 36, f"Collation Notes formula count {ncn} != 36 (32 v10 + H78:H81)")

# 7. the six fixes present; the false sentence gone
md = open(MD, encoding="utf-8").read()
cn_text = json.dumps(NJd, ensure_ascii=False)
zparts_text = "".join(z11.read(p).decode("utf-8", "ignore") for p in z11.namelist() if p.endswith((".xml", ".vml", ".rels")))
false_md = sum(md.count(p) for p in FALSE_PATS)
false_wb = sum(zparts_text.count(p) for p in FALSE_PATS)
check(false_md == 0, f"false F1 sentence still in the md ({false_md})")
check(false_wb == 0, f"false F1 sentence still in the workbook ({false_wb})")
check(FIX_SENT in md and FIX_SENT in cn_text, "F1 replacement sentence missing")
check(md.count("2026-10-07") >= 1 and "2026-10-07" in cn_text, "the workfile's real 2026-10-07 date was lost")
res["false_sentence"] = {"md": false_md, "workbook": false_wb}
for r in (33, 34, 35):
    t = f11["PO"].cell(r, 35).value
    check(isinstance(t, str) and "LESS HC-PO r20" in t and "moved to CO" in t and "652,820 -> 590,318" in t,
          f"PO!AI{r} not updated")
for frag, where in [
    ("## Changes from v10 (v11)", "md v11 section"),
    ("unedited roster roll-up", "HC-COO reader note (md)"),
    ("rolls up to Production Operations", "banner pointer (md)"),
    ("booked in Central Operations (CO 6610-6640) per the user decision of 2026-10-10", "banner pointer booking (md)"),
    ("six P&L sheets (COO P&L, FO, PO, CO, FE, PE)", "B:N scope (md)"),
    ("note (b)", "precision note pointer (md)"),
    ("well under $1k", "precision note (md)"),
    ("## Decisions (v11, builder)", "md v11 decisions"),
]:
    check(frag in md, f"md lacks {where}: {frag!r}")
for frag, where in [
    ("Changes from v10 (v11)", "CN v11 section"),
    ("unedited roster roll-up", "HC-COO reader note (CN)"),
    ("rolls up to Production Operations", "banner pointer (CN)"),
    ("six P&L sheets (COO P&L, FO, PO, CO, FE, PE)", "B:N scope (CN)"),
    ("well under $1k", "precision note (CN)"),
]:
    check(frag in cn_text, f"Collation Notes lack {where}: {frag!r}")
check("748,768" in md and "1,147,260" in md, "HC-COO reader note totals missing (md)")

# 8. privacy / per-person
priv = open(PRIV).read(); pay = open(PAY).read()
check(re.search(r"hits 0\b", priv) is not None, "privacy_v6 found names")
check(re.search(r"exact hits 0;", pay) is not None, "paylist found exact per-person amounts")

res["criteria"] = collections.OrderedDict([
    ("All six items addressed", "fix presence asserted in the md, the Collation Notes and PO!AI33:AI35"),
    ("0 value changes outside Collation Notes", f"diff: PO AI33:AI35 only (3 text cells); other sheets 0/0; "
     f"parts changed {changed}; parts added/removed 0"),
    ("AG132 unchanged", f"{ag_v11:,.2f} (cached {ag_v11!r}, = v10)"),
    ("False sentence gone from md and workbook", f"occurrences md {false_md}, workbook {false_wb}; replacement present"),
    ("0 new errors", f"error cells {len(errors)}; stored vs recalculated max {mx:.1e} over {ncells:,} cells"),
    ("Collation Notes checks live", f"H78:H81 formulas; recalculated max |check| {hmax:.1e}"),
    ("No names / exact per-person amounts", "privacy_v6 hits 0; paylist exact hits 0"),
])
res["fails"] = fails
json.dump(res, open(OUT, "w"), indent=1, default=str)
print(f"analyze_v11: diff confined {not outside} (PO {sorted(po_cells)}), parts {changed}, AG132 {ag_v11:,.2f}, "
      f"errors {len(errors)}, recalc max {mx:.1e} over {ncells:,} cells, CN formulas {ncn} max {cnmax:.1e}, "
      f"H max {hmax:.1e}; fails {len(fails)}")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
