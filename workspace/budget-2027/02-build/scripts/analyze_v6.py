"""v6 checks. Exit 1 if any completion criterion fails.

Usage:
  python3 -I analyze_v6.py V5_XLSX V6_XLSX V6_RECALC_XLSX DIFF_JSON BUILD_INFO_JSON RECON_JSON RECON_ON_V6_JSON OUT_JSON

  - diff_versions.py result: 0 formula and 0 value differences on every existing sheet (Collation Notes excluded);
  - package: every v5 part byte-identical except workbook.xml, its rels, [Content_Types].xml, styles.xml (append only)
    and Collation Notes; no external-link part;
  - HC tabs: present, named and ordered as required after Fld Eng Budget; 0 errors after a LibreOffice recalculation;
    cached values = recalculated values; formulas reference only the HC tabs; no external references;
  - HC-PO / HC-CO / HC-PE rows 67-69 tie to the PO / CO / PE payroll rows (2027);
  - no new errors on the existing sheets; cached values = LibreOffice recalculation (as v5 checked);
  - Collation Notes formulas = recalculation;
  - recon_v6.py run on the v6 workbook gives the same output as on v5 (figures recompute from the final file).
"""
import sys, json, re, zipfile, datetime
import openpyxl

V5, V6, LO6, DIFF, BINFO, REC5, REC6, OUT = sys.argv[1:9]
PRIV = sys.argv[9] if len(sys.argv) > 9 else None          # privacy_v6.py output on the pass-1 notes
HC = ["HC-FO", "HC-PO", "HC-CO", "HC-FE", "HC-PE", "HC-COO"]
fails = []
res = {}


def check(cond, msg):
    if not cond:
        fails.append(msg)


# diff
d = json.load(open(DIFF))
res["diff"] = {"total": d["total"], "sheets": {k: {kk: v[kk] for kk in ("cells", "formula_diffs", "value_diffs")} for k, v in d["sheets"].items()},
               "comments": [len(d["comments_added"]), len(d["comments_removed"]), len(d["comments_changed"])],
               "only_new": d["sheets_only_in_new"], "only_old": d["sheets_only_in_old"]}
check(d["total"]["formula_diffs"] == 0 and d["total"]["value_diffs"] == 0, "existing sheets differ from v5")
check(sorted(d["sheets_only_in_new"]) == sorted(HC) and not d["sheets_only_in_old"], "sheet set")
check(res["diff"]["comments"] == [0, 0, 0], "comments changed")

# package
z5, z6 = zipfile.ZipFile(V5), zipfile.ZipFile(V6)
n5, n6 = z5.namelist(), z6.namelist()
same = [n for n in n5 if n in n6 and z5.read(n) == z6.read(n)]
changed = [n for n in n5 if n in n6 and z5.read(n) != z6.read(n)]
added = [n for n in n6 if n not in n5]
allowed = {"xl/workbook.xml", "xl/_rels/workbook.xml.rels", "[Content_Types].xml", "xl/styles.xml", "xl/worksheets/sheet1.xml"}
check(set(changed) <= allowed and not [n for n in n5 if n not in n6], f"unexpected part changes {changed}")
s5, s6 = z5.read("xl/styles.xml").decode(), z6.read("xl/styles.xml").decode()


def items(xml, tag, child):
    blk = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", xml, re.S)
    return re.findall(rf"<{child}(?:\s[^>]*)?/>|<{child}(?:\s[^>]*)?>.*?</{child}>", blk.group(1), re.S) if blk else []


app_only = all(items(s6, t, c)[:len(items(s5, t, c))] == items(s5, t, c) for t, c in
               (("numFmts", "numFmt"), ("fonts", "font"), ("fills", "fill"), ("borders", "border"), ("cellXfs", "xf"), ("cellStyleXfs", "xf"), ("dxfs", "dxf")))
check(app_only, "styles.xml not append-only")
wb5, wb6 = z5.read("xl/workbook.xml").decode(), z6.read("xl/workbook.xml").decode()
check(wb6[:wb6.index("</sheets>")].startswith(wb5[:wb5.index("</sheets>")]) and wb6[wb6.index("</sheets>"):] == wb5[wb5.index("</sheets>"):],
      "workbook.xml changed outside the appended sheets")
ext = [n for n in n6 if n.startswith("xl/externalLinks/")]
check(not ext, "external link parts present")
res["package"] = {"v5_parts": len(n5), "v6_parts": len(n6), "identical": len(same), "changed": changed, "added": added,
                  "styles_append_only": app_only, "external_links": len(ext),
                  "defined_names": wb6.count("<definedName "), "defined_names_v5": wb5.count("<definedName ")}
check(res["package"]["defined_names"] == res["package"]["defined_names_v5"], "defined names changed")
sheets = [(m.group(1).replace("&amp;", "&"), m.group(2)) for m in re.finditer(r'<sheet name="([^"]+)" sheetId="\d+" state="(\w+)"', wb6)]
res["sheets"] = sheets

