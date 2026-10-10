#!/bin/bash
# Usage: run_build_v11.sh V10_XLSX V10_NOTES_MD WORK_DIR OUT_DIR
# v11 build (handoff 2026-10-10): corrections pass on v10 - six documentation fixes, no value changes. The only parts
# that differ from v10 are the Collation Notes sheet (regenerated; F1 fixed, H78:H81 live formulas, reader notes,
# precision wording) and PO!AI33:AI35 (note texts). WORK_DIR must be outside the repo (it receives the scratch name
# list and the LibreOffice profile). No name file: v11 edits no roster cell; names for the privacy scan are read from
# the workbook itself (names_v11.py) into WORK_DIR and deleted at the end.
#
# The whole pipeline runs TWICE (pass1, pass2) and both xlsx and md outputs must be byte-identical (no script reads
# file properties, a clock or a date, so the build is not date-dependent - F1 root cause). Each pass:
#   1. cnotes_v6 extract of the v10 Collation Notes (round trip byte-identical)
#   2. report_v11 pass A (H78:H81 cached 0.0) -> build_v11 stage -> recalc.sh (full LibreOffice recalculation)
#   3. hvals_v11: H78:H81 cached values from the recalculation; stops if any other cell moves > 1e-6 or any error cell
#   4. report_v11 pass B (real H values) -> build_v11 final = the v11 workbook
#   5. diff_versions v10 -> v11, recalc of the final file, recon_v11 + names_v11 + privacy_v6 + paylist_v10,
#      analyze_v11 (exit 1 on any failed criterion)
#   6. report_v11 pass C (check numbers into the md; Collation Notes JSON must equal pass B), then privacy / paylist /
#      analyze again on the final md (analyze JSONs must be identical)
# run_build_v10.sh ... run_build.sh still reproduce v10 ... v1.
set -euo pipefail
V10="$1"; V10MD="$2"; WORK="$3"; OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v11.xlsx
MD=02-build_notes_v11.md
case "$WORK" in /*) ;; *) echo "WORK_DIR must be absolute (LibreOffice profile path)"; exit 1;; esac
REPO="$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$REPO" ]; then
  case "$(realpath -m "$WORK")" in "$REPO"/*) echo "$WORK must be outside the repo"; exit 1;; esac
fi
for f in "$OUT/$NAME" "$OUT/$MD"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
mkdir -p "$WORK" "$OUT"
cleanup () { rm -f "$WORK"/*.names; }
trap cleanup EXIT
recalc () {   # recalc.sh exits 0 even if LibreOffice wrote nothing; check the output and retry once
  rm -f "$2/$(basename "$1")"
  "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"
  [ -s "$2/$(basename "$1")" ] || { echo "recalc: no output, retrying once"; sleep 5; "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"; }
  [ -s "$2/$(basename "$1")" ] || { echo "recalc failed for $1"; exit 1; }
}
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"

build_pass () {   # $1 = pass dir
  local P="$1"
  mkdir -p "$P/s1" "$P/lo1" "$P/p" "$P/lo2"
  python3 -I "$HERE/cnotes_v6.py" "$V10" "$P/cn10.json"
  python3 -I "$HERE/report_v11.py" "$V10MD" "$P/cn10.json" "$V10" "$WORK/lo_version.txt" - "$P/notesA.json" "$P/mdA.md"
  python3 -I "$HERE/build_v11.py" "$V10" "$P/notesA.json" "$P/s1/stage1.xlsx" "$P/specA.json"
  recalc "$P/s1/stage1.xlsx" "$P/lo1"
  python3 -I "$HERE/hvals_v11.py" "$P/s1/stage1.xlsx" "$P/lo1/stage1.xlsx" "$P/hvals.json"
  python3 -I "$HERE/report_v11.py" "$V10MD" "$P/cn10.json" "$V10" "$WORK/lo_version.txt" "$P/hvals.json" "$P/notesB.json" "$P/mdB.md"
  python3 -I "$HERE/build_v11.py" "$V10" "$P/notesB.json" "$P/p/$NAME" "$P/specB.json"
  python3 -I "$HERE/diff_versions.py" "$V10" "$P/p/$NAME" "$P/diff.json" \
    || echo "diff_versions: differences found (expected in v11: the 3 PO note cells; classified by analyze_v11)"
  recalc "$P/p/$NAME" "$P/lo2"
  python3 -I "$HERE/recon_v11.py" "$P/p/$NAME" "$P/recon.json"
  python3 -I "$HERE/names_v11.py" "$P/p/$NAME" "$WORK/v11.names"
  python3 -I "$HERE/privacy_v6.py" "$WORK/v11.names" "$P/mdB.md" "$P/notesB.json" "$P/p/$NAME" > "$P/privacy1.txt" || true
  cat "$P/privacy1.txt"
  python3 -I "$HERE/paylist_v10.py" "$P/p/$NAME" "$P/recon.json" "$P/mdB.md" > "$P/paylist1.txt" || true
  cat "$P/paylist1.txt"
  python3 -I "$HERE/analyze_v11.py" "$V10" "$P/p/$NAME" "$P/lo2/$NAME" "$P/diff.json" "$P/notesB.json" "$P/mdB.md" \
    "$P/privacy1.txt" "$P/paylist1.txt" "$P/analyze.json"
  python3 -I "$HERE/report_v11.py" "$V10MD" "$P/cn10.json" "$V10" "$WORK/lo_version.txt" "$P/hvals.json" "$P/notesC.json" "$P/$MD" "$P/analyze.json"
  cmp "$P/notesB.json" "$P/notesC.json" || { echo "Collation Notes JSON not stable between passes"; exit 1; }
  echo "Collation Notes JSON stable between report passes"
  python3 -I "$HERE/privacy_v6.py" "$WORK/v11.names" "$P/$MD" "$P/notesC.json" "$P/p/$NAME" > "$P/privacy2.txt" || true
  cat "$P/privacy2.txt"
  python3 -I "$HERE/paylist_v10.py" "$P/p/$NAME" "$P/recon.json" "$P/$MD" > "$P/paylist2.txt" || true
  cat "$P/paylist2.txt"
  python3 -I "$HERE/analyze_v11.py" "$V10" "$P/p/$NAME" "$P/lo2/$NAME" "$P/diff.json" "$P/notesC.json" "$P/$MD" \
    "$P/privacy2.txt" "$P/paylist2.txt" "$P/analyze2.json"
  cmp "$P/analyze.json" "$P/analyze2.json" || { echo "analyze JSON not stable between md passes"; exit 1; }
}

echo "=== pass 1 ==="
build_pass "$WORK/p1"
echo "=== pass 2 (must be byte-identical) ==="
build_pass "$WORK/p2"
cmp "$WORK/p1/p/$NAME" "$WORK/p2/p/$NAME" || { echo "two-pass xlsx not byte-identical"; exit 1; }
cmp "$WORK/p1/$MD" "$WORK/p2/$MD" || { echo "two-pass md not byte-identical"; exit 1; }
echo "two-pass build byte-identical (xlsx and md)"
cp "$WORK/p1/p/$NAME" "$OUT/$NAME"
cp "$WORK/p1/$MD" "$OUT/$MD"
cleanup
ls "$WORK"/*.names >/dev/null 2>&1 && { echo "scratch name list still present"; exit 1; }
echo "done: $OUT/$NAME and $OUT/$MD (no CSV); scratch name list deleted"
