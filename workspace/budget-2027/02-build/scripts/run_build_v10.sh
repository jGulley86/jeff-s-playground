#!/bin/bash
# Usage: run_build_v10.sh V9_XLSX V9_NOTES_MD SD_BOOK_V2 WORKFILE COO_BOOK DEPLOY_BOOK NAME_FILE WORK_DIR OUT_DIR
# v10 build (brief v6): Logistics & Warehouse payroll booked in Central Operations, the material handler (MH-01 = PO HC r20) moved
# PO -> CO, and the new CO employee (HC-CO r18, 110,000). NAME_FILE holds the new CO employee's name as the user gave it; it must be
# outside the repo (the name goes on HC-CO r18 only). WORK_DIR must be outside the repo too: it receives the scratch name list.
#   1. build_v10 stage1 (edits on v9) -> recalc.sh -> patches_v10 (static trace; values of the edited cells and their downstream set
#      only; stops if anything else moves > 1e-6) -> build_v10 final = stage 2 (no Collation Notes change yet)
#   2. scen_v8 + recalc: base; B131 = 0; B135 = 0; B131 = B135 = 0; B132 = 1; B132 = 1 and B131 = 0; B13 = 1; v9 with B131 = 0
#   3. cnotes_v6 extract of the v9 Collation Notes; figures_v10 on stage 2 -> report_v10 pass 1 -> build_v10 final with Collation Notes
#   4. checks: diff_versions v9 -> v10, recalc of v10 and of v9, figures_v10 on the final file (must equal step 3), names_v10 +
#      privacy_v6, paylist_v10, analyze_v10 (exit 1 on any failed criterion), report_v10 pass 2 (Collation Notes JSON must equal pass 1)
#   5. copy the xlsx and md to OUT_DIR; delete the scratch name list. run_build_v9.sh ... run_build.sh still reproduce v9 ... v1.
set -euo pipefail
V9="$1"; V9MD="$2"; SD="$3"; WF="$4"; COO="$5"; NEW="$6"; NAMEF="$7"; WORK="$8"; OUT="$9"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v10.xlsx
MD=02-build_notes_v10.md
DSN="Depreciation Schedule"
case "$WORK" in /*) ;; *) echo "WORK_DIR must be absolute (LibreOffice profile path)"; exit 1;; esac
REPO="$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$REPO" ]; then
  for p in "$WORK" "$NAMEF"; do
    case "$(realpath -m "$p")" in "$REPO"/*) echo "$p must be outside the repo"; exit 1;; esac
  done
fi
for f in "$OUT/$NAME" "$OUT/$MD"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
mkdir -p "$WORK/s1" "$WORK/lo1" "$WORK/s2" "$WORK/sc10" "$WORK/lo_sc10" "$WORK/p" "$WORK/lo2" "$WORK/lo9" "$OUT"
cleanup () { rm -f "$WORK"/*.names; }
trap cleanup EXIT
recalc () {   # recalc.sh exits 0 even if LibreOffice wrote nothing; check the output and retry once
  rm -f "$2/$(basename "$1")"
  "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"
  [ -s "$2/$(basename "$1")" ] || { echo "recalc: no output, retrying once"; sleep 5; "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"; }
  [ -s "$2/$(basename "$1")" ] || { echo "recalc failed for $1"; exit 1; }
}
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"
# 1
python3 -I "$HERE/build_v10.py" stage1 "$V9" "$SD" "$NAMEF" "$WORK/s1/stage1.xlsx" "$WORK/spec.json"
recalc "$WORK/s1/stage1.xlsx" "$WORK/lo1"
python3 -I "$HERE/patches_v10.py" "$WORK/s1/stage1.xlsx" "$WORK/lo1/stage1.xlsx" "$WORK/spec.json" "$WORK/patch.json" "$WORK/noise.json"
python3 -I "$HERE/build_v10.py" final "$WORK/s1/stage1.xlsx" "$WORK/patch.json" "$WORK/s2/stage2.xlsx"
# 2
cp "$WORK/s2/stage2.xlsx" "$WORK/sc10/base.xlsx"
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc10/cur.xlsx" "$DSN!B131" 0
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc10/idle.xlsx" "$DSN!B135" 0
python3 -I "$HERE/scen_v8.py" "$WORK/sc10/cur.xlsx" "$WORK/sc10/idlecur.xlsx" "$DSN!B135" 0
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc10/q4.xlsx" "$DSN!B132" 1
python3 -I "$HERE/scen_v8.py" "$WORK/sc10/cur.xlsx" "$WORK/sc10/q4cur.xlsx" "$DSN!B132" 1
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc10/b13.xlsx" "$DSN!B13" 1
python3 -I "$HERE/scen_v8.py" "$V9" "$WORK/sc10/v9cur.xlsx" "$DSN!B131" 0
for n in base cur idle idlecur q4 q4cur b13 v9cur; do recalc "$WORK/sc10/$n.xlsx" "$WORK/lo_sc10"; done
# 3
python3 -I "$HERE/cnotes_v6.py" "$V9" "$WORK/cn9.json"
python3 -I "$HERE/figures_v10.py" "$V9" "$WORK/s2/stage2.xlsx" "$SD" "$WORK/cn9.json" "$WORK/lo_sc10" "$WORK/fig10.json"
python3 -I "$HERE/report_v10.py" "$V9MD" "$WORK/cn9.json" "$WORK/s2/stage2.xlsx" "$WORK/fig10.json" "$WORK/fig10_recon.json" "$WORK/spec.json" \
  "$WORK/noise.json" "$WORK/lo_version.txt" "$V9" "$SD" "$WF" "$COO" "$NEW" "$WORK/notes1.json" "$WORK/notes1.md"
python3 -I "$HERE/build_v10.py" final "$WORK/s1/stage1.xlsx" "$WORK/patch.json" "$WORK/p/$NAME" "$WORK/notes1.json"
# 4
python3 -I "$HERE/diff_versions.py" "$V9" "$WORK/p/$NAME" "$WORK/diff.json" || echo "diff_versions: differences found (expected in v10; classified by analyze_v10)"
recalc "$WORK/p/$NAME" "$WORK/lo2"
cp "$V9" "$WORK/lo9/v9src.xlsx"
recalc "$WORK/lo9/v9src.xlsx" "$WORK/lo9/out"
python3 -I "$HERE/figures_v10.py" "$V9" "$WORK/p/$NAME" "$SD" "$WORK/cn9.json" "$WORK/lo_sc10" "$WORK/fig10_final.json"
cmp "$WORK/fig10.json" "$WORK/fig10_final.json" || { echo "figures differ between stage 2 and the final file"; exit 1; }
python3 -I "$HERE/names_v10.py" "$WORK/p/$NAME" "$NAMEF" "$WORK/v10.names"
python3 -I "$HERE/privacy_v6.py" "$WORK/v10.names" "$WORK/notes1.md" "$WORK/notes1.json" "$WORK/p/$NAME" > "$WORK/privacy1.txt" || true
cat "$WORK/privacy1.txt"
python3 -I "$HERE/paylist_v10.py" "$WORK/p/$NAME" "$WORK/fig10_recon.json" "$WORK/notes1.md" > "$WORK/paylist1.txt" || true
cat "$WORK/paylist1.txt"
python3 -I "$HERE/analyze_v10.py" "$V9" "$WORK/p/$NAME" "$WORK/lo2/$NAME" "$WORK/lo9/out/v9src.xlsx" "$WORK/diff.json" "$WORK/spec.json" \
  "$WORK/fig10.json" "$WORK/notes1.md" "$WORK/notes1.json" "$WORK/privacy1.txt" "$WORK/paylist1.txt" "$WORK/analyze.json"
python3 -I "$HERE/report_v10.py" "$V9MD" "$WORK/cn9.json" "$WORK/p/$NAME" "$WORK/fig10.json" "$WORK/fig10_recon.json" "$WORK/spec.json" \
  "$WORK/noise.json" "$WORK/lo_version.txt" "$V9" "$SD" "$WF" "$COO" "$NEW" "$WORK/notes2.json" "$WORK/notes2.md" "$WORK/analyze.json"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "Collation Notes JSON not stable between passes"; exit 1; }
echo "Collation Notes JSON stable between passes"
python3 -I "$HERE/privacy_v6.py" "$WORK/v10.names" "$WORK/notes2.md" "$WORK/notes2.json" "$WORK/p/$NAME"
python3 -I "$HERE/paylist_v10.py" "$WORK/p/$NAME" "$WORK/fig10_recon.json" "$WORK/notes2.md"
# 5
cp "$WORK/p/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/$MD"
cleanup
ls "$WORK"/*.names >/dev/null 2>&1 && { echo "scratch name list still present"; exit 1; }
echo "done: $OUT/$NAME and $OUT/$MD (no CSV); scratch name list deleted"
