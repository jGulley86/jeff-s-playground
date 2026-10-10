"""Write 02-build_notes_v8.md and the v8 Collation Notes content (JSON).

Usage:
  python3 -I report_v8.py V7_MD CN7_JSON V7_XLSX V8_XLSX FIG8_JSON FIG7_JSON RECON_JSON SPEC_JSON NOISE_JSON LO_VERSION_TXT
                          WORKFILE COO SD NEW OUT_NOTES_JSON OUT_MD [ANALYZE_JSON]

v8 = production labour capitalised (brief v5). Text is built from the shipped v7 notes (md and the v7 Collation Notes,
extracted byte-exactly by cnotes_v6.py); each edit of carried text is a targeted replacement that must hit exactly once.
Numbers: V8_XLSX cached values (= LibreOffice recalculation), FIG8_JSON (figures_v8.py: replicas, scenarios, bridge),
FIG7_JSON / RECON_JSON (v7 figures that do not change). Carried caveat rows keep their v7 effect and act on the v8
headline. No figure is typed here.
PRIVACY: md only - per-person amounts for identified employees are rounded to the nearest $5k by paylist_v8.round_text
(paylist_v7 rule); a per-person amount that is a multiple of $5k is unchanged by rounding and stays exact (stated in the
banner, counted by paylist_v8). The Collation Notes sheet keeps exact figures. No names are read here.
Without ANALYZE_JSON the md has placeholders for the check sections (pass 1); the Collation Notes JSON does not depend on
ANALYZE_JSON, so both passes must give the same JSON.
"""
import sys, os, json, re, hashlib, copy, collections
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paylist_v8

(V7_MD, CN7, V7X, V8X, FIG8, FIG7, RECON, SPEC, NOISE, LOV, WFILE, COO, SD, NEW, OUT_JSON, OUT_MD) = sys.argv[1:17]
AN = json.load(open(sys.argv[17])) if len(sys.argv) > 17 else None
F = json.load(open(FIG8)); F7 = json.load(open(FIG7)); R = json.load(open(RECON)); SPECJ = json.load(open(SPEC)); NZ = json.load(open(NOISE))
cn7 = json.load(open(CN7)); md7 = open(V7_MD).read(); lov = open(LOV).read().strip()
w7 = openpyxl.load_workbook(V7X, data_only=True); w8 = openpyxl.load_workbook(V8X, data_only=True)
BANNER = "CONFIDENTIAL – contains named compensation data (HC-* tabs); restrict distribution"
DSQ = "'Depreciation Schedule'"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def f0(x):
    if x is None: return ""
    x = float(x)
    if abs(x) < 0.5: return "0"
    return f"({abs(x):,.0f})" if x < 0 else f"{x:,.0f}"


def f2(x):
    x = float(x)
    if abs(x) < 0.005: return "0.00"
    return f"({abs(x):,.2f})" if x < 0 else f"{x:,.2f}"


def eff(x):
    x = float(x)
    if abs(x) < 0.5: return "0"
    return f"+{x:,.0f}" if x > 0 else f"({abs(x):,.0f})"


def pct(x, d=1):
    return f"{x * 100:.{d}f}%"


def r5(x):
    return round(abs(x) / 5000) * 5000 * (1 if x >= 0 else -1)


def rep(text, old, new, count=1):
    n = text.count(old)
    assert n == count, (n, old[:100])
    return text.replace(old, new)


def mdtable(header, rows, align=None):
    align = align or ["---"] * len(header)
    out = "| " + " | ".join(header) + " |\n|" + "|".join(align) + "|\n"
    for r in rows:
        out += "| " + " | ".join("" if v is None else str(v) for v in r) + " |\n"
    return out


def md_issue(row):
    return "| " + " | ".join(str(x) for x in row) + " |"


def num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0


def val(w, col, rows):
    return sum(num(w["COO P&L"][f"{col}{r}"].value) for r in rows)


def pct_nm(new, base):
    if base is None or base <= 0 or new < 0:
        return "n/m"
    return f"{(new - base) / base * 100:.0f}%"


# ------------------------------------------------------------------ figures
E = F["effects"]; LB = F["labour"]; X = F["exposures"]; SC = F["scen"]; BR = F["bridge"]; PPF = F["prodpay"]; MEMO = F["memo"]; RM = F["rowmap"]
C = E["C8"]; C7 = E["C7"]
assert abs(C - val(w8, "AG", [132])) < 1e-6 and abs(C7 - val(w7, "AG", [132])) < 1e-6
DEP, DEP_L, DEP_T = LB["dep"], LB["dep_lift"], LB["dep_tray"]
PO7 = E["po_5100_v7"]
S81 = PPF["S"]["total"]; S41, S62, S79 = PPF["S"]["lift"], PPF["S"]["tray"], PPF["S"]["sup"]
CUR9 = LB["cur_2027"]
I05 = F7["I05"]; I17 = F7["I17"]; ev = F7["b1_evidence"]; b2 = F7["b2"]; o1 = F7["o1"]; o6 = F7["o6"]; b3 = F7["b3"]
C_SENS = SC["cur"]["C"]; SENS = X["sens_current_expensed"]; Q4 = X["q4_labour_excluded"]; BOTH = X["both_policy_alternatives"]
MH = X["mh_roles_cost"]; I17_9 = X["i17_9dedup"]; I17_7 = X["i17_7_with_mh"]
O1D = X["o1_dep_pro_rata"]; RRG = X["run_rate_gap_2027"]; I37 = X["i37_co_pe"]
A14S, A14M, A14L = X["a14_start_after"], X["a14_mid"], X["a14_labour_part"]
MON = PPF["months"]
LIFT_COST, TRAY_COST = ev["lift_unit_cost"], ev["tray_unit_cost"]
avg_l, avg_t = MEMO["avg_lift"], MEMO["avg_tray"]
UNITS27 = F["evidence_check"]["builds_2027"]; LIVE27 = F["evidence_check"]["live_2027_built_2027"]

# ------------------------------------------------------------------ caveat rows: carried from v7 (effects unchanged), recomputed, new
carried = collections.OrderedDict()
for row in F["carried_v7_rows"]:
    carried.setdefault(row[0], []).append(list(row))


def car(item, k=None):
    rows = carried[item] if k is None else [carried[item][k]]
    out = []
    for r in rows:
        r = list(r)
        if isinstance(r[3], (int, float)):
            r[4] = C + r[3]
        elif r[0] == "I-26":
            r[4] = C
        out.append(r)
    return out


SRC_SW = f"{DSQ}!B{RM['sw_current']}:B{RM['sw_q4']}; PO!U33:AF35"
cav = []
cav.append(["Decision #1 scope: current 9 expensed (sensitivity, not booked)", "downside",
            f"If only the ramp is capitalised and the 9 current PO staff stay expensed, PO 5110-5140 returns to its v7 amount ({f0(PO7)}), 2027 "
            f"capitalised labour falls to {f0(SC['cur']['cap_2027'])} and its 2027 depreciation to {f0(SC['cur']['dep_lab'])} (booked: {f0(DEP)}). "
            f"Recalculated with the workbook switch {DSQ}!B{RM['sw_current']} = 0.", SENS, C + SENS, SRC_SW, False])
cav.append(["Decision #1 scope: Oct-Dec 26 labour not capitalised", "upside",
            f"2026 expensed production labour (COO 5100 {f0(ev['coo_5100_2026'])} in 2026), so the Oct-Dec 26 model labour in the Jan-Feb 27 go-lives "
            f"({f0(LB['from26_to_2027'])}) may not be capitalisable. Without it 2027 labour depreciation is {f0(SC['q4']['dep_lab'])}. Switch B{RM['sw_q4']} = 0.",
            Q4, C + Q4, f"{DSQ}!B{RM['sw_q4']}; rows 143-145 (B:E)", False])
cav.append(["Decision #1 scope: both alternatives", "downside", "Current 9 expensed and no Oct-Dec 26 labour capitalised (B131 = 0, B132 = 0), recalculated.",
            BOTH, C + BOTH, SRC_SW, False])
cav.append(["I-41 (7-overlap): material-handling roles stay expensed", "downside",
            "PO 5110-5140 = 0 also removes the 2 material-handling roles (PO HC r16 Material Handling Team Lead, r20 Material Handler). On the 7-of-9 role "
            "reading they are warehouse staff (Logistics&WH), not production labour, so their cost stays an expense: the 2 people together at PO HC rates.",
            -MH, C - MH, "'HC-PO'!C16:Z16, C20:Z20, D6:D7; PO!U33:AF35", False])
cav.append(["I-05 burden (O1), capitalised", "downside",
            f"The ramp at PO HC burden rates (+{o1['diff']:,.0f} of 2027 cost, v7 O1) is now capitalised, so only its depreciation reaches 2027 (pro rata: "
            f"{pct(X['ratio_dep_per_2027_payroll'], 2)} of 2027 payroll is depreciated in 2027 under the booked method without Oct-Dec 26 labour).",
            -O1D, C - O1D, "Prod Payroll!B6:C7, H6:H7; 'HC-PO'!D6:D7", False])
cav.append(["Run rate: 2026 go-lives carry no labour", "downside",
            f"The existing-fleet run rate (PO Dec-26) holds no labour. Under the same policy the Sep-26 model labour ({f0(X['run_rate_sep26_labour'])}) sits in "
            f"the Nov-26 go-lives: 12 months of 2027 depreciation. Earlier 2026 go-lives: not determinable (no 2026 labour by build month before Sep-26).",
            -RRG, C - RRG, f"{DSQ}!B{RM['pool_lift']}, B{RM['pool_tray']}, row {RM['lab_2026']}; PO!M20:M21", False])
cav += car("I-17")
cav.append(["I-17 deduplicated, 9-overlap", "downside",
            f"On the 9-of-9 count reading PO HC r20 is one of Prod Payroll's 9 current staff, now capitalised; Logistics&WH seat MH-01 (r20 by name) is then a "
            f"new seat (+{b2['mh01_cost']:,.0f}).", -I17_9, C - I17_9, "SD Logistics&WH Payroll MH-01; Prod Payroll B9:C9", False])
cav.append(["I-17 + I-41, 7-overlap", "downside", "The 7 Logistics&WH seats plus the 2 material-handling roles staying expensed (I-41); no seat counted twice.",
            -I17_7, C - I17_7, "as above", False])
cav += car("I-10") + car("I-26") + car("I-28", 0) + [car("I-28", 1)[0] + [True]] + car("I-31") + car("I-32") + car("I-33") + car("I-34") + car("I-34 with FE tax at 7.65%")
cav.append(["I-37", "downside", f"CO and PE payroll tax uses the HC T&B rates (CO {pct(o6['depts']['CO']['hc_rate'], 2)}, PE {pct(o6['depts']['PE']['hc_rate'], 2)}), "
            f"below {pct(o6['fica'], 2)}; at {pct(o6['fica'], 2)} on every salary dollar (upper bound). v8: PO's part (v7 {f0(X['i37_po_part_v7'])}) is gone: PO "
            f"production payroll is capitalised at the model's own rates.", -I37, C - I37, "'HC-CO'!D6; 'HC-PE'!D6; CO!AG68; PE!AG68", False])
cav.append(car("I-37", 1)[0])
cav += [car("I-35")[0] + [True]] + car("I-36") + car("I-39")
cav.append(["A-14", "upside", f"Depreciation convention: mid-month in the go-live month instead of a full month (new units and, from v8, their capitalised labour: "
            f"+{A14L / 2:,.0f} of it).", A14M, C + A14M, "'Depreciation Schedule'!B13", False])
cav.append(["A-14", "upside", f"Depreciation convention: start the month after go-live (B13 = 1), recalculated; of which capitalised labour +{A14L:,.0f}.",
            A14S, C + A14S, "'Depreciation Schedule'!B13 = 1", False])
cav += car("A-22")
cav = [r if len(r) == 7 else r + [False] for r in cav]
assert carried["I-28"][1][2].startswith("Same person") and carried["I-37"][1][2].startswith("FO and FE")


