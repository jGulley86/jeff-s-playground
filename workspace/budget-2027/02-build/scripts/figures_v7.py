"""v7 figures: every new number in the v7 notes (critic v6 B1-B3, O1-O8; verifier v6 V1). No budget value changes.

Usage:
  python3 -I figures_v7.py V6_XLSX PP_RECALC_XLSX RECON_JSON SCEN_JSON WORKFILE SD_BOOK OUT_JSON

  V6_XLSX         the v6 workbook (cached values; budget values are identical in v7)
  PP_RECALC_XLSX  LibreOffice recalculation of the prodpay_v6.py scratch copy of V6 (Prod Payroll tray/supervisor rows)
  RECON_JSON      recon_v6.py output on V6 (people identified by roster + row + title; no names)
  SCEN_JSON       scen_v7.py compare output (Fld Ops Payroll!B11 - 1, recalculated: I-28 FO side with knock-ons)
  WORKFILE        COO_HC_and_PL_workfile.xlsx (file date only)
  SD_BOOK         Service_Delivery_PL_worksheets.xlsx (file date only)

Every figure is read from cells or computed from them. The only constants typed here are statutory or definitional and
are named: FICA_EMPLOYER (6.2% Social Security + 1.45% Medicare). No names are read.
"""
import sys, json, re, datetime
import openpyxl

V6, PPR, RECON, SCEN, WF, SD, OUT = sys.argv[1:8]
R = json.load(open(RECON)); SC = json.load(open(SCEN))
wb = openpyxl.load_workbook(V6, data_only=True)
wf_ = openpyxl.load_workbook(V6)          # formulas (for the driver-link evidence)
ppr = openpyxl.load_workbook(PPR, data_only=True)
FICA_EMPLOYER = 0.062 + 0.0145


def num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0


def ag(sheet, r):
    return num(wb[sheet].cell(r, 33).value)


def n26(sheet, r):
    return num(wb[sheet].cell(r, 14).value)


def label(sheet, r):
    return str(wb[sheet].cell(r, 1).value)


pp, po, lw, fo, fe, hc, dup = R["pp"], R["po"], R["lw"], R["fo"], R["fe"], R["hc"], R["dup"]
C = ag("COO P&L", 132)
I05, I17 = po["net_i05"], po["net_i17"]
out = {"contribution": C, "I05": I05, "I17": I17, "I05_I17_v6": I05 + I17}

# ------------------------------------------------------------------ B1: evidence for capitalised production labour
ds = wb["DeploySum"]
capex_lbl = [(c.coordinate, c.value) for row in ds.iter_rows() for c in row if isinstance(c.value, str) and "Unit cost (CapEx)" in c.value]
assert len(capex_lbl) == 1
dsch = wb["Depreciation Schedule"]
ev = {"deploysum_unit_cost_cell": capex_lbl[0][0], "deploysum_unit_cost_text": capex_lbl[0][1],
      "lift_unit_cost": num(dsch["B6"].value), "lift_periph": num(dsch["B7"].value), "tray_unit_cost": num(dsch["B8"].value),
      "lift_life": num(dsch["B9"].value), "tray_life": num(dsch["B10"].value), "dep_start_offset": num(dsch["B13"].value)}
assert label("PO", 73).startswith("Total - 6000") and label("PE", 35).startswith("5140") and label("COO P&L", 36).startswith("Total - 5100")
assert label("COO P&L", 91).startswith("7200")
MON26 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def neg_months(sheet, r):
    return [(MON26[c - 2], num(wb[sheet].cell(r, c).value)) for c in range(2, 14) if num(wb[sheet].cell(r, c).value) < -0.5]


