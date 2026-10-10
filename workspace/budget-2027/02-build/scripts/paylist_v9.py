"""v9 privacy helper (= paylist_v8 with the v9 diff section added to the no-people list). v8 docstring follows.

v8 privacy helper: paylist_v7 with the v8 numeric-only md sections added to the 'no people' list, plus an honest count of
per-person amounts that rounding cannot hide.

paylist_v7 rounds every per-person amount for an identified employee to the nearest $5k. An amount that is already a
multiple of $5k (e.g. a unique role's annual salary of 160,000) is unchanged by rounding, so it still appears at its exact
value. v7's notes implied that no exact per-person amount remained; the v7 verifier showed that is not true. v8 states it.

Usage as a check:
  python3 -I paylist_v9.py XLSX RECON_JSON FILE [FILE ...]
Prints the paylist_v7 line (exit 1 if any exact amount that rounding should have changed is left) and a 'disclosed' line:
the number of distinct per-person amounts that are $5k multiples and appear in a people section of FILE (values not
printed).
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paylist_v7

# md sections with workbook / model figures only (fleet depreciation, production labour by build month, diff and package)
paylist_v7.NO_PEOPLE = paylist_v7.NO_PEOPLE + ("## Production labour: capitalised", "## v8 -> v9 diff", "## Error scan", "## Package")
amounts, round_text, find, patterns = paylist_v7.amounts, paylist_v7.round_text, paylist_v7.find, paylist_v7.patterns


def disclosed(text, am, md=True):
    """Distinct per-person amounts that are multiples of $5k (rounding leaves them exact) found in people sections."""
    vals = sorted({round(abs(a["v"])) for a in am if round(abs(a["v"])) % 5000 == 0 and abs(abs(a["v"]) - round(abs(a["v"]))) < 0.005})
    found = set()
    for people, chunk in (paylist_v7._blocks(text) if md else [(True, text)]):
        if not people:
            continue
        for v in vals:
            if re.search(r"(?<![\d,.~])" + re.escape(f"{v:,.0f}") + r"(?![\d]|[.,]\d)", chunk):
                found.add(v)
    return len(found), len(vals)


if __name__ == "__main__":
    am = amounts(sys.argv[1], sys.argv[2])
    tot = sk = 0; disc = 0; nv = 0
    for f in sys.argv[3:]:
        text = open(f, encoding="utf-8").read()
        hits, skipped = find(text, am, md=f.endswith(".md"))
        sk += skipped
        d, nv = disclosed(text, am, md=f.endswith(".md")); disc += d
        for line, ln in hits:
            tot += 1
            print(f"EXACT {f} line {line} (length {ln})")
    print(f"paylist_v9: {len(am)} per-person amounts ({len(patterns(am))} forms) checked in {len(sys.argv) - 3} files; "
          f"exact hits {tot}; coincidental equal numbers in non-people md sections (not changed) {sk}; "
          f"$5k-multiple per-person amounts that rounding leaves exact and that appear: {disc} (of {nv} such amounts)")
    sys.exit(1 if tot else 0)
