"""v14 stale-value sweep of the Collation Notes current-state areas (verifier v13 instruction).

Scans rows 8-71, 357, 375-381 (the handoff scope) plus rows 323 and 336 (builder-extended: the A-31/A-44 register
rows carry the same-vintage figures) for known v12-era-or-older stale values. A value on the list is a finding
UNLESS its occurrence sits inside an allowed historical context (an explicit vN marker) or an allow-listed cell.
Extra whole-sheet scan: the hard-stale strings that must appear nowhere on the sheet at all.

Modes:
  pre   report-only (run on v13): exit 0, findings listed in OUT_JSON["disallowed"].
  gate  run on the v14 deliverable: exit 1 if any disallowed occurrence remains.

Usage:
  python3 -I sweep_v14.py XLSX MODE OUT_JSON
"""
import sys, json, re
import openpyxl

X, MODE, OUT = sys.argv[1:4]
assert MODE in ("pre", "gate")
SCOPE = set(range(8, 72)) | {357} | set(range(375, 382)) | {323, 336}
B = lambda s: r"(?<![\d,.])" + re.escape(s) + r"(?!\d)"   # number boundaries

# (name, pattern, [allowed-context regexes: the occurrence is OK if one of these matches a span containing it])
RULES = [
    ("399,860",   B("399,860"),   [r"v10-v12 -> \(399,860\) on the then-headline"]),
    ("32,228",    B("32,228"),    []),
    ("480,264",   B("480,264"),   []),
    ("98,441",    B("98,441"),    []),
    ("2,289,154", B("2,289,154"), []),
    ("319,393",   B("319,393"),   []),
    ("74,099",    B("74,099"),    []),
    ("54,703",    B("54,703"),    []),
    ("15,525",    B("15,525"),    []),
    ("2,715",     B("2,715"),     []),
    ("43,967",    B("43,967"),    []),
    ("3,100,031", B("3,100,031"), []),
    ("34,169",    B("34,169"),    [r"v7: PO/CO/PE 77,882, FO/FE 34,169"]),
    ("77,882",    B("77,882"),    [r"v7: PO/CO/PE 77,882"]),
    ("21,081",    B("21,081"),    []),
    ("12,834",    B("12,834"),    []),
    ("26,350",    B("26,350"),    []),
    ("62,207",    B("62,207"),    [r"v12:? \(62,207\)"]),
    ("56,801",    B("56,801"),    [r"v9:? \(56,801\)"]),
    ("398,492",   B("398,492"),   [r"v10-v12 \(?398,492\)?", r"398,492 -> 210,023"]),
    ("159,136",   B("159,136"),   [r"v1[02]:? 159,136", r"159,136 \(v12\)", r"159,136(\.40)? -> \(646,75"]),
    ("19,396",    B("19,396"),    [r"v10-v12:? \+?19,396", r"\(v12 \+?19,396"]),
    ("13 hires",  r"13 hires",    []),
    ("ten hires", r"ten hires",   []),
    ("A35-stale", r"'Carried from v9' have inputs v10 does not touch", []),
    ("A35-stale2", r"switch rows are recalculated on v10", []),
]
CELL_ALLOW = {"398,492": {"D357"}}   # D357 narrates the v10 booking history in so many words
# strings that must not appear anywhere on the sheet (full-sheet scan)
HARD = ["13 hires", "ten hires", "10 user-approved", "399,860", "480,264", "2,289,154", "98,441", "32,228",
        "(2,289,154)"]
HARD_ALLOW = [r"v10-v12 -> \(399,860\) on the then-headline"]   # D380 keeps the old endpoint as marked history

wb = openpyxl.load_workbook(X)
ws = wb["Collation Notes"]
disallowed, historical = [], []
for row in ws.iter_rows():
    for c in row:
        if not isinstance(c.value, str):
            continue
        txt = c.value
        if c.row in SCOPE:
            for name, pat, allows in RULES:
                if name in CELL_ALLOW and c.coordinate in CELL_ALLOW[name]:
                    if re.search(pat, txt):
                        historical.append(f"{c.coordinate}:{name} (allow-listed cell)")
                    continue
                for m in re.finditer(pat, txt):
                    spans = [mm.span() for a in allows for mm in re.finditer(a, txt)]
                    if any(s <= m.start() and m.end() <= e for s, e in spans):
                        historical.append(f"{c.coordinate}:{name} (context-marked)")
                    else:
                        disallowed.append(f"{c.coordinate}:{name}")
        for h in HARD:
            for m in re.finditer(B(h) if h[0].isdigit() else re.escape(h), txt):
                spans = [mm.span() for a in HARD_ALLOW for mm in re.finditer(a, txt)]
                if any(s <= m.start() and m.end() <= e for s, e in spans):
                    continue
                tag = f"{c.coordinate}:{h} [whole-sheet]"
                if c.row not in SCOPE and tag not in disallowed:
                    disallowed.append(tag)

disallowed = sorted(set(disallowed), key=lambda s: (re.sub(r"\d+", lambda m: f"{int(m.group()):06d}", s)))
historical = sorted(set(historical), key=lambda s: (re.sub(r"\d+", lambda m: f"{int(m.group()):06d}", s)))
json.dump({"mode": MODE, "scope_rows": "8-71, 357, 375-381 + 323/336 (extended); hard list whole-sheet",
           "disallowed": disallowed, "historical_context_marked": historical}, open(OUT, "w"), indent=1)
print(f"sweep_v14 [{MODE}]: {len(disallowed)} disallowed stale occurrence(s); "
      f"{len(historical)} historical (context-marked, kept)")
for d in disallowed:
    print("  STALE", d)
sys.exit(1 if (MODE == "gate" and disallowed) else 0)
