"""v7 checks. Exit 1 if any completion criterion fails.

Usage:
  python3 -I analyze_v7.py V6_XLSX V7_XLSX V7_RECALC_XLSX DIFF_JSON RECON_V6_JSON RECON_V7_JSON FIG7_JSON NOTES_MD NOTES_JSON
                           PRIVACY_TXT PAYLIST_TXT OUT_JSON

  - diff_versions.py v6 -> v7: 0 formula and 0 value differences on every sheet except Collation Notes; same sheet set;
  - package: every v6 part byte-identical except the Collation Notes worksheet part; nothing added or removed;
  - LibreOffice recalculation of v7 = stored values on every sheet except Collation Notes; no new errors vs v6;
  - Collation Notes: live formulas = recalculation; the first section is the CONFIDENTIAL banner;
  - recon_v6.py on v7 gives the same output as on v6;
  - the v6 I-28 FO figure (and its 'after' value) is left only in explicit 'v6' references; the v6 'no overlap left' wording is gone;
  - privacy_v6.py (names) and paylist_v7.py (per-person amounts) found nothing (their outputs are passed in).
"""
import sys, json, re, zipfile, datetime
import openpyxl

V6, V7, LO7, DIFF, REC6, REC7, FIG7, MD, NJ, PRIV, PAY, OUT = sys.argv[1:13]
BANNER = "CONFIDENTIAL – contains named compensation data (HC-* tabs); restrict distribution"
fails = []; res = {}


def check(cond, msg):
    if not cond:
        fails.append(msg)


d = json.load(open(DIFF))
res["diff"] = {"total": d["total"], "sheets": {k: {kk: v[kk] for kk in ("cells", "formula_diffs", "value_diffs")} for k, v in d["sheets"].items()},
               "comments": [len(d["comments_added"]), len(d["comments_removed"]), len(d["comments_changed"])],
               "only_new": d["sheets_only_in_new"], "only_old": d["sheets_only_in_old"]}
check(d["total"]["formula_diffs"] == 0 and d["total"]["value_diffs"] == 0, "sheets differ from v6")
check(not d["sheets_only_in_new"] and not d["sheets_only_in_old"], "sheet set changed")
check(res["diff"]["comments"] == [0, 0, 0], "comments changed")

