"""v10 per-person amount check (= paylist_v9 with the v10 numeric-only md sections added to the no-people list).

Usage:
  python3 -I paylist_v10.py V10_XLSX RECON_LITE_JSON FILE [FILE ...]
RECON_LITE_JSON (figures_v10.py): the Logistics&WH seats, with LOG-01 and MH-01 flagged as held by people on an HC roster.
Exit 1 if any FILE still holds an exact per-person amount (file, line and length printed, never the amount).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paylist_v7, paylist_v9

paylist_v7.NO_PEOPLE = paylist_v7.NO_PEOPLE + ("## v9 -> v10 diff", "## Error scan", "## Completion criteria", "## Build and sources")
if __name__ == "__main__":
    am = paylist_v7.amounts(sys.argv[1], sys.argv[2])
    tot = sk = disc = nv = 0
    for f in sys.argv[3:]:
        text = open(f, encoding="utf-8").read()
        hits, skipped = paylist_v7.find(text, am, md=f.endswith(".md"))
        sk += skipped
        d, nv = paylist_v9.disclosed(text, am, md=f.endswith(".md")); disc += d
        for line, ln in hits:
            tot += 1
            print(f"EXACT {f} line {line} (length {ln})")
    print(f"paylist_v10: {len(am)} per-person amounts ({len(paylist_v7.patterns(am))} forms) checked in {len(sys.argv) - 3} files; "
          f"exact hits {tot}; coincidental equal numbers in non-people md sections (not changed) {sk}; "
          f"$5k-multiple per-person amounts that rounding leaves exact and that appear: {disc} (of {nv} such amounts)")
    sys.exit(1 if tot else 0)
