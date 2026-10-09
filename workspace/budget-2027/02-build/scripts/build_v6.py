"""v6 build: v5 package + six HC tabs copied from the COO HC & PL workfile + regenerated Collation Notes.

Usage:
  python3 -I build_v6.py V5_XLSX WORKFILE OUT_XLSX OUT_INFO_JSON [NOTES_JSON]

No budget value changes. Every v5 part is copied byte for byte except:
  - xl/workbook.xml, xl/_rels/workbook.xml.rels, [Content_Types].xml: six sheets appended after the last driver tab
    (Fld Eng Budget), in the order HC-FO, HC-PO, HC-CO, HC-FE, HC-PE, HC-COO;
  - xl/styles.xml: the workfile cell formats used by the HC tabs are APPENDED (fonts, fills, borders, number formats,
    cellXfs). Existing entries keep their index and bytes, so no existing cell changes format;
  - the Collation Notes part, when NOTES_JSON is given (same renderer as v4/v5, cnotes_v6.render).
New parts: xl/worksheets/sheet14.xml .. sheet19.xml (+ rels), their comments and VML drawings (the workfile's notes).

HC tabs are copied cell by cell from the workfile sheet XML:
  - values, formulas (including shared formulas), cached values, styles, column widths, row heights, frozen panes,
    data validations and cell notes are kept;
  - shared strings become inline strings (same text and runs), so sharedStrings.xml is untouched;
  - sheet references are renamed to the new tab names ('PO HC'! -> 'HC-PO'!, ...);
  - cells that link to an external workbook ([1] = the T&B rates file, D6/D7 on each dept tab) keep their cached value
    as a typed number; the formula text is listed in OUT_INFO_JSON and on Collation Notes. No external link is added;
  - theme and palette colours are resolved to RGB from the workfile's theme/palette (the v5 theme and palette differ),
    so the tabs look as they do in the workfile;
  - the 'tabSelected' flag is dropped (v5 keeps its active tab).
The script stops if any HC formula would still reference a sheet outside the six HC tabs or an external workbook.
"""
import sys, re, json, zipfile, colorsys
from xml.sax.saxutils import escape
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import cnotes_v6

V5, WF, OUT, INFO = sys.argv[1:5]
NOTES = sys.argv[5] if len(sys.argv) > 5 else None
ORDER = [("FO HC", "HC-FO"), ("PO HC", "HC-PO"), ("CO HC", "HC-CO"), ("FE HC", "HC-FE"), ("PE HC", "HC-PE"), ("COO HC", "HC-COO")]
RENAME = dict(ORDER)

zv = zipfile.ZipFile(V5)
zw = zipfile.ZipFile(WF)


def part_map(z):
    wb = z.read("xl/workbook.xml").decode(); rels = z.read("xl/_rels/workbook.xml.rels").decode()
    out = {}
    for m in re.finditer(r'<sheet name="([^"]+)" sheetId="(\d+)"[^>]*r:id="(rId\d+)"', wb):
        nm = m.group(1).replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
        tgt = re.search(rf'<Relationship Id="{m.group(3)}"[^>]*Target="([^"]+)"', rels).group(1)
        out[nm] = tgt if tgt.startswith("xl/") else "xl/" + tgt.lstrip("/")
    return out


vparts, wparts = part_map(zv), part_map(zw)

# ------------------------------------------------------------------ colours
STD_PALETTE = ("000000 FFFFFF FF0000 00FF00 0000FF FFFF00 FF00FF 00FFFF 000000 FFFFFF FF0000 00FF00 0000FF FFFF00 FF00FF "
               "00FFFF 800000 008000 000080 808000 800080 008080 C0C0C0 808080 9999FF 993366 FFFFCC CCFFFF 660066 FF8080 "
               "0066CC CCCCFF 000080 FF00FF FFFF00 00FFFF 800080 800000 008080 0000FF 00CCFF CCFFFF CCFFCC FFFF99 99CCFF "
               "FF99CC CC99FF FFCC99 3366FF 33CCCC 99CC00 FFCC00 FF9900 FF6600 666699 969696 003366 339966 003300 333300 "
               "993300 993366 333399 333333").split()
assert len(STD_PALETTE) == 64
wst = zw.read("xl/styles.xml").decode()
assert "<indexedColors>" not in wst, "workfile has a custom palette; resolve against it"
theme = zw.read("xl/theme/theme1.xml").decode()
cs = re.search(r"<a:clrScheme.*?</a:clrScheme>", theme, re.S).group(0)
scheme = {}
for k in ("dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"):
    blk = re.search(rf"<a:{k}>(.*?)</a:{k}>", cs, re.S).group(1)
    m = re.search(r'srgbClr val="([0-9A-Fa-f]{6})"', blk) or re.search(r'lastClr="([0-9A-Fa-f]{6})"', blk)
    scheme[k] = m.group(1).upper()
