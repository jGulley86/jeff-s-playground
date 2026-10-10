"""v9 checks. Exit 1 if any completion criterion fails.

Usage:
  python3 -I analyze_v9.py V8_XLSX V9_XLSX V9_RECALC_XLSX DIFF_JSON PATCH_JSON SPEC_JSON FIG9_JSON NOTES_MD NOTES_JSON PRIVACY_TXT PAYLIST_TXT OUT_JSON

  - diff v8 -> v9 confined to the allowed areas (handoff v9): Depreciation Schedule labour block (rows 128+): the switch cells and
    labels, the labour-block formulas edited for the Sep-26 consistency and the idle switch, new section 11, and every formula
    there whose value moves (static trace); PO rows 33-35 (2027 months: + idle labour, 0 while B135 = 1) and their AI notes;
    the downstream PO 5011 / 5012 values, subtotals and the COO P&L roll-up (values only, in the static trace written by
    patches_v9.py); no other sheet; no 2026 column (B:N) of COO P&L / FO / PO / CO / FE / PE;
  - package: only the Depreciation Schedule, PO, COO P&L and Collation Notes parts change;
  - LibreOffice recalculation of v9 = stored values on every sheet except Collation Notes; 0 new errors;
  - COO P&L = FO + PO + CO + FE + PE on every GL row (2027 months and AG); check row 133 = 0;
  - Collation Notes: live formulas = recalculation; the first section is the CONFIDENTIAL banner;
  - the false run-rate / inventory wording is gone from the md, the Collation Notes and the workbook labels;
  - figures: replicas, hand recompute inside tolerance; privacy_v6.py and paylist_v9.py found nothing.
"""
import sys, json, re, zipfile, datetime, collections
import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.worksheet.formula import ArrayFormula

V7, V8, LO8, DIFF, PATCH, SPEC, FIG8, MD, NJ, PRIV, PAY, OUT = sys.argv[1:13]
BANNER = "CONFIDENTIAL – contains named compensation data (HC-* tabs); restrict distribution"
fails = []; res = {}


def check(cond, msg):
    if not cond:
        fails.append(msg)


spec = json.load(open(SPEC)); patch = json.load(open(PATCH)); F = json.load(open(FIG8))
patched = {(s, c) for s, c, _, _ in patch["values"]}
edited = {("Depreciation Schedule", x["cell"]) for x in spec["ds_new"] + spec["ds_edit"]} | {("PO", x["cell"]) for x in spec["po"]}
d = json.load(open(DIFF))
res["diff"] = {"total": d["total"], "sheets": {k: {kk: v[kk] for kk in ("cells", "formula_diffs", "value_diffs")} for k, v in d["sheets"].items()},
               "comments": [len(d["comments_added"]), len(d["comments_removed"]), len(d["comments_changed"])],
               "only_new": d["sheets_only_in_new"], "only_old": d["sheets_only_in_old"]}
check(not d["sheets_only_in_new"] and not d["sheets_only_in_old"], "sheet set changed")
check(res["diff"]["comments"] == [0, 0, 0], "comments changed")

f7 = openpyxl.load_workbook(V7); v7 = openpyxl.load_workbook(V7, data_only=True)
f8 = openpyxl.load_workbook(V8); v8 = openpyxl.load_workbook(V8, data_only=True)
lo = openpyxl.load_workbook(LO8, data_only=True)


def norm(v):
    if isinstance(v, ArrayFormula):
        return ("array", v.ref, v.text)
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()
    return v


PL = ("COO P&L", "FO", "PO", "CO", "FE", "PE")
areas = collections.OrderedDict(); outside = []; cols26 = 0; sheets_changed = set()


