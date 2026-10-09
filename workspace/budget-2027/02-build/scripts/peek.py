import sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], data_only=True, read_only=True)
print(wb.sheetnames)
for spec in sys.argv[2:]:
    sh, cell = spec.split('|')
    print(spec, wb[sh][cell].value)
