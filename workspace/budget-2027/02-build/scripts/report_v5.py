"""Write 02-build_notes_v5.md and the v5 Collation Notes content (JSON).

Usage:
  python3 -I report_v5.py V3_MD V3_XLSX V4_XLSX V5_XLSX FIG_V5_JSON FIG_V4_JSON PATCH_JSON LO_VERSION_TXT COO SD NEW
                          OUT_NOTES_JSON OUT_MD [ANALYZE_JSON]

v5 = v4 + one input (Fld Eng Budget!B21 = Head of Service Delivery salary, user-confirmed) + critic v4 N1-N3.
The text is built exactly as report_v4.py builds it (v3 md + structured v3 Collation Notes + the v4 edits), with the
v5 edits on top. Numbers come from FIG_V5_JSON (figures_v5.py on the v5 workbook) and, for the v4 -> v5 deltas, from
FIG_V4_JSON (figures_v5.py on v4). Tables carried from v2/v3 that quote workbook values (variance scan,
cross-department overlap, raise steps) are regenerated from V5_XLSX; each generator must first reproduce the v4 text
exactly from V4_XLSX, so a generator that does not match the old table stops the script.
- Every new number comes from FIG_JSON (figures_v5.py: workbook cached values + inputs). No figure is typed here.
- v3 text is reused section by section from V3_MD; each edit is a targeted replacement that must hit exactly once
  (the script stops otherwise), so nothing is changed silently.
- The assumptions register, issues list, '$000s' relabel table and external-formula list are read from the v3
  Collation Notes sheet (structured cells) and checked against the v3 md before editing.
- Without ANALYZE_JSON the md has placeholders for the diff / package sections (pass 1); the Collation Notes JSON
  does not depend on ANALYZE_JSON, so it is identical in both passes.
"""
import sys, json, re, hashlib, collections
import openpyxl

