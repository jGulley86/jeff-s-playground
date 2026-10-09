"""v3 build: start from the delivered v2 workbook and apply the brief_v3 changes.

Usage:
  python3 -I build_v3.py V2_XLSX NEW_DEPLOYSUM_XLSX OUT_XLSX EXT_JSON [NOTES_JSON]

What it does (and nothing else):
  A. DeploySum refresh from the 9/30/26 resolved file (rows 3-49 of the new file):
     - row map by label: new rows 1-38 -> same row; new rows 39-49 -> row + 1 (the collated sheet keeps the
       SD 'ARR - end of period' row 39, which the new file does not have; its B:R cells are cleared).
     - cells whose new-file formula references the external workbook '[1]' are stored as the new file's cached
       value (the formula text is listed on Collation Notes and in EXT_JSON); internal formulas are kept.
     - the 17 v2 'stale external-link value' comments (B17:R17) are removed (cells now hold resolved values).
     - '$000s' labels are relabelled '$' and flagged with a cell comment (values are whole dollars).
     - row visibility follows the new file for the mapped rows (recognized revenue row 40 becomes visible).
     - a live tie-out block (rows 69-76) compares rows 16-21 with the split rows 54-64.
  B. PO revenue: PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27); PO!R12 = 'Manual'.
  C. Depreciation: new visible 'Depreciation Schedule' tab; PO!U19:AF22 link to its output-by-GL rows;
     PO!R19:R22 = 'Manual'.
  D. Collation Notes: the v2 sheet is removed; if NOTES_JSON is given a v3 sheet is inserted at the front.
No other sheet, row or cell is touched.
"""
import sys, json, re, datetime
import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.formula import ArrayFormula

V2, NEW, OUT, EXT_JSON = sys.argv[1:5]
NOTES = sys.argv[5] if len(sys.argv) > 5 else None

AUTHOR = "v3 collation build"
DS = "DeploySum"
SCHED = "Depreciation Schedule"
EXCEL_ERRORS = {"#REF!", "#N/A", "#VALUE!", "#DIV/0!", "#NAME?", "#NUM!", "#NULL!", "#ERROR!"}


def maprow(r):
    """New-file row -> collated DeploySum row (label map verified in analyze_v3.py)."""
    return r if r <= 38 else r + 1


def note(text, w=320, h=110):
    c = Comment(text, AUTHOR)
    c.width, c.height = w, h
    return c


# ---------------------------------------------------------------- load
wb = openpyxl.load_workbook(V2)
nf = openpyxl.load_workbook(NEW)
nv = openpyxl.load_workbook(NEW, data_only=True)
ds = wb[DS]
src_f, src_v = nf[DS], nv[DS]

# ---------------------------------------------------------------- A. DeploySum refresh
ext = []          # external cells: (v3 coord, new coord, formula, stored value)
kept_formulas = 0
written_values = 0
for r in range(3, 50):
    for c in range(1, 19):                       # A:R
        f = src_f.cell(r, c).value
        if isinstance(f, ArrayFormula):          # e.g. A3 in the 9/30/26 file is an array formula
            f = f.text if f.text.startswith("=") else "=" + f.text
        v = src_v.cell(r, c).value
        tgt = ds.cell(maprow(r), c)
        if isinstance(f, str) and f.startswith("="):
            if "[1]" in f:
                tgt.value = v
                if isinstance(v, str) and v.startswith("="):
                    tgt.data_type = "s"
                ext.append([tgt.coordinate, src_f.cell(r, c).coordinate, f, v])
                written_values += 1
            else:
                # internal formula: shift any reference to rows >= 39 (none today; kept for safety)
                def sh(m):
                    col, row = m.group(1), int(m.group(2))
                    return f"{col}{maprow(row)}"
                fm = re.sub(r"(\$?[A-Z]{1,3}\$?)(\d+)\b", sh, f)
                if isinstance(src_f.cell(r, c).value, ArrayFormula):    # keep array-formula form (R27, R28)
                    fm = ArrayFormula(tgt.coordinate, fm)
                tgt.value = fm
                kept_formulas += 1
        else:
            if tgt.value != f:
                tgt.value = f
            if f is not None:
                written_values += 1
        if tgt.comment is not None and tgt.comment.text.startswith("stale external-link value"):
            tgt.comment = None

