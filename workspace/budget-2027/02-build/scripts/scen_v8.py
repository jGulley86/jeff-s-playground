"""v8 scenario helper: a scratch copy of a workbook with one typed numeric input changed (analysis input only; never
shipped). Only that one <v> changes; every other zip part is copied byte for byte.

Usage:
  python3 -I scen_v8.py IN_XLSX OUT_SCRATCH_XLSX "SHEET!CELL" VALUE
"""
import sys, re, zipfile
from xml.sax.saxutils import escape

IN, OUT, REF, VAL = sys.argv[1:5]
sheet, cell = REF.rsplit("!", 1)
z = zipfile.ZipFile(IN)
wb = z.read("xl/workbook.xml").decode(); rels = z.read("xl/_rels/workbook.xml.rels").decode()
rid = re.search(rf'<sheet name="{re.escape(escape(sheet))}"[^>]*r:id="(rId\d+)"', wb).group(1)
part = "xl/" + re.search(rf'<Relationship Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)
zo = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
old = None
for info in z.infolist():
    data = z.read(info.filename)
    if info.filename == part:
        x = data.decode("utf-8")
        m = re.search(rf'(<c r="{cell}"[^>]*>)<v>([-0-9.E]+)</v></c>', x)
        assert m and "<f" not in m.group(0), f"{REF} must be a typed number"
        old = m.group(2)
        x = x[:m.start()] + f"{m.group(1)}<v>{VAL}</v></c>" + x[m.end():]
        data = x.encode("utf-8")
    zo.writestr(info, data)
zo.close()
assert old is not None
print(f"scratch {OUT}: {REF} {old} -> {VAL}")
