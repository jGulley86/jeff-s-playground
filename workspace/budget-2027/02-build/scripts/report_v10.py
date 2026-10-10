"""v10 notes (md) and Collation Notes (JSON for cnotes_v6.render), from figures_v10.py output. No typed figure.

Usage:
  python3 -I report_v10.py V9_MD CN9_JSON V10_XLSX FIG10_JSON RECON_LITE_JSON SPEC_JSON NOISE_JSON LO_VERSION_TXT V9_XLSX SD_BOOK \
      WORKFILE COO_BOOK DEPLOY_BOOK OUT_NOTES_JSON OUT_MD [ANALYZE_JSON]

- V9_MD / CN9_JSON: the v9 notes and the v9 Collation Notes (extracted). Rows that v10 does not change (decisions #2-#5,
  #7-#9; issues other than I-17, I-27, I-37, I-38, I-40, I-41; the revenue caveat text) are carried from them verbatim.
- The md rounds per-person amounts of identified employees to $5k (paylist_v7.round_text, as v7-v9); the Collation Notes keep
  exact figures (restricted workbook).
- The Collation Notes JSON never depends on ANALYZE_JSON, so pass 1 (before the final build) and pass 2 (after the checks) give
  the same JSON; the md of pass 2 adds the diff and check results.
- No name is read: people are '<tab> r<row> <title>'; the new CO employee is 'new CO employee (user-confirmed, 110k)'.
"""
import sys, os, re, json, hashlib, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paylist_v7

(V9MD, CN9, V10X, FIGJ, RECON, SPECJ, NOISEJ, LOV, V9X, SD, WF, COO, NEW, OUTJ, OUTMD) = sys.argv[1:16]
ANJ = sys.argv[16] if len(sys.argv) > 16 else None
F = json.load(open(FIGJ)); cn = json.load(open(CN9)); spec = json.load(open(SPECJ)); noise = json.load(open(NOISEJ))
AN = json.load(open(ANJ)) if ANJ else None
md9 = open(V9MD, encoding="utf-8").read()
NEWCO = "new CO employee (user-confirmed, 110k)"
BANNER = "CONFIDENTIAL – contains named compensation data (HC-* tabs); restrict distribution"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def f0(x):
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


def r5s(x):
    r = round(abs(x) / 5000) * 5000
    return "<5,000" if r == 0 else f"~{r:,.0f}"


def pct_nm(new, base):
    if base <= 0 or new < 0:
        return "n/m"
    return f"{(new - base) / base * 100:.0f}%"


def mdtable(header, rows):
    out = "| " + " | ".join(header) + " |\n|" + "|".join("---" for _ in header) + "|\n"
    for r in rows:
        out += "| " + " | ".join("" if v is None else str(v) for v in r) + " |\n"
    return out


