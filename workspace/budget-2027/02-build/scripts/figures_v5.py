"""v5 figures: every number in the v5 notes, computed from a workbook's cached values and the inputs.

Usage:
  python3 -I figures_v5.py WORKBOOK_XLSX COO_INPUT_XLSX SD_INPUT_XLSX OUT_JSON

Same as figures_v4.py, except: I-26 reads the Head of Service Delivery salary (Fld Eng Budget!B21) and rebuilds the
model's 2027 treatment of it from the payroll inputs (start month, raise, tax, benefits), checked against the
workbook's own rows; FE / COO P&L SG&A payroll rows are read; the I-32 trend also has a case that continues the
2026 decline from Sep-26 (N3). Run on v4 (for the deltas) and on v5 (analyze_v5.py checks the v5 run on the
stage-2 and final packages is identical). Every cell read is label-checked first, so a moved row stops the script instead of giving a wrong number.
No figure in this file is typed: constants are only cell addresses, labels and month counts.
"""
import sys, json, re
import openpyxl

WB, COO, SD, OUT = sys.argv[1:5]
v = openpyxl.load_workbook(WB, data_only=True)
f = openpyxl.load_workbook(WB)


def cell(sh, a, wb=v):
    x = wb[sh][a].value
    return x


def num(sh, a, wb=v):
    x = cell(sh, a, wb)
    assert isinstance(x, (int, float)) and not isinstance(x, bool), (sh, a, x)
    return float(x)


def label(sh, row, expect, col="A", wb=v):
    got = wb[sh][f"{col}{row}"].value
    assert isinstance(got, str) and expect in got, (sh, row, expect, got)
    return got


fig = {}
# ------------------------------------------------------------------ headline (COO P&L)
HL = [("Revenue", 16, "Total - Income"), ("COGS", 63, "Total - Cost Of Sales"),
      ("Gross Profit", 64, "Gross Profit"), ("Opex", 116, "Total - Expense"),
      ("Net Ordinary Income", 117, "Net Ordinary Income"), ("Net Other Income", 131, "Net Other Income"),
      ("Net Income", 132, "Net Income")]
hl = {}
for k, r, lab in HL:
    label("COO P&L", r, lab)
    hl[k] = {"row": r, "N": num("COO P&L", f"N{r}"), "AG": num("COO P&L", f"AG{r}")}
for r, lab in ((19, "5010"), (20, "5011"), (21, "5012"), (22, "5020")):
    label("COO P&L", r, lab)
hl["Depreciation"] = {"row": "19-22", "N": sum(num("COO P&L", f"N{r}") for r in range(19, 23)),
                      "AG": sum(num("COO P&L", f"AG{r}") for r in range(19, 23))}
fig["headline"] = hl
C = hl["Net Income"]["AG"]                    # COO contribution 2027
fig["contribution"] = C

# ------------------------------------------------------------------ revenue basis
label("DeploySum", 40, "Recognized revenue")
label("DeploySum", 49, "5. Sep")
note5 = cell("DeploySum", "A49")
m = re.search(r"unsigned forecast of \$([\d,]+)", note5)
assert m, note5
fig["unsigned_sep_dec26"] = float(m.group(1).replace(",", ""))
fig["note5"] = note5
fig["plan_date"] = cell("DeploySum", "B4").date().isoformat()
label("DeploySum", 13, "Total bookings")
label("DeploySum", 7, "New logos – bookings")
label("DeploySum", 9, "Expansion – bookings")
fig["bookings_fy27"] = num("DeploySum", "R13")
fig["bookings_fy27_newlogo"] = num("DeploySum", "R7")
fig["bookings_fy27_expansion"] = num("DeploySum", "R9")
fig["bookings_sep_dec26"] = sum(num("DeploySum", f"{c}13") for c in "BCDE")
rev_dec26 = num("DeploySum", "E40")
fig["rev_dec26_monthly"] = rev_dec26
fig["rev_fy27"] = num("DeploySum", "R40")
fig["rev_exit_runrate_x12"] = rev_dec26 * 12
fig["rev_above_exit"] = fig["rev_fy27"] - rev_dec26 * 12
fig["rev_above_exit_pct"] = fig["rev_above_exit"] / fig["rev_fy27"]
fig["rev_po_ag12"] = num("PO", "AG12")
fig["rev_breakeven_pct"] = C / hl["Revenue"]["AG"]
# PO!U12:AF12 must still be formulas pointing at DeploySum F40:Q40 (static cached values there: A-24)
po_f = [f["PO"].cell(12, 21 + k).value for k in range(12)]
fig["po12_formulas_ok"] = all(isinstance(x, str) and x.upper() == f"=DEPLOYSUM!{openpyxl.utils.get_column_letter(6 + k)}40"
                              for k, x in enumerate(po_f))
