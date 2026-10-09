#!/bin/bash
# Usage: run_build_v7.sh COO_BOOK SD_BOOK NEW_DEPLOYSUM WORKFILE V6_XLSX V6_NOTES_MD WORK_DIR OUT_DIR
# v7 build: notes and presentation fix of v6 (critic v6 B1-B3, O1-O8; verifier v6 V1). NO budget value changes: the
# workbook is the v6 package with a regenerated Collation Notes sheet. run_build_v6.sh ... run_build.sh still reproduce
# v6 ... v1 (untouched). WORK_DIR must be outside the repo: it receives the scratch name list and per-person data, and
# the name lists are deleted at the end.
#   1. prodpay_v6 + recalc on v6 -> recon_v6 on v6 (reconciliation JSON; the roster CSV stays in WORK_DIR, none is shipped)
#   2. scen_v7: scratch copy of v6 with Fld Ops Payroll!B11 - 1; recalc it and v6 -> I-28 FO side with knock-ons
#   3. figures_v7: every new v7 figure (B1-B3, O1, O2, O5, O6, V1)
#   4. cnotes_v6 (v6 Collation Notes, byte-exact round trip) -> report_v7 pass 1 -> build_v7 (v6 + Collation Notes)
#   5. checks: diff_versions v6 -> v7 (must be 0/0), recalc of v7, recon_v6 on v7 (must equal step 1), privacy_v6,
#      paylist_v7, analyze_v7 (exit 1 on any failed criterion), report_v7 pass 2 (JSON must equal pass 1), checks again
#   6. copy the xlsx and md to OUT_DIR; delete the scratch name lists (*.names) in WORK_DIR
set -euo pipefail
COO="$1"; SD="$2"; NEW="$3"; WF="$4"; V6="$5"; V6MD="$6"; WORK="$7"; OUT="$8"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v7.xlsx
MD=02-build_notes_v7.md
case "$WORK" in /*) ;; *) echo "WORK_DIR must be absolute (LibreOffice profile path)"; exit 1;; esac
REPO="$(git -C "$HERE" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$REPO" ]; then case "$(cd "$(dirname "$WORK")" && pwd)/$(basename "$WORK")" in "$REPO"/*) echo "WORK_DIR must be outside the repo"; exit 1;; esac; fi
for f in "$OUT/$NAME" "$OUT/$MD"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
mkdir -p "$WORK/pp" "$WORK/lo_pp" "$WORK/pp7" "$WORK/lo_pp7" "$WORK/sc" "$WORK/lo_base" "$WORK/lo_sc" "$WORK/p" "$WORK/lo2" "$OUT"
cleanup () { rm -f "$WORK"/*.names; }
trap cleanup EXIT
recalc () {   # recalc.sh exits 0 even if LibreOffice wrote nothing; check the output and retry once
  "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"
  [ -s "$2/$(basename "$1")" ] || { echo "recalc: no output, retrying once"; sleep 5; "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"; }
  [ -s "$2/$(basename "$1")" ] || { echo "recalc failed for $1"; exit 1; }
}
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"
# 1
python3 -I "$HERE/prodpay_v6.py" "$V6" "$WORK/pp/pp_scratch.xlsx"
recalc "$WORK/pp/pp_scratch.xlsx" "$WORK/lo_pp"
python3 -I "$HERE/recon_v6.py" "$WF" "$SD" "$COO" "$V6" "$WORK/lo_pp/pp_scratch.xlsx" "$WORK/recon.json" "$WORK/roster.csv"
# 2
python3 -I "$HERE/scen_v7.py" make "$V6" "$WORK/sc/scen.xlsx"
cp "$V6" "$WORK/sc/base.xlsx"
recalc "$WORK/sc/base.xlsx" "$WORK/lo_base"
recalc "$WORK/sc/scen.xlsx" "$WORK/lo_sc"
python3 -I "$HERE/scen_v7.py" compare "$V6" "$WORK/lo_base/base.xlsx" "$WORK/lo_sc/scen.xlsx" "$WORK/scen.json"
# 3
python3 -I "$HERE/figures_v7.py" "$V6" "$WORK/lo_pp/pp_scratch.xlsx" "$WORK/recon.json" "$WORK/scen.json" "$WF" "$SD" "$WORK/fig7.json"
# 4
python3 -I "$HERE/cnotes_v6.py" "$V6" "$WORK/cn6.json"
python3 -I "$HERE/report_v7.py" "$V6MD" "$WORK/cn6.json" "$V6" "$WORK/recon.json" "$WORK/fig7.json" "$WORK/lo_version.txt" "$WF" "$COO" "$SD" "$NEW" \
  "$WORK/notes1.json" "$WORK/notes1.md"
python3 -I "$HERE/build_v7.py" "$V6" "$WORK/notes1.json" "$WORK/p/$NAME"
# 5
python3 -I "$HERE/diff_versions.py" "$V6" "$WORK/p/$NAME" "$WORK/diff.json"   # exit 1 on any formula/value difference
recalc "$WORK/p/$NAME" "$WORK/lo2"
python3 -I "$HERE/prodpay_v6.py" "$WORK/p/$NAME" "$WORK/pp7/pp_scratch.xlsx"
recalc "$WORK/pp7/pp_scratch.xlsx" "$WORK/lo_pp7"
python3 -I "$HERE/recon_v6.py" "$WF" "$SD" "$COO" "$WORK/p/$NAME" "$WORK/lo_pp7/pp_scratch.xlsx" "$WORK/recon_v7.json" "$WORK/roster_v7.csv"
cmp "$WORK/roster.csv" "$WORK/roster_v7.csv" || { echo "roster map differs when recomputed from v7"; exit 1; }
python3 -I "$HERE/privacy_v6.py" "$WORK/recon.json.names" "$WORK/notes1.md" "$WORK/notes1.json" "$WORK/p/$NAME" > "$WORK/privacy1.txt"
cat "$WORK/privacy1.txt"
python3 -I "$HERE/paylist_v7.py" "$WORK/p/$NAME" "$WORK/recon.json" "$WORK/notes1.md" > "$WORK/paylist1.txt"
cat "$WORK/paylist1.txt"
python3 -I "$HERE/analyze_v7.py" "$V6" "$WORK/p/$NAME" "$WORK/lo2/$NAME" "$WORK/diff.json" "$WORK/recon.json" "$WORK/recon_v7.json" "$WORK/fig7.json" \
  "$WORK/notes1.md" "$WORK/notes1.json" "$WORK/privacy1.txt" "$WORK/paylist1.txt" "$WORK/analyze.json"
python3 -I "$HERE/report_v7.py" "$V6MD" "$WORK/cn6.json" "$V6" "$WORK/recon.json" "$WORK/fig7.json" "$WORK/lo_version.txt" "$WF" "$COO" "$SD" "$NEW" \
  "$WORK/notes2.json" "$WORK/notes2.md" "$WORK/analyze.json"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "Collation Notes JSON not stable between passes"; exit 1; }
echo "Collation Notes JSON stable between passes"
python3 -I "$HERE/privacy_v6.py" "$WORK/recon.json.names" "$WORK/notes2.md" "$WORK/notes2.json" "$WORK/p/$NAME"
python3 -I "$HERE/paylist_v7.py" "$WORK/p/$NAME" "$WORK/recon.json" "$WORK/notes2.md"
# 6
cp "$WORK/p/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/$MD"
cleanup
ls "$WORK"/*.names >/dev/null 2>&1 && { echo "scratch name list still present"; exit 1; }
echo "done: $OUT/$NAME and $OUT/$MD (no CSV); scratch name lists deleted"
