#!/bin/bash
# Usage: run_build_v14.sh V13_XLSX V13_MD WORK_DIR OUT_DIR
#
# v14 build (handoff 2026-10-12): documentation corrections only on v13 - critic v13 B1 + O1-O4 and the verifier's
# stale-text findings. NO budget value changes (AG132 stays (646,753.85)); the v13 -> v14 diff is confined to the
# Collation Notes sheet. v12/v13 technique: scripted openpyxl text edits + ONE full LibreOffice recalculation +
# engine save as the deliverable (no XML spliced into saved parts). Pipeline per pass:
#   sweep pass 1 (on v13; must find the documented 31 stale occurrences) -> build_v14.py (Collation Notes text
#   edits) -> recalc+save = DELIVERABLE -> twin save (determinism) -> confined diff -> fresh recalc + suite ->
#   sweep pass 2 gate (on the deliverable; must be clean) -> notes md (asserted replacements on the v13 md, cross-
#   checked against the sweep) -> privacy/per-person gates.
# The whole pipeline runs TWICE; the two passes must produce a byte-identical md and xlsx files content-identical
# part for part after sorting <dataValidations> children (normcmp_v12.py; LibreOffice's one nondeterministic
# element order; zip timestamps are wall-clock - the v12-documented deviation). The shipped workbook is pass 1's
# engine save, untouched. No script reads a clock, file properties or dates (F1 rule).
# run_build_v13.sh ... run_build.sh still reproduce v13 ... v1.
set -euo pipefail
V13="$1"; V13MD="$2"; WORK="$3"; OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v14.xlsx
MD=02-build_notes_v14.md
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

build_pass () {   # $1 = pass dir
  local P="$1"
  mkdir -p "$P/save1" "$P/save2" "$P/rc"
  # sweep pass 1: the documented stale occurrences must be found on v13 (report_v14.py asserts the exact list)
  python3 -I "$HERE/sweep_v14.py" "$V13" pre "$P/sweep_pre.json"
  # the Collation Notes text edits -> THE engine save (one full recalc + save of the final content)
  python3 -I "$HERE/build_v14.py" "$V13" "$P/s2_$NAME"
  mv "$P/s2_$NAME" "$P/$NAME"; recalc "$P/$NAME" "$P/save1"; recalc "$P/$NAME" "$P/save2"; mv "$P/$NAME" "$P/s2_$NAME"
  python3 -I "$HERE/normcmp_v12.py" "$P/save1/$NAME" "$P/save2/$NAME" "$P/twopass.json"
  # confined diff + suite (with a fresh recalc of the deliverable)
  python3 -I "$HERE/diff_v14.py" "$V13" "$P/save1/$NAME" "$P/diff.json"
  recalc "$P/save1/$NAME" "$P/rc"
  python3 -I "$HERE/suite_v14.py" "$P/save1/$NAME" "$P/rc/$NAME" "$V13" "$P/suite.json"
  # sweep pass 2: the deliverable must be clean (gate)
  python3 -I "$HERE/sweep_v14.py" "$P/save1/$NAME" gate "$P/sweep_post.json"
  # notes + gates (scratch name list never leaves WORK; deleted on exit)
  python3 -I "$HERE/report_v14.py" "$V13MD" "$P/sweep_pre.json" "$P/$MD"
  python3 -I "$HERE/recon_v13.py" "$P/save1/$NAME" "$P/recon.json"
  python3 -I "$HERE/names_v11.py" "$P/save1/$NAME" "$WORK/v14.names"
  python3 -I "$HERE/cntext_v12.py" "$P/save1/$NAME" "$P/cn.txt"
  python3 -I "$HERE/privacy_v6.py" "$WORK/v14.names" "$P/$MD" "$P/cn.txt" "$P/save1/$NAME"
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