# ARR row (kept for the row map; not in the 9/30/26 file)
for c in range(2, 19):
    ds.cell(39, c).value = None
ds["A39"].comment = note("v3: 'ARR - end of period' is not in the 9/30/26 resolved file (it has no ARR row). "
                         "The row is kept empty so rows 40-42 and 53-66 keep their SD row numbers.")

# row visibility for mapped rows follows the new file
for r in range(3, 50):
    hid = bool(src_f.row_dimensions[r].hidden) if r in src_f.row_dimensions else False
    ds.row_dimensions[maprow(r)].hidden = hid
ds.row_dimensions[39].hidden = False

# '$000s' relabel (values are whole dollars) - flagged, not silent
relabel = []
for r in range(1, 50):
    cell = ds.cell(r, 1)
    t = cell.value
    if isinstance(t, str) and "$000s" in t:
        new = t.replace("Dollars in $000s.", "Dollars in $ (relabelled in v3; the source said $000s).")
        new = new.replace("($000s)", "($)")
        cell.value = new
        cell.comment = note(f"v3 relabel: source label was '{t[:120]}'. The values are whole dollars, not "
                            f"thousands (e.g. R13 total bookings 29,452,766; R29 CapEx 32,410,900). "
                            f"See 02-build_notes_v3.md I-30.")
        relabel.append([cell.coordinate, t, new])

# tie-out block (rows 69-76): rows 16-21 vs split rows 54-64
bold = Font(bold=True)
ds["A69"] = "v3 CHECK (added by the collation build): deployment rows 16-21 vs split rows 54-64 (0 = ties)"
ds["A69"].font = bold
checks = [
    (70, "Row 16+17 deployments − (rows 54+57+60)", "={c}16+{c}17-({c}54+{c}57+{c}60)"),
    (71, "Row 18 total deployments − row 64", "={c}18-{c}64"),
    (72, "Row 19 SlipLifts going live − (rows 55+58+61)", "={c}19-({c}55+{c}58+{c}61)"),
    (73, "Row 20 SlipTrays going live − (rows 56+59+62)", "={c}20-({c}56+{c}59+{c}62)"),
    (74, "Row 21 SlipBots going live − row 63", "={c}21-{c}63"),
    (75, "Row 17 SlipBot deployments (memo; no split row - must be 0 for row 16 to tie alone)", "={c}17"),
]
for r, lab, fm in checks:
    ds.cell(r, 1, lab)
    for c in range(2, 19):
        L = get_column_letter(c)
        ds.cell(r, c, fm.format(c=L)).number_format = "#,##0;(#,##0);0"
ds["A76"] = '=IF(SUMPRODUCT(ABS(B70:R74))=0,"Tie-out rows 16-21 vs 54-64: OK","Tie-out rows 16-21 vs 54-64: CHECK")'
ds["A76"].font = bold

# ---------------------------------------------------------------- C. Depreciation Schedule tab
ws = wb.create_sheet(SCHED, wb.sheetnames.index(DS) + 1)
H1 = Font(bold=True, size=14)
H2 = Font(bold=True, size=12)
HDR = PatternFill("solid", fgColor="DDEBF7")
INP = PatternFill("solid", fgColor="FFF2CC")
BLUE = Font(color="0000FF")
NUM = '#,##0.00;(#,##0.00);"-"'
INT = '#,##0;(#,##0);"-"'
MONTHS = list(range(6, 18))            # F..Q = Jan..Dec 27
FY = 18                                # R
NOTE_COL = 19                          # S
DSC = [get_column_letter(c) for c in range(6, 18)]   # DeploySum F..Q = Jan..Dec 27 (same letters)

