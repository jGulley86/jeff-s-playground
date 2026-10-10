"""v11: cached values for the new live check formulas (Collation Notes H78:H81) from a full LibreOffice
recalculation of the stage build, plus a stage-level sanity check that nothing else moved.

Usage:
  python3 -I hvals_v11.py STAGE_XLSX STAGE_LO_XLSX OUT_HVALS_JSON

- STAGE_XLSX: build_v11.py output rendered with H78:H81 = live formulas, cached 0.0 placeholders.
- STAGE_LO_XLSX: recalc.sh output (full LibreOffice recalculation).
- Stops if: any error cell anywhere; any numeric cell outside Collation Notes moves > 1e-6 vs its stored value; any
  non-numeric cell differs; any pre-existing Collation Notes formula moves > 1e-6; |H78..H81| > 1e-6 (the checks must
  still be 0); H81 != H78+H79+H80 (> 1e-9).
- Writes {"H78": float, ...} with the exact doubles LibreOffice computed (json round-trips repr, so build_v11's
  final render stores exactly these values and a recalculation of the final file reproduces them).
"""
import sys, re, json
import openpyxl

STAGE, LO, OUT = sys.argv[1:4]
ERR = re.compile(r"^#(REF!|NAME\?|VALUE!|DIV/0!|N/A|NUM!|NULL!)$")
CN = "Collation Notes"
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)

a = openpyxl.load_workbook(STAGE, data_only=True)
b = openpyxl.load_workbook(LO, data_only=True)
assert a.sheetnames == b.sheetnames

errors = []
mx = 0.0
ncells = 0
nonnum = []
cn_mx = 0.0
for s in a.sheetnames:
    wa, wb = a[s], b[s]
    for row in wb.iter_rows():
        for c in row:
            if isinstance(c.value, str) and ERR.match(c.value):
                errors.append(f"{s}!{c.coordinate}")
    for row in wa.iter_rows():
        for c in row:
            x, y = c.value, wb[c.coordinate].value
            if x is None and y is None:
                continue
            if s == CN:
                if isnum(x) and isnum(y) and c.coordinate not in ("H78", "H79", "H80", "H81"):
                    cn_mx = max(cn_mx, abs(x - y))
                continue
            if isnum(x) and isnum(y):
                ncells += 1
                mx = max(mx, abs(x - y))
            elif x != y and not (x in (None, "") and y in (None, "")):
                nonnum.append(f"{s}!{c.coordinate}")

H = {k: b[CN][k].value for k in ("H78", "H79", "H80", "H81")}
assert all(isnum(v) for v in H.values()), H
assert not errors, ("error cells after recalculation", errors[:10])
assert mx <= 1e-6, ("a cell outside Collation Notes moved", mx)
assert not nonnum, ("non-numeric differences", nonnum[:10])
assert cn_mx <= 1e-6, ("a pre-existing Collation Notes formula moved", cn_mx)
assert max(abs(v) for v in H.values()) <= 1e-6, ("the H78:H81 checks are not 0", H)
assert abs(H["H81"] - (H["H78"] + H["H79"] + H["H80"])) <= 1e-9, H
json.dump({k: float(v) for k, v in H.items()}, open(OUT, "w"))
print(f"hvals_v11: H78..H81 = {[f'{v:.2e}' for v in H.values()]} (max |check| {max(abs(v) for v in H.values()):.1e}); "
      f"stage recalc clean: errors 0, non-CN max diff {mx:.1e} over {ncells:,} numeric cells, non-numeric 0, "
      f"CN pre-existing formulas max diff {cn_mx:.1e}")
