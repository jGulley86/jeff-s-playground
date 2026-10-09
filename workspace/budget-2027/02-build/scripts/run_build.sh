#!/bin/bash
# Usage: run_build.sh COO_BOOK SD_BOOK WORK_DIR OUT_DIR
# Two-pass build: pass 1 (no notes) -> recalc -> analyze -> report
#                 pass 2 (with Collation Notes) -> recalc -> analyze -> report -> copy to OUT_DIR
set -euo pipefail
COO="$1"; SD="$2"; WORK="$3"; OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v1.xlsx
mkdir -p "$WORK/p1" "$WORK/p2" "$WORK/rc1" "$WORK/rc2" "$OUT"
python3 -I "$HERE/build.py" "$COO" "$SD" "$WORK/p1/$NAME" "$WORK/extrefs.json"
"$HERE/recalc.sh" "$WORK/p1/$NAME" "$WORK/rc1" "$WORK/loprofile"
python3 -I "$HERE/analyze.py" "$COO" "$SD" "$WORK/rc1/$NAME" "$WORK/extrefs.json" "$WORK/res1.json"
python3 -I "$HERE/report.py" "$COO" "$SD" "$WORK/res1.json" "$WORK/extrefs.json" "$WORK/notes1.json" "$WORK/notes1.md" "$NAME"
python3 -I "$HERE/build.py" "$COO" "$SD" "$WORK/p2/$NAME" "$WORK/extrefs.json" "$WORK/notes1.json"
"$HERE/recalc.sh" "$WORK/p2/$NAME" "$WORK/rc2" "$WORK/loprofile"
python3 -I "$HERE/analyze.py" "$COO" "$SD" "$WORK/rc2/$NAME" "$WORK/extrefs.json" "$WORK/res2.json"
python3 -I "$HERE/report.py" "$COO" "$SD" "$WORK/res2.json" "$WORK/extrefs.json" "$WORK/notes2.json" "$WORK/notes2.md" "$NAME"
cmp "$WORK/notes1.json" "$WORK/notes2.json" && echo "notes stable between passes"
cp "$WORK/rc2/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/02-build_notes_v1.md"
echo "done: $OUT/$NAME"
