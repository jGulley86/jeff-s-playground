"""v13 standard suite. No clock, no file properties, no dates (F1 rule).

  1. Headline and department figures = figures_v13.json (which was computed from the recalculated stage-1 content
     and carries all internal tie assertions): COO P&L AG132/N132/AG16, CO 6610-6640 + 7700/8600, PE 6610-6640,
     PO 5110-5140 = 0 and 6610-6640, 'Depreciation Schedule' R195 unchanged, HC Z totals = the user's file.
  2. COO P&L = sum of departments on every SUM(FO,PO,CO,FE,PE) cell (<= 1e-6).
  3. Zero error caches on every sheet, in the deliverable and in its recalculation; zero '#REF!' in any formula text.
  4. Recalculation self-consistency: a LibreOffice full recalc of v13 reproduces its cache (numeric <= 1e-6).
  5. Deliverable = stage-1 content: every cached value outside the Collation Notes sheet equals S1RC (<= 1e-6), so
     the figures and scenarios computed on S1RC hold for the deliverable.
  6. Collation Notes: C21:F28 live formulas unchanged from v12; H78:H80 are the v13 de-dup checks; H81 = SUM; all
     four cache AND recalc to 0 (|x| <= 0.01). CONFIDENTIAL banner present (A3).
  7. Package: no shared formulas; no #REF! anywhere in stored XML formulas.
  8. Structure: HC-PO r20 blanked (B/C/D empty, M20 computes empty/0); PO!U33 uses SUM('HC-PO'!M14:M33); PE!U67 and
     PO!U67 are live roster links; CO!U67 subtracts rows 34/36/38/39.

Usage:
  python3 -I suite_v13.py V13_XLSX V13_RECALC_XLSX S1RC_XLSX V12_XLSX FIGURES_JSON OUT_JSON
Exit 1 on any failure.
"""
import sys, json, re, zipfile
import openpyxl

V13, V13RC, S1RC, V12, FIGJ, OUT = sys.argv[1:7]
TOL = 1e-6
ERR = {"#REF!", "#NAME?", "#DIV/0!", "#VALUE!", "#N/A", "#NUM!", "#NULL!"}
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
F = json.load(open(FIGJ))
fails, rep = [], {}


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


v = openpyxl.load_workbook(V13, data_only=True)
f = openpyxl.load_workbook(V13)
vr = openpyxl.load_workbook(V13RC, data_only=True)
s1 = openpyxl.load_workbook(S1RC, data_only=True)
n = lambda x: float(x) if isnum(x) else 0.0

# 1. figures
EXP = [("COO P&L", "AG132", F["AG132_v13"]), ("COO P&L", "N132", -899222.05), ("COO P&L", "AG16", 15563645.54),
       ("CO", "AG67", F["co66_v13_rows"][0]), ("CO", "AG68", F["co66_v13_rows"][1]), ("CO", "AG69", F["co66_v13_rows"][2]),
       ("CO", "AG98", 24000), ("CO", "AG106", 78000),
       ("PE", "AG67", F["pe66_v13_rows"][0]), ("PE", "AG68", F["pe66_v13_rows"][1]), ("PE", "AG69", F["pe66_v13_rows"][2]),
       ("PO", "AG67", F["po66_v13_rows"][0]), ("PO", "AG68", F["po66_v13_rows"][1]), ("PO", "AG69", F["po66_v13_rows"][2]),
       ("PO", "AG33", 0), ("PO", "AG34", 0), ("PO", "AG35", 0),
       ("Depreciation Schedule", "R195", 104416.68),
       ("HC-CO", "Z67", F["user_z"]["CO"]), ("HC-FE", "Z67", F["user_z"]["FE"]), ("HC-PE", "Z67", F["user_z"]["PE"]),
       ("HC-PO", "Z67", F["user_z"]["PO"])]
for sh, ad, exp in EXP:
    got = n(v[sh][ad].value)
    check(abs(got - exp) <= 0.01, f"{sh}!{ad} = {got:,.2f} (expected {exp:,.2f})")
rep["AG132"] = n(v["COO P&L"]["AG132"].value)

# 2. roll-up
pat = re.compile(r"^=SUM\(FO!([A-Z]+\d+),PO!\1,CO!\1,FE!\1,PE!\1\)$")
cnt, mx = 0, 0.0
for row in f["COO P&L"].iter_rows():
    for c in row:
        if isinstance(c.value, str):
            m = pat.match(c.value.replace(" ", ""))
            if m:
                ad = m.group(1)
                s = sum(n(v[d][ad].value) for d in ("FO", "PO", "CO", "FE", "PE"))
                mx = max(mx, abs(n(v["COO P&L"][c.coordinate].value) - s)); cnt += 1
check(cnt > 2000 and mx <= TOL, f"COO P&L = FO+PO+CO+FE+PE on {cnt} cells (max dev {mx:.2e})")
rep["rollup"] = {"cells": cnt, "max_dev": mx}

