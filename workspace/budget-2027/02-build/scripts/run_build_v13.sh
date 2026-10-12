#!/bin/bash
# Usage: run_build_v13.sh V12_XLSX USER_EDIT_XLSX WORK_DIR OUT_DIR
#
# v13 build (handoff 2026-10-12): brief_v7 (CO!S98=24000, CO!S106=78000) + brief_v8 as amended (user HC roster merge,
# decisions 1-4), applied to v12 by script and shipped as ONE full LibreOffice recalculation + engine save (the v12
# technique; no XML spliced into saved parts). Pipeline per pass:
#   stage1 edits -> recalc -> 5 scenario recalcs -> figures (ties + user-file Z cross-check) -> stage2 (Collation
#   Notes) -> recalc+save = DELIVERABLE -> twin save (determinism) -> confined diff -> suite -> 3 switches re-run on
#   the shipped file -> privacy/per-person gates -> notes md.
# The whole pipeline runs TWICE; the two passes must produce a byte-identical md and xlsx files content-identical
# part for part after sorting <dataValidations> children (normcmp_v12.py; LibreOffice's one nondeterministic element
# order; zip timestamps are wall-clock - the v12-documented deviation). The shipped workbook is pass 1's engine save,
# untouched. No script reads a clock, file properties or dates (F1 rule); the handoff date is a constant.
# run_build_v12.sh ... run_build.sh still reproduce v12 ... v1.
set -euo pipefail
V12="$1"; USEREDIT="$2"; WORK="$3"; OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v13.xlsx
MD=02-build_notes_v13.md
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
  "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile" >/dev/null 2>&1 || true
  [ -s "$2/$(basename "$1")" ] || { echo "recalc: no output for $1, retrying once"; sleep 5; "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"; }
  [ -s "$2/$(basename "$1")" ] || { echo "recalc failed for $1"; exit 1; }
}
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"

switch () {   # $1=in xlsx  $2=out xlsx  $3..=cell=value pairs (chained scen_v8 edits)
  local IN="$1" OUTX="$2"; shift 2
  local CUR="$IN" TMP
  for kv in "$@"; do
    TMP="${OUTX%.xlsx}.$RANDOM.tmp.xlsx"
    python3 -I "$HERE/scen_v8.py" "$CUR" "$TMP" "${kv%%=*}" "${kv##*=}" >/dev/null
    [ "$CUR" != "$IN" ] && rm -f "$CUR"
    CUR="$TMP"
  done
  mv "$CUR" "$OUTX"
}

scenario () {   # $1=pass dir  $2=key  $3=base xlsx  $4..=cell=value pairs
  local P="$1" K="$2" BASE="$3"; shift 3
  mkdir -p "$P/scen/$K/in" "$P/scen/$K/out"
  switch "$BASE" "$P/scen/$K/in/$NAME" "$@"
  recalc "$P/scen/$K/in/$NAME" "$P/scen/$K/out"
}