ev["po_6000_2026"] = n26("PO", 73); ev["po_6610_2026"] = n26("PO", 67)
ev["po_6610_neg_months"] = neg_months("PO", 67)
ev["pe_5140_2026"] = n26("PE", 35); ev["pe_5140_neg_months"] = neg_months("PE", 35)
ev["coo_5100_2026"] = n26("COO P&L", 36); ev["coo_5100_2027"] = ag("COO P&L", 36)
ev["coo_5100_2027_with_ramp"] = ev["coo_5100_2027"] + I05
ev["ratio_budget_vs_2026"] = ev["coo_5100_2027"] / ev["coo_5100_2026"]
ev["ratio_ramp_vs_2026"] = ev["coo_5100_2027_with_ramp"] / ev["coo_5100_2026"]
ev["dept_5100_2026"] = {d: n26(d, 36) for d in ("FO", "PO", "CO", "FE", "PE")}
ev["coo_7200_2026"] = n26("COO P&L", 91); ev["coo_7200_2027"] = ag("COO P&L", 91)
ev["dept_7200_2026"] = {d: n26(d, 91) for d in ("FO", "PO", "CO", "FE", "PE")}
assert abs(sum(ev["dept_7200_2026"].values()) - ev["coo_7200_2026"]) < 0.01
assert abs(sum(ev["dept_5100_2026"].values()) - ev["coo_5100_2026"]) < 0.01
out["b1_evidence"] = ev

# ------------------------------------------------------------------ B1: capitalised case, depreciation only
# Allocation of the ramp to lifts and trays: derived from the model (lift ramp = lift model total less the model's cost
# of the current lift staff; same for trays). Supervisors are shared: allocated pro rata to the lift : tray ramp cost
# (assumption A-32). The handoff's fallback split (model totals lift / tray, supervisors pro rata) is shown as a check.
co = pp["current_only"]
ramp = {"lift": pp["lift_total"] - co["lift"], "tray": pp["tray_total"] - co["tray"], "sup": pp["sup_total"] - co["sup"]}
assert abs(sum(ramp.values()) - I05) < 1e-6
sh_lift = ramp["lift"] / (ramp["lift"] + ramp["tray"])
alloc = {"lift": ramp["lift"] + ramp["sup"] * sh_lift, "tray": ramp["tray"] + ramp["sup"] * (1 - sh_lift)}
sh_lift_fb = pp["lift_total"] / (pp["lift_total"] + pp["tray_total"])
alloc_fb = {"lift": I05 * sh_lift_fb, "tray": I05 * (1 - sh_lift_fb)}
# Build lag: DeploySum production row 24 (lifts to build) vs go-live row 19, columns B..Q (Sep-26..Dec-27)
golive_l = [num(ds.cell(19, c).value) for c in range(2, 18)]; golive_t = [num(ds.cell(20, c).value) for c in range(2, 18)]
build_l = [num(ds.cell(24, c).value) for c in range(2, 18)]; build_t = [num(ds.cell(25, c).value) for c in range(2, 18)]
lags = [k for k in range(0, 6) if all(build_l[i] == golive_l[i + k] and build_t[i] == golive_t[i + k] for i in range(16 - k))]
assert len(lags) == 1, lags
LAG = lags[0]
units_built_2027 = {"lift": sum(build_l[4:16]), "tray": sum(build_t[4:16])}
assert units_built_2027["lift"] == num(ds["R24"].value) and units_built_2027["tray"] == num(ds["R25"].value)
# 2027 go-live vintages from the Depreciation Schedule (rows 38-49 lifts, 51-62 trays; C = go-live month #, D = units)
vint = []
for k in range(12):
    rl, rt = 38 + k, 51 + k
    g = int(num(dsch.cell(rl, 3).value)); assert g == k + 1 and int(num(dsch.cell(rt, 3).value)) == g
    months = sum(1 for m in range(1, 13) if m >= g + ev["dep_start_offset"])
    # check the months-in-service rule against the schedule's own monthly cells (rows with units)
    e_l = num(dsch.cell(rl, 5).value)
    if e_l:
        assert abs(sum(num(dsch.cell(rl, c).value) for c in range(6, 18)) - e_l * months) < 1e-6
    vint.append({"golive": g, "lifts": num(dsch.cell(rl, 4).value), "trays": num(dsch.cell(rt, 4).value), "months_2027": months,
                 "built_in_2027": g - LAG >= 1})


def dep_2027(al):
    rate_l = al["lift"] / units_built_2027["lift"]; rate_t = al["tray"] / units_built_2027["tray"]
    d_l = sum(rate_l * v["lifts"] / ev["lift_life"] * v["months_2027"] for v in vint if v["built_in_2027"])
    d_t = sum(rate_t * v["trays"] / ev["tray_life"] * v["months_2027"] for v in vint if v["built_in_2027"])
    return {"labour_per_lift": rate_l, "labour_per_tray": rate_t, "dep_lift": d_l, "dep_tray": d_t, "dep": d_l + d_t,
            "labour_pct_of_lift_cost": rate_l / ev["lift_unit_cost"], "labour_pct_of_tray_cost": rate_t / ev["tray_unit_cost"],
            "capitalised": al["lift"] + al["tray"], "on_balance_sheet_end27": al["lift"] + al["tray"] - d_l - d_t}