ws["A1"] = "Depreciation Schedule - 2027 budget (added in collation build v3)"; ws["A1"].font = H1
ws["A2"] = ("Straight-line, no salvage. Yellow cells are inputs. Section 4 feeds PO rows 19-22 (U:AF), which roll "
            "into COO P&L. Sections 5-7 are memo checks and do not feed the budget.")
r = 4
ws.cell(r, 1, "1. INPUTS").font = H2; r += 1
for j, h in enumerate(["Input", "Value", "Unit", "Source / status"], 1):
    c = ws.cell(r, j, h); c.font = bold; c.fill = HDR
r += 1
INPUT_ROW = {}
inputs = [
    ("lift_cost", "SlipLift unit cost ($ per lift)", 65000, "$",
     "DeploySum!A46 (note 3, 9/30/26 file A46): 'SlipLift $65,000'. Stated in the source."),
    ("periph_cost", "SlipLift peripherals ($ per lift)",
     "=(DeploySum!R29-DeploySum!R25*B{tray})/DeploySum!R24-B{lift}", "$",
     "Derived: (FY27 CapEx DeploySum!R29 − SlipTrays to build R25 × tray cost) ÷ SlipLifts to build R24 − lift cost "
     "= 4,137.50. Note 3 shows '$4,138' because its TEXT format rounds to whole dollars. Reconciles every month (section 6)."),
    ("tray_cost", "SlipTray unit cost ($ per tray)", 8000, "$",
     "DeploySum!A46 (note 3): 'SlipTray $8,000'. Stated in the source."),
    ("lift_life", "SlipLift useful life (months)", 84, "months", "User-confirmed 2026-10-09: 7 years, straight-line."),
    ("tray_life", "SlipTray useful life (months)", 120, "months", "User-confirmed 2026-10-09: 10 years, straight-line."),
    ("periph_life", "SlipLift peripherals useful life (months)", "=B{lift_life}", "months",
     "Builder assumption: same life as the SlipLift (no life given for peripherals). User to confirm."),
    ("salvage", "Salvage value (% of cost)", 0, "%", "Brief v3 / user: no salvage value."),
    ("delay", "Depreciation start: months after the go-live month", 0, "months",
     "Brief v3 convention (labelled, user may change): 0 = full month of depreciation in the go-live month "
     "(DeploySum rows 19/20); 1 = start the month after go-live."),
    ("gl_lift", "GL - SlipLift", 5011, "GL", "User-confirmed (handoff): SlipLift -> 5011 SlipLift Depreciation (PO row 20)."),
    ("gl_tray", "GL - SlipTray", 5012, "GL",
     "User-confirmed 2026-10-09 ('Trays = carriers'): SlipTray -> 5012 SlipCarrier Depreciation (PO row 21)."),
    ("gl_periph", "GL - SlipLift peripherals", 5020, "GL",
     "Builder assumption: 5020 Robot Peripherals Depreciation (PO row 22), because PO's 2026 forecast books 5011 at "
     "exactly $65,000/84 per lift, i.e. without peripherals. Alternative: 5011. User to confirm."),
    ("oct_dec", "Oct-Dec 26 go-lives (DeploySum C19:E20)", "In run rate", "text",
     "Decision: NOT added explicitly; they are carried inside the PO Dec-26 run rate (section 2), which steps up for "
     "Q4-26 go-lives. Never both. Unit-count gap vs DeploySum is shown as a memo in section 5."),
]
for key, lab, val, unit, src in inputs:
    INPUT_ROW[key] = r
    r += 1