(V3_MD, V3_XLSX, V4_XLSX, V5_XLSX, FIG, FIG4, PATCH, LOV, COO, SD, NEW, OUT_JSON, OUT_MD) = sys.argv[1:14]
AN = json.load(open(sys.argv[14])) if len(sys.argv) > 14 else None
F = json.load(open(FIG)); F4 = json.load(open(FIG4)); PT = json.load(open(PATCH))
C4 = F4["contribution"]; I26 = F["i26"]; SGA, SGA4 = F["sga"], F4["sga"]
assert F["i26_b21"] == PT["input"][2] and F4["i26_b21"] is None
lov = open(LOV).read().strip()
v3md = open(V3_MD).read()
H = F["headline"]; C = F["contribution"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def f0(x):
    if x is None: return ""
    x = float(x)
    if abs(x) < 0.5: return "0"
    return f"({abs(x):,.0f})" if x < 0 else f"{x:,.0f}"


def f2(x):
    x = float(x)
    return f"({abs(x):,.2f})" if x < 0 else f"{x:,.2f}"


def eff(x):
    """Effect on the 2027 COO contribution: + raises it, ( ) lowers it."""
    x = float(x)
    if abs(x) < 0.5: return "0"
    return f"+{x:,.0f}" if x > 0 else f"({abs(x):,.0f})"


def pct_nm(new, base):
    """% change; 'n/m' when the base is zero or negative, or the sign flips (positive base, negative new)."""
    if base is None or base <= 0 or new < 0:
        return "n/m"
    return f"{(new - base) / base * 100:.0f}%"


def rep(text, old, new, count=1):
    n = text.count(old)
    assert n == count, (n, old[:90])
    return text.replace(old, new)


# ------------------------------------------------------------------ v3 md sections
parts = re.split(r"(?m)^## ", v3md)
head_txt = parts[0]
SEC = collections.OrderedDict()
for p in parts[1:]:
    title, _, body = p.partition("\n")
    SEC[title.strip()] = body
expected = ["Headline", "Changes from v2", "Completion criteria", "Depreciation schedule summary",
            "Unit-cost reconciliation", "Revenue", "Assumptions register", "DeploySum refresh and tie-out",
            "v2 -> v3 diff", "Error scan", "Package", "Sheets in the output", "Severity scale", "Issues (v3)",
            "Carried from v2 (still valid: FO, FE, CO, PE and PO payroll unchanged)", "Decisions", "Not done / limits"]
assert list(SEC) == expected, list(SEC)

# ------------------------------------------------------------------ v3 Collation Notes sheet (structured)
wb3 = openpyxl.load_workbook(V3_XLSX)
cn3 = wb3["Collation Notes"]
sheet_secs = collections.OrderedDict(); cur = None; mode = None
for r in range(1, cn3.max_row + 1):
    vals = [cn3.cell(r, c).value for c in range(1, cn3.max_column + 1)]
    a = cn3.cell(r, 1)
    if all(x is None for x in vals):
        mode = None; continue
    if a.font is not None and a.font.b and a.font.sz == 12 and all(x is None for x in vals[1:]):
        cur = a.value; sheet_secs[cur] = {"lines": [], "header": None, "rows": []}; mode = "start"; continue
    if cur is None:
        continue
    if mode == "start" and a.font is not None and a.font.b:
        while vals and vals[-1] is None: vals.pop()
        sheet_secs[cur]["header"] = vals; mode = "rows"; continue
    if mode == "rows":
        n = len(sheet_secs[cur]["header"])
        sheet_secs[cur]["rows"].append(vals[:n])
    else:
        sheet_secs[cur]["lines"].append(a.value)


def sec_by_prefix(pfx):
    k = [x for x in sheet_secs if x.startswith(pfx)]
    assert len(k) == 1, (pfx, list(sheet_secs))
    return sheet_secs[k[0]]


reg = [list(x) for x in sec_by_prefix("Assumptions register")["rows"]]
iss_rows = [list(x) for x in sec_by_prefix("Issues (v3)")["rows"]]
relabel = sec_by_prefix("'$000s' relabel")
extf = sec_by_prefix("DeploySum external-link formulas")
mdrow = lambda row: "| " + " | ".join("" if x is None else str(x) for x in row) + " |"
# consistency: the sheet rows render to exactly the v3 md rows
for row in reg:
    assert mdrow(row) in SEC["Assumptions register"], row[0]
for row in iss_rows:
    assert mdrow(row) in SEC["Issues (v3)"], row[0]
iss = collections.OrderedDict((row[0], row) for row in iss_rows)
IHDR = ["ID", "Sev", "Location (sheet!cell)", "Finding", "Evidence", "2027 impact", "Basis", "Recommended action"]

# ------------------------------------------------------------------ derived figures (all from F)
q4 = F["q4"]; di = F["dep_inputs"]; i32 = F["i32_5010"]; i02 = F["i02"]
lifts_po, trays_po = sum(q4["po_lifts"]), sum(q4["po_trays"])
lifts_ds, trays_ds = sum(q4["ds_lifts"]), sum(q4["ds_trays"])
dec_l, dec_t = F["i31_dec_units"]
jl, jt = F["jan27_units"]
RR = F["runrate"]
rev = H["Revenue"]["AG"]; cost27 = H["COGS"]["AG"] + H["Opex"]["AG"]
flip = F["flip_alone"]; after = F["after_alone"]

# ------------------------------------------------------------------ 1. Decisions pending
DEC_HDR = ["#", "Decision (user)", "Issue", "Current treatment in the budget",
           "Alternatives: effect on 2027 COO contribution (+ raises, ( ) lowers)", "Who"]
DEC = [
    ["1", "SlipBot fleet status (5010 depreciation)", "I-32",
     f"Carried flat at the PO Dec-26 run rate {f2(RR['19'])}/month = {f0(F['i32_full'])} in 2027 (builder assumption, A-17).",
     f"Fully depreciated or retired from Jan-27: {eff(F['i32_full'])}. Continue the 2026 decline ({f0(i32['slope_jan_sep'])}/month, Jan-Sep 26) from the Sep-26 level in Jan-27: {eff(F['i32_trend'])} "
     f"(actuals Jan-Aug only, {f0(i32['slope_jan_aug'])}/month: {eff(F['i32_trend_actuals'])}). Same decline also running through Oct-Dec 26, floored at 0: {eff(F['i32_trend_sep'])} "
     f"(actuals-only slope: {eff(F['i32_trend_sep_actuals'])}). Ongoing at the run rate: 0. "
     f"Related: the 5020 base of {f0(F['i32_5020_jan26'])}/month (Jan-26, before any SlipLift depreciation) may end with the SlipBots: up to {eff(F['i32_5020_base_x12'])}.",
     "User, with PO/Finance (fixed-asset register)"],
    ["2", "Q4-26 go-lives: PO run rate or DeploySum", "I-31",
     f"Inside the PO Dec-26 run rate: PO steps up for {lifts_po} lifts / {trays_po} trays (DeploySum: {f0(lifts_ds)} / {f0(trays_ds)}).",
     f"Sep-26 run rate + DeploySum Oct-Dec 26 vintages: {eff(F['i31_short'])}. If PO's Dec-26 step-up ({f0(dec_l)} lifts, {f0(dec_t)} trays) is Jan-27 units already in the Jan-27 vintage and PO's Oct/Nov counts are right: {eff(F['i31_double'])}. Keep as is: 0.",
     "User, after the PO owner says what the Q4-26 step-ups are"],
    ["3", "SlipLift peripherals: GL and useful life", "I-33",
     f"5020 Robot Peripherals, {f0(di['life_periph'])} months: {f0(F['i33_new_periph'])} of 2027 depreciation (builder assumption, A-10/A-11).",
     f"GL 5011 instead of 5020: 0 (moves {f0(F['i33_new_periph'])} from PO row 22 to row 20). Life 60 months: {eff(F['i33_life60'])}. Life {f0(di['life_tray'])} months: {eff(F['i33_life_tray'])}.",
     "User"],
    ["4", "Revenue split across 4100 / 4500 / 4900", "I-01 (A-02, A-03)",
     f"All {f0(F['rev_fy27'])} of plan revenue on 4100; 4500 and 4900 = 0 (orchestrator assumption).",
     f"Split the plan revenue across the three lines: 0 (classification only; gross margin unchanged). Budget implementation / one-time revenue in addition to the plan: not determinable (2026 4500 + 4900: {f0(F['rev_4500_4900_2026'])}).",
     "User / Finance"],
]

# ------------------------------------------------------------------ 2. Headline (renamed)
HL = [("Revenue", "Revenue (company recognized revenue, 9/30/26 sales plan)", "16"),
      ("COGS", "COGS (COO departments)", "63"),
      ("Depreciation", "  of which depreciation (in COGS)", "19-22"),
      ("Gross Profit", "Gross Profit", "64"),
      ("Opex", "Opex (COO departments)", "116"),
      ("Net Ordinary Income", "COO contribution before other income (workbook label 'Net Ordinary Income')", "117"),
      ("Net Other Income", "Net Other Income", "131"),
      ("Net Income", "**COO contribution** (workbook label 'Net Income')", "132")]
H4 = F4["headline"]
hl_md = ["| Line | COO P&L row | 2026 (N) | 2027 v5 (AG) | Change | % | 2027 v4 (AG) | v5 - v4 |", "|---|---|---:|---:|---:|---:|---:|---:|"]
for k, lab, row in HL:
    n, ag = H[k]["N"], H[k]["AG"]
    hl_md.append(f"| {lab} | {row} | {f0(n)} | {f0(ag)} | {f0(ag - n)} | {pct_nm(ag, n)} | {f0(H4[k]['AG'])} | {f0(ag - H4[k]['AG'])} |")
nm_rows = [lab for k, lab, row in HL if pct_nm(H[k]["AG"], H[k]["N"]) == "n/m"]

# ------------------------------------------------------------------ 3. Caveat block
CAV_HDR = ["Item", "Direction", "What could happen", "Effect on 2027 COO contribution", "Contribution after this item alone", "Source cells"]
CAV = [
    ["I-17", "downside", "Logistics & warehouse payroll (SD model) is not in PO 5100; if PO's typed production payroll excludes the warehouse team, PO is understated.",
     -F["i17"], C - F["i17"], f"SD Logistics&WH Payroll!S{F['i17_row']} (not carried)"],
    ["I-05", "downside", f"Production payroll model 'Total lift payroll' {f0(F['i05_model'])} vs PO 5100 typed {f0(F['i05_po'])}; gap if the model is right (lift payroll only; tray and supervisor rows do not compute in LibreOffice). May overlap I-17.",
     -F["i05"], C - F["i05"], "Prod Payroll!S41; PO!AG36"],
    ["I-10", "downside", "FO/FE lines with 2026 spend budgeted at 0 for 2027 (5920 software, 6610 SG&A salaries, 7200 contractors); effect if they continue at the 2026 level.",
     -F["i10"], C - F["i10"], "FO!N58, N67, N91; FE!N91 (AG = 0)"],
    ["I-26", "RESOLVED", f"RESOLVED (user-confirmed 2026-10-09): Head of Service Delivery salary {f0(I26['salary'])}/year entered in v5 and now inside the headline "
     f"(2027 cost {f0(I26['total_2027'])}: salary {f0(I26['salary_2027'])} + payroll tax {f0(I26['tax_2027'])} + benefits {f0(I26['ben_2027'])}; v4 contribution was {f0(C4)}). No remaining exposure.",
     "0 (now in the headline)", C, "Fld Eng Budget!B21 = " + f0(I26["salary"])],
    ["I-31", "two-way", f"Shortfall if DeploySum's Q4-26 go-lives are right ({f0(lifts_ds - lifts_po)} lifts, {f0(trays_ds - trays_po)} trays more than PO's run rate).",
     F["i31_short"], C + F["i31_short"], "PO!J20:M21; DeploySum!C19:E20"],
    ["I-31", "two-way", f"Double count if PO's Dec-26 step-up ({f0(dec_l)} lifts, {f0(dec_t)} trays; DeploySum Dec-26 go-lives 0) is Jan-27 units ({f0(jl)} lifts, {f0(jt)} trays go live Jan-27, built Nov-26). Excludes the 5020 Dec step ({eff(F['i31_double_5020'])} more if it is the same units).",
     F["i31_double"], C + F["i31_double"], "PO!L20:M21; DeploySum!E19:F20"],
    ["I-32", "upside", "SlipBot fleet fully depreciated or retired from Jan-27 (5010 = 0).",
     F["i32_full"], C + F["i32_full"], "PO!M19; 'Depreciation Schedule'!B21"],
    ["I-32", "upside", f"Trend alternative: 5010 keeps falling at the 2026 rate ({f0(i32['jan'])} Jan-26 -> {f0(i32['sep'])} Sep-26, {f0(i32['slope_jan_sep'])}/month).",
     F["i32_trend"], C + F["i32_trend"], "PO!B19, J19, M19"],
    ["I-32", "upside", f"Trend alternative continued from Sep-26: the same {f0(i32['slope_jan_sep'])}/month decline also runs through Oct-Dec 26, so Jan-27 starts 4 months below Sep-26 "
     f"({f0(F['i32_trend_sep_path']['jan27'])} in Jan-27, {f0(F['i32_trend_sep_path']['dec27'])} in Dec-27; floored at 0, {F['i32_trend_sep_path']['floored_months']} months at the floor).",
     F["i32_trend_sep"], C + F["i32_trend_sep"], "PO!B19, J19, M19"],
    ["I-33", "two-way", "Peripherals life 60 months instead of 84 (a longer life, e.g. 120 months, gives the opposite sign).",
     F["i33_life60"], C + F["i33_life60"], "'Depreciation Schedule'!B11"],
    ["A-14", "upside", "Depreciation convention: mid-month in the go-live month instead of a full month.",
     -F["sens_mid_month"], C - F["sens_mid_month"], "'Depreciation Schedule'!B13"],
    ["A-14", "upside", "Depreciation convention: start the month after go-live.",
     -F["sens_next_month"], C - F["sens_next_month"], "'Depreciation Schedule'!B13 = 1"],
    ["A-22", "downside", f"Revenue rests on unsigned / forecast bookings (Sep-Dec 26 includes {f0(F['unsigned_sep_dec26'])} unsigned at 100%). Revenue effect not determinable from the workbook.",
     None, None, "DeploySum!A49 (note 5), row 40"],
]
cav_md = ["| " + " | ".join(CAV_HDR) + " |", "|---|---|---|---:|---:|---|"]
for it, d, what, e, a, src in CAV:
    cav_md.append(f"| {it} | {d} | {what} | {'n/d' if e is None else (e if isinstance(e, str) else eff(e))} | {'n/d' if a is None else f0(a)} | {src} |")

# sign-flip statement, built from the numbers (v5: generic wording; N2 range label)
alone_flip = [k for k in ("I-05", "I-17", "I-10", "I-31") if flip[k]]
alone_keep = [k for k in ("I-05", "I-17", "I-10", "I-31") if not flip[k]]
assert C > 0
s1 = (f"The 2027 COO contribution of {f0(C)} changes sign on " +
      " or ".join(f"{k} alone ({f0(C)} - {f0(C - after[k])} = {f0(after[k])})" for k in alone_flip) + "." if alone_flip
      else f"No single quantified downside changes the sign of the {f0(C)} contribution.")
if alone_keep:
    s1 += " " + "; ".join(f"{k} alone leaves {f0(after[k])}" for k in alone_keep) + "."
s2 = (f"Together, I-17 + I-05 take it to {f0(F['after_i17_i05'])} (if they do not overlap; the PO owner must say). "
      f"I-10 with the I-31 shortfall gives {f0(F['after_i10_i31'])}. "
      f"All quantified downsides together (I-17, I-05, I-10, I-31 shortfall): {f0(F['after_all_down'])}.")
s3 = (f"Upside: I-32 can add up to {f0(F['i32_full'])} (contribution {f0(F['upside_full'])}); the trend alternative adds {f0(F['i32_trend'])} ({f0(F['upside_trend'])}), "
      f"or {f0(F['i32_trend_sep'])} ({f0(F['upside_trend_sep'])}) if the decline also ran through Oct-Dec 26. "
      f"With costs held fixed, revenue {f0(C)} ({F['rev_breakeven_pct'] * 100:.1f}%) below plan also takes the contribution to zero.")
RANGE_LABEL = "illustrative extremes of quantified items; excludes I-02, A-22; lower end assumes no I-05/I-17 overlap"
s4 = (f"Conclusion: the sign of the 2027 COO contribution is not established by this budget. Treat {f0(C)} as a point estimate inside a range from "
      f"{f0(F['after_all_down'])} to {f0(F['upside_full'])} ({RANGE_LABEL}; lower end = all four quantified downsides added: I-17, I-05, I-10, I-31 shortfall; "
      f"upper end = I-32 full only, the other upsides A-14, I-31 double count and I-33 are not added) until I-17, I-05 and I-32 are answered.")
assert len(alone_flip) >= 1 and F["after_i17_i05"] < 0 and F["upside_full"] > 0   # the conclusion above depends on these
SIGN = [s1, s2, s3, s4]
# the same statement on v4's numbers, for the change log (what the v4 statement said, recomputed)
SIGN4_FLIPS = [k for k in ("I-05", "I-17", "I-10", "I-31") if F4["flip_alone"][k]]

CAV1 = (f"(1) What the figure is. The bottom line, {f0(C)}, is a **COO contribution**: the company's recognized revenue ({f0(rev)}, all of it) "
        f"less the costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: {f0(cost27)}). Costs outside COO (for example sales, G&A, R&D) "
        f"are not in this workbook, so it is **not company Net Income**. The workbook row keeps its GL label 'Net Income' (COO P&L!A132) because v4 and v5 change no label on the P&L tabs; "
        f"the notes and Collation Notes call it 'COO contribution'.")
CAV2 = (f"(2) What the revenue is. 2027 revenue is the 9/30/26 sales plan's recognized revenue (DeploySum row 40, static cached values, A-24), not signed contracts. "
        f"It includes unsigned and forecast bookings: Sep-Dec 26 bookings of {f0(F['bookings_sep_dec26'])} include {f0(F['unsigned_sep_dec26'])} of unsigned forecast at 100% "
        f"(DeploySum note 5, A49: bookings are gross ACV), and all {f0(F['bookings_fy27'])} of FY27 bookings are forecast (new logos {f0(F['bookings_fy27_newlogo'])}, expansion {f0(F['bookings_fy27_expansion'])}). "
        f"{f0(F['rev_above_exit'])} ({F['rev_above_exit_pct'] * 100:.0f}%) of 2027 revenue is above the Dec-26 exit rate x 12 ({f0(F['rev_exit_runrate_x12'])}), so it depends on go-lives that have not happened yet.")
CAV3 = "(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. Items can overlap (I-05 and I-17 both concern production payroll), so do not add them without the owners' answers."

# ------------------------------------------------------------------ 4. issue edits (O1, O2, O3, O6, B1)
def set_issue(i, **kw):
    row = iss[i]
    for k, v in kw.items():
        row[IHDR.index(k)] = v

# O6: I-02 restated in cost terms (v2 evidence quoted Net Income before revenue was budgeted)
drivers = iss["I-02"][4].split("Drivers:")[1].strip()
set_issue("I-02",
          **{"Location (sheet!cell)": "FO!AG63; FO!AG116; FE!AG63; FE!AG116; COO P&L!AG132",
             "Finding": f"Replacing FO and FE with the SD versions adds {f0(i02['delta'])} to 2027 COO cost (COGS + Opex). The SD build is much heavier than the COO book's FO/FE. (v4: restated in cost terms; the earlier evidence quoted 2027 Net Income from before revenue was budgeted.)",
             "Evidence": f"FO cost (AG63 + AG116): COO book {f0(i02['FO_coo'])} -> SD {f0(i02['FO_sd'])}; FE: COO book {f0(i02['FE_coo'])} -> SD {f0(i02['FE_sd'])}; together {f0(i02['FO_coo'] + i02['FE_coo'])} -> {f0(i02['FO_sd'] + i02['FE_sd'])}. With the COO book's FO/FE, the 2027 COO contribution would be {f0(i02['contribution_with_coo_book'])} instead of {f0(C)}. Drivers: {drivers}",
             "2027 impact": f"{f0(-i02['delta'])} on the contribution",
             "Basis": f"impact {f0(-i02['delta'])}"})
# B1 / I-05: quantify the gap
iss["I-05"][4] = rep(iss["I-05"][4], "Cells read from Prod Payroll by other sheets",
                     f"Gap: {f0(F['i05_model'])} - {f0(F['i05_po'])} = {f0(F['i05'])} (lift payroll only). If the model is right and PO 5100 is the whole production payroll, the 2027 COO contribution falls by at least this gap, which on its own turns it negative ({f0(after['I-05'])}). May overlap I-17. Cells read from Prod Payroll by other sheets")
iss["I-05"][5] = f"not determinable (exposure {f0(F['i05'])}: lift payroll model {f0(F['i05_model'])} vs PO 5100 {f0(F['i05_po'])})"
# O1: I-31 two-way
set_issue("I-31",
          **{"Finding": (f"Oct-Dec 26 go-lives are carried in the PO Dec-26 run rate, not added explicitly. The risk runs both ways. "
                         f"(a) Shortfall: PO steps up for {lifts_po} lifts and {trays_po} trays in Q4-26, DeploySum has {f0(lifts_ds)} and {f0(trays_ds)}; if DeploySum is right the budget is short {f0(-F['i31_short'])}. "
                         f"(b) Possible double count: PO's Dec-26 step-up ({f0(dec_l)} lifts, {f0(dec_t)} trays) has no DeploySum Dec-26 go-live. If these are units DeploySum places in Jan-27 ({f0(jl)} lifts, {f0(jt)} trays, built Nov-26), they sit in both the run rate and the Jan-27 vintage: {f0(F['i31_double'])} too much. "
                         f"If (b) holds and DeploySum's Q4 counts are right, the gross Q4 shortfall is {f0(-F['i31_gross_short_if_double'])} and the net is still {f0(F['i31_short'])}. The 5020 step-ups cannot be reproduced from DeploySum's peripheral cost."),
             "2027 impact": f"{eff(F['i31_short'])} to {eff(F['i31_double'])} (5020 Dec step: up to {eff(F['i31_double_5020'])} more)",
             "Basis": f"impact {f0(max(-F['i31_short'], F['i31_double']))} (< $50k)",
             "Recommended action": "PO owner to say what the Oct/Nov/Dec-26 step-ups on PO rows 20-22 are (which go-lives, which month). Then the user chooses: keep the PO run rate (current), or Sep-26 run rate + DeploySum Oct-Dec 26 vintages. Do not do both."})
iss["I-31"][4] = rep(iss["I-31"][4], "Gap not budgeted:", f"Dec-26 step-ups with no DeploySum Dec-26 go-live: {f0(dec_l)} lifts x {f2(di['m_lift'])} + {f0(dec_t)} trays x {f2(di['m_tray'])} = {f2(F['i31_double'] / 12)}/month, {f0(F['i31_double'])} for 2027. Gap not budgeted:")
# O2, O3: I-32 attribution, trend alternative, 5020 base
iss["I-32"][3] = rep(iss["I-32"][3], "for all 12 months of 2027, as the handoff instructed.",
                     "for all 12 months of 2027. The flat carry is a builder assumption (A-17): the brief asked for the PO 2026 monthly depreciation as the existing-fleet input, not for a flat carry.")
iss["I-32"][3] += (f" Trend alternative: 5010 fell through 2026 ({f0(i32['jan'])} Jan -> {f0(i32['sep'])} Sep, {f0(i32['slope_jan_sep'])}/month); continuing that decline through 2027 from the Sep-26 level lowers depreciation by {f0(F['i32_trend'])} "
                   f"({f0(F['i32_trend_actuals'])} on the Jan-Aug actuals trend, {f0(i32['slope_jan_aug'])}/month); if the decline also runs through Oct-Dec 26 (floored at 0) it lowers it by {f0(F['i32_trend_sep'])} ({f0(F['i32_trend_sep_actuals'])} on the actuals trend). The 5020 base ({f0(F['i32_5020_jan26'])} in Jan-26, when 5011 was {f0(F['i32_5011_jan26'])}) predates SlipLift depreciation, so it is probably SlipBot-related and may share the SlipBot end-of-life risk ({f0(F['i32_5020_base_x12'])} for 2027 at that rate).")
iss["I-32"][5] = f"up to {eff(F['i32_full'])} (5010 = 0); trend {eff(F['i32_trend'])} (continued from Sep-26: {eff(F['i32_trend_sep'])}); 5020 base up to {eff(F['i32_5020_base_x12'])}"
iss["I-32"][7] = rep(iss["I-32"][7], "USER DECISION: confirm SlipBot fleet status (fully depreciated / retired / ongoing)",
                     "USER DECISION: confirm SlipBot fleet status (fully depreciated / retired / ongoing / declining as in 2026)")
# I-07: attribution of the flat carry
iss["I-07"][3] = rep(iss["I-07"][3], "Existing fleet = PO Dec-26 run rate, carried flat.", "Existing fleet = PO Dec-26 run rate, carried flat (builder assumption, A-17).")
# v5: I-26 resolved by the user's answer (salary entered in B21)
v4_i26 = list(iss["I-26"])
assert v4_i26[1] == "MED", v4_i26
set_issue("I-26",
          **{"Sev": "RESOLVED",
             "Finding": (f"RESOLVED (user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). v5 enters {f0(I26['salary'])} in Fld Eng Budget!B21, the designated input cell. "
                         f"Was (v4, MED): 'Head of Service Delivery – Rasheen Henry' had no salary entered, so FE 6610 carried $0 for this current employee."),
             "Evidence": (f"Fld Eng Budget!B21 = {f0(I26['salary'])}; row 67 uses the roster formula of rows 59-66 ({I26['formula_b67'][:60]}...): start {I26['start']} (C21) so {I26['months_paid']} months paid, "
                          f"{f2(I26['monthly_pre'])}/month, +{I26['raise_pct'] * 100:.0f}% from {I26['raise_month']} (B24, B25) for {I26['months_raised']} months ({f2(I26['monthly_post'])}/month): 2027 salary {f0(I26['salary_2027'])}; "
                          f"payroll tax {I26['tax_pct'] * 100:.1f}% (B22) {f0(I26['tax_2027'])}; benefits {I26['ben_pct'] * 100:.1f}% (B23) {f0(I26['ben_2027'])}; total {f0(I26['total_2027'])}. "
                          f"FE!AG67 {f0(SGA4['6610']['FE_AG'])} -> {f0(SGA['6610']['FE_AG'])}."),
             "2027 impact": f"{eff(-I26['total_2027'])} on the contribution (in the v5 headline)",
             "Basis": "resolved; was MED (owner confirmation)",
             "Recommended action": "None. Confirm at sign-off that the Head of Service Delivery is not also budgeted on CO or PE (I-28)."})
# v5: I-28 quotes FE SG&A payroll; refresh the FE amounts (each must occur exactly once in the row)
for gl in ("6610", "6630", "6640"):
    iss["I-28"][4] = rep(iss["I-28"][4], f"FE {f0(SGA4[gl]['FE_AG'])},", f"FE {f0(SGA[gl]['FE_AG'])},")
sev_count = collections.Counter(r[1] for r in iss.values())

# ------------------------------------------------------------------ 5. register edits (O3, O4, O5) and new lines
regd = collections.OrderedDict((r[0], r) for r in reg)
regd["A-14"][2] = rep(regd["A-14"][2], "sensitivity: 1-month delay lowers 2027 by 274,833",
                      f"sensitivity: 1-month delay lowers 2027 depreciation by {f0(-F['sens_next_month'])}; mid-month convention lowers it by {f0(-F['sens_mid_month'])}")
regd["A-17"][2] = f"{regd['A-17'][2]}; trend alternative on 5010 {eff(F['i32_trend'])} to the contribution"
regd["A-18"][1] = "Oct-Dec 26 go-lives covered by the PO run rate, not added explicitly; the risk runs both ways"
regd["A-18"][2] = f"{eff(F['i31_short'])} if DeploySum's Q4 counts are right; {eff(F['i31_double'])} if PO's Dec-26 step-ups are Jan-27 units"
regd["A-18"][4] = "builder decision between the brief's two options; PO owner to confirm what the step-ups are (I-31)"
regd["A-19"][4] = rep(regd["A-19"][4], "orchestrator instruction to carry;", "builder assumption (flat carry, A-17);")
regd["A-22"] = ["A-22", "Revenue includes unsigned and forecast bookings, taken at 100%",
                f"Sep-Dec 26 bookings {f0(F['bookings_sep_dec26'])} incl. {f0(F['unsigned_sep_dec26'])} unsigned; FY27 bookings {f0(F['bookings_fy27'])} all forecast",
                "DeploySum!A49 (note 5); DeploySum rows 7-13, 40", "source: 9/30/26 sales plan; no probability weighting applied (builder: taken as given)"]
regd["A-23"] = ["A-23", "Existing-fleet base is the PO Dec-26 forecast, not an actual",
                f"{f2(sum(RR.values()))}/month (PO!M19:M22; Sep-Dec 26 are forecast columns J:M; actuals run to Aug-26)",
                "'Depreciation Schedule'!B21:B24", "builder note (PO 2026 file); refresh when Q4-26 actuals close"]
regd["A-24"] = ["A-24", "DeploySum F40:Q40 (2027 revenue) are static cached values from the 9/30/26 file, not live links",
                f"{F['ds40_static_values']} of 12 months static; PO!U12:AF12 link to them (formulas)",
                "DeploySum!F40:Q40 -> PO!U12:AF12", "build v3 (external workbook [1] not supplied); a plan change needs a new resolved export"]
regd["A-25"] = ["A-25", "Revenue start timing vs go-live: revenue follows the plan's own recognition timing; depreciation starts in the go-live month (A-14)",
                "not determinable: the workbook cannot show whether revenue starts in the go-live month",
                "DeploySum row 40 vs rows 19/20; 'Depreciation Schedule'!B13", "builder note; plan owner to confirm (Revenue Roll-up not supplied)"]
regd["A-17"][2] = f"{regd['A-17'][2]} ({eff(F['i32_trend_sep'])} if the decline also ran through Oct-Dec 26)"
regd["A-26"] = ["A-26", "Head of Service Delivery annual salary (current employee), entered in v5",
                f"{f0(I26['salary'])}/year in B21; model: full year from {I26['start']}, +{I26['raise_pct'] * 100:.0f}% from {I26['raise_month']}, tax {I26['tax_pct'] * 100:.1f}%, benefits {I26['ben_pct'] * 100:.1f}%: 2027 cost {f0(I26['total_2027'])}",
                "Fld Eng Budget!B21 -> rows 67-71, 78-80 -> FE rows 67-69", "user-confirmed 2026-10-09 ('Head of Service delivery salary is $205k annually'); treatment = existing workbook logic"]
reg = list(regd.values())
RHDR = ["ID", "Assumption", "Value / effect", "Where", "Source"]

# ------------------------------------------------------------------ 6. variance scan with n/m (O8), regenerated (v5)
# Rule (reproduces the v3/v4 list exactly on v4): rows of FO, PO, CO, FE, PE, COO P&L with |AG - N| > 50,000 and
# (N = 0 or |AG - N| / |N| > 50%), empty cells as 0, label from column A.
wb4v = openpyxl.load_workbook(V4_XLSX, data_only=True)
wb5v = openpyxl.load_workbook(V5_XLSX, data_only=True)
wb5f = openpyxl.load_workbook(V5_XLSX)
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)


