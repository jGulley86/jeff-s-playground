"""v9 figures: every new number in the v9 notes (critic v8 B1 / B2 / O1-O7 on top of the v8 capitalisation).

Usage:
  python3 -I figures_v9.py V7_XLSX V8_XLSX V9_XLSX PP7_LO_XLSX SPEC_JSON SC_CUR SC_Q4 SC_B13 SC_IDLE SC_IDLECUR SC_Q4CUR FIG7_JSON RECON_JSON CN7_JSON OUT_JSON

  V7_XLSX, V8_XLSX  the delivered v7 and v8 workbooks (cached values)
  V9_XLSX      the v9 workbook (cached values = LibreOffice recalculation, patched by patches_v9.py)
  PP7_LO_XLSX  LibreOffice recalculation of the v7 scratch copy with Prod Payroll row 48 as SMALL/COUNTIF (prodpay_v6.py)
  SPEC_JSON    build_v9.py stage1 spec (edited cells, row map of the labour block incl. section 11)
  SC_*         LibreOffice recalculations of v9 scratch copies (scen_v8.py), each one switch away from the booked v9
               (B131 = 1, B132 = 0, B133 = 2, B13 = 0, B135 = 1): cur B131 = 0 (current 9 expensed: the sensitivity);
               q4 B132 = 1 (all Sep-Dec 26 labour capitalised); b13 B13 = 1; idle B135 = 0 (idle-month labour expensed);
               idlecur B131 = 0 and B135 = 0; q4cur B131 = 0 and B132 = 1
  FIG7_JSON    figures_v7.py output (v7 figures: I-05, I-17, MH-01, O1, O6, d9)
  RECON_JSON   recon_v6.py output on v7 (no names)
  CN7_JSON     the v7 Collation Notes (cnotes_v6.py extract): carried caveat rows

Independent checks done here:
  - Python replica of the whole Prod Payroll model from its input cells (as v8), vs the v9 workbook.
  - Python replica of the labour block (sections 8-11) incl. the v9 switches (B132 for all Sep-Dec 26 labour, B135 idle months),
    vs the workbook and vs every scenario recalculation.
  - Hand recompute of one month (Jun-27) of labour depreciation by vintage, vs PO!Z20 / Z21 (v9 - v7).
  - v8 -> v9 change = the 2027 depreciation of the Oct-Dec 26 labour (B1) exactly; nothing else moves.
No figure is typed here; constants are read from cells.
"""
import sys, json, math, datetime, calendar
import openpyxl

(V7, V8OLD, V8, PP7, SPEC, SC_CUR, SC_Q4, SC_B13, SC_IDLE, SC_IDLECUR, SC_Q4CUR, FIG7, RECON, CN7, OUT) = sys.argv[1:16]
w7 = openpyxl.load_workbook(V7, data_only=True)
wprev = openpyxl.load_workbook(V8OLD, data_only=True)
w8 = openpyxl.load_workbook(V8, data_only=True)          # NB: in this script w8 / P8 / S8 are the v9 (current) workbook
pp7 = openpyxl.load_workbook(PP7, data_only=True)
spec = json.load(open(SPEC)); RM = spec["rowmap"]
F7 = json.load(open(FIG7)); R = json.load(open(RECON)); cn7 = json.load(open(CN7))
sc = {k: openpyxl.load_workbook(p, data_only=True) for k, p in (("cur", SC_CUR), ("q4", SC_Q4), ("b13", SC_B13), ("idle", SC_IDLE),
                                                                 ("idlecur", SC_IDLECUR), ("q4cur", SC_Q4CUR))}
DSN = "Depreciation Schedule"


def num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0


out = {}
P8 = w8["Prod Payroll"]; D8 = w8["DeploySum"]; S8 = w8[DSN]
N = 16
COLS = list(range(2, 18))                                       # B..Q
dates = [D8.cell(4, c).value for c in COLS]
MON = [d.strftime("%b-%y") for d in dates]
inp = lambda a: num(P8[a].value)