def cav_md_row(r):
    e, a, person = r[3], r[4], r[6]
    if isinstance(e, (int, float)) and person:
        es = ("+" if e > 0 else "-") + f"~{abs(r5(e)):,.0f}"
        as_ = f"~{r5(C + r5(e)):,.0f}"
        return [r[0], r[1], r[2] + " (per-person amount rounded to $5k)", es, as_, r[5]]
    es = eff(e) if isinstance(e, (int, float)) else e
    as_ = f0(a) if isinstance(a, (int, float)) else a
    return [r[0], r[1], r[2], es, as_, r[5]]


# ------------------------------------------------------------------ sign flip and range
i10 = carried["I-10"][0][3]; i31s = [r for r in carried["I-31"] if r[3] < 0][0][3]
i32full = max(r[3] for r in carried["I-32"])
i32tr = [r for r in carried["I-32"] if r[2].startswith("Trend alternative:")][0][3]
i32tr2 = [r for r in carried["I-32"] if r[2].startswith("Trend alternative continued")][0][3]
DOWN = {"the sensitivity (current 9 expensed)": SENS, "I-17 + I-41 (7-overlap)": -I17_7, "I-17 deduplicated (9-overlap)": -I17_9, "I-17": -I17,
        "I-10": i10, "I-31 shortfall": i31s}
single_flip = [k for k, v in DOWN.items() if C + v < 0]
I17SET = {"I-17 + I-41 (7-overlap)", "I-17 deduplicated (9-overlap)", "I-17"}
pairs = []
keys = list(DOWN)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = keys[i], keys[j]
        if a in I17SET and b in I17SET: continue
        if "sensitivity" in a and b == "I-17 + I-41 (7-overlap)": continue          # under the sensitivity the MH roles are already expensed
        if C + DOWN[a] + DOWN[b] < 0:
            pairs.append((a, b, C + DOWN[a] + DOWN[b]))
LB1 = C - I17_7 + i10 + i31s - O1D - RRG
LB2 = C_SENS - I17_9 + i10 + i31s - O1D - RRG
UB = C + i32full
assert LB2 < LB1 < C < UB
sf = []
sf.append(f"Sign-flip statement (computed, v8): with production labour capitalised the 2027 COO contribution is {f0(C)} (v7 {f0(C7)}). "
          + ("No single quantified item turns it negative" if not single_flip else "It turns negative on " + " or ".join(single_flip) + " alone")
          + f": the largest single downsides leave {f0(C + SENS)} (scope sensitivity: current 9 expensed), {f0(C - I17_7)} (I-17 + I-41 at the 7-overlap), "
          f"{f0(C - I17_9)} (I-17 deduplicated, 9-overlap) and {f0(C + i10)} (I-10). Pairs that turn it negative: "
          + "; ".join(f"{a} + {b} {f0(v)}" for a, b, v in pairs) + ".")
sf.append(f"Upside: I-32 can add up to {f0(i32full)} (contribution {f0(C + i32full)}); the trend alternative adds {f0(i32tr)} ({f0(C + i32tr)}), or {f0(i32tr2)} "
          f"({f0(C + i32tr2)}) if the decline also ran through Oct-Dec 26. Policy scope: without the Oct-Dec 26 labour {eff(Q4)} ({f0(C + Q4)}). Smaller: A-14 "
          f"+{A14M:,.0f} to +{A14S:,.0f}, I-28 +{carried['I-28'][0][3]:,.0f} to +~{r5(carried['I-28'][1][3]):,.0f}, I-34 +{carried['I-34'][0][3]:,.0f}, I-35 up to "
          f"+~{r5(carried['I-35'][0][3]):,.0f}, I-36 +{carried['I-36'][0][3]:,.0f}, I-39 up to +{carried['I-39'][0][3]:,.0f}. With costs held fixed, revenue "
          f"{f0(C)} ({C / E['rev'] * 100:.1f}%) below plan also takes the contribution to zero.")
sf.append(f"Range (v8): asymmetric by construction, as in v7. Lower bound 1, booked policy, all quantified downsides (I-17 + I-41 at the 7-overlap, the more "
          f"adverse reading; I-10; I-31 shortfall; I-05 burden capitalised; run-rate labour): {f0(LB1)}. Lower bound 2, the same under the scope sensitivity "
          f"(current 9 expensed; I-17 deduplicated at the 9-overlap, the more adverse reading there): {f0(LB2)}. Upper end, I-32 in full only: {f0(UB)}. I-37 "
          f"(unverified upper bound) is not in the range. v7 range: (2,723,481) to 1,492,606 (with production labour expensed).")
sf.append(f"Conclusion: capitalising production labour (Decision #1) moves the 2027 COO contribution from {f0(C7)} to {f0(C)}, and with it the sign question: "
          f"no single quantified item now turns it negative, but two together can (the pairs listed above). Treat {f0(C)} as a point "
          f"estimate inside {f0(LB1)} to {f0(UB)} (lower bound 2 with the current staff expensed: {f0(LB2)}) until Decisions #10, #6 and #2 (I-40, I-17, I-32) "
          f"are answered.")

# ------------------------------------------------------------------ decisions pending
dp7 = cn7["sections"][1]
assert dp7["heading"].startswith("Decisions pending") and len(dp7["table"]["rows"]) == 9
DEC = []
for r in dp7["table"]["rows"]:
    r = list(r)
    if r[0] == "1":
        r = ["1", "RESOLVED (user-confirmed 2026-10-10: 'production labor is capitalized. Use the same formula as the file has.'). Production labour: expensed, "
             "or capitalised into the unit cost?", "I-05 (RESOLVED), I-23, I-40",
             f"Booked in v8: all Prod Payroll labour is capitalised (model 2027 {f0(S81)}, the 9 current staff included) and depreciated by the Depreciation "
             f"Schedule logic: 5011 +{DEP_L:,.0f}, 5012 +{DEP_T:,.0f}; PO 5110-5140 2027 = 0 (v7 {f0(PO7)}). Contribution {f0(C)} (v7 {f0(C7)}).",
             "Resolved. The scope (current staff, Oct-Dec 26 labour) is Decision #10.", "User (resolved)"]
    elif r[2] == "I-05, I-17":
        r[3] = (f"v8: the Prod Payroll model (ramp and current 9) is in the budget as capitalised labour (Decision #1). The Logistics&WH model is not: PO "
                f"5110-5140 held the 9 current PO HC staff, now 0 (capitalised).")
        r[4] = (f"Add the 7 new Logistics&WH seats: ({I17:,.0f}); deduplicated at the 9-overlap ({I17_9:,.0f}) (MH-01 then a new seat); at the 7-overlap the 2 "
                f"material-handling roles also stay expensed: ({I17_7:,.0f}) (I-41). Keep as is: 0. (The Prod Payroll ramp is no longer an expense: Decision #1.)")
        r[1] = "Warehouse payroll (Logistics&WH) and the material-handling roles"
        r[2] = "I-17, I-41"
    DEC.append(r)
DEC.append(["10", "Scope of the capitalisation policy: are the 9 current production staff and the Oct-Dec 26 model labour (in the Jan-Feb 27 go-lives) "
            "capitalised too? 2026 expensed COO 5100 production labour, so the 2026 policy may have been partial.", "I-40",
            f"Both capitalised (brief v5 primary case): 'Depreciation Schedule'!B{RM['sw_current']} = 1, B{RM['sw_q4']} = 1.",
            f"Current 9 expensed (sensitivity): ({abs(SENS):,.0f}) -> {f0(C + SENS)}. Oct-Dec 26 labour not capitalised: {eff(Q4)} -> {f0(C + Q4)}. Both: "
            f"({abs(BOTH):,.0f}) -> {f0(C + BOTH)}. Each is one switch on the Depreciation Schedule; the workbook recalculates.", "User / Finance"])

# ------------------------------------------------------------------ labour tables
UNITS_L = [num(w8["DeploySum"].cell(24, c).value) for c in range(2, 18)]; UNITS_T = [num(w8["DeploySum"].cell(25, c).value) for c in range(2, 18)]
GOL = [w8["Depreciation Schedule"].cell(RM["golive"], c).value for c in range(2, 18)]
LAG = num(w8["Depreciation Schedule"].cell(RM["lag"], 2).value); LAGCHK = num(w8["Depreciation Schedule"].cell(RM["lag_check"], 2).value)
import datetime as _dt
GOL_TXT = [(g if isinstance(g, _dt.datetime) else _dt.datetime(1899, 12, 30) + _dt.timedelta(days=num(g))).strftime("%b-%y") for g in GOL]
assert GOL_TXT[0] == "Nov-26" and GOL_TXT[-1] == "Feb-28", GOL_TXT
LPU = []
for i in range(16):
    LPU.append([MON[i], f0(PPF["monthly"]["total"][i]), f0(LB["cap_lift"][i]), f0(LB["cap_tray"][i]), f"{UNITS_L[i]:.0f}", f"{UNITS_T[i]:.0f}",
                f0(LB["pool_lift"][i]), f0(LB["pool_tray"][i]), f0(LB["per_lift"][i]), f0(LB["per_tray"][i]), GOL_TXT[i]])
LPU_H = ["Build month", "Prod Payroll (row 81)", "Capitalised: lifts (row 147)", "Capitalised: trays (row 148)", "Lifts built", "Trays built",
         "Lift labour pooled (row 152)", "Tray labour pooled (row 154)", "Labour per lift (row 156)", "Labour per tray (row 157)", "Go-live"]
WHERE = [
    ["Production payroll 2027 (Prod Payroll!S81) = capitalised labour from 2027 payroll", f0(S81), f"B{RM['m_pp_2027']}, B{RM['m_cap_2027']}"],
    ["  into 2027 go-lives (Feb-Oct 27 builds; Jan-27 rolls into Feb-27): depreciated from go-live", f0(LB["to_2027"]), f"B{RM['m_to_2027']}"],
    ["  into 2028 go-lives (Nov-Dec 27 builds): CIP / inventory at Dec-27, no 2027 depreciation", f0(LB["to_2028"]), f"B{RM['m_to_2028']}"],
    ["  waiting for a build at Dec-27", f0(LB["waiting"]), f"B{RM['m_waiting']}"],
    ["Oct-Dec 26 model labour into the Jan-Feb 27 go-lives (Nov-Dec 26 builds; Oct-26 rolls into Nov-26)", f0(LB["from26_to_2027"]), f"B{RM['m_from26_to_2027']}"],
    ["Sep-26 model labour in the Nov-26 go-lives (2026 vintage, inside the PO run rate; not added)", f0(LB["from26_to_2026"]), f"B{RM['m_from26_to_2026']}"],
    ["Depreciable labour in the 2027 go-live vintages (2027 + Oct-Dec 26 labour)", f0(LB["vint_total"]), f"B{RM['m_vint_total']}"],
    ["2027 depreciation of capitalised labour (5011 / 5012)", f"{f0(DEP)} ({f0(DEP_L)} / {f0(DEP_T)})", f"R{RM['out_total']} (rows {RM['out_lift']}-{RM['out_tray']})"],
    ["Capitalised labour in service at Dec-27, net of 2027 depreciation", f0(LB["nbv_end27"]), f"B{RM['m_nbv_end27']}"],
    ["Average labour per unit built in 2027: lift / tray", f"{avg_l:,.0f} ({pct(avg_l / LIFT_COST)} of {LIFT_COST:,.0f}) / {avg_t:,.0f} ({pct(avg_t / TRAY_COST)} of {TRAY_COST:,.0f})",
     f"B{RM['m_avg_lift']}:B{RM['m_avg_tray']}"],
]
SENS_T = [
    ["Booked (primary): all Prod Payroll labour capitalised, incl. the current 9 and Oct-Dec 26 labour", f0(S81), f0(DEP), f0(0), f0(C), "-"],
    ["Sensitivity (shown, not booked): only the ramp capitalised; the current 9 stay expensed", f0(SC["cur"]["cap_2027"]), f0(SC["cur"]["dep_lab"]), f0(PO7),
     f0(C_SENS), eff(SENS)],
    ["Alternative: Oct-Dec 26 labour not capitalised", f0(SC["q4"]["cap_2027"]), f0(SC["q4"]["dep_lab"]), f0(0), f0(SC["q4"]["C"]), eff(Q4)],
    ["Both alternatives", f0(SC["both"]["cap_2027"]), f0(SC["both"]["dep_lab"]), f0(PO7), f0(SC["both"]["C"]), eff(BOTH)],
    ["v7 headline (labour not capitalised; ramp not budgeted)", "-", "0", f0(PO7), f0(C7), eff(C7 - C)],
]
SENS_H = ["Case", "2027 payroll capitalised", "2027 labour depreciation", "PO 5110-5140 2027 (expense)", "2027 COO contribution", "vs booked"]
BRIDGE = [
    ["v7 'capitalised on top' (ramp only; annual average per unit built in 2027; 2027 labour only)", f0(BR["v7_ramp_annual_avg"]), "v7 figure, reproduced"],
    ["+ the current 9 (whole model, v7 method)", eff(BR["step_full_model"]), f"= {f0(BR['v7_method_full_model'])}"],
    ["+ labour per unit by build month, zero-build months rolled forward (A-38)", eff(BR["step_monthly_pooling"]), f"= {f0(BR['monthly_no_q4_labour'])} (= switch B{RM['sw_q4']} = 0)"],
    ["+ Oct-Dec 26 labour in the Jan-Feb 27 go-lives (A-40)", eff(BR["step_q4_labour"]), f"= {f0(BR['monthly_booked'])} (booked)"],
    ["Sensitivity on the same method (ramp only, monthly, incl. Oct-Dec 26 ramp labour)", f0(BR["sens_monthly"]), f"v7 method {f0(BR['sens_v7_method'])}; difference {eff(BR['sens_step'])}"],
]
H = F["hand"]
HAND = [[r["vintage"], r["build"], f"{r['lifts']:.0f}", f2(r["per_lift"]), f"{r['lifts']:.0f} x {f2(r['per_lift'])} / 84 = {f2(r['lift_month'])}",
         f"{r['trays']:.0f}", f2(r["per_tray"]), f"{r['trays']:.0f} x {f2(r['per_tray'])} / 120 = {f2(r['tray_month'])}"] for r in H["rows"]]