lift, tray = INPUT_ROW["lift_cost"], INPUT_ROW["tray_cost"]
for key, lab, val, unit, src in inputs:
    rr = INPUT_ROW[key]
    if isinstance(val, str) and val.startswith("="):
        val = val.format(tray=tray, lift=lift, lift_life=INPUT_ROW["lift_life"])
    ws.cell(rr, 1, lab)
    c = ws.cell(rr, 2, val); c.fill = INP; c.font = BLUE
    c.number_format = {"$": NUM, "months": "0", "%": "0.0%", "GL": "0", "text": "@"}[unit]
    ws.cell(rr, 3, unit)
    ws.cell(rr, 4, src)
I = {k: f"$B${v}" for k, v in INPUT_ROW.items()}

r += 1
ws.cell(r, 1, "2. EXISTING FLEET (in service before Jan-27): Dec-26 monthly run rate from PO 2026 forecast, carried flat").font = H2
r += 1
for j, h in enumerate(["Line", "Value ($/month)", "GL", "Source / status"], 1):
    c = ws.cell(r, j, h); c.font = bold; c.fill = HDR
r += 1
EXIST = []
exist_src = {
    19: "PO!M19 (Dec-26 forecast; J:M flat at this value). SlipBot fleet status - fully depreciated, retired or "
        "ongoing - is not in the workbook: USER TO CONFIRM. DeploySum note 4: no SlipBots are built; existing bots are redeployed.",
    20: "PO!M20 (Dec-26 forecast). Includes the PO forecast's Q4-26 step-ups (+9, +3, +3 lifts at $65,000/84).",
    21: "PO!M21 (Dec-26 forecast). Includes the PO forecast's Q4-26 step-ups (+29, +12, +12 trays at $8,000/120).",
    22: "PO!M22 (Dec-26 forecast). Q4-26 step-ups (+2,608.33, +1,025, +1,025) do not match DeploySum peripherals; basis unknown.",
}
gl_of = {19: 5010, 20: 5011, 21: 5012, 22: 5020}
for po_row in (19, 20, 21, 22):
    lab = wb["PO"].cell(po_row, 1).value
    ws.cell(r, 1, f"{lab} - existing fleet, Dec-26 run rate")
    c = ws.cell(r, 2, f"=PO!M{po_row}"); c.fill = INP; c.font = BLUE; c.number_format = NUM
    ws.cell(r, 3, gl_of[po_row])
    ws.cell(r, 4, exist_src[po_row])
    EXIST.append((po_row, r))
    r += 1

r += 1
ws.cell(r, 1, "3. MONTHLY CALCULATION (2027)").font = H2
r += 1
HROW = r
for j, h in enumerate(["Line", "GL", "Go-live month #", "Units", "$/month per row"], 1):
    c = ws.cell(r, j, h); c.font = bold; c.fill = HDR
for k, col in enumerate(MONTHS):
    c = ws.cell(r, col, f"=DeploySum!{DSC[k]}4"); c.number_format = "mmm-yy"; c.font = bold; c.fill = HDR
c = ws.cell(r, FY, "FY2027"); c.font = bold; c.fill = HDR
c = ws.cell(r, NOTE_COL, "Source / formula"); c.font = bold; c.fill = HDR
r += 1
MROW = r
ws.cell(r, 1, "Month # (Jan-27 = 1)")
for k, col in enumerate(MONTHS):
    ws.cell(r, col, k + 1)
r += 1
UNITS = {}
for key, lab, dsr in (("lift", "SlipLifts going live (units)", 19), ("tray", "SlipTrays going live (units)", 20)):
    ws.cell(r, 1, lab)
    for k, col in enumerate(MONTHS):
        ws.cell(r, col, f"=DeploySum!{DSC[k]}{dsr}").number_format = INT
    ws.cell(r, FY, f"=SUM(F{r}:Q{r})").number_format = INT
    ws.cell(r, NOTE_COL, f"DeploySum!F{dsr}:Q{dsr} (9/30/26 file row {dsr}); FY check vs DeploySum!R{dsr}")
    UNITS[key] = r
    r += 1