ds40 = [f["DeploySum"].cell(40, 6 + k).value for k in range(12)]
fig["ds40_static_values"] = sum(1 for x in ds40 if isinstance(x, (int, float)))
label("PO", 13, "4500"); label("PO", 15, "4900")
fig["rev_4500_4900_2026"] = num("PO", "N13") + num("PO", "N15")

# ------------------------------------------------------------------ I-17 Logistics & WH payroll (SD input)
sd = openpyxl.load_workbook(SD, data_only=True)
ws = sd["Logistics&WH Payroll"]
r17 = [c.row for c in ws["A"] if c.value == "Total logistics & warehouse payroll"]
assert len(r17) == 1, r17
fig["i17_row"] = r17[0]
fig["i17"] = float(ws.cell(r17[0], 19).value)                 # column S = FY2027
hdr = [c.value for c in ws[r17[0] + 2]]
assert "FY2027" in str(ws.cell(r17[0] + 2, 19).value), hdr

# ------------------------------------------------------------------ I-05 Prod Payroll lift model vs PO 5100
label("Prod Payroll", 41, "Total lift payroll")
label("PO", 36, "Total - 5100 - Labor Expense - Production")
fig["i05_model"] = num("Prod Payroll", "S41")
fig["i05_po"] = num("PO", "AG36")
fig["i05"] = fig["i05_model"] - fig["i05_po"]
label("PO", 33, "5110"); fig["po_ag33"] = num("PO", "AG33")

# ------------------------------------------------------------------ I-10 lines zeroed in 2027
i10 = []
for sh, r, lab in (("FO", 58, "5920"), ("FO", 67, "6610"), ("FO", 91, "7200"), ("FE", 91, "7200")):
    label(sh, r, lab)
    assert num(sh, f"AG{r}") == 0, (sh, r)
    i10.append([sh, r, v[sh][f"A{r}"].value, num(sh, f"N{r}")])
fig["i10_lines"] = i10
fig["i10"] = sum(x[3] for x in i10)

# ------------------------------------------------------------------ I-26 Head of Service Delivery salary (B21)
FEB = "Fld Eng Budget"
label(FEB, 21, "Head of Service Delivery")
for r, lab in ((22, "Payroll taxes"), (23, "Benefits"), (24, "Annual raise"), (25, "Raise effective month"),
               (58, "PAYROLL"), (68, "Total salaries"), (69, "Payroll taxes"), (70, "Benefits"), (71, "Total payroll"),
               (78, "6610"), (79, "6630"), (80, "6640")):
    label(FEB, r, lab)