HAND.append(["**Hand total Jun-27**", "", "", "", f"**{f2(H['hand_lift'])}**", "", "", f"**{f2(H['hand_tray'])}**"])
HAND.append(["Workbook: PO!Z20 / Z21 v8 - v7", "", "", "", f2(H["po_z20_delta"]), "", "", f2(H["po_z21_delta"])])
HAND_H = ["Go-live vintage", "Built", "Lifts", "Labour per lift", "5011 per month", "Trays", "Labour per tray", "5012 per month"]
XLT = [[x["cell"], f"`{x['old']}`", f"`{x['new']}`", f"{x['x']:.2f}", f"{x['v8']:.0f}", f"{x['v7_scratch']:.0f}", f"{x['replica']:.0f}"] for x in PPF["xlookup"]]
XLT_H = ["Cell", "Old formula (v7)", "New formula (v8)", "x = MAX(C8, trays/week)", "Tier v8 (LibreOffice)", "Tier v7 scratch (SMALL/COUNTIF)", "Tier Python replica"]
PROOF = [[k, f2(PPF["S"][k]), f2(PPF["replica_fy27"][k]), f"{PPF['totals_diff_replica_vs_v8'][k]:.1e}"] for k in ("lift", "tray", "sup", "total")]
PROOF_H = ["Prod Payroll 2027 (S41 / S62 / S79 / S81)", "v8 workbook (LibreOffice)", "Python replica (from input cells)", "Difference"]
GLDELTA = [[gl, f0(E["gl"][gl]["v7"]), f0(E["gl"][gl]["v8"]), eff(E["gl"][gl]["delta"])] for gl in ("5010", "5011", "5012", "5020")] + \
          [[f"{gl} (PO row {r})", f0(E["po_rows_5100"][gl]["v7"]), f0(E["po_rows_5100"][gl]["v8"]), eff(E["po_rows_5100"][gl]["v8"] - E["po_rows_5100"][gl]["v7"])]
           for gl, r in (("5110", 33), ("5130", 34), ("5140", 35))] + \
          [["2027 COO contribution (COO P&L AG132)", f0(C7), f0(C), eff(C - C7)]]

# ------------------------------------------------------------------ issues
iss7 = [s for s in cn7["sections"] if s["heading"].startswith("Issues (v7)")][0]
rows = collections.OrderedDict((r[0], list(r)) for r in iss7["table"]["rows"])
sec7 = collections.OrderedDict()
for p in re.split(r"(?m)^## ", md7)[1:]:
    t, _, b = p.partition("\n")
    sec7[t.strip()] = b
EXP = ["Decisions pending", "Headline: 2027 COO contribution", "Changes from v6", "Production labour: expensed or capitalised (B1, Decision #1)",
       "Prod Payroll overlap: 9 by count vs 7 by role (B2)", "Other v7 checks (critic v6 O1-O8, verifier V1)", "Payroll reconciliation",
       "HC tabs added to the workbook (v6; unchanged in v7)", "Head of Service Delivery salary (I-26, resolved in v5)", "Build and sources", "Completion criteria (v7)",
       "Depreciation schedule summary", "Unit-cost reconciliation", "Revenue", "Assumptions register", "DeploySum refresh and tie-out (v3 build; unchanged in v4-v7)",
       "v6 -> v7 diff", "Error scan", "Package", "Sheets in the output", "Severity scale", "Issues (v7)",
       "Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; unchanged in v6 and v7)", "Decisions", "Not done / limits"]
assert list(sec7) == EXP, list(sec7)
md_rows7 = collections.OrderedDict()
for l in sec7["Issues (v7)"].split("\n"):
    if l.startswith("| I-"):
        md_rows7[l.split("|")[1].strip()] = l
assert list(md_rows7) == list(rows)
CHANGED = ("I-05", "I-07", "I-11", "I-14", "I-17", "I-23", "I-25", "I-37", "I-38")
r = rows["I-05"]
r[1] = "RESOLVED"
r[2] += f"; {DSQ}!A128:S216; PO!U20:AF21"
r[3] = (f"RESOLVED by policy in v8 (Decision #1, user-confirmed 2026-10-10: production labour is capitalised). The whole Prod Payroll model is in the budget as "
        f"capitalised labour: {f0(S81)} for 2027 (lift {f0(S41)}, tray {f0(S62)}, supervisors {f0(S79)}; the 9 current staff {f0(CUR9)} at model rates, the ramp "
        f"{f0(I05)}). PO 5110-5140 2027 = 0 (formulas, labelled capitalised; v7 {f0(PO7)}), and the labour reaches 2027 only as depreciation of the units it "
        f"builds: {f0(DEP)} (5011 {f0(DEP_L)}, 5012 {f0(DEP_T)}). Remaining exposure = depreciation only, plus the policy scope (I-40) and the material-handling "
        f"roles (I-41). Was (v7, HIGH): the {f0(I05)} net ramp was not in the budget and its treatment was open.")
r[4] = (f"Prod Payroll computes in the workbook (16 XLOOKUP cells replaced, A-28): S81 {f2(S81)}; Python replica from the input cells, max monthly difference "
        f"{PPF['max_diff_replica_vs_v8_monthly']:.1e}. 2027 labour {f0(S81)} = into 2027 go-lives {f0(LB['to_2027'])} + into 2028 go-lives (CIP / inventory) "
        f"{f0(LB['to_2028'])}; Oct-Dec 26 labour into the Jan-Feb 27 go-lives {f0(LB['from26_to_2027'])}; depreciable labour in the 2027 vintages "
        f"{f0(LB['vint_total'])}, {f0(LB['nbv_end27'])} net at Dec-27. Average labour per unit built in 2027: lift {avg_l:,.0f} ({pct(avg_l / LIFT_COST)} of "
        f"{LIFT_COST:,.0f}), tray {avg_t:,.0f} ({pct(avg_t / TRAY_COST)} of {TRAY_COST:,.0f}).")
r[5] = f"({DEP:,.0f}) depreciation (in the headline) and +{PO7:,.0f} PO 5110-5140 removed: {eff(C - C7)} vs v7"
r[6] = "resolved (was HIGH); scope exposure in I-40"
r[7] = "None for I-05. Finance: confirm the scope (I-40, Decision #10). PO owner: the material-handling roles (I-41). SD owner: the model date (I-38)."
r = rows["I-07"]
r[4] += (f" v8: + capitalised production labour {f0(DEP)} (5011 {f0(DEP_L)}, 5012 {f0(DEP_T)}; 'Depreciation Schedule' sections 8-9): 2027 depreciation "
         f"{f0(E['dep_total_v8'])}.")
r = rows["I-14"]
r[3] += (" v8: Prod Payroll now computes and drives the budget (capitalised labour, I-05), so these placeholders (M7 new-hire cost, B9 / C9 current staff, the "
         "absence factors) now move 5011 / 5012 depreciation.")
r = rows["I-17"]
r[3] += (f" v8 (production labour capitalised): I-17 stays an expensed cost (warehouse, not production). Deduplicated against the capitalised Prod Payroll: "
         f"{f0(I17_9)} at the 9-overlap (MH-01 then a new seat); {f0(I17_7)} at the 7-overlap, incl. the 2 material-handling roles that PO 5110-5140 = 0 removes "
         f"(I-41).")
r = rows["I-23"]
r[7] += " v8: Decision #1 is resolved (capitalised); the 2026 credits now bear on the 2026 policy and the scope (I-40)."
r = rows["I-25"]
r[3] += " v8: Prod Payroll's XLOOKUP cells are replaced by an INDEX/MATCH equivalent (A-28), so LibreOffice evaluates the whole model."
r[4] += f" v8: Prod Payroll errors {PPF['errors_v7']} -> {PPF['errors_v8']}."
r = rows["I-37"]
r[3] += " v8: PO production payroll is capitalised (PO 5110-5140 = 0), so PO's part is no longer an expensed P&L risk; the model's own 7.5% applies."
r[5] = f"up to ({I37:,.0f}) CO/PE (v7 ({o6['po_co_pe_gap']:,.0f}) incl. PO {X['i37_po_part_v7']:,.0f}); up to ({o6['fo_gap_at_fica'] + o6['fe_gap_at_fica']:,.0f}) FO/FE"
r[6] = f"impact {I37:,.0f} ($50k-250k)"
r = rows["I-38"]
r[3] += (f" v8: the model now drives the budget (capitalised labour and its depreciation), so its date matters more: its Sep-Dec 26 hires set the Oct-Dec 26 "
         f"labour in the Jan-Feb 27 vintages ({f0(LB['from26_to_2027'])}).")
coo5100 = ev["coo_5100_2026"]
rows["I-40"] = ["I-40", "HIGH", f"{DSQ}!B{RM['sw_current']}:B{RM['sw_q4']}, rows 141-149; PO!U33:AF35; COO P&L!N36",
                f"Scope of the capitalisation policy (Decision #10). The user confirmed that production labour is capitalised; brief v5 reads the policy as covering "
                f"the whole Prod Payroll model, including the 9 current PO staff (PO 5110-5140), and v8 also capitalises the Oct-Dec 26 model labour into the Jan-Feb "
                f"27 go-lives it builds. The 2026 books point to a partial policy: COO 5100 production labour of {f0(coo5100)} was expensed in 2026 (PO "
                f"{f0(ev['dept_5100_2026']['PO'])}, PE {f0(ev['dept_5100_2026']['PE'])}), next to credits that fit a capitalised-labour credit (PO 6000 "
                f"{f0(ev['po_6000_2026'])}, PE 5140 {f0(ev['pe_5140_2026'])}; I-23). Idle-capacity labour (months with no builds roll into the next build, A-38) may "
                f"also have to be expensed under the inventory rules.",
                f"Current 9 expensed ({DSQ}!B{RM['sw_current']} = 0; ramp only capitalised): contribution {f0(C_SENS)} ({eff(SENS)}); 2027 labour depreciation "
                f"{f0(SC['cur']['dep_lab'])}. Oct-Dec 26 labour not capitalised (B{RM['sw_q4']} = 0): {eff(Q4)}. Both: {eff(BOTH)}. Labour in zero-build months "
                f"rolled forward: Oct-26 {f0(LB['cap_total'][1])}, Jan-27 {f0(LB['cap_total'][4])}.",
                f"({abs(SENS):,.0f}) if the current 9 stay expensed; {eff(Q4)} if the Oct-Dec 26 labour is not capitalised",
                f"impact {abs(SENS):,.0f} (> $250k)",
                f"Finance: confirm that the policy covers the current production staff, the Oct-Dec 26 labour and idle months; set {DSQ}!B{RM['sw_current']} / "
                f"B{RM['sw_q4']} to match (the workbook recalculates PO and the depreciation)."]