z6, z7 = zipfile.ZipFile(V6), zipfile.ZipFile(V7)
n6, n7 = z6.namelist(), z7.namelist()
wbx = z7.read("xl/workbook.xml").decode(); rels = z7.read("xl/_rels/workbook.xml.rels").decode()
rid = re.search(r'<sheet name="Collation Notes"[^>]*r:id="(rId\d+)"', wbx).group(1)
CN = "xl/" + re.search(rf'<Relationship Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)
same = [n for n in n6 if n in n7 and z6.read(n) == z7.read(n)]
changed = [n for n in n6 if n in n7 and z6.read(n) != z7.read(n)]
added = [n for n in n7 if n not in n6]; removed = [n for n in n6 if n not in n7]
check(changed == [CN] and not added and not removed and n6 == n7, f"unexpected part changes {changed} {added} {removed}")
ext = [n for n in n7 if n.startswith("xl/externalLinks/")]
check(not ext, "external link parts present")
wb6x = z6.read("xl/workbook.xml").decode()
res["package"] = {"v6_parts": len(n6), "v7_parts": len(n7), "identical": len(same), "changed": changed, "added": added, "removed": removed,
                  "external_links": len(ext), "defined_names": wbx.count("<definedName "), "defined_names_v6": wb6x.count("<definedName ")}
res["sheets"] = [(m.group(1).replace("&amp;", "&"), m.group(2)) for m in re.finditer(r'<sheet name="([^"]+)" sheetId="\d+" state="(\w+)"', wbx)]

f7 = openpyxl.load_workbook(V7); v7 = openpyxl.load_workbook(V7, data_only=True); lo = openpyxl.load_workbook(LO7, data_only=True)
v6w = openpyxl.load_workbook(V6, data_only=True)
HC = [s for s in f7.sheetnames if s.startswith("HC-")]
by = {}; new = 0; nd = 0; md_ = 0.0; tm = 0
hc = {"errors": 0, "max_diff": 0.0, "cells": 0}


def is_err(v):
    return isinstance(v, str) and v.startswith("#") and v.endswith(("!", "?", "A", "0"))


for s in f7.sheetnames:
    if s == "Collation Notes":
        continue
    e6 = {}; e7 = {}
    for row in v7[s].iter_rows():
        for c in row:
            if is_err(c.value):
                e7[c.value] = e7.get(c.value, 0) + 1
                if v6w[s][c.coordinate].value != c.value:
                    new += 1
            a, b = c.value, lo[s][c.coordinate].value
            if s in HC:
                if is_err(b):
                    hc["errors"] += 1
                if a is not None or b is not None:
                    hc["cells"] += 1
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    hc["max_diff"] = max(hc["max_diff"], abs(a - b))
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                if a != b:
                    nd += 1; md_ = max(md_, abs(a - b))
            elif a != b and not (a in (None, "") and b in (None, "")):
                if not (isinstance(a, datetime.datetime) or isinstance(b, datetime.datetime)):
                    tm += 1
    for row in v6w[s].iter_rows():
        for c in row:
            if is_err(c.value):
                e6[c.value] = e6.get(c.value, 0) + 1
    by[s] = [str(e6) if e6 else "none", str(e7) if e7 else "none"]
res["errors"] = {"by_sheet": by, "new": new}
res["hc_tabs"] = hc
check(new == 0 and hc["errors"] == 0, "new errors")
res["recalc"] = {"n_diff": nd, "max_diff": md_, "text_mismatch": tm}
check(md_ < 1e-6 and tm == 0, "recalculation differs from stored values")
cnf = 0; cnd = 0.0; cnt = 0
for row in f7["Collation Notes"].iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("="):
            cnf += 1
            a, b = v7["Collation Notes"][c.coordinate].value, lo["Collation Notes"][c.coordinate].value
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                cnd = max(cnd, abs(a - b))
            elif a != b:
                cnt += 1
banner_first = v7["Collation Notes"]["A3"].value == BANNER
res["cn"] = {"formulas": cnf, "max_diff": cnd, "text_mismatch": cnt, "banner_first": banner_first}
check(cnd < 1e-6 and cnt == 0 and cnf == 32, "Collation Notes formulas")
check(banner_first, "Collation Notes banner is not the first section")
md = open(MD).read(); nj = open(NJ).read()
check(md.split("\n")[2].startswith("> **" + BANNER), "md banner is not at the top")
res["recon_same"] = json.load(open(REC6)) == json.load(open(REC7))
check(res["recon_same"], "recon on v7 differs from recon on v6")
F = json.load(open(FIG7)); v1 = F["v1"]


def f0(x):
    return f"({abs(x):,.0f})" if x < 0 else f"{x:,.0f}"


def v6_fo_left(text):
    s6, a6 = re.escape(f"{v1['v6_stated']:,.0f}"), re.escape(f0(v1["v6_after"]))
    t = re.sub(rf"(v6 stated |v6: \+|payroll \+?){s6}(\.\d\d)?|\+{s6} -> |after {a6} -> |, {a6}\)", "", text)
    return len(re.findall(rf"(?<![\d,])({s6}|{a6})(?![\d]|,\d)", t))


res["v1_left"] = v6_fo_left(md) + v6_fo_left(nj)
res["phrase_left"] = sum(t.lower().count("no person-level overlap") for t in (md, nj))
check(res["v1_left"] == 0 and res["phrase_left"] == 0, "v6 I-28 FO figure or the v6 overlap wording left")
check(f"{v1['fo_effect']:,.0f}" in md and f"{v1['fo_effect']:,.0f}" in nj and f"{v1['after']:,.0f}" in md, "V1 figure missing")
for lab, path, key in (("privacy", PRIV, "privacy_v6:"), ("paylist", PAY, "paylist_v7:")):
    line = [l for l in open(path).read().splitlines() if l.startswith(key)][-1]
    res[lab] = line.replace(key + " ", "")
    check(re.search(r"(hits|exact hits) 0\b", line) is not None, f"{lab} check failed")
res["fails"] = fails
json.dump(res, open(OUT, "w"), indent=1, default=str)
print(f"analyze_v7: diff {d['total']}; parts identical {len(same)}/{len(n6)}, changed {changed}; new errors {new}; recalc diffs {nd} (max {md_:.1e}); "
      f"HC tabs {hc}; CN formulas {cnf} (max {cnd:.1e}), banner first {banner_first}; recon same {res['recon_same']}; v1_left {res['v1_left']}; "
      f"FAILS {fails}")
sys.exit(1 if fails else 0)