# ------------------------------------------------------------------ 1. Prod Payroll replica (from input cells only)
lift_tiers = [num(P8.cell(15, c).value) for c in range(2, 16)]
lift_inc = [num(P8.cell(16, c).value) for c in range(2, 16)]
tray_tiers = [num(P8.cell(20, c).value) for c in range(2, 16)]
tray_inc = [num(P8.cell(21, c).value) for c in range(2, 16)]
lift_tot = [sum(lift_inc[:k + 1]) for k in range(14)]
tray_tot = [sum(tray_inc[:k + 1]) for k in range(14)]
assert tray_tiers == sorted(set(tray_tiers)) and lift_tiers == sorted(set(lift_tiers))
built_l = [num(D8.cell(24, c).value) for c in COLS]; built_t = [num(D8.cell(25, c).value) for c in COLS]
rate_l = [built_l[i] / (dates[i].day / 7) for i in range(N)]; rate_t = [built_t[i] / (dates[i].day / 7) for i in range(N)]
B5, C5, H5 = inp("B5"), inp("C5"), inp("H5")
B6, C6, H6, B7, C7, H7 = inp("B6"), inp("C6"), inp("H6"), inp("B7"), inp("C7"), inp("H7")
B8, C8, B9, C9 = inp("B8"), inp("C8"), inp("B9"), inp("C9")
H8, H9, H10 = inp("H8"), inp("H9"), inp("H10")
M5, M6, M7, M8, M9, M10 = inp("M5"), P8["M6"].value, inp("M7"), inp("M8"), inp("M9"), inp("M10")
ab_l = [num(P8.cell(33, c).value) for c in COLS]; ot_l = [num(P8.cell(35, c).value) for c in COLS]
ab_t = [num(P8.cell(54, c).value) for c in COLS]; ot_t = [num(P8.cell(56, c).value) for c in COLS]
ab_s = [num(P8.cell(73, c).value) for c in COLS]
# salary input S9 = weighted hourly x 2080 (row 5-7, Q/R/S)
S9 = sum(num(P8.cell(r, 17).value) * num(P8.cell(r, 18).value) * 2080 for r in (5, 6, 7))
assert abs(S9 - B5) < 1e-6 and abs(S9 - C5) < 1e-6


def eom(d, m):
    y, mo = d.year, d.month + m
    while mo <= 0: mo += 12; y -= 1
    while mo > 12: mo -= 12; y += 1
    return datetime.datetime(y, mo, calendar.monthrange(y, mo)[1])


ref = eom(M6, -int(M9) - 1)
IDX = dates.index(ref) if ref in dates else 0


def roundup(x):
    return math.ceil(x - 1e-12) if x >= 0 else -math.ceil(-x - 1e-12)


def xlookup_next(x, tiers):
    for t in tiers:
        if t >= x:
            return t
    return max(tiers)


def block(hc, sal, tax, ben, ab, ot, hires, hire_cost):
    base = [hc[i] * sal / 12 + (min(hc[i], hc[IDX]) * sal / 12 * M5 if dates[i] >= M6 else 0) for i in range(N)]
    a = [base[i] * ab[i] for i in range(N)]; o = [base[i] * ot[i] * M10 for i in range(N)]
    t = [(base[i] + a[i] + o[i]) * tax for i in range(N)]; b = [base[i] * ben for i in range(N)]
    tot = [base[i] + a[i] + o[i] + t[i] + b[i] + hires[i] * hire_cost for i in range(N)]
    return tot, {"base": base, "abs": a, "ot": o, "tax": t, "ben": b}


def headcount(req_by_month, current):
    req, prev = [], 0
    for i, v in enumerate(req_by_month):
        prev = v if i == 0 else max(prev, v); req.append(prev)
    inc = [max(0, r - current) for r in req]
    hires = [inc[0]] + [max(0, inc[i] - inc[i - 1]) for i in range(1, N)]
    return [current + x for x in inc], hires


tier_l = [min(max(B8, roundup(rate_l[i])), max(lift_tiers)) for i in range(N)]
hc_l, hires_l = headcount([lift_tot[lift_tiers.index(t)] for t in tier_l], B9)
tier_t = [xlookup_next(max(C8, rate_t[i]), tray_tiers) for i in range(N)]
hc_t, hires_t = headcount([tray_tot[tray_tiers.index(t)] for t in tier_t], C9)
L, Lp = block(hc_l, B5, B6, B7, ab_l, ot_l, hires_l, M7)
T, Tp = block(hc_t, C5, C6, C7, ab_t, ot_t, hires_t, M7)
tc = [hc_l[i] + hc_t[i] for i in range(N)]
req_s, prev = [], 0
for i in range(N):
    v = max(H9, roundup(tc[i] / H8)); prev = v if i == 0 else max(prev, v, H9); req_s.append(prev)
inc_s = [max(0, r - H10) for r in req_s]
hc_s = [H10 + x for x in inc_s]
hires_s = [inc_s[0]] + [max(0, inc_s[i] - inc_s[i - 1]) for i in range(1, N)]
base_s = [hc_s[i] * H5 / 12 + (min(hc_s[i], hc_s[IDX]) * H5 / 12 * M5 if dates[i] >= M6 else 0) for i in range(N)]
Sv = [base_s[i] * (1 + ab_s[i]) * (1 + H6) + base_s[i] * H7 + hires_s[i] * M8 for i in range(N)]
TOT = [L[i] + T[i] + Sv[i] for i in range(N)]
row = lambda ws, r: [num(ws.cell(r, c).value) for c in COLS]
wb_rows = {"lift": row(P8, 41), "tray": row(P8, 62), "sup": row(P8, 79), "total": row(P8, 81)}
sc_rows = {"lift": row(pp7["Prod Payroll"], 41), "tray": row(pp7["Prod Payroll"], 62), "sup": row(pp7["Prod Payroll"], 79),
           "total": row(pp7["Prod Payroll"], 81)}
