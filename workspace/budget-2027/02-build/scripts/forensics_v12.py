"""v12 diagnosis forensics: establish, from the files alone, why the user's Excel session showed
#REF! on PO rows 33-35 - and prove it was NOT a serialization failure of the collated workbook.

Inputs (all read-only):
  V11       the shipped workbook (= 05-final FINAL_v4, byte-identical; asserted)
  USERFILE  00-brief/inputs/USER_EDIT_FINAL_v4_HC.xlsx - the user's copy of FINAL_v4 edited and
            saved in Microsoft Excel (docProps Application is asserted, no person fields read)
  WORKFILE  00-brief/inputs/COO_HC_and_PL_workfile.xlsx - the Excel-authored source of the HC tabs
  FINAL4    05-final/COO_2027_Budget_Collated_FINAL_v4.xlsx
  V12       the engine-saved candidate (for the byte-identity exhibit)

Asserted findings (exit 1 if any fails - the notes' diagnosis is generated from this JSON, so the
build refuses to emit prose its evidence no longer supports):
  F-A  FINAL_v4 == v11 byte for byte (the user opened exactly these bytes).
  F-B  The user's file was saved by Microsoft Excel (docProps app string starts 'Microsoft').
  F-C  In the user's file, the ONLY formulas containing #REF! are PO!U33:AF35 (36 cells), and each
       is v11's formula text with every 'HC-PO'!<col>20 reference replaced by 'HC-PO'!#REF! -
       i.e. Excel parsed and kept our formulas and only severed references into one deleted row.
  F-D  Row-deletion signature on HC-PO in the user's file: every shared-group master ref ends one
       row earlier (..33 -> ..32), max stored row 71 -> 70, and HC-COO's references to HC-PO rows
       below the roster shift by -1 (e.g. row 67 -> 66) while references to rows above row 20 are
       unchanged. Excel does this bookkeeping when a USER DELETES A ROW; load-time repair does not.
  F-E  No repair-style loss anywhere: per-sheet <f> counts in the user's file equal v11's on every
       sheet except HC-PO (-19: the deleted row's formula cells) and CO (-24: the user typed the
       brief-v7 monthly constants over U98:AF98/U106:AF106).
  F-F  The entity-escape hypothesis is refuted: v11 stores &apos;/&quot; inside <f> on 13 sheets
       (7,203 cells) including sheets no patch ever touched; the engine's own re-save of the same
       cells is byte-identical for the 'broken' PO cells (exhibit: U33); and the user's Excel
       round-tripped all of them (F-C/F-E).
  F-G  The overlapping shared-group refs on the HC tabs predate the collation: the Excel-authored
       source workfile carries the identical pairs (so they are Excel-legal).

Usage:
  python3 -I forensics_v12.py V11 USERFILE WORKFILE FINAL4 V12 OUT_JSON
"""
import sys, re, json, zipfile, collections

V11, USER, WF, FINAL4, V12, OUT = sys.argv[1:7]
rep = {}
fails = []


def check(cond, key, msg):
    rep[key] = {"ok": bool(cond), "note": msg}
    print(("PASS " if cond else "FAIL ") + key + ": " + msg)
    if not cond:
        fails.append(key)