r += 1
CALC_START = r
ws.cell(r, 1, "Existing fleet (section 2), flat").font = bold; r += 1
for po_row, irow in EXIST:
    ws.cell(r, 1, ws.cell(irow, 1).value)
    ws.cell(r, 2, f"=C{irow}")
    ws.cell(r, 5, f"=B{irow}").number_format = NUM
    for col in MONTHS:
        ws.cell(r, col, f"=$E{r}").number_format = NUM
    ws.cell(r, FY, f"=SUM(F{r}:Q{r})").number_format = NUM
    ws.cell(r, NOTE_COL, f"Section 2 input B{irow}, every month")
    r += 1

month_lbl = []
for col in DSC:
    d = src_v[f"{col}4"].value
    month_lbl.append(d.strftime("%b-%y") if isinstance(d, (datetime.date, datetime.datetime)) else col)

VINT = {}
blocks = [
    ("lift", "New SlipLifts (2027 go-lives): one row per go-live month", "SlipLift", I["gl_lift"], I["lift_cost"], I["lift_life"], UNITS["lift"]),
    ("tray", "New SlipTrays (2027 go-lives): one row per go-live month", "SlipTray", I["gl_tray"], I["tray_cost"], I["tray_life"], UNITS["tray"]),
    ("periph", "New SlipLift peripherals (same units as SlipLifts)", "SlipLift peripherals", I["gl_periph"], I["periph_cost"], I["periph_life"], UNITS["lift"]),
]
for key, title, nm, gl, cost, life, urow in blocks:
    ws.cell(r, 1, title).font = bold; r += 1
    first = r
    for k in range(12):
        ucol = get_column_letter(MONTHS[k])
        ws.cell(r, 1, f"{nm} - go-live {month_lbl[k]}")
        ws.cell(r, 2, f"={gl}")
        ws.cell(r, 3, k + 1)
        ws.cell(r, 4, f"={ucol}${urow}").number_format = INT
        ws.cell(r, 5, f"=D{r}*{cost}*(1-{I['salvage']})/{life}").number_format = NUM
        for col in MONTHS:
            L = get_column_letter(col)
            ws.cell(r, col, f"=IF(AND({L}${MROW}>=$C{r}+{I['delay']},{L}${MROW}<$C{r}+{I['delay']}+{life}),$E{r},0)").number_format = NUM
        ws.cell(r, FY, f"=SUM(F{r}:Q{r})").number_format = NUM
        r += 1
    VINT[key] = (first, r - 1)
    ws.cell(first, NOTE_COL, f"Units x cost x (1 - salvage) / life; on from go-live month + start delay; GL from inputs")
CALC_END = r - 1

r += 1
ws.cell(r, 1, "4. OUTPUT BY GL (feeds PO rows 19-22, columns U:AF)").font = H2
r += 1
for j, h in enumerate(["GL line", "GL", "PO row"], 1):
    c = ws.cell(r, j, h); c.font = bold; c.fill = HDR
for k, col in enumerate(MONTHS):
    c = ws.cell(r, col, f"={get_column_letter(col)}{HROW}"); c.number_format = "mmm-yy"; c.font = bold; c.fill = HDR
c = ws.cell(r, FY, "FY2027"); c.font = bold; c.fill = HDR
r += 1
OUT_ROW = {}
for po_row in (19, 20, 21, 22):
    ws.cell(r, 1, wb["PO"].cell(po_row, 1).value)
    ws.cell(r, 2, gl_of[po_row])
    ws.cell(r, 3, po_row)
    for col in MONTHS:
        L = get_column_letter(col)
        ws.cell(r, col, f"=SUMIF($B${CALC_START}:$B${CALC_END},$B{r},{L}${CALC_START}:{L}${CALC_END})").number_format = NUM
    ws.cell(r, FY, f"=SUM(F{r}:Q{r})").number_format = NUM
    ws.cell(r, NOTE_COL, f"-> PO!U{po_row}:AF{po_row}")
    OUT_ROW[po_row] = r
    r += 1