rep = {"lift": L, "tray": T, "sup": Sv, "total": TOT}
dmax_rep = max(abs(rep[k][i] - wb_rows[k][i]) for k in rep for i in range(N))
dmax_scr = max(abs(sc_rows[k][i] - wb_rows[k][i]) for k in rep for i in range(N))
fy = lambda x: sum(x[4:16])
tiers_wb = row(P8, 48); tiers_scr = row(pp7["Prod Payroll"], 48)
xl = []
f7x = openpyxl.load_workbook(V7)["Prod Payroll"]; f9x = openpyxl.load_workbook(V8)["Prod Payroll"]   # row 48 formulas: v7 (XLOOKUP) and v9 (= v8)
for c in range(16):
    cell = f"{openpyxl.utils.get_column_letter(c + 2)}48"
    old_f = f7x[cell].value; new_f = f9x[cell].value
    assert "xlookup" in str(old_f).lower() and str(new_f).startswith("=IF(MAX(")
    xl.append({"cell": cell, "old": old_f, "new": new_f, "x": max(C8, rate_t[c]), "v8": tiers_wb[c], "v7_scratch": tiers_scr[c],
               "replica": tier_t[c]})
assert all(x["v8"] == x["replica"] == x["v7_scratch"] for x in xl)
pp_tot = {k: num(P8.cell(r, 19).value) for k, r in (("lift", 41), ("tray", 62), ("sup", 79), ("total", 81))}
out["prodpay"] = {"S": pp_tot, "replica_fy27": {k: fy(v) for k, v in rep.items()}, "replica_sep_dec26": {k: sum(v[:4]) for k, v in rep.items()},
                  "max_diff_replica_vs_v8_monthly": dmax_rep, "max_diff_v7_scratch_vs_v8_monthly": dmax_scr,
                  "totals_diff_replica_vs_v8": {k: fy(rep[k]) - pp_tot[k] for k in rep},
                  "xlookup": xl, "errors_v8": sum(1 for r_ in P8.iter_rows() for c in r_ if isinstance(c.value, str) and c.value.startswith("#")),
                  "errors_v7": sum(1 for r_ in w7["Prod Payroll"].iter_rows() for c in r_ if isinstance(c.value, str) and c.value.startswith("#")),
                  "monthly": {k: v for k, v in rep.items()}, "months": MON,
                  "hc": {"lift": hc_l, "tray": hc_t, "sup": hc_s}}
assert dmax_rep < 1e-6 and all(abs(v) < 1 for v in out["prodpay"]["totals_diff_replica_vs_v8"].values())


# ------------------------------------------------------------------ 2. labour block replica (sections 8-11, v9 switches)
TAX = [Lp["tax"][i] + Tp["tax"][i] + base_s[i] * (1 + ab_s[i]) * H6 for i in range(N)]
BEN = [Lp["ben"][i] + Tp["ben"][i] + base_s[i] * H7 for i in range(N)]
tax_sh = [TAX[i] / TOT[i] if TOT[i] else 0.0 for i in range(N)]
ben_sh = [BEN[i] / TOT[i] if TOT[i] else 0.0 for i in range(N)]


def ds_in(a, w=w8):
    return num(w[DSN][a].value)


