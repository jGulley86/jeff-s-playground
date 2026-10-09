#!/bin/bash
# Usage: run_build_v6.sh COO_BOOK SD_BOOK NEW_DEPLOYSUM WORKFILE V5_XLSX V5_NOTES_MD WORK_DIR OUT_DIR
# v6 build: v5 + six HC tabs from the COO HC & PL workfile (supporting, provenance) + payroll reconciliation against the
# employee-level rosters + regenerated Collation Notes. NO budget value changes. run_build_v5.sh ... run_build.sh still
# reproduce v5 ... v1 (untouched).
#   1. prodpay_v6 + recalc: scratch copy of v5 with Prod Payroll's XLOOKUP row replaced, recalculated (analysis only)
#   2. recon_v6: reconciliation JSON + roster-to-P&L map CSV (no names) + scratch name list for the privacy check
#   3. cnotes_v6: v5 Collation Notes extracted (byte-exact round trip)
#   4. build_v6 stage 1 (v5 + HC tabs) -> report_v6 pass 1 (Collation Notes JSON) -> build_v6 final
#   5. checks: diff_versions v5 -> v6 (must be 0/0), recalc of v6, recon_v6 on v6 (must equal step 2), analyze_v6
#      (exit 1 on any failed criterion), report_v6 pass 2 (JSON must equal pass 1), privacy_v6 (exit 1 on any name)
set -euo pipefail
COO="$1"; SD="$2"; NEW="$3"; WF="$4"; V5="$5"; V5MD="$6"; WORK="$7"; OUT="$8"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=02-build_COO_2027_Budget_Collated_v6.xlsx
MD=02-build_notes_v6.md
CSV=02-build_roster_map_v6.csv
case "$WORK" in /*) ;; *) echo "WORK_DIR must be absolute (LibreOffice profile path)"; exit 1;; esac
for f in "$OUT/$NAME" "$OUT/$MD" "$OUT/$CSV"; do
  [ -e "$f" ] && { echo "refusing to overwrite $f"; exit 1; }
done
mkdir -p "$WORK/pp" "$WORK/lo_pp" "$WORK/pp6" "$WORK/lo_pp6" "$WORK/s1" "$WORK/p" "$WORK/lo2" "$OUT"
recalc () {   # recalc.sh exits 0 even if LibreOffice wrote nothing; check the output and retry once
  "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"
  [ -s "$2/$(basename "$1")" ] || { echo "recalc: no output, retrying once"; sleep 5; "$HERE/recalc.sh" "$1" "$2" "$WORK/loprofile"; }
  [ -s "$2/$(basename "$1")" ] || { echo "recalc failed for $1"; exit 1; }
}
/usr/bin/soffice --version | head -1 > "$WORK/lo_version.txt"
python3 -I "$HERE/prodpay_v6.py" "$V5" "$WORK/pp/pp_scratch.xlsx"
recalc "$WORK/pp/pp_scratch.xlsx" "$WORK/lo_pp"
python3 -I "$HERE/recon_v6.py" "$WF" "$SD" "$COO" "$V5" "$WORK/lo_pp/pp_scratch.xlsx" "$WORK/recon.json" "$WORK/roster.csv"
python3 -I "$HERE/cnotes_v6.py" "$V5" "$WORK/cn5.json"
python3 -I "$HERE/build_v6.py" "$V5" "$WF" "$WORK/s1/stage1.xlsx" "$WORK/binfo1.json"
python3 -I "$HERE/report_v6.py" "$V5MD" "$WORK/cn5.json" "$V5" "$WORK/s1/stage1.xlsx" "$WORK/recon.json" "$WORK/binfo1.json" \
  "$WORK/lo_version.txt" "$WF" "$COO" "$SD" "$NEW" "$WORK/notes1.json" "$WORK/notes1.md"
python3 -I "$HERE/build_v6.py" "$V5" "$WF" "$WORK/p/$NAME" "$WORK/binfo.json" "$WORK/notes1.json"
cmp "$WORK/binfo1.json" "$WORK/binfo.json" || { echo "build info differs between stage 1 and final"; exit 1; }
python3 -I "$HERE/diff_versions.py" "$V5" "$WORK/p/$NAME" "$WORK/diff.json"   # exit 1 on any formula/value difference
recalc "$WORK/p/$NAME" "$WORK/lo2"
python3 -I "$HERE/prodpay_v6.py" "$WORK/p/$NAME" "$WORK/pp6/pp_scratch.xlsx"
recalc "$WORK/pp6/pp_scratch.xlsx" "$WORK/lo_pp6"
python3 -I "$HERE/recon_v6.py" "$WF" "$SD" "$COO" "$WORK/p/$NAME" "$WORK/lo_pp6/pp_scratch.xlsx" "$WORK/recon_v6.json" "$WORK/roster_v6.csv"
cmp "$WORK/roster.csv" "$WORK/roster_v6.csv" || { echo "roster map differs when recomputed from v6"; exit 1; }
python3 -I "$HERE/privacy_v6.py" "$WORK/recon.json.names" "$WORK/notes1.md" "$WORK/notes1.json" "$WORK/roster.csv" "$WORK/p/$NAME" > "$WORK/privacy1.txt"
cat "$WORK/privacy1.txt"
python3 -I "$HERE/analyze_v6.py" "$V5" "$WORK/p/$NAME" "$WORK/lo2/$NAME" "$WORK/diff.json" "$WORK/binfo.json" "$WORK/recon.json" \
  "$WORK/recon_v6.json" "$WORK/analyze.json" "$WORK/privacy1.txt"
python3 -I "$HERE/report_v6.py" "$V5MD" "$WORK/cn5.json" "$V5" "$WORK/p/$NAME" "$WORK/recon.json" "$WORK/binfo.json" \
  "$WORK/lo_version.txt" "$WF" "$COO" "$SD" "$NEW" "$WORK/notes2.json" "$WORK/notes2.md" "$WORK/analyze.json"
cmp "$WORK/notes1.json" "$WORK/notes2.json" || { echo "Collation Notes JSON not stable between passes"; exit 1; }
echo "Collation Notes JSON stable between passes"
python3 -I "$HERE/privacy_v6.py" "$WORK/recon.json.names" "$WORK/notes2.md" "$WORK/notes2.json" "$WORK/roster.csv" "$WORK/p/$NAME"
cp "$WORK/p/$NAME" "$OUT/$NAME"
cp "$WORK/notes2.md" "$OUT/$MD"
cp "$WORK/roster.csv" "$OUT/$CSV"
echo "done: $OUT/$NAME, $OUT/$MD and $OUT/$CSV"