cap = {"ramp_by_model": ramp, "sup_share_to_lift": sh_lift, "alloc": alloc, "alloc_fallback": alloc_fb, "build_lag_months": LAG,
       "units_built_2027": units_built_2027, "vintages_built_in_2027": [v["golive"] for v in vint if v["built_in_2027"]],
       "units_live_2027_built_2027": {"lift": sum(v["lifts"] for v in vint if v["built_in_2027"]), "tray": sum(v["trays"] for v in vint if v["built_in_2027"])},
       "units_built_2027_live_2028": {"lift": num(ds["R33"].value), "tray": num(ds["R34"].value)},
       "d9": dep_2027(alloc), "d9_fallback": dep_2027(alloc_fb)}

# ------------------------------------------------------------------ B2: overlap 9 (count) vs 7 (production roles)
B9, C9, H10 = pp["inputs"]["B9"], pp["inputs"]["C9"], pp["inputs"]["H10"]
per_head = {"lift": co["lift"] / B9, "tray": co["tray"] / C9, "avg": co["total"] / pp["current_hc"]}
titles = hc["PO"]["titles"]
mh_titles = {t: n for t, n in titles.items() if "material" in t.lower()}
n_mh = sum(mh_titles.values()); n_prod = hc["PO"]["n_people"] - n_mh
assert n_prod == 7 and n_mh == 2, (n_prod, n_mh)
n_extra = pp["current_hc"] - n_prod                              # model current seats no PO HC production person fills
extra = {"central": n_extra * per_head["avg"], "low": n_extra * min(per_head["lift"], per_head["tray"]),
         "high": n_extra * max(per_head["lift"], per_head["tray"])}
I05_7 = I05 + extra["central"]
mh01 = [e for e in lw["seats"] if e["overlap"] and e["overlap_with"].startswith("PO HC")]
assert len(mh01) == 1
mh01 = mh01[0]
lw_po_links = {"name": mh01["overlap_with"], "backfill": po["lw_backfill_refs"]}
b2 = {"n_prod": n_prod, "n_mh": n_mh, "mh_titles": mh_titles, "n_extra": n_extra, "per_head": per_head, "extra": extra,
      "I05_9": I05, "I05_7": I05_7, "I05_7_low": I05 + extra["low"], "I05_7_high": I05 + extra["high"],
      "mh01_seat": mh01["seat"], "mh01_cost": mh01["cost_2027"], "mh01_is": mh01["overlap_with"], "lw_po_links": lw_po_links,
      "combined_v6": I05 + I17,
      "combined_9_dedup": I05 + I17 + mh01["cost_2027"],
      "combined_7": I05_7 + I17}
cap["d7"] = dep_2027({k: v * I05_7 / I05 for k, v in alloc.items()})    # 7-reading: same lift/tray mix, scaled (A-33)
out["b2"] = b2
out["b1_cap"] = cap

# ------------------------------------------------------------------ contributions under each treatment / reading
out["contrib"] = {"budget": C,
                  "expensed_9": C - I05, "expensed_7": C - I05_7,
                  "capitalised_on_top_9": C - cap["d9"]["dep"], "capitalised_on_top_7": C - cap["d7"]["dep"],
                  "capitalised_in_unit_cost": C}

# ------------------------------------------------------------------ B3: asymmetry, same deployment plan drives both ramps
links = {}
for sh in ("Fld Ops Payroll", "Prod Payroll"):
    rows_ = set()
    for row in wf_[sh].iter_rows():
        for c in row:
            if isinstance(c.value, str) and "DeploySum" in c.value:
                for m in re.findall(r"DeploySum!\$?[A-Z]+\$?(\d+)", c.value):
                    rows_.add(int(m))
    links[sh] = {r: str(ds.cell(r, 1).value).strip() for r in sorted(rows_)}