def labour(sw_cur, sw_q4, lag, delay, sw_idle=1):
    lift_life = ds_in("B9"); tray_life = ds_in("B10"); salvage = ds_in("B12")
    cur_l, _ = block([B9] * N, B5, B6, B7, ab_l, ot_l, [0] * N, 0)
    cur_t, _ = block([C9] * N, C5, C6, C7, ab_t, ot_t, [0] * N, 0)
    q = [sw_q4 if i < 4 else 1 for i in range(N)]                    # B132 applies to all of Sep-Dec 26 (v8 and v9 alike)
    xl_ = [(L[i] - (1 - sw_cur) * cur_l[i]) * q[i] for i in range(N)]
    xt_ = [(T[i] - (1 - sw_cur) * cur_t[i]) * q[i] for i in range(N)]
    xs_ = [Sv[i] * q[i] for i in range(N)]
    sl = [0 if xl_[i] + xt_[i] == 0 else xs_[i] * xl_[i] / (xl_[i] + xt_[i]) for i in range(N)]
    cap_l = [xl_[i] + sl[i] for i in range(N)]; cap_t = [xt_[i] + xs_[i] - sl[i] for i in range(N)]

    def pool(cap, b):
        P, W, E, carry = [], [], [], 0.0
        for i in range(N):
            if b[i] > 0:
                P.append(cap[i] + carry); E.append(0.0); carry = 0.0
            elif sw_idle:
                P.append(0.0); E.append(0.0); carry += cap[i]
            else:
                P.append(0.0); E.append(cap[i] + carry); carry = 0.0
            W.append(carry)
        return P, W, E
    pl, wl, el_ = pool(cap_l, built_l); pt, wt, et_ = pool(cap_t, built_t)
    per_l = [pl[i] / built_l[i] if built_l[i] else 0 for i in range(N)]; per_t = [pt[i] / built_t[i] if built_t[i] else 0 for i in range(N)]
    golive = [eom(dates[i], lag) for i in range(N)]
    yr = [d.year for d in golive]
    gl_l = [num(D8.cell(19, c).value) for c in range(6, 18)]; gl_t = [num(D8.cell(20, c).value) for c in range(6, 18)]
    vint = []
    dep_l = [0.0] * 12; dep_t = [0.0] * 12
    for g in range(1, 13):
        bi = 4 + g - 1 - lag
        vl = per_l[bi] * gl_l[g - 1]; vt = per_t[bi] * gl_t[g - 1]
        el = vl * (1 - salvage) / lift_life; et = vt * (1 - salvage) / tray_life
        for m in range(1, 13):
            if g + delay <= m < g + delay + lift_life: dep_l[m - 1] += el
            if g + delay <= m < g + delay + tray_life: dep_t[m - 1] += et
        vint.append({"golive": g, "build": MON[bi], "lifts": gl_l[g - 1], "trays": gl_t[g - 1], "per_lift": per_l[bi], "per_tray": per_t[bi],
                     "lab_lift": vl, "lab_tray": vt, "m_lift": el, "m_tray": et})
    # v9: builds of Sep-Dec 26 that go live in 2026 (Sep-26 -> Nov-26) are depreciated in 2027 from go-live + delay
    d26_l = [0.0] * 12; d26_t = [0.0] * 12
    for i in range(4):
        if yr[i] < 2027:
            g = (golive[i].year - 2027) * 12 + golive[i].month              # month number relative to Jan-27 = 1
            for m in range(1, 13):
                if g + delay <= m:
                    d26_l[m - 1] += pl[i] * (1 - salvage) / lift_life; d26_t[m - 1] += pt[i] * (1 - salvage) / tray_life
    dep_l = [dep_l[k] + d26_l[k] for k in range(12)]; dep_t = [dep_t[k] + d26_t[k] for k in range(12)]
    idle = [el_[i] + et_[i] for i in range(N)]
    res = {"cur_lift": cur_l, "cur_tray": cur_t, "cap_lift": cap_l, "cap_tray": cap_t, "cap_total": [cap_l[i] + cap_t[i] for i in range(N)],
           "sup_to_lift": sl, "pool_lift": pl, "pool_tray": pt, "wait_lift": wl, "wait_tray": wt, "per_lift": per_l, "per_tray": per_t,
           "golive_year": yr, "vint": vint, "dep_lift_m": dep_l, "dep_tray_m": dep_t, "dep26_lift_m": d26_l, "dep26_tray_m": d26_t,
           "dep_lift": sum(dep_l), "dep_tray": sum(dep_t), "dep": sum(dep_l) + sum(dep_t), "dep26": sum(d26_l) + sum(d26_t),
           "idle_m": idle, "idle_lift_m": el_, "idle_tray_m": et_, "idle_2027": sum(idle[4:]),
           "idle_gl_2027": {"5110": sum(idle[i] * (1 - tax_sh[i] - ben_sh[i]) for i in range(4, N)), "5130": sum(idle[i] * tax_sh[i] for i in range(4, N)),
                            "5140": sum(idle[i] * ben_sh[i] for i in range(4, N))},
           "cap_2027": sum(cap_l[4:]) + sum(cap_t[4:]), "cap_2026": sum(cap_l[:4]) + sum(cap_t[:4]),
           "to_2027": sum(pl[i] + pt[i] for i in range(4, N) if yr[i] == 2027), "to_2028": sum(pl[i] + pt[i] for i in range(4, N) if yr[i] > 2027),
           "waiting": wl[-1] + wt[-1],
           "from26_to_2027": sum(pl[i] + pt[i] for i in range(4) if yr[i] == 2027), "from26_to_2026": sum(pl[i] + pt[i] for i in range(4) if yr[i] < 2027),
           "vint_total": sum(v["lab_lift"] + v["lab_tray"] for v in vint), "cur_2027": sum(cur_l[4:]) + sum(cur_t[4:])}
    res["nbv_end27"] = res["vint_total"] - (res["dep"] - res["dep26"])
    res["capex_2027"] = res["cap_2027"] - res["idle_2027"]
    res["cip_end27"] = res["to_2028"] + res["waiting"]
    return res


SW = (ds_in(f"B{RM['sw_current']}"), ds_in(f"B{RM['sw_q4']}"), int(ds_in(f"B{RM['lag']}")), int(ds_in("B13")), ds_in(f"B{RM['sw_idle']}"))
assert SW == (1, 0, 2, 0, 1), SW
lab = labour(*SW)
cmp = []


def cmpr(r, vals, cols=COLS):
    for k, c in enumerate(cols):
        cmp.append(abs(num(S8.cell(r, c).value) - vals[k]))


