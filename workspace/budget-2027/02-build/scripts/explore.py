import sys, openpyxl, collections
for p in sys.argv[1:]:
    wb = openpyxl.load_workbook(p)
    print("=====", p)
    dn = wb.defined_names
    print("n defined names (global):", len(dn))
    refs = collections.Counter()
    for n,d in dn.items():
        t=d.attr_text
        if '#REF' in t: refs['#REF']+=1
        elif t.startswith('{'): refs['array']+=1
        elif '[' in t: refs['external']+=1
        else: refs['other']+=1; print("  ", n, t[:120])
    print(refs)
    print("external links:", [ (l.file_link.Target if l.file_link else None) for l in wb._external_links])
    for ws in wb.worksheets:
        print(ws.title, ws.sheet_state, ws.dimensions, "dv:", len(ws.data_validations.dataValidation), "cf:", len(ws.conditional_formatting), "merged:", len(ws.merged_cells.ranges), "localnames:", len(ws.defined_names), "freeze:", ws.freeze_panes)