THEME_IDX = ["lt1", "dk1", "lt2", "dk2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"]


def tint_rgb(hexrgb, tint):
    r, g, b = (int(hexrgb[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = l * (1 + tint) if tint < 0 else l * (1 - tint) + tint
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "".join(f"{round(x * 255):02X}" for x in (r, g, b))


colour_stats = {"theme": 0, "indexed": 0}


def fix_colours(x):
    def rep(m):
        tag, attrs = m.group(1), m.group(2)
        th = re.search(r'theme="(\d+)"', attrs); ix = re.search(r'indexed="(\d+)"', attrs)
        tn = re.search(r'tint="([-0-9.Ee]+)"', attrs)
        if th:
            rgb = scheme[THEME_IDX[int(th.group(1))]]
            if tn:
                rgb = tint_rgb(rgb, float(tn.group(1)))
            colour_stats["theme"] += 1
            return f'<{tag} rgb="FF{rgb}"/>'
        if ix and int(ix.group(1)) < 64:
            colour_stats["indexed"] += 1
            return f'<{tag} rgb="FF{STD_PALETTE[int(ix.group(1))]}"/>'
        return m.group(0)
    return re.sub(r"<(color|fgColor|bgColor)(\s[^>]*?)/>", rep, x)


# ------------------------------------------------------------------ styles: append what the HC tabs use
def items(xml, tag, child):
    blk = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", xml, re.S)
    return re.findall(rf"<{child}(?:\s[^>]*)?/>|<{child}(?:\s[^>]*)?>.*?</{child}>", blk.group(1), re.S) if blk else []


vst = zv.read("xl/styles.xml").decode()
w_fonts, w_fills, w_borders = items(wst, "fonts", "font"), items(wst, "fills", "fill"), items(wst, "borders", "border")
w_xfs = items(wst, "cellXfs", "xf")
w_nf = {int(a): b for a, b in re.findall(r'<numFmt numFmtId="(\d+)" formatCode="([^"]*)"/>', wst)}
v_fonts, v_fills, v_borders = items(vst, "fonts", "font"), items(vst, "fills", "fill"), items(vst, "borders", "border")
v_xfs = items(vst, "cellXfs", "xf")
v_nf = {int(a): b for a, b in re.findall(r'<numFmt numFmtId="(\d+)" formatCode="([^"]*)"/>', vst)}
assert len(v_xfs) == int(re.search(r'<cellXfs count="(\d+)"', vst).group(1))
new_fonts, new_fills, new_borders, new_nf, new_xfs = [], [], [], {}, []
fmap, flmap, bmap, nmap, xmap = {}, {}, {}, {}, {}


def map_xf(i):
    if i in xmap:
        return xmap[i]
    xf = w_xfs[i]
    at = dict(re.findall(r'(\w+)="([^"]*)"', re.match(r"<xf([^>]*?)/?>", xf).group(1)))
    nf = int(at.get("numFmtId", 0))
    if nf >= 164:
        if nf not in nmap:
            code = w_nf[nf]
            same = [k for k, v in v_nf.items() if v == code]
            nmap[nf] = same[0] if same else max(list(v_nf) + list(new_nf) + [163]) + 1
            if not same:
                new_nf[nmap[nf]] = code
        nf = nmap[nf]
    fo = int(at.get("fontId", 0)); fi = int(at.get("fillId", 0)); bo = int(at.get("borderId", 0))
    if fo not in fmap:
        fmap[fo] = len(v_fonts) + len(new_fonts); new_fonts.append(fix_colours(w_fonts[fo]))
    if fi not in flmap:
        flmap[fi] = len(v_fills) + len(new_fills); new_fills.append(fix_colours(w_fills[fi]))
    if bo not in bmap:
        bmap[bo] = len(v_borders) + len(new_borders); new_borders.append(fix_colours(w_borders[bo]))
    body = re.search(r"<xf[^>]*?>(.*)</xf>", xf, re.S)
    body = body.group(1) if body else ""
    attrs = (f'numFmtId="{nf}" fontId="{fmap[fo]}" fillId="{flmap[fi]}" borderId="{bmap[bo]}" xfId="0" '
             f'applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"')
    if "<alignment" in body:
        attrs += ' applyAlignment="1"'
    if "<protection" in body:
        attrs += ' applyProtection="1"'
    new = f"<xf {attrs}>{body}</xf>" if body else f"<xf {attrs}/>"
    xmap[i] = len(v_xfs) + len(new_xfs); new_xfs.append(new)
    return xmap[i]


# ------------------------------------------------------------------ shared strings (workfile)
sst = zw.read("xl/sharedStrings.xml").decode()
SI = re.findall(r"<si>(.*?)</si>", sst, re.S)

# ------------------------------------------------------------------ transform each HC sheet
ext_cells, sheet_out, rels_out, comments_out, vml_out = [], {}, {}, {}, {}
first_new = max(int(re.search(r"sheet(\d+)\.xml", p).group(1)) for p in vparts.values()) + 1
v_vml = [n for n in zv.namelist() if n.startswith("xl/drawings/vmlDrawing")]
next_vml = max(int(re.search(r"(\d+)\.vml", n).group(1)) for n in v_vml) + 1 if v_vml else 1
stats = {}
for k, (src, dst) in enumerate(ORDER):
    xml = zw.read(wparts[src]).decode()
    n_str = n_f = n_ext = 0

    def cell(m):
        attrs, inner = m.group(1), m.group(2)
        ref = re.search(r'r="([A-Z]+\d+)"', attrs).group(1)
        attrs = re.sub(r' s="(\d+)"', lambda mm: f' s="{map_xf(int(mm.group(1)))}"', attrs)
        if inner is None:
            return f"<c{attrs}/>"
        fm = re.search(r"<f[^>]*>(.*?)</f>", inner, re.S)
        if fm and re.search(r"\[\d+\]", fm.group(1)):
            v = re.search(r"<v>(.*?)</v>", inner).group(1)
            ext_cells.append({"sheet": dst, "cell": ref, "formula": fm.group(1).replace("&amp;", "&").replace("&quot;", '"')
                              .replace("&lt;", "<").replace("&gt;", ">"), "value": v})
            if ' t="str"' in attrs:
                return f'<c{attrs.replace(" t=\"str\"", " t=\"inlineStr\"")}><is><t>{v}</t></is></c>'
            assert ' t="' not in attrs, (dst, ref, attrs)
            return f"<c{attrs}><v>{v}</v></c>"
        if ' t="s"' in attrs:
            idx = int(re.search(r"<v>(\d+)</v>", inner).group(1))
            return f'<c{attrs.replace(" t=\"s\"", " t=\"inlineStr\"")}><is>{SI[idx]}</is></c>'
        if fm:
            body = fm.group(1)
            for a, b in RENAME.items():
                body = body.replace(f"'{a}'!", f"'{b}'!")
            for sref in re.findall(r"'([^']+)'!", body):
                assert sref in RENAME.values(), (dst, ref, sref)
            assert not re.search(r"\[\d+\]", body)
            inner = inner[:fm.start(1)] + body + inner[fm.end(1):]
        return f"<c{attrs}>{inner}</c>"

    xml = re.sub(r"<c(\s[^>]*?)(?:/>|>(.*?)</c>)", cell, xml, flags=re.S)
    xml = re.sub(r'(<row\s[^>]*?) s="(\d+)"', lambda m: f'{m.group(1)} s="{map_xf(int(m.group(2)))}"', xml)
    xml = re.sub(r'(<col\s[^>]*?) style="(\d+)"', lambda m: f'{m.group(1)} style="{map_xf(int(m.group(2)))}"', xml)
    xml = xml.replace(' tabSelected="1"', "")
    for a, b in RENAME.items():                                   # data validations / other formula text
        xml = xml.replace(f"'{a}'!", f"'{b}'!")
    assert "[1]" not in xml and "[2]" not in xml
    num = first_new + k
    sheet_out[f"xl/worksheets/sheet{num}.xml"] = xml
    srel_name = wparts[src].replace("worksheets/", "worksheets/_rels/") + ".rels"
    if srel_name in zw.namelist():
        srel = zw.read(srel_name).decode()
        for rid, typ, tgt in re.findall(r'<Relationship Id="(rId\d+)" Type="([^"]+)" Target="([^"]+)"/>', srel):
            if typ.endswith("/comments"):
                new_t = f"../comments{num}.xml"
                comments_out[f"xl/comments{num}.xml"] = zw.read("xl/" + tgt.replace("../", "")).decode()
            elif typ.endswith("/vmlDrawing"):
                new_t = f"../drawings/vmlDrawing{next_vml}.vml"
                vml_out[f"xl/drawings/vmlDrawing{next_vml}.vml"] = zw.read("xl/" + tgt.replace("../", ""))
                next_vml += 1
            else:
                raise SystemExit(f"unexpected sheet relationship {typ} on {src}")
            srel = srel.replace(f'Target="{tgt}"', f'Target="{new_t}"')
        rels_out[f"xl/worksheets/_rels/sheet{num}.xml.rels"] = srel
    stats[dst] = {"part": f"xl/worksheets/sheet{num}.xml", "from": src,
                  "cells": len(re.findall(r"<c\s", xml)), "formulas": xml.count("<f")}

# ------------------------------------------------------------------ styles.xml (append only)
def append_block(xml, tag, new_items):
    if not new_items:
        return xml
    m = re.search(rf'<{tag} count="(\d+)"', xml)
    n = int(m.group(1))
    xml = xml[:m.start(1)] + str(n + len(new_items)) + xml[m.end(1):]
    i = xml.index(f"</{tag}>")
    return xml[:i] + "".join(new_items) + xml[i:]


st = vst
st = append_block(st, "numFmts", [f'<numFmt numFmtId="{k}" formatCode="{v}"/>' for k, v in sorted(new_nf.items())])
st = append_block(st, "fonts", new_fonts)
st = append_block(st, "fills", new_fills)
st = append_block(st, "borders", new_borders)
st = append_block(st, "cellXfs", new_xfs)
for tag, child, old in (("fonts", "font", v_fonts), ("fills", "fill", v_fills), ("borders", "border", v_borders), ("cellXfs", "xf", v_xfs)):
    assert items(st, tag, child)[:len(old)] == old, f"existing {tag} changed"

# ------------------------------------------------------------------ workbook, rels, content types
wbx = zv.read("xl/workbook.xml").decode()
rels = zv.read("xl/_rels/workbook.xml.rels").decode()
ct = zv.read("[Content_Types].xml").decode()
assert re.findall(r'<sheet name="([^"]+)"', wbx)[-1] == "Fld Eng Budget"
max_sid = max(int(x) for x in re.findall(r'<sheet name="[^"]+" sheetId="(\d+)"', wbx))
max_rid = max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels))
add_sheets, add_rels, add_ct = "", "", ""
for k, (src, dst) in enumerate(ORDER):
    num = first_new + k
    add_sheets += f'<sheet name="{dst}" sheetId="{max_sid + 1 + k}" state="visible" r:id="rId{max_rid + 1 + k}"/>'
    add_rels += (f'<Relationship Id="rId{max_rid + 1 + k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                 f'relationships/worksheet" Target="worksheets/sheet{num}.xml"/>')
    add_ct += (f'<Override PartName="/xl/worksheets/sheet{num}.xml" '
               f'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
for p in comments_out:
    add_ct += f'<Override PartName="/{p}" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.comments+xml"/>'
for p in vml_out:
    add_ct += f'<Override PartName="/{p}" ContentType="application/vnd.openxmlformats-officedocument.vmlDrawing"/>'
for p in rels_out:
    add_ct += f'<Override PartName="/{p}" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
assert wbx.count("</sheets>") == 1 and rels.count("</Relationships>") == 1 and ct.count("</Types>") == 1
wbx = wbx.replace("</sheets>", add_sheets + "</sheets>")
rels = rels.replace("</Relationships>", add_rels + "</Relationships>")
ct = ct.replace("</Types>", add_ct + "</Types>")
new_names = set(sheet_out) | set(rels_out) | set(comments_out) | set(vml_out)
assert not (new_names & set(zv.namelist())), "new part name collides with a v5 part"

# ------------------------------------------------------------------ write
CN_PART = vparts["Collation Notes"]
zout = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
changed = []
for info in zv.infolist():
    data = zv.read(info.filename)
    new = None
    if info.filename == "xl/workbook.xml":
        new = wbx
    elif info.filename == "xl/_rels/workbook.xml.rels":
        new = rels
    elif info.filename == "[Content_Types].xml":
        new = ct
    elif info.filename == "xl/styles.xml":
        new = st
    elif info.filename == CN_PART and NOTES:
        new, last, nform = cnotes_v6.render(data.decode("utf-8"), json.load(open(NOTES)), vst)
    if new is None:
        zout.writestr(info, data)
    else:
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = info.external_attr
        zout.writestr(zi, new.encode("utf-8")); changed.append(info.filename)
for name in sorted(sheet_out) + sorted(rels_out) + sorted(comments_out) + sorted(vml_out):
    data = sheet_out.get(name) or rels_out.get(name) or comments_out.get(name) or vml_out.get(name)
    zout.writestr(name, data if isinstance(data, bytes) else data.encode("utf-8"))
zout.close()
info = {"sheets": stats, "external_cells": ext_cells, "parts_added": sorted(new_names),
        "styles_appended": {"cellXfs": len(new_xfs), "fonts": len(new_fonts), "fills": len(new_fills),
                            "borders": len(new_borders), "numFmts": len(new_nf)},
        "colours_resolved": colour_stats, "v5_cellXfs": len(v_xfs)}
json.dump(info, open(INFO, "w"), indent=1)
print(f"built {OUT}: +{len(ORDER)} HC tabs ({', '.join(d for _, d in ORDER)}); external cells stored as values "
      f"{len(ext_cells)}; styles appended {info['styles_appended']}; parts changed {changed}")