build_pass () {   # $1 = pass dir
  local P="$1"
  mkdir -p "$P/s1rc" "$P/save1" "$P/save2" "$P/rc"
  # stage 1 edits + full recalc of the edited content
  python3 -I "$HERE/build_v13.py" stage1 "$V12" "$USEREDIT" "$P/s1_$NAME" "$P/spec.json"
  mv "$P/s1_$NAME" "$P/$NAME"; recalc "$P/$NAME" "$P/s1rc"; mv "$P/$NAME" "$P/s1_$NAME"
  # scenarios on the recalculated stage-1 content (values = the deliverable's)
  local DS="Depreciation Schedule"
  scenario "$P" b131     "$P/s1rc/$NAME" "$DS!B131=0"
  scenario "$P" b135     "$P/s1rc/$NAME" "$DS!B135=0"
  scenario "$P" b132     "$P/s1rc/$NAME" "$DS!B132=1"
  scenario "$P" b131b135 "$P/s1rc/$NAME" "$DS!B131=0" "$DS!B135=0"
  scenario "$P" b132b131 "$P/s1rc/$NAME" "$DS!B132=1" "$DS!B131=0"
  # figures (all ties asserted) -> stage 2 -> THE engine save (one full recalc + save of the final content)
  python3 -I "$HERE/figures_v13.py" "$V12" "$P/s1rc/$NAME" "$USEREDIT" "$P/scen" "$P/figures.json"
  python3 -I "$HERE/build_v13.py" stage2 "$P/s1_$NAME" "$P/figures.json" "$P/s2_$NAME"
  mv "$P/s2_$NAME" "$P/$NAME"; recalc "$P/$NAME" "$P/save1"; recalc "$P/$NAME" "$P/save2"; mv "$P/$NAME" "$P/s2_$NAME"
  python3 -I "$HERE/normcmp_v12.py" "$P/save1/$NAME" "$P/save2/$NAME" "$P/twopass.json"
  # confined diff + suite (with a fresh recalc of the deliverable)
  python3 -I "$HERE/diff_v13.py" "$V12" "$P/save1/$NAME" "$P/diff.json"
  recalc "$P/save1/$NAME" "$P/rc"
  python3 -I "$HERE/suite_v13.py" "$P/save1/$NAME" "$P/rc/$NAME" "$P/s1rc/$NAME" "$V12" "$P/figures.json" "$P/suite.json"
  # the three single switches re-run on the SHIPPED file (expected values from figures.json; $1 tolerance)
  local EXP_B131 EXP_B135 EXP_B132
  EXP_B131=$(python3 -I -c "import json;print(json.load(open('$P/figures.json'))['scen_b131'])")
  EXP_B135=$(python3 -I -c "import json;print(json.load(open('$P/figures.json'))['scen_b135'])")
  EXP_B132=$(python3 -I -c "import json;print(json.load(open('$P/figures.json'))['scen_b132'])")
  mkdir -p "$P/ship_scen"/{b131,b135,b132}/{in,out}
  switch "$P/save1/$NAME" "$P/ship_scen/b131/in/$NAME" "$DS!B131=0"; recalc "$P/ship_scen/b131/in/$NAME" "$P/ship_scen/b131/out"
  switch "$P/save1/$NAME" "$P/ship_scen/b135/in/$NAME" "$DS!B135=0"; recalc "$P/ship_scen/b135/in/$NAME" "$P/ship_scen/b135/out"
  switch "$P/save1/$NAME" "$P/ship_scen/b132/in/$NAME" "$DS!B132=1"; recalc "$P/ship_scen/b132/in/$NAME" "$P/ship_scen/b132/out"
  python3 -I "$HERE/scenread_v12.py" "$P/ship_scen/b131/out/$NAME" "$EXP_B131" 590317.51 > "$P/ship_scen/b131.json"
  python3 -I "$HERE/scenread_v12.py" "$P/ship_scen/b135/out/$NAME" "$EXP_B135" > "$P/ship_scen/b135.json"
  python3 -I "$HERE/scenread_v12.py" "$P/ship_scen/b132/out/$NAME" "$EXP_B132" > "$P/ship_scen/b132.json"
  cat "$P/ship_scen"/b131.json "$P/ship_scen"/b135.json "$P/ship_scen"/b132.json
  # notes + gates (scratch name list never leaves WORK; deleted on exit)
  python3 -I "$HERE/recon_v13.py" "$P/save1/$NAME" "$P/recon.json"
  python3 -I "$HERE/report_v13.py" "$P/figures.json" "$P/diff.json" "$P/suite.json" "$V12" "$USEREDIT" "$P/$MD"
  python3 -I "$HERE/names_v11.py" "$P/save1/$NAME" "$WORK/v13.names"
  python3 -I "$HERE/cntext_v12.py" "$P/save1/$NAME" "$P/cn.txt"
  python3 -I "$HERE/privacy_v6.py" "$WORK/v13.names" "$P/$MD" "$P/cn.txt" "$P/save1/$NAME"
  python3 -I "$HERE/paylist_v10.py" "$P/save1/$NAME" "$P/recon.json" "$P/$MD"
}

echo "=== pass 1 ==="
build_pass "$WORK/p1"
echo "=== pass 2 (md byte-identical; xlsx part-identical modulo dataValidation order) ==="
build_pass "$WORK/p2"
cmp "$WORK/p1/$MD" "$WORK/p2/$MD" || { echo "two-pass md not byte-identical"; exit 1; }
python3 -I "$HERE/normcmp_v12.py" "$WORK/p1/save1/$NAME" "$WORK/p2/save1/$NAME" "$WORK/crosspass.json" \
  || { echo "two-pass xlsx differ beyond dataValidation order"; exit 1; }
echo "two-pass build reproducible (md byte-identical; xlsx content-identical, see crosspass.json)"
cp "$WORK/p1/save1/$NAME" "$OUT/$NAME"
cp "$WORK/p1/$MD" "$OUT/$MD"
cleanup
ls "$WORK"/*.names >/dev/null 2>&1 && { echo "scratch name list still present"; exit 1; }
echo "done: $OUT/$NAME and $OUT/$MD; scratch name list deleted"
