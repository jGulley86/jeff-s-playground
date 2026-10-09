#!/bin/bash
# Usage: run_build_v4.sh COO_BOOK SD_BOOK NEW_DEPLOYSUM V3_XLSX V3_NOTES_MD WORK_DIR OUT_DIR
# v4 build: notes-and-presentation fix of v3 (critic v3 B1 + O1-O8). Budget values do not change.
# run_build_v3.sh / run_build_v2.sh / run_build.sh still reproduce v3 / v2 / v1 (untouched).
#   1. figures_v4 on v3 (all new numbers, from the v3 workbook + inputs)
#   2. report_v4 pass 1 -> Collation Notes JSON (+ draft md)
#   3. build_v4: copy the v3 package, rewrite only the Collation Notes sheet part
#   4. diff_versions v3 -> v4 (exact; exit 1 on any diff), figures_v4 on v4, LibreOffice recalc of v4 (check only)
#   5. analyze_v4 (exit 1 on any failed criterion) -> report_v4 pass 2 (final md); notes JSON must be identical
set -euo pipefail
COO="$1"; SD="$2"; NEW="$3"; V3="$4"; V3MD="$5"; WORK="$6"; OUT="$7"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v4.xlsx
MD=02-build_notes_v4.md
case "$WORK" in /*) ;; *) echo "WORK_DIR must be absolute (LibreOffice profile path)"; exit 1;; esac
for f in "$OUT/$NAME" "$OUT/$MD"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
mkdir -p "$WORK/p" "$WORK/lo" "$OUT"
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"
python3 -I "$HERE/figures_v4.py" "$V3" "$COO" "$SD" "$WORK/fig_v3.json"
python3 -I "$HERE/report_v4.py" "$V3MD" "$V3" "$WORK/fig_v3.json" "$WORK/lo_version.txt" "$COO" "$SD" "$NEW" \
  "$WORK/notes1.json" "$WORK/notes1.md"
python3 -I "$HERE/build_v4.py" "$V3" "$WORK/notes1.json" "$WORK/p/$NAME"
python3 -I "$HERE/diff_versions.py" "$V3" "$WORK/p/$NAME" "$WORK/diff.json"
python3 -I "$HERE/figures_v4.py" "$WORK/p/$NAME" "$COO" "$SD" "$WORK/fig_v4.json"
"$HERE/recalc.sh" "$WORK/p/$NAME" "$WORK/lo" "$WORK/loprofile"
python3 -I "$HERE/analyze_v4.py" "$V3" "$WORK/p/$NAME" "$WORK/lo/$NAME" "$WORK/diff.json" "$WORK/fig_v3.json" \
  "$WORK/fig_v4.json" "$WORK/notes1.json" "$WORK/analyze.json"
python3 -I "$HERE/report_v4.py" "$V3MD" "$V3" "$WORK/fig_v3.json" "$WORK/lo_version.txt" "$COO" "$SD" "$NEW" \
  "$WORK/notes2.json" "$WORK/notes2.md" "$WORK/analyze.json"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "Collation Notes JSON not stable between passes"; exit 1; }
echo "Collation Notes JSON stable between passes"
cp "$WORK/p/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/$MD"
echo "done: $OUT/$NAME and $OUT/$MD"