t_po, b_po = num(w8["HC-PO"]["D6"].value), num(w8["HC-PO"]["D7"].value)
rows["I-41"] = ["I-41", "MED", "PO!U33:AF35; 'HC-PO'!B16:Z16, B20:Z20; Logistics&WH MH-01, MH-02",
                "PO 5110-5140 = 0 removes all 9 PO HC people from the expense, including the 2 material-handling roles (r16 Material Handling Team Lead, r20 "
                "Material Handler). Prod Payroll's 9 current staff match PO HC 9 by count only; on the 7-of-9 role reading (v7 B2) the 2 are warehouse staff tied "
                "to Logistics&WH (r20 = MH-01 by name; MH-02 backfills r16), so their cost is not production labour and would stay an expense.",
                f"The 2 people together at PO HC rates: {f0(MH)} (2027 salary x (1 + {pct(t_po, 2)} + {pct(b_po, 2)})). The 2 Prod Payroll seats they would leave "
                f"stay in the model and are capitalised.",
                f"({MH:,.0f}) on the 7-overlap reading; 0 on the 9 reading", f"impact {MH:,.0f} ($50k-250k)",
                "PO owner: are r16 / r20 production or warehouse staff? If warehouse, budget them outside the capitalised labour (keep their PO HC cost in "
                "5110-5140 or move it to 5350 Warehouse)."]
ISS_NEW = ("I-40", "I-41")
sev = collections.Counter(r[1] for r in rows.values())

# ------------------------------------------------------------------ variance scan / cross-department / raise steps (regenerated; must reproduce v7 first)
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)


def var_scan(wb):
    out = []
    for s_ in ("FO", "PO", "CO", "FE", "PE", "COO P&L"):
        ws = wb[s_]
        for r_ in range(1, ws.max_row + 1):
            n_, ag = ws[f"N{r_}"].value, ws[f"AG{r_}"].value
            if not (isnum(n_) or isnum(ag)): continue
            n_ = n_ if isnum(n_) else 0; ag = ag if isnum(ag) else 0
            d = ag - n_
            if abs(d) > 50000 and (n_ == 0 or abs(d / n_) > 0.5):
                out.append(f"| {s_} | {r_} | {ws[f'A{r_}'].value} | {f0(n_)} | {f0(ag)} | {f0(d)} | {pct_nm(ag, n_)} |")
    return out


ib = sec7["Issues (v7)"]
var7 = ib[ib.index("### Variance scan"):]
v7_rows = [ln for ln in var7.splitlines() if re.match(r"\| (COO P&L|FO|PO|CO|FE|PE) \| \d+ \|", ln)]
assert var_scan(w7) == v7_rows, "variance generator does not reproduce the v7 table"
var8 = var_scan(w8)
k7 = [x.split(" | ")[:2] for x in v7_rows]; k8 = [x.split(" | ")[:2] for x in var8]
var_added = [x for x in var8 if x.split(" | ")[:2] not in k7]
var_removed = [x for x in v7_rows if x.split(" | ")[:2] not in k8]
var_changed = [x for x in var8 if x not in v7_rows and x not in var_added]
rows["I-11"][4] += (f" v8: {len(var8)} rows (regenerated: {len(var_added)} added, {len(var_changed)} changed, {len(var_removed)} removed; production labour "
                    f"capitalised).")
DEPTS = ("FO", "PO", "CO", "FE", "PE")


def xdept_cells(wb, r_):
    vals = [wb[s_][f"AG{r_}"].value for s_ in DEPTS] + [wb["COO P&L"][f"AG{r_}"].value]
    return ["" if (v is None or (isnum(v) and abs(v) < 0.5)) else f0(v) for v in vals]


def regen_xdept(text):
    out = []; changed = 0
    for ln in text.split("\n"):
        m = re.match(r"\| (\d+) \| ", ln)
        if m and ln.count(" | ") >= 10:
            r_ = int(m.group(1)); cells = ln.split(" | ")
            assert cells[2:8] == xdept_cells(w7, r_), (r_, cells[2:8], xdept_cells(w7, r_))
            new = cells[:2] + xdept_cells(w8, r_) + cells[8:]
            changed += new != cells; ln = " | ".join(new)
        out.append(ln)
    return "\n".join(out), changed


def steps(wb, s_, r_):
    xs = [wb[s_].cell(r_, c).value for c in range(21, 33)]
    out = []
    for k in range(1, 12):
        a_, b_ = xs[k - 1], xs[k]
        if isnum(a_) and isnum(b_) and a_ != 0 and abs(b_ / a_ - 1) > 1e-9:
            out.append(f"{openpyxl.utils.get_column_letter(21 + k)}: {(b_ / a_ - 1) * 100:.2f}%")
    return ", ".join(out)


def regen_steps(text):
    out = []; changed = 0; nstep = 0; nrows = 0
    for ln in text.split("\n"):
        m = re.match(r"\| (PO|CO|FE|PE|FO) \| (\d+) \| (.*?) \| (True|False) \| (.*) \|$", ln)
        if m:
            s_, r_ = m.group(1), int(m.group(2))
            assert m.group(5) == steps(w7, s_, r_), (ln, steps(w7, s_, r_))
            typed = m.group(4)
            if s_ == "PO" and r_ in (33, 34, 35):
                typed = "False (v8: formula = 0, capitalised)"
            st = steps(w8, s_, r_)
            new = f"| {s_} | {r_} | {m.group(3)} | {typed} | {st if st else 'none (0 all year)' if s_ == 'PO' and r_ in (33, 34, 35) else st} |"
            changed += new != ln; ln = new; nrows += 1; nstep += "AD: 3.00%" in st
        out.append(ln)
    return "\n".join(out), changed, nstep, nrows


# ------------------------------------------------------------------ assumptions
A_NEW = [
    ["A-36", "Production labour capitalised (Decision #1 RESOLVED): every Prod Payroll cost row (rows 41, 62, 79) is capitalised into the units built that "
     "month; the current staff are included (switch B131 = 1)", f"2027 {f0(S81)}; 2027 depreciation {f0(DEP)}",
     f"{DSQ}!B{RM['sw_current']}, rows {RM['pp_lift']}-{RM['cap_total']}", "user-confirmed 2026-10-10; scope per brief v5 (orchestrator); Finance to confirm (I-40)"],
    ["A-37", "Supervisors are allocated to lifts and trays pro rata to the month's lift : tray capitalised labour (v7 A-32, now by month)",
     f"2027 supervisors {f0(S79)}: {f0(sum(LB['sup_to_lift'][4:]))} to lifts", f"{DSQ}!row {RM['sup_to_lift']}", "builder (v7 A-32 carried to monthly)"],
    ["A-38", "Labour per unit = the build month's capitalised labour / units built that month; a month with no units built (Oct-26, Jan-27) rolls its labour "
     "into the next build month (work in progress)", f"Oct-26 {f0(LB['cap_total'][1])} into Nov-26 builds; Jan-27 {f0(LB['cap_total'][4])} into Feb-27 builds",
     f"{DSQ}!rows {RM['pool_lift']}-{RM['per_tray']}", "builder assumption (v8); Finance to confirm idle-month treatment (I-40)"],
    ["A-39", "Build-to-go-live lag 2 months (DeploySum note 1); labour joins the vintage cost at go-live and is depreciated like the unit (full month from go-live "
     "+ B13, 84 / 120 months, salvage B12)", f"lag check {f0(LAGCHK)} (DeploySum go-lives = builds 2 months earlier, every 2027 month)",
     f"{DSQ}!B{RM['lag']}:B{RM['lag_check']}, rows {RM['vint_lift'][0]}-{RM['vint_tray'][-1]}", "DeploySum note 1; Depreciation Schedule logic (brief v5)"],
    ["A-40", "Sep-Dec 26 model months: Sep-26 builds go live Nov-26 (2026 vintage, inside the PO run rate; not added); Oct-26 has no builds and rolls into "
     "Nov-26; the Nov-Dec 26 builds go live Jan-Feb 27 and carry the Oct-Dec 26 labour (switch B132 = 1)",
     f"{f0(LB['from26_to_2027'])} into Jan-Feb 27; {f0(LB['from26_to_2026'])} in the Nov-26 go-lives (not added)",
     f"{DSQ}!B{RM['sw_q4']}, rows {RM['lab_2027']}-{RM['lab_2026']}, B{RM['m_cap_2026']}:B{RM['m_from26_to_2026']}", "builder assumption (brief v5: state how)"],
    ["A-41", "Builds for 2028 go-lives (Nov-Dec 27) carry labour that is not depreciated in 2027: CIP / inventory at Dec-27", f0(LB["to_2028"]),
     f"{DSQ}!row {RM['lab_2028']}, B{RM['m_to_2028']}", "follows A-14 / A-15"],
]
A_AMEND = {
    "A-15": f". v8: their capitalised labour ({f0(LB['to_2028'])}) is not depreciated either (A-41).",
    "A-28": ". v8: the 16 XLOOKUP cells are replaced in the workbook by an INDEX/MATCH equivalent (Prod Payroll!B48:Q48): tiers and model totals identical to the scratch method; the scratch copy is no longer needed.",
    "A-32": ". v8: superseded for the booked figure by A-36..A-41; reproduced as the bridge check (64,735).",
    "A-33": ". v8: superseded for the booked figure by A-36..A-41; reproduced as the bridge check (64,735).",
}

# ------------------------------------------------------------------ changes from v7
CHG = [
    ["Policy", "Decision #1 RESOLVED", f"Production labour capitalised (user-confirmed 2026-10-10); primary case: all Prod Payroll labour incl. the current 9 "
     f"(brief v5).", "Decisions pending #1; I-05"],
    ["Prod Payroll", "XLOOKUP not evaluated by LibreOffice", f"16 cells (B48:Q48) -> INDEX/MATCH equivalent; no other model cell edited. Model errors "
     f"{PPF['errors_v7']} -> {PPF['errors_v8']}; 2027 {f2(S81)} = Python replica (diff {PPF['totals_diff_replica_vs_v8']['total']:.1e}).", "Prod Payroll!B48:Q48"],
    ["Depreciation Schedule", "Capitalised-labour block", f"New sections 8-10 (rows 128-216): labour by build month, per unit, by go-live vintage, by GL, memo; "
     f"switches B{RM['sw_current']} / B{RM['sw_q4']}; rows 1-126 unchanged.", f"{DSQ}!A128:S216"],
    ["PO 5011 / 5012", "Labour depreciation booked", f"+{DEP_L:,.0f} / +{DEP_T:,.0f} (formulas: section 4 + section 9).", "PO!U20:AF21"],
    ["PO 5110-5140", "Capitalised", f"{f0(PO7)} -> 0: formulas =(1 - B{RM['sw_current']}) x the v7 amount, labelled CAPITALISED in column AI.", "PO!U33:AF35, AI33:AI35"],
    ["Headline", "Contribution", f"{f0(C7)} -> {f0(C)} ({eff(C - C7)} = 5100 removed {f0(PO7)} less labour depreciation {f0(DEP)}).", "COO P&L!AG132"],
    ["Caveats", "Recomputed", "Expensed / capitalised-on-top / inside-unit-cost rows removed (resolved); scope alternatives (I-40), material-handling roles "
     "(I-41), run-rate labour, I-05 burden added; A-14 and I-37 recomputed; carried rows act on the new headline. Sign-flip and range recomputed.",
     "Headline caveats"],
    ["Issues", "Updated", "I-05 RESOLVED; I-40 (HIGH) and I-41 (MED) new; I-07, I-11, I-14, I-17, I-23, I-25, I-37, I-38 updated.", "Issues (v8)"],
    ["Decisions pending", "Updated", "#1 RESOLVED; #6 reworded (warehouse payroll); #10 new (scope of the policy).", "Decisions pending"],
    ["Privacy", "Wording", "v7's wording that every per-person amount in the md is rounded is withdrawn: salaries that are $5k multiples are unchanged by the $5k "
     "rounding, so some unique-role salaries appear exactly (counted in the completion criteria).", "banner; completion criteria"],
]