cmpr(RM["cur_lift"], lab["cur_lift"]); cmpr(RM["cur_tray"], lab["cur_tray"])
cmpr(RM["cap_lift"], lab["cap_lift"]); cmpr(RM["cap_tray"], lab["cap_tray"]); cmpr(RM["sup_to_lift"], lab["sup_to_lift"])
cmpr(RM["pool_lift"], lab["pool_lift"]); cmpr(RM["pool_tray"], lab["pool_tray"])
cmpr(RM["wait_lift"], lab["wait_lift"]); cmpr(RM["wait_tray"], lab["wait_tray"])
cmpr(RM["per_lift"], lab["per_lift"]); cmpr(RM["per_tray"], lab["per_tray"])
cmpr(RM["out_lift"], lab["dep_lift_m"], range(6, 18)); cmpr(RM["out_tray"], lab["dep_tray_m"], range(6, 18))
cmpr(RM["idle_lift"], lab["idle_lift_m"]); cmpr(RM["idle_tray"], lab["idle_tray_m"])
cmpr(RM["tax_share"], tax_sh); cmpr(RM["ben_share"], ben_sh)
cmpr(RM["dep26_lift"], lab["dep26_lift_m"], range(6, 18)); cmpr(RM["dep26_tray"], lab["dep26_tray_m"], range(6, 18))
for k, v in enumerate(lab["vint"]):
    cmp.append(abs(num(S8.cell(RM["vint_lift"][k], 4).value) - v["lab_lift"])); cmp.append(abs(num(S8.cell(RM["vint_tray"][k], 4).value) - v["lab_tray"]))
memo = {k[2:]: num(S8.cell(r, 2).value) for k, r in RM.items() if k.startswith("m_")}
for k in ("cap_2027", "to_2027", "to_2028", "waiting", "cap_2026", "from26_to_2027", "from26_to_2026", "vint_total", "nbv_end27", "cur_2027"):
    cmp.append(abs(memo[k] - lab[k]))
for k, lk in (("capex_2027", "capex_2027"), ("bs_cip", "cip_end27"), ("bs_in_service", "nbv_end27"), ("idle_2027", "idle_2027"), ("dep26_2027", "dep26")):
    cmp.append(abs(memo[k] - lab[lk]))
cmp.append(abs(memo["dep_2027"] - lab["dep"]))
out["labour_replica_max_diff"] = max(cmp)
assert out["labour_replica_max_diff"] < 1e-6, out["labour_replica_max_diff"]
for k in ("chk_2027", "chk_vint"):
    assert abs(memo[k]) < 1e-6
assert abs(num(S8.cell(RM["out_check"], 18).value)) < 1e-6 and abs(num(S8.cell(RM["lag_check"], 2).value)) < 1e-9
assert abs(num(S8.cell(RM["idle_check"], 18).value)) < 1e-6
out["labour"] = {k: v for k, v in lab.items()}
out["memo"] = memo
out["rowmap"] = RM
out["shares"] = {"tax": tax_sh, "ben": ben_sh}

# ------------------------------------------------------------------ 3. budget effects (v7 -> v8 -> v9)
ag = lambda w, s, r: num(w[s].cell(r, 33).value)
CON7 = ag(w7, "COO P&L", 132); CONP = ag(wprev, "COO P&L", 132); CON9 = ag(w8, "COO P&L", 132)
lab8 = labour(1, 1, 2, 0)                                           # v8 switches; v8's block had no Sep-26 depreciation term
DEP8 = num(wprev[DSN].cell(RM["out_total"], 18).value)
assert abs(lab8["dep"] - lab8["dep26"] - DEP8) < 1e-6, "replica does not reproduce v8"
eff = {"C7": CON7, "C8": CONP, "C9": CON9, "delta_v8": CON9 - CONP, "delta_v7": CON9 - CON7, "dep_v8": DEP8,
       "po_5100_v7": ag(w7, "PO", 36), "po_5100_v8": ag(wprev, "PO", 36), "po_5100_v9": ag(w8, "PO", 36),
       "gl": {gl: {"v7": ag(w7, "PO", r), "v8": ag(wprev, "PO", r), "v9": ag(w8, "PO", r)} for gl, r in (("5010", 19), ("5011", 20), ("5012", 21), ("5020", 22))},
       "po_rows_5100": {gl: {"v7": ag(w7, "PO", r), "v8": ag(wprev, "PO", r), "v9": ag(w8, "PO", r)} for gl, r in (("5110", 33), ("5130", 34), ("5140", 35))},
       "dep_total_v7": sum(ag(w7, "COO P&L", r) for r in (19, 20, 21, 22)), "dep_total_v8": sum(ag(wprev, "COO P&L", r) for r in (19, 20, 21, 22)),
       "dep_total_v9": sum(ag(w8, "COO P&L", r) for r in (19, 20, 21, 22)),
       "cogs_v7": ag(w7, "COO P&L", 63), "cogs_v8": ag(wprev, "COO P&L", 63), "cogs_v9": ag(w8, "COO P&L", 63), "opex_v9": ag(w8, "COO P&L", 116),
       "rev": ag(w8, "COO P&L", 16), "n132": num(w8["COO P&L"]["N132"].value)}