# 3. error caches + #REF! in formulas
err = sum(1 for ws in v.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value in ERR)
err_rc = sum(1 for ws in vr.worksheets for row in vr[ws.title].iter_rows() for c in row if isinstance(c.value, str) and c.value in ERR)
fref = sum(1 for ws in f.worksheets for row in ws.iter_rows() for c in row
           if isinstance(c.value, str) and c.value.startswith("=") and "#REF!" in c.value)
check(err == 0 and err_rc == 0 and fref == 0, f"0 error caches (v13 {err}, recalc {err_rc}); 0 #REF! in formulas ({fref})")

# 4. recalc self-consistency + 5. deliverable = stage-1 content
def cmp_books(a, b, skip_cn):
    mxd, cells, bad = 0.0, 0, 0
    for ws in a.worksheets:
        if skip_cn and ws.title == "Collation Notes":
            continue
        wb2 = b[ws.title]
        for row in ws.iter_rows():
            for c in row:
                x, y = c.value, wb2.cell(c.row, c.column).value
                if isnum(x) and isnum(y):
                    mxd = max(mxd, abs(x - y)); cells += 1
                elif (x if x != "" else None) != (y if y != "" else None):
                    bad += 1
    return mxd, cells, bad

mxd, cells, bad = cmp_books(v, vr, False)
check(mxd <= TOL and bad == 0, f"recalc reproduces the cache: {cells} numeric cells, max {mxd:.2e}, non-numeric diffs {bad}")
mxd2, cells2, bad2 = cmp_books(s1, v, True)
check(mxd2 <= TOL and bad2 == 0, f"deliverable = stage-1 content outside Collation Notes ({cells2} cells, max {mxd2:.2e}, other {bad2})")

# 6. Collation Notes
v12f = openpyxl.load_workbook(V12)
old_live = {c.coordinate: c.value for row in v12f["Collation Notes"].iter_rows(min_row=21, max_row=28)
            for c in row if isinstance(c.value, str) and c.value.startswith("=")}
new_live = {c.coordinate: c.value for row in f["Collation Notes"].iter_rows(min_row=21, max_row=28)
            for c in row if isinstance(c.value, str) and c.value.startswith("=")}
check(old_live == new_live and len(new_live) == 32, "Collation Notes C21:F28 live formulas unchanged (32)")
h = [f["Collation Notes"][f"H{r}"].value for r in (78, 79, 80, 81)]
ok_h = all(isinstance(x, str) and x.startswith("=") for x in h) and all(
    all(t in h[i] for t in ("S36", "S38", "S39")) for i in range(3)) and h[3] == "=SUM(H78:H80)"
hv = [abs(n(v["Collation Notes"][f"H{r}"].value)) for r in (78, 79, 80, 81)]
hvr = [abs(n(vr["Collation Notes"][f"H{r}"].value)) for r in (78, 79, 80, 81)]
check(ok_h and max(hv) <= 0.01 and max(hvr) <= 0.01,
      f"H78:H81 de-dup checks live and 0 (cache max {max(hv):.2e}, recalc max {max(hvr):.2e})")
check(isinstance(f["Collation Notes"]["A3"].value, str) and "CONFIDENTIAL" in f["Collation Notes"]["A3"].value,
      "CONFIDENTIAL banner present")

# 7. package
z = zipfile.ZipFile(V13)
shared = sum(z.read(nm).decode("utf-8", "ignore").count('t="shared"') for nm in z.namelist() if nm.startswith("xl/worksheets/"))
check(shared == 0, "0 shared formulas in the package")

# 8. structure
hcpo = f["HC-PO"]
check(all(hcpo[f"{c}20"].value in (None, "") for c in "BCD"), "HC-PO r20 blanked (B/C/D empty)")
m20 = v["HC-PO"]["M20"].value
check(m20 in (None, "", 0) or (isnum(m20) and abs(m20) < TOL), "HC-PO M20 computes empty/0")
check("SUM('HC-PO'!M14:M33)" in str(f["PO"]["U33"].value), "PO!U33 live 8-staff basis")
check(str(f["PE"]["U67"].value) == "='HC-PE'!M67", "PE!U67 live roster link")
check(str(f["PO"]["U67"].value) == "='HC-PO'!M41", "PO!U67 live PM link")
co_u67 = str(f["CO"]["U67"].value)
check(all(t in co_u67 for t in ("F34", "F36", "F38", "F39", "F46")), "CO!U67 subtracts rows 34/36/38/39 + hire cost")

rep["fails"] = fails
json.dump(rep, open(OUT, "w"), indent=1)
print(f"suite_v13: {'ALL GREEN' if not fails else str(len(fails)) + ' FAILURES'}")
sys.exit(1 if fails else 0)