# ------------------------------------------------------------------ Collation Notes JSON (from v7)
cn = copy.deepcopy(cn7)
cn["title"] = rep(cn["title"], "build v7", "build v8")
sec = lambda h: [s for s in cn["sections"] if s["heading"].startswith(h)][0]
b = sec("CONFIDENTIAL")
b["lines"] = ["This workbook holds employee names and salaries on the HC-* tabs (copied from the COO HC & PL workfile). Share it only with people cleared to see "
              "compensation. This sheet keeps exact figures. The notes file (02-build_notes_v8.md) rounds per-person amounts to the nearest $5k, but a salary "
              "that is itself a multiple of $5k is unchanged by that rounding, so some unique-role salaries appear there at their exact value."]
sec("Decisions pending")["table"]["rows"] = DEC
hl = sec("Headline")
HL = [("Revenue (company recognized revenue, 9/30/26 sales plan)", "16", [16]), ("COGS (COO departments)", "63", [63]),
      ("  of which depreciation (in COGS)", "19-22", [19, 20, 21, 22]), ("Gross Profit", "64", [64]), ("Opex (COO departments)", "116", [116]),
      ("COO contribution before other income (workbook label 'Net Ordinary Income')", "117", [117]), ("Net Other Income", "131", [131]),
      ("COO contribution (workbook label 'Net Income')", "132", [132])]
assert [r_[0] for r_ in hl["table"]["rows"]] == [h[0] for h in HL]
for r_, (lab, rr, rws) in zip(hl["table"]["rows"], HL):
    n_, ag = val(w8, "N", rws), val(w8, "AG", rws)
    r_[2]["v"], r_[3]["v"], r_[4]["v"] = n_, ag, ag - n_
    r_[5]["v"] = "n/m" if (n_ <= 0 or ag < 0) else f"{round((ag - n_) / n_ * 100):.0f}%"
    r_[6] = round(val(w7, "AG", rws), 2)
hl["table"]["header"][-1] = "2027 in v7 (value)"
cv = sec("Caveats on the headline")
L1 = (f"(0) Headline caveat resolved (Decision #1, user-confirmed 2026-10-10): production labour is capitalised. The whole Prod Payroll model ({f0(S81)} for "
      f"2027: ramp and the current 9) is budgeted as capitalised labour and reaches 2027 only as depreciation ({f0(DEP)}); the FO ramp ({f0(b3['fo_ramp'])}) stays "
      f"an operating cost (field labour). Both follow the same 9/30/26 deployment plan. The contribution moves from {f0(C7)} to {f0(C)}: PO 5110-5140 "
      f"({f0(PO7)}) leaves the P&L and {f0(DEP)} of labour depreciation enters 5011/5012. Scope sensitivity (current 9 expensed, ramp only capitalised): "
      f"{f0(C_SENS)}.")
cost7 = val(w7, "AG", [63]) + val(w7, "AG", [116]); cost8 = val(w8, "AG", [63]) + val(w8, "AG", [116])
l1 = rep(rep(cv["lines"][1], f"The bottom line, {f0(C7)}, is", f"The bottom line, {f0(C)}, is"), f"PE: {f0(cost7)})", f"PE: {f0(cost8)})")
cv["lines"] = [L1, l1, cv["lines"][2],
               "(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. Production labour is capitalised (Decision "
               "#1); the scope alternatives (Decision #10) are shown as rows, as are the I-17 readings with the capitalised Prod Payroll (9 by count, 7 by role)."]
cv["table"]["rows"] = [[r_[0], r_[1], r_[2], round(r_[3], 2) if isinstance(r_[3], float) else r_[3], round(r_[4], 2) if isinstance(r_[4], float) else r_[4], r_[5]]
                       for r_ in cav]
cv["after"] = sf
sup = sec("Workbook text superseded")
sup["lines"].append(f"v8: the Depreciation Schedule's section 4 (rows 79-82) still shows depreciation of the units only; PO rows 20/21 add the capitalised-labour "
                    f"depreciation of section 9 (rows {RM['out_lift']}-{RM['out_tray']}); row {RM['dep_total']} gives the total. The headline text at "
                    f"'Depreciation Schedule'!A2 ('Section 4 feeds PO rows 19-22') predates v8.")
src = sec("Source and build")
src["lines"] = [f"Base: v7 collated workbook. v8 books production labour as capitalised (brief v5): Prod Payroll!B48:Q48 (XLOOKUP -> INDEX/MATCH), new "
                f"Depreciation Schedule rows 128-216, PO rows 20-21 and 33-35 (2027 months and the AI notes), and their subtotals and the COO P&L roll-up. Every "
                f"other cell has 0 formula and 0 value differences vs v7.",
                "Full notes: 02-build/02-build_notes_v8.md. Figures: figures_v8.py (Prod Payroll and labour-block replicas, scenarios, bridge, hand recompute) and "
                "scen_v8.py (switch scenarios recalculated in LibreOffice); numbers on this sheet are live formulas (headline) or values computed by those scripts."]
chg = sec("Changes from v6")
chg["heading"] = "Changes from v7"
chg["table"] = {"header": ["Item", "Point", "What v8 did", "Where"], "rows": CHG, "after": []}
i8 = cn["sections"].index(sec("Decision #1 evidence"))
j8 = cn["sections"].index(sec("2027 COO contribution under each treatment"))
assert j8 == i8 + 1
cn["sections"][i8:j8 + 1] = [
    {"heading": "Production labour capitalised (Decision #1 RESOLVED): where the labour sits", "table": {"header": ["Item", "Value", "Depreciation Schedule cell"], "rows": WHERE, "after": []}},
    {"heading": "Labour per unit built, by build month (Depreciation Schedule section 8)", "table": {"header": LPU_H, "rows": LPU, "after": []}},
    {"heading": "Budget effect by GL, v7 -> v8 (2027, AG)", "table": {"header": ["Line", "v7", "v8", "Change"], "rows": GLDELTA, "after": []}},
    {"heading": "Scope sensitivity and alternatives (recalculated with the switches)", "table": {"header": SENS_H, "rows": SENS_T, "after": []}},
    {"heading": "Bridge: v7 'capitalised on top' (64,735) to the booked v8 labour depreciation", "table": {"header": ["Step", "2027 depreciation", "Note"], "rows": BRIDGE, "after": []}},
    {"heading": "Prod Payroll XLOOKUP replacement (row 48): cell by cell", "table": {"header": XLT_H, "rows": [[x[0], x[1].strip('`'), x[2].strip('`')] + x[3:] for x in XLT],
                                                                                      "after": ["Model totals 2027 (v8 / Python replica): " + "; ".join(f"{k} {f2(PPF['S'][k])} / {f2(PPF['replica_fy27'][k])}" for k in ("lift", "tray", "sup", "total"))]}},
]
oth = sec("Other v7 checks")
oth["heading"] = "Other v7 checks (critic v6 O1-O8, verifier V1; v7 figures, I-05 parts superseded by the capitalisation)"
rec = sec("Payroll reconciliation (v6)")
po_line = [i for i, l in enumerate(rec["lines"]) if l.startswith("PO: PO HC")][0]
rec["lines"][po_line] += (f" v8: production labour is capitalised: PO 5110-5140 2027 = 0 and the whole Prod Payroll model is in the budget as capitalised labour "
                          f"(I-05 RESOLVED), so the Prod Payroll 'net increment' no longer applies; Logistics&WH stays outside (I-17, I-41).")
asr = sec("Assumptions register")
for r_ in asr["table"]["rows"]:
    if r_[0] in A_AMEND:
        r_[1] += A_AMEND[r_[0]]
    if r_[0] == "A-28":
        r_[3] = rep(r_[3], "(workbook unchanged)", "(v8: replaced in the workbook)")
asr["table"]["rows"] += A_NEW
iss = sec("Issues (v7)")
iss["heading"] = iss["heading"].replace("Issues (v7)", "Issues (v8)")
iss["table"]["rows"] = list(rows.values())
cnj = json.dumps(cn, indent=1, ensure_ascii=False)
assert "no exact per-person" not in cnj.lower()
open(OUT_JSON, "w").write(cnj)

# ------------------------------------------------------------------ md
L = []
A = L.append
A("# 02-build notes v8 - 2027 COO budget collation\n")
A(f"> **{BANNER}.** The workbook's HC-* tabs hold employee names and salaries; share the workbook and these notes only with people cleared to see "
  "compensation. In this file per-person amounts for identified employees are rounded to the nearest $5k (shown with '~') or aggregated. Rounding does not "
  "change an amount that is already a multiple of $5k, so some unique-role salaries (one person per role) still appear at their exact value; the Collation "
  "Notes sheet keeps exact figures. A department total compared across versions can also reveal one person's cost.\n")
A("## Decisions pending\n")
A(f"Decision #1 is RESOLVED (user-confirmed 2026-10-10: production labour is capitalised) and booked in v8. {len(DEC) - 1} decisions remain open: #2-#9 as in "
  f"v7 (#6 reworded now that the production ramp is capitalised) and #10, new, on the scope of the policy (I-40). The budget carries the 'current treatment' "
  f"column. Effects are on the 2027 COO contribution, each on its own.\n")
A(mdtable(dp7["table"]["header"], DEC))
A(f"Why #10 (I-40): brief v5 reads the policy as covering the whole Prod Payroll model, the 9 current staff included, but the 2026 books expensed production "
  f"labour (COO 5100 {f0(ev['coo_5100_2026'])} in 2026: PO {f0(ev['dept_5100_2026']['PO'])}, PE {f0(ev['dept_5100_2026']['PE'])}) next to credits that fit a "
  f"capitalised-labour credit (PO 6000 {f0(ev['po_6000_2026'])}, PE 5140 {f0(ev['pe_5140_2026'])}; I-23). So the 2026 policy may have been partial. DeploySum "
  f"labels the unit costs 'Unit cost (CapEx)' ({ev['deploysum_unit_cost_cell']}); v8 adds the labour on top of those costs.\n")
