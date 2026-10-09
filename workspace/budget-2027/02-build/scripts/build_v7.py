"""v7 build: the v6 package with a regenerated Collation Notes sheet. Nothing else changes.

Usage:
  python3 -I build_v7.py V6_XLSX NOTES_JSON OUT_XLSX

Every v6 zip part is copied byte for byte (same order, same zip info) except the Collation Notes worksheet part, which
is rendered from NOTES_JSON by cnotes_v6.render (the renderer used since v4). No budget cell, no other sheet, no style,
no defined name and no workbook-level part changes.
"""
import sys, re, json, zipfile, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cnotes_v6

V6, NOTES, OUT = sys.argv[1:4]
z = zipfile.ZipFile(V6)
wb = z.read("xl/workbook.xml").decode(); rels = z.read("xl/_rels/workbook.xml.rels").decode()
rid = re.search(r'<sheet name="Collation Notes"[^>]*r:id="(rId\d+)"', wb).group(1)
CN = "xl/" + re.search(rf'<Relationship Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)
styles = z.read("xl/styles.xml").decode()
notes = json.load(open(NOTES))
zo = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
changed = []
for info in z.infolist():
    data = z.read(info.filename)
    if info.filename == CN:
        xml, last, nform = cnotes_v6.render(data.decode("utf-8"), notes, styles)
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = info.external_attr
        zo.writestr(zi, xml.encode("utf-8")); changed.append(info.filename)
    else:
        zo.writestr(info, data)
zo.close()
assert changed == [CN]
print(f"built {OUT}: Collation Notes ({CN}) regenerated: {len(notes['sections'])} sections, {last} rows, {nform} formulas; "
      f"all other {len(z.infolist()) - 1} parts copied byte for byte")
