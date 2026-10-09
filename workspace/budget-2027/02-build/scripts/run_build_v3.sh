#!/bin/bash
# Usage: run_build_v3.sh COO_BOOK SD_BOOK NEW_DEPLOYSUM V2_XLSX V2_NOTES_MD WORK_DIR OUT_DIR
# v3 build (run_build_v2.sh still reproduces v2; run_build.sh reproduces v1). Starts from the delivered v2 workbook.
#   pass 1: build_v3 (no Collation Notes) -> recalc -> analyze_v3 -> report_v3 (notes json + md)
#   pass 2: build_v3 with the pass-1 Collation Notes -> recalc -> analyze_v3 -> report_v3 -> notes must be identical
# Stops (set -e) if analyze_v3.py finds a failed completion criterion (exit 1).
set -euo pipefail
COO="$1"; SD="$2"; NEW="$3"; V2="$4"; V2MD="$5"; WORK="$6"; OUT="$7"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v3.xlsx
mkdir -p "$WORK/p1" "$WORK/p2" "$WORK/rc1" "$WORK/rc2" "$OUT"
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"

pass () {   # $1 = pass number, $2 = optional notes json
  local n="$1"; local notes="${2:-}"
  python3 -I "$HERE/build_v3.py" "$V2" "$NEW" "$WORK/p$n/$NAME" "$WORK/ext$n.json" $notes
  "$HERE/recalc.sh" "$WORK/p$n/$NAME" "$WORK/rc$n" "$WORK/loprofile"
  python3 -I "$HERE/analyze_v3.py" "$V2" "$WORK/rc$n/$NAME" "$NEW" "$WORK/ext$n.json" "$WORK/res$n.json"
  python3 -I "$HERE/report_v3.py" "$V2MD" "$WORK/res$n.json" "$WORK/ext$n.json" "$WORK/lo_version.txt" \
    "$COO" "$SD" "$NEW" "$WORK/notes$n.json" "$WORK/notes$n.md" "$NAME"
}
pass 1
pass 2 "$WORK/notes1.json"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "notes NOT stable between passes"; exit 1; }
echo "notes stable between passes"
for f in "$OUT/$NAME" "$OUT/02-build_notes_v3.md"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
cp "$WORK/rc2/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/02-build_notes_v3.md"
echo "done: $OUT/$NAME"