assert f[FEB]["A67"].value == "=A21", f[FEB]["A67"].value
b21 = cell(FEB, "B21")
fig["i26_b21"] = b21
sal = float(b21) if isinstance(b21, (int, float)) else 0.0
start = cell(FEB, "C21"); raise_m = cell(FEB, "B25")
tax, ben, rse = num(FEB, "B22"), num(FEB, "B23"), num(FEB, "B24")
months = [cell(FEB, f"{openpyxl.utils.get_column_letter(2 + k)}58") for k in range(12)]
model = [sal / 12 * (1 + (rse if m >= raise_m else 0)) if m >= start else 0.0 for m in months]
row67 = [num(FEB, f"{openpyxl.utils.get_column_letter(2 + k)}67") for k in range(12)]
assert all(abs(x - y) < 1e-6 for x, y in zip(model, row67)), (model, row67)      # the workbook does what we describe
fig["i26"] = {"salary": sal, "start": start.date().isoformat(), "raise_pct": rse, "raise_month": raise_m.date().isoformat(),
              "tax_pct": tax, "ben_pct": ben,
              "months_paid": sum(1 for x in model if x > 0), "months_raised": sum(1 for m in months if m >= raise_m and m >= start),
              "monthly_pre": sal / 12, "monthly_post": sal / 12 * (1 + rse),
              "salary_2027": num(FEB, "N67"), "tax_2027": num(FEB, "N67") * tax, "ben_2027": num(FEB, "N67") * ben}
fig["i26"]["total_2027"] = fig["i26"]["salary_2027"] + fig["i26"]["tax_2027"] + fig["i26"]["ben_2027"]
fig["i26"]["formula_b67"] = f[FEB]["B67"].value
# FE tab and COO P&L SG&A payroll rows (2027 AG, 2026 N)
sga = {}
for r, gl in ((67, "6610"), (68, "6630"), (69, "6640")):
    label("FE", r, gl); label("COO P&L", r, gl)
    sga[gl] = {"row": r, "FE_AG": num("FE", f"AG{r}"), "FE_N": num("FE", f"N{r}"), "FE_U": f["FE"][f"U{r}"].value,
               "COO_AG": num("COO P&L", f"AG{r}"), "FEB_N": num(FEB, f"N{76 + r - 65}")}
    assert abs(sga[gl]["FE_AG"] - sga[gl]["FEB_N"]) < 1e-6, (gl, sga[gl])
fig["sga"] = sga
fig["feb_total_payroll"] = num(FEB, "N71")
label("FE", 116, "Total - Expense"); label("FE", 132, "Net Income")
fig["fe_opex"] = num("FE", "AG116"); fig["fe_net"] = num("FE", "AG132")

# ------------------------------------------------------------------ depreciation inputs (schedule)
S = "Depreciation Schedule"
for r, lab in ((6, "SlipLift unit cost"), (7, "SlipLift peripherals"), (8, "SlipTray unit cost"),
               (9, "SlipLift useful life"), (10, "SlipTray useful life"), (11, "peripherals useful life"),
               (13, "Depreciation start")):
    label(S, r, lab)
lift, periph, tray = num(S, "B6"), num(S, "B7"), num(S, "B8")
L_lift, L_tray, L_per = num(S, "B9"), num(S, "B10"), num(S, "B11")
assert num(S, "B13") == 0
m_lift, m_tray, m_per = lift / L_lift, tray / L_tray, periph / L_per
fig["dep_inputs"] = {"lift": lift, "periph": periph, "tray": tray, "life_lift": L_lift, "life_tray": L_tray,
                     "life_periph": L_per, "m_lift": m_lift, "m_tray": m_tray, "m_periph": m_per}
label("DeploySum", 19, "SlipLifts going live"); label("DeploySum", 20, "SlipTrays going live")
lifts27 = [num("DeploySum", f"{openpyxl.utils.get_column_letter(6 + k)}19") for k in range(12)]
trays27 = [num("DeploySum", f"{openpyxl.utils.get_column_letter(6 + k)}20") for k in range(12)]
um_lift = sum(u * (12 - k) for k, u in enumerate(lifts27))      # unit-months in service, full-month rule
um_tray = sum(u * (12 - k) for k, u in enumerate(trays27))
fig["unit_months"] = {"lift": um_lift, "tray": um_tray}
new_month_total = sum(lifts27) * (m_lift + m_per) + sum(trays27) * m_tray   # one month of every 2027 vintage
fig["sens_next_month"] = -new_month_total
fig["sens_mid_month"] = -new_month_total / 2
# cross-check against the schedule output (Dec-27 PO minus Dec-26 run rate)
dec_new = sum(num("PO", f"AF{r}") - num("PO", f"M{r}") for r in (20, 21, 22))
assert abs(dec_new - new_month_total) < 1e-6, (dec_new, new_month_total)

