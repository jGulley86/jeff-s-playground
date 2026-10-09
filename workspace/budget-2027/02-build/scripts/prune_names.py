"""Prune unused legacy defined names whose target is external-looking or #REF! (v2, logged step).

Usage:
  python3 -I prune_names.py IN_XLSX OUT_XLSX PRUNED_CSV LOG_JSON

Rule (v2 handoff, B2): a defined name is removed only if BOTH
  (a) its target text contains '[' or '.xls' (any case) or '#REF!', and
  (b) it is not referenced anywhere: cell formulas, data validations, conditional formats, charts,
      or the definition of any name that is kept (checked to a fixed point).
Built-in names (_xlnm.*: print areas, print titles, filter ranges) are never removed.
Only xl/workbook.xml is rewritten; every other package part is copied byte for byte.
"""
import sys, os, csv, json, zipfile, importlib.util
sys.dont_write_bytecode = True   # do not leave __pycache__ next to the scripts
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pkgscan", os.path.join(HERE, "pkgscan.py"))
pk = importlib.util.module_from_spec(spec); spec.loader.exec_module(pk)

IN, OUT, CSV_OUT, LOG = sys.argv[1:5]


def main():
    zin = zipfile.ZipFile(IN)
    names, _ = pk.read_names(zin)
    used_parts, by_name_refs, counts = pk.usage(zin, names)

    def candidate(d):
        return pk.is_external_or_ref(d["text"]) and not d["name"].startswith("_xlnm.")

    cands = {d["name"].upper() for d in names if candidate(d)}
    used = set(used_parts)
    # fixed point: names referenced by any kept name are used
    while True:
        kept = {d["name"].upper() for d in names} - (cands - used)
        add = set().union(*(by_name_refs[k] for k in kept)) - used
        if not add:
            break
        used |= add
    prune = cands - used
    rows = [d for d in names if d["name"].upper() in prune]

    root = etree.fromstring(zin.read("xl/workbook.xml"))
    dn_parent = root.find("{%s}definedNames" % pk.MAIN)
    removed = 0
    for el in list(dn_parent):
        if (el.get("name") or "").upper() in prune and el.get("localSheetId") is None:
            dn_parent.remove(el); removed += 1
    if len(dn_parent) == 0:
        root.remove(dn_parent)
    wb_xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = wb_xml if info.filename == "xl/workbook.xml" else zin.read(info.filename)
            zout.writestr(info, data)

    with open(CSV_OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "reason", "target_text"])
        for d in rows:
            reason = "#REF!" if "#REF!" in d["text"] else "external-looking ('[' or '.xls')"
            w.writerow([d["name"], reason, d["text"]])
    log = {"names_before": len(names), "candidates": len(cands), "candidates_used": len(cands & used),
           "pruned": removed, "names_after": len(names) - removed,
           "pruned_ref": sum(1 for d in rows if "#REF!" in d["text"]),
           "pruned_external_looking": sum(1 for d in rows if "#REF!" not in d["text"]),
           "formula_elements_scanned": dict(counts),
           "names_used_in_parts": sorted(used_parts),
           "builtin_xlnm_kept": [d["name"] for d in names if d["name"].startswith("_xlnm.")]}
    with open(LOG, "w") as fh:
        json.dump(log, fh, indent=1)
    print("defined names: before", log["names_before"], "pruned", removed, "after", log["names_after"],
          "| candidates", len(cands), "of which used", len(cands & used), "| scanned", dict(counts))


if __name__ == "__main__":
    main()
