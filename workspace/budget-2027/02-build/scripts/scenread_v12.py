"""v12 scenario reader: after scen_v8.py set a Depreciation Schedule switch on a SCRATCH copy and
LibreOffice fully recalculated it, assert the 2027 COO contribution (COO P&L!AG132) and optionally
the PO 5110-5140 total (the B131 = 0 base) against the handoff's v11 scenario values.

Usage:
  python3 -I scenread_v12.py RECALCED_XLSX EXPECTED_AG132 [EXPECTED_PO_5100_SUM]
Tolerance $1 on AG132 (handoff), $0.01 on the PO base. Prints JSON on stdout; exit 1 on miss.
"""
import sys, json
import openpyxl

X = sys.argv[1]
exp = float(sys.argv[2])
exp_po = float(sys.argv[3]) if len(sys.argv) > 3 else None
wb = openpyxl.load_workbook(X, data_only=True)
ag132 = float(wb["COO P&L"]["AG132"].value)
out = {"AG132": ag132, "expected": exp, "ok": abs(ag132 - exp) <= 1.0}
if exp_po is not None:
    po = sum(float(wb["PO"][f"AG{r}"].value) for r in (33, 34, 35))
    out["PO_5100_sum"] = po
    out["PO_expected"] = exp_po
    out["ok"] = out["ok"] and abs(po - exp_po) <= 0.01
print(json.dumps(out))
sys.exit(0 if out["ok"] else 1)