# HC tabs
f6 = openpyxl.load_workbook(V6); v6 = openpyxl.load_workbook(V6, data_only=True); lo = openpyxl.load_workbook(LO6, data_only=True)
names = f6.sheetnames
order_ok = names[names.index("Fld Eng Budget") + 1:] == HC
check(order_ok, "HC tab order")
errs = maxd = cells = txt = foreign = extref = 0
for s in HC:
    for row in f6[s].iter_rows():
        for c in row:
            fv = c.value
            if isinstance(fv, str) and fv.startswith("="):
                for ref in re.findall(r"'([^']+)'!", fv):
                    foreign += ref not in HC
                extref += bool(re.search(r"\[\d+\]", fv))
            a, b = v6[s][c.coordinate].value, lo[s][c.coordinate].value
            if isinstance(b, str) and b.startswith("#"):
                errs += 1
            if a is None and b is None:
                continue
            cells += 1
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                maxd = max(maxd, abs(a - b))
            elif isinstance(a, datetime.datetime) or isinstance(b, datetime.datetime):
                txt += a != b
            elif not ((a in (None, "")) and (b in (None, ""))) and a != b:
                txt += 1
res["hc_tabs"] = {"names": HC, "order_ok": order_ok, "errors": errs, "max_diff": maxd, "cells": cells, "text_mismatch": txt,
                  "foreign_refs": foreign, "external_refs": extref}
check(errs == 0 and maxd < 1e-6 and txt == 0 and foreign == 0 and extref == 0, "HC tab check failed")
# tie
tie = 0.0
for hcs, pl, rows in (("HC-PO", "PO", (33, 34, 35)), ("HC-CO", "CO", (67, 68, 69)), ("HC-PE", "PE", (67, 68, 69))):
    for hr, pr in zip((67, 68, 69), rows):
        for i in range(12):
            tie = max(tie, abs(float(v6[hcs].cell(hr, 13 + i).value or 0) - float(v6[pl].cell(pr, 21 + i).value or 0)))
res["hc_tie"] = tie
check(tie < 0.02, f"HC tabs do not tie to P&L ({tie})")

# errors and recalculation on the existing sheets
v5w = openpyxl.load_workbook(V5, data_only=True)
by = {}; new = 0; nd = 0; md_ = 0.0; tm = 0
for s in names:
    if s == "Collation Notes":
        continue
    e5 = {}; e6 = {}
    for row in v6[s].iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("#") and c.value.endswith(("!", "?", "A", "0")):
                e6[c.value] = e6.get(c.value, 0) + 1
                if s in v5w.sheetnames and v5w[s][c.coordinate].value != c.value:
                    new += 1
            if s in HC:
                continue
            a, b = c.value, lo[s][c.coordinate].value
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                if a != b:
                    nd += 1; md_ = max(md_, abs(a - b))
            elif a != b and not (a in (None, "") and b in (None, "")):
                if not (isinstance(a, datetime.datetime) or isinstance(b, datetime.datetime)):
                    tm += 1
    if s in v5w.sheetnames:
        for row in v5w[s].iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("#") and c.value.endswith(("!", "?", "A", "0")):
                    e5[c.value] = e5.get(c.value, 0) + 1
    by[s] = [str(e5) if e5 else ("none" if s in v5w.sheetnames else "n/a (new)"), str(e6) if e6 else "none"]
    if s in HC:
        new += sum(e6.values())
res["errors"] = {"by_sheet": by, "new": new}
check(new == 0, "new errors")
res["recalc"] = {"n_diff": nd, "max_diff": md_, "text_mismatch": tm}
check(md_ < 1e-6 and tm == 0, "recalculation differs on existing sheets")
# Collation Notes formulas
cnf = 0; cnd = 0.0; cnt = 0
for row in f6["Collation Notes"].iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("="):
            cnf += 1
            a, b = v6["Collation Notes"][c.coordinate].value, lo["Collation Notes"][c.coordinate].value
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                cnd = max(cnd, abs(a - b))
            elif a != b:
                cnt += 1
res["cn"] = {"formulas": cnf, "max_diff": cnd, "text_mismatch": cnt}
check(cnd < 1e-6 and cnt == 0, "Collation Notes formulas differ from recalculation")
# recon reproducibility
res["recon_same"] = json.load(open(REC5)) == json.load(open(REC6))
check(res["recon_same"], "recon on v6 differs from recon on v5")
if PRIV:
    line = [l for l in open(PRIV).read().splitlines() if l.startswith("privacy_v6:")][-1]
    res["privacy"] = line.replace("privacy_v6: ", "")
    check(line.endswith("hits 0"), "privacy check failed")
else:
    res["privacy"] = "not run"
res["fails"] = fails
json.dump(res, open(OUT, "w"), indent=1, default=str)
print(f"analyze_v6: diff {d['total']}; parts identical {len(same)}/{len(n5)}, changed {changed}; HC errors {errs}, max diff {maxd:.1e}; "
      f"tie {tie:.2e}; new errors {new}; recalc diffs {nd} (max {md_:.1e}); CN formulas {cnf} (max {cnd:.1e}); recon same {res['recon_same']}; "
      f"FAILS {fails}")
sys.exit(1 if fails else 0)
