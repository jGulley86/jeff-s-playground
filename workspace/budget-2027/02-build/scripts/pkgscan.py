"""Scan an .xlsx package at XML level: parts, external links, defined names and where names are used.

Usage:
  python3 -I pkgscan.py XLSX OUT_JSON [PRUNED_CSV]

Reads only. Usage of a defined name is searched in every formula-bearing element of every XML part
under xl/: cell formulas (<f>), data validations (<formula1>/<formula2>, x14 <xm:f>), conditional
formats (<formula>), chart series/axis references (<c:f>), plus the text of the other defined names
(names that refer to names). Print areas / print titles are the built-in _xlnm.* names and are
reported separately. If PRUNED_CSV is given, the scan also confirms none of those names is referenced.

Also importable (by prune_names.py) through importlib; it has no side effects on import.
"""
import sys, re, json, zipfile, collections, csv
from lxml import etree

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
FORMULA_TAGS = {"f", "formula", "formula1", "formula2"}
STR_LIT = re.compile(r'"(?:[^"]|"")*"')
QSHEET = re.compile(r"'(?:[^']|'')+'!")
SHEET = re.compile(r"\b[A-Za-z_][A-Za-z0-9_.]*!")
CELLREF = re.compile(r"\$?\b[A-Z]{1,3}\$?\d+\b")
COLRANGE = re.compile(r"\$?\b[A-Z]{1,3}:\$?[A-Z]{1,3}\b")
ROWRANGE = re.compile(r"\$?\b\d+:\$?\d+\b")
ERRS = re.compile(r"#(?:N/A|REF!|NAME\?|VALUE!|DIV/0!|NUM!|NULL!)")
TOKEN = re.compile(r"(?<![A-Za-z0-9_.\\])([A-Za-z_\\][A-Za-z0-9_.\\?]*)(?![A-Za-z0-9_.\\?(])")


def name_tokens(text):
    """Identifier tokens in a formula that could be defined-name references (upper-cased)."""
    t = STR_LIT.sub("", text or "")
    t = ERRS.sub("", t)
    t = QSHEET.sub("", t)
    t = SHEET.sub("", t)
    t = CELLREF.sub("", t)
    t = COLRANGE.sub("", t)
    t = ROWRANGE.sub("", t)
    return {m.group(1).upper() for m in TOKEN.finditer(t)} - {"TRUE", "FALSE"}


def is_external_or_ref(text):
    """Prune criterion from the v2 handoff: target contains '[' or '.xls' (any case) or '#REF!'."""
    t = text or ""
    return ("[" in t) or (".xls" in t.lower()) or ("#REF!" in t)


def read_names(z):
    root = etree.fromstring(z.read("xl/workbook.xml"))
    out = []
    for d in root.iter("{%s}definedName" % MAIN):
        out.append({"name": d.get("name"), "text": d.text or "", "local": d.get("localSheetId"),
                    "hidden": d.get("hidden")})
    sheets = [s.get("name") for s in root.iter("{%s}sheet" % MAIN)]
    return out, sheets


def formula_texts(z):
    """Yield (part, kind, text) for every formula-bearing element in every xl/*.xml part except workbook.xml."""
    for info in z.infolist():
        n = info.filename
        if not n.startswith("xl/") or not n.endswith(".xml") or n == "xl/workbook.xml" or n == "xl/sharedStrings.xml":
            continue
        with z.open(n) as fh:
            for _, el in etree.iterparse(fh, events=("end",), huge_tree=True):
                tag = el.tag
                if not isinstance(tag, str):
                    continue
                local = tag.rsplit("}", 1)[-1]
                if local in FORMULA_TAGS and el.text:
                    kind = ("chart" if n.startswith("xl/charts/") else
                            "cell" if local == "f" and tag.startswith("{%s}" % MAIN) else
                            "cf" if local == "formula" else
                            "dv" if local in ("formula1", "formula2") else "other-f")
                    yield n, kind, el.text
                el.clear()


def usage(z, names):
    """Return {NAME_UPPER: {kind: count}} for names referenced from parts and from other names."""
    upper = {d["name"].upper() for d in names}
    used = collections.defaultdict(collections.Counter)
    counts = collections.Counter()
    for part, kind, text in formula_texts(z):
        counts[kind] += 1
        for tok in name_tokens(text) & upper:
            used[tok][kind] += 1
    by_name_refs = {}
    for d in names:
        refs = name_tokens(d["text"]) & upper - {d["name"].upper()}
        by_name_refs[d["name"].upper()] = refs
    return used, by_name_refs, counts


def scan(path, pruned=None):
    z = zipfile.ZipFile(path)
    parts = sorted(i.filename for i in z.infolist())
    names, sheets = read_names(z)
    used, by_name_refs, counts = usage(z, names)
    used_from_names = collections.Counter()
    for src, refs in by_name_refs.items():
        for r in refs:
            used_from_names[r] += 1
    cats = collections.Counter()
    ext_like = []
    for d in names:
        t = d["text"]
        k = ("#REF!" if "#REF!" in t else
             "external-looking ('[' or '.xls')" if is_external_or_ref(t) else
             "array constant" if t.startswith("{") else
             "string constant" if t.startswith('"') else
             "range/other")
        cats[k] += 1
        if is_external_or_ref(t) and "#REF!" not in t:
            ext_like.append({"name": d["name"], "text": t[:200], "quoted_string_constant": t.startswith(('"', "{"))})
    res = {
        "file": path,
        "parts": parts,
        "external_link_parts": [p for p in parts if p.startswith("xl/externalLinks/")],
        "external_reference_elements": z.read("xl/workbook.xml").count(b"<externalReference"),
        "chart_parts": [p for p in parts if p.startswith("xl/charts/")],
        "defined_names_total": len(names),
        "defined_names_by_category": dict(cats),
        "builtin_xlnm_names": [d["name"] for d in names if d["name"].startswith("_xlnm.")],
        "sheet_scoped_names": [f"{d['name']}@{sheets[int(d['local'])]}" for d in names if d["local"] is not None],
        "external_looking_names": ext_like,
        "formula_elements_scanned": dict(counts),
        "names_used_in_parts": {k: dict(v) for k, v in used.items()},
        "names_used_by_other_names": dict(used_from_names),
        "names_prunable_criterion": sum(1 for d in names if is_external_or_ref(d["text"])),
        "names_prunable_and_unused": sum(1 for d in names if is_external_or_ref(d["text"])
                                         and d["name"].upper() not in used and d["name"].upper() not in used_from_names),
        "sheets": sheets,
    }
    if pruned is not None:
        pu = {p.upper() for p in pruned}
        res["pruned_names_checked"] = len(pu)
        res["pruned_names_still_defined"] = sorted(d["name"] for d in names if d["name"].upper() in pu)
        res["pruned_names_referenced"] = sorted(n for n in pu if n in used or n in used_from_names)
    return res


def main():
    path, out = sys.argv[1], sys.argv[2]
    pruned = None
    if len(sys.argv) > 3:
        with open(sys.argv[3], newline="") as fh:
            pruned = [row["name"] for row in csv.DictReader(fh)]
    res = scan(path, pruned)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
    print("parts", len(res["parts"]), "externalLinks", res["external_link_parts"], "externalReference",
          res["external_reference_elements"], "names", res["defined_names_total"], res["defined_names_by_category"],
          "used-in-parts", len(res["names_used_in_parts"]), "prunable&unused", res["names_prunable_and_unused"],
          "pruned-referenced", res.get("pruned_names_referenced"))


if __name__ == "__main__":
    main()
