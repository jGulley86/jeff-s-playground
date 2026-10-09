#!/bin/bash
# Usage: run_build_v2.sh COO_BOOK SD_BOOK V1_XLSX WORK_DIR OUT_DIR
# v2 build (run_build.sh still reproduces v1). Two passes, as in v1:
#   pass 1: build (+frozen-cell comments) -> prune names -> recalc -> analyze/analyze_v2/pkgscan/diff vs v1 -> report
#   pass 2: same with the Collation Notes sheet from pass 1 -> notes must be identical -> copy outputs to OUT_DIR
# Stops (set -e) if v1 vs v2 differ on any budget/driver cell formula or value (diff_versions.py exits 1).
set -euo pipefail
COO="$1"; SD="$2"; V1="$3"; WORK="$4"; OUT="$5"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v2.xlsx
mkdir -p "$WORK/p1" "$WORK/p2" "$WORK/rc1" "$WORK/rc2" "$OUT"
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"
python3 -I "$HERE/pkgscan.py" "$COO" "$WORK/pkg_coo.json"
python3 -I "$HERE/pkgscan.py" "$SD" "$WORK/pkg_sd.json"

pass () {   # $1 = pass number, $2 = optional notes json
  local n="$1"; local notes="${2:-}"
  python3 -I "$HERE/build.py" "$COO" "$SD" "$WORK/p$n/built.xlsx" "$WORK/extrefs.json" $notes --mark-frozen-zeros
  python3 -I "$HERE/prune_names.py" "$WORK/p$n/built.xlsx" "$WORK/p$n/$NAME" "$WORK/pruned$n.csv" "$WORK/prune$n.json"
  "$HERE/recalc.sh" "$WORK/p$n/$NAME" "$WORK/rc$n" "$WORK/loprofile"
  python3 -I "$HERE/analyze.py" "$COO" "$SD" "$WORK/rc$n/$NAME" "$WORK/extrefs.json" "$WORK/res$n.json"
  python3 -I "$HERE/analyze_v2.py" "$COO" "$SD" "$WORK/rc$n/$NAME" "$WORK/extrefs.json" "$WORK/v2res$n.json"
  python3 -I "$HERE/pkgscan.py" "$WORK/rc$n/$NAME" "$WORK/pkg$n.json" "$WORK/pruned$n.csv"
  python3 -I "$HERE/diff_versions.py" "$V1" "$WORK/rc$n/$NAME" "$WORK/diff$n.json"
  python3 -I "$HERE/report.py" "$COO" "$SD" "$WORK/res$n.json" "$WORK/v2res$n.json" "$WORK/pkg$n.json" \
    "$WORK/pkg_coo.json" "$WORK/pkg_sd.json" "$WORK/prune$n.json" "$WORK/extrefs.json" "$WORK/diff$n.json" \
    "$WORK/lo_version.txt" "$WORK/notes$n.json" "$WORK/notes$n.md" "$NAME"
}
pass 1
pass 2 "$WORK/notes1.json"
cmp "$WORK/pruned1.csv" "$WORK/pruned2.csv" || { echo "pruned-name list NOT stable"; exit 1; }
echo "pruned-name list stable between passes"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "notes NOT stable between passes"; exit 1; }
echo "notes stable between passes"
cp "$WORK/rc2/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/02-build_notes_v2.md"
cp "$WORK/pruned2.csv" "$OUT/02-build_pruned_names_v2.csv"
echo "done: $OUT/$NAME"