def var_scan(wb):
    out = []
    for s_ in ("FO", "PO", "CO", "FE", "PE", "COO P&L"):
        ws = wb[s_]
        for r in range(1, ws.max_row + 1):
            n, ag = ws[f"N{r}"].value, ws[f"AG{r}"].value
            if not (isnum(n) or isnum(ag)): continue
            n = n if isnum(n) else 0; ag = ag if isnum(ag) else 0
            d = ag - n
            if abs(d) > 50000 and (n == 0 or abs(d / n) > 0.5):
                out.append(f"| {s_} | {r} | {ws[f'A{r}'].value} | {f0(n)} | {f0(ag)} | {f0(d)} | {pct_nm(ag, n)} |")
    return out


var_body = SEC["Issues (v3)"].split("### Variance scan")[1]
v3_rows = [ln for ln in var_body.splitlines() if re.match(r"\| (COO P&L|FO|PO|CO|FE|PE) \| \d+ \|", ln)]
v4_rows = var_scan(wb4v)
assert [x.rsplit("|", 2)[0] for x in v4_rows] == [x.rsplit("|", 2)[0] for x in v3_rows], "variance generator does not reproduce the v4 list"
var_rows = var_scan(wb5v)
var_md = ["| Sheet | Row | Line | 2026 N | 2027 AG | Change | % |", "|---|---:|---|---:|---:|---:|---:|"] + var_rows
nvar = len(var_rows); nnm = sum(1 for x in var_rows if x.endswith("| n/m |"))
var_added = [x for x in var_rows if x.split(" | ")[:2] not in [y.split(" | ")[:2] for y in v4_rows]]
var_changed = [x for x in var_rows if x not in v4_rows and x not in var_added]
var_removed = [x for x in v4_rows if x.split(" | ")[:2] not in [y.split(" | ")[:2] for y in var_rows]]

