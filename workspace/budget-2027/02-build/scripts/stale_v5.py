"""v5 stale-number scan: v4 numbers that changed must not survive in the v5 notes (outside the change log).

Usage (module): from stale_v5 import scan; res = scan(MD_TEXT, CN_TEXT, V4_XLSX, PATCH_JSON, FIG_V4, FIG_V5)

Old numbers = v4 cached value of every recalculated cell + every numeric leaf of figures_v5.py on v4 that differs on
v5, |x| >= 1,000, formatted as the notes format them (1,234 and (1,234)). Numbers that are also a current v5 value
(cell or figure) are skipped, since they may legitimately appear. The md is searched with the sections
'Changes from v4' and 'Head of Service Delivery salary' removed (they quote v4 on purpose); the Collation Notes text
is searched without the 'Changes from v4' and salary sections.
"""
import json, re
import openpyxl


def f0(x):
    return f"({abs(x):,.0f})" if x < 0 else f"{x:,.0f}"


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, f"{p}/{i}")
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        yield p, float(o)


def scan(md, cn_text, v4_xlsx, patch, fig4, fig5, v5_xlsx):
    a = openpyxl.load_workbook(v4_xlsx, data_only=True); b = openpyxl.load_workbook(v5_xlsx, data_only=True)
    old, new = {}, set()
    for s, c, _ in patch["values"]:
        x, y = a[s][c].value, b[s][c].value
        if isinstance(x, (int, float)) and abs(x) >= 1000: old[f0(x)] = f"{s}!{c}"
        if isinstance(y, (int, float)): new.add(f0(y))
    l4, l5 = dict(leaves(fig4)), dict(leaves(fig5))
    for k, x in l4.items():
        if abs(x) >= 1000 and k in l5 and abs(l5[k] - x) > 0.5: old[f0(x)] = "fig" + k
    for k, y in l5.items(): new.add(f0(y))
    # every number in the v5 md that is also a v5 value is legitimate
    old = {k: v for k, v in old.items() if k not in new}
    md_chk = re.sub(r"(?s)## Changes from v4\n.*?\n## ", "## ", md)
    md_chk = re.sub(r"(?s)## Head of Service Delivery salary \(I-26, resolved in v5\)\n.*?\n## ", "## ", md_chk)
    # a v4 number is allowed where the text says it is v4: 'v4' within the 120 characters before it, '(v4)' or
    # ' -> ' right after it, or the 'v4' column of the headline table (column 7 of a row in that table)
    hl = re.search(r"(?s)## Headline: 2027 COO contribution\n(.*?)\n\n- ", md_chk)
    hl_span = hl.span(1) if hl else (0, 0)
    hits, allowed = [], []
    for num, src in sorted(old.items()):
        pat = re.compile(r"(?<![\d,.])" + re.escape(num) + r"(?![\d,]|\.\d)")
        for where, txt in (("md", md_chk), ("cn", cn_text)):
            for m in pat.finditer(txt):
                before, after = txt[max(0, m.start() - 120):m.start()], txt[m.end():m.end() + 6]
                line_start = txt.rfind("\n", 0, m.start()) + 1
                col = txt[line_start:m.start()].count(" | ")
                ok = ("v4" in before or after.startswith(" (v4)") or after.startswith(" -> ")
                      or (where == "md" and hl_span[0] <= m.start() < hl_span[1] and col == 6))
                (allowed if ok else hits).append([where, num, src, txt[max(0, m.start() - 80):m.end() + 40].replace("\n", " ")])
    return {"checked": len(old), "hits": len(hits), "allowed_v4_quotes": len(allowed), "examples": hits[:40]}


if __name__ == "__main__":
    import sys
    MD, NOTES, V4, PATCH, FIG4, FIG5, V5 = sys.argv[1:8]
    notes = json.load(open(NOTES))

    def flat(o):
        if isinstance(o, dict): return " ".join(flat(v) for v in o.values())
        if isinstance(o, list): return " ".join(flat(v) for v in o)
        return str(o)

    secs = [x for x in notes["sections"] if not x["heading"].startswith(("Changes from v4", "Head of Service Delivery salary"))]
    r = scan(open(MD).read(), flat(secs), V4, json.load(open(PATCH)), json.load(open(FIG4)), json.load(open(FIG5)), V5)
    print(f"stale_v5: {r['hits']} stale v4 numbers ({r['checked']} checked, {r['allowed_v4_quotes']} labelled v4 quotes)")
    for h in r["examples"]: print("  ", h)
    sys.exit(1 if r["hits"] else 0)