out["b3"] = {"fo_ramp": fo["ramp"]["total"], "fo_current": fo["current"]["total"], "fo_total": fo["total"], "po_ramp_9": I05, "po_ramp_7": I05_7,
             "deploysum_links": links, "both_ramps": fo["ramp"]["total"] + I05}

# ------------------------------------------------------------------ O1: I-05 at PO HC burden rates
rp = pp["ramp_parts"]
t_hc, b_hc = hc["PO"]["rate_tax"], hc["PO"]["rate_ben"]
model_burden = rp["tax"] + rp["ben"]
po_rate_burden = (rp["sal"] + rp["abs"] + rp["ot"]) * t_hc + rp["sal"] * b_hc
fica_burden = (rp["sal"] + rp["abs"] + rp["ot"]) * max(t_hc, FICA_EMPLOYER) + rp["sal"] * b_hc
out["o1"] = {"model_burden": model_burden, "model_burden_pct_of_sal": model_burden / rp["sal"],
             "po_rates": [t_hc, b_hc], "po_rate_burden": po_rate_burden, "po_rate_pct": t_hc + b_hc,
             "diff": po_rate_burden - model_burden, "I05_at_po_rates": I05 + po_rate_burden - model_burden,
             "diff_fica_floor": fica_burden - model_burden, "I05_at_po_rates_fica": I05 + fica_burden - model_burden,
             "model_rates": {"lift_tax": pp["inputs"]["B6"], "tray_tax": pp["inputs"]["C6"], "lift_ben": pp["inputs"]["B7"], "tray_ben": pp["inputs"]["C7"]}}

# ------------------------------------------------------------------ O2: model hires dated Sep-Dec 26 vs the roster file date
pl = ppr["Prod Payroll"]
hc26 = {"lift": [num(pl.cell(31, c).value) for c in range(2, 6)], "tray": [num(pl.cell(52, c).value) for c in range(2, 6)],
        "sup": [num(pl.cell(71, c).value) for c in range(2, 6)]}
base0 = {"lift": B9, "tray": C9, "sup": H10}
hires26 = {k: [max(0, v[i] - (v[i - 1] if i else base0[k])) for i in range(4)] for k, v in hc26.items()}
for k in hires26:
    assert abs(sum(hires26[k]) - po["sd_hires_sep_dec26"][k]) < 1e-9
dates26 = [openpyxl.load_workbook(V6, data_only=True)["Prod Payroll"].cell(24, c).value for c in range(2, 6)]
lw26 = [e for e in lw["seats"] if not e["overlap"] and e["start"][-2:] == "26"]
wfp = openpyxl.load_workbook(WF, read_only=True).properties; sdp = openpyxl.load_workbook(SD, read_only=True).properties
out["o2"] = {"pp_hires_by_month": {k: v for k, v in hires26.items()}, "months": [d.strftime("%b-%y") for d in dates26],
             "pp_hires_total": sum(sum(v) for v in hires26.values()),
             "lw_2026_seats": [(e["seat"].replace("Logistics&WH ", ""), e["start"]) for e in lw26],
             "workfile_modified": wfp.modified.strftime("%Y-%m-%d"), "sd_modified": sdp.modified.strftime("%Y-%m-%d"),
             "sd_created": sdp.created.strftime("%Y-%m-%d") if sdp.created else ""}

# ------------------------------------------------------------------ O3 / V1: the FO/FE probable duplicate
fofe = dup["fo_fe"][0]
out["v1"] = {"fo_effect": SC["effect"], "fo_payroll": SC["fo_payroll_effect"], "knock_on": SC["knock_on_effect"],
             "knock_on_rows": SC["knock_on_rows"], "after": C + SC["effect"], "v6_stated": fofe["fo_model_one_tech_2027"],
             "v6_after": C + fofe["fo_model_one_tech_2027"], "sup_hc_unchanged": SC["sup_hc_by_month_base"] == SC["sup_hc_by_month_scen"],
             "B11": [SC["B11_base"], SC["B11_scen"]],
             "fe_effect": fofe["fe_cost_2027"], "fe_after": C + fofe["fe_cost_2027"],
             "fo_per_month_avg": SC["effect"] / 12, "fe_per_month_avg": fofe["fe_cost_2027"] / 12}
assert abs(out["v1"]["fo_payroll"] - fofe["fo_model_one_tech_2027"]) < 0.01