# ------------------------------------------------------------------ 7a. v5 figures used in several places
d_sal = {gl: SGA[gl]["FE_AG"] - SGA4[gl]["FE_AG"] for gl in ("6610", "6630", "6640")}
d_coo = {gl: SGA[gl]["COO_AG"] - SGA4[gl]["COO_AG"] for gl in ("6610", "6630", "6640")}
dC = C - C4
assert abs(dC + I26["total_2027"]) < 1e-6, (dC, I26["total_2027"])            # contribution moves by exactly the new cost
assert all(abs(d_sal[g] - d_coo[g]) < 1e-6 for g in d_sal)                        # COO P&L rows move with FE
assert abs(d_sal["6610"] - I26["salary_2027"]) < 1e-6 and abs(d_sal["6630"] - I26["tax_2027"]) < 1e-6 and abs(d_sal["6640"] - I26["ben_2027"]) < 1e-6
n_patched = len(PT["values"])
by_sheet_patched = collections.Counter(x[0] for x in PT["values"])
SAL_LINES = [
    f"Input: Fld Eng Budget!B21 = {f0(I26['salary'])} (annual salary, user-confirmed 2026-10-09: 'Head of Service delivery salary is $205k annually'). This is the only typed input that changed; no formula, label or other cell was edited.",
    f"How the model treats it: row 67 uses the same formula as the other roster rows ({I26['formula_b67']}). Start month C21 = {I26['start']}, so all {I26['months_paid']} months of 2027 are paid: "
    f"{f2(I26['monthly_pre'])}/month Jan-Sep, then +{I26['raise_pct'] * 100:.0f}% (Fld Eng Budget!B24 = Fld Ops Payroll M5 = Prod Payroll M5) from {I26['raise_month']} (B25 = Fld Ops Payroll M6 = Prod Payroll M6) = {f2(I26['monthly_post'])}/month for {I26['months_raised']} months. "
    f"No raise-eligibility test applies on this tab (I-29); the salary is treated as the Dec-26 rate.",
    f"Burden: payroll taxes {I26['tax_pct'] * 100:.1f}% (B22 = Fld Ops Payroll B7) and benefits {I26['ben_pct'] * 100:.1f}% (B23 = Fld Ops Payroll B8), applied to the salary rows total (rows 69-70).",
    f"2027 cost of the role: salary {f0(I26['salary_2027'])} + payroll tax {f0(I26['tax_2027'])} + benefits {f0(I26['ben_2027'])} = {f0(I26['total_2027'])}.",
    f"FE 2027 (AG): 6610 {f0(SGA4['6610']['FE_AG'])} -> {f0(SGA['6610']['FE_AG'])} (+{f0(d_sal['6610'])}); 6630 {f0(SGA4['6630']['FE_AG'])} -> {f0(SGA['6630']['FE_AG'])} (+{f0(d_sal['6630'])}); "
    f"6640 {f0(SGA4['6640']['FE_AG'])} -> {f0(SGA['6640']['FE_AG'])} (+{f0(d_sal['6640'])}). FE Total - Expense {f0(F4['fe_opex'])} -> {f0(F['fe_opex'])}. COO P&L rows 67-69 move by the same amounts.",
    f"2027 COO contribution (COO P&L AG132): {f0(C4)} (v4) -> {f0(C)} (v5), {f0(dC)}. 2026 FE 6610 was {f0(SGA['6610']['FE_N'])}; FE 6610 2027 is now {f0(SGA['6610']['FE_AG'])} ({pct_nm(SGA['6610']['FE_AG'], SGA['6610']['FE_N'])} vs 2026; v4 {pct_nm(SGA4['6610']['FE_AG'], SGA4['6610']['FE_N'])}).",
]
N1_LINE = ("Depreciation Schedule tab text superseded (critic v4 N1): the explanatory text at 'Depreciation Schedule'!B17 ('In run rate', with its note in D17: 'Never both'), D21 and the "
           "row 19 heading ('... carried flat') predates the v4 review and is replaced by A-17, A-18, A-19 and I-31 on this sheet: the flat carry is a builder assumption (A-17, A-19), and the "
           "Q4-26 treatment is a two-way risk awaiting the PO owner (A-18, I-31), not a settled 'never both' rule. The tab text was not edited, so that no cell other than Fld Eng Budget!B21 changes in v5.")