TOT = r
ws.cell(r, 1, "Total depreciation 2027").font = bold
for col in list(MONTHS) + [FY]:
    L = get_column_letter(col)
    ws.cell(r, col, f"=SUM({L}{OUT_ROW[19]}:{L}{OUT_ROW[22]})").number_format = NUM
r += 1
ws.cell(r, 1, "  of which existing fleet (section 2)")
for col in list(MONTHS) + [FY]:
    L = get_column_letter(col)
    ws.cell(r, col, f"=SUM({L}{CALC_START + 1}:{L}{CALC_START + 4})").number_format = NUM
EXIST_TOT = r; r += 1
ws.cell(r, 1, "  of which new 2027 go-lives")
for col in list(MONTHS) + [FY]:
    L = get_column_letter(col)
    ws.cell(r, col, f"=SUM({L}{VINT['lift'][0]}:{L}{CALC_END})").number_format = NUM
NEW_TOT = r; r += 1
ws.cell(r, 1, "Check: GL outputs − all calc lines (must be 0; a non-0 means a GL input is not one of 5010/5011/5012/5020)")
for col in list(MONTHS) + [FY]:
    L = get_column_letter(col)
    ws.cell(r, col, f"={L}{TOT}-SUM({L}{CALC_START}:{L}{CALC_END})").number_format = NUM
CHECK_ROW = r; r += 2

# 5. memo: Q4-26 go-lives vs PO forecast step-ups
ws.cell(r, 1, "5. MEMO (not in budget): Oct-Dec 26 go-lives - DeploySum vs the step-ups inside the PO Dec-26 run rate").font = H2
r += 1
for j, h in enumerate(["Item", "SlipLift (5011)", "SlipTray (5012)", "Peripherals (5020)"], 1):
    c = ws.cell(r, j, h); c.font = bold; c.fill = HDR
r += 1
M5 = r
rows5 = [
    ("PO forecast Dec-26 − Sep-26 run rate ($/month) (PO!M − PO!J)", "=PO!M20-PO!J20", "=PO!M21-PO!J21", "=PO!M22-PO!J22", NUM),
    ("Monthly depreciation per unit at the inputs above ($/month)",
     f"={I['lift_cost']}/{I['lift_life']}", f"={I['tray_cost']}/{I['tray_life']}", f"={I['periph_cost']}/{I['periph_life']}", NUM),
    ("Units implied by the PO step-up (row 1 ÷ row 2)", f"=B{M5}/B{M5+1}", f"=C{M5}/C{M5+1}", f"=D{M5}/D{M5+1}", "#,##0.00"),
    ("DeploySum units going live Oct-Dec 26 (C:E)", "=SUM(DeploySum!C19:E19)", "=SUM(DeploySum!C20:E20)", "=SUM(DeploySum!C19:E19)", INT),
    ("Gap: DeploySum − PO step-up (units)", f"=B{M5+3}-B{M5+2}", f"=C{M5+3}-C{M5+2}", "n/a - 5020 step-ups are not a whole number of DeploySum peripheral sets", "#,##0.00"),
    ("Gap in $/month at the inputs (not budgeted)", f"=B{M5+4}*B{M5+1}", f"=C{M5+4}*C{M5+1}", "n/a - 5020 basis unknown", NUM),
    ("Gap for 12 months of 2027 (not budgeted)", f"=B{M5+5}*12", f"=C{M5+5}*12", "n/a", NUM),
]
for lab, b, c_, d, fmt in rows5:
    ws.cell(r, 1, lab)
    for j, v in ((2, b), (3, c_), (4, d)):
        cc = ws.cell(r, j, v); cc.number_format = fmt
    r += 1
