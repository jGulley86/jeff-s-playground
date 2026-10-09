#!/bin/bash
# Usage: run_build_v5.sh COO_BOOK SD_BOOK NEW_DEPLOYSUM V3_XLSX V3_NOTES_MD V4_XLSX WORK_DIR OUT_DIR
# v5 build: v4 + one user-confirmed input (Fld Eng Budget!B21 = 205000, Head of Service Delivery annual salary) +
# critic v4 N1-N3 in the notes. run_build_v4.sh ... run_build.sh still reproduce v4 ... v1 (untouched).
#   1. build_v5 stage 1: v4 package with only B21 set (no cached value changed)
#   2. recalc.sh: LibreOffice full recalculation of stage 1
#   3. deps_v5: static trace of every formula downstream of B21 (on v4)
#   4. patches_v5: recalculated values of downstream cells that changed; stops if anything else moved > 1e-6
#   5. build_v5 stage 2: v4 package + B21 + those cached values (Collation Notes still v4)
#   6. figures_v5 on v4 and on stage 2 -> report_v5 pass 1 -> Collation Notes JSON + draft md
#   7. build_v5 final: stage-2 content + regenerated Collation Notes
#   8. checks: diff_versions v4 -> v5 (exit 1 expected: values differ), figures_v5 on final, recalc of final,
#      analyze_v5 (exit 1 on any failed criterion), report_v5 pass 2 (JSON must equal pass 1), stale_v5 on final md
set -euo pipefail
COO="$1"; SD="$2"; NEW="$3"; V3="$4"; V3MD="$5"; V4="$6"; WORK="$7"; OUT="$8"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v5.xlsx
MD=02-build_notes_v5.md
SHEET="Fld Eng Budget"; CELL=B21; VALUE=205000
case "$WORK" in /*) ;; *) echo "WORK_DIR must be absolute (LibreOffice profile path)"; exit 1;; esac
for f in "$OUT/$NAME" "$OUT/$MD"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
mkdir -p "$WORK/s1" "$WORK/lo1" "$WORK/s2" "$WORK/p" "$WORK/lo2" "$OUT"
recalc () {   # recalc.sh exits 0 even if LibreOffice wrote nothing; check the output and retry once
  "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"
  [ -s "$2/$(basename "$1")" ] || { echo "recalc: no output, retrying once"; sleep 5; "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"; }
  [ -s "$2/$(basename "$1")" ] || { echo "recalc failed for $1"; exit 1; }
}
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"
printf '{"input": ["%s", "%s", %s], "values": []}\n' "$SHEET" "$CELL" "$VALUE" > "$WORK/patch0.json"
python3 -I "$HERE/build_v5.py" "$V4" "$WORK/patch0.json" "$WORK/s1/stage1.xlsx"
recalc "$WORK/s1/stage1.xlsx" "$WORK/lo1"
python3 -I "$HERE/deps_v5.py" "$V4" "$WORK/deps.json" "$SHEET!$CELL"
python3 -I "$HERE/patches_v5.py" "$V4" "$WORK/lo1/stage1.xlsx" "$WORK/deps.json" "$SHEET" "$CELL" "$VALUE" "$WORK/patch.json" "$WORK/noise.json"
python3 -I "$HERE/build_v5.py" "$V4" "$WORK/patch.json" "$WORK/s2/stage2.xlsx"
python3 -I "$HERE/figures_v5.py" "$V4" "$COO" "$SD" "$WORK/fig_v4.json"
python3 -I "$HERE/figures_v5.py" "$WORK/s2/stage2.xlsx" "$COO" "$SD" "$WORK/fig_s2.json"
python3 -I "$HERE/report_v5.py" "$V3MD" "$V3" "$V4" "$WORK/s2/stage2.xlsx" "$WORK/fig_s2.json" "$WORK/fig_v4.json" "$WORK/patch.json" \
  "$WORK/lo_version.txt" "$COO" "$SD" "$NEW" "$WORK/notes1.json" "$WORK/notes1.md"
python3 -I "$HERE/build_v5.py" "$V4" "$WORK/patch.json" "$WORK/p/$NAME" "$WORK/notes1.json"
python3 -I "$HERE/diff_versions.py" "$V4" "$WORK/p/$NAME" "$WORK/diff.json" || echo "diff_versions: differences found (expected in v5; classified by analyze_v5)"
python3 -I "$HERE/figures_v5.py" "$WORK/p/$NAME" "$COO" "$SD" "$WORK/fig_v5.json"
recalc "$WORK/p/$NAME" "$WORK/lo2"
python3 -I "$HERE/analyze_v5.py" "$V4" "$WORK/p/$NAME" "$WORK/lo2/$NAME" "$WORK/diff.json" "$WORK/deps.json" "$WORK/noise.json" \
  "$WORK/patch.json" "$WORK/fig_s2.json" "$WORK/fig_v5.json" "$WORK/notes1.json" "$WORK/notes1.md" "$WORK/fig_v4.json" "$WORK/analyze.json"
python3 -I "$HERE/report_v5.py" "$V3MD" "$V3" "$V4" "$WORK/p/$NAME" "$WORK/fig_v5.json" "$WORK/fig_v4.json" "$WORK/patch.json" \
  "$WORK/lo_version.txt" "$COO" "$SD" "$NEW" "$WORK/notes2.json" "$WORK/notes2.md" "$WORK/analyze.json"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "Collation Notes JSON not stable between passes"; exit 1; }
echo "Collation Notes JSON stable between passes"
python3 -I "$HERE/stale_v5.py" "$WORK/notes2.md" "$WORK/notes2.json" "$V4" "$WORK/patch.json" "$WORK/fig_v4.json" "$WORK/fig_v5.json" "$WORK/p/$NAME"
cp "$WORK/p/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/$MD"
echo "done: $OUT/$NAME and $OUT/$MD"