C10, C9 = F["c10"], F["c9"]
L = F["lw"]; NC = F["newco"]; CO = F["co"]; PO = F["po"]; SC = F["sc"]; D = F["d"]; BU = F["burden"]; I37 = F["i37"]
OV = F["overlap9"]; I41 = F["i41"]; CAR = F["carried"]; HL = F["headline"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
REV = HL["rev"]["ag"]
seats = L["seats"]
S = {s["code"]: s for s in seats}
new_seats = [s for s in seats if s["in_co"] and s["code"] != "MH-01"]
NEW7 = sum(s["cost_2027"] for s in new_seats)
LW_SHEET = "'Logistics&WH Payroll'"
am = paylist_v7.amounts(V10X, RECON)


def is_pp(v):
    return isinstance(v, (int, float)) and abs(v) >= 1000 and any(abs(abs(v) - abs(a["v"])) < 0.01 for a in am)


def r5x(v):
    return f"({r5s(v)})" if v < 0 else r5s(v)

# ================================================================== caveat rows (exact; md rounds per-person values later)
cav = []   # [item, direction, what, effect (float or str), after (float or str), source]


def add(item, direction, what, effect, src):
    if direction == "RESOLVED":
        after = C10
    elif isinstance(effect, (int, float)):
        after = C10 + effect
    else:
        after = "-"
    cav.append([item, direction, what, effect, after, src])


add("Decision #10 scope: current 9 expensed (sensitivity, not booked)", "downside",
    f"If only the ramp is capitalised and the current PO staff stay expensed, PO 5110-5140 returns to the PO HC roster amount, now "
    f"without PO HC r20 (Material Handler = Logistics&WH MH-01, booked in CO since v10): {f0(SC['cur']['po5100'])} (v9 {f0(PO['base_v9'])}). "
    f"2027 capitalised labour falls to {f0(SC['cur']['capex'])} and its 2027 depreciation to {f0(SC['cur']['dep'])} (booked: {f0(SC['base']['dep'])}). "
    f"Recalculated with the workbook switch 'Depreciation Schedule'!B131 = 0. v9: {eff(-PO['base_v9'] + (SC['base']['dep'] - SC['cur']['dep']))}.",
    D["cur"], "'Depreciation Schedule'!B131; PO!U33:AF35; 'HC-PO'!M20:X20")
add("I-40 idle-month labour expensed (critic v8 B2; not booked)", "downside",
    f"Jan-27 builds nothing, so its labour rolls into the Feb-27 builds (A-38). If idle-month labour is a period cost ('Depreciation "
    f"Schedule'!B135 = 0) it is expensed in PO 5110-5140 and the depreciation of the Feb-27 builds falls. Recalculated; unchanged from v9 "
    f"(v10 does not touch the labour block). With the current staff expensed (B131 = 0): {eff(F['d_idle_under_cur'])}.",
    D["idle"], "'Depreciation Schedule'!B135, rows 221-228; PO!U33:AF35")
add("Decision #10 scope: all Sep-Dec 26 labour capitalised (B132 = 1; only with a 2026 restatement)", "downside",
    "Sep-Dec 26 model labour joins the Nov-26 and Jan-Feb 27 go-lives and is depreciated in 2027. Double counts the 2026 PO forecast "
    "unless 2026 is restated. Recalculated; unchanged from v9. Not in the range.", D["q4"], "'Depreciation Schedule'!B132; rows 231-232")
c = CAR["3"]; add(c["item"], c["direction"], c["what"] + " Carried from v9: " + c["why"] + ".", c["effect"], c["src"])
add("I-41 (7-overlap): Material Handling Team Lead stays expensed", "downside",
    f"v10: PO HC r20 Material Handler (= MH-01) is now booked in CO through the Logistics&WH model (user decision), so I-41 is down to "
    f"PO HC r16 Material Handling Team Lead. On the 7-of-9 role reading r16 is warehouse staff, not production labour; PO 5110-5140 = 0 "
    f"removes it and no expense line carries it: its 2027 cost at PO HC rates. 0 if r16 fills Logistics&WH seat TL-01 (same title, "
    f"Dec-26 start; then costed in CO). v9 (r16 + r20): {eff(-I41['v9_both'])}.",
    -I41["r16_cost"], "'HC-PO'!C16:Z16, D6:D7; PO!U33:AF35; Logistics&WH TL-01")
add("MH-01 on the 9-of-9 count reading: capitalised in PO and expensed in CO (v10)", "upside",
    f"Prod Payroll counts its 9 current staff by number only and is unchanged (brief v6). On the 9-of-9 reading one of those 9 is "
    f"PO HC r20 = MH-01, now expensed in CO 6610-6640: the capitalised labour then holds one head too many (the model's average current "
    f"cost per head {f0(OV['per_head'])}; 2027 CapEx overstated by that amount). Taking it out lowers 2027 labour depreciation pro rata "
    f"({pct(OV['dep_rate'], 2)} of 2027 capitalised payroll is depreciated in 2027). Not on the 7-of-9 reading.",
    OV["dep_effect"], "'Depreciation Schedule'!B214, R195, B236; Prod Payroll B9:C9")
add("Logistics&WH seats at CO HC burden rates instead of the model's (v10)", "upside",
    f"v10 books the logistics seats at the model's own rates (payroll tax {pct(L['tax'])}, benefits {pct(L['ben'])}: 'the WH and "
    f"logistics numbers'). CO HC rates are {pct(NC['co_d6'], 2)} / {pct(NC['co_d7'], 2)}. On the {f0(BU['ex_sal'])} of 2027 logistics "
    f"salaries in CO: burden {f0(BU['model'])} booked vs {f0(BU['co_rates'])} at CO HC rates. Both CO HC rates are unverified (I-37).",
    BU["diff"], "'Logistics&WH Payroll'!B5:B6; 'HC-CO'!D6:D7; CO!U68:AF69")
add(f"New CO employee start month (A-43; {NEWCO})", "upside",
    f"Booked as in seat all of 2027 (HC-CO r18, Jan-27 start, CO HC rates, 3% from Oct-27). Each month the start is later lowers 2027 "
    f"cost by {r5s(NC['per_month_jan'])} (Jan-Sep monthly cost incl. CO HC burden).", "per month later: ~" + f"{round(NC['per_month_jan'] / 5000) * 5000:,.0f}",
    "'HC-CO'!E18, M18:X18")
c = CAR["5"]; add(c["item"], c["direction"], c["what"] + " Carried from v9: " + c["why"] + ".", c["effect"], c["src"])
c = CAR["6"]; add(c["item"], c["direction"], c["what"] + " Carried from v9: " + c["why"] + " (the model still costs 9 current staff).", c["effect"], c["src"])
add("I-17", "RESOLVED",
    f"RESOLVED (user decision 2026-10-10): the Logistics&WH model is booked in CO 6610-6640, less seat LOG-01 (already on CO HC r17): "
    f"{f0(L['ex_total'])} in the headline (the 7 new seats {f0(NEW7)} + MH-01 {f0(S['MH-01']['cost_2027'])} at model rates). v9 showed it as "
    f"a downside of (336,530) to (471,093) depending on the reading.", "0 (now in the headline)", "CO!U67:AF69; 'Logistics&WH Payroll'!rows 34-46")
for k in ("10",):
    c = CAR[k]; add(c["item"], c["direction"], c["what"], c["effect"], c["src"])
add("I-26", "RESOLVED", F["i26_text"], "0 (now in the headline)", "Fld Eng Budget!B21 = 205,000")
for k in ("12", "13", "14", "15", "16", "17", "18", "19", "20", "21"):
    c = CAR[k]; add(c["item"], c["direction"], c["what"], c["effect"], c["src"])
add("I-37", "downside",
    f"CO and PE payroll tax below 7.65% (upper bound on every salary dollar). v10: the CO base now includes the {NEWCO} at the CO HC "
    f"rate ({pct(NC['co_d6'], 2)}) and the logistics salaries at the model rate ({pct(L['tax'])}): CO HC {f0(I37['co_hc'])} + logistics "
    f"{f0(I37['co_lw'])} + PE {f0(I37['pe'])}. v9: {eff(-I37['v9_reproduced'])}.", -I37["total"],
    "'HC-CO'!D6, Z67; 'Logistics&WH Payroll'!B5; 'HC-PE'!D6; CO!AG68; PE!AG68")
for k in ("23", "24", "25", "26", "27"):
    c = CAR[k]; add(c["item"], c["direction"], c["what"], c["effect"], c["src"])
add("A-14", "upside", "Depreciation convention: start the month after go-live (B13 = 1), recalculated on v10 (same as v9).", D["b13"],
    "'Depreciation Schedule'!B13 = 1")
c = CAR["29"]; add(c["item"], c["direction"], c["what"], "n/d", c["src"]); cav[-1][4] = "n/d"

# ================================================================== sign flip, range, conclusion
sing = F["singles"]; flips = F["singles_flip"]; pairs = F["pairs_flip"]
nonflip = [s for s in sing if s[3] >= 0]
LB1, LB2, UP = F["lb1"], F["lb2"], F["upper"]
R9 = F["v9_range"]
up32 = CAR["16"]["effect"]; up32t = CAR["17"]["effect"]; up32c = CAR["18"]["effect"]
def signflip_txt(md):
    def a_(v, eff_v):       # contribution after an item; rounded in the md when the item is one person's cost
        return r5x(v) if (md and is_pp(eff_v)) else f0(v)
    return (f"Sign-flip statement (computed, v10): with the Logistics&WH payroll and the {NEWCO} booked in CO, the 2027 COO contribution is "
            f"{f0(C10)} (v9 {f0(C9)}). Single quantified items that turn it negative: "
            + "; ".join(f"{s_[1]} {eff(s_[2])} -> {f0(s_[3])}" for s_ in flips) + ". "
            f"The other downsides leave it positive on their own (smallest remaining: "
            + "; ".join(f"{s_[1]} {a_(s_[3], s_[2])}" for s_ in nonflip[:3]) + "). "
            f"Pairs of the remaining range components (idle months, I-41, I-31 shortfall, I-05 burden, O7) that turn it negative: "
            + ("; ".join(f"{a} + {b} ({r5s(-v) if (md and any(is_pp(F_DOWN[x]) for x in (a, b))) else f0(-v)})" for a, b, v in pairs) if pairs else "none") + ". "
            f"With both switches the sensitivity + idle-month pair is recalculated, not added: {f0(F['pair_sens_idle'])}. "
            f"With costs held fixed, revenue {f0(C10)} ({pct(F['rev_breakeven_pct'])}) below plan also takes the contribution to zero.")


F_DOWN = {s_[1]: s_[2] for s_ in sing}
signflip = signflip_txt(False)
upside = (f"Upside: I-32 can add up to {f0(up32)} (contribution {f0(C10 + up32)}); the trend alternative adds {f0(up32t)} ({f0(C10 + up32t)}), "
          f"or {f0(up32c)} ({f0(C10 + up32c)}) if the decline also ran through Oct-Dec 26. Labour already in the unit cost (O1): up to "
          f"{eff(CAR['3']['effect'])} ({f0(C10 + CAR['3']['effect'])}). Logistics at CO HC burden rates {eff(BU['diff'])}; MH-01 on the 9-of-9 "
          f"reading {eff(OV['dep_effect'])}.")
lb1_txt = "; ".join(f"{a} {f0(b)}" for a, b in LB1["items"])
lb2_txt = "; ".join(f"{a} {f0(b)}" for a, b in LB2["items"])
range_txt = (f"Range (v10): asymmetric by construction, as in v7-v9. Lower bound 1, booked policy, all quantified downsides ({lb1_txt}): "
             f"{f0(LB1['value'])}. Lower bound 2, the same under the scope sensitivity, components at B131 = 0 ({lb2_txt}; I-41 is 0 there: r16 "
             f"is expensed in PO 5110-5140): {f0(LB2['value'])}. Upper end, I-32 in full only: {f0(UP)}. Not in the range: I-37 (unverified "
             f"upper bound); B132 = 1 (only with a 2026 restatement); the O1, burden-rate and 9-of-9 MH-01 upsides. The I-17 terms of v9 are "
             f"gone (booked). v9 range: {f0(R9['lb1'])} to {f0(R9['upper'])} (lower bound 2 {f0(R9['lb2'])}).")
concl = (f"Conclusion: booking the Logistics&WH payroll ({f0(L['ex_total'])}) and the {NEWCO} in CO lowers the 2027 COO contribution from "
         f"{f0(C9)} (v9) to {f0(C10)}. Two single items now turn it negative on their own (the scope sensitivity, Decision #10, and I-10, "
         f"the FO/FE lines budgeted at 0), and two pairs of smaller downsides do as well. Treat {f0(C10)} as a point estimate inside "
         f"{f0(LB1['value'])} to {f0(UP)} (lower bound 2: {f0(LB2['value'])}) until Decisions #10 (I-40) and #2 (I-32) are answered, I-10 "
         f"is confirmed, and the PO owner says whether the Material Handling Team Lead (I-41) fills TL-01.")

# ================================================================== decisions table (rows #1, #6, #10 regenerated)
dec_cn = copy.deepcopy(cn["sections"][1]["table"])
assert [r[0] for r in dec_cn["rows"]] == [str(i) for i in range(1, 11)]
r1 = dec_cn["rows"][0]
old = "Contribution 687,435 (v8 638,814, v7 139,032)."
assert old in r1[3], r1[3]
r1[3] = r1[3].replace(old, f"Contribution v10 {f0(C10)} (v9 {f0(C9)}; v10 books the Logistics&WH payroll and the {NEWCO} in CO, Decision #6).")
r6 = ["6", "RESOLVED (user decision 2026-10-10: 'The WH and logistics numbers should hit central operations, along with [the named CO "
      "employee]'; 'Yes, the material handler should move to CO.'). Warehouse payroll (Logistics&WH) and the material-handling roles",
      "I-17 (RESOLVED), I-41",
      f"Booked in v10: CO 6610-6640 (2027) = CO HC roster (incl. the {NEWCO}) + the Logistics&WH model less seat LOG-01 (already CO HC "
      f"r17): {f0(L['ex_total'])} = the 7 new seats {f0(NEW7)} + MH-01 {f0(S['MH-01']['cost_2027'])}, at the model's rates "
      f"({pct(L['tax'])} / {pct(L['ben'])}); new-hire cost {f0(L['nh'])} to 6610. MH-01 (= PO HC r20) is out of the PO 5110-5140 B131 base.",
      f"Resolved. Still open: PO HC r16 Material Handling Team Lead on the 7-of-9 reading (I-41): {eff(-I41['r16_cost'])} if its cost stays "
      f"an expense, 0 if r16 fills TL-01. Logistics at CO HC burden rates: {eff(BU['diff'])}.", "User (resolved); PO owner for r16"]
dec_cn["rows"][5] = r6
r10 = dec_cn["rows"][9]
r10[3] = r10[3] + " v10: the B131 base holds 8 PO HC people; PO HC r20 (MH-01) is in CO."
r10[4] = (f"Current staff expensed (sensitivity): {eff(D['cur'])} -> {f0(SC['cur']['c'])}. Idle-month labour expensed (B135 = 0): "
          f"{eff(D['idle'])} -> {f0(SC['idle']['c'])} (with the current staff expensed too: {f0(SC['idlecur']['c'])}). All Sep-Dec 26 labour "
          f"capitalised (B132 = 1; only with a 2026 restatement): {eff(D['q4'])} -> {f0(SC['q4']['c'])}. Each is one switch on the "
          f"Depreciation Schedule; the workbook recalculates.")

# ================================================================== tables shared by md and Collation Notes
co_hdr = ["GL (CO, 2027)", "v9", "CO HC roster, 5 existing people", f"{NEWCO} (HC-CO r18)", "Logistics&WH less LOG-01", "v10", "v10 - v9", "Check (must be 0)"]
co_rows = []
for gl, lab in (("6610", "6610 Salaries and Wages (incl. new-hire cost)"), ("6630", "6630 Payroll Taxes"), ("6640", "6640 Benefits")):
    e = CO[gl]
    co_rows.append([lab, e["v9"], e["hc_v10"] - e["new"], e["new"], e["lw"], e["v10"], e["v10"] - e["v9"], e["check"]])
t = CO["total"]
co_rows.append(["Total 6610-6640", t["v9"], t["hc_v10"] - t["new"], t["new"], t["lw"], t["v10"], t["v10"] - t["v9"],
                sum(CO[g]["check"] for g in ("6610", "6630", "6640"))])
seat_hdr = ["Seat", "Team", "Start", "Annual base", "2027 salary", "2027 cost at model rates (incl. new-hire cost)", "Booked in CO 6610-6640?"]
seat_rows = []
for s in seats:
    if s["code"] == "LOG-01":
        where = "no: already CO HC r17 Field Logistics Manager (CO HC rates); excluded by formula (row 43 - row 34)"
    elif s["code"] == "MH-01":
        where = "yes: = PO HC r20 Material Handler (moved PO -> CO; out of the PO B131 base)"
    else:
        where = "yes: new seat (no HC roster)" + ("; same title as PO HC r16 (I-41)" if s["code"] == "TL-01" else "") + \
                (f"; hired {s['start']}, on no roster (I-38)" if s["code"] in ("TL-01", "MH-02") else "")
    seat_rows.append([s["seat"], s["team"], s["start"], s["annual"], s["sal_2027"], s["cost_2027"], where])
seat_rows.append(["Total booked in CO (8 seats)", "", "", "", L["ex_sal"], L["ex_total"], f"tax {f0(L['ex_tax'])}, benefits {f0(L['ex_ben'])}, new-hire cost {f0(L['nh'])}"])
seat_rows.append(["Model total (9 seats)", "", "", "", L["sal"], L["total_2027"], f"= 'Logistics&WH Payroll'!S47; LOG-01 {f0(L['log01_cost'])}"])
sc_hdr = ["Case", "2027 CapEx: payroll capitalised", "2027 labour depreciation", "PO 5110-5140 2027 (expense)", "Dec-27 PP&E in service (net)",
          "Dec-27 CIP (not yet in service)", "2027 COO contribution v10", "vs booked v10", "2027 COO contribution v9"]
v9sc = {r[0]: r[6] for r in cn["sections"][11]["table"]["rows"]}


def v9c(prefix):
    for k, v in v9sc.items():
        if k.startswith(prefix):
            return v
    raise KeyError(prefix)


sc_rows = [
    ["Booked: Prod Payroll labour capitalised incl. the current staff; Sep-Dec 26 labour a 2026 cost; idle months rolled forward", "base", v9c("Booked (v9)")],
    ["Sensitivity (not booked): only the ramp capitalised; the current PO staff stay expensed (B131 = 0); v10 base without PO HC r20", "cur", v9c("Sensitivity")],
    ["Idle-month labour expensed (B135 = 0)", "idle", v9c("Idle-month labour expensed (B135 = 0)")],
    ["Idle-month labour expensed and the current staff expensed (B131 = 0, B135 = 0)", "idlecur", v9c("Idle-month labour expensed and")],
    ["All Sep-Dec 26 labour capitalised (B132 = 1; only with a 2026 restatement)", "q4", v9c("All Sep-Dec 26")],
    ["B132 = 1 and the current staff expensed (B131 = 0)", "q4cur", v9c("B132 = 1 and")],
]
sc_tab = [[lab, f0(SC[k]["capex"]), f0(SC[k]["dep"]), f0(SC[k]["po5100"]), f0(SC[k]["ppe"]), f0(SC[k]["cip"]), f0(SC[k]["c"]),
           "-" if k == "base" else f0(SC[k]["c"] - C10), v9] for lab, k, v9 in sc_rows]
chg_hdr = ["Item", "What v10 did", "Where"]
chg_rows = [
    ["Logistics&WH Payroll tab", f"Copied from the SD book (Service_Delivery_PL_worksheets_v2.xlsx; values identical to the original SD input) cell by cell with "
     f"styles, notes and merged cells, after HC-COO. {L['formulas']} formulas; they read DeploySum, Fld Ops Payroll and Prod Payroll in the "
     f"workbook. LibreOffice recalculation: 0 errors; 2027 total {f2(L['total_2027'])} (verified 547,441.22); check B60 = {f0(L['check_B60'])}; "
     f"max difference vs the SD cached values {L['max_diff_vs_sd_cache']:.1e} over {L['cells_compared']} cells. The SD sheet's empty "
     f"drawing part was not copied.", "'Logistics&WH Payroll'!A1:Y87"],
    ["CO 6610 / 6630 / 6640 (2027)", f"Typed values -> formulas: 'HC-CO' rows 67-69 + Logistics&WH rows 43 / 44 / 45 less seat LOG-01 (row 34 "
     f"x (1, B5, B6)); new-hire cost (row 46) -> 6610. 2027 total {f0(CO['total']['v9'])} -> {f0(CO['total']['v10'])}. Notes in AI67:AI69.",
     "CO!U67:AF69, AI67:AI69; subtotals and ratios rows 73, 116, 117, 132, 137-142"],
    ["New CO employee", f"{NEWCO}: HC-CO row 18 (the empty current-employee row): annual 110,000, Jan-27 to Dec-27, 3% from Oct-27, CO HC "
     f"rates. CO 6610-6640 read the roster total, so the cost flows from the roster. Name on HC-CO only.", "'HC-CO'!B18:E18 (+ row 18 and rows 67-70 values)"],
    ["Material handler PO -> CO", f"PO 5110-5140 B131 base = v7 amount less PO HC r20 (= MH-01) at PO HC rates: {f0(PO['base_v9'])} -> "
     f"{f0(PO['base_v10'])} (2027). Booked values unchanged (0, capitalised).", "PO!U33:AF35 (formulas; values 0)"],
    ["Headline", f"{f0(C9)} -> {f0(C10)}: Logistics&WH {eff(-L['ex_total'])}, {NEWCO} {eff(-NC['cost_2027'])}.", "COO P&L!AG132"],
    ["I-17", "RESOLVED (user decision). I-41, I-37, I-38, I-27, I-40 updated; Decision #6 RESOLVED; caveats, range and sign-flip recomputed.", "Issues; caveats"],
    ["Downstream outside the listed areas", "HC-COO (organisation roll-up of the HC tabs; formulas unchanged) shows the new CO person in its 2027 "
     "CO rows and totals. No 2026 column moves.", "'HC-COO'!M:Z rows 18-75"],
]

# ================================================================== Collation Notes JSON
N = copy.deepcopy(cn)
N["title"] = "2027 COO Budget - Collation Notes (build v10, draft for review)"
Sx = N["sections"]
assert Sx[0]["heading"] == BANNER
Sx[0]["lines"] = ["This workbook holds employee names and salaries on the HC-* tabs (copied from the COO HC & PL workfile) and seat-holder "
                  "names on the 'Logistics&WH Payroll' tab (copied from the SD book). Share it only with people cleared to see compensation. "
                  "This sheet keeps exact figures. The notes file (02-build_notes_v10.md) rounds per-person amounts to the nearest $5k, but a "
                  "salary that is itself a multiple of $5k is unchanged by that rounding, so some unique-role salaries appear there at their exact "
                  "value. The new CO employee's name is on HC-CO r18 only."]
Sx[1]["table"] = dec_cn
Sx[1]["heading"] = "Decisions pending (user) - not resolved by the builder (v10: #6 RESOLVED by the user)"
hd = Sx[2]["table"]
assert hd["header"][-1] == "2027 in v8 (value)"
hd["header"][-1] = "2027 in v9 (value)"
keys = ["rev", "cogs", "dep", "gp", "opex", "noi", "other", "ni"]
for row, k in zip(hd["rows"], keys):
    h = HL[k]
    row[2]["v"] = h["n"]; row[3]["v"] = h["ag"]; row[4]["v"] = h["ag"] - h["n"]; row[5]["v"] = pct_nm(h["ag"], h["n"]); row[6] = round(h["ag9"], 2)
cav_lines = [
    f"(0) v10 (user decision 2026-10-10): the Logistics & Warehouse payroll and the {NEWCO} are booked in Central Operations. CO 6610-6640 "
    f"2027 {f0(CO['total']['v9'])} -> {f0(CO['total']['v10'])}: Logistics&WH less LOG-01 {f0(L['ex_total'])} (7 new seats {f0(NEW7)}, MH-01 "
    f"{f0(S['MH-01']['cost_2027'])}; model rates), {NEWCO} {f0(NC['cost_2027'])} (CO HC rates). The contribution moves from {f0(C9)} to {f0(C10)}. "
    f"Production labour stays capitalised (Decision #1): 2027 CapEx +{f0(SC['base']['capex'])}, labour depreciation {f0(SC['base']['dep'])}. "
    f"Scope sensitivity (current staff expensed): {f0(SC['cur']['c'])}; idle-month labour expensed: {f0(SC['idle']['c'])}.",
    f"(0b) Year on year is not like-for-like: 2026 expensed production labour, 2027 capitalises it. Policy effect in v10: +{f0(F['policy_effect'])} "
    f"(PO 5110-5140 at B131 = 0 {f0(SC['cur']['po5100'])} + the ramp {f0(F['ramp'])} - booked labour depreciation {f0(SC['base']['dep'])}; v9 "
    f"+{f0(F['policy_effect_v9_check'])}): on the 2026 policy the 2027 contribution would be {f0(C10 - F['policy_effect'])}.",
    f"(1) What the figure is. The bottom line, {f0(C10)}, is a COO contribution: the company's recognized revenue ({f0(REV)}, all of it) less the "
    f"costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: {f0(HL['cogs']['ag'] + HL['opex']['ag'])}). It is not company "
    f"Net Income; the workbook row keeps its GL label 'Net Income' (COO P&L!A132).",
    Sx[3]["lines"][3],
    "(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. Rows marked 'Carried from v9' "
    "have inputs v10 does not touch (the v9 -> v10 diff shows 0 changes there); the switch rows are recalculated on v10.",
]
assert Sx[3]["lines"][3].startswith("(2) What the revenue is.")
Sx[3]["lines"] = cav_lines
Sx[3]["table"]["rows"] = [[r[0], r[1], r[2], round(r[3], 2) if isinstance(r[3], float) else r[3],
                           round(r[4], 2) if isinstance(r[4], float) else r[4], r[5]] for r in cav]
Sx[3]["table"]["after"] = [signflip, upside, range_txt, concl, "v7-v9 sign-flip and range statements: see 02-build_notes_v9.md."]
Sx[5]["lines"] = Sx[5]["lines"] + ["v10: CO!AI67:AI69 describe the v10 CO payroll formulas. PO!AI33:AI35 (v8/v9 notes) were not edited (the "
                                   "v10 diff is confined to PO!U33:AF35 there); the 5110-5140 base is now 'the v7 amount less PO HC r20'."]
Sx[6]["lines"] = [f"Base: v9 collated workbook. v10 (brief v6): new tab 'Logistics&WH Payroll'; HC-CO row 18 ({NEWCO}); CO U67:AF69 "
                  f"formulas and AI67:AI69 notes; PO U33:AF35 formulas (B131 base less PO HC r20); the downstream CO / COO P&L subtotals and "
                  f"ratio rows, HC-CO rows 67-70 and the HC-COO roll-up. Every other cell has 0 formula and 0 value differences vs v9; no 2026 "
                  f"column (B:N) of the P&L tabs changes.",
                  "Full notes: 02-build/02-build_notes_v10.md. Figures: figures_v10.py (from the workbook and 7 LibreOffice recalculations of "
                  "switch scenarios, scen_v8.py); numbers on this sheet are live formulas (headline) or values computed by those scripts."]
Sx[7] = {"heading": "Changes from v9 (brief v6: Logistics&WH payroll and the new CO employee booked in CO)", "table": {"header": chg_hdr, "rows": chg_rows, "after": []}}
Sx[10]["table"]["after"] = [f"v10: the GL lines above are unchanged; the contribution is {f0(C10)} (CO payroll, see 'Changes from v9')."]
Sx[11]["table"] = {"header": sc_hdr, "rows": sc_tab, "after": [f"v10: the B131 = 0 base excludes PO HC r20 (MH-01, booked in CO): PO 5110-5140 "
                                                                f"{f0(PO['base_v9'])} -> {f0(PO['base_v10'])} (5110 {f0(PO['by_gl_v10']['5110'])}, "
                                                                f"5130 {f0(PO['by_gl_v10']['5130'])}, 5140 {f0(PO['by_gl_v10']['5140'])})."]}
Sx[15]["lines"] = [f"v10: PO HC r20 (MH-01) is booked in CO through the Logistics&WH model (user decision). Prod Payroll is unchanged and still "
                   f"counts 9 current staff. 9-of-9 reading: MH-01 is then capitalised (one of the 9) and expensed in CO: +{f0(OV['dep_effect'])} "
                   f"of 2027 depreciation if taken out of the capitalised labour. 7-of-9 reading: no MH-01 overlap; PO HC r16 (Material Handling "
                   f"Team Lead) is in no expense line: {eff(-I41['r16_cost'])} (I-41), 0 if r16 fills TL-01."]
rec = Sx[17]
rec["heading"] = "Payroll reconciliation (v10): HC roster vs P&L payroll lines (2027, salary + tax + benefits)"
rec["lines"] = rec["lines"][:1] + [
    f"PO: PO HC 9 = {f0(PO['hcpo_Z70'])}. PO 5110-5140 2027 = 0 (capitalised, Decision #1). B131 = 0 base = PO HC less r20 (MH-01, now in CO): "
    f"{f0(PO['base_v10'])} (v9 {f0(PO['base_v9'])}). Prod Payroll capitalises its 9 current staff by count (unchanged).",
    f"CO: CO 6610-6640 = CO HC roster {f0(CO['total']['hc_v10'])} ({F['hcco']['people10']} people: the 5 of v9 + the {NEWCO}) + "
    f"Logistics&WH less LOG-01 {f0(L['ex_total'])} (8 seats incl. MH-01) = {f0(CO['total']['v10'])} (v9 {f0(CO['total']['v9'])}).",
    re.sub(r"^CO: CO HC 5 = CO 6610-6640\. ", "", rec["lines"][3])]
assert rec["lines"][-1].startswith("PE: "), rec["lines"][-1][:40]
rr = rec["table"]["rows"]
assert rr[1][0] == "PO" and rr[2][0] == "CO"
rec["table"]["header"] = rec["table"]["header"] + ["v10 P&L line (2027)"]
for r in rr:
    r.append(None)
rr[1][-1] = f"0 booked; B131 = 0: {f0(PO['base_v10'])}"
rr[2][2] = F["hcco"]["people10"]; rr[2][3] = round(F["hcco"]["Z70_10"], 2); rr[2][-1] = round(CO["total"]["v10"], 2)
for r in rr:
    if r[-1] is None:
        r[-1] = r[4]
# assumptions: A-43..A-45
Sx[20]["table"]["rows"] += [
    ["A-43", f"{NEWCO}: current employee in seat for all of 2027 (Jan-Dec 27), CO HC rates (D6 / D7), CO 3% raise from Oct-27 (D8); HC-CO r18 "
     f"start Jan-27 so no 2026 column moves", f"2027 cost {f0(NC['cost_2027'])}", "'HC-CO'!B18:Z18; CO!U67:AF69", "user (salary 110,000, 2026-10-10); builder (timing)"],
    ["A-44", "Logistics&WH seats booked at the model's own burden rates (6.8% / 16.4%), not CO HC rates", f"{eff(BU['diff'])} at CO HC rates (caveat)",
     "'Logistics&WH Payroll'!B5:B6; CO!U68:AF69", "orchestrator (handoff v10)"],
    ["A-45", "Logistics&WH new-hire cost ($1,000 per 2027 hire) booked in 6610, as the FO model books it in 5510", f"{f0(L['nh'])} (5 hires)",
     "'Logistics&WH Payroll'!row 46; CO!U67:AF67", "builder (v10)"],
]
# issues
iss = Sx[21]
iss["heading"] = iss["heading"].replace("Issues (v9)", "Issues (v10)")
irows = {r[0]: r for r in iss["table"]["rows"]}
v9_i17 = irows["I-17"]
irows["I-17"][:] = ["I-17", "RESOLVED", "'Logistics&WH Payroll'!A14:S51; CO!U67:AF69; 'HC-CO'!B17:C17; 'HC-PO'!B20:C20; PO!U33:AF35",
    f"RESOLVED (user decision 2026-10-10: 'The WH and logistics numbers should hit central operations'; 'Yes, the material handler should "
    f"move to CO.'). v10 copies the SD Logistics&WH Payroll tab into the workbook and books it in CO 6610-6640 (2027) by formula, less "
    f"seat LOG-01 (= CO HC r17, already in CO): {f0(L['ex_total'])} = the 7 new seats ({f0(NEW7)}) + MH-01 ({f0(S['MH-01']['cost_2027'])} at "
    f"model rates; = PO HC r20, which leaves the PO 5110-5140 B131 base). New-hire cost ({f0(L['nh'])}) to 6610. Was (v9, HIGH): not carried; "
    f"(336,530) net, (398,492) at the 9-overlap, (471,093) at the 7-overlap.",
    "Seats: " + "; ".join(f"{s['code']} {f0(s['cost_2027'])} ({s['start']})" for s in seats) + f". CO 6610-6640 check (v10 - HC-CO - "
    f"logistics less LOG-01) = {f2(sum(CO[g]['check'] for g in ('6610', '6630', '6640')))}.",
    f"{eff(-L['ex_total'])} booked in the headline", "user decision",
    f"None for the booking. Open: burden rates (A-44, {eff(BU['diff'])} at CO HC rates); r16 vs TL-01 (I-41); Q4-26 hires on no roster (I-38)."]
irows["I-41"][3] = irows["I-41"][3] + (f" v10: PO HC r20 (MH-01) is booked in CO through the Logistics&WH model (user decision) and left the PO "
    f"B131 base, so I-41 is down to r16 (Material Handling Team Lead): {eff(-I41['r16_cost'])} on the 7-of-9 reading, 0 if r16 fills "
    f"Logistics&WH TL-01 (same title, Dec-26). On the 9-of-9 count reading MH-01 is still one of Prod Payroll's 9 current staff (model "
    f"unchanged): capitalised in PO and expensed in CO; taking one head ({f0(OV['per_head'])}) out of the capitalised labour gives "
    f"+{f0(OV['dep_effect'])} of 2027 depreciation.")
irows["I-41"][5] = f"{eff(-I41['r16_cost'])} (v10, r16 only; v9 (134,563) for r16 + r20)"
irows["I-37"][3] = irows["I-37"][3] + (f" v10: the CO base now includes the {NEWCO} (CO HC rate) and the logistics salaries (model rate 6.8%): "
                                       f"CO + PE gap at 7.65% {eff(-I37['total'])} (v9 {eff(-I37['v9_reproduced'])}).")
irows["I-37"][5] = f"up to {eff(-I37['total'])} CO/PE (v9 (56,801)); up to (34,169) FO/FE"
irows["I-37"][6] = f"impact {f0(I37['total'])} ($50k-250k)"
irows["I-41"][6] = f"impact {f0(I41['r16_cost'])} ($50k-250k)"
irows["I-40"][4] = "v9 figures: " + irows["I-40"][4]
irows["I-40"][5] = (f"{eff(D['cur'])} if the current staff stay expensed; {eff(D['idle'])} if idle-month labour is expensed; together "
                    f"{eff(SC['idlecur']['c'] - C10)}")
irows["I-40"][6] = f"impact {f0(-D['cur'])} (> $250k)"
irows["I-38"][3] = irows["I-38"][3] + (f" v10: the Logistics&WH model is in the budget (CO): TL-01 (Dec-26) and MH-02 (Oct-26) are booked for all of "
                                       f"2027 although no roster holds them; if they were not hired, CO is overstated by their 2027 cost (TL-01 "
                                       f"{f0(S['TL-01']['cost_2027'])}, MH-02 {f0(S['MH-02']['cost_2027'])} at model rates).")
irows["I-27"][3] = irows["I-27"][3] + " v10: the Logistics&WH tab is now in the workbook ('Logistics&WH Payroll'!B56); MH-05 is still in neither model."
irows["I-40"][3] = irows["I-40"][3] + (f" v10: the B131 base excludes PO HC r20 (MH-01, in CO): sensitivity {eff(D['cur'])} -> {f0(SC['cur']['c'])} "
                                       f"(v9 (621,499) -> 65,936).")
sev = {}
for r in iss["table"]["rows"]:
    sev[r[1]] = sev.get(r[1], 0) + 1
F_sev = sev
# new section: Logistics&WH in CO, CO before -> after
new_sec = {"heading": "Logistics & Warehouse payroll booked in CO; new CO employee (v10, user decision 2026-10-10; I-17 RESOLVED)",
           "lines": [f"CO 6610 = 'HC-CO'!row 67 + 'Logistics&WH Payroll'!row 43 - row 34 + row 46; 6630 = 'HC-CO'!row 68 + row 44 - row 34 x B5; "
                     f"6640 = 'HC-CO'!row 69 + row 45 - row 34 x B6 (2027 months U:AF <- F:Q / M:X). Seat LOG-01 (row 34) is CO HC r17 and is "
                     f"excluded by formula. MH-01 (row 38) = PO HC r20, now out of the PO 5110-5140 base. New-hire cost -> 6610 (A-45).",
                     f"{NEWCO}: HC-CO r18, 110,000 a year, Jan-27 to Dec-27, +3% from Oct-27, CO HC rates {pct(NC['co_d6'], 3)} / "
                     f"{pct(NC['co_d7'], 3)}: 2027 salary {f2(NC['sal_2027'])}, tax {f2(NC['tax_2027'])}, benefits {f2(NC['ben_2027'])}, total "
                     f"{f2(NC['cost_2027'])} (A-43)."],
           "table": {"header": co_hdr, "rows": [[r[0]] + [round(v, 2) for v in r[1:]] for r in co_rows], "after": []}}
seat_sec = {"heading": "Logistics&WH seats (model rates 6.8% / 16.4%; 2027)",
            "table": {"header": seat_hdr, "rows": [[r[0], r[1], r[2], round(r[3], 2) if isinstance(r[3], float) else r[3],
                                                    round(r[4], 2), round(r[5], 2), r[6]] for r in seat_rows], "after": []}}
Sx.insert(4, new_sec); Sx.insert(5, seat_sec)
json.dump(N, open(OUTJ, "w"), indent=1, ensure_ascii=False)

# ================================================================== md
def md_cav_row(r):
    def fmt(v):
        return f0(v) if isinstance(v, (int, float)) else str(v)
    eff_s = (eff(r[3]) if isinstance(r[3], (int, float)) else str(r[3]))
    if is_pp(r[3]):          # one identified person's cost: the 'after' figure would reveal it, so round it as v9 did
        return [r[0], r[1], r[2], eff_s, r5x(r[4]), r[5]]
    return [r[0], r[1], r[2], eff_s, fmt(r[4]), r[5]]


md = []
w = md.append
w("# 02-build notes v10 - 2027 COO budget collation\n")
w(f"> **{BANNER}.** The workbook's HC-* tabs hold employee names and salaries, and the 'Logistics&WH Payroll' tab (copied from the SD "
  f"book in v10) names seat holders; share the workbook and these notes only with people cleared to see compensation. In this file "
  f"per-person amounts for identified employees are rounded to the nearest $5k (shown with '~') or aggregated. Rounding does not change an "
  f"amount that is already a multiple of $5k, so some unique-role salaries (one person per role) still appear at their exact value; the "
  f"Collation Notes sheet keeps exact figures. A department total compared across versions, or a bound that includes one person's cost, can "
  f"also reveal that cost. The {NEWCO} is named on HC-CO r18 only.\n")
w("## Decisions pending\n")
w(f"Decision #1 (production labour capitalised) and, in v10, Decision #6 (warehouse payroll: user decision 2026-10-10, booked in CO) are "
  f"RESOLVED. 8 decisions remain open: #2-#5 and #7-#9 as in v9, and #10 (scope of the capitalisation policy; numbers recomputed). The "
  f"budget carries the 'current treatment' column. Effects are on the 2027 COO contribution, each on its own.\n")
# md decision rows: v9 md rows for unchanged ones (already rounded); regenerated rows otherwise
dm = re.search(r"\| # \| Decision \(user\).*?\n\|---.*?\n((?:\|.*\n)+)", md9)
md_dec_rows = [l for l in dm.group(1).splitlines()]
assert len(md_dec_rows) == 10
out_rows = []
for i, l in enumerate(md_dec_rows):
    if i in (0, 5, 9):
        out_rows.append("| " + " | ".join(str(x) for x in dec_cn["rows"][i]) + " |")
    else:
        out_rows.append(l)
w("| # | Decision (user) | Issue | Current treatment in the budget | Alternatives: effect on 2027 COO contribution (+ raises, ( ) lowers) | Who |\n|---|---|---|---|---|---|\n" + "\n".join(out_rows) + "\n")
w("## Headline: 2027 COO contribution\n")
hrows = []
for lab, k in (("Revenue (company recognized revenue, 9/30/26 sales plan)", "rev"), ("COGS (COO departments)", "cogs"),
               ("  of which depreciation (in COGS)", "dep"), ("Gross Profit", "gp"), ("Opex (COO departments)", "opex"),
               ("COO contribution before other income (workbook label 'Net Ordinary Income')", "noi"), ("Net Other Income", "other"),
               ("**COO contribution (workbook label 'Net Income')**", "ni")):
    h = HL[k]
    hrows.append([lab, h["row"], f0(h["n"]), f0(h["ag"]), f0(h["ag"] - h["n"]), pct_nm(h["ag"], h["n"]) + (" (a)" if k == "ni" else ""),
                  f0(h["ag9"]), eff(h["ag"] - h["ag9"])])
w(mdtable(["Line", "COO P&L row", "2026 (N)", "2027 v10 (AG)", "Change", "%", "2027 v9 (AG)", "v10 - v9"], hrows))
w(f"(a) Year on year is not like-for-like: 2026 expensed production labour, 2027 capitalises it. Policy effect in v10 +{f0(F['policy_effect'])} "
  f"(v9 +{f0(F['policy_effect_v9_check'])}; lower because PO HC r20 is now in CO, an expense either way): on the 2026 policy the 2027 "
  f"contribution would be {f0(C10 - F['policy_effect'])}.\n")
w(f"- **2027 COO contribution (COO P&L AG132): {f0(C10)}** (v9 {f0(C9)}, {eff(C10 - C9)}). The whole change is CO 6610-6640: the Logistics&WH "
  f"payroll less LOG-01 {eff(-L['ex_total'])} (7 new seats {eff(-NEW7)}; MH-01 {eff(-S['MH-01']['cost_2027'])}) and the {NEWCO} "
  f"{eff(-NC['cost_2027'])}. Revenue {f0(REV)}; COGS + Opex {f0(HL['cogs']['ag'] + HL['opex']['ag'])}.")
w(f"- PO is unchanged in the booked figure (5110-5140 = 0, capitalised). MH-01 leaves the PO B131 base (sensitivity), so it is counted once.")
w(f"- Issues: {F_sev.get('HIGH', 0)} HIGH, {F_sev.get('MED', 0)} MED, {F_sev.get('LOW', 0)} LOW open; {F_sev.get('RESOLVED', 0)} RESOLVED. v10: "
  f"I-17 RESOLVED (user decision); I-27, I-37, I-38, I-40 and I-41 updated.\n")
w(f"**Headline caveat: v10 books the Logistics & Warehouse payroll ({f0(L['ex_total'])}: 7 new seats and the material handler MH-01, at the "
  f"model's 6.8% / 16.4% rates; the Logistics Manager seat LOG-01 is already on CO HC) and the {NEWCO} ({f0(NC['cost_2027'])}, CO HC rates, "
  f"full year assumed) in Central Operations. The 2027 COO contribution falls from {f0(C9)} to {f0(C10)}. It is now thin: the scope "
  f"sensitivity (current staff expensed: {f0(SC['cur']['c'])}) and I-10 (FO/FE lines at 0: {f0(C10 + CAR['10']['effect'])}) each turn it "
  f"negative on their own. Production labour stays capitalised (2027 CapEx +{f0(SC['base']['capex'])}; 2027 labour depreciation "
  f"{f0(SC['base']['dep'])}).**\n")
w("### Caveats on the headline (read before using the figure)\n")
w(f"(1) What the figure is. The bottom line, {f0(C10)}, is a **COO contribution**: the company's recognized revenue ({f0(REV)}, all of it) "
  f"less the costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: {f0(HL['cogs']['ag'] + HL['opex']['ag'])}). Costs "
  f"outside COO are not in this workbook, so it is **not company Net Income**. The workbook row keeps its GL label 'Net Income' (COO P&L!A132).\n")
m2 = re.search(r"^\(2\) What the revenue is\..*$", md9, re.M)
w(m2.group(0) + "\n")
w("(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. 'Carried from v9' = the item's inputs "
  "are outside every cell v10 changes (the v9 -> v10 diff shows 0 changes there), so v9's computed effect stands; the switch rows are "
  "recalculated on v10. I-17 is RESOLVED (booked).\n")
w(mdtable(["Item", "Direction", "What could happen", "Effect on 2027 COO contribution", "Contribution after this item alone", "Source cells"],
          [md_cav_row(r) for r in cav]))
w(f"**{signflip_txt(True)}** {upside}\n")
w(f"**{range_txt}**\n")
w(mdtable(["Bound", "What it adds to the headline", "2027 COO contribution"],
          [["Lower bound 1 (booked policy, all quantified downsides)", lb1_txt, f0(LB1["value"])],
           ["Lower bound 2 (scope sensitivity: current staff expensed; components at B131 = 0)", lb2_txt, f0(LB2["value"])],
           ["Point estimate", "-", f0(C10)], ["Upper end", "I-32 in full only", f0(UP)]]))
w(f"**{concl}**\n")
w("## Changes from v9\n")
w("Brief v6 (user, 2026-10-10): 'The WH and logistics numbers should hit central operations, along with [the named CO employee].' The "
  "employee's salary is $110,000 a year. 'Yes, the material handler should move to CO.' Every item of the brief is done; nothing is declined.\n")
w(mdtable(chg_hdr, chg_rows))
w("## Logistics & Warehouse payroll in Central Operations (I-17 RESOLVED)\n")
w(f"**What is booked.** CO 6610 / 6630 / 6640, 2027 months (U:AF), are formulas: the CO HC roster total ('HC-CO' rows 67 / 68 / 69, now "
  f"including the {NEWCO}) + the Logistics&WH model's salaries / payroll taxes / benefits (rows 43 / 44 / 45) less seat LOG-01 (row 34; "
  f"burdened with the model's B5 / B6), + the model's new-hire cost (row 46) on 6610. LOG-01 Logistics Manager is CO HC r17 Field Logistics "
  f"Manager, already in the CO roster at CO HC rates, so it is excluded by formula and counted once (check below). MH-01 Material Handler "
  f"(row 38) is PO HC r20 Material Handler (same person; same 2027 salary, difference {f2(PO['mh01_model_vs_hc_sal_diff'])}); it moves to CO "
  f"through this model, as the user confirmed, and leaves the PO base (next section).\n")
w(f"**New-hire cost.** {f0(L['nh'])} in 2027 ({f0(L['hires_2027'])} hires at {f0(L['nh_per_hire'])}: INV-01 Feb, MH-03 Mar, MH-04 Jun, TL-02 Jul, "
  f"MH-06 Jul) is booked in 6610 Salaries and Wages, the same way the SD field model books its new-hire cost in FO 5510 (A-45). 6660 "
  f"Recruiting would also fit, but it is outside the areas this build may change; moving it would not change the total.\n")
w(f"**Burden rates (A-44, caveat).** The seats are booked at the model's own rates, payroll tax {pct(L['tax'])} and benefits {pct(L['ben'])} "
  f"('the WH and logistics numbers'), not CO HC rates ({pct(NC['co_d6'], 2)} / {pct(NC['co_d7'], 2)}). On the {f0(BU['ex_sal'])} of 2027 "
  f"logistics salaries in CO the burden is {f0(BU['model'])}; at CO HC rates it would be {f0(BU['co_rates'])}: {eff(BU['diff'])} on the "
  f"contribution. CO now carries two rate bases (roster people at CO HC rates, logistics seats at model rates). The CO HC tax rate is below "
  f"7.65% and unverified (I-37).\n")
w(mdtable(seat_hdr, [[r[0], r[1], r[2], f0(r[3]) if isinstance(r[3], float) else r[3], f0(r[4]), f0(r[5]), r[6]] for r in seat_rows]))
w(f"Seats the model's own check block excludes (unchanged): LOG-02 (budgeted in FO) and MH-05 (in no model, I-27). The tab in the workbook: "
  f"{L['formulas']} formulas, 0 errors after LibreOffice recalculation, 2027 total {f2(L['total_2027'])}, check B60 = {f0(L['check_B60'])}, "
  f"max difference vs the SD book's cached values {L['max_diff_vs_sd_cache']:.1e} over {L['cells_compared']} cells.\n")
mrows = [["Logistics&WH seats in CO (headcount, excl. LOG-01)"] + [f0(x) for x in L["hc_ex_by_month"]] + [""],
         ["Logistics&WH cost in CO (excl. LOG-01)"] + [f0(x) for x in L["cost_ex_by_month"]] + [f0(sum(L["cost_ex_by_month"]))]]
for gl in ("6610", "6630", "6640"):
    mrows.append([f"CO {gl} v10"] + [f0(x) for x in CO[gl]["months_v10"]] + [f0(CO[gl]["v10"])])
    mrows.append([f"CO {gl} v9"] + [f0(x) for x in CO[gl]["months_v9"]] + [f0(CO[gl]["v9"])])
w(mdtable(["Row (2027)"] + MON + ["2027"], mrows))
w("## New CO employee (HC-CO r18)\n")
w(f"- Who: the {NEWCO}. The user named the person in chat; the name is on HC-CO r18 only, like the other roster rows, and not in these "
  f"notes, the Collation Notes or any CSV (none written).")
w(f"- Assumption A-43 (labelled): a current employee in seat for all of 2027, Jan-Dec 27. HC-CO r18 starts Jan-27 (E18), so the row's "
  f"Sep-Dec 26 columns are 0 and no 2026 figure moves; if the person is already on payroll in 2026, the 2026 CO forecast (book data, not "
  f"part of this build) would need checking.")
w(f"- Annual salary 110,000 (user-confirmed), the CO 3% raise from Oct-27 (G18 / H18 = D8, as every CO roster row), CO HC rates D6 / D7 "
  f"({pct(NC['co_d6'], 3)} / {pct(NC['co_d7'], 3)}).")
w(f"- 2027 cost: salary {f0(NC['sal_2027'])}, payroll tax {f0(NC['tax_2027'])}, benefits {f0(NC['ben_2027'])}, total {f0(NC['cost_2027'])}. "
  f"CO 6610-6640 read the roster total ('HC-CO' rows 67-69), so the cost flows from HC-CO.")
w(f"- CO HC roster: {F['hcco']['people9']} -> {F['hcco']['people10']} people with a 2027 cost; HC-CO 2027 total {f0(F['hcco']['Z70_9'])} -> "
  f"{f0(F['hcco']['Z70_10'])}.\n")
w("## CO 6610 / 6630 / 6640: v9 -> v10 (2027, AG)\n")
w(mdtable(co_hdr, [[r[0]] + [f0(v) if i < 6 else f2(v) for i, v in enumerate(r[1:])] for r in co_rows]))
w("Check = v10 less the HC-CO roster less the logistics model less LOG-01; 0 means LOG-01 is not double counted and nothing else enters. "
  "The HC-CO roster's 5 existing people equal the v9 typed values in every month (the old constants were HC-CO rows 67-69).\n")
w(mdtable(["CO subtotal (AG)", "v9", "v10", "v10 - v9"], [[k, f0(v["v9"]), f0(v["v10"]), eff(v["v10"] - v["v9"])] for k, v in CO["subtotals"].items()]))
w("## PO: material handler out of the B131 base; the B131 sensitivity\n")
w(f"PO!U33:AF35 (5110 / 5130 / 5140, 2027) = (1 - 'Depreciation Schedule'!B131) x (v7 amount less PO HC r20 {PO['r20_title']} at PO HC "
  f"rates: 'HC-PO'!M20:X20, x D6, x D7) + the idle labour of that GL. In the booked case (B131 = 1, B135 = 1) every cell is 0, as in v9, so "
  f"the booked P&L does not move. Under the sensitivity (B131 = 0) PO 5110-5140 now holds 8 PO HC people; r20 is in CO through MH-01, so it "
  f"is counted once in every case.\n")
w(mdtable(["PO 2027 (B131 = 0)", "v9", "v10", "v10 - v9"],
          [[gl, f0(PO["by_gl_v9"][gl]), f0(PO["by_gl_v10"][gl]), eff(PO["by_gl_v10"][gl] - PO["by_gl_v9"][gl])] for gl in ("5110", "5130", "5140")] +
          [["5110-5140", f0(PO["base_v9"]), f0(PO["base_v10"]), eff(PO["base_v10"] - PO["base_v9"])]]))
w(f"The difference is PO HC r20 at PO HC rates (salary x (1 + {pct(PO['pd6'], 2)} + {pct(PO['pd7'], 2)})); the same person costs "
  f"{f0(S['MH-01']['cost_2027'])} in CO at the model's rates.\n")
w(mdtable(sc_hdr, sc_tab))
w(f"Each case is a LibreOffice recalculation of a scratch copy of v10 with the switches changed (scen_v8.py). The sensitivity is now "
  f"{f0(SC['cur']['c'])} ({eff(D['cur'])} vs booked; v9 (621,499)): the switch no longer adds r20 back to PO (r20 is in CO in "
  f"every case), and it starts from the lower v10 headline. Prod Payroll (capitalised labour) still counts 9 current staff by number (unchanged, brief v6): see I-41 / the 9-vs-7 overlap.\n")
w("## Payroll reconciliation (v10)\n")
w("v10 changes the PO and CO rows; FO, FE and PE are unchanged from v9 (see 02-build_notes_v9.md, 'Payroll reconciliation').\n")
w(mdtable(["Dept", "GL", "HC roster (people with a 2027 cost; 2027 total)", "SD model in the P&L", "P&L 2027 v10", "P&L 2027 v9", "Overlaps / notes"],
          [["PO", "5110-5140", f"{PO['hcpo_people']}; {f0(PO['hcpo_Z70'])}", "Prod Payroll (capitalised labour, 5011 / 5012 depreciation)",
            f"0 (B131 = 0 base: {f0(PO['base_v10'])})", f"0 (B131 = 0 base: {f0(PO['base_v9'])})",
            "r20 Material Handler = Logistics&WH MH-01: now in CO, out of the PO base; Prod Payroll's 9 current staff are a count match (I-41)"],
           ["CO", "6610-6640", f"{F['hcco']['people10']}; {f0(F['hcco']['Z70_10'])} (v9 {F['hcco']['people9']}; {f0(F['hcco']['Z70_9'])})",
            f"Logistics&WH less LOG-01: {f0(L['ex_total'])} (8 seats)", f0(CO["total"]["v10"]), f0(CO["total"]["v9"]),
            "r17 Field Logistics Manager = LOG-01 (excluded from the model part); MH-01 = PO HC r20"]]))
w(f"**9 by count vs 7 by role (I-41), updated.** One of PO HC's 9 is now in CO. On the 9-of-9 count reading Prod Payroll's 9 current staff "
  f"include r20; r20 (MH-01) is now expensed in CO and still capitalised in PO through the model's count: one head too many in the capitalised "
  f"labour ({f0(OV['per_head'])} of 2027 CapEx at the model's average current cost; {eff(OV['dep_effect'])} of 2027 depreciation if taken out). "
  f"On the 7-of-9 role reading the model's 9 seats are the 7 production staff plus 2 seats no roster fills, so there is no MH-01 overlap; "
  f"r16 Material Handling Team Lead is warehouse staff that no expense line carries ({eff(-I41['r16_cost'])}), unless r16 fills Logistics&WH "
  f"TL-01 (same title, Dec-26 start), in which case it is in CO already. The model is left unchanged, as the brief asks.\n")
# issues
w("## Issues (v10)\n")
w(f"Severity as in v9 (HIGH = blocks sign-off or > $250k; MED = $50k-250k or owner confirmation; LOW = < $50k or hygiene). Open: "
  f"{F_sev.get('HIGH', 0)} HIGH, {F_sev.get('MED', 0)} MED, {F_sev.get('LOW', 0)} LOW; {F_sev.get('RESOLVED', 0)} RESOLVED. v10: I-17 "
  f"RESOLVED (user decision); I-27, I-37, I-38, I-40 and I-41 updated (no severity change). Rows not listed as changed are carried from v9.\n")
im = re.search(r"\| ID \| Sev \| Location \(sheet!cell\).*?\n\|---.*?\n((?:\|.*\n)+)", md9)
md_iss = {l.split("|")[1].strip(): l for l in im.group(1).splitlines()}
CHG = ("I-17", "I-27", "I-37", "I-38", "I-40", "I-41")
lines = []
for r in iss["table"]["rows"]:
    if r[0] in CHG:
        lines.append("| " + " | ".join(str(x).replace("\n", " ") for x in r) + " |")
    else:
        lines.append(md_iss[r[0]])
w("| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |\n|---|---|---|---|---|---|---|---|\n" + "\n".join(lines) + "\n")
w("## Assumptions added in v10\n")
w(mdtable(["ID", "Assumption", "Value / effect", "Where", "Source"], Sx[22]["table"]["rows"][-3:] if Sx[22]["heading"] == "Assumptions register" else []))
w("A-01..A-42 are unchanged (02-build_notes_v9.md, 'Assumptions register').\n")
# diff / checks (pass 2)
w("## v9 -> v10 diff\n")
if AN:
    dd = AN["diff"]
    w(f"diff_versions.py, every cell of the 6 P&L tabs and every driver / HC tab present in both files (Collation Notes excluded; it is "
      f"regenerated): {dd['total']['cells']:,} cells, {dd['total']['formula_diffs']} formula differences, {dd['total']['value_diffs']} value "
      f"differences; comments added / removed / changed {dd['comments']}. New sheet: {', '.join(dd['only_new'])}.\n")
    w(mdtable(["Sheet", "Area", "Cells (formula or value differs)"], [[a["sheet"], a["area"], a["cells"]] for a in AN["areas"]]))
    w(f"Outside the allowed areas: {AN['outside']} cells. 2026 columns (B:N) of COO P&L / FO / PO / CO / FE / PE: {AN['cols26']} changes. "
      f"Package parts changed: {', '.join(AN['parts_changed'])}; added: {', '.join(AN['parts_added'])}.\n")
    w("## Error scan\n")
    w(f"LibreOffice recalculation of the v10 file: error cells {AN['errors_v10']} (v9 recalculation {AN['errors_v9']}); new errors "
      f"{AN['new_errors']}. 'Logistics&WH Payroll': {AN['lw_errors']} errors. Stored values vs the recalculation (every sheet except "
      f"Collation Notes): max difference {AN['recalc_max_diff']:.1e} over {AN['recalc_cells']:,} numeric cells; non-numeric differences "
      f"{AN['recalc_nonnum']}. COO P&L = FO + PO + CO + FE + PE on every GL row (2027 months and AG): max difference "
      f"{AN['sum_depts_max']:.1e}; check row 133 max |value| {AN['row133_max']:.1e}.\n")
    w("## Completion criteria (v10)\n")
    w(mdtable(["Criterion", "Result"], [[k, v] for k, v in AN["criteria"].items()]))
else:
    w("(filled in pass 2 from analyze_v10.py)\n")
w("## Build and sources\n")
w(f"Output: `02-build/02-build_COO_2027_Budget_Collated_v10.xlsx` and this file (v1-v9 files unchanged; no v10 CSV).  \n"
  f"Scripts: `02-build/scripts/` - v10 entry point `run_build_v10.sh`: build_v10.py stage1 (edits on v9) -> recalc.sh (LibreOffice full "
  f"recalculation) -> patches_v10.py (static downstream trace, deps_v5.py; values of the edited cells and their downstream set only; stops if "
  f"anything else moves > 1e-6) -> build_v10.py final -> scen_v8.py + recalc.sh (7 switch scenarios) -> figures_v10.py -> report_v10.py "
  f"pass 1 -> build_v10.py final with Collation Notes -> diff_versions.py v9 -> v10, recalc.sh, figures_v10.py again on the final file (must "
  f"be identical) -> names_v10.py + privacy_v6.py (names) and paylist_v10.py (per-person amounts) -> analyze_v10.py -> report_v10.py pass 2 "
  f"(Collation Notes JSON must equal pass 1) -> scratch name lists deleted. `run_build_v9.sh` ... `run_build.sh` still reproduce v9 ... v1.  \n"
  f"Inputs (read-only): `Service_Delivery_PL_worksheets_v2.xlsx` sha256 `{sha(SD)}`; `COO_HC_and_PL_workfile.xlsx` sha256 `{sha(WF)}`; "
  f"`COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `{sha(COO)}`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `{sha(NEW)}`.  \n"
  f"Base: v9 workbook sha256 `{sha(V9X)}`. LibreOffice: {open(LOV).read().strip()}. Python run with -I. The new CO employee's name is read "
  f"from a file outside the repository (run_build_v10.sh argument), never from the scripts.\n")
w("## Sections of the v9 notes not restated\n")
w("Unchanged by v10 and not repeated here (02-build_notes_v9.md): production labour capitalisation (method, labour per unit, CapEx and "
  "Dec-27 balance sheet, hand recompute, idle months, bridge), Prod Payroll XLOOKUP replacement, other v7 checks, the FO / FE / PE payroll "
  "reconciliation and the duplicate scan, HC tabs, Head of Service Delivery, depreciation schedule summary, unit-cost reconciliation, revenue, "
  "assumptions A-01..A-42, DeploySum tie-out, variance scan, cross-department checks. Where those sections quote the v9 contribution "
  "(687,435) or the v9 caveats, this file supersedes them.\n")
w("## Decisions (v10, builder)\n")
for d in [
    "D1 (v10): Patch the v9 package (v5 method). Stage 1 = v9 + the edits; LibreOffice recalculates it in full; values are written only for the "
    "edited cells and their static downstream trace, and only where the recalculated value moves by more than 1e-6 (smaller moves are float "
    "noise and keep their v9 bytes). The build stops if any other cell moves.",
    "D2 (v10): The Logistics&WH tab is copied at the XML level (build_v6 method): SD styles appended to styles.xml, theme colours resolved to "
    "RGB, shared strings inlined; appended after HC-COO so no existing sheet index moves. The tab's own text names seat holders (SD input as "
    "supplied); the banner says so.",
    "D3 (v10): LOG-01 is excluded in the CO formulas as 'model total less row 34 burdened' (salary row 34, x B5, x B6), so the tab stays an "
    "unedited copy of the SD model and the exclusion is visible in CO.",
    "D4 (v10): CO 6610-6640 read the HC-CO roster totals (rows 67-69) instead of the v9 typed values: they are equal for the 5 existing people "
    "(checked every month), and the new CO employee then flows from the roster as the brief asks.",
    "D5 (v10): New-hire cost to 6610 (A-45), consistent with FO 5510; 6660 Recruiting is outside the allowed diff.",
    "D6 (v10): The new CO employee starts Jan-27 on HC-CO (E18) rather than the row's Sep-26 default: same 2027 cost, and no 2026 column moves "
    "(brief: in seat all of 2027). Title left as a placeholder (not given).",
    "D7 (v10): The PO base drops PO HC r20 at PO HC rates (its roster cost), not at model rates; PO!AI33:AI35 notes are not edited (the "
    "allowed PO area is the base cells); Collation Notes records the new base.",
    "D8 (v10): Caveat items whose inputs v10 does not touch carry v9's computed effects (listed per row); the switch scenarios, I-37, I-41 and "
    "the new items are recomputed on v10. Pairs for the sign-flip are taken from the range components (v9 rule).",
    "D9 (v10): HC-COO (organisation roll-up of the HC tabs) recalculates with the new HC-CO row. It is not in the handoff's list of allowed "
    "areas, but it is a downstream consequence of the required HC-CO row (formulas unchanged); reported, not suppressed.",
]:
    w("- " + d)
w("")
w("## Not done / limits\n")
for d in [
    "Not opened in Microsoft Excel (LibreOffice recalculation only).",
    "The new CO employee's title and start date were not given; the title cell holds a placeholder and the timing is assumption A-43.",
    "Prod Payroll still counts 9 current staff (brief v6: leave the model unchanged); the 9-of-9 MH-01 overlap is quantified as a caveat, not booked.",
    "Logistics&WH TL-01 / MH-02 (Q4-26 hires on no roster, I-38) are booked as the model has them; whether they were hired is for the PO owner.",
    "The 2026 CO forecast is book data and was not changed; if the new CO employee or the logistics hires are already on payroll in 2026, "
    "2026 would need a separate update.",
    "PO!AI33:AI35 still describe the v8/v9 formula ('the v7 amount'); the v10 base (less PO HC r20) is described here and on Collation Notes.",
]:
    w("- " + d)
text = "\n".join(md) + "\n"
# privacy: per-person amounts of identified employees -> nearest $5k (people sections only)
paylist_v7.NO_PEOPLE = paylist_v7.NO_PEOPLE + ("## v9 -> v10 diff", "## Error scan", "## Completion criteria", "## Build and sources")
text, nrep = paylist_v7.round_text(text, am, md=True)
open(OUTMD, "w", encoding="utf-8").write(text)
print(f"report_v10: md {len(text.splitlines())} lines ({nrep} per-person amounts rounded); Collation Notes {len(N['sections'])} sections; "
      f"issues {F_sev}; pass {'2' if AN else '1'}")