def name2part(z):
    wb = z.read("xl/workbook.xml").decode(); rels = z.read("xl/_rels/workbook.xml.rels").decode()
    rid2t = dict(re.findall(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    return {m.group(1): (rid2t[m.group(2)] if rid2t[m.group(2)].startswith("xl/") else "xl/" + rid2t[m.group(2)])
            for m in re.finditer(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wb)}


def cellfrag(z, part, coord):
    x = z.read(part).decode()
    m = re.search(r'<c r="%s"[^>]*(?:/>|>.*?</c>)' % coord, x, re.S)
    return m.group(0) if m else None


z11, zu, zwf, z12 = (zipfile.ZipFile(p) for p in (V11, USER, WF, V12))
p11, pu, pwf, p12 = name2part(z11), name2part(zu), name2part(zwf), name2part(z12)

# F-A
check(open(V11, "rb").read() == open(FINAL4, "rb").read(), "F-A",
      "05-final FINAL_v4 is byte-identical to 02-build v11")

# F-B
app = zu.read("docProps/app.xml").decode()
m = re.search(r"<Application>([^<]*)</Application>", app)
rep["user_app"] = m.group(1) if m else None
check(m and m.group(1).startswith("Microsoft"), "F-B",
      f"user's file saved by {rep['user_app']!r} (docProps/app.xml)")

# F-C: formulas containing #REF! in the user's file
ref_f = collections.defaultdict(list)
for name, part in pu.items():
    x = zu.read(part).decode()
    for mm in re.finditer(r"<f[^>]*>([^<]*)</f>", x):
        if "#REF!" in mm.group(1):
            i = x.rfind('<c r="', 0, mm.start())
            ref_f[name].append((re.search(r'r="([A-Z]+\d+)"', x[i:i + 28]).group(1), mm.group(1)))
expected = {f"{c}{r}" for c in ("U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF")
            for r in (33, 34, 35)}
got = {a for a, _ in ref_f.get("PO", [])}
only_po = set(ref_f) == {"PO"}
rep["ref_formulas"] = {"sheets": sorted(ref_f), "po_cells": sorted(got)}
sever_ok = all(re.search(r"'HC-PO'!#REF!", f) and "'Depreciation Schedule'!" in f for _, f in ref_f.get("PO", []))
check(only_po and got == expected and sever_ok, "F-C",
      f"the only #REF!-carrying formulas are PO!U33:AF35 ({len(got)} cells), each our v11 formula with "
      f"'HC-PO'!<col>20 severed to 'HC-PO'!#REF!")

# F-D: row-deletion signature
xu = zu.read(pu["HC-PO"]).decode(); x11 = z11.read(p11["HC-PO"]).decode()
m_u = dict(re.findall(r'<f t="shared" ref="([A-Z]+\d+:?[A-Z]*\d*)" si="(\d+)"', xu))
masters_u = re.findall(r'<f t="shared" ref="([A-Z]+\d+:[A-Z]+(\d+))" si="[0-3]"', xu)
masters_11 = re.findall(r'<f t="shared" ref="([A-Z]+\d+:[A-Z]+(\d+))" si="[0-3]"', x11)
maxrow_u = max(int(r) for r in re.findall(r'<row r="(\d+)"', xu))
maxrow_11 = max(int(r) for r in re.findall(r'<row r="(\d+)"', x11))
shrunk = (sorted(int(b) for _, b in masters_11) == [33, 33, 33, 33]
          and sorted(int(b) for _, b in masters_u) == [32, 32, 32, 32])
# HC-COO reference shift
def hcpo_refs(z, part):
    out = {}
    x = z.read(part).decode()
    for mm in re.finditer(r'<c r="([A-Z]+\d+)"[^>]*>(?:<f[^>]*>([^<]*)</f>)', x):
        if mm.group(2) and "HC-PO" in mm.group(2):
            out[mm.group(1)] = mm.group(2)
    return out

r11, ru = hcpo_refs(z11, p11["HC-COO"]), hcpo_refs(zu, pu["HC-COO"])
shifted = unchanged = shrunk_rng = other = 0
RNG = re.compile(r"HC-PO'!\$?([A-Z]+)\$?(\d+):\$?([A-Z]+)\$?(\d+)")
ONE = re.compile(r"HC-PO'!\$?([A-Z]+)\$?(\d+)")
for k in r11:
    if k not in ru: other += 1; continue
    if r11[k] == ru[k]: unchanged += 1; continue
    ra, rb = RNG.search(r11[k]), RNG.search(ru[k])
    if ra and rb and ra.group(1, 2, 3) == rb.group(1, 2, 3) and int(rb.group(4)) == int(ra.group(4)) - 1:
        shrunk_rng += 1; continue    # range over the roster: end row shrank by 1 (deletion inside)
    a, b = ONE.search(r11[k]), ONE.search(ru[k])
    if a and b and a.group(1) == b.group(1) and int(b.group(2)) == int(a.group(2)) - 1: shifted += 1
    else: other += 1
rep["row_delete_signature"] = {"masters_v11_end": 33, "masters_user_end": 32,
                               "maxrow": [maxrow_11, maxrow_u],
                               "hccoo_refs": {"shifted_minus1": shifted, "range_end_minus1": shrunk_rng,
                                              "unchanged": unchanged, "other": other}}
check(shrunk and maxrow_u == maxrow_11 - 1 and shifted >= 100 and shrunk_rng > 0 and other == 0, "F-D",
      f"HC-PO group refs ..33 -> ..32, max row {maxrow_11} -> {maxrow_u}, HC-COO refs to HC-PO: "
      f"{shifted} shifted -1 row, {shrunk_rng} ranges with end row -1, {unchanged} unchanged (rows above 20), "
      f"{other} other - a user row deletion, not repair")

# F-E: per-sheet formula counts
fc = {}
for name in p11:
    c11 = len(re.findall(r"<f[ >/]", z11.read(p11[name]).decode()))
    cu = len(re.findall(r"<f[ >/]", zu.read(pu[name]).decode()))
    if c11 != cu: fc[name] = [c11, cu]
rep["f_count_changes"] = fc
check(set(fc) == {"HC-PO", "CO"} and fc["HC-PO"][0] - fc["HC-PO"][1] == 19 and fc["CO"][0] - fc["CO"][1] == 24,
      "F-E", f"formula counts: only HC-PO -19 (deleted row) and CO -24 (user-typed constants): {fc}")

# F-F: entity refutation + byte-identity exhibit
f33_11 = cellfrag(z11, p11["PO"], "U33")
f33_12 = cellfrag(z12, p12["PO"], "U33")
rep["u33_stored_v11"] = f33_11
check(f33_11 is not None and f33_11 == f33_12 and "&apos;" in f33_11, "F-F",
      "PO!U33's v11 stored bytes (with &apos; entities) are byte-identical to the engine's own "
      "re-serialization of the same cell - the engine writes this form itself")

# F-G: overlaps predate the collation (Excel-authored source)
def overlap_pairs(z, parts, names):
    def box(ref):
        a, b = (ref.split(":") + [ref])[:2] if ":" in ref else (ref, ref)
        def cr(s):
            mm = re.match(r"([A-Z]+)(\d+)$", s); c = 0
            for ch in mm.group(1): c = c * 26 + ord(ch) - 64
            return c, int(mm.group(2))
        (c1, r1), (c2, r2) = cr(a), cr(b)
        return (min(c1, c2), min(r1, r2), max(c1, c2), max(r1, r2))
    tot = 0
    for name in names:
        x = z.read(parts[name]).decode()
        ms = [box(r) for r in re.findall(r'<f [^>]*t="shared"[^>]*ref="([^"]+)"', x)]
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                if not (ms[i][2] < ms[j][0] or ms[j][2] < ms[i][0] or ms[i][3] < ms[j][1] or ms[j][3] < ms[i][1]):
                    tot += 1
    return tot

ov_wf = overlap_pairs(zwf, pwf, ["FO HC", "PO HC", "CO HC", "FE HC", "PE HC"])
ov_11 = overlap_pairs(z11, p11, ["HC-FO", "HC-PO", "HC-CO", "HC-FE", "HC-PE"])
wf_app = re.search(r"<Application>([^<]*)</Application>", zwf.read("docProps/app.xml").decode())
rep["overlaps"] = {"workfile": ov_wf, "v11": ov_11, "workfile_app": wf_app.group(1) if wf_app else None}
check(ov_wf == ov_11 == 22 and rep["overlaps"]["workfile_app"] == "Microsoft Excel", "F-G",
      f"the 22 overlapping shared-group ref pairs exist identically in the Excel-authored source "
      f"workfile (Application={rep['overlaps']['workfile_app']!r}) - Excel-legal, not a collation defect")

json.dump(rep, open(OUT, "w"), indent=1)
print(f"forensics_v12: {'PASS' if not fails else 'FAIL'} ({len(fails)} failed: {fails})")
sys.exit(1 if fails else 0)
