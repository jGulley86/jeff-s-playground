import sys, openpyxl
p, sheet, out = sys.argv[1], sys.argv[2], sys.argv[3]
wb = openpyxl.load_workbook(p); wbv = openpyxl.load_workbook(p, data_only=True)
ws = wb[sheet]; wv = wbv[sheet]
with open(out,'w') as f:
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None:
                f.write(f"{c.coordinate}\t{c.value!r}\t=> {wv[c.coordinate].value!r}\n")