ws.cell(r, 1, "PO forecast step-ups by month: 5011 +9 (Oct), +3 (Nov), +3 (Dec) lifts; 5012 +29, +12, +12 trays. "
              "DeploySum: lifts 9, 9, 0; trays 35, 32, 0. Oct lifts match; the rest do not.")
r += 2

# 6. memo: unit-cost reconciliation by production month
ws.cell(r, 1, "6. MEMO: unit-cost reconciliation - Production CapEx (DeploySum row 29) vs units to build (rows 24/25)").font = H2
r += 1
hdr6 = ["Production month", "SlipLifts to build", "SlipTrays to build", "CapEx (DeploySum)",
        "CapEx ÷ all units (single price)", "Lifts×(lift+periph)+trays×tray", "Residual", "Using note's rounded $4,138",
        "Residual (rounded)"]
for j, h in enumerate(hdr6, 1):
    c = ws.cell(r, j, h); c.font = bold; c.fill = HDR; c.alignment = Alignment(wrap_text=True)
r += 1
R6 = r
for col in [get_column_letter(c) for c in range(2, 18)]:      # DeploySum B..Q = Sep-26..Dec-27
    c = ws.cell(r, 1, f"=DeploySum!{col}4"); c.number_format = "mmm-yy"
    ws.cell(r, 2, f"=DeploySum!{col}24").number_format = INT
    ws.cell(r, 3, f"=DeploySum!{col}25").number_format = INT
    ws.cell(r, 4, f"=DeploySum!{col}29").number_format = NUM
    ws.cell(r, 5, f'=IF(B{r}+C{r}=0,"",D{r}/(B{r}+C{r}))').number_format = NUM
    ws.cell(r, 6, f"=B{r}*({I['lift_cost']}+{I['periph_cost']})+C{r}*{I['tray_cost']}").number_format = NUM
    ws.cell(r, 7, f"=D{r}-F{r}").number_format = NUM
    ws.cell(r, 8, f"=B{r}*({I['lift_cost']}+ROUND({I['periph_cost']},0))+C{r}*{I['tray_cost']}").number_format = NUM
    ws.cell(r, 9, f"=D{r}-H{r}").number_format = NUM
    r += 1
R6E = r - 1
ws.cell(r, 1, "Total Sep-26..Dec-27").font = bold
for j in (2, 3, 4, 6, 7, 8, 9):
    L = get_column_letter(j)
    ws.cell(r, j, f"=SUM({L}{R6}:{L}{R6E})").number_format = NUM if j > 3 else INT
R6T = r
r += 1
ws.cell(r, 1, "Max |residual| any month (derived peripherals)")
ws.cell(r, 7, f"=SUMPRODUCT(MAX(ABS(G{R6}:G{R6E})))").number_format = NUM
R6MAX = r
r += 2

# 7. memo: depreciable base of 2027 go-lives vs CapEx bridge
ws.cell(r, 1, "7. MEMO: depreciable cost of 2027 go-lives vs Production CapEx (builds run 2 months before go-live, note 1)").font = H2
r += 1
R7 = r
rows7 = [
    ("Depreciable cost of 2027 go-lives: lifts×(lift+periph) + trays×tray",
     f"=R{UNITS['lift']}*({I['lift_cost']}+{I['periph_cost']})+R{UNITS['tray']}*{I['tray_cost']}"),
    ("FY27 Production CapEx (DeploySum!R29)", "=DeploySum!R29"),
    ("less: CapEx for 2028 go-lives (DeploySum!R35)", "=-DeploySum!R35"),
    ("plus: Nov-Dec 26 builds for Jan-Feb 27 go-lives (DeploySum!D29+E29)", "=DeploySum!D29+DeploySum!E29"),
    ("Bridge total", f"=SUM(B{R7+1}:B{R7+3})"),
    ("Difference (must be 0)", f"=B{R7}-B{R7+4}"),
]
for lab, f in rows7:
    ws.cell(r, 1, lab); ws.cell(r, 2, f).number_format = NUM; r += 1

