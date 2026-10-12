"""v12 standard suite on the re-serialized workbook. No clock, no file properties, no dates (F1 rule).

  1. Evidence figures (handoff, cached values): COO P&L AG132 = 159,136.40; N132 = -899,222.05;
     AG16 (revenue) = 15,563,645.54; CO AG67/AG68/AG69 = 963,670.09 / 55,098.30 / 128,491.55;
     PO AG33:AG35 (5110/5130/5140) = 0; 'Depreciation Schedule' R195 (2027 labour depreciation) = 104,416.68.
  2. COO P&L = sum of departments: every COO P&L cell whose formula is SUM(FO!x,PO!x,CO!x,FE!x,PE!x)
     must cache the sum of the five departments' cached values (<= 1e-6).
  3. Zero error cells: no cell on any sheet caches an error token (#REF! etc.); error tokens inside
     prose (Collation Notes sentences) are not errors and are not flagged (whole-cell match only).
  4. Recalculation self-consistency: a LibreOffice full recalc of the v12 file must reproduce the
     v12 cache - every value equal (numeric <= 1e-6; max drift reported).
  5. Collation Notes live formulas: the cell->formula map on v12 equals v11's (36 formulas, incl. the
     H78:H81 'Check (must be 0)' block), and H78:H81 cache 0 before and after recalc.
  6. CONFIDENTIAL banner present on the Collation Notes sheet.
  7. No t="shared" formulas left in any v12 worksheet part (every formula stored explicitly).

Usage:
  python3 -I suite_v12.py V12_XLSX V12_RECALC_XLSX V11_XLSX OUT_JSON
Exit 1 on any failure.
"""
import sys, json, re, zipfile
import openpyxl

V12, V12RC, V11, OUT = sys.argv[1:5]
TOL = 1e-6
ERR = {"#REF!", "#NAME?", "#DIV/0!", "#VALUE!", "#N/A", "#NUM!", "#NULL!"}
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
fails = []
rep = {}


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


v = openpyxl.load_workbook(V12, data_only=True)
f = openpyxl.load_workbook(V12)
vr = openpyxl.load_workbook(V12RC, data_only=True)
v11f = openpyxl.load_workbook(V11)
v11v = openpyxl.load_workbook(V11, data_only=True)

# 1. evidence figures
EXP = [
    ("COO P&L", "AG132", 159136.40, "2027 COO contribution"),
    ("COO P&L", "N132", -899222.05, "2026 contribution"),
    ("COO P&L", "AG16", 15563645.54, "2027 revenue"),
    ("CO", "AG67", 963670.09, "CO 6610"),
    ("CO", "AG68", 55098.30, "CO 6630"),
    ("CO", "AG69", 128491.55, "CO 6640"),
    ("PO", "AG33", 0.0, "PO 5110"),
    ("PO", "AG34", 0.0, "PO 5130"),
    ("PO", "AG35", 0.0, "PO 5140"),
    ("Depreciation Schedule", "R195", 104416.68, "2027 labour depreciation"),
]
rep["figures"] = {}
for sheet, cell, exp, label in EXP:
    got = v[sheet][cell].value
    rep["figures"][f"{sheet}!{cell}"] = got
    # the handoff states display-rounded (2dp) figures; a cached x.xx5 is the same figure
    check(isnum(got) and abs(got - exp) <= 0.0051, f"{label} {sheet}!{cell} = {got!r} (expected {exp})")

# 2. COO P&L = sum of departments
pl = f["COO P&L"]; plv = v["COO P&L"]
pat = re.compile(r"^=SUM\(FO!([A-Z]+\d+),PO!\1,CO!\1,FE!\1,PE!\1\)$")
n_sum = 0; bad_sum = 0; max_dev = 0.0
for row in pl.iter_rows():
    for c in row:
        if isinstance(c.value, str):
            m = pat.match(c.value.replace(" ", ""))
            if m:
                n_sum += 1
                ref = m.group(1)
                total = sum(x for x in (v[d][ref].value for d in ("FO", "PO", "CO", "FE", "PE")) if isnum(x))
                got = plv[c.coordinate].value
                got = got if isnum(got) else 0.0
                dev = abs(got - total)
                max_dev = max(max_dev, dev)
                if dev > TOL: bad_sum += 1
