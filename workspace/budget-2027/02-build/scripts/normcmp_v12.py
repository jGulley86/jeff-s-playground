"""v12 reproducibility comparison of two engine saves.

LibreOffice's xlsx export emits the children of <dataValidations> in nondeterministic order
(hash-map iteration; everything else observed deterministic). Two saves of the same document are
therefore byte-identical per part EXCEPT possibly that ordering. This tool compares two xlsx files:
  - same part names in the same order;
  - every part's bytes identical, after sorting <dataValidation ...>...</dataValidation> blocks
    inside <dataValidations> (worksheet parts only);
  - reports which parts were raw-identical vs identical-only-after-normalization (the set may vary
    run to run; only the boolean verdict is stable and only it belongs in the notes).

Usage:
  python3 -I normcmp_v12.py A_XLSX B_XLSX OUT_JSON
Exit 1 unless content-identical under the rule above.
"""
import sys, json, re, zipfile

A, B, OUT = sys.argv[1:4]
DV = re.compile(r"(<dataValidations[^>]*>)(.*?)(</dataValidations>)", re.S)
DVITEM = re.compile(r"<dataValidation .*?</dataValidation>|<dataValidation [^>]*/>", re.S)


def norm(name, data):
    if not name.startswith("xl/worksheets/sheet"):
        return data
    x = data.decode("utf-8")

    def fix(m):
        items = DVITEM.findall(m.group(2))
        rest = DVITEM.sub("", m.group(2))
        assert rest.strip() == "", f"unexpected content in dataValidations of {name}: {rest[:80]!r}"
        return m.group(1) + "".join(sorted(items)) + m.group(3)

    return DV.sub(fix, x).encode("utf-8")


za, zb = zipfile.ZipFile(A), zipfile.ZipFile(B)
na, nb = za.namelist(), zb.namelist()
rep = {"same_part_list": na == nb, "parts": len(na), "raw_identical": [], "normalized_identical": [],
       "different": []}
if na == nb:
    for n in na:
        da, db = za.read(n), zb.read(n)
        if da == db:
            rep["raw_identical"].append(n)
        elif norm(n, da) == norm(n, db):
            rep["normalized_identical"].append(n)
        else:
            rep["different"].append(n)
ok = rep["same_part_list"] and not rep["different"]
rep["ok"] = ok
json.dump(rep, open(OUT, "w"), indent=1)
print(f"normcmp_v12: parts {rep['parts']}, raw-identical {len(rep['raw_identical'])}, "
      f"identical after dataValidation-order normalization {len(rep['normalized_identical'])} "
      f"({rep['normalized_identical'] or '-'}), DIFFERENT {rep['different'] or 'none'} -> "
      f"{'OK' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