# sign-flip in v4 (recomputed from v4 figures, for the change log)
SF4 = (f"v4: {C4:,.0f} flipped on {' or '.join(SIGN4_FLIPS)} alone; range {f0(F4['after_all_down'])} to {f0(F4['upside_full'])}")
SF5 = (f"v5: {C:,.0f} flips on {' or '.join(alone_flip)} alone; range {f0(F['after_all_down'])} to {f0(F['upside_full'])}")

# ------------------------------------------------------------------ 7b. carried tables regenerated from the workbook (each must reproduce v4 on v4)
wb4f = openpyxl.load_workbook(V4_XLSX)
car = SEC["Carried from v2 (still valid: FO, FE, CO, PE and PO payroll unchanged)"]
car = rep(car, "### Cross-department overlap (from v2)", "### Cross-department overlap")
car = rep(car, "### Raise timing consistency (O10)", "### Raise timing consistency")
car = rep(car, "### Logistics & Warehouse payroll (O2) and MeLi (O3)", "### Logistics & Warehouse payroll and MeLi")
old_trace = re.search(r"Rates and timing only, no headcount and no cost:.*\n", car).group(0)
pp = F["prodpay"]
car = rep(car, old_trace,
          (f"Rates and timing only: other sheets read only these typed raise inputs from Prod Payroll, never a headcount or cost cell. "
           f"Prod Payroll now partly computes (v3 resolved DeploySum): 'Total lift payroll' S41 = {f0(F['i05_model'])}, but {pp['errors']} cells are errors ({', '.join(f'{k} {v}' for k, v in pp['codes'].items())}; XLOOKUP rows that LibreOffice cannot evaluate, see I-05), out of {pp['formulas']} formulas. "
           f"PO 5110-5140 2027 (PO!U33:AF35) are typed values with no link to any tab, so PO AG33 {f0(F['po_ag33'])} and FO 5510 share no headcount source: no double count through Prod Payroll. "
           f"The open question is the reverse: the model's lift payroll exceeds PO 5100 ({f0(F['i05_po'])}) by {f0(F['i05'])} (I-05).\n"))
DEPTS = ("FO", "PO", "CO", "FE", "PE")


def xdept_cells(wb, r):
    vals = [wb[s_][f"AG{r}"].value for s_ in DEPTS] + [wb["COO P&L"][f"AG{r}"].value]
    return ["" if (v is None or (isnum(v) and abs(v) < 0.5)) else f0(v) for v in vals]


def regen_xdept(text, wb_old, wb_new):
    out = []; changed = 0
    for ln in text.split("\n"):
        m = re.match(r"\| (\d+) \| ", ln)
        if m and ln.count(" | ") >= 10:
            r = int(m.group(1)); cells = ln.split(" | ")
            assert cells[2:8] == xdept_cells(wb_old, r), (r, cells[2:8], xdept_cells(wb_old, r))
            new = cells[:2] + xdept_cells(wb_new, r) + cells[8:]
            changed += new != cells
            ln = " | ".join(new)
        out.append(ln)
    return "\n".join(out), changed


def steps(wb, s_, r):
    xs = [wb[s_].cell(r, c).value for c in range(21, 33)]                  # U..AF
    out = []
    for k in range(1, 12):
        a_, b_ = xs[k - 1], xs[k]
        if isnum(a_) and isnum(b_) and a_ != 0 and abs(b_ / a_ - 1) > 1e-9:
            out.append(f"{openpyxl.utils.get_column_letter(21 + k)}: {(b_ / a_ - 1) * 100:.2f}%")
    return ", ".join(out)


def regen_steps(text, wb_old, wb_new):
    out = []; changed = 0
    for ln in text.split("\n"):
        m = re.match(r"\| (PO|CO|FE|PE|FO) \| (\d+) \| (.*?) \| (True|False) \| (.*) \|$", ln)
        if m:
            s_, r = m.group(1), int(m.group(2))
            assert m.group(5) == steps(wb_old, s_, r), (ln, steps(wb_old, s_, r))
            new = f"| {s_} | {r} | {m.group(3)} | {m.group(4)} | {steps(wb_new, s_, r)} |"
            changed += new != ln; ln = new
        out.append(ln)
    return "\n".join(out), changed


xd_head, xd_rest = car.split("### Cross-department overlap", 1)
xd_body, xd_tail = xd_rest.split("**Prod Payroll trace", 1)
xd_body, n_xd = regen_xdept(xd_body, wb4v, wb5v)
xd_body = rep(xd_body, "a current employee with no salary (I-26).",
              f"the current employee with no salary in v4 (I-26) has a salary from v5 (Fld Eng Budget!B21 = {f0(I26['salary'])}).")
car = xd_head + "### Cross-department overlap" + xd_body + "**Prod Payroll trace" + xd_tail
rt_head, rt_rest = car.split("### Raise timing consistency", 1)
rt_body, rt_tail = rt_rest.split("### Logistics & Warehouse payroll and MeLi", 1)
rt_body, n_rt = regen_steps(rt_body, wb4v, wb5v)
car = rt_head + "### Raise timing consistency" + rt_body + "### Logistics & Warehouse payroll and MeLi" + rt_tail
CARRIED_REGEN = {"variance": [len(var_added), len(var_changed), len(var_removed)], "xdept_rows_changed": n_xd, "raise_rows_changed": n_rt}

