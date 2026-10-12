"""v12 helper: dump every Collation Notes cell text of an xlsx to a plain-text file so privacy_v6.py
can scan it even though the engine save moved the sheet's strings into sharedStrings.xml (privacy_v6's
own .xlsx mode reads the sheet part raw, which only works for inlineStr parts).

Usage:
  python3 -I cntext_v12.py XLSX OUT_TXT
"""
import sys
import openpyxl

X, OUT = sys.argv[1:3]
wb = openpyxl.load_workbook(X, data_only=True)
ws = wb["Collation Notes"]
with open(OUT, "w", encoding="utf-8") as f:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value:
                f.write(c.value + "\n")
print(f"cntext_v12: Collation Notes texts of {X} -> {OUT}")
