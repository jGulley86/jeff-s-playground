"""v13 figures: every number for the v13 md and the Collation Notes updates, computed from the workbooks.

Reads: V12 (base, cached), S1RC (the stage-1 edit file after a full LibreOffice recalculation - value-identical to
the deliverable on every non-Collation-text cell), USER (the user's edited FINAL_v4 copy, for the roster Z
cross-check), SCENDIR (five LibreOffice-recalculated scenario copies of S1RC written by run_build_v13.sh).
Writes FIGURES_JSON. No names are read into the output (names stay on the HC tabs); no clock, no file properties,
no dates are read (F1 rule). Exits 1 if any internal tie or carried-delta assertion fails.

Usage:
  python3 -I figures_v13.py V12_XLSX S1RC_XLSX USER_XLSX SCENDIR OUT_JSON
"""
import sys, json, os
import openpyxl

V12P, S1P, USERP, SCEND, OUT = sys.argv[1:6]
TOL = 0.01
LWS = "Logistics&WH Payroll"

v12 = openpyxl.load_workbook(V12P, data_only=True)
s1 = openpyxl.load_workbook(S1P, data_only=True)
usr = openpyxl.load_workbook(USERP, data_only=True)

n = lambda v: float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0
cell = lambda wb, sh, ad: n(wb[sh][ad].value)
fails = []