# ------------------------------------------------------------------ 7c. change log v4 -> v5
CHG = [
    ["I-26", "Head of Service Delivery salary (user-confirmed 2026-10-09)",
     f"Fld Eng Budget!B21 = {f0(I26['salary'])}. Existing row-67 mechanics apply (full year from {I26['start']}, +{I26['raise_pct'] * 100:.0f}% from {I26['raise_month']}, tax {I26['tax_pct'] * 100:.1f}%, benefits {I26['ben_pct'] * 100:.1f}%): "
     f"FE 6610 +{f0(d_sal['6610'])}, 6630 +{f0(d_sal['6630'])}, 6640 +{f0(d_sal['6640'])}; COO contribution {f0(C4)} -> {f0(C)} ({f0(dC)}). I-26 marked RESOLVED.",
     "Fld Eng Budget!B21; FE / COO P&L rows 67-69 and subtotals (recalculated); I-26; caveat table; Headline"],
    ["Recalc", "Downstream values",
     f"{n_patched} cached values recalculated, all downstream of B21 by static trace ({', '.join(f'{k} {v}' for k, v in sorted(by_sheet_patched.items()))}); 0 formulas changed.",
     "v4 -> v5 diff"],
    ["Sign flip", "Recomputed on the new contribution", f"{SF4}. {SF5}.", "Sign-flip statement"],
    ["N1", "Depreciation Schedule tab text conflicts with A-17/A-19 and I-31",
     "Collation Notes line added: the tab text at B17 (with D17), D21 and the row 19 heading is superseded by A-17, A-18, A-19 and I-31. Tab text not edited (only B21 may change in v5).",
     "Collation Notes 'Workbook text superseded'; Depreciation schedule summary"],
    ["N2", "Sign-flip range is illustrative", f"Range labelled '{RANGE_LABEL}', with what each end includes.", "Sign-flip statement (md and Collation Notes)"],
    ["N3", "I-32 trend understated if the decline ran through Oct-Dec 26",
     f"New case: decline continued from Sep-26, floored at 0: {eff(F['i32_trend_sep'])} (vs {eff(F['i32_trend'])} starting from the Sep-26 level in Jan-27; actuals-only slope {eff(F['i32_trend_sep_actuals'])}).",
     "Caveat table; Decisions pending #1; I-32; A-17"],
    ["Carried tables", "Recomputed from the v5 workbook",
     f"Variance scan: {len(var_added)} rows added, {len(var_changed)} changed, {len(var_removed)} removed; cross-department overlap: {n_xd} rows changed; raise-step table: {n_rt} rows changed; I-02 and I-28 FE amounts refreshed. Each generator reproduces the v4 table exactly from v4 first.",
     "Variance scan; Cross-department checks; I-02; I-28"],
]

# ------------------------------------------------------------------ 7d. md assembly
L = []; A = L.append
A("# 02-build notes v5 - 2027 COO budget collation")
A("")
A("## Decisions pending")
A("")
A("Four user decisions are open. The builder has not resolved them; the budget carries the 'current treatment' column. Effects are on the 2027 COO contribution, each on its own.")
A("")
A("| " + " | ".join(DEC_HDR) + " |"); A("|---|---|---|---|---|---|")
for d in DEC: A(mdrow(d))
A("")
A(f"v5 enters one user-confirmed input: the Head of Service Delivery's annual salary, {f0(I26['salary'])}, in Fld Eng Budget!B21 (resolves I-26). Everything else that moved is downstream recalculation. "
  f"The 2027 COO contribution falls from {f0(C4)} (v4) to **{f0(C)}** ({f0(dC)}). "
  + (f"Diff vs v4: {AN['diff']['class']['input_cells']} input cell, {AN['diff']['class']['downstream_value_cells']} downstream value changes, {AN['diff']['class']['outside']} changes outside the downstream set, {AN['diff']['class']['formula_text_diffs']} formula changes; see 'v4 -> v5 diff'."
     if AN else "Diff vs v4: see 'v4 -> v5 diff'."))
A("")
A("## Headline: 2027 COO contribution")
A("")
L.extend(hl_md)
A("")
A(f"- **2027 COO contribution (COO P&L AG132): {f0(C)}** vs 2026 {f0(H['Net Income']['N'])}. Change {f0(C - H['Net Income']['N'])}; % n/m (2026 base negative). It includes 2027 plan revenue of {f0(rev)} (all to 4100, orchestrator assumption) and depreciation of {f0(H['Depreciation']['AG'])}. v4: {f0(C4)}.")
A(f"- Cost-only view: total COO cost (COGS + Opex, AG63 + AG116) {f0(cost27)} vs 2026 {f0(H['COGS']['N'] + H['Opex']['N'])} (change {f0(cost27 - H['COGS']['N'] - H['Opex']['N'])}, {pct_nm(cost27, H['COGS']['N'] + H['Opex']['N'])}). Excluding depreciation: {f0(cost27 - H['Depreciation']['AG'])} vs 2026 {f0(H['COGS']['N'] + H['Opex']['N'] - H['Depreciation']['N'])}.")
A(f"- 2027 gross margin {H['Gross Profit']['AG'] / rev * 100:.1f}% (unchanged: the new cost is Opex). '%' is 'n/m' where the 2026 base is zero or negative or the sign flips: {'; '.join(x.replace('**', '') for x in nm_rows)}.")
A(f"- Issues: {sev_count['HIGH']} HIGH, {sev_count['MED']} MED, {sev_count['LOW']} LOW open; {sev_count['RESOLVED']} RESOLVED (I-26, v5).")
A("")
A("### Caveats on the headline (read before using the figure)")
A("")
A(CAV1); A(""); A(CAV2); A(""); A(CAV3); A("")
L.extend(cav_md)
A("")
A("**Sign-flip statement (computed from the table):** " + " ".join(SIGN))
A("")
A("## Changes from v4")
A("")
A("| Item | Point | What v5 did | Where |"); A("|---|---|---|---|")
for c in CHG: A(mdrow(c))
A("")
A("No critic v4 item was declined. N1 is handled by a superseding note rather than by editing the tab text, because the v5 brief allows only Fld Eng Budget!B21 to change. v4's own changes from v3 (critic v3 B1, O1-O8) are listed in `02-build_notes_v4.md` and still apply.")
A("")
A("## Head of Service Delivery salary (I-26, resolved in v5)")
A("")
for x in SAL_LINES: A(f"- {x}")
A("")
A("## Build and sources")
A("")
A("Output: `02-build/02-build_COO_2027_Budget_Collated_v5.xlsx` (v1-v4 files unchanged)  ")
A("Scripts: `02-build/scripts/` - v5 entry point `run_build_v5.sh`: build_v5.py (stage 1: v4 package with only B21 set) -> recalc.sh (LibreOffice full recalculation of stage 1) -> deps_v5.py (static trace of every formula downstream of B21) -> patches_v5.py "
  "(recalculated values of downstream cells that changed; anything that changed outside the trace stops the build) -> build_v5.py (stage 2: v4 package + B21 + those cached values) -> figures_v5.py -> report_v5.py -> build_v5.py (final, with Collation Notes) -> "
  "diff_versions.py, recalc.sh and analyze_v5.py (checks). Every zip part other than the three patched sheets and Collation Notes is copied byte for byte from v4. `run_build_v4.sh` ... `run_build.sh` still reproduce v4 ... v1.  ")
A(f"Inputs (read-only): `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `{sha(COO)}`; `Service_Delivery_PL_worksheets.xlsx` sha256 `{sha(SD)}`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `{sha(NEW)}`; user answer 2026-10-09 (B21).  ")
A("Reviews: critic `03-review/03-review_critic_v4.md` (N1-N3); verifier `04-verify/04-verify_report_v3.md` (v3 PASS).  ")
A(f"Recalculation engine: {lov} (used to compute the downstream values and to check the result).")
A("")
A("## Completion criteria (v5)")
A("")
if AN:
    d = AN["diff"]; k = d["class"]
    A("| Criterion | Result |"); A("|---|---|")
    A(f"| Only input diff is Fld Eng Budget!B21 = {f0(I26['salary'])} | Input (non-formula) cells changed: {k['input_cells']} ({', '.join(k['input_list'])}). Formulas changed: {k['formula_text_diffs']} (diff_versions.py reports {d['total']['formula_diffs']} 'formula diff' because it compares cell contents and B21 went from empty to a typed number). Comments changed: {d['comments']}. |")
    A(f"| Value changes only downstream of B21 | {k['downstream_value_cells']} value diffs, all in the static downstream set ({k['by_sheet']}); outside the set: {k['outside']}. Recalc noise left at v4 values outside the set: {AN['noise']['noise_outside']['cells']} cells, max {AN['noise']['noise_outside']['max_abs']:.1e} (< 1e-6, not a change). |")
    A(f"| Cached values are what the formulas give | LibreOffice recalculation of v5 vs its stored values, every sheet except Collation Notes: {AN['lo_check']['cells_diff']} cells differ, max {AN['lo_check']['max_abs']:.1e}; non-numeric mismatches {AN['lo_check']['text_mismatch']}. |")
    A(f"| COO P&L = sum of the departments | {AN['coo_sum']['cells']:,} COO P&L cells checked (rows 12 onward, columns B:N and U:AG, ratio rows and columns excluded): max |COO - (FO+PO+CO+FE+PE)| {AN['coo_sum']['max_abs']:.1e}; failures {AN['coo_sum']['fail']}. |")
    A(f"| 0 new errors | New errors vs v4: {len(AN['new_errors'])}. |")
    A(f"| I-26 shows RESOLVED | Issues table Sev = RESOLVED; caveat table row 'RESOLVED'; Collation Notes text check: {AN['cn']['resolved_ok']}. |")
    A(f"| N1-N3 addressed | N1 line on Collation Notes: {AN['cn']['n1_ok']}; N2 range label: {AN['cn']['n2_ok']}; N3 trend case: {AN['cn']['n3_ok']}. |")
    A(f"| Collation Notes live formulas | {AN['cn']['formulas']} formulas; LibreOffice recalc vs stored values: max diff {AN['cn']['max_num_diff']:.1e}, text mismatches {AN['cn']['text_mismatch']}. |")
    A(f"| Figures recompute from the final file | figures_v5.py on the final v5 = on stage 2: {AN['figures_identical']}. |")
    A(f"| No stale v4 numbers | v4 values of every recalculated cell and every changed figure (>= 1,000) searched in this file outside 'Changes from v4' and 'Head of Service Delivery salary': {AN['stale_numbers']['hits']} hits ({AN['stale_numbers']['checked']} numbers checked). |")
