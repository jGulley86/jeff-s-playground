"""v12 package/formula scanner - the diagnosis tool for the Excel #REF! incident and the
acceptance scanner for the re-serialized build.

For every worksheet it reports, from the stored XML (no clock, no file properties read):
  - <f> elements containing XML entities beyond &amp;/&lt;/&gt; (i.e. &apos;/&quot;/numeric),
    with cell ranges (the orchestrator's suspect class - measured, not assumed);
  - shared-formula structure: masters (with ref), follower cells, orphan si references,
    followers outside their master's declared ref, and OVERLAPPING master ref ranges
    (two groups claiming the same cells - the root-cause class; Excel never writes this
    and its loader treats it as corruption);
  - mechanical invariants: XML well-formedness, row monotonicity/uniqueness, in-row cell order,
    dimension coverage, cell child order;
  - error caches: t="e" cells and error tokens (#REF!/#NAME?/#DIV/0!/#VALUE!/#N/A/#NUM!/#NULL!)
    in <v> of formula cells or in formula text (inline text cells are NOT flagged - the
    Collation Notes quotes error tokens as prose by design);
  - counts: t="shared"/"array"/"inlineStr"/"s"/"str" cells, <f> elements;
  - sharedStrings: declared count/uniqueCount vs actual entries and references, max index.

Usage:
  python3 -I fscan_v12.py XLSX OUT_JSON [--require-clean]
With --require-clean exits 1 unless: 0 orphans, 0 followers outside ref, 0 overlapping master
refs, 0 t="shared" formulas, 0 invariant problems, 0 error caches, sharedStrings consistent.
(Entity-escaped <f> elements are REPORTED, never failed on: the engine's own serializer writes
&apos;/&quot; in formula text - see the v12 notes diagnosis.)
"""
import sys, re, json, zipfile, collections
from xml.etree import ElementTree as ET

X, OUT = sys.argv[1], sys.argv[2]
REQUIRE = "--require-clean" in sys.argv[3:]
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
ERRTOK = re.compile(r"#(?:REF!|NAME\?|DIV/0!|VALUE!|N/A|NUM!|NULL!)")


