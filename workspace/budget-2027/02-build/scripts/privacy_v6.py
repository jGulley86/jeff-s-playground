"""v6 privacy check: no employee name in the notes md, the Collation Notes (JSON and the sheet in the workbook), the CSV,
or any other text file given.

Usage:
  python3 -I privacy_v6.py NAMES_JSON FILE [FILE ...]

NAMES_JSON is the scratch file written by recon_v6.py (WORK dir only; it is never copied to the output folder):
{"tokens": [...lower-case name tokens...], "full": [...full names...]}.
A hit is: a full name (case-insensitive), or a name token of 2+ letters written as a name (capitalised or upper case,
whole word, case-sensitive). Lower-case ordinary words (e.g. 'price', 'will') are not names. .xlsx files are checked
on their Collation Notes sheet only (the HC tabs carry the user's names by design).
Exit 1 on any hit; only file, line and token length are printed, never the name.
"""
import sys, json, re, zipfile

N = json.load(open(sys.argv[1]))
pats = [re.compile(re.escape(f), re.I) for f in N["full"]]
for t in N["tokens"]:
    if len(t) >= 2:
        pats.append(re.compile(r"(?<![A-Za-z])(" + re.escape(t.capitalize()) + "|" + re.escape(t.upper()) + r")(?![A-Za-z])"))
hits = 0
for f in sys.argv[2:]:
    if f.endswith(".xlsx"):
        z = zipfile.ZipFile(f)
        wb = z.read("xl/workbook.xml").decode(); rels = z.read("xl/_rels/workbook.xml.rels").decode()
        rid = re.search(r'<sheet name="Collation Notes"[^>]*r:id="(rId\d+)"', wb).group(1)
        part = "xl/" + re.search(rf'<Relationship Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)
        text = z.read(part).decode()
    else:
        text = open(f, encoding="utf-8").read()
    for p in pats:
        for m in p.finditer(text):
            hits += 1
            print(f"HIT {f} line {text[:m.start()].count(chr(10)) + 1} (length {len(m.group(0))})")
print(f"privacy_v6: {len(N['full'])} full names, {len(N['tokens'])} tokens checked in {len(sys.argv) - 2} files; hits {hits}")
sys.exit(1 if hits else 0)
