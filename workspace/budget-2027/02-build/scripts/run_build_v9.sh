#!/bin/bash
# Usage: run_build_v9.sh COO_BOOK SD_BOOK NEW_DEPLOYSUM WORKFILE V7_XLSX V7_NOTES_MD V8_XLSX WORK_DIR OUT_DIR
# v9 build (critic v8 B1 / B2 / O1-O7, orchestrator rulings): Depreciation Schedule B132 = 0 (Sep-Dec 26 labour a 2026 cost; the
# Sep-26 builds follow the same switch), new idle-month switch B135 (default 1 = roll forward) with section 11, PO 5110-5140
# + idle labour (0 while B135 = 1), labels (run-rate wording removed; CIP). Notes regenerated from v7's text base with the v9
# figures (as report_v8 did). run_build_v8.sh ... run_build.sh still reproduce v8 ... v1 (untouched). WORK_DIR must be outside
# the repo: it receives the scratch name list and per-person data (recon_v6.py); the name lists are deleted at the end.
#   1. build_v9 stage1 (edits on v8) -> recalc.sh -> patches_v9 (static trace; values of the edited cells and their downstream set
#      only) -> build_v9 final = stage 2 (no Collation Notes change yet)
#   2. scen_v8 + recalc: B131 = 0; B132 = 1; B13 = 1; B135 = 0; B131 = B135 = 0; B131 = 0 and B132 = 1
#   3. carried v7 figures: prodpay_v6 + recalc + recon_v6 on v7, scen_v7 on v7, figures_v7; cnotes_v6 on v7
#   4. figures_v9 on stage 2 -> report_v9 pass 1 -> build_v9 final with the Collation Notes
#   5. checks: diff_versions v8 -> v9 (differences expected; classified by analyze_v9), recalc of v9, figures_v9 on the final file
#      (must equal step 4), privacy_v6, paylist_v9, analyze_v9 (exit 1 on any failed criterion), report_v9 pass 2 (JSON must
#      equal pass 1), privacy / paylist again
#   6. copy the xlsx and md to OUT_DIR; delete the scratch name lists (*.names) in WORK_DIR
set -euo pipefail
COO="$1"; SD="$2"; NEW="$3"; WF="$4"; V7="$5"; V7MD="$6"; V8="$7"; WORK="$8"; OUT="$9"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v9.xlsx
MD=02-build_notes_v9.md
DSN="Depreciation Schedule"
case "$WORK" in /*) ;; *) echo "WORK_DIR must be absolute (LibreOffice profile path)"; exit 1;; esac
REPO="$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$REPO" ]; then case "$(cd "$(dirname "$WORK")" && pwd)/$(basename "$WORK")" in "$REPO"/*) echo "WORK_DIR must be outside the repo"; exit 1;; esac; fi
for f in "$OUT/$NAME" "$OUT/$MD"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
mkdir -p "$WORK/s1" "$WORK/lo1" "$WORK/s2" "$WORK/sc9" "$WORK/lo_sc9" "$WORK/pp" "$WORK/lo_pp" "$WORK/sc" "$WORK/lo_base" "$WORK/lo_sc" "$WORK/p" "$WORK/lo2" "$OUT"
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
python3 -I "$HERE/build_v9.py" stage1 "$V8" "$WORK/s1/stage1.xlsx" "$WORK/spec.json"
recalc "$WORK/s1/stage1.xlsx" "$WORK/lo1"
python3 -I "$HERE/patches_v9.py" "$WORK/s1/stage1.xlsx" "$WORK/lo1/stage1.xlsx" "$WORK/spec.json" "$WORK/patch.json" "$WORK/noise.json"
python3 -I "$HERE/build_v9.py" final "$WORK/s1/stage1.xlsx" "$WORK/patch.json" "$WORK/s2/stage2.xlsx"
# 2
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc9/cur.xlsx" "$DSN!B131" 0
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc9/q4.xlsx" "$DSN!B132" 1
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc9/b13.xlsx" "$DSN!B13" 1
python3 -I "$HERE/scen_v8.py" "$WORK/s2/stage2.xlsx" "$WORK/sc9/idle.xlsx" "$DSN!B135" 0
python3 -I "$HERE/scen_v8.py" "$WORK/sc9/cur.xlsx" "$WORK/sc9/idlecur.xlsx" "$DSN!B135" 0
python3 -I "$HERE/scen_v8.py" "$WORK/sc9/cur.xlsx" "$WORK/sc9/q4cur.xlsx" "$DSN!B132" 1
for n in cur q4 b13 idle idlecur q4cur; do recalc "$WORK/sc9/$n.xlsx" "$WORK/lo_sc9"; done
# 3
python3 -I "$HERE/prodpay_v6.py" "$V7" "$WORK/pp/pp_scratch.xlsx"
recalc "$WORK/pp/pp_scratch.xlsx" "$WORK/lo_pp"
python3 -I "$HERE/recon_v6.py" "$WF" "$SD" "$COO" "$V7" "$WORK/lo_pp/pp_scratch.xlsx" "$WORK/recon.json" "$WORK/roster.csv"
python3 -I "$HERE/scen_v7.py" make "$V7" "$WORK/sc/scen.xlsx"
cp "$V7" "$WORK/sc/base.xlsx"
recalc "$WORK/sc/base.xlsx" "$WORK/lo_base"
recalc "$WORK/sc/scen.xlsx" "$WORK/lo_sc"
python3 -I "$HERE/scen_v7.py" compare "$V7" "$WORK/lo_base/base.xlsx" "$WORK/lo_sc/scen.xlsx" "$WORK/scen.json"
python3 -I "$HERE/figures_v7.py" "$V7" "$WORK/lo_pp/pp_scratch.xlsx" "$WORK/recon.json" "$WORK/scen.json" "$WF" "$SD" "$WORK/fig7.json"
python3 -I "$HERE/cnotes_v6.py" "$V7" "$WORK/cn7.json"
# 4
SC="$WORK/lo_sc9/cur.xlsx $WORK/lo_sc9/q4.xlsx $WORK/lo_sc9/b13.xlsx $WORK/lo_sc9/idle.xlsx $WORK/lo_sc9/idlecur.xlsx $WORK/lo_sc9/q4cur.xlsx"
python3 -I "$HERE/figures_v9.py" "$V7" "$V8" "$WORK/s2/stage2.xlsx" "$WORK/lo_pp/pp_scratch.xlsx" "$WORK/spec.json" $SC "$WORK/fig7.json" "$WORK/recon.json" \
  "$WORK/cn7.json" "$WORK/fig9.json"
python3 -I "$HERE/report_v9.py" "$V7MD" "$WORK/cn7.json" "$V7" "$V8" "$WORK/s2/stage2.xlsx" "$WORK/fig9.json" "$WORK/fig7.json" "$WORK/recon.json" "$WORK/spec.json" \
  "$WORK/noise.json" "$WORK/lo_version.txt" "$WF" "$COO" "$SD" "$NEW" "$WORK/notes1.json" "$WORK/notes1.md"
python3 -I "$HERE/build_v9.py" final "$WORK/s1/stage1.xlsx" "$WORK/patch.json" "$WORK/p/$NAME" "$WORK/notes1.json"
# 5
python3 -I "$HERE/diff_versions.py" "$V8" "$WORK/p/$NAME" "$WORK/diff.json" || echo "diff_versions: differences found (expected in v9; classified by analyze_v9)"
recalc "$WORK/p/$NAME" "$WORK/lo2"
python3 -I "$HERE/figures_v9.py" "$V7" "$V8" "$WORK/p/$NAME" "$WORK/lo_pp/pp_scratch.xlsx" "$WORK/spec.json" $SC "$WORK/fig7.json" "$WORK/recon.json" \
  "$WORK/cn7.json" "$WORK/fig9_final.json"
cmp "$WORK/fig9.json" "$WORK/fig9_final.json" || { echo "figures differ between stage 2 and the final file"; exit 1; }
python3 -I "$HERE/privacy_v6.py" "$WORK/recon.json.names" "$WORK/notes1.md" "$WORK/notes1.json" "$WORK/p/$NAME" > "$WORK/privacy1.txt"
cat "$WORK/privacy1.txt"
python3 -I "$HERE/paylist_v9.py" "$WORK/p/$NAME" "$WORK/recon.json" "$WORK/notes1.md" > "$WORK/paylist1.txt"
cat "$WORK/paylist1.txt"
python3 -I "$HERE/analyze_v9.py" "$V8" "$WORK/p/$NAME" "$WORK/lo2/$NAME" "$WORK/diff.json" "$WORK/patch.json" "$WORK/spec.json" "$WORK/fig9.json" \
  "$WORK/notes1.md" "$WORK/notes1.json" "$WORK/privacy1.txt" "$WORK/paylist1.txt" "$WORK/analyze.json"
python3 -I "$HERE/report_v9.py" "$V7MD" "$WORK/cn7.json" "$V7" "$V8" "$WORK/p/$NAME" "$WORK/fig9.json" "$WORK/fig7.json" "$WORK/recon.json" "$WORK/spec.json" \
  "$WORK/noise.json" "$WORK/lo_version.txt" "$WF" "$COO" "$SD" "$NEW" "$WORK/notes2.json" "$WORK/notes2.md" "$WORK/analyze.json"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "Collation Notes JSON not stable between passes"; exit 1; }
echo "Collation Notes JSON stable between passes"
python3 -I "$HERE/privacy_v6.py" "$WORK/recon.json.names" "$WORK/notes2.md" "$WORK/notes2.json" "$WORK/p/$NAME"
python3 -I "$HERE/paylist_v9.py" "$WORK/p/$NAME" "$WORK/recon.json" "$WORK/notes2.md"
# 6
cp "$WORK/p/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/$MD"
cleanup
ls "$WORK"/*.names >/dev/null 2>&1 && { echo "scratch name list still present"; exit 1; }
echo "done: $OUT/$NAME and $OUT/$MD (no CSV); scratch name lists deleted"
