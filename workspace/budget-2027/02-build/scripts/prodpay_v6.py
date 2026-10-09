"""v6 analysis helper: make a SCRATCH copy of the v5 workbook in which Prod Payroll row 48 (the 16 XLOOKUP cells that
LibreOffice 24.2 cannot evaluate) uses an equivalent classic formula, so a LibreOffice recalculation can evaluate the
tray and supervisor rows of the production payroll model. The scratch file is analysis input only; it is never shipped
and the v6 workbook keeps the original XLOOKUP formulas.

Usage:
  python3 -I prodpay_v6.py V5_XLSX OUT_SCRATCH_XLSX

Original (Prod Payroll!B48:Q48):
  _xlfn.xlookup(X,$B$20:$O$20,$B$20:$O$20,MAX($B$20:$O$20),1)
  = the smallest tray tier >= X (match_mode 1: exact or next larger), or MAX(tiers) if X is above every tier.
Replacement (tiers B20:O20 are ascending and unique; checked here):
  IF(X>MAX(r),MAX(r),SMALL(r,COUNTIF(r,"<"&X)+1))
Every other zip part is copied byte for byte.
"""
import sys, re, zipfile
import openpyxl

V5, OUT = sys.argv[1:3]
wb = openpyxl.load_workbook(V5, data_only=True)
tiers = [wb["Prod Payroll"].cell(20, c).value for c in range(2, 16)]
assert all(isinstance(t, (int, float)) for t in tiers) and tiers == sorted(set(tiers)), ("tray tiers must ascend", tiers)

zin = zipfile.ZipFile(V5)
wbxml = zin.read("xl/workbook.xml").decode()
rels = zin.read("xl/_rels/workbook.xml.rels").decode()
rid = re.search(r'<sheet name="Prod Payroll"[^>]*r:id="(rId\d+)"', wbxml).group(1)
part = "xl/" + re.search(rf'<Relationship Id="{rid}"[^>]*Target="([^"]+)"', rels).group(1)

R = "$B$20:$O$20"
pat = re.compile(r'<c r="([B-Q])48"( s="\d+")? t="e"><f aca="false">_xlfn\.xlookup\(MAX\(\$C\$8,([B-Q])47\),'
                 r'\$B\$20:\$O\$20,\$B\$20:\$O\$20,MAX\(\$B\$20:\$O\$20\),1\)</f><v>#NAME\?</v></c>')


def repl(m):
    col, s, col2 = m.group(1), m.group(2) or "", m.group(3)
    assert col == col2
    x = f"MAX($C$8,{col}47)"
    f = f'IF({x}&gt;MAX({R}),MAX({R}),SMALL({R},COUNTIF({R},"&lt;"&amp;{x})+1))'
    return f'<c r="{col}48"{s}><f aca="false">{f}</f><v>0</v></c>'


zout = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
n = 0
for info in zin.infolist():
    data = zin.read(info.filename)
    if info.filename == part:
        x, n = pat.subn(repl, data.decode("utf-8"))
        data = x.encode("utf-8")
    zout.writestr(info, data)
zout.close()
assert n == 16, ("expected 16 XLOOKUP cells in Prod Payroll row 48", n)
print(f"scratch {OUT}: Prod Payroll!B48:Q48 XLOOKUP -> SMALL/COUNTIF equivalent ({n} cells); tiers {tiers}")