def req(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


def money(x, dp=0):
    s = f"{abs(x):,.{dp}f}"
    return f"({s})" if x < -0.004 else s


def r5(x):
    """Per-person amount rounded to the nearest $5k (banner convention; used in prose shared with the md)."""
    v = round(abs(x) / 5000) * 5000
    return f"(~{v:,.0f})" if x < 0 else f"~{v:,.0f}"


F = {}
# ---------------------------------------------------------------- headline and department lines
F["AG132_v12"] = cell(v12, "COO P&L", "AG132")
F["AG132_v13"] = cell(s1, "COO P&L", "AG132")
F["N132"] = cell(s1, "COO P&L", "N132")
F["rev_v13"] = cell(s1, "COO P&L", "AG16")
F["cogs_v13"] = cell(s1, "COO P&L", "AG63")
F["opex_v13"] = cell(s1, "COO P&L", "AG116")
F["cost_v13"] = F["cogs_v13"] + F["opex_v13"]
F["gp_v13"] = cell(s1, "COO P&L", "AG64")
F["dep_in_cogs_v13"] = sum(cell(s1, "COO P&L", f"AG{r}") for r in (19, 20, 21, 22))
for ad in ("N16", "N63", "N64", "N116", "N117", "N131"):
    F[f"coo_{ad}"] = cell(s1, "COO P&L", ad)
F["coo_AG117"], F["coo_AG131"] = cell(s1, "COO P&L", "AG117"), cell(s1, "COO P&L", "AG131")
F["dep_in_cogs_2026"] = sum(cell(s1, "COO P&L", f"N{r}") for r in (19, 20, 21, 22))
F["opex_v12"] = cell(v12, "COO P&L", "AG116")
F["cogs_v12"] = cell(v12, "COO P&L", "AG63")
req(abs(cell(v12, "COO P&L", "AG16") - F["rev_v13"]) < TOL, "revenue unchanged")

F["co66_v12_rows"] = [cell(v12, "CO", f"AG{r}") for r in (67, 68, 69)]
F["co66_v12_rows"].append(sum(F["co66_v12_rows"]))
F["co66_v13_rows"] = [cell(s1, "CO", f"AG{r}") for r in (67, 68, 69)]
F["co66_v13_rows"].append(sum(F["co66_v13_rows"]))
F["co66_v12"], F["co66_v13"] = F["co66_v12_rows"][3], F["co66_v13_rows"][3]
F["co7700_v13"], F["co8600_v13"] = cell(s1, "CO", "AG98"), cell(s1, "CO", "AG106")
F["co8600_2026"] = cell(s1, "CO", "N106")
F["co_exp_v13"] = cell(s1, "CO", "AG116")
req(abs(F["co7700_v13"] - 24000) < TOL and abs(F["co8600_v13"] - 78000) < TOL, "CO 7700 = 24,000 / 8600 = 78,000")
req(abs(cell(s1, "CO", "U98") - 2000) < TOL and abs(cell(s1, "CO", "AF106") - 6500) < TOL, "CO 7700/8600 monthly spread 2,000 / 6,500")

F["pe66_v12_rows"] = [cell(v12, "PE", f"AG{r}") for r in (67, 68, 69)]
F["pe66_v12"] = sum(F["pe66_v12_rows"])
F["pe66_v13_rows"] = [cell(s1, "PE", f"AG{r}") for r in (67, 68, 69)]
F["pe66_v13"] = sum(F["pe66_v13_rows"])
F["po66_v13_rows"] = [cell(s1, "PO", f"AG{r}") for r in (67, 68, 69)]
F["po66_v13"] = sum(F["po66_v13_rows"])
F["po5100_v13"] = sum(cell(s1, "PO", f"AG{r}") for r in (33, 34, 35))
req(abs(F["po5100_v13"]) < TOL, "PO 5110-5140 booked stays 0 (capitalised)")

# FO: the I-28 fix
fo_v12 = cell(v12, "FO", "AG63") + cell(v12, "FO", "AG116")
fo_v13 = cell(s1, "FO", "AG63") + cell(s1, "FO", "AG116")
F["b11_effect"] = fo_v12 - fo_v13
F["b11_payroll"] = sum(cell(v12, "FO", f"AG{r}") - cell(s1, "FO", f"AG{r}") for r in (52, 53, 54))
F["b11_5330"] = cell(v12, "FO", "AG46") - cell(s1, "FO", "AG46")
req(abs(F["b11_effect"] - 78529.08) < 1.0, f"B11 14->13 effect {F['b11_effect']:.2f} = +78,529 (evidence)")
req(abs(F["b11_effect"] - F["b11_payroll"] - F["b11_5330"]) < TOL, "B11 effect = payroll + 5330 only")
req(abs(cell(s1, "Fld Ops Payroll", "B11") - 13) < TOL and abs(cell(s1, "Fld Maint Budget", "B29") - 20) < TOL,
    "Fld Ops Payroll B11 = 13; Fld Maint Budget B29 = 20")
fe_v12 = cell(v12, "FE", "AG63") + cell(v12, "FE", "AG116")
fe_v13 = cell(s1, "FE", "AG63") + cell(s1, "FE", "AG116")
req(abs(fe_v12 - fe_v13) < TOL, "FE P&L unchanged (roster add feeds nothing)")

# ---------------------------------------------------------------- HC rosters and the user-file cross-check
for d in ("CO", "PO", "FE", "PE"):
    F[f"hc{d.lower()}_v13_z"] = [cell(s1, f"HC-{d}", f"Z{r}") for r in (67, 68, 69, 70)]
    F[f"hc{d.lower()}_v12_z"] = [cell(v12, f"HC-{d}", f"Z{r}") for r in (67, 68, 69, 70)]
F["hcco_v13_rows"] = [F["hcco_v13_z"][0], F["hcco_v13_z"][1], F["hcco_v13_z"][2], F["hcco_v13_z"][3]]
F["hcco_total_v13"] = F["hcco_v13_z"][3]
F["co_adds_rows"] = [F["hcco_v13_z"][i] - F["hcco_v12_z"][i] for i in range(4)]
# user's file Z totals (their HC-PO totals sit one row higher after their row deletion)
user_z = {"CO": cell(usr, "HC-CO", "Z67"), "PO": cell(usr, "HC-PO", "Z66"),
          "FE": cell(usr, "HC-FE", "Z67"), "PE": cell(usr, "HC-PE", "Z67")}
for d, uz in user_z.items():
    ours = F[f"hc{d.lower()}_v13_z"][0]
    req(abs(ours - uz) < TOL, f"HC-{d} 2027 salary total {ours:,.2f} = user's file {uz:,.2f}")
F["user_z"] = user_z
F["pm_z"] = cell(s1, "HC-PO", "Z41")
F["tl_roster_2027_salary"] = cell(s1, "HC-PO", "Z16")   # same person/salary as HC-CO r20
req(abs(cell(s1, "HC-CO", "Z20")) < TOL, "HC-CO r20 (MH Team Lead) 2027 = 0 (end-dated Nov-26, user's file value)")
req(abs(cell(s1, "HC-CO", "Z19") - 50294.40) < TOL, "HC-CO r19 (Material Handler) 2027 salary 50,294.40")
po_d6, po_d7 = cell(s1, "HC-PO", "D6"), cell(s1, "HC-PO", "D7")
co_d6, co_d7 = cell(s1, "HC-CO", "D6"), cell(s1, "HC-CO", "D7")
pe_d6, pe_d7 = cell(s1, "HC-PE", "D6"), cell(s1, "HC-PE", "D7")
F["i41_effect"] = round(F["tl_roster_2027_salary"] * (1 + po_d6 + po_d7), 2)
F["tl_roster_2027_cost"] = round(F["tl_roster_2027_salary"] * (1 + co_d6 + co_d7), 2)
req(abs(F["po66_v13"] - F["pm_z"] * (1 + po_d6 + po_d7)) < TOL, "PO 6610-6640 = the PM at PO HC rates (live)")
# HC-COO roll-up
F["hccoo_total_v13"] = cell(s1, "HC-COO", "Z43")
F["hccoo_people"] = [cell(s1, "HC-COO", f"Z{r}") for r in range(65, 70)]  # PO FO FE PE CO Dec-27 ending
req(abs(cell(s1, "HC-COO", "M49")) < TOL and abs(cell(s1, "HC-COO", "M76")) < TOL,
    "HC-COO internal checks (M49 classification, M76 headcount) = 0")

# ---------------------------------------------------------------- logistics seats: in/out
lw = s1[LWS]
b5, b6 = n(lw["B5"].value), n(lw["B6"].value)
nh_per = n(lw["B10"].value)
SEATS = {}   # code -> dict
for r in range(14, 23):
    code = str(lw.cell(r, 1).value).split()[0]
    sal27 = sum(n(lw.cell(r + 20, c).value) for c in range(6, 18))      # F..Q on row r+20 (rows 34-42)
    start = lw.cell(r, 21).value                                        # U column
    nh27 = nh_per if (start is not None and start.year == 2027) else 0.0
    SEATS[code] = {"sal27": sal27, "cost27": sal27 * (1 + b5 + b6) + nh27, "start": None if start is None else start.strftime("%b-%y")}
OUT_SEATS = ["LOG-01", "TL-01", "MH-01", "MH-02"]
IN_SEATS = ["INV-01", "MH-03", "MH-04", "TL-02", "MH-06"]
for c in IN_SEATS + OUT_SEATS:
    F[f"seat_{c}"] = round(SEATS[c]["cost27"], 2)
req(abs(F["seat_MH-01"] - 61962.70) < 0.5 and abs(F["seat_LOG-01"] - 148948.80) < 0.5, "seat costs match evidence (MH-01 61,962.70; LOG-01 148,948.80)")
F["lw_in_sal"] = sum(SEATS[c]["sal27"] for c in IN_SEATS)
F["lw_in_tax"] = F["lw_in_sal"] * b5
F["lw_in_ben"] = F["lw_in_sal"] * b6
F["lw_in_nh"] = sum(n(lw.cell(46, c).value) for c in range(6, 18))
req(abs(F["lw_in_nh"] - 5000) < TOL, "2027 new-hire cost 5,000 (5 in-seats)")
req(abs(n(lw["C46"].value) - 1000) < TOL and abs(n(lw["E46"].value) - 1000) < TOL,
    "MH-02 (Oct-26) and TL-01 (Dec-26) hire costs sit in 2026 columns and drop out of 2027")
F["lw_in_rows"] = [F["lw_in_sal"] + F["lw_in_nh"], F["lw_in_tax"], F["lw_in_ben"]]
F["lw_in_rows"].append(sum(F["lw_in_rows"]))
F["lw_added_v13"] = F["lw_in_rows"][3]
F["lw_out_total"] = sum(SEATS[c]["cost27"] for c in ("TL-01", "MH-01", "MH-02"))
# v12 add-on (LOG-01 excluded only), from the v12 cache
lw12 = v12[LWS]
s43, s44, s45, s46, s34 = (n(lw12[f"S{r}"].value) for r in (43, 44, 45, 46, 34))
F["lw_added_v12"] = (s43 - s34) + (s44 - s34 * b5) + (s45 - s34 * b6) + s46
req(abs(F["lw_added_v12"] - 398492.42) < 0.5, "v12 logistics add-on 398,492 reproduced")
req(abs(F["lw_added_v12"] - F["lw_out_total"] - F["lw_added_v13"]) < TOL, "add-on v12 - 3 excluded seats = v13 add-on")
# CO composition tie
for i in range(4):
    req(abs(F["hcco_v13_rows"][i] + F["lw_in_rows"][i] - F["co66_v13_rows"][i]) < TOL,
        f"CO 66{('10','30','40','10-6640')[i]} = HC-CO + logistics in-seats (row {i})")

# ---------------------------------------------------------------- bridge A-G
F["d_gl"] = -(F["co7700_v13"] + F["co8600_v13"])
F["d_co66"] = -(F["co66_v13"] - F["co66_v12"])
F["d_pe66"] = -(F["pe66_v13"] - F["pe66_v12"])
F["d_po66"] = -F["po66_v13"]
F["d_fo"] = F["b11_effect"]
F["bridge_sum"] = F["d_gl"] + F["d_co66"] + F["d_pe66"] + F["d_po66"] + F["d_fo"]
req(abs((F["AG132_v13"] - F["AG132_v12"]) - F["bridge_sum"]) < TOL,
    f"bridge ties to the cent: {F['bridge_sum']:,.2f} = AG132 delta {(F['AG132_v13'] - F['AG132_v12']):,.2f}")

# ---------------------------------------------------------------- scenarios (recalculated on the v13 content)
def scen(key):
    p = os.path.join(SCEND, key, "out")
    fn = [x for x in os.listdir(p) if x.endswith(".xlsx")]
    assert len(fn) == 1, p
    wb = openpyxl.load_workbook(os.path.join(p, fn[0]), data_only=True)
    ag = n(wb["COO P&L"]["AG132"].value)
    po = sum(n(wb["PO"][f"AG{r}"].value) for r in (33, 34, 35))
    wb.close()
    return ag, po

F["scen_booked"] = F["AG132_v13"]
F["scen_b131"], F["scen_b131_po_base"] = scen("b131")
F["scen_b135"], _ = scen("b135")
F["scen_b132"], _ = scen("b132")
F["scen_b131_b135"], _ = scen("b131b135")
F["scen_b132_b131"], _ = scen("b132b131")
hl = F["AG132_v13"]
req(abs(F["scen_b131_po_base"] - 590317.51) < 0.02, f"B131 = 0 base {F['scen_b131_po_base']:,.2f} = 590,317.51")
CARRY = {"scen_b131": -558996.25, "scen_b135": -126908.44, "scen_b132": -60695.09,
         "scen_b131_b135": -639400.17, "scen_b132_b131": -592410.57}
for k, d12 in CARRY.items():
    req(abs((F[k] - hl) - d12) < 2.0, f"{k}: delta {(F[k] - hl):,.2f} = v12's {d12:,.2f} (orthogonal to v13 edits)")
F["d_b131"] = round(F["scen_b131"] - hl, 2)
F["d_b135"] = round(F["scen_b135"] - hl, 2)
F["d_b132"] = round(F["scen_b132"] - hl, 2)
F["d_idle_at_b131"] = round(F["scen_b131_b135"] - F["scen_b131"], 2)

# ---------------------------------------------------------------- recomputed caveat effects
F["d_i41"] = -F["i41_effect"]
F["burden_upside"] = round(F["lw_in_sal"] * ((b5 + b6) - (co_d6 + co_d7)), 2)
F["d_burden"] = F["burden_upside"]
F["d_i37_cope"] = -round((0.0765 - co_d6) * F["hcco_v13_z"][0] + (0.0765 - b5) * F["lw_in_sal"]
                         + (0.0765 - pe_d6) * F["hcpe_v13_z"][0] + (0.0765 - po_d6) * F["pm_z"], 2)
d61_v12 = n(v12["Collation Notes"]["D61"].value)
F["d_i37_fofe"] = round(d61_v12 + (F["b11_payroll"] / (1 + 0.068 + 0.164)) * 0.0085, 2)
F["caveat_rows"] = [[37, "d_b131"], [38, "d_b135"], [39, "d_b132"], [40, None], [41, "d_i41"], [42, None],
                    [43, "d_burden"], [45, None], [46, None], [48, None], [52, None], [53, None], [54, None],
                    [55, None], [56, None], [57, None], [58, None], [59, None], [60, "d_i37_cope"],
                    [61, "d_i37_fofe"], [62, None], [63, None], [64, None], [65, None], [66, None]]
cn12 = v12["Collation Notes"]
carried = {r: n(cn12[f"D{r}"].value) for r, k in F["caveat_rows"] if k is None}
F["carried_D"] = carried

# ---------------------------------------------------------------- sign-flip / range / conclusion texts
ups = {"I-32 full": 1353574.20, "I-32 trend": 276163.88, "I-32 trend from Sep-26": 403624.13,
       "A-14 month-after": 295806.56, "I-35": carried[62], "I-39": carried[64], "O1": carried[40],
       "I-34": carried[58], "A-14 mid-month": carried[65], "burden rates": F["burden_upside"],
       "9-of-9 MH-01": carried[42], "I-31 double count": carried[53], "I-36": carried[63]}
pos_alone = {k: v for k, v in ups.items() if hl + v > 0}
F["rev_to_zero_pct"] = -hl / F["rev_v13"]
F["text_signflip"] = (
    f"Sign-flip statement (computed, v13): the headline itself is NEGATIVE: {money(hl)} (v12 {money(F['AG132_v12'])}; "
    "the user-approved 2026-10-12 additions move it by "
    f"{money(F['bridge_sum'])}). Downsides no longer flip the sign - they deepen it (largest: the B131 = 0 scope "
    f"sensitivity {money(F['d_b131'])} -> {money(F['scen_b131'])}; I-10 {money(carried[48])} -> "
    f"{money(hl + carried[48])}). Single quantified UPSIDES that make the contribution positive on their own: "
    + (", ".join(f"{k} +{money(v)} -> {money(hl + v)}" for k, v in sorted(pos_alone.items(), key=lambda kv: -kv[1]))
       if pos_alone else "none")
    + ". No other single quantified item does (next largest: I-32 trend continued from Sep-26 "
    f"+{money(ups['I-32 trend from Sep-26'])} -> {money(hl + ups['I-32 trend from Sep-26'])}; A-14 month-after "
    f"+{money(ups['A-14 month-after'])} -> {money(hl + ups['A-14 month-after'])}). With costs held fixed, revenue "
    f"{money(-hl)} ({F['rev_to_zero_pct']:.1%}) ABOVE plan is needed to bring the contribution to zero.")
F["text_upside"] = (
    f"Upside: I-32 can add up to 1,353,574 (contribution {money(hl + 1353574.20)}); the trend alternative adds "
    f"276,164 ({money(hl + 276163.88)}), or 403,624 ({money(hl + 403624.13)}) if the decline also ran through "
    f"Oct-Dec 26. Labour already in the unit cost (O1): up to +{money(carried[40])} ({money(hl + carried[40])}). "
    f"Logistics at CO HC burden rates +{money(F['burden_upside'])} (v12 19,396; smaller: only 5 model seats remain "
    f"in CO). MH-01 on the 9-of-9 reading +{money(carried[42])}. I-35 (PE transfer) +{r5(carried[62])} (one person; "
    f"exact in the caveat row on this sheet); I-39 +{money(carried[64])}; I-34 +{money(carried[58])}.")
lb1_items = [F["d_i41"], carried[48], carried[52], carried[45], carried[46], F["d_b135"]]
F["lb1"] = hl + sum(lb1_items)
lb2_items = [F["d_b131"], carried[48], carried[52], -5286.0, F["d_idle_at_b131"]]
F["lb2"] = hl + sum(lb2_items)
F["ub"] = hl + 1353574.20
F["text_range"] = (
    f"Range (v13): asymmetric by construction, as in v7-v12. Lower bound 1, booked policy, all quantified downsides "
    f"(I-41 restated {r5(F['d_i41'])}; I-10 {money(carried[48])}; I-31 shortfall {money(carried[52])}; I-05 "
    f"burden capitalised {money(carried[45])}; rate base of the current staff (O7) {money(carried[46])}; idle-month "
    f"labour expensed (I-40) {money(F['d_b135'])}): {money(F['lb1'])}. Lower bound 2, the same under the scope "
    f"sensitivity, components at B131 = 0 (sensitivity {money(F['d_b131'])}; I-10 {money(carried[48])}; I-31 "
    f"shortfall {money(carried[52])}; I-05 burden at the B131 = 0 rate (5,286); idle-month labour at B131 = 0 "
    f"{money(F['d_idle_at_b131'])}; I-41 is 0 there: r16 is expensed inside PO 5110-5140): {money(F['lb2'])}. "
    f"Upper end, I-32 in full only: {money(F['ub'])}. Not in the range: I-37 (unverified upper bound, recomputed "
    f"{money(F['d_i37_cope'])} CO/PE/PO and {money(F['d_i37_fofe'])} FO/FE); B132 = 1 (only with a 2026 "
    f"restatement); the O1, burden-rate, 9-of-9 and I-35/I-39/I-34 upsides. v12 range: (469,929) to 1,512,711 "
    f"(lower bound 2 (909,032)).")
F["text_conclusion"] = (
    f"Conclusion: the user additions of 2026-10-12 (brief v7: CO 7700 +24,000 and 8600 +78,000; brief v8: the HC "
    f"roster merge - 4 CO adds, 5 PE adds, the PO Production Manager, the FE Associate, I-28 resolved) move the "
    f"2027 COO contribution from {money(F['AG132_v12'])} (v12) to {money(hl)}: NEGATIVE at the booked policy. "
    f"Bridge: CO GL adds {money(F['d_gl'])}; CO payroll net {money(F['d_co66'])}; PE payroll {money(F['d_pe66'])}; "
    f"PO Production Manager {r5(F['d_po66'])} (one person; exact in the v13 block below); I-28 resolution "
    f"+{money(F['d_fo'])}. Treat {money(hl)} as a point "
    f"estimate inside {money(F['lb1'])} to {money(F['ub'])} (lower bound 2: {money(F['lb2'])}) until Decisions #2 "
    f"(I-32) and #10 (I-40) are answered, I-10 is confirmed, and the PO owner answers the restated I-41 (the Team "
    f"Lead's Nov-26 end date and seat TL-01).")

# ---------------------------------------------------------------- recon table rows 257-261 (FO PO CO FE PE)
fo_5510 = sum(cell(s1, "FO", f"AG{r}") for r in (52, 53, 54))
F["recon_table"] = [
    [F["hccoo_people"][1], cell(s1, "HC-COO", "Z39"), fo_5510],
    [F["hccoo_people"][0], F["hcpo_v13_z"][3], f"0 booked; B131 = 0: 590,318; PM expensed 6610-6640: {money(F['po66_v13'])}"],
    [F["hccoo_people"][4], F["hcco_v13_z"][3], F["co66_v13"]],
    [F["hccoo_people"][2], F["hcfe_v13_z"][3], sum(cell(s1, "FE", f"AG{r}") for r in (67, 68, 69))],
    [F["hccoo_people"][3], F["hcpe_v13_z"][3], F["pe66_v13"]],
]

# ---------------------------------------------------------------- 2026-side HC cells (Sep-Dec 26 starters), disclosed
hc2026 = {}
for d in ("CO", "PO", "FE", "PE"):
    tots12 = [cell(v12, f"HC-{d}", f"{c}70") for c in "IJKL"]
    tots13 = [cell(s1, f"HC-{d}", f"{c}70") for c in "IJKL"]
    hc2026[d] = [round(b - a, 2) for a, b in zip(tots12, tots13)]
F["hc2026_delta"] = hc2026

# ---------------------------------------------------------------- v13 block for the Collation Notes sheet
B = []
A = B.append
A(["Changes from v12 (v13) - user additions of 2026-10-12 (briefs v7 + v8 as amended); all figures computed by figures_v13.py"])
A(["v13 headline: 2027 COO contribution (COO P&L!AG132) = " + money(hl, 2) + f" (v12 {money(F['AG132_v12'], 2)}; change {money(F['AG132_v13'] - F['AG132_v12'], 2)})."])
A(["Bridge from v12 (ties to the cent; every term = the department's 2027 GL-line change)"])
A(["#", "Change", "Effect on AG132", "New cells"])
A(["A", "CO GL 7700 Inventory Obsolescence-old 24,000 (2,000/mo) + GL 8600 Repairs and Maintenance 78,000 (6,500/mo); label '-old' flagged for the user (I-42); 8600 = +153% vs 2026 30,775, user-directed", round(F["d_gl"], 2), "CO!S98, S106 (R stays 'Even')"],)
A(["B+D", f"CO 6610-6640: roster adds (HC-CO: Material Handler, MH Team Lead (2027 = 0, end-dated Nov-26), Material Flow Supervisor, Applications Engineer) less the de-duplicated model seats (TL-01, MH-01, MH-02 out; {money(F['lw_out_total'], 2)}): {money(F['co66_v12'], 2)} -> {money(F['co66_v13'], 2)}", round(F["d_co66"], 2), "CO!U67:AF69 (+ 'HC-CO' rows)"])
A(["C", f"PE 6610-6640 wired live to 'HC-PE' rows 67-69 (decision 1), incl. 5 adds: {money(F['pe66_v12'], 2)} -> {money(F['pe66_v13'], 2)}", round(F["d_pe66"], 2), "PE!U67:AF69 (+ 'HC-PE' rows)"])
A(["E", f"PO 6610-6640 = Production Manager (decision 3; 125,000 Oct-26 at PO HC rates, live links; NOT in the capitalised base): 0 -> {money(F['po66_v13'], 2)} ({money(F['po66_v13_rows'][0], 2)} / {money(F['po66_v13_rows'][1], 2)} / {money(F['po66_v13_rows'][2], 2)})", round(F["d_po66"], 2), "PO!U67:AF69 (+ 'HC-PO' r41)"])
A(["F", f"Fld Ops Payroll B11 14 -> 13 (decision 4; I-28 RESOLVED): FO 5510/5530/5540 {money(F['b11_payroll'], 2)} and 5330 {money(F['b11_5330'], 2)} lower", round(F["d_fo"], 2), "Fld Ops Payroll!B11"])
A(["G", "PO 5110-5140 re-anchored to the live 8-production-staff basis SUM('HC-PO'!M14:M33) x (1, D6, D7) + idle rows (B131 = 0 base unchanged 590,317.51; booked value unchanged 0)", 0, "PO!U33:AF35"])
A(["H", "Notes, Collation Notes, caveats/range/sign-flip recomputed; I-28 RESOLVED; I-41 restated; I-38 narrowed; I-42 added", "-", "this sheet; 02-build_notes_v13.md"])
A(["Total", "", round(F["bridge_sum"], 2), f"AG132 {money(F['AG132_v12'], 2)} -> {money(hl, 2)}"])
A([])
A(["Logistics&WH seat in/out (2027 $ at model rates incl. 2027 new-hire cost; de-dup by formula in CO!U67:AF69)"])
A(["Seat", "In CO v12", "In CO v13", "2027 cost", "Why"])
for code, why in [("LOG-01", "roster r17 (since v10)"), ("MH-01", "moved to HC-CO r19 (roster)"),
                  ("TL-01", "realized on HC-CO r20 (end-dated Nov-26; I-41)"),
                  ("MH-02", "realized by the Material Flow Supervisor backfill (HC-CO r35; user-confirmed, A-46)")]:
    A([code, "no" if code == "LOG-01" else "yes", "no", round(SEATS[code]["cost27"], 2), why])
for code in IN_SEATS:
    A([code, "yes", "yes", round(SEATS[code]["cost27"], 2), f"model seat, no roster ({SEATS[code]['start']})"])
A(["Out in v13 (3 seats)", "", "", round(F["lw_out_total"], 2), "TL-01 + MH-01 + MH-02"])
A(["Still in (5 seats + hire costs)", "", "", round(F["lw_added_v13"], 2), f"salaries {money(F['lw_in_sal'], 2)} + tax {money(F['lw_in_tax'], 2)} + benefits {money(F['lw_in_ben'], 2)} + new-hire {money(F['lw_in_nh'], 2)}"])
A(["MH-02 / TL-01 2026 hire costs", "", "", 0, "1,000 each in Oct-26 / Dec-26 model columns; not in 2027 (verified)"])
A([])
A(["HC roster 2027 salary totals (Z67) - ours vs the user's file (completion criterion)"])
A(["Tab", "v12", "v13", "user's file", "difference"])
for d in ("CO", "PO", "FE", "PE"):
    A([f"HC-{d}", round(F[f"hc{d.lower()}_v12_z"][0], 2), round(F[f"hc{d.lower()}_v13_z"][0], 2), round(user_z[d], 2),
       round(F[f"hc{d.lower()}_v13_z"][0] - user_z[d], 2)])
A(["Note: HC-CO matches because r20 (MH Team Lead) carries the user's own end month Nov-26 and so costs 0 in 2027 (A-47; the same person stays on HC-PO r16 inside the capitalised B131 base - I-41)."])
A([])
A(["2026-side HC cells (Sep-Dec 26 columns I:L, Total Payroll row 70) moved by the Sep-Dec 26 starters (disclosed; the six P&L sheets' 2026 columns B:N are unchanged - 2026 P&L is book data and reads no HC tab)"])
A(["Tab", "Sep-26", "Oct-26", "Nov-26", "Dec-26"])
for d in ("CO", "PO", "FE", "PE"):
    A([f"HC-{d}"] + hc2026[d])
A(["HC-COO roll-up follows (same months); its 2027 columns and Z totals also move with the roster edits."])
A([])
A(["New assumptions (v13)"])
A(["A-46", "The Material Flow Supervisor (85,000, Nov-26, HC-CO r35) IS the realized backfill that the logistics model carries as seat MH-02 (user 2026-10-12: the backfill 'should be included'; orchestrator mapping). If wrong, one formula term per CO row flips: re-add row 39 to CO!U67:AF69 (+" + money(F["seat_MH-02"], 2) + ")."])
A(["A-47", "HC-CO r20 (MH Team Lead) end month Nov-26 is the user's file's own value (their edit; the brief named only '57,554 Sep-26'). It makes the row's 2027 cost 0 while the same person stays on HC-PO r16. If the person should instead be costed in CO through 2027: HC-CO F20 = Dec-27 (one cell, +" + money(F["tl_roster_2027_cost"], 2) + " at CO HC rates). See I-41."])
A(["A-48", "Production Manager timing: Oct-26 start on HC-PO r41 (New Hires); his Oct-Dec 26 cost sits on the HC tab only (no 2026 P&L change - 2026 is book data); 2027 fully expensed in PO 6610-6640; 3% raise Oct-27 per the roster row."])
A(["New issue (v13)"])
A(["I-42", "LOW", "CO!A98; CO!S98", "The 7700 row the user's 2,000/month was booked to is labelled '7700 - Inventory Obsolescence-old' - the only 7700 row in the book, but the '-old' suffix suggests a retired account. User to confirm the intended account; 2026 actuals on the row are 0.", "User asked for 'GL 7700 in CO' (2026-10-12); label read from CO!A98.", "0 (classification only)", "hygiene", "Confirm the account; move S98 if a different 7700 row is meant."])
A(["8600 flag", "", "CO!S106", f"8600 Repairs and Maintenance 2027 = 78,000 vs 2026 {money(F['co8600_2026'], 2)} (+{(78000 / F['co8600_2026'] - 1):.0%}), above the variance-scan threshold; user-directed 2026-10-12 (brief v7).", "", "", "", ""])
A([])
A(["Scenario switches (scratch copies of the v13 build, one/two typed inputs flipped, LibreOffice full recalc)"])
A(["Scenario", "AG132", "vs booked", "Check"])
A(["Booked (B131 = 1, B132 = 0, B135 = 1)", round(hl, 2), "-", ""])
A(["B131 = 0 (current staff expensed)", round(F["scen_b131"], 2), round(F["scen_b131"] - hl, 2), f"PO 5110-5140 base {money(F['scen_b131_po_base'], 2)} (= 590,317.51; live 8-staff basis, PM not in it)"])
A(["B135 = 0 (idle-month labour expensed)", round(F["scen_b135"], 2), round(F["scen_b135"] - hl, 2), ""])
A(["B132 = 1 (Sep-Dec 26 labour capitalised; needs 2026 restatement)", round(F["scen_b132"], 2), round(F["scen_b132"] - hl, 2), ""])
A(["B131 = 0 and B135 = 0", round(F["scen_b131_b135"], 2), round(F["scen_b131_b135"] - hl, 2), ""])
A(["B132 = 1 and B131 = 0", round(F["scen_b132_b131"], 2), round(F["scen_b132_b131"] - hl, 2), ""])
A([])
A(["YoY footnote (extended for the new hires): 2026 vs 2027 is not like-for-like. 2026 expensed production labour (2027 capitalises it), and the 2027 payroll adds 10 user-approved 2026-10-12 hires/moves (4 CO, 5 PE, 1 PO) plus the CO 7700/8600 lines that have little or no 2026 spend. The Sep-Dec 26 costs of the new starters are on the HC tabs only - the 2026 P&L columns are book data and were not restated. On the 2026 policy AND before these additions the 2027 contribution would differ by both effects; see the md for the policy-effect recompute."])
A(["Full v13 notes: 02-build/02-build_notes_v13.md. The in-place updates above (decision table rows 13-14, caveat rows 31-71, CO block rows 74-95, reconciliation rows 250-261, issue rows I-06/I-17/I-28/I-38/I-41) describe v13; historical v7-v12 sections stand as records of those builds."])
F["v13_block"] = B

json.dump(F, open(OUT, "w"), indent=1)
print(f"figures_v13: {len(F)} keys -> {OUT}")
if fails:
    print(f"figures_v13: {len(fails)} FAILED assertions"); sys.exit(1)