assert abs(eff["delta_v8"] - (DEP8 - lab["dep"])) < 1e-6, "v8 -> v9 change is not the Oct-Dec 26 labour depreciation"
assert abs(eff["delta_v7"] - (eff["po_5100_v7"] - lab["dep"])) < 1e-6
for gl in ("5010", "5020"):
    assert eff["gl"][gl]["v7"] == eff["gl"][gl]["v8"] == eff["gl"][gl]["v9"]
assert abs(eff["gl"]["5011"]["v9"] - eff["gl"]["5011"]["v7"] - lab["dep_lift"]) < 1e-6 and abs(eff["gl"]["5012"]["v9"] - eff["gl"]["5012"]["v7"] - lab["dep_tray"]) < 1e-6
assert eff["po_5100_v9"] == 0
out["effects"] = eff

# ------------------------------------------------------------------ 4. hand recompute: Jun-27 (month 6)
M_ = 6
rows_h = []
for v in lab["vint"]:
    if v["golive"] <= M_ and (v["lab_lift"] or v["lab_tray"]):
        rows_h.append({"vintage": f"{['Jan','Feb','Mar','Apr','May','Jun'][v['golive'] - 1]}-27", "build": v["build"], "lifts": v["lifts"],
                       "per_lift": v["per_lift"], "lift_month": v["per_lift"] * v["lifts"] / ds_in("B9"),
                       "trays": v["trays"], "per_tray": v["per_tray"], "tray_month": v["per_tray"] * v["trays"] / ds_in("B10")})
hand_l = sum(x["lift_month"] for x in rows_h); hand_t = sum(x["tray_month"] for x in rows_h)
po_l = num(w8["PO"]["Z20"].value) - num(w7["PO"]["Z20"].value); po_t = num(w8["PO"]["Z21"].value) - num(w7["PO"]["Z21"].value)
out["hand"] = {"month": "Jun-27", "rows": rows_h, "hand_lift": hand_l, "hand_tray": hand_t, "po_z20_delta": po_l, "po_z21_delta": po_t,
               "ds_k193": num(S8.cell(RM["out_lift"], 11).value), "ds_k194": num(S8.cell(RM["out_tray"], 11).value),
               "v8_k193": num(wprev[DSN].cell(RM["out_lift"], 11).value), "v8_k194": num(wprev[DSN].cell(RM["out_tray"], 11).value),
               "diff": max(abs(hand_l - po_l), abs(hand_t - po_t))}
assert out["hand"]["diff"] < 1e-6

# ------------------------------------------------------------------ 5. scenarios (LibreOffice recalculation of v9 scratch copies)
scen = {}
REPL = {"cur": (0, 0, 2, 0, 1), "q4": (1, 1, 2, 0, 1), "b13": (1, 0, 2, 1, 1), "idle": (1, 0, 2, 0, 0), "idlecur": (0, 0, 2, 0, 0), "q4cur": (0, 1, 2, 0, 1)}
for k, w in sc.items():
    D = w[DSN]
    scen[k] = {"C": ag(w, "COO P&L", 132), "dep_lab": num(D.cell(RM["out_total"], 18).value), "po_5100": ag(w, "PO", 36),
               "po_rows": [ag(w, "PO", r) for r in (33, 34, 35)],
               "dep_total": sum(ag(w, "COO P&L", r) for r in (19, 20, 21, 22)), "to_2028": num(D.cell(RM["m_to_2028"], 2).value),
               "cap_2027": num(D.cell(RM["m_cap_2027"], 2).value), "vint_total": num(D.cell(RM["m_vint_total"], 2).value),
               "capex_2027": num(D.cell(RM["m_capex_2027"], 2).value), "bs_in_service": num(D.cell(RM["m_bs_in_service"], 2).value),
               "bs_cip": num(D.cell(RM["m_bs_cip"], 2).value), "idle_2027": num(D.cell(RM["m_idle_2027"], 2).value),
               "dep26": num(D.cell(RM["m_dep26_2027"], 2).value), "cap_2026": num(D.cell(RM["m_cap_2026"], 2).value),
               "checks": [num(D.cell(RM["out_check"], 18).value), num(D.cell(RM["m_chk_2027"], 2).value), num(D.cell(RM["idle_check"], 18).value),
                          num(D.cell(RM["m_chk_vint"], 2).value)]}
    scen[k]["effect"] = scen[k]["C"] - CON9
    r_ = labour(*REPL[k])
    scen[k]["replica"] = {kk: r_[kk] for kk in ("dep", "dep_lift", "dep_tray", "dep26", "cap_2027", "to_2027", "to_2028", "from26_to_2027", "from26_to_2026",
                                                "vint_total", "nbv_end27", "idle_2027", "capex_2027", "cip_end27")}
    scen[k]["replica"]["idle_gl_2027"] = r_["idle_gl_2027"]
    assert abs(scen[k]["dep_lab"] - r_["dep"]) < 1e-6, (k, scen[k]["dep_lab"], r_["dep"])
    assert abs(scen[k]["idle_2027"] - r_["idle_2027"]) < 1e-6 and abs(scen[k]["capex_2027"] - r_["capex_2027"]) < 1e-6, k
    assert abs(scen[k]["bs_in_service"] - r_["nbv_end27"]) < 1e-6 and abs(scen[k]["bs_cip"] - r_["cip_end27"]) < 1e-6, k
    assert max(abs(x) for x in scen[k]["checks"]) < 1e-6, (k, scen[k]["checks"])
    po_exp = (eff["po_5100_v7"] if REPL[k][0] == 0 else 0.0) + r_["idle_2027"]
    assert abs(scen[k]["po_5100"] - po_exp) < 1e-6, (k, scen[k]["po_5100"], po_exp)
    # contribution moves only by the labour depreciation and PO 5110-5140
    assert abs(scen[k]["effect"] - (lab["dep"] - r_["dep"] - po_exp)) < 1e-6 or k == "b13", k