def area(s, r, c):
    col = get_column_letter(c)
    key = (s, f"{col}{r}")
    if s == "Depreciation Schedule":
        if key in edited and r in (131, 132, 133, 135):
            return "switch rows 131-135 (B132 1 -> 0; new idle switch row 135; labels)"
        if key in edited and r >= 218:
            return "new section 11 (rows 218+): idle labour, Sep-26 builds, memo"
        if key in edited:
            return "labour block rows 128-216: edited formulas (rows 153, 155, 193-194, R196, B206, B213) and labels"
        return "labour block rows 128-216: values of unchanged formulas (static trace of the edits)"
    if s == "PO":
        if r in (20, 21) and 21 <= c <= 32: return "U20:AF21 (5011 / 5012, 2027 months): values"
        if r in (33, 34, 35) and 21 <= c <= 32: return "U33:AF35 (5110-5140, 2027 months): + idle labour (0 while B135 = 1)"
        if col == "AI" and r in (33, 34, 35): return "AI33:AI35 (notes)"
        return "subtotals and ratios of those rows (AG / AH / AJ; rows 37, 63, 64, 117, 132, 137-142)"
    if s == "COO P&L":
        return "roll-up of the PO rows and subtotals (U:AF, AG, AH, AJ)"
    return "other"


for s in f8.sheetnames:
    if s == "Collation Notes":
        continue
    a_f, b_f, a_v, b_v = f7[s], f8[s], v7[s], v8[s]
    mr = max(a_f.max_row, b_f.max_row); mc = max(a_f.max_column, b_f.max_column)
    for row in b_f.iter_rows(min_row=1, max_row=mr, max_col=mc):
        for cell in row:
            r, c = cell.row, cell.column
            fa, fb = norm(a_f.cell(r, c).value), norm(cell.value)
            va, vb = norm(a_v.cell(r, c).value), norm(b_v.cell(r, c).value)
            fd, vd = fa != fb, va != vb
            if not (fd or vd):
                continue
            key = (s, cell.coordinate); sheets_changed.add(s)
            if s in PL and c <= 14:
                cols26 += 1
            ok = False
            if s == "Depreciation Schedule":
                ok = r >= 128 and ((key in edited) if fd else (key in edited or key in patched))
            elif s == "PO":
                ok = (key in edited) if fd else (key in edited or key in patched)
            elif s == "COO P&L":
                ok = (not fd) and key in patched
            if not ok:
                outside.append([s, cell.coordinate, str(fa)[:60], str(fb)[:60]])
            k = (s, area(s, r, c))
            a_ = areas.setdefault(k, [0, 0]); a_[0] += fd; a_[1] += vd
ALLOW = {"Depreciation Schedule": "switch cells and labels; labour-block formulas for the Sep-26 consistency and the idle switch (rows 128+)",
         "PO": "downstream PO 5011/5012 values and subtotals; PO 5110-5140 + idle labour (builder decision D11, values unchanged)",
         "COO P&L": "the COO P&L roll-up"}
res["allowed"] = {"areas": [[s, a_, v[0], v[1], ALLOW.get(s, "NOT ALLOWED")] for (s, a_), v in areas.items()], "outside": len(outside),
                  "outside_examples": outside[:10], "cols_2026": cols26, "sheets": sorted(sheets_changed)}
check(not outside, f"changes outside the allowed areas: {outside[:5]}")
check(cols26 == 0, "2026 columns changed")
check(sheets_changed <= {"Depreciation Schedule", "PO", "COO P&L"}, f"unexpected sheets changed {sheets_changed}")
tot_f = sum(v[0] for v in areas.values()); tot_v = sum(v[1] for v in areas.values())
check(tot_f == d["total"]["formula_diffs"] and tot_v == d["total"]["value_diffs"], ("classification does not cover the diff", tot_f, tot_v, d["total"]))

z7, z8 = zipfile.ZipFile(V7), zipfile.ZipFile(V8)
n7, n8 = z7.namelist(), z8.namelist()
wbx = z8.read("xl/workbook.xml").decode(); rels = z8.read("xl/_rels/workbook.xml.rels").decode()