A("## Headline: 2027 COO contribution\n")
A(mdtable(["Line", "COO P&L row", "2026 (N)", "2027 v8 (AG)", "Change", "%", "2027 v7 (AG)", "v8 - v7"],
          [[("**" + lab + "**") if rr == "132" else lab, rr, f0(val(w8, "N", rws)), f0(val(w8, "AG", rws)), f0(val(w8, "AG", rws) - val(w8, "N", rws)),
            pct_nm(val(w8, "AG", rws), val(w8, "N", rws)), f0(val(w7, "AG", rws)), f0(val(w8, "AG", rws) - val(w7, "AG", rws))]
           for lab, rr, rws in HL], ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:"]))
A(f"- **2027 COO contribution (COO P&L AG132): {f0(C)}** (v7 {f0(C7)}, {eff(C - C7)}). The change is exactly PO 5110-5140 removed ({f0(PO7)}, now "
  f"capitalised) less the depreciation of the capitalised labour ({f0(DEP)}: 5011 {f0(DEP_L)}, 5012 {f0(DEP_T)}). Revenue {f0(E['rev'])} (all to 4100); "
  f"COGS + Opex {f0(cost8)}.")
A(f"- Issues: {sev['HIGH']} HIGH, {sev['MED']} MED, {sev['LOW']} LOW open; {sev['RESOLVED']} RESOLVED. v8 resolves I-05, adds I-40 (HIGH) and I-41 (MED), and "
  f"updates I-07, I-11, I-14, I-17, I-23, I-25, I-37 and I-38.\n")
A("**Headline caveat: " + L1[4:].replace("Headline caveat resolved", "resolved", 1) + "**\n")
hb = sec7["Headline: 2027 COO contribution"]
blk = hb[hb.index("### Caveats on the headline"):hb.index("(3) Open exposures")].rstrip()
blk = rep(blk, f"The bottom line, {f0(C7)}, is", f"The bottom line, {f0(C)}, is")
blk = rep(blk, f"PE: {f0(cost7)})", f"PE: {f0(cost8)})")
A(blk + "\n")
A("(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. Production labour is capitalised (Decision #1); the "
  "**scope alternatives** (Decision #10) are rows here, as are the I-17 readings with the capitalised Prod Payroll (9 by count, 7 by role). The v7 rows for "
  "'I-05 expensed', 'capitalised on top' and 'inside the unit cost' are removed: the policy is decided.\n")
A(mdtable(["Item", "Direction", "What could happen", "Effect on 2027 COO contribution", "Contribution after this item alone", "Source cells"],
          [cav_md_row(r_) for r_ in cav], ["---", "---", "---", "---:", "---:", "---"]))
A("**" + sf[0].split(":")[0] + ":**" + sf[0].split(":", 1)[1] + " " + sf[1] + "\n")
A("**" + sf[2].split(":")[0] + ":**" + sf[2].split(":", 1)[1] + "\n")
A(mdtable(["Bound", "What it adds to the headline", "2027 COO contribution"],
          [["Lower bound 1 (booked policy, all quantified downsides)", "I-17 + I-41 (7-overlap); I-10; I-31 shortfall; I-05 burden capitalised; run-rate labour", f0(LB1)],
           ["Lower bound 2 (scope sensitivity: current 9 expensed)", "sensitivity; I-17 deduplicated (9-overlap); I-10; I-31 shortfall; I-05 burden; run-rate labour", f0(LB2)],
           ["Point estimate", "-", f0(C)],
           ["Upper end", "I-32 in full only", f0(UB)]], ["---", "---", "---:"]))
A("**" + sf[3].split(":")[0] + ":**" + sf[3].split(":", 1)[1] + "\n")
A("## Changes from v7\n")
A(mdtable(["Item", "Point", "What v8 did", "Where"], CHG))
A("The verifier's v7 note (privacy wording) is addressed in the banner. v7's own changes from v6 are listed in `02-build_notes_v7.md` and still apply.\n")
# ------------------------------------------------------------------ the capitalisation section
A("## Production labour: capitalised (Decision #1 RESOLVED)\n")
A(f"User, 2026-10-10: 'production labor is capitalized. Use the same formula as the file has.' Brief v5 reads 'the file's formula' as the SD Prod Payroll "
  f"model for the labour and the existing Depreciation Schedule logic for the capitalisation. v8 books the primary case: **all production payroll in the "
  f"model is capitalised, including the 9 current PO staff**, and PO 5110-5140 2027 goes to 0 (formulas, labelled CAPITALISED in PO column AI). The sensitivity "
  f"(only the ramp capitalised, the current 9 expensed) is shown, not booked.\n")
A("### 1. Prod Payroll computes in the workbook (XLOOKUP replaced)\n")
A("LibreOffice does not evaluate XLOOKUP, so v7's Prod Payroll showed #NAME? in 430 cells (tray and supervisor rows) and v6/v7 evaluated it in a scratch copy "
  "(A-28). v8 replaces only the 16 XLOOKUP cells of row 48 ('staffing tier used, trays/week') with an equivalent that LibreOffice and Excel both evaluate: the "
  "smallest tier >= x (exact match, else the next tier up), or MAX(tiers) if x is above every tier. On the ascending, unique tier row B20:O20 (checked), "
  "MATCH(x, r, 1) is the position of the largest tier <= x, and ISNA(MATCH(x, r, 0)) adds 1 when x is not itself a tier; below the first tier IFERROR gives 0 + 1. "
  "No other Prod Payroll cell is edited.\n")
A(mdtable(XLT_H, XLT))
A(f"**Proof (model totals within $1 of the Python replica):** the replica rebuilds the whole model from its input cells (grids, rates, raise, absence, "
  f"DeploySum builds) with no cached model value.\n")
A(mdtable(PROOF_H, PROOF, ["---", "---:", "---:", "---:"]))
A(f"Every month of rows 41, 62, 79 and 81 (Sep-26..Dec-27): max difference replica vs v8 {PPF['max_diff_replica_vs_v8_monthly']:.1e}; v7 scratch "
  f"(SMALL/COUNTIF) vs v8 {PPF['max_diff_v7_scratch_vs_v8_monthly']:.1e}. Prod Payroll errors: v7 {PPF['errors_v7']}, v8 {PPF['errors_v8']}. The handoff's "
  f"verified figures hold: 2027 {f2(S81)} (lift {f2(S41)}, tray {f2(S62)}, supervisors {f2(S79)}); the 9 current staff at model rates "
  f"{f2(CUR9)}; builds 2027 {UNITS27['lift']:.0f} lifts / {UNITS27['tray']:,.0f} trays, of which live in 2027 {LIVE27['lift']:.0f} / {LIVE27['tray']:.0f}.\n")
A("### 2. Method (Depreciation Schedule sections 8-10, rows 128-216)\n")
A(f"1. Labour by build month: Prod Payroll rows 41 (lift), 62 (tray), 79 (supervisors), Sep-26..Dec-27, same columns B:Q (rows {RM['pp_lift']}-{RM['pp_total']}).\n"
  f"2. Capitalised share: all of it (B{RM['sw_current']} = 1). With B{RM['sw_current']} = 0 the model's own cost of the current staff (rows "
  f"{RM['cur_lift']}-{RM['cur_tray']}, same cost formula at 7 lift + 2 tray, no hires) is left out and PO 5110-5140 returns to its v7 amount.\n"
  f"3. Supervisors to lifts / trays pro rata to the month's lift : tray labour (A-37, v7 A-32 by month).\n"
  f"4. Labour per unit built = the month's labour / units built that month (DeploySum rows 24/25). Oct-26 and Jan-27 build nothing; their labour waits and "
  f"joins the next build month (A-38).\n"
  f"5. Each unit's labour joins its go-live vintage {LAG:.0f} months later (B{RM['lag']}; check B{RM['lag_check']} = 0: DeploySum go-lives equal the "
  f"builds 2 months earlier in every 2027 month) and is depreciated exactly like the unit: full month from go-live (+B13), 84 months lifts (5011), 120 months "
  f"trays (5012), salvage B12 (A-39). Peripherals (5020) carry no labour.\n"
  f"6. Sep-Dec 26 model months (A-40): Sep-26 builds go live Nov-26 (a 2026 vintage inside the PO run rate, so its labour, {f0(LB['from26_to_2026'])}, is not "
  f"added; see the run-rate row in the caveats); Oct-26 rolls into Nov-26; the Nov-26 and Dec-26 builds are the Jan-27 and Feb-27 go-lives and carry the "
  f"Oct-Dec 26 labour ({f0(LB['from26_to_2027'])}; switch B{RM['sw_q4']}).\n"
  f"7. Builds for 2028 go-lives (Nov-Dec 27) carry {f0(LB['to_2028'])} of labour with no 2027 depreciation (CIP / inventory, A-41).\n"
  f"8. Output: section 9 rows {RM['out_lift']}/{RM['out_tray']} by GL, added to PO rows 20/21 (U:AF). Section 4 (rows 79-82) is unchanged and still "
  f"shows the units only; row {RM['dep_total']} = total.\n")
A("### 3. Labour per unit, by build month\n")
A(mdtable(LPU_H, LPU, ["---"] + ["---:"] * 9 + ["---"]))
A("### 4. Capitalised labour: 2027 total, depreciated in 2027 vs carried into 2028\n")
A(mdtable(["Item", "Value", "Depreciation Schedule cell"], WHERE, ["---", "---:", "---"]))
A(f"So of the **{f0(S81)} of 2027 production payroll capitalised**, {f0(LB['to_2027'])} sits in units that go live in 2027 and are depreciated from "
  f"go-live, and **{f0(LB['to_2028'])} is carried into 2028 go-lives** (CIP / inventory at Dec-27). The 2027 vintages also carry {f0(LB['from26_to_2027'])} of "
  f"Oct-Dec 26 labour. 2027 depreciation of the labour: **{f0(DEP)}** (5011 {f0(DEP_L)}, 5012 {f0(DEP_T)}).\n")
A(mdtable(["Line", "v7", "v8", "Change"], GLDELTA, ["---", "---:", "---:", "---:"]))
A("### 5. Hand recompute of one month: Jun-27\n")
A(f"Vintages in service in Jun-27 under the full-month rule: Jan-Jun 27 go-lives (Mar-27 has none). Labour per unit from the build month (table above).\n")
A(mdtable(HAND_H, HAND, ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:"]))
A(f"Hand vs workbook: max difference {H['diff']:.1e} (also = 'Depreciation Schedule'!K{RM['out_lift']} {f2(H['ds_k193'])} and K{RM['out_tray']} {f2(H['ds_k194'])}). "
  f"The whole block is also rebuilt in Python from the replica payroll: max difference {F['labour_replica_max_diff']:.1e} over every row of sections 8-10.\n")
A("### 6. Sensitivity (current 9 expensed) and the other scope alternatives\n")
A(mdtable(SENS_H, SENS_T, ["---", "---:", "---:", "---:", "---:", "---:"]))
A(f"Each case is a LibreOffice recalculation of a scratch copy of v8 with the switch changed (scen_v8.py), checked against the Python replica (difference "
  f"< 1e-6). The sensitivity books PO 5110-5140 at the v7 amount ({f0(PO7)}, the PO HC roster) and capitalises the ramp only: 2027 labour {f0(SC['cur']['cap_2027'])}, "
  f"depreciation {f0(SC['cur']['dep_lab'])}, contribution **{f0(C_SENS)}** ({eff(SENS)} vs booked).\n")
A("### 7. Bridge from v7's verified 64,735\n")
A(mdtable(["Step", "2027 depreciation", "Note"], BRIDGE, ["---", "---:", "---"]))
A(f"v7's method (ramp only, annual average labour per unit built in 2027, 2027 labour only) is reproduced exactly ({f2(BR['v7_ramp_annual_avg'])}). v8 keeps "
  f"its parts (model split, supervisors pro rata, 2-month lag, Depreciation Schedule rules) and applies them by build month, as brief v5 asks: early builds carry "
  f"more labour per unit (Nov-26 to Feb-27: up to {max(LB['per_lift']):,.0f} per lift) and are in service longer in 2027, so the monthly method depreciates "
  f"more in 2027 than the annual average.\n")
A("### 8. Interactions not booked\n")
A(f"- **Material-handling roles (I-41).** PO 5110-5140 = 0 removes the 2 material-handling roles too. On the 7-of-9 role reading they are warehouse staff and "
  f"their cost ({f0(MH)} together at PO HC rates) should stay an expense.\n"
  f"- **Logistics&WH (I-17).** Unchanged as an expense ({f0(I17)}); deduplicated with the capitalised Prod Payroll {f0(I17_9)} (9-overlap) or {f0(I17_7)} "
  f"(7-overlap, with I-41).\n"
  f"- **Existing-fleet run rate.** The PO Dec-26 run rate carries no labour; the Sep-26 labour in the Nov-26 go-lives would add {f0(RRG)} of 2027 depreciation "
  f"(earlier 2026 go-lives not determinable).\n"
  f"- **2026 columns.** PO and COO P&L 2026 (B:N) are unchanged: 2026 still expenses its 5100 production labour (I-40). The Prod Payroll Sep-Dec 26 model "
  f"columns now compute (they were #NAME? for trays and supervisors); they are model months, not P&L 2026 columns.\n")
# carried analysis sections
b2s = sec7["Prod Payroll overlap: 9 by count vs 7 by role (B2)"].strip()
A("## Prod Payroll overlap: 9 by count vs 7 by role (B2)\n")
A(f"v8 note: with production labour capitalised, the overlap no longer changes an expensed ramp. It decides two things: whether the 2 material-handling roles "
  f"belong in the capitalised labour at all (7 reading: no, I-41, {f0(MH)}) and how I-17 is deduplicated ({f0(I17_9)} at 9, {f0(I17_7)} at 7). The v7 text "
  f"below (I-05 as an expensed net increment) is history.\n")
A(b2s + "\n")
A("## Other v7 checks (critic v6 O1-O8, verifier V1; v7 figures)\n")
A(f"v8 note: O1 (I-05 at PO HC burden rates, +{o1['diff']:,.0f}) is now capitalised: 2027 effect ({O1D:,.0f}) (caveat row). O7's range is replaced by the v8 "
  f"range. The rest is unchanged.\n")
A(sec7["Other v7 checks (critic v6 O1-O8, verifier V1)"].strip() + "\n")
pr = sec7["Payroll reconciliation"]
A("## Payroll reconciliation\n")
A(f"v8 note: PO 5110-5140 2027 is now 0 (capitalised; I-05 RESOLVED). The reconciliation below (v6/v7) compares the PO HC roster ({f0(PO7)}, the amount "
  f"removed from PO and restored by the sensitivity) with the SD models; for Prod Payroll the 'net increment not in the budget' no longer applies, because the "
  f"whole model is in the budget as capitalised labour ({f0(S81)} for 2027). Logistics&WH stays outside (I-17, I-41).\n")
A(pr.strip() + "\n")
hct = sec7["HC tabs added to the workbook (v6; unchanged in v7)"]
if AN:
    hct = hct[:hct.index("Checks (v6, unchanged in v7)")] + (
        f"Checks (v6, unchanged in v7 and v8): HC tabs copied byte for byte from v7; v8 recalculation of the HC tabs: errors {AN['hc_tabs']['errors']}, cached vs "
        f"recalculated max difference {AN['hc_tabs']['max_diff']:.1e} over {AN['hc_tabs']['cells']:,} cells.\n")
A("## HC tabs added to the workbook (v6; unchanged in v7 and v8)\n"); A(hct.strip() + "\n")
A("## Head of Service Delivery salary (I-26, resolved in v5)\n"); A(sec7["Head of Service Delivery salary (I-26, resolved in v5)"].strip() + "\n")
A("## Build and sources\n")
A(f"Output: `02-build/02-build_COO_2027_Budget_Collated_v8.xlsx` and this file (v1-v7 files unchanged; no v8 CSV).  \n"
  f"Scripts: `02-build/scripts/` - v8 entry point `run_build_v8.sh`: build_v8.py stage1 (formula edits on v7) -> recalc.sh (LibreOffice full recalculation) -> "
  f"patches_v8.py (static downstream trace with deps_v5.py; values of the edited cells and their downstream set only; stops if anything else moves > 1e-6) -> "
  f"build_v8.py final -> scen_v8.py + recalc.sh (switch scenarios) -> prodpay_v6.py, recon_v6.py, scen_v7.py, figures_v7.py on v7 (carried v7 figures) -> "
  f"figures_v8.py -> cnotes_v6.py (v7 Collation Notes) -> report_v8.py pass 1 -> build_v8.py final with Collation Notes -> diff_versions.py v7 -> v8, recalc.sh, "
  f"analyze_v8.py -> report_v8.py pass 2 (JSON must equal pass 1) -> privacy_v6.py (names) and paylist_v8.py (per-person amounts) -> scratch name lists "
  f"deleted. `run_build_v7.sh` ... `run_build.sh` still reproduce v7 ... v1.  \n"
  f"Inputs (read-only): `COO_HC_and_PL_workfile.xlsx` sha256 `{sha(WFILE)}`; `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `{sha(COO)}`; "
  f"`Service_Delivery_PL_worksheets.xlsx` sha256 `{sha(SD)}`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `{sha(NEW)}`.  \n"
  f"Recalculation engine: {lov}.  \n"
  f"Base: v7 workbook sha256 `{sha(V7X)}`.\n")
A("## Completion criteria (v8)\n")
if AN:
    c = AN
    A(mdtable(["Criterion", "Result"], [
        ["COO P&L = sum of the departments", f"Every COO P&L GL row, 2027 months U:AF and AG: max |COO - (FO + PO + CO + FE + PE)| {c['coo_sum']['max_diff']:.1e} over "
         f"{c['coo_sum']['cells']:,} cells; check row 133 (AG) {c['coo_sum']['row133']:.1e}."],
        ["0 new errors; Prod Payroll computes", f"Errors v7 -> v8: Prod Payroll {c['errors']['pp']}; new errors {c['errors']['new']}; LibreOffice recalculation of v8 vs "
         f"stored values: {c['recalc']['n_diff']} cells differ, max {c['recalc']['max_diff']:.1e}, non-numeric mismatches {c['recalc']['text_mismatch']}."],
        ["Diff confined to the allowed areas", f"diff_versions.py v7 -> v8: {c['diff']['total']['formula_diffs']} formula and {c['diff']['total']['value_diffs']} value "
         f"differences, all inside the allowed areas (classified below): outside {c['allowed']['outside']}; 2026 columns (B:N) of the P&L tabs changed "
         f"{c['allowed']['cols_2026']}; sheets with differences {', '.join(c['allowed']['sheets'])}."],
        ["Package", f"{c['package']['identical']} of {c['package']['v7_parts']} v7 parts byte-identical; changed: {', '.join(c['package']['changed'])}; added / removed "
         f"{len(c['package']['added'])} / {len(c['package']['removed'])}; external links {c['package']['external_links']}."],
        ["Hand recompute of one month", f"Jun-27 labour depreciation by hand = PO!Z20 / Z21 (v8 - v7): max difference {F['hand']['diff']:.1e}."],
        ["XLOOKUP replacement proof", f"16 cells; tiers identical to the v7 scratch and the replica; model totals vs replica max {max(abs(v) for v in PPF['totals_diff_replica_vs_v8'].values()):.1e} (< $1)."],
        ["Every figure computed by script", "figures_v8.py, figures_v7.py, recon_v6.py, scen_v7/v8.py; report_v8.py types no figure."],
        ["Collation Notes live formulas", f"{c['cn']['formulas']} formulas; recalc vs stored max diff {c['cn']['max_diff']:.1e}, text mismatches {c['cn']['text_mismatch']}; "
         f"first section is the CONFIDENTIAL banner: {c['cn']['banner_first']}."],
        ["No names", f"privacy_v6.py on the md, the Collation Notes JSON and sheet: {c['privacy']}. The return message is checked the same way."],
        ["Per-person amounts in the md", f"paylist_v8.py: {c['paylist']}. Those $5k-multiple amounts are unique-role salaries that the $5k rounding cannot hide (banner)."],
    ]))
else:
    A("[pass 1: pending]\n")
dsum = sec7["Depreciation schedule summary"].strip()
dsum = rep(dsum, "user decision (Decisions pending #2).", "user decision (Decisions pending #3).") if "user decision (Decisions pending #2)." in dsum else dsum
ds8 = w8["Depreciation Schedule"]; po8 = w8["PO"]
GLR = [("5010 SlipBot (PO row 19)", 19, 33, None), ("5011 SlipLift (PO row 20)", 20, 34, RM["out_lift"]), ("5012 SlipCarrier (SlipTray) (PO row 21)", 21, 35, RM["out_tray"]),
       ("5020 Robot Peripherals (PO row 22)", 22, 36, None)]
gt = []; tots = [0.0] * 9
for lab, porow, exrow, labrow in GLR:
    n26 = num(po8.cell(porow, 14).value); rr = num(ds8.cell(21 + (exrow - 33), 2).value)          # section 2 run rate B21:B24
    ex27 = num(ds8.cell(exrow, 18).value); tot = num(po8.cell(porow, 33).value)
    lab27 = num(ds8.cell(labrow, 18).value) if labrow else 0.0
    new27 = tot - ex27 - lab27
    jan, dec = num(po8.cell(porow, 21).value), num(po8.cell(porow, 32).value)
    vals = [n26, rr, ex27, new27, lab27, tot, jan, dec]
    gt.append([lab, f0(n26), f2(rr), f0(ex27), f0(new27), f0(lab27), f0(tot), f2(jan), f2(dec)])
    tots = [tots[i] + vals[i] for i in range(8)] + [0]
gt.append(["**Total**", f0(tots[0]), f2(tots[1]), f0(tots[2]), f0(tots[3]), f0(tots[4]), f0(tots[5]), f2(tots[6]), f2(tots[7])])
assert abs(tots[5] - E["dep_total_v8"]) < 1e-6 and abs(tots[4] - DEP) < 1e-6
old_tab = dsum[dsum.index("| GL | 2026 (PO N)"):dsum.index("Monthly per unit:")]
dsum = rep(dsum, old_tab, mdtable(["GL", "2026 (PO N)", "Existing: Dec-26 run rate /month", "Existing 2027", "New 2027 go-lives (units): 2027",
                                   "Capitalised labour (v8): 2027", "Total 2027", "Jan-27 /month", "Dec-27 /month"], [r_ for r_ in gt],
                                  ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]) + "\n")
dsum = rep(dsum, "Output = SUMIF by GL over all calc lines, then PO!U19:AF22.", "Output = SUMIF by GL over all calc lines, then PO!U19:AF22. v8: PO rows "
           f"20/21 also add section 9 (capitalised production labour, rows {RM['out_lift']}/{RM['out_tray']}); section 4 itself is unchanged.")
dsum = rep(dsum, "**Depreciation by GL, existing vs new**", "**Depreciation by GL, existing vs new units vs capitalised labour (v8)**")
old_h = dsum[dsum.index("| GL | Existing run rate | New units | Hand total | Workbook PO!Z (Jun-27) |"):dsum.index("**Existing fleet: PO 2026 monthly depreciation")]
hrows = []
for ln in old_h.strip().split("\n")[2:]:
    c_ = [x.strip() for x in ln.strip("|").split("|")]
    gl = c_[0]; hand_old = float(c_[3].replace(",", ""))
    labm = H["hand_lift"] if gl == "5011" else H["hand_tray"] if gl == "5012" else 0.0
    porow = {"5010": 19, "5011": 20, "5012": 21, "5020": 22}[gl]
    hrows.append([gl, c_[1], c_[2], f2(labm) if labm else "none", f2(hand_old + labm), f2(num(po8.cell(porow, 26).value))])
    assert abs(hand_old + labm - num(po8.cell(porow, 26).value)) < 0.006
dsum = rep(dsum, old_h, mdtable(["GL", "Existing run rate", "New units", "Capitalised labour (v8; section 5 of the labour section)", "Hand total", "Workbook PO!Z (Jun-27)"],
                                hrows, ["---", "---:", "---", "---:", "---:", "---:"]) + "\n")
A("## Depreciation schedule summary\n"); A(dsum + "\n")
ucr = sec7["Unit-cost reconciliation"].strip()
ucr += (f"\n\nv8: the DeploySum CapEx (and the 65,000 / 4,137.50 / 8,000 unit costs) holds no production labour. The capitalised labour is added on top "
        f"per vintage: {f0(LB['vint_total'])} in the 2027 go-lives (depreciable cost of the 2027 go-lives incl. labour "
        f"{f0(num(ds8['B121'].value) + LB['vint_total'])}), {f0(LB['to_2028'])} in the builds for 2028 go-lives.")
A("## Unit-cost reconciliation\n"); A(ucr + "\n")
A("## Revenue\n"); A(sec7["Revenue"].strip() + "\n")
A("## Assumptions register\n")
asr7 = sec7["Assumptions register"]
for aid, add in A_AMEND.items():
    line = [l for l in asr7.split("\n") if l.startswith(f"| {aid} |")][0]
    parts = line.split(" | ")
    parts[1] = parts[1] + add
    if aid == "A-28":
        parts[3] = rep(parts[3], "(workbook unchanged)", "(v8: replaced in the workbook)")
    asr7 = rep(asr7, line, " | ".join(parts))
asr7 = rep(asr7, "A-31..A-35 are new in v7", "A-36..A-41 are new in v8 and A-15, A-28, A-32, A-33 were amended in v8; A-31..A-35 are new in v7")
tab_end = asr7.index("\n\nA-22..A-25")
A(asr7[:tab_end].strip() + "\n" + "\n".join(md_issue(r_) for r_ in A_NEW) + "\n" + asr7[tab_end:].rstrip() + "\n")
A("## DeploySum refresh and tie-out (v3 build; unchanged in v4-v8)\n"); A(sec7["DeploySum refresh and tie-out (v3 build; unchanged in v4-v7)"].strip() + "\n")
A("## v7 -> v8 diff\n")
if AN:
    A("`diff_versions.py` (exact: formulas as text, cached values with no tolerance) on every sheet present in both files except Collation Notes:\n")
    A(mdtable(["Sheet", "Cells", "Formula diffs", "Value diffs"], [[k, f"{v['cells']:,}", v["formula_diffs"], v["value_diffs"]] for k, v in AN["diff"]["sheets"].items()]
              + [["**Total**", f"{AN['diff']['total']['cells']:,}", AN["diff"]["total"]["formula_diffs"], AN["diff"]["total"]["value_diffs"]]], ["---", "---:", "---:", "---:"]))
    A("Where the differences are (analyze_v8.py; every changed cell is an edited cell or in the static downstream trace of the edits):\n")
    A(mdtable(["Sheet", "Area", "Formula diffs", "Value diffs", "Allowed by the handoff as"], AN["allowed"]["areas"], ["---", "---", "---:", "---:", "---"]))
    A(f"Outside the allowed areas: **{AN['allowed']['outside']}** cells. 2026 columns (B:N) of COO P&L, FO, PO, CO, FE, PE: **{AN['allowed']['cols_2026']}** changed. "
      f"Cells outside the edits and their trace that LibreOffice moved by floating-point noise only were not written (max {NZ['noise_outside']['max_abs']:.1e}, "
      f"{NZ['noise_outside']['cells']} cells, kept at their v7 bytes).\n")
    A(f"Package: {AN['package']['identical']} of {AN['package']['v7_parts']} v7 parts byte-identical; changed: {', '.join(AN['package']['changed'])}.\n")
    A("## Error scan\n")
    A(mdtable(["Sheet", "v7", "v8"], [[k, v[0], v[1]] for k, v in AN["errors"]["by_sheet"].items()]))
    A(f"New errors in v8: **{AN['errors']['new']}**. Prod Payroll's 430 #NAME? cells of v7 are gone (XLOOKUP replaced, A-28).\n")
    A("## Package\n")
    A(f"Parts {AN['package']['v8_parts']} (v7 {AN['package']['v7_parts']}); `xl/externalLinks/*` **{AN['package']['external_links']}**; defined names "
      f"{AN['package']['defined_names']:,} (v7: {AN['package']['defined_names_v7']:,}).\n")
    A("## Sheets in the output\n")
    A(mdtable(["#", "Sheet", "State"], [[i + 1, s_, st] for i, (s_, st) in enumerate(AN["sheets"])]))
else:
    A("[pass 1: pending]\n")
A("## Severity scale\n"); A(sec7["Severity scale"].strip() + "\n")
A("## Issues (v8)\n")
A(f"Severity per the scale above. Open: {sev['HIGH']} HIGH, {sev['MED']} MED, {sev['LOW']} LOW; {sev['RESOLVED']} RESOLVED. v8: I-05 RESOLVED by policy (production "
  f"labour capitalised); I-40 (HIGH, scope of the policy) and I-41 (MED, material-handling roles) are new; I-07, I-11, I-14, I-17, I-23, I-25, I-37 and I-38 are "
  f"updated. No other severity changed.\n")
iss_rest = ib[ib.index("| ID | Sev"):]
A("\n".join(iss_rest.split("\n")[:2]) + "\n" + "\n".join(md_issue(r_) if (k in CHANGED or k in ISS_NEW) else md_rows7[k] for k, r_ in rows.items()) + "\n")
A(f"### Variance scan: rows with |AG-N| > $50k and > 50% (regenerated from the v8 workbook; the generator first reproduces the v7 table exactly)\n")
var_intro = var7.split("\n", 1)[1]
var_intro = var_intro[:var_intro.index("| Sheet | Row |")]
A(var_intro.strip() + f" v8: {len(var_added)} rows added, {len(var_changed)} changed, {len(var_removed)} removed (production labour capitalised).\n")
A("| Sheet | Row | Line | 2026 N | 2027 AG | Change | % |\n|---|---:|---|---:|---:|---:|---:|\n" + "\n".join(var8) + "\n")
cx = sec7["Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; unchanged in v6 and v7)"]
xd_head, xd_rest = cx.split("### Cross-department overlap", 1)
xd_body, xd_tail = xd_rest.split("**Prod Payroll trace", 1)
xd_body, n_xd = regen_xdept(xd_body)
xd_body = rep(xd_body, "(PO 5110-5140 typed and unlinked: see Prod Payroll trace;", "(PO 5110-5140 = 0 in 2027, capitalised in v8: see Prod Payroll trace;", count=3)
cx = xd_head + "### Cross-department overlap" + xd_body + "**Prod Payroll trace" + xd_tail
old_trace = re.search(r"(?m)^Rates and timing only:.*$", cx).group(0)
cx = rep(cx, old_trace,
         f"Rates and timing only: other sheets read only these typed raise inputs from Prod Payroll, never a headcount or cost cell, except the v8 capitalised-"
         f"labour block on the Depreciation Schedule (rows {RM['pp_lift']}-{RM['pp_total']} read Prod Payroll rows 41, 62, 79, 81; rows {RM['cur_lift']}-"
         f"{RM['cur_tray']} read its rate inputs). v8: Prod Payroll computes in full ({PPF['errors_v8']} errors; XLOOKUP replaced, A-28) and reaches the budget "
         f"only as capitalised-labour depreciation (PO 5011 / 5012). PO 5110-5140 2027 (PO!U33:AF35) are formulas = 0 (capitalised), and FO 5510 shares no "
         f"headcount source with Prod Payroll: no double count through Prod Payroll.")
rt_head, rt_rest = cx.split("### Raise timing consistency", 1)
rt_body, rt_tail = rt_rest.split("### Logistics & Warehouse payroll and MeLi", 1)
rt_body, n_rt, n_step, n_rows = regen_steps(rt_body)
rt_body = re.sub(r"(?m)^\d+ of \d+ payroll rows step by", f"{n_step} of {n_rows} payroll rows step by", rt_body, count=1)
rt_body = rep(rt_body, "in month 10 of 2027 (Prod Payroll!M6);", "in month 10 of 2027 (Prod Payroll!M6; v8: PO 5110-5140 are 0, capitalised);")
cx = rt_head + "### Raise timing consistency" + rt_body + "### Logistics & Warehouse payroll and MeLi" + rt_tail
old_po = re.search(r"(?m)^- PO 2027: .*$", cx).group(0)
pv = lambda s_, r_, c_: num(w8[s_].cell(r_, c_).value)
R5350 = [r_ for r_ in range(1, 140) if str(w8['PO'].cell(r_, 1).value).startswith('5350')][0]
cx = rep(cx, old_po, f"- PO 2027 (v8: production labour capitalised): 5110 - Salaries and Wages - Production {f0(pv('PO', 33, 33))}; 5130 - Payroll Taxes - "
         f"Production {f0(pv('PO', 34, 33))}; 5140 - Benefits - Production {f0(pv('PO', 35, 33))}; Total - 5100 - Labor Expense - Production "
         f"{f0(pv('PO', 36, 33))} (v7 {f0(PO7)}; 2026 {f0(pv('PO', 36, 14))}); 5350 - Warehouse {f0(pv('PO', R5350, 33))} (2026 {f0(pv('PO', R5350, 14))}). See I-17, I-41.")
A("## Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; v8: payroll rows regenerated)\n")
A(cx.strip() + "\n")
A("## Decisions\n")
A(sec7["Decisions"].strip())
DEC8 = [
    "D1 (v8): Patch, do not round-trip (v5 method). Stage 1 = v7 + the formula edits; LibreOffice recalculates it in full; values are written only for the edited "
    "cells and their static downstream trace (deps_v5.py), and the build stops if any other cell moves by more than 1e-6. Every other cell keeps its v7 bytes.",
    "D2 (v8): XLOOKUP is replaced by IF / INDEX / MATCH / ISNA (brief v5: INDEX/MATCH, 'next tier up, else max'), not v6's SMALL/COUNTIF: MATCH compares numbers "
    "directly, while COUNTIF(\"<\"&x) turns a decimal x into text. Proven equal three ways (v7 scratch, Python replica, model totals).",
    "D3 (v8): The capitalised labour is the Prod Payroll model ('the file's formula', brief v5), not the PO HC roster: the current 9 are capitalised at the "
    "model's rates (630,504), and their PO HC cost (652,820) leaves PO. The 22,315 difference between the two costings goes with it.",
    "D4 (v8): PO 5110-5140 2027 = (1 - B131) x the v7 amount, not a bare 0: the formula gives 0 when capitalised, keeps the v7 amount visible, and makes the "
    "sensitivity a single switch. Column AI labels the rows CAPITALISED.",
    "D5 (v8): Labour per unit by build month (brief v5 item 2) instead of v7's annual average; months with no builds roll forward (A-38). The bridge shows the "
    "effect of each change from v7's 64,735.",
    "D6 (v8): The Oct-Dec 26 labour is included where its builds go live in 2027 (brief v5), with a switch (B132); the Sep-26 labour is not added because its "
    "units went live in 2026 (inside the PO run rate); it is shown as a caveat row.",
    "D7 (v8): The new block sits below the existing schedule (rows 128+); section 4 (rows 79-82) is not edited, so the labour depreciation is added at PO rows "
    "20/21 (an allowed area) and row 197 gives the total.",
    "D8 (v8): Caveats: the v7 expensed / capitalised-on-top / inside-unit-cost rows are dropped (policy decided). Lower bound 1 uses the booked policy, lower bound "
    "2 the scope sensitivity; each uses the more adverse I-17 reading consistent with it. Upper end unchanged in kind (I-32 only).",
    "D9 (v8): Privacy. The md keeps v7's $5k rounding; the banner now says that $5k-multiple salaries stay exact (paylist_v8.py counts them). No per-person CSV is "
    "written; the scratch name lists are deleted after the build.",
]
A("\n".join(f"- {d}" for d in DEC8) + "\n")
A("## Not done / limits\n")
nd = sec7["Not done / limits"].strip()
v7cap = [l for l in nd.split("\n") if l.startswith("- v7: the capitalised case is an approximation")][0]
nd = rep(nd, v7cap, v7cap + " (v8: superseded - v8 rolls the cost per build month, capitalises the current staff and includes the Oct-Dec 26 labour.)")
xl_line = [l for l in nd.split("\n") if l.startswith("- Not opened in Microsoft Excel. Prod Payroll's XLOOKUP rows")][0]
nd = rep(nd, xl_line, xl_line + " (v8: replaced by INDEX/MATCH; evaluates in LibreOffice.)")
A(nd)
A("- v8: not opened in Microsoft Excel. The new formulas use standard functions (INDEX, MATCH, ISNA, IFERROR, SUMIF, SUMPRODUCT, EOMONTH, YEAR).")
A("- v8: idle months (no builds) are capitalised into the next build month (A-38); inventory rules may require abnormal idle-capacity labour to be expensed. "
  "Finance to confirm (I-40); not quantified separately beyond the Oct-26 and Jan-27 amounts in I-40.")
A("- v8: the existing-fleet run rate (PO Dec-26 forecast) carries no labour for 2026 go-lives; only the Sep-26 part is quantified (caveat row).")
A("- v8: 2026 columns are untouched, so 2026 still expenses its 5100 production labour; whether 2026 should also be restated is outside this budget (I-40).")
A("- v8: the Depreciation Schedule's text at A2 ('Section 4 feeds PO rows 19-22') predates v8 and was not edited (rows 1-126 are outside the allowed areas); "
  "Collation Notes records it.\n")
md = "\n".join(L)
assert "no exact per-person" not in md.lower()
am = paylist_v8.amounts(V8X, RECON)
md, n_round = paylist_v8.round_text(md, am)
hits, skipped = paylist_v8.find(md, am)
assert not hits, f"exact per-person amounts left in the md: {len(hits)}"
open(OUT_MD, "w").write(md)
print(f"report_v8: md {len(md):,} chars ({n_round} per-person amounts rounded, {skipped} coincidences left in non-people sections); Collation Notes JSON "
      f"{len(cnj):,} chars; issues {dict(sev)}; contribution {f0(C7)} -> {f0(C)}; sensitivity {f0(C_SENS)}; LB1 {f0(LB1)}, LB2 {f0(LB2)}, UB {f0(UB)}; "
      f"variance +{len(var_added)}/~{len(var_changed)}/-{len(var_removed)}; xdept {n_xd}, raise {n_rt}; pass {'2' if AN else '1'}")