# ------------------------------------------------------------------ O5: FE HC r35 is an open seat
fws = wb["HC-FE"]
r35_sec = None
for r in range(35, 13, -1):
    v = fws.cell(r, 2).value
    if isinstance(v, str) and v.strip() in ("Current Employees", "Open Positions", "New Hires", "Transfers In", "Transfers Out"):
        r35_sec = (r, v.strip()); break
r35 = [e for e in fe["rows"] if e.get("hc") and e["hc"].startswith("FE HC r35")][0]
out["o5"] = {"section_row": r35_sec[0], "section": r35_sec[1], "sd_row": r35["sd"], "basis": r35["basis"], "hc_start": r35["hc_start"],
             "sd_start": r35["sd_start"], "coo_book_excludes": fe["coo_book_gap_rows"], "coo_book_gap": fe["coo_book_gap_vs_hc"],
             "sd_cost_2027": r35["sd_2027"] * (1 + fe["sd_rates"]["tax"] + fe["sd_rates"]["ben"])}

# ------------------------------------------------------------------ O6: HC T&B tax rates vs employer FICA
o6 = {"fica": FICA_EMPLOYER, "depts": {}}
for d in ("FO", "PO", "CO", "FE", "PE"):
    t = hc[d]["rate_tax"]; base = hc[d]["z"]["sal"]
    o6["depts"][d] = {"hc_rate": t, "below_fica": t < FICA_EMPLOYER, "hc_salary_2027": base,
                      "gap_at_fica_on_hc_salary": max(0.0, FICA_EMPLOYER - t) * base}
# budget-side: PO/CO/PE use their HC rates on the HC salaries; FO/FE use the SD rate (6.8%) on the SD salary base
o6["budget_uses_hc_rate"] = ["PO", "CO", "PE"]
o6["po_co_pe_gap"] = sum(o6["depts"][d]["gap_at_fica_on_hc_salary"] for d in ("PO", "CO", "PE"))
sd_t = fe["sd_rates"]["tax"]
fo_sal_budget = fo["current"]["sal"] + fo["ramp"]["sal"]
o6["sd_rate"] = sd_t
o6["fo_gap_at_fica"] = max(0.0, FICA_EMPLOYER - sd_t) * fo_sal_budget
o6["fe_gap_at_fica"] = max(0.0, FICA_EMPLOYER - sd_t) * fe["pl_v5"]["sal"]
o6["fo_sal_budget"] = fo_sal_budget; o6["fe_sal_budget"] = fe["pl_v5"]["sal"]
o6["i34_tax_part"] = fe["burden"]["diff_tax"]; o6["i34_ben_part"] = fe["burden"]["diff_ben"]
o6["i34_if_tax_at_fica"] = fe["burden"]["diff_ben"] + (sd_t - max(fe["hc_rates"]["tax"], FICA_EMPLOYER)) * fe["pl_v5"]["sal"]
o6["all_gap"] = o6["po_co_pe_gap"] + o6["fo_gap_at_fica"] + o6["fe_gap_at_fica"]
out["o6"] = o6

# ------------------------------------------------------------------ O7: range, both lower bounds
# carried downside amounts (I-10, I-31 shortfall) are read from the v6 caveat rows by the report; here only the payroll parts
out["o7"] = {"note": "lower bounds are assembled in report_v7.py from the carried I-10 / I-31 rows and these payroll figures"}
json.dump(out, open(OUT, "w"), indent=1, default=str)
print(f"figures_v7: contribution {C:,.2f}; I-05 9-overlap {I05:,.2f}, 7-overlap {I05_7:,.2f} (+{extra['central']:,.2f}; "
      f"range {extra['low']:,.0f}..{extra['high']:,.0f}); capitalised dep 2027 9 {cap['d9']['dep']:,.2f} / 7 {cap['d7']['dep']:,.2f} "
      f"(fallback split {cap['d9_fallback']['dep']:,.2f}); combined v6 {I05 + I17:,.2f}, 9 dedup {b2['combined_9_dedup']:,.2f}, "
      f"7 {b2['combined_7']:,.2f}; O1 +{out['o1']['diff']:,.2f}; V1 FO {SC['effect']:+,.2f}; O6 PO/CO/PE gap {o6['po_co_pe_gap']:,.2f}")