widths = {1: 62, 2: 14, 3: 12, 4: 14, 5: 16}
for j in range(1, 20):
    ws.column_dimensions[get_column_letter(j)].width = widths.get(j, 13)
ws.column_dimensions["S"].width = 70
ws.freeze_panes = "B4"

# ---------------------------------------------------------------- B + C. PO links
po = wb["PO"]
po["R12"] = "Manual"
for k in range(12):
    po.cell(12, 21 + k, f"=DeploySum!{DSC[k]}40")          # U..AF <- DeploySum F..Q row 40
po["AI12"] = ("v3: = DeploySum!F40:Q40 recognized revenue Jan-Dec 27 (9/30/26 file row 39). Orchestrator "
              "assumption: all to 4100; 4500/4900 stay 0.")
for po_row in (19, 20, 21, 22):
    po.cell(po_row, 18).value = "Manual"
    for k in range(12):
        po.cell(po_row, 21 + k, f"='{SCHED}'!{get_column_letter(MONTHS[k])}{OUT_ROW[po_row]}")
    po.cell(po_row, 35).value = f"v3: from '{SCHED}' row {OUT_ROW[po_row]} (straight-line; see inputs)."

# ---------------------------------------------------------------- D. Collation Notes
if "Collation Notes" in wb.sheetnames:
    del wb["Collation Notes"]
if NOTES:
    notes = json.load(open(NOTES))
    cn = wb.create_sheet("Collation Notes", 0)
    r = 1
    cn.cell(r, 1, notes["title"]).font = Font(bold=True, size=14); r += 2
    for sec in notes["sections"]:
        cn.cell(r, 1, sec["heading"]).font = Font(bold=True, size=12); r += 1
        for line in sec.get("lines", []):
            c = cn.cell(r, 1, line)
            if isinstance(line, str) and line.startswith("="):
                c.value = line[1:]; c.data_type = "s"
            r += 1
        t = sec.get("table")
        if t:
            for j, h in enumerate(t["header"], 1):
                c = cn.cell(r, j, h); c.font = bold; c.fill = HDR
            r += 1
            fcols = set(t.get("formula_cols", []))
            for row in t["rows"]:
                for j, v in enumerate(row, 1):
                    c = cn.cell(r, j, v)
                    c.alignment = Alignment(wrap_text=True, vertical="top")
                    if isinstance(v, str) and v.startswith("="):
                        if j in fcols:
                            c.number_format = "#,##0;(#,##0)"
                        else:
                            c.value = v[1:]; c.data_type = "s"
                    elif isinstance(v, str) and v in EXCEL_ERRORS:
                        c.data_type = "s"
                    elif isinstance(v, (int, float)):
                        c.number_format = "#,##0;(#,##0)"
                r += 1
        r += 1
    for j, w in enumerate(notes.get("col_widths", [14, 10, 26, 60, 60, 50, 16, 16]), 1):
        cn.column_dimensions[get_column_letter(j)].width = w

wb.save(OUT)
json.dump({"ext": ext, "kept_formulas": kept_formulas, "written": written_values, "relabel": relabel,
           "layout": {"input_row": INPUT_ROW, "exist": EXIST, "units": UNITS, "month_row": MROW, "header_row": HROW,
                      "calc": [CALC_START, CALC_END], "vint": VINT, "out_row": OUT_ROW, "tot": TOT,
                      "exist_tot": EXIST_TOT, "new_tot": NEW_TOT, "check": CHECK_ROW, "m5": M5,
                      "r6": [R6, R6E, R6T, R6MAX], "r7": R7}},
          open(EXT_JSON, "w"), indent=1, default=str)
print(f"built {OUT}: DeploySum external cells stored as values {len(ext)}, internal formulas kept {kept_formulas}, "
      f"relabelled {len(relabel)}; schedule outputs rows {OUT_ROW}")