rep["collation_sums"] = {"cells": n_sum, "bad": bad_sum, "max_dev": max_dev}
check(n_sum > 2000 and bad_sum == 0, f"COO P&L = sum of departments: {n_sum} SUM(FO,PO,CO,FE,PE) cells, "
                                     f"{bad_sum} deviating, max dev {max_dev:.3e}")

# 3. zero error cells (v12 and its recalc)
def errcells(book):
    out = []
    for s in book.sheetnames:
        for row in book[s].iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.strip() in ERR:
                    out.append(f"{s}!{c.coordinate}")
    return out

e1, e2 = errcells(v), errcells(vr)
rep["error_cells"] = {"v12": e1[:20], "v12_recalc": e2[:20]}
check(not e1, f"0 error cells in v12 (found {len(e1)}: {e1[:5]})")
check(not e2, f"0 error cells in v12 recalc (found {len(e2)}: {e2[:5]})")

# 4. recalc self-consistency
maxd = 0.0; where = None; nbad = 0; ncmp = 0
for s in v.sheetnames:
    ws, wr = v[s], vr[s]
    cells_r = {c.coordinate: c.value for row in wr.iter_rows() for c in row}
    for row in ws.iter_rows():
        for c in row:
            a = c.value; b = cells_r.get(c.coordinate)
            if a is None and b is None: continue
            ncmp += 1
            if isnum(a) and isnum(b):
                d = abs(a - b)
                if d > maxd: maxd, where = d, f"{s}!{c.coordinate}"
                if d > TOL: nbad += 1
            elif (a if a is not None else "") != (b if b is not None else ""):
                nbad += 1
                if where is None: where = f"{s}!{c.coordinate}"
rep["recalc"] = {"cells": ncmp, "bad": nbad, "max_drift": maxd, "at": where}
check(nbad == 0, f"recalc reproduces the v12 cache: {ncmp} cells, {nbad} off, max drift {maxd:.3e} at {where}")

# 5. Collation Notes live formulas
def cn_formulas(book):
    return {c.coordinate: c.value for row in book["Collation Notes"].iter_rows()
            for c in row if isinstance(c.value, str) and c.value.startswith("=")}

f12, f11 = cn_formulas(f), cn_formulas(v11f)
rep["cn_formulas"] = {"v12": len(f12), "v11": len(f11)}
check(f12 == f11, f"Collation Notes formulas identical to v11 ({len(f12)} vs {len(f11)} incl. H78:H81)")
h = [v["Collation Notes"][f"H{r}"].value for r in range(78, 82)]
hr = [vr["Collation Notes"][f"H{r}"].value for r in range(78, 82)]
rep["cn_checks_H78_H81"] = {"v12": h, "recalc": hr}
check(all(isnum(x) and abs(x) < 0.005 for x in h + hr),
      f"Collation Notes H78:H81 'must be 0' checks: cached {h}, recalculated {hr}")

# 6. CONFIDENTIAL banner
banner = any(isinstance(c.value, str) and "CONFIDENTIAL" in c.value
             for row in v["Collation Notes"].iter_rows(min_row=1, max_row=6) for c in row)
check(banner, "CONFIDENTIAL banner present on Collation Notes rows 1-6")

# 7. no shared formulas left
z = zipfile.ZipFile(V12)
shared = sum(z.read(n).decode().count('t="shared"') for n in z.namelist()
             if n.startswith("xl/worksheets/sheet"))
rep["shared_f_left"] = shared
check(shared == 0, f"no t=\"shared\" formulas left in v12 worksheets ({shared})")

# scenario values asserted by scenread_v12.py in the run script; stored here for the report
json.dump(rep, open(OUT, "w"), indent=1)
print(f"suite_v12: {'PASS' if not fails else 'FAIL'} ({len(fails)} failures)")
sys.exit(1 if fails else 0)