def part(name):
    rid = re.search(rf'<sheet name="{re.escape(name)}"[^>]*r:id="(rId\d+)"', wbx).group(1)
    return "xl/" + re.search(rf'<Relationship Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)


exp_changed = sorted(part(n) for n in ("Collation Notes", "COO P&amp;L", "PO", "Depreciation Schedule"))
same = [n for n in n7 if n in n8 and z7.read(n) == z8.read(n)]
changed = [n for n in n7 if n in n8 and z7.read(n) != z8.read(n)]
added = [n for n in n8 if n not in n7]; removed = [n for n in n7 if n not in n8]
check(sorted(changed) == exp_changed and not added and not removed and n7 == n8, f"unexpected part changes {changed} {added} {removed}")
ext = [n for n in n8 if n.startswith("xl/externalLinks/")]
check(not ext, "external link parts present")
wb7x = z7.read("xl/workbook.xml").decode()
res["package"] = {"v7_parts": len(n7), "v8_parts": len(n8), "identical": len(same), "changed": changed, "added": added, "removed": removed,
                  "external_links": len(ext), "defined_names": wbx.count("<definedName "), "defined_names_v7": wb7x.count("<definedName ")}
check(wbx == wb7x, "workbook.xml changed")
res["sheets"] = [(m.group(1).replace("&amp;", "&"), m.group(2)) for m in re.finditer(r'<sheet name="([^"]+)" sheetId="\d+" state="(\w+)"', wbx)]


def is_err(v):
    return isinstance(v, str) and v.startswith("#") and v.endswith(("!", "?", "A", "0"))


HC = [s for s in f8.sheetnames if s.startswith("HC-")]
by = {}; new = 0; nd = 0; md_ = 0.0; tm = 0
hc = {"errors": 0, "max_diff": 0.0, "cells": 0}
for s in f8.sheetnames:
    if s == "Collation Notes":
        continue
    e7 = collections.Counter(); e8 = collections.Counter()
    for row in v8[s].iter_rows():
        for c in row:
            if is_err(c.value):
                e8[c.value] += 1
                if v7[s][c.coordinate].value != c.value:
                    new += 1
            a, b = c.value, lo[s][c.coordinate].value
            if s in HC:
                if is_err(b): hc["errors"] += 1
                if a is not None or b is not None: hc["cells"] += 1
                if isinstance(a, (int, float)) and isinstance(b, (int, float)): hc["max_diff"] = max(hc["max_diff"], abs(a - b))
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                if a != b:
                    nd += 1; md_ = max(md_, abs(a - b))
            elif a != b and not (a in (None, "") and b in (None, "")):
                if not (isinstance(a, datetime.datetime) or isinstance(b, datetime.datetime)):
                    tm += 1
    for row in v7[s].iter_rows():
        for c in row:
            if is_err(c.value):
                e7[c.value] += 1
    by[s] = [str(dict(e7)) if e7 else "none", str(dict(e8)) if e8 else "none"]
res["errors"] = {"by_sheet": by, "new": new, "pp": f"{by['Prod Payroll'][0]} -> {by['Prod Payroll'][1]}"}
res["hc_tabs"] = hc
check(new == 0 and hc["errors"] == 0 and by["Prod Payroll"][1] == "none" and by["Depreciation Schedule"][1] == "none", "errors")
res["recalc"] = {"n_diff": nd, "max_diff": md_, "text_mismatch": tm}
check(md_ < 1e-6 and tm == 0, "recalculation differs from stored values")

# COO P&L = sum of the departments (GL rows: label 'NNNN - ...'), 2027 months U:AF and AG
cp = v8["COO P&L"]; mx = 0.0; ncell = 0
for r in range(9, 133):
    lab = cp.cell(r, 1).value
    if not (isinstance(lab, str) and re.match(r"\d{4} - ", lab)):
        continue
    for c in list(range(21, 33)) + [33]:
        s_ = sum(float(v8[dd].cell(r, c).value or 0) for dd in ("FO", "PO", "CO", "FE", "PE"))
        mx = max(mx, abs(float(cp.cell(r, c).value or 0) - s_)); ncell += 1
res["coo_sum"] = {"max_diff": mx, "cells": ncell, "row133": float(cp["AG133"].value or 0)}
check(mx < 1e-6 and abs(res["coo_sum"]["row133"]) < 1e-6, "COO P&L is not the sum of the departments")
for r in (132, 117, 63, 36, 20, 21):
    s_ = sum(float(v8[dd].cell(r, 33).value or 0) for dd in ("FO", "PO", "CO", "FE", "PE"))
    check(abs(float(cp.cell(r, 33).value or 0) - s_) < 1e-6, f"COO P&L AG{r} != sum of departments")

cnf = 0; cnd = 0.0; cnt = 0
for row in f8["Collation Notes"].iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("="):
            cnf += 1
            a, b = v8["Collation Notes"][c.coordinate].value, lo["Collation Notes"][c.coordinate].value
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                cnd = max(cnd, abs(a - b))
            elif a != b:
                cnt += 1
banner_first = v8["Collation Notes"]["A3"].value == BANNER
res["cn"] = {"formulas": cnf, "max_diff": cnd, "text_mismatch": cnt, "banner_first": banner_first}
check(cnd < 1e-6 and cnt == 0 and cnf == 32, "Collation Notes formulas")
check(banner_first, "Collation Notes banner is not the first section")
md = open(MD).read(); nj = open(NJ).read()
check(md.split("\n")[2].startswith("> **" + BANNER), "md banner is not at the top")
for t in (md, nj):
    check("no exact per-person" not in t.lower(), "the withdrawn privacy claim is back")
# figures
check(F["hand"]["diff"] < 1e-6, "hand recompute")
check(max(abs(v) for v in F["prodpay"]["totals_diff_replica_vs_v8"].values()) < 1, "XLOOKUP proof: model totals vs replica > $1")
check(F["labour_replica_max_diff"] < 1e-6, "labour block replica")
check(abs(F["effects"]["C9"] - float(cp["AG132"].value)) < 1e-6, "figures contribution != workbook")
# wording (critic v8 B1 / O3): no false run-rate reason, no 'inventory' for the CIP, in the md, the Collation Notes and the workbook labels
BAD = ("inside the PO run rate", "in the PO run rate", "CIP / inventory", "inventory at Dec-27", "carries no labour", "holds no labour")
lab_txt = " ".join(str(c.value) for row in f8["Depreciation Schedule"].iter_rows(min_row=128) for c in row if isinstance(c.value, str)) + " " + \
          " ".join(str(f8["PO"][f"AI{r}"].value) for r in (20, 21, 33, 34, 35))
cn_txt = " ".join(str(c.value) for row in v8["Collation Notes"].iter_rows() for c in row if isinstance(c.value, str))
hits = {k: sum(t.count(b) for b in BAD) for k, t in (("md", md), ("Collation Notes JSON", nj), ("Collation Notes sheet", cn_txt), ("workbook labels", lab_txt))}
check(not any(hits.values()), f"false wording left: {hits}")
res["wording"] = (f"{sum(hits.values())} hits of {len(BAD)} withdrawn phrases (the run-rate reason for leaving out the Sep-26 labour, the inventory label for "
                  f"the CIP, the 'no labour' claims) in " + ", ".join(hits) + "; remaining 'run rate' mentions are the existing-fleet depreciation run rate "
                  "(Decision #2, I-31) and the v8 item named as withdrawn.")
for lab, path, key in (("privacy", PRIV, "privacy_v6:"), ("paylist", PAY, "paylist_v9:")):
    line = [l for l in open(path).read().splitlines() if l.startswith(key)][-1]
    res[lab] = line.replace(key + " ", "")
    check(re.search(r"(hits|exact hits) 0\b", line) is not None, f"{lab} check failed")
res["fails"] = fails
json.dump(res, open(OUT, "w"), indent=1, default=str)
print(f"analyze_v9: diff {d['total']}; outside allowed {len(outside)}; 2026 cols {cols26}; parts identical {len(same)}/{len(n7)}, changed {changed}; "
      f"new errors {new}; PP errors {res['errors']['pp']}; recalc diffs {nd} (max {md_:.1e}); COO=sum max {mx:.1e}; CN formulas {cnf} (max {cnd:.1e}), "
      f"banner first {banner_first}; FAILS {fails}")
sys.exit(1 if fails else 0)
