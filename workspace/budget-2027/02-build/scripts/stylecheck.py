"""Compare formatting of carried sheets: SD source vs final output. Usage: stylecheck.py SD_BOOK OUT_XLSX"""
import sys, openpyxl
norm = lambda f: (f or "").replace("\\", "").replace('"', "")  # LibreOffice re-escapes literals ($ ( ) - ) without changing the format
sd = openpyxl.load_workbook(sys.argv[1]); out = openpyxl.load_workbook(sys.argv[2])
outv = openpyxl.load_workbook(sys.argv[2], data_only=True)
print("output sheets:", [(ws.title, ws.sheet_state) for ws in out.worksheets])
for sh in ["FO", "FE", "DeploySum", "Fld Ops Payroll", "Prod Payroll", "Fld Maint Budget", "Fld Eng Budget"]:
    a, b = sd[sh], out[sh]
    nf = fill = font = bold = n = 0
    for row in a.iter_rows():
        for c in row:
            if c.value is None and not c.has_style: continue
            d = b[c.coordinate]; n += 1
            if norm(c.number_format) != norm(d.number_format): nf += 1
            fa = c.fill.fgColor.rgb if c.fill and c.fill.fill_type else None
            fb = d.fill.fgColor.rgb if d.fill and d.fill.fill_type else None
            if (fa or "")[-6:] != (fb or "")[-6:]: fill += 1
            if bool(c.font.b) != bool(d.font.b): bold += 1
    widths = sum(1 for k, dim in a.column_dimensions.items() if dim.width and abs((b.column_dimensions[k].width or 0) - dim.width) > 0.6)
    hid_a = sorted(k for k, d in a.row_dimensions.items() if d.hidden); hid_b = sorted(k for k, d in b.row_dimensions.items() if d.hidden)
    print(f"{sh}: cells {n} numfmt-diff {nf} fill-diff {fill} bold-diff {bold} width-diff {widths} "
          f"dv {len(a.data_validations.dataValidation)}->{len(b.data_validations.dataValidation)} "
          f"cf {len(a.conditional_formatting)}->{len(b.conditional_formatting)} merged {len(a.merged_cells.ranges)}->{len(b.merged_cells.ranges)} "
          f"freeze {a.freeze_panes}->{b.freeze_panes} hiddenrows-equal {hid_a==hid_b} state {a.sheet_state}->{b.sheet_state}")
ws = outv["Collation Notes"]
for r in range(1, 40):
    vals = [ws.cell(r, c).value for c in range(1, 5)]
    if any(v is not None for v in vals): print(r, [str(v)[:70] if v is not None else None for v in vals])