# idle: the expensed amount lands on 5110 / 5130 / 5140 in the split of section 11
for gl, i in (("5110", 0), ("5130", 1), ("5140", 2)):
    assert abs(scen["idle"]["po_rows"][i] - scen["idle"]["replica"]["idle_gl_2027"][gl]) < 1e-6
# the critic's B1 point: v8's B132 = 1 equals v9's B132 = 1 less the Sep-26 builds' depreciation (now inside the switch)
assert abs(scen["q4"]["dep_lab"] - scen["q4"]["dep26"] - DEP8) < 1e-6
r_b13 = labour(1, 0, 2, 1)
scen["b13"]["labour_part"] = lab["dep"] - r_b13["dep"]
scen["b13"]["mid_month"] = scen["b13"]["effect"] / 2
# idle effect, decomposed: Jan-27 labour expensed less the 2027 depreciation it would have carried in the Feb-27 builds
for k, base in (("idle", lab), ("idlecur", labour(0, 0, 2, 0))):
    scen[k]["expensed"] = scen[k]["idle_2027"]
    scen[k]["dep_saved"] = base["dep"] - scen[k]["dep_lab"]
    scen[k]["effect_vs_base"] = -scen[k]["expensed"] + scen[k]["dep_saved"]
assert abs(scen["idle"]["effect_vs_base"] - scen["idle"]["effect"]) < 1e-6
assert abs(scen["idlecur"]["effect_vs_base"] - (scen["idlecur"]["C"] - scen["cur"]["C"])) < 1e-6
idle_months = [MON[i] for i in range(N) if built_l[i] == 0 or built_t[i] == 0]
scen["idle"]["months_no_builds"] = idle_months
out["scen"] = scen

# ------------------------------------------------------------------ 6. v7 method reproduced and the bridge to v9
cur_l, cur_t = lab["cur_lift"], lab["cur_tray"]
units27 = {"lift": sum(built_l[4:]), "tray": sum(built_t[4:])}
golive_l = [num(D8.cell(19, c).value) for c in range(6, 18)]; golive_t = [num(D8.cell(20, c).value) for c in range(6, 18)]


def v7_method(lift, tray, sup):
    sh = lift / (lift + tray)
    al = {"lift": lift + sup * sh, "tray": tray + sup * (1 - sh)}
    pl_, pt_ = al["lift"] / units27["lift"], al["tray"] / units27["tray"]
    d = 0.0
    for g in range(1, 13):
        if g - 2 >= 1:
            mo = 12 - g + 1
            d += pl_ * golive_l[g - 1] / ds_in("B9") * mo + pt_ * golive_t[g - 1] / ds_in("B10") * mo
    return d, pl_, pt_


ramp = (fy(L) - sum(cur_l[4:]), fy(T) - sum(cur_t[4:]), fy(Sv))
d_v7_ramp, _, _ = v7_method(*ramp)
assert abs(d_v7_ramp - F7["b1_cap"]["d9"]["dep"]) < 0.01, (d_v7_ramp, F7["b1_cap"]["d9"]["dep"])
d_v7_full, pl_full, pt_full = v7_method(fy(L), fy(T), fy(Sv))
out["bridge"] = {"v7_ramp_annual_avg": d_v7_ramp, "v7_method_full_model": d_v7_full, "monthly_booked": lab["dep"], "v8_booked": DEP8,
                 "step_full_model": d_v7_full - d_v7_ramp, "step_monthly_pooling": lab["dep"] - d_v7_full,
                 "alt_q4_all": scen["q4"]["dep_lab"], "step_q4_all": scen["q4"]["dep_lab"] - lab["dep"], "step_q4_v8": DEP8 - lab["dep"],
                 "step_sep26": scen["q4"]["dep26"],
                 "sens_monthly": scen["cur"]["dep_lab"], "sens_v7_method": d_v7_ramp, "sens_step": scen["cur"]["dep_lab"] - d_v7_ramp}

