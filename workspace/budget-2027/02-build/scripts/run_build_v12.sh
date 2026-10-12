#!/bin/bash
# Usage: run_build_v12.sh V11_XLSX V11_NOTES_MD USER_EDIT_XLSX WORKFILE_XLSX FINAL4_XLSX WORK_DIR OUT_DIR
#
# v12 build (handoff 2026-10-12): Excel #REF! incident on FINAL_v4 (= v11).
#   1. DIAGNOSIS (forensics_v12.py, asserted): the workbook loaded cleanly in the user's Excel; the #REF!s in
#      PO 33-35 + dependents are the correct result of the user's own in-Excel deletion of HC-PO row 20
#      (Material Handler, MH-01), which PO!U33:AF35 reference. The handoff's entity-escape hypothesis is refuted
#      by measurement (fscan_v12.py on v11 + the byte-identity exhibit + the user's re-saved copy).
#   2. FIX (commissioned hardening): v11 saved once, whole, by LibreOffice headless with a full-recalculation
#      profile (recalc.sh) -> every part engine-serialized; no package patch. Values/formulas proven identical
#      (fdiff_v12.py), standard suite + scenario switches green (suite_v12.py, scen_v8.py + scenread_v12.py),
#      package clean (fscan_v12.py --require-clean).
#
# The whole pipeline runs TWICE. The two passes must produce a byte-identical md, and xlsx files that are
# byte-identical part for part after sorting <dataValidations> children (normcmp_v12.py): LibreOffice emits that
# one element list in nondeterministic order, and zip entry timestamps are wall-clock, so whole-file byte-identity
# is not achievable (documented deviation). The shipped workbook is pass 1's FIRST engine save, untouched.
# No script reads a clock, file properties or dates (F1 rule); the handoff date is a constant in report_v12.py.
# run_build_v11.sh ... run_build.sh still reproduce v11 ... v1.
set -euo pipefail
V11="$1"; V11MD="$2"; USEREDIT="$3"; WORKFILE="$4"; FINAL4="$5"; WORK="$6"; OUT="$7"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v12.xlsx
MD=02-build_notes_v12.md
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

scenario () {  # $1=pass dir  $2=key  $3=cell  $4=value  $5=expected AG132  [$6=expected PO 5110-5140 sum]
  local P="$1" K="$2"
  mkdir -p "$P/scen/$K/in" "$P/scen/$K/out"   # separate dirs: recalc output keeps the input's basename
  python3 -I "$HERE/scen_v8.py" "$P/save1/$NAME" "$P/scen/$K/in/$NAME" "$3" "$4"
  recalc "$P/scen/$K/in/$NAME" "$P/scen/$K/out"
  python3 -I "$HERE/scenread_v12.py" "$P/scen/$K/out/$NAME" "$5" ${6:+"$6"} > "$P/scen/$K/result.json"
  cat "$P/scen/$K/result.json"
}

build_pass () {   # $1 = pass dir
  local P="$1"
  mkdir -p "$P/in" "$P/save1" "$P/save2" "$P/rc"
  # the engine save (the deliverable) + an independent twin save for the determinism exhibit
  cp "$V11" "$P/in/$NAME"
  recalc "$P/in/$NAME" "$P/save1"
  recalc "$P/in/$NAME" "$P/save2"
  python3 -I "$HERE/normcmp_v12.py" "$P/save1/$NAME" "$P/save2/$NAME" "$P/twopass.json"
  # diagnosis + package scans
  python3 -I "$HERE/forensics_v12.py" "$V11" "$USEREDIT" "$WORKFILE" "$FINAL4" "$P/save1/$NAME" "$P/forensics.json"
  python3 -I "$HERE/fscan_v12.py" "$V11" "$P/fscan11.json"
  python3 -I "$HERE/fscan_v12.py" "$P/save1/$NAME" "$P/fscan12.json" --require-clean
  # semantic identity v11 -> v12
  python3 -I "$HERE/fdiff_v12.py" "$V11" "$P/save1/$NAME" "$P/fdiff.json"
  # standard suite (needs a full recalc of the candidate)
  recalc "$P/save1/$NAME" "$P/rc"
  python3 -I "$HERE/suite_v12.py" "$P/save1/$NAME" "$P/rc/$NAME" "$V11" "$P/suite.json"
  # scenario switches (scratch copies; handoff targets, $1 tolerance)
  scenario "$P" b131 "Depreciation Schedule!B131" 0 -399860 590317.51
  scenario "$P" b135 "Depreciation Schedule!B135" 0 32228
  scenario "$P" b132 "Depreciation Schedule!B132" 1 98441
  python3 -I -c "
import json, sys
out = {k: json.load(open(f'$P/scen/{k2}/result.json')) for k, k2 in
       [('B131=0','b131'), ('B135=0','b135'), ('B132=1','b132')]}
json.dump(out, open('$P/scen.json', 'w'), indent=1)
print('scenarios:', json.dumps(out))
"
  # notes
  python3 -I "$HERE/report_v12.py" "$V11MD" "$P/fscan11.json" "$P/fscan12.json" "$P/fdiff.json" \
    "$P/suite.json" "$P/scen.json" "$P/forensics.json" "$P/twopass.json" "$WORK/lo_version.txt" "$P/$MD"
  # privacy + per-person amount gates (names scratch list never leaves WORK)
  python3 -I "$HERE/names_v11.py" "$P/save1/$NAME" "$WORK/v12.names"
  python3 -I "$HERE/cntext_v12.py" "$P/save1/$NAME" "$P/cn.txt"
  python3 -I "$HERE/privacy_v6.py" "$WORK/v12.names" "$P/$MD" "$P/cn.txt" "$P/save1/$NAME"
  python3 -I "$HERE/recon_v11.py" "$P/save1/$NAME" "$P/recon.json"
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