else:
    A("(pass 1 placeholder)")
A("")
dep = SEC["Depreciation schedule summary"]
dep = rep(dep, re.search(r"\*\*Decision: rely on the run rate\.\*\*.*\n", dep).group(0),
          (f"**Treatment: rely on the run rate (builder decision; two-way risk, I-31).** Oct-Dec 26 go-lives are not added explicitly. Why: the run rate is PO's own forecast and already contains Q4-26 step-ups priced like the schedule; adding DeploySum's Q4 units on top would count the {lifts_po} lifts and {trays_po} trays already in it twice. "
           f"The risk runs both ways. If DeploySum's Q4 counts are right, the run rate is short {f0(lifts_ds - lifts_po)} lifts / {f0(trays_ds - trays_po)} trays ({f0(-F['i31_short'])} for 2027; memo in schedule section 5). "
           f"If PO's Dec-26 step-up ({f0(dec_l)} lifts, {f0(dec_t)} trays; DeploySum has no Dec-26 go-lives) is units that DeploySum places in Jan-27, they are also in the Jan-27 vintage: {f0(F['i31_double'])} counted twice. PO owner to confirm; user decision (Decisions pending #2).\n"))
dep = rep(dep, "This carries the run rate through 2027 as instructed; it is not evidence that the fleet is still depreciating.",
          f"The flat carry is a builder assumption (A-17), not evidence that the fleet is still depreciating. 5010 fell through 2026 ({f0(i32['slope_jan_sep'])}/month Jan-Sep); continuing that trend would lower 2027 by {f0(F['i32_trend'])}, or by {f0(F['i32_trend_sep'])} if the decline also ran through Oct-Dec 26 (floored at 0).")
A("## Depreciation schedule summary"); A(dep.rstrip()); A("")
A(N1_LINE); A("")
A("## Unit-cost reconciliation"); A(SEC["Unit-cost reconciliation"].rstrip()); A("")
A("## Revenue"); A(SEC["Revenue"].rstrip()); A("")
A(f"Revenue basis (A-22, A-24, A-25): plan figures, not contracts. Sep-Dec 26 bookings {f0(F['bookings_sep_dec26'])} include {f0(F['unsigned_sep_dec26'])} unsigned at 100%; FY27 bookings {f0(F['bookings_fy27'])} are forecast. "
  f"DeploySum!F40:Q40 hold static values ({F['ds40_static_values']} of 12). Dec-26 exit rate {f0(F['rev_dec26_monthly'])}/month x 12 = {f0(F['rev_exit_runrate_x12'])}; the other {f0(F['rev_above_exit'])} of 2027 revenue depends on 2027 go-lives.")
A("")
A("## Assumptions register"); A("")
A("| " + " | ".join(RHDR) + " |"); A("|---|---|---|---|---|")
for r in reg: A(mdrow(r))
A("")
A("A-22..A-25 are new in v4; A-26 is new in v5; A-14, A-17, A-18 and A-19 were edited in v4 (critic O1, O3, O4); A-17 also shows the N3 trend case in v5.")
A("")
A("## DeploySum refresh and tie-out (v3 build; unchanged in v4 and v5)"); A(SEC["DeploySum refresh and tie-out"].rstrip()); A("")
A("## v4 -> v5 diff"); A("")
if AN:
    k = AN["diff"]["class"]
    A("`diff_versions.py` (exact: formulas as text, cached values with no tolerance) on every sheet present in both files except Collation Notes:")
    A("")
    A("| Sheet | Cells | Formula diffs | Value diffs |"); A("|---|---:|---:|---:|")
    for s, x in AN["diff"]["sheets"].items():
        A(f"| {s} | {x['cells']:,} | {x['formula_diffs']} | {x['value_diffs']} |")
    A(f"| **Total** | {AN['diff']['total']['cells']:,} | {AN['diff']['total']['formula_diffs']} | {AN['diff']['total']['value_diffs']} |")
    A("")
    A(f"The one 'formula diff' is Fld Eng Budget!B21 (empty -> {f0(I26['salary'])}, a typed input: diff_versions.py compares cell contents). Cells whose formula text changed: {k['formula_text_diffs']}.")
    A("")
    A(f"Classification of the {AN['diff']['total']['value_diffs']} value diffs: input cells {k['input_cells']} ({', '.join(k['input_list'])}); formula cells downstream of B21 {k['downstream_value_cells']}; anything else {k['outside']}. "
      f"Static trace: {AN['noise']['downstream_total']} formula cells can depend on B21 ({AN['deps']['by_sheet']}); {AN['noise']['downstream_unchanged']} of them did not change value; the Collation Notes ones are regenerated. "
      f"Of the recalculated downstream cells, {AN['noise']['downstream_noise_only_patched']} moved by <= 1e-6 only. "
      f"Recalculation noise outside the trace (left at the v4 value, not a change): {AN['noise']['noise_outside']['cells']} cells, max abs {AN['noise']['noise_outside']['max_abs']:.1e}, sheets {AN['noise']['noise_outside']['by_sheet']}.")
    A("")
    A(f"Comments added / removed / changed: {AN['diff']['comments']}. Sheets only in v4 / only in v5: {AN['diff']['only']}. "
      f"Package: {AN['package']['identical_parts']} of {AN['package']['parts_v4']} parts byte-identical to v4; changed: {', '.join(AN['package']['changed_parts'])}; added: {AN['package']['added_parts'] or 'none'}; removed: {AN['package']['removed_parts'] or 'none'}.")
A("")
A("## Error scan"); A("")
if AN:
    A("| Sheet | v4 | v5 |"); A("|---|---|---|")
    for s, x in AN["errors"].items(): A(f"| {s} | {x['v4'] or 'none'} | {x['v5'] or 'none'} |")
    A(""); A(f"New errors in v5: **{len(AN['new_errors'])}**. Prod Payroll's #NAME? cells are the XLOOKUP rows LibreOffice cannot evaluate (I-05, I-25).")
A("")
A("## Package"); A("")
if AN:
    A(f"Parts {AN['package']['parts_v5']}; `xl/externalLinks/*` **{AN['package']['externalLink_parts']}**; defined names {AN['package']['defined_names_v5']:,} (v4: {AN['package']['defined_names_v4']:,}).")
A("")
A("## Sheets in the output"); A("")
if AN:
    A("| # | Sheet | State |"); A("|---|---|---|")
    for i, (s, st) in enumerate(AN["sheets"], 1): A(f"| {i} | {s} | {st} |")
A("")
A("## Severity scale"); A(SEC["Severity scale"].rstrip()); A("")
A("## Issues (v5)"); A("")
A("Severity per the scale above. v5: I-26 RESOLVED (user-confirmed salary entered); I-32 adds the N3 trend case; I-02 and I-28 quote the recalculated FE amounts. v4 changed the text of I-02 (O6), I-05 (B1), I-07 and I-32 (O2, O3) and I-31 (O1). No other severity changed.")
A(""); A("| " + " | ".join(IHDR) + " |"); A("|---|---|---|---|---|---|---|---|")
for r in iss.values(): A(mdrow(r))
A("")
A("### Variance scan: rows with |AG-N| > $50k and > 50% (recomputed from the v5 workbook)")
A("")
A("'%' = (AG - N) / N; 'n/m' where N is zero or negative, or AG is negative while N is positive. "
  + (f"Rows new in v5: {'; '.join(x.split(' | ')[0][2:] + ' ' + x.split(' | ')[1] + ' ' + x.split(' | ')[2] for x in var_added)}. " if var_added else "No rows new in v5. ")
  + (f"Rows dropped in v5: {'; '.join(x.split(' | ')[0][2:] + ' ' + x.split(' | ')[1] for x in var_removed)}." if var_removed else "No rows dropped."))