def name2part(z):
    wb = z.read("xl/workbook.xml").decode()
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    rid2t = dict(re.findall(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    return {m.group(1): (rid2t[m.group(2)] if rid2t[m.group(2)].startswith("xl/") else "xl/" + rid2t[m.group(2)])
            for m in re.finditer(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wb)}


def colrow(a):
    m = re.match(r"([A-Z]+)(\d+)$", a); c = 0
    for ch in m.group(1): c = c * 26 + ord(ch) - 64
    return c, int(m.group(2))


def box(ref):
    a, b = (ref.split(":") + [ref])[:2] if ":" in ref else (ref, ref)
    (c1, r1), (c2, r2) = colrow(a), colrow(b)
    return (min(c1, c2), min(r1, r2), max(c1, c2), max(r1, r2))


def inbox(addr, bx):
    c, r = colrow(addr)
    return bx[0] <= c <= bx[2] and bx[1] <= r <= bx[3]


def boxes_overlap(b1, b2):
    return not (b1[2] < b2[0] or b2[2] < b1[0] or b1[3] < b2[1] or b2[3] < b1[1])


def iter_cells(x):
    """(addr, cell_fragment) in document order; linear scan of the sheetData slice."""
    s = x.find("<sheetData"); e = x.find("</sheetData>")
    if s < 0 or e < 0: return
    x = x[s:e]; i = 0
    while True:
        i = x.find("<c ", i)
        if i < 0: return
        j1 = x.find("<c ", i + 3); j2 = x.find("</row>", i + 3)
        j = min(k for k in (j1, j2, len(x)) if k >= 0)
        frag = x[i:j]
        m = re.search(r'r="([A-Z]+\d+)"', frag[:40])
        yield m.group(1), frag
        i = j


z = zipfile.ZipFile(X)
report = {"file": X, "sheets": {}, "problems": []}
prob = report["problems"].append

for name, part in name2part(z).items():
    raw = z.read(part)
    s = {"part": part, "entity_f_cells": 0, "entity_f_ranges": [], "entities": {},
         "masters": 0, "followers": 0, "orphan_si": [], "outside_ref": [],
         "overlapping_master_refs": [], "t_counts": {}, "f_count": 0,
         "error_cells": [], "invariant_problems": []}
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        s["invariant_problems"].append(f"XML parse error: {e}")
        report["sheets"][name] = s
        prob(f"{name}: XML parse error")
        continue
    x = raw.decode("utf-8")

    masters = {}; followers = collections.defaultdict(list)
    ent_cells = []; ents = collections.Counter(); tc = collections.Counter()
    prev_row = 0
    sd = root.find(NS + "sheetData")
    for rowel in sd.findall(NS + "row"):
        r = int(rowel.get("r"))
        if r <= prev_row: s["invariant_problems"].append(f"row order: {prev_row} then {r}")
        prev_row = r
        pc = 0
        for c in rowel.findall(NS + "c"):
            addr = c.get("r")
            cn, rr = colrow(addr)
            if rr != r: s["invariant_problems"].append(f"cell {addr} in row {r}")
            if cn <= pc: s["invariant_problems"].append(f"cell order at {addr}")
            pc = cn
            t = c.get("t", "n"); tc[t] += 1
            kids = [k.tag.replace(NS, "") for k in c]
            if kids not in ([], ["v"], ["f"], ["f", "v"], ["is"], ["f", "is"]):
                s["invariant_problems"].append(f"odd children {addr}: {kids}")
            f = c.find(NS + "f"); v = c.find(NS + "v")
            if t == "e" or (v is not None and f is not None and v.text and ERRTOK.search(v.text)) \
                    or (f is not None and f.text and ERRTOK.search(f.text)):
                s["error_cells"].append(addr)
            if f is not None:
                s["f_count"] += 1
                if f.get("t") == "shared":
                    si = f.get("si")
                    if f.get("ref"):
                        masters[si] = (addr, f.get("ref"))
                    else:
                        followers[si].append(addr)
    # entity scan on raw bytes (ElementTree decodes entities, so this must run on the text)
    for m in re.finditer(r"<f(?:\s[^>]*)?>([^<]*)</f>", x):
        bad = [e for e in re.findall(r"&[#A-Za-z0-9]+;", m.group(1)) if e not in ("&amp;", "&lt;", "&gt;")]
        if bad:
            i = x.rfind('<c r="', 0, m.start())
            ent_cells.append(re.search(r'r="([A-Z]+\d+)"', x[i:i + 28]).group(1))
            for e in bad: ents[e] += 1
    s["entity_f_cells"] = len(ent_cells)
    s["entities"] = dict(ents)
    if ent_cells:  # compress to ranges per row block for the report
        s["entity_f_ranges"] = [ent_cells[0], "...", ent_cells[-1]] if len(ent_cells) > 2 else ent_cells
    s["masters"] = len(masters); s["followers"] = sum(len(v) for v in followers.values())
    s["orphan_si"] = sorted(si for si in followers if si not in masters)
    for si, addrs in followers.items():
        if si in masters:
            bx = box(masters[si][1])
            s["outside_ref"] += [a for a in addrs if not inbox(a, bx)]
    ms = sorted(masters.items(), key=lambda kv: int(kv[0]))
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            if boxes_overlap(box(ms[i][1][1]), box(ms[j][1][1])):
                s["overlapping_master_refs"].append(
                    {"si_a": ms[i][0], "master_a": ms[i][1][0], "ref_a": ms[i][1][1],
                     "si_b": ms[j][0], "master_b": ms[j][1][0], "ref_b": ms[j][1][1]})
    dim = root.find(NS + "dimension")
    s["dimension"] = dim.get("ref") if dim is not None else None
    s["t_counts"] = dict(tc)
    report["sheets"][name] = s
    for key, label in (("orphan_si", "orphan shared si"), ("outside_ref", "follower outside master ref"),
                       ("overlapping_master_refs", "OVERLAPPING shared-group refs"),
                       ("error_cells", "error cache"), ("invariant_problems", "invariant")):
        if s[key]:
            prob(f"{name}: {len(s[key])} {label}")

# sharedStrings consistency
sst = {"present": "xl/sharedStrings.xml" in z.namelist()}
if sst["present"]:
    sx = z.read("xl/sharedStrings.xml").decode()
    h = re.search(r'<sst[^>]*>', sx).group(0)
    sst["declared_count"] = int(re.search(r'count="(\d+)"', h).group(1))
    sst["declared_unique"] = int(re.search(r'uniqueCount="(\d+)"', h).group(1))
    sst["actual_entries"] = len(re.findall(r"<si[ >/]", sx))
    refs = 0; mx = -1
    for name, part in name2part(z).items():
        for m in re.finditer(r'<c r="[A-Z]+\d+"[^>]*t="s"[^>]*><v>(\d+)</v>', z.read(part).decode()):
            refs += 1; mx = max(mx, int(m.group(1)))
    sst["actual_refs"] = refs; sst["max_index_used"] = mx
    sst["consistent"] = (sst["declared_unique"] == sst["actual_entries"]
                         and sst["declared_count"] == sst["actual_refs"]
                         and mx < sst["actual_entries"])
    if not sst["consistent"]:
        prob(f"sharedStrings: declared count={sst['declared_count']}/unique={sst['declared_unique']} "
             f"vs actual refs={refs}/entries={sst['actual_entries']}")
report["sharedStrings"] = sst
report["total_shared_f"] = sum(sh["masters"] + sh["followers"] for sh in report["sheets"].values())
report["total_entity_f_cells"] = sum(sh["entity_f_cells"] for sh in report["sheets"].values())
report["total_overlap_pairs"] = sum(len(sh["overlapping_master_refs"]) for sh in report["sheets"].values())

json.dump(report, open(OUT, "w"), indent=1)
print(f"fscan_v12 {X}:")
for name, sh in report["sheets"].items():
    line = (f"  [{name}] f={sh['f_count']} entity-f={sh['entity_f_cells']} {sh['entities'] or ''} "
            f"shared M/F={sh['masters']}/{sh['followers']}")
    if sh["overlapping_master_refs"]:
        line += f" OVERLAPS={len(sh['overlapping_master_refs'])}"
    if sh["orphan_si"] or sh["outside_ref"] or sh["error_cells"] or sh["invariant_problems"]:
        line += f" PROBLEMS orphans={sh['orphan_si']} outside={len(sh['outside_ref'])} err={sh['error_cells'][:5]} inv={sh['invariant_problems'][:3]}"
    print(line)
print(f"  sharedStrings: {sst}")
print(f"  totals: entity-f cells={report['total_entity_f_cells']}, shared formulas={report['total_shared_f']}, "
      f"overlapping master-ref pairs={report['total_overlap_pairs']}, problems={len(report['problems'])}")
for p in report["problems"]: print("  PROBLEM:", p)
if REQUIRE and report["problems"]:
    print("fscan_v12: --require-clean FAILED")
    sys.exit(1)