# ------------------------------------------------------------------ I-33 peripherals
fig["i33_new_periph"] = um_lift * m_per
# contribution effect (+ = contribution up): life 60 months, or the SlipTray life
fig["i33_life60"] = -(um_lift * periph / 60 - um_lift * m_per)
fig["i33_life_tray"] = -(um_lift * periph / L_tray - um_lift * m_per)

# ------------------------------------------------------------------ I-31 Q4-26 go-lives (two-way)
PO_M = "JKLM"                                                       # Sep..Dec 26
for r, lab in ((19, "5010"), (20, "5011"), (21, "5012"), (22, "5020")):
    label("PO", r, lab)
steps = {r: [num("PO", f"{PO_M[i + 1]}{r}") - num("PO", f"{PO_M[i]}{r}") for i in range(3)] for r in (20, 21, 22)}
po_lifts = [round(s / m_lift, 6) for s in steps[20]]
po_trays = [round(s / m_tray, 6) for s in steps[21]]
assert all(abs(x - round(x)) < 1e-6 for x in po_lifts + po_trays), (po_lifts, po_trays)
po_lifts = [round(x) for x in po_lifts]; po_trays = [round(x) for x in po_trays]
ds_lifts = [num("DeploySum", f"{c}19") for c in "CDE"]
ds_trays = [num("DeploySum", f"{c}20") for c in "CDE"]
fig["q4"] = {"po_lifts": po_lifts, "po_trays": po_trays, "ds_lifts": ds_lifts, "ds_trays": ds_trays,
             "steps_5020": steps[22]}
gap_l, gap_t = sum(ds_lifts) - sum(po_lifts), sum(ds_trays) - sum(po_trays)
fig["i31_short"] = -(gap_l * m_lift + gap_t * m_tray) * 12            # replace with DeploySum Q4: more cost
# PO Dec-26 step-ups with no DeploySum Dec-26 go-live: possibly Jan-27 units (built Nov-26), already a Jan-27 vintage
dec_l, dec_t = po_lifts[2] - ds_lifts[2], po_trays[2] - ds_trays[2]
fig["i31_dec_units"] = [dec_l, dec_t]
fig["i31_double"] = (dec_l * m_lift + dec_t * m_tray) * 12            # critic: 3 x 773.81 x 12 + 12 x 66.67 x 12
fig["i31_double_5020"] = steps[22][2] * 12
# under that reading, the genuine Q4 shortfall is larger; the net against DeploySum is unchanged
fig["i31_gross_short_if_double"] = -((gap_l + dec_l) * m_lift + (gap_t + dec_t) * m_tray) * 12
fig["jan27_units"] = [lifts27[0], trays27[0]]

# ------------------------------------------------------------------ I-32 existing fleet / SlipBot
rr = {r: num("PO", f"M{r}") for r in (19, 20, 21, 22)}
fig["runrate"] = rr
fig["i32_full"] = rr[19] * 12
jan, aug, sep = num("PO", "B19"), num("PO", "I19"), num("PO", "J19")
slope_js = (sep - jan) / 8                     # Jan-26 -> Sep-26 (8 steps)
slope_ja = (aug - jan) / 7                     # Jan-26 -> Aug-26, actuals only (7 steps)
def trend_cut(slope):
    return sum(min(rr[19], -slope * k) for k in range(1, 13))
fig["i32_5010"] = {"jan": jan, "aug": aug, "sep": sep, "slope_jan_sep": slope_js, "slope_jan_aug": slope_ja}
fig["i32_trend"] = trend_cut(slope_js)
fig["i32_trend_actuals"] = trend_cut(slope_ja)
# N3: the decline also continues through Oct-Dec 26, so Jan-27 is 4 months after Sep-26; 5010 floored at 0.
# Effect = budgeted flat carry (12 x Dec-26 run rate) less the trend path from the Sep-26 level.
def trend_from_sep(slope):
    path = [max(0.0, sep + slope * (k + 3)) for k in range(1, 13)]
    return rr[19] * 12 - sum(path), path