A("")
L.extend(var_md)
A("")
A("## Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5)")
A(car.rstrip()); A("")
dec = SEC["Decisions"].rstrip()
A("## Decisions"); A(dec)
for x in [
    "D1 (v4): Patch, do not round-trip. v4 copied the v3 package and rewrote only the Collation Notes part; LibreOffice re-saves change cached values in the last floating-point digit.",
    "D2 (v4): Collation Notes strings are written as inline strings, and existing v3 cell styles are reused, so sharedStrings.xml and styles.xml stay byte-identical (the v3 notes strings remain in sharedStrings.xml, unused).",
    "D3 (v4): Formula cells on Collation Notes store values computed by the figures script; the analyze script checks them against a LibreOffice recalculation.",
    "D4 (v4): '% change' = n/m when the base is zero or negative or the new value is negative with a positive base; the live formula returns text ('n/m' or e.g. '110%') so no new number format is needed.",
    "D5 (v4): The workbook's 'Net Income' label (COO P&L!A132 and dept tabs) is not renamed; the notes and Collation Notes use 'COO contribution'.",
    "D6 (v4): Exposures are shown one at a time against the headline and not netted, because I-05 and I-17 may overlap; combined figures are shown with that caveat.",
    "D7 (v4): The I-32 trend alternative uses the Jan->Sep-26 slope (critic's basis, Sep is the first forecast month) and also shows the Jan->Aug actuals-only slope; each is floored so 5010 cannot go negative.",
    "D8 (v4): Decisions pending are presented, not resolved; the budget keeps the v3 treatment.",
    "D1 (v5): Recalculate with LibreOffice, keep only downstream changes. Stage 1 (v4 + B21) is fully recalculated; a static trace of all formulas lists every cell that can depend on B21; only those cells take the recalculated value (when it differs). Every other cell keeps its v4 bytes, so the v4 -> v5 diff shows exactly the input and its consequences; the build stops if any cell outside the trace moves by more than 1e-6.",
    "D2 (v5): The salary is entered as the annual figure the user gave (205,000) in the designated input cell; the model's own row-67 logic applies unchanged (full year from the C21 start month Jan-27, the tab-wide 3% raise from Oct-27, the tab's tax and benefit rates). No new logic was added. Read as the current (Dec-26) salary, consistent with the other roster rows.",
    "D3 (v5): Workbook text cells that the salary makes out of date are left as they are (only B21 may change). Fld Eng Budget!D21 still says 'Enter annual salary in B21' (now done); the Depreciation Schedule text is superseded by a Collation Notes line (N1).",
    "D4 (v5): N2 label used as given, plus what each end contains, because the upper end is I-32 alone and does not add the other quantified upsides (A-14, I-31 double count, I-33).",
    "D5 (v5): N3 case continues the Jan->Sep-26 slope through Oct-Dec 26, so Jan-27 is 4 slope steps below Sep-26; effect = flat carry (12 x Dec-26 run rate) less the trend path, each month floored at 0. The Dec-26 run rate equals the Sep-26 level in the PO forecast ("
    + ("checked" if F["i32_dec26_eq_sep"] else "NOT equal; see figures") + ").",
    "D6 (v5): Tables carried from v2/v3 that quote workbook values (variance scan, cross-department overlap, raise steps) are regenerated from the v5 workbook by generators that first reproduce the v4 tables exactly from v4.",
]:
    A(f"- {x}")
A("")
A("## Not done / limits")
nd = SEC["Not done / limits"].rstrip()
nd = rep(nd, "No change made to FO, FE, CO, PE, or to PO lines other than 12 and 19-22 (and their subtotals/ratios).",
         "No change made in v3 to FO, FE, CO, PE, or to PO lines other than 12 and 19-22 (and their subtotals/ratios); v5 changes only Fld Eng Budget!B21 (FE payroll and its totals recalculate).")
A(nd)
A("- v4: revenue effect of unsigned/forecast bookings and the revenue-vs-go-live timing (A-22, A-25) cannot be quantified from the workbook; the Revenue Roll-up and 2026 Exist New tabs of the plan were not supplied.")
A("- v5: the explanatory text on the Depreciation Schedule tab (B17/D17, D21, row 19 heading) was not edited; it is superseded by A-17, A-18, A-19 and I-31 (Collation Notes line, N1).")
A("- v5: the workbook cannot confirm the Head of Service Delivery is not also inside CO or PE typed SG&A payroll (I-28 open); the salary is assumed to be the current rate, raised from Oct-27 like the rest of the roster.")
A("- v5: not opened in Microsoft Excel; Excel will show the stored values until it recalculates (they match a LibreOffice recalculation).")
md = "\n".join(L) + "\n"

# stale-text checks
STALE = ["as the handoff instructed", "as instructed;", "before (5,277,004)", "796 of Prod Payroll", "still valid",
         "not added explicitly, so there is no double count", "orchestrator instruction to carry", "(O10)", "(O2)", "(O3)", "2027 v2 (AG)",
         "Changes from v2", "Issues (v3)", "Issues (v4)", "has no salary entered (current employee)", "Fld Eng Budget!B21 (blank)", "notes v4 -", "2027 v4 (AG) |  |"]
md_chk = re.sub(r"(?s)## Changes from v4\n.*?\n## ", "## ", md)
md_chk = re.sub(r"(?s)## Completion criteria \(v5\)\n.*?\n## ", "## ", md_chk)
assert "## Changes from v4" not in md_chk and "## Completion criteria" not in md_chk
for s in STALE:
    assert s not in md_chk, s
for k, lab, row in HL:
    if H[k]["N"] <= 0 or H[k]["AG"] < 0:
        assert pct_nm(H[k]["AG"], H[k]["N"]) == "n/m"
open(OUT_MD, "w").write(md)

# ------------------------------------------------------------------ 8. Collation Notes JSON (independent of ANALYZE_JSON)
CP = "'COO P&L'!"
def fnum(expr, value):
    return {"f": expr, "v": value}
hl_rows = []
for k, lab, row in HL:
    n, ag = H[k]["N"], H[k]["AG"]
    if k == "Depreciation":
        nf, af = f"SUM({CP}N19:N22)", f"SUM({CP}AG19:AG22)"
    else:
        nf, af = f"{CP}N{row}", f"{CP}AG{row}"
    pf = f'IF(OR({nf}<=0,{af}<0),"n/m",TEXT(({af}-{nf})/{nf},"0%"))'
    hl_rows.append([lab.replace("**", ""), row, fnum(nf, n), fnum(af, ag), fnum(f"{af}-({nf})", ag - n),
                    {"f": pf, "v": pct_nm(ag, n), "t": "str"}, round(H4[k]["AG"], 2)])
cav_rows = [[it, d, what, ("n/d" if e is None else (e if isinstance(e, str) else round(e, 2))), ("n/d" if a is None else round(a, 2)), src]
            for it, d, what, e, a, src in CAV]
notes = {"title": "2027 COO Budget - Collation Notes (build v5, draft for review)", "stale_checked": STALE,
         "col_widths": [22, 12, 44, 60, 60, 30, 30, 50],
         "sections": [
             {"heading": "Decisions pending (user) - not resolved by the builder", "style": "highlight",
              "table": {"header": DEC_HDR, "rows": DEC}},
             {"heading": "Headline: 2027 COO contribution (live formulas on COO P&L)",
              "table": {"header": ["Line", "COO P&L row", "2026 (N)", "2027 (AG)", "Change", "% (n/m if base <= 0 or sign flips)", "2027 in v4 (value)"], "rows": hl_rows}},
             {"heading": "Caveats on the headline (read before using the figure)", "style": "highlight",
              "lines": [CAV1.replace("**", ""), CAV2.replace("**", ""), CAV3],
              "table": {"header": CAV_HDR, "rows": cav_rows},
              "after": ["Sign-flip statement (computed): " + SIGN[0], SIGN[1], SIGN[2], SIGN[3]]},
             {"heading": "Head of Service Delivery salary (I-26, RESOLVED in v5)", "lines": SAL_LINES},
             {"heading": "Workbook text superseded by these notes", "lines": [N1_LINE]},
             {"heading": "Source and build",
              "lines": [f"Base: v4 collated workbook. v5 changes one input, Fld Eng Budget!B21 = {f0(I26['salary'])}; {n_patched} cached values downstream of it were recalculated "
                        f"({', '.join(f'{k} {v}' for k, v in sorted(by_sheet_patched.items()))}); no formula changed; every other cell keeps its v4 value. Inputs unchanged; plan file sha256 {sha(NEW)[:16]}...",
                        "Full notes: 02-build/02-build_notes_v5.md. Numbers on this sheet: live formulas (headline) or values computed by figures_v5.py from this workbook and the inputs."]},
             {"heading": "Changes from v4", "table": {"header": ["Item", "Point", "What v5 did", "Where"], "rows": CHG}},
             {"heading": "Assumptions register", "table": {"header": RHDR, "rows": reg}},
             {"heading": "Issues (v5) - severity: HIGH = blocks sign-off or > $250k; MED = $50k-250k or owner confirmation; LOW = < $50k or hygiene; RESOLVED = closed by a user answer",
              "table": {"header": ["ID", "Sev", "Location", "Finding", "Evidence", "2027 impact", "Basis", "Recommended action"], "rows": list(iss.values())}},
             {"heading": "'$000s' relabel (DeploySum)", "table": {"header": relabel["header"], "rows": relabel["rows"]}},
             {"heading": "DeploySum external-link formulas in the 9/30/26 file, stored as cached values",
              "table": {"header": extf["header"], "rows": extf["rows"]}},
         ]}
json.dump(notes, open(OUT_JSON, "w"), indent=1, default=str, sort_keys=True)
print(f"report_v5: wrote {OUT_MD} ({len(md):,} chars, analyze={'yes' if AN else 'no'}) and {OUT_JSON}; issues {dict(sev_count)}; "
      f"register {len(reg)}; variance n/m {nnm}/{nvar}; carried regen {CARRIED_REGEN}")
