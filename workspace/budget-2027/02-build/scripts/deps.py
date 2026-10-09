import sys, openpyxl, re, collections
p = sys.argv[1]
wb = openpyxl.load_workbook(p)
names = wb.sheetnames
pat = re.compile(r"(?:'((?:[^']|'')+)'|([A-Za-z0-9_\.&\[\]]+))!")
for ws in wb.worksheets:
    deps = collections.Counter(); ext = []; nform=0
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and v.startswith('='):
                nform+=1
                for m in pat.finditer(v):
                    s = (m.group(1) or m.group(2)).replace("''","'")
                    deps[s]+=1
                    if '[' in s: ext.append((c.coordinate, v[:150]))
            elif v is not None and not isinstance(v,(str,int,float)) :
                pass
    print(ws.title, "formulas:", nform, dict(deps))
    for e in ext[:10]: print("   EXT", e)
    if len(ext)>10: print("   ... ext total", len(ext))