fig["i32_trend_sep"], path_js = trend_from_sep(slope_js)
fig["i32_trend_sep_actuals"], _ = trend_from_sep(slope_ja)
fig["i32_trend_sep_path"] = {"jan27": path_js[0], "dec27": path_js[-1], "floored_months": sum(1 for x in path_js if x == 0)}
fig["i32_dec26_eq_sep"] = rr[19] == sep
fig["i32_5020_jan26"] = num("PO", "B22")
fig["i32_5011_jan26"] = num("PO", "B20")
fig["i32_5020_base_x12"] = num("PO", "B22") * 12
fig["existing_fy"] = sum(rr.values()) * 12

# ------------------------------------------------------------------ I-02 (O6): FO/FE COO book vs SD, in cost terms
coo = openpyxl.load_workbook(COO, data_only=True)
def cost(wb, sh):
    label(sh, 63, "Total - Cost Of Sales", wb=wb); label(sh, 116, "Total - Expense", wb=wb)
    return float(wb[sh]["AG63"].value or 0) + float(wb[sh]["AG116"].value or 0)
fig["i02"] = {"FO_coo": cost(coo, "FO"), "FE_coo": cost(coo, "FE"), "FO_sd": cost(v, "FO"), "FE_sd": cost(v, "FE")}
fig["i02"]["delta"] = fig["i02"]["FO_sd"] + fig["i02"]["FE_sd"] - fig["i02"]["FO_coo"] - fig["i02"]["FE_coo"]
fig["i02"]["contribution_with_coo_book"] = C + fig["i02"]["delta"]

# ------------------------------------------------------------------ O7: Prod Payroll error / formula counts
ERR = {"#REF!", "#N/A", "#VALUE!", "#DIV/0!", "#NAME?", "#NUM!", "#NULL!", "#ERROR!"}
pf, pv = f["Prod Payroll"], v["Prod Payroll"]
nform = nerr = 0; codes = {}
for row in pf.iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("="):
            nform += 1
        x = pv[c.coordinate].value
        if isinstance(x, str) and x in ERR:          # every error-valued cell (same basis as the v3 error scan)
            nerr += 1; codes[x] = codes.get(x, 0) + 1
fig["prodpay"] = {"formulas": nform, "errors": nerr, "codes": codes}

# ------------------------------------------------------------------ sign-flip arithmetic
down = {"I-17": fig["i17"], "I-05": fig["i05"], "I-10": fig["i10"], "I-31": -fig["i31_short"]}
fig["flip_alone"] = {k: x > C for k, x in down.items()}
fig["after_alone"] = {k: C - x for k, x in down.items()}
fig["after_i10_i31"] = C - fig["i10"] + fig["i31_short"]
fig["after_i17_i05"] = C - fig["i17"] - fig["i05"]
fig["after_all_down"] = C - sum(down.values())
fig["upside_full"] = C + fig["i32_full"]
fig["upside_trend"] = C + fig["i32_trend"]
fig["upside_trend_sep"] = C + fig["i32_trend_sep"]

json.dump(fig, open(OUT, "w"), indent=1, sort_keys=True, default=str)
print(f"figures: B21 {fig['i26_b21']}; FE 6610/6630/6640 {sga['6610']['FE_AG']:,.0f}/{sga['6630']['FE_AG']:,.0f}/{sga['6640']['FE_AG']:,.0f}; "
      f"I-32 trend from Sep +{fig['i32_trend_sep']:,.0f}")
print(f"figures: contribution {C:,.2f}; I-17 {fig['i17']:,.0f}; I-05 {fig['i05']:,.0f}; I-10 {fig['i10']:,.0f}; "
      f"I-31 {fig['i31_short']:,.0f} / +{fig['i31_double']:,.0f}; I-32 +{fig['i32_full']:,.0f} trend +{fig['i32_trend']:,.0f}; "
      f"mid-month {fig['sens_mid_month']:,.0f}; next-month {fig['sens_next_month']:,.0f}")