# ------------------------------------------------------------------ 7. exposures
hp = w8["HC-PO"]
t_po, b_po = num(hp["D6"].value), num(hp["D7"].value)
mh = [r for r in range(14, 58) if isinstance(hp.cell(r, 3).value, str) and "material handl" in hp.cell(r, 3).value.lower()]
assert len(mh) == 2, mh
mh_cost = sum(num(hp.cell(r, 26).value) for r in mh) * (1 + t_po + b_po)
assert abs(num(hp["Z67"].value) * (1 + t_po + b_po) - num(hp["Z70"].value)) < 0.01
b2 = F7["b2"]; o1 = F7["o1"]; o6 = F7["o6"]
I17 = F7["I17"]
ratio_27 = lab["dep"] / lab["cap_2027"]                              # booked: 2027 depreciation per $ of 2027 payroll capitalised
ratio_27_sens = scen["cur"]["dep_lab"] / scen["cur"]["cap_2027"]    # under B131 = 0
rate_gap = eff["po_5100_v7"] - lab["cur_2027"]                       # O7: current 9 at PO HC rates less at model rates
out["exposures"] = {
    "sens_current_expensed": scen["cur"]["effect"],
    "q4_all_capitalised": scen["q4"]["effect"], "q4cur": scen["q4cur"]["effect"],
    "idle": scen["idle"]["effect"], "idle_sens": scen["idlecur"]["C"] - scen["cur"]["C"], "C_idlecur": scen["idlecur"]["C"],
    "mh_roles_rows": mh, "mh_roles_cost": mh_cost, "mh01_cost": b2["mh01_cost"],
    "i17": I17, "i17_9dedup": I17 + b2["mh01_cost"], "i17_7_with_mh": I17 + mh_cost,
    "o1_burden_diff": o1["diff"], "o1_dep_pro_rata": o1["diff"] * ratio_27, "ratio_dep_per_2027_payroll": ratio_27,
    "o1_dep_pro_rata_sens": o1["diff"] * ratio_27_sens, "ratio_dep_per_2027_payroll_sens": ratio_27_sens,
    "labour_in_unit_cost": lab["dep"],
    "rate_gap": rate_gap, "rate_gap_dep": rate_gap * ratio_27,
    "sep26_labour_v8": lab8["from26_to_2026"], "sep26_dep_if_capitalised": scen["q4"]["dep26"],
    "i37_co_pe": o6["depts"]["CO"]["gap_at_fica_on_hc_salary"] + o6["depts"]["PE"]["gap_at_fica_on_hc_salary"],
    "i37_po_part_v7": o6["depts"]["PO"]["gap_at_fica_on_hc_salary"],
    "a14_start_after": scen["b13"]["effect"], "a14_mid": scen["b13"]["mid_month"], "a14_labour_part": scen["b13"]["labour_part"],
    "expensed_policy_C": CON7 - F7["I05"], "policy_effect": CON9 - (CON7 - F7["I05"]),
}
cv7 = [s for s in cn7["sections"] if s["heading"].startswith("Caveats on the headline")][0]
for r_ in cv7["table"]["rows"]:
    if isinstance(r_[3], (int, float)):
        assert abs(r_[4] - (CON7 + r_[3])) < 0.011, r_[0]
out["carried_v7_rows"] = cv7["table"]["rows"]
out["v8_q4_26"] = {"oct_dec26_labour": lab8["from26_to_2027"], "dep": DEP8, "q4_hires": None}
out["evidence_check"] = {"S81": pp_tot["total"], "S41": pp_tot["lift"], "S62": pp_tot["tray"], "S79": pp_tot["sup"],
                         "current_9": lab["cur_2027"], "po_5100_v7": eff["po_5100_v7"], "builds_2027": units27,
                         "live_2027_built_2027": {"lift": sum(golive_l[2:]), "tray": sum(golive_t[2:])}, "contribution_v7": CON7,
                         "contribution_v8": CONP, "v7_dep_9": F7["b1_cap"]["d9"]["dep"]}
json.dump(out, open(OUT, "w"), indent=1, default=str)
print(f"figures_v9: contribution v8 {CONP:,.2f} -> v9 {CON9:,.2f} ({CON9 - CONP:+,.2f}); labour dep {lab['dep']:,.2f} (5011 {lab['dep_lift']:,.2f}, 5012 "
      f"{lab['dep_tray']:,.2f}); replica max diff {out['labour_replica_max_diff']:.1e}; CapEx 2027 {lab['capex_2027']:,.2f}; Dec-27 in service "
      f"{lab['nbv_end27']:,.2f}, CIP {lab['cip_end27']:,.2f}; sensitivity {scen['cur']['C']:,.2f}; B132=1 {scen['q4']['effect']:+,.2f}; idle "
      f"{scen['idle']['effect']:+,.2f} (under B131=0 {out['exposures']['idle_sens']:+,.2f}); hand Jun-27 diff {out['hand']['diff']:.1e}")
