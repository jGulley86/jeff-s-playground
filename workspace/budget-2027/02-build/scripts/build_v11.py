"""v11 build: corrections pass on v10 (handoff 2026-10-10). Package patch of v10 - only two parts change:
  1. PO!AI33:AI35 (the 5110-5140 note texts): updated to the v10 base wording (B131 = 0 restores the v7 amount LESS
     HC-PO r20, which moved to CO, user decision 2026-10-10). Text only; styles kept; the U:AF formula cells and every
     value are untouched (same part, but only the three <is> texts differ).
  2. Collation Notes: regenerated from NOTES_JSON (cnotes_v6.render, the same generator as v4-v10).
Every other zip part is copied byte for byte (entry order, date_time and attributes preserved), so '0 value changes on
every other sheet' holds at the byte level. No file properties are read or written; the build is not date-dependent.

Usage:
  python3 -I build_v11.py V10_XLSX NOTES_JSON OUT_XLSX SPEC_JSON
"""
import sys, os, re, json, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cnotes_v6
from build_v8 import part_of, cell_xml

CELL = lambda coord: re.compile(rf'<c r="{coord}"(?: [^>]*?)?(?:/>|>.*?</c>)', re.S)

# the new AI33:AI35 note texts (GL, Depreciation Schedule idle row)
AI = {}
for row, (gl, dsrow) in {33: ("5110", 226), 34: ("5130", 227), 35: ("5140", 228)}.items():
    AI[row] = (
        f"v8: {gl} 2027 = 0, CAPITALISED (production labour capitalised, user-confirmed 2026-10-10); the labour "
        "reaches the P&L as 5011/5012 depreciation via 'Depreciation Schedule' sections 8-9. "
        f"v9: + 'Depreciation Schedule' row {dsrow} (idle-month labour expensed to this GL when B135 = 0; 0 while "
        "B135 = 1, booked). "
        "v10 (user decision 2026-10-10): PO HC r20 Material Handler = Logistics&WH seat MH-01 moved to CO 6610-6640, "
        "so the formula is (1 - 'Depreciation Schedule'!B131) x (the v7 amount less 'HC-PO' r20 at PO HC rates) + the "
        "idle row: B131 = 0 restores the v7 amount LESS HC-PO r20 (5110-5140 B131 base 652,820 -> 590,318). "
        "v11: note text updated to the v10 formula (text only; values unchanged)."
    )


def main(v10, notes_json, out, spec_out):
    z = zipfile.ZipFile(v10)
    po_part = part_of(z, "PO")
    cn_part = part_of(z, "Collation Notes")
    styles = z.read("xl/styles.xml").decode()

    # 1. PO!AI33:AI35
    x = z.read(po_part).decode("utf-8")
    spec = {"po": [], "parts": {"PO": po_part, "Collation Notes": cn_part}}
    for row, new_text in AI.items():
        coord = f"AI{row}"
        m = list(CELL(coord).finditer(x))
        assert len(m) == 1, (coord, len(m))
        old = m[0].group(0)
        ot = re.search(r"<t[^>]*>(.*?)</t>", old, re.S)
        assert ot, (coord, "expected an inlineStr note cell")
        old_text = ot.group(1)
        assert old_text.startswith(f"v8: {AI[row][4:8]} 2027 = 0, CAPITALISED"), (coord, old_text[:60])
        assert "B131 = 0 restores the v7 amount (sensitivity)." in old_text, coord
        style = int(re.search(r' s="(\d+)"', old).group(1))
        x = x[:m[0].start()] + cell_xml(coord, "text", new_text, style) + x[m[0].end():]
        spec["po"].append({"cell": coord, "old": old_text, "new": new_text})
    new_po = x.encode("utf-8")

    # 2. Collation Notes
    notes = json.load(open(notes_json))
    cn_xml, last, nform = cnotes_v6.render(z.read(cn_part).decode("utf-8"), notes, styles)
    spec["cn"] = {"rows": last, "formulas": nform, "sections": len(notes["sections"])}
    new_cn = cn_xml.encode("utf-8")

    repl = {po_part: new_po, cn_part: new_cn}
    zo = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    for info in z.infolist():
        data = z.read(info.filename)
        if info.filename in repl:
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zo.writestr(zi, repl[info.filename])
        else:
            zo.writestr(info, data)
    zo.close()
    json.dump(spec, open(spec_out, "w"), indent=1)
    print(f"build_v11 {out}: PO notes {sorted(c['cell'] for c in spec['po'])} replaced in {po_part}; Collation Notes "
          f"regenerated in {cn_part} ({last} rows, {nform} formulas, {spec['cn']['sections']} sections); every other "
          f"part copied byte for byte")


if __name__ == "__main__":
    main(*sys.argv[1:5])
