"""v6 payroll reconciliation: HC rosters (COO HC & PL workfile) vs P&L payroll lines vs SD payroll models.

Usage:
  python3 -I recon_v6.py WORKFILE SD_BOOK COO_BOOK V5_XLSX PP_RECALC_XLSX OUT_JSON OUT_CSV

  WORKFILE        COO_HC_and_PL_workfile.xlsx (HC tabs FO/PO/CO/FE/PE HC; cached values)
  SD_BOOK         Service_Delivery_PL_worksheets.xlsx (Logistics&WH Payroll, not carried into the workbook)
  COO_BOOK        COO_Dept_PLs_2027_Budget_2.xlsx (old FO/FE payroll lines)
  V5_XLSX         v5 workbook (P&L tabs, Fld Ops Payroll, Fld Eng Budget, Prod Payroll inputs)
  PP_RECALC_XLSX  LibreOffice recalculation of the prodpay_v6.py scratch copy (Prod Payroll tray/supervisor rows)

PRIVACY: employee names are read only to match people across rosters, inside this process. Nothing written to
OUT_JSON or OUT_CSV contains a name: people are identified as '<tab> r<row> <title>'. The script stops if any roster
name token appears in its own output.
Every figure is computed here from cell values; nothing is typed.
"""
import sys, json, re, csv, datetime, io, collections
import openpyxl

WF, SD, COO, V5, PPR, OUT_JSON, OUT_CSV = sys.argv[1:8]
wf = openpyxl.load_workbook(WF, data_only=True)
sd = openpyxl.load_workbook(SD, data_only=True)
coo = openpyxl.load_workbook(COO, data_only=True)
v5 = openpyxl.load_workbook(V5, data_only=True)
ppr = openpyxl.load_workbook(PPR, data_only=True)

DEPTS = ["FO", "PO", "CO", "FE", "PE"]
M27 = list(range(13, 25))          # HC tabs: M..X = Jan..Dec 27
P27 = list(range(21, 33))          # P&L tabs: U..AF = Jan..Dec 27
S27 = list(range(6, 18))           # SD models: F..Q = Jan..Dec 27
SDALL = list(range(2, 18))         # SD models: B..Q = Sep-26..Dec-27
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
NAMES = set()                      # every name token seen (for the self-check)
FULL = set()                       # every full name seen (scratch file for privacy_v6.py; never in the deliverables)
EPS = 1e-6


def num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0


def d2(v):
    if isinstance(v, datetime.datetime):
        return v.date()
    return v


def ym(d):
    return d.strftime("%b-%y") if d else ""


def toks(name):
    return [t for t in re.split(r"[^a-z]+", (name or "").lower()) if t]


def name_match(a, b):
    """Same person by name: every token of the shorter name is in the longer one (handles first-name-only labels)."""
    ta, tb = toks(a), toks(b)
    if not ta or not tb:
        return False
    s, l = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    return all(t in l for t in s) and s[0] == l[0]


def tnorm(t):
    t = (t or "").lower().replace("engineering", "engineer")
    return re.sub(r"[^a-z]+", " ", t).strip()


# ------------------------------------------------------------------ 1. HC rosters
PLACEHOLDER = {"backfill", "tbd", "open", "new hire", "vacant"}


def section(r):
    return "current" if 14 <= r <= 33 else "open" if 35 <= r <= 39 else "new hire" if 41 <= r <= 50 else \
        "transfer in" if 52 <= r <= 57 else None


hc = {}
people = []
for d in DEPTS:
    ws = wf[f"{d} HC"]
    rows = []
    for r in range(14, 58):
        sec = section(r)
        if not sec:
            continue
        nm, title, sal = ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value
        if not title and not isinstance(sal, (int, float)):
            continue
        nm = nm.strip() if isinstance(nm, str) else None
        if nm and nm.lower() in PLACEHOLDER:
            nm = None
        if nm:
            NAMES.update(t for t in toks(nm) if len(t) > 1); FULL.add(nm)
        m27 = [num(ws.cell(r, c).value) for c in M27]
        allm = [num(ws.cell(r, c).value) for c in range(9, 25)]
        p = {"id": f"{d} HC r{r} {title}", "roster": f"{d} HC", "dept": d, "row": r, "section": sec,
             "title": title, "salary": sal if isinstance(sal, (int, float)) else None,
             "start": ym(d2(ws.cell(r, 5).value)) if ws.cell(r, 5).value else "",
             "end": ym(d2(ws.cell(r, 6).value)) if ws.cell(r, 6).value else "",
             "flag_col_a": ws.cell(r, 1).value if isinstance(ws.cell(r, 1).value, str) and ws.cell(r, 1).value.strip() else "",
             "sal_2027": sum(m27), "z": num(ws.cell(r, 26).value), "m27": m27,
             "hc_months_2027": sum(1 for x in m27 if x > 0), "hc_dec26": 1 if allm[3] > 0 else 0, "_name": nm}
        assert abs(p["sal_2027"] - p["z"]) < EPS, p["id"]
        rows.append(p); people.append(p)
    tot = {k: [num(ws.cell(rr, c).value) for c in M27] for k, rr in (("sal", 67), ("tax", 68), ("ben", 69), ("tot", 70))}
    z = {k: num(ws.cell(rr, 26).value) for k, rr in (("sal", 67), ("tax", 68), ("ben", 69), ("tot", 70))}
    rate_t, rate_b = num(ws["D6"].value), num(ws["D7"].value)
    assert abs(sum(p["sal_2027"] for p in rows) - z["sal"]) < 1e-4, d
    assert abs(z["tax"] - z["sal"] * rate_t) < 1e-4 and abs(z["ben"] - z["sal"] * rate_b) < 1e-4, d
    hc[d] = {"rate_tax": rate_t, "rate_ben": rate_b, "z": z, "monthly": tot,
             "n_people": sum(1 for p in rows if p["salary"]), "n_open_no_salary": sum(1 for p in rows if not p["salary"]),
             "hc_by_month_2027": [sum(1 for p in rows if p["m27"][i] > 0) for i in range(12)],
             "flags": [p["id"] + f" (col A '{p['flag_col_a']}')" for p in rows if p["flag_col_a"]],
             "titles": dict(collections.Counter(p["title"] for p in rows if p["salary"])),
             "sections": dict(collections.Counter(p["section"] for p in rows if p["salary"]))}

# ------------------------------------------------------------------ 2. HC vs P&L payroll lines (v5 and COO book _2)
PL_ROWS = {"FO": (52, 53, 54), "PO": (33, 34, 35), "CO": (67, 68, 69), "FE": (67, 68, 69), "PE": (67, 68, 69)}
tie = {}
for d in DEPTS:
    rs = PL_ROWS[d]
    out = {}
    for lab, book in (("v5", v5), ("coo_book", coo)):
        ws = book[d]
        vals = {k: [num(ws.cell(r, c).value) for c in P27] for k, r in zip(("sal", "tax", "ben"), rs)}
        out[lab] = {k: sum(v) for k, v in vals.items()}
        out[lab]["max_monthly_diff_vs_hc"] = max(abs(a - b) for k in ("sal", "tax", "ben")
                                                for a, b in zip(vals[k], hc[d]["monthly"][k]))
        out[lab]["ag_check"] = max(abs(num(ws.cell(r, 33).value) - sum(vals[k])) for k, r in zip(("sal", "tax", "ben"), rs))
    out["gl"] = [v5[d].cell(r, 1).value.split(" - ")[0] for r in rs]
    tie[d] = out

# ------------------------------------------------------------------ 3. FO: Fld Ops Payroll current vs ramp
fop = v5["Fld Ops Payroll"]


def row(ws, r, cols=S27):
    return [num(ws.cell(r, c).value) for c in cols]


FO_GL = {"5510": [21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77], "5530": [22, 32, 44, 57, 70, 78],
         "5540": [23, 33, 45, 58, 71, 79]}
fo_check = 0.0
for gl, rr in FO_GL.items():
    plr = {"5510": 52, "5530": 53, "5540": 54}[gl]
    pl = row(v5["FO"], plr, P27)
    sm = [sum(row(fop, r)[i] for r in rr) for i in range(12)]
    fo_check = max(fo_check, max(abs(a - b) for a, b in zip(pl, sm)))
assert fo_check < 1e-6, fo_check
blocks = {
    "current_techs": {"sal": [21], "nh": [], "tax": [22], "ben": [23], "hc": 20},
    "current_named": {"sal": [76, 77], "nh": [], "tax": [78], "ben": [79], "hc": None},
    "ramp_new_logo_techs": {"sal": [31], "nh": [34], "tax": [32], "ben": [33], "hc": 30},
    "ramp_expansion_techs": {"sal": [43], "nh": [46], "tax": [44], "ben": [45], "hc": 41},
    "ramp_floaters": {"sal": [56], "nh": [59], "tax": [57], "ben": [58], "hc": 54},
    "ramp_supervisors": {"sal": [69], "nh": [72], "tax": [70], "ben": [71], "hc": 66},
}
fo = {"blocks": {}}
for k, b in blocks.items():
    e = {x: sum(sum(row(fop, r)) for r in b[x]) for x in ("sal", "nh", "tax", "ben")}
    e["total"] = e["sal"] + e["nh"] + e["tax"] + e["ben"]
    if b["hc"]:
        e["hc_by_month"] = row(fop, b["hc"])
    else:
        e["hc_by_month"] = [sum(1 for r in (76, 77) if num(fop.cell(r, c).value) > 0) for c in S27]
    fo["blocks"][k] = e
tot_fo = sum(e["total"] for e in fo["blocks"].values())
assert abs(tot_fo - sum(row(fop, 82))) < 1e-4
fo["total"] = tot_fo
fo["pl_5510_5540"] = {gl: sum(row(v5["FO"], r, P27)) for gl, r in (("5510", 52), ("5530", 53), ("5540", 54))}
cur = [fo["blocks"]["current_techs"], fo["blocks"]["current_named"]]
ramp = [fo["blocks"][k] for k in blocks if k.startswith("ramp")]
fo["current"] = {x: sum(e[x] for e in cur) for x in ("sal", "nh", "tax", "ben", "total")}
fo["ramp"] = {x: sum(e[x] for e in ramp) for x in ("sal", "nh", "tax", "ben", "total")}
fo["current_hc_by_month"] = [sum(e["hc_by_month"][i] for e in cur) for i in range(12)]
fo["ramp_hc_by_month"] = [sum(e["hc_by_month"][i] for e in ramp) for i in range(12)]
fo["inputs"] = {"techs_B11": num(fop["B11"].value), "avg_tech_salary_B6": num(fop["B6"].value),
                "tax_B7": num(fop["B7"].value), "ben_B8": num(fop["B8"].value),
                "coord_H15": num(fop["H15"].value), "mgr_H16": num(fop["H16"].value),
                "sup_tax_H6": num(fop["H6"].value), "sup_ben_H7": num(fop["H7"].value)}
# match the FO HC roster to the model's current staff
fohc = [p for p in people if p["roster"] == "FO HC" and p["salary"]]
techs = [p for p in fohc if tnorm(p["title"]) == "field technician"]
named_lbl = {"coord": fop["E15"].value, "mgr": fop["E16"].value}
fo_match = []
for key, lbl, sal_cell, sd_row in (("coord", named_lbl["coord"], "H15", 76), ("mgr", named_lbl["mgr"], "H16", 77)):
    nm = lbl.split("–")[0].split(" - ")[0].strip()
    NAMES.update(t for t in toks(nm) if len(t) > 1)
    hits = [p for p in fohc if name_match(nm, p["_name"])]
    assert len(hits) == 1, (key, len(hits))
    p = hits[0]
    sd_sal = sum(row(fop, sd_row))
    fo_match.append({"hc": p["id"], "sd": f"Fld Ops Payroll row {sd_row} ({'Operations Coordinator' if key == 'coord' else 'Manager'})",
                     "basis": "name + salary", "hc_salary": p["salary"], "sd_salary": num(fop[sal_cell].value),
                     "hc_2027": p["sal_2027"], "sd_2027": sd_sal, "diff_2027": sd_sal - p["sal_2027"]})
    p["_mapped"] = f"FO 5510-5540 via Fld Ops Payroll row {sd_row}"
for p in techs:
    p["_mapped"] = "FO 5510-5540 via Fld Ops Payroll rows 20-24 (14 current techs, by count; model uses an average salary)"
other_fo = [p for p in fohc if "_mapped" not in p]
fo["match"] = {"named": fo_match, "techs_hc": len(techs), "techs_model": num(fop["B11"].value),
               "techs_hc_salary": sum(p["salary"] for p in techs), "techs_model_salary": num(fop["B11"].value) * num(fop["B6"].value),
               "techs_hc_2027": sum(p["sal_2027"] for p in techs), "techs_model_2027": fo["blocks"]["current_techs"]["sal"],
               "unmapped": [p["id"] for p in other_fo], "fo_hc_people": len(fohc)}
fo["current_vs_hc"] = {"model_sal": fo["current"]["sal"], "hc_sal": hc["FO"]["z"]["sal"],
                       "diff_sal": fo["current"]["sal"] - hc["FO"]["z"]["sal"],
                       "model_tax_ben": fo["current"]["tax"] + fo["current"]["ben"],
                       "hc_tax_ben": hc["FO"]["z"]["tax"] + hc["FO"]["z"]["ben"],
                       "coo_book_5510": tie["FO"]["coo_book"]["sal"], "coo_book_total": sum(tie["FO"]["coo_book"][k] for k in ("sal", "tax", "ben"))}

# ------------------------------------------------------------------ 4a. PO: Prod Payroll model (replica + LO check)
ppv = v5["Prod Payroll"]
pp_lo = ppr["Prod Payroll"]


def cv(c):
    return num(ppv[c].value)


I = {k: cv(k) for k in ("B5", "C5", "B6", "C6", "B7", "C7", "B8", "C8", "B9", "C9", "H5", "H6", "H7", "H8", "H9", "H10",
                         "M5", "M7", "M8", "M9", "M10")}
M6 = d2(ppv["M6"].value)
dates = [d2(ppv.cell(24, c).value) for c in SDALL]
lift_tiers = [num(ppv.cell(15, c).value) for c in range(2, 16)]
lift_emp = [num(ppv.cell(17, c).value) for c in range(2, 16)]
tray_tiers = [num(ppv.cell(20, c).value) for c in range(2, 16)]
tray_emp = [num(ppv.cell(22, c).value) for c in range(2, 16)]
lifts_wk = [num(ppv.cell(26, c).value) for c in SDALL]
trays_wk = [num(ppv.cell(47, c).value) for c in SDALL]
abs_l = [num(ppv.cell(33, c).value) for c in SDALL]
ot_l = [num(ppv.cell(35, c).value) for c in SDALL]
abs_t = [num(ppv.cell(54, c).value) for c in SDALL]
ot_t = [num(ppv.cell(56, c).value) for c in SDALL]
abs_s = [num(ppv.cell(73, c).value) for c in SDALL]
import math


def eomonth(d, k):
    y, m = d.year, d.month + k
    while m > 12: y, m = y + 1, m - 12
    while m < 1: y, m = y - 1, m + 12
    nxt = datetime.date(y + (m == 12), m % 12 + 1, 1)
    return nxt - datetime.timedelta(days=1)


ref = eomonth(M6, -int(I["M9"]) - 1)
ref_i = dates.index(ref) if ref in dates else 0


def salaries(hcs, annual):
    out = []
    for i, h in enumerate(hcs):
        s = h * annual / 12
        if dates[i] >= M6:
            s += min(h, hcs[ref_i]) * annual / 12 * I["M5"]
        out.append(s)
    return out


def hires(inc):
    return [inc[0]] + [max(0, inc[i] - inc[i - 1]) for i in range(1, len(inc))]


def lift_model(current_only=False):
    if current_only:
        tot = [I["B9"]] * 16; inc = [0] * 16
    else:
        req = []
        for i, x in enumerate(lifts_wk):
            tier = min(max(I["B8"], math.ceil(x - 1e-12)), max(lift_tiers))
            v = lift_emp[lift_tiers.index(tier)]
            req.append(v if i == 0 else max(req[-1], v))
        inc = [max(0, r - I["B9"]) for r in req]; tot = [I["B9"] + x for x in inc]
    sal = salaries(tot, I["B5"])
    ab = [s * f for s, f in zip(sal, abs_l)]
    ot = [s * f * I["M10"] for s, f in zip(sal, ot_l)]
    tax = [(s + a + o) * I["B6"] for s, a, o in zip(sal, ab, ot)]
    ben = [s * I["B7"] for s in sal]
    nh = [h * I["M7"] for h in hires(inc)]
    return {"hc": tot, "sal": sal, "abs": ab, "ot": ot, "tax": tax, "ben": ben, "nh": nh,
            "total": [sum(x) for x in zip(sal, ab, ot, tax, ben, nh)]}


def tray_model(current_only=False):
    if current_only:
        tot = [I["C9"]] * 16; inc = [0] * 16
    else:
        req = []
        for i, x in enumerate(trays_wk):
            xx = max(I["C8"], x)
            tier = max(tray_tiers) if xx > max(tray_tiers) else min(t for t in tray_tiers if t >= xx)
            v = tray_emp[tray_tiers.index(tier)]
            req.append(v if i == 0 else max(req[-1], v))
        inc = [max(0, r - I["C9"]) for r in req]; tot = [I["C9"] + x for x in inc]
    sal = salaries(tot, I["C5"])
    ab = [s * f for s, f in zip(sal, abs_t)]
    ot = [s * f * I["M10"] for s, f in zip(sal, ot_t)]
    tax = [(s + a + o) * I["C6"] for s, a, o in zip(sal, ab, ot)]
    ben = [s * I["C7"] for s in sal]
    nh = [h * I["M7"] for h in hires(inc)]
    return {"hc": tot, "sal": sal, "abs": ab, "ot": ot, "tax": tax, "ben": ben, "nh": nh,
            "total": [sum(x) for x in zip(sal, ab, ot, tax, ben, nh)]}


def sup_model(lift, tray, current_only=False):
    if current_only:
        tot = [I["H10"]] * 16; inc = [0] * 16
    else:
        req = []
        for i, (a, b) in enumerate(zip(lift["hc"], tray["hc"])):
            v = max(I["H9"], math.ceil((a + b) / I["H8"] - 1e-12))
            req.append(v if i == 0 else max(req[-1], v))
        inc = [max(0, r - I["H10"]) for r in req]; tot = [I["H10"] + x for x in inc]
    sal = salaries(tot, I["H5"])
    ab = [s * f for s, f in zip(sal, abs_s)]
    tax = [(s + a) * I["H6"] for s, a in zip(sal, ab)]
    ben = [s * I["H7"] for s in sal]
    nh = [h * I["M8"] for h in hires(inc)]
    return {"hc": tot, "sal": sal, "abs": ab, "ot": [0] * 16, "tax": tax, "ben": ben, "nh": nh,
            "total": [sum(x) for x in zip(sal, ab, tax, ben, nh)]}


L, T = lift_model(), tray_model(); S = sup_model(L, T)
L0, T0 = lift_model(True), tray_model(True); S0 = sup_model(L0, T0, True)
# check the replica against LibreOffice (lift rows: v5 cached values; tray / supervisor rows: scratch recalculation)
chk = {}
for lab, mdl, rows_, src in (("lift", L, {"hc": 31, "sal": 32, "abs": 34, "tax": 37, "ben": 38, "nh": 40, "total": 41}, ppv),
                             ("tray", T, {"hc": 52, "sal": 53, "abs": 55, "tax": 58, "ben": 59, "nh": 61, "total": 62}, pp_lo),
                             ("sup", S, {"hc": 71, "sal": 72, "abs": 74, "tax": 75, "ben": 76, "nh": 78, "total": 79}, pp_lo)):
    chk[lab] = max(abs(mdl[k][i] - num(src.cell(r, SDALL[i]).value)) for k, r in rows_.items() for i in range(16))
chk["lift_lo_scratch_vs_v5"] = max(abs(num(pp_lo.cell(r, c).value) - num(ppv.cell(r, c).value)) for r in range(25, 42) for c in SDALL)
chk["total_row81_lo"] = max(abs(L["total"][i] + T["total"][i] + S["total"][i] - num(pp_lo.cell(81, SDALL[i]).value)) for i in range(16))
assert all(v < 1e-6 for v in chk.values()), chk


def y27(x):
    return sum(x[4:16])


pp = {"check_max_abs_diff": chk, "inputs": {k: I[k] for k in ("B5", "C5", "B6", "C6", "B7", "C7", "B9", "C9", "H5", "H10", "M7", "M8")},
      "lift_total": y27(L["total"]), "tray_total": y27(T["total"]), "sup_total": y27(S["total"]),
      "lift_s41_v5": num(ppv["S41"].value), "tray_s62_lo": num(pp_lo["S62"].value), "sup_s79_lo": num(pp_lo["S79"].value),
      "total_s81_lo": num(pp_lo["S81"].value)}
pp["total"] = pp["lift_total"] + pp["tray_total"] + pp["sup_total"]
pp["current_only"] = {"lift": y27(L0["total"]), "tray": y27(T0["total"]), "sup": y27(S0["total"])}
pp["current_only"]["total"] = sum(pp["current_only"].values())
pp["current_only_parts"] = {k: y27(L0[k]) + y27(T0[k]) + y27(S0[k]) for k in ("sal", "abs", "ot", "tax", "ben", "nh")}
pp["ramp"] = pp["total"] - pp["current_only"]["total"]
pp["ramp_parts"] = {k: y27(L[k]) + y27(T[k]) + y27(S[k]) - pp["current_only_parts"][k] for k in ("sal", "abs", "ot", "tax", "ben", "nh")}
pp["hc_by_month"] = {"lift": L["hc"][4:], "tray": T["hc"][4:], "sup": S["hc"][4:]}
pp["hc_total_by_month"] = [a + b + c for a, b, c in zip(L["hc"][4:], T["hc"][4:], S["hc"][4:])]
pp["current_hc"] = I["B9"] + I["C9"] + I["H10"]
pp["ramp_hc_by_month"] = [x - pp["current_hc"] for x in pp["hc_total_by_month"]]
pp["ramp_by_month"] = [L["total"][i] + T["total"][i] + S["total"][i] - L0["total"][i] - T0["total"][i] - S0["total"][i] for i in range(4, 16)]
pp["hires_2027"] = {"lift": sum(hires([x - I["B9"] for x in L["hc"]])[4:]), "tray": sum(hires([x - I["C9"] for x in T["hc"]])[4:]),
                    "sup": sum(hires([x - I["H10"] for x in S["hc"]])[4:])}

# ------------------------------------------------------------------ 4b. PO: Logistics&WH Payroll (SD, not carried)
lw = sd["Logistics&WH Payroll"]
lw_dates = [d2(lw.cell(13, c).value) for c in SDALL]
B5, B6, B7, B10 = num(lw["B5"].value), num(lw["B6"].value), num(lw["B7"].value), num(lw["B10"].value)
B8 = d2(lw["B8"].value)
seats = []
for r in range(14, 23):
    lbl = lw.cell(r, 1).value
    code, rest = lbl.split(" ", 1)
    m = re.search(r"\((backfill for )?([^)]+)\)", rest)
    title = re.sub(r"\s*\(.*\)", "", rest).strip()
    nm = backfill_of = None
    if m:
        if m.group(1):
            backfill_of = m.group(2).strip()
        else:
            nm = m.group(2).strip()
    for x in (nm, backfill_of):
        if x:
            NAMES.update(t for t in toks(x) if len(t) > 1)
    start = d2(lw.cell(r, 21).value)
    annual = num(lw.cell(r, 24).value); elig = num(lw.cell(r, 25).value)
    hcm = [1 if (start is None or dt >= start) else 0 for dt in lw_dates]
    sal = [h * annual / 12 * (1 + (B7 if (dt >= B8 and elig == 1) else 0)) for h, dt in zip(hcm, lw_dates)]
    nh = [B10 if (start is not None and eomonth(dt, -1) < start <= dt) else 0 for dt in lw_dates]
    tot = [s * (1 + B5 + B6) + n for s, n in zip(sal, nh)]
    seats.append({"code": code, "title": title, "team": lw.cell(r, 20).value, "start": ym(start) if start else "on payroll",
                  "annual": annual, "pay_type": lw.cell(r, 22).value, "_name": nm, "_backfill_of": backfill_of,
                  "hc": hcm, "sal": sal, "nh": nh, "tot": tot, "row": r})
# replica check against the SD cached values
lw_chk = max(max(abs(sum(s["sal"][i] for s in seats) - num(lw.cell(43, SDALL[i]).value)) for i in range(16)),
             max(abs(sum(s["nh"][i] for s in seats) - num(lw.cell(46, SDALL[i]).value)) for i in range(16)),
             max(abs(sum(s["tot"][i] for s in seats) - num(lw.cell(47, SDALL[i]).value)) for i in range(16)))
assert lw_chk < 1e-4, lw_chk          # SD cached values carry ~10 significant digits
lw_total = num(lw["S51"].value)
assert abs(sum(sum(s["tot"][4:]) for s in seats) - lw_total) < 1e-4
# match seats to the HC rosters
lwo = {"total": lw_total, "check_max_abs_diff": lw_chk, "rates": {"tax": B5, "ben": B6}, "seats": []}
lw_named = {p["id"] for s in seats for p in people if s["_name"] and name_match(s["_name"], p["_name"])}
for s in seats:
    hits = [p for p in people if s["_name"] and name_match(s["_name"], p["_name"])]
    bf = [p for p in people if s["_backfill_of"] and name_match(s["_backfill_of"], p["_name"])]
    tmatch = [p for p in people if p["salary"] and tnorm(p["title"]) == tnorm(s["title"])]
    # title + salary + start (the handoff rule), one-to-one: people already matched by name to a seat are taken
    tss = [p for p in tmatch if abs(p["salary"] - s["annual"]) < 0.5 and p["start"] == s["start"] and p["id"] not in lw_named]
    e = {"seat": f"Logistics&WH {s['code']} {s['title']}", "team": s["team"], "start": s["start"], "annual": s["annual"],
         "cost_2027": sum(s["tot"][4:]), "sal_2027": sum(s["sal"][4:]), "nh_2027": sum(s["nh"][4:]),
         "hc_by_month": s["hc"][4:],
         "name_match": [p["id"] for p in hits], "backfill_of": [p["id"] for p in bf],
         "title_match_only": [p["id"] + f" (salary {p['salary']:,.0f}, start {p['start']}" +
                              ("; already matched by name to another seat)" if p["id"] in lw_named else ")")
                              for p in tmatch if p not in tss and p not in hits],
         "title_salary_match": [p["id"] for p in tss if p not in hits]}
    assert len(hits) <= 1
    e["overlap"] = bool(hits)
    if hits:
        p = hits[0]
        e["overlap_with"] = p["id"]
        e["hc_side_2027_cost"] = p["sal_2027"] * (1 + hc[p["dept"]]["rate_tax"] + hc[p["dept"]]["rate_ben"])
        p.setdefault("_also", []).append(f"Logistics&WH {s['code']} (SD model, not carried; by name)")
    for p in bf:
        p.setdefault("_also", []).append(f"named as the person Logistics&WH {s['code']} backfills (SD model, not carried)")
    lwo["seats"].append(e)
lwo["overlap_cost"] = sum(e["cost_2027"] for e in lwo["seats"] if e["overlap"])
lwo["net"] = lw_total - lwo["overlap_cost"]
lwo["net_seats"] = [e["seat"] for e in lwo["seats"] if not e["overlap"]]
lwo["net_hc_by_month"] = [sum(e["hc_by_month"][i] for e in lwo["seats"] if not e["overlap"]) for i in range(12)]
lwo["net_by_month"] = [sum(s["tot"][4 + i] for s, e in zip(seats, lwo["seats"]) if not e["overlap"]) for i in range(12)]
lwo["all_hc_by_month"] = [sum(s["hc"][4 + i] for s in seats) for i in range(12)]
# seats excluded in the model's own check block (rows 55-56)
excl = []
for r in (55, 56):
    lbl = lw.cell(r, 1).value or ""
    m = re.search(r"(LOG-\d+|MH-\d+)\s+(.*?)\s*\(", lbl)
    code = m.group(1) if m else ""
    rest = lbl.split(code, 1)[1] if code else lbl
    hits = [p for p in people if p["_name"] and any(name_match(" ".join(rest.split()[i:i + 2]), p["_name"]) for i in range(len(rest.split()) - 1))]
    for p in hits:
        NAMES.update(t for t in toks(p["_name"]) if len(t) > 1)
    excl.append({"cell": f"Logistics&WH Payroll!A{r}", "code": code, "amount_B": num(lw.cell(r, 2).value),
                 "matches": [p["id"] for p in hits]})
lwo["excluded_in_model"] = excl

# ------------------------------------------------------------------ 4c. PO overlap summary
pohc = [p for p in people if p["roster"] == "PO HC" and p["salary"]]
for p in pohc:
    p["_mapped"] = "PO 5110-5140 (typed 2027 values = PO HC rows 67-69)"
    p.setdefault("_also", []).append("Prod Payroll current staff (count match: model 7 lift + 2 tray on payroll Sep-26; no names or titles in the model)")
po = {"hc_people": len(pohc), "pp_current": pp["current_hc"],
      "in_pp_by_count": len(pohc) if abs(len(pohc) - pp["current_hc"]) < 0.5 else None,
      "in_lw_by_name": [e["overlap_with"] for e in lwo["seats"] if e["overlap"] and e["overlap_with"].startswith("PO HC")],
      "lw_backfill_refs": [x for e in lwo["seats"] for x in e["backfill_of"]],
      "po_5100": sum(tie["PO"]["v5"][k] for k in ("sal", "tax", "ben")),
      "pp_gross_gap": pp["total"] - sum(tie["PO"]["v5"][k] for k in ("sal", "tax", "ben")),
      "pp_lift_gap_v5": pp["lift_s41_v5"] - sum(tie["PO"]["v5"][k] for k in ("sal", "tax", "ben"))}
po["backfilled"] = [{"id": p["id"], "sal_2027": p["sal_2027"],
                     "cost_2027": p["sal_2027"] * (1 + hc["PO"]["rate_tax"] + hc["PO"]["rate_ben"])}
                    for p in pohc if p["id"] in po["lw_backfill_refs"]]
po["sd_hires_sep_dec26"] = {"lift": sum(hires([x - I["B9"] for x in L["hc"]])[:4]),
                            "tray": sum(hires([x - I["C9"] for x in T["hc"]])[:4]),
                            "sup": sum(hires([x - I["H10"] for x in S["hc"]])[:4])}
po["net_i05"] = pp["ramp"]
po["net_i17"] = lwo["net"]
po["net_combined"] = pp["ramp"] + lwo["net"]
po["net_combined_hc_by_month"] = [a + b for a, b in zip(pp["ramp_hc_by_month"], lwo["net_hc_by_month"])]
po["net_combined_by_month"] = [a + b for a, b in zip(pp["ramp_by_month"], lwo["net_by_month"])]
po["pp_current_vs_po_hc"] = {"model_current_cost": pp["current_only"]["total"], "po_5100": po["po_5100"],
                             "diff": pp["current_only"]["total"] - po["po_5100"],
                             "model_avg_salary": I["B5"], "hc_avg_salary": sum(p["salary"] for p in pohc) / len(pohc)}

# ------------------------------------------------------------------ 5. FE: Fld Eng Budget roster vs FE HC
feb = v5["Fld Eng Budget"]
fehc = [p for p in people if p["roster"] == "FE HC"]
fe_rows = []
for r in range(13, 22):
    lbl = feb.cell(r, 1).value
    parts = [x.strip() for x in lbl.split("–")]
    title = parts[0]
    nm = parts[1] if len(parts) > 1 and parts[1].lower() not in PLACEHOLDER else None
    if nm:
        NAMES.update(t for t in toks(nm) if len(t) > 1)
    sal = num(feb.cell(r, 2).value); start = d2(feb.cell(r, 3).value)
    sd_m = [num(feb.cell(59 + (r - 13), c).value) for c in range(2, 14)]
    hits = [p for p in fehc if nm and name_match(nm, p["_name"])]
    basis = "name" if hits else ""
    if not hits:   # one-to-one: title + salary only among FE HC rows with no name (rows already matched by name are taken)
        hits = [p for p in fehc if p["salary"] and not p["_name"] and abs(p["salary"] - sal) < 0.5 and tnorm(p["title"]) == tnorm(title)]
        basis = "title + salary" if hits else ""
    assert len(hits) <= 1
    e = {"sd": f"Fld Eng Budget r{r} {title}", "sd_salary": sal, "sd_start": ym(start), "sd_2027": sum(sd_m),
         "basis": basis, "hc": hits[0]["id"] if hits else None}
    if hits:
        p = hits[0]
        e.update({"hc_salary": p["salary"], "hc_start": p["start"], "hc_2027": p["sal_2027"],
                  "diff_2027": sum(sd_m) - p["sal_2027"],
                  "max_monthly_diff": max(abs(a - b) for a, b in zip(sd_m, p["m27"])),
                  "start_differs": p["start"] != ym(start)})
        p["_mapped"] = f"FE 6610-6640 via Fld Eng Budget row {r} (matched on {basis})"
    else:
        open_rows = [q for q in fehc if not q["salary"] and tnorm(q["title"]) in tnorm(title)]
        e["possible_hc_row"] = [q["id"] + " (no salary, no start)" for q in open_rows]
        e["not_on_hc"] = True
        other = [q for q in people if q["roster"] != "FE HC" and nm and name_match(nm, q["_name"])]
        e["on_other_roster_by_name"] = [q["id"] for q in other]
        for q in other:
            q.setdefault("_also", []).append(f"Fld Eng Budget r{r} {title} (by name): also costed in FE 6610-6640")
    fe_rows.append(e)
for q in fehc:
    if not q["salary"]:
        q["_mapped"] = "none: open row with no salary (0 in FE HC)"
        cands = [e["sd"] for e in fe_rows if e.get("not_on_hc") and tnorm(q["title"]) in tnorm(e["sd"].split(" ", 3)[-1])]
        q.setdefault("_also", []).append("possibly " + "; ".join(cands) if cands else "no SD row")
fe = {"rows": fe_rows, "sd_total_sal": sum(e["sd_2027"] for e in fe_rows), "hc_total_sal": hc["FE"]["z"]["sal"],
      "not_on_hc": [e["sd"] for e in fe_rows if e.get("not_on_hc")],
      "not_on_hc_2027": sum(e["sd_2027"] for e in fe_rows if e.get("not_on_hc")),
      "matched_diff_2027": sum(e.get("diff_2027", 0) for e in fe_rows),
      "matched_max_monthly_diff": max(e.get("max_monthly_diff", 0) for e in fe_rows),
      "start_differs": [e["sd"] + f": HC {e['hc_start']}, SD {e['sd_start']}" for e in fe_rows if e.get("start_differs")],
      "sd_rates": {"tax": num(feb["B22"].value), "ben": num(feb["B23"].value)},
      "hc_rates": {"tax": hc["FE"]["rate_tax"], "ben": hc["FE"]["rate_ben"]},
      "pl_v5": {k: tie["FE"]["v5"][k] for k in ("sal", "tax", "ben")}}
assert abs(fe["sd_total_sal"] - fe["pl_v5"]["sal"]) < 1e-4
base = fe["pl_v5"]["sal"]
fe["burden"] = {"sd_tax": fe["pl_v5"]["tax"], "sd_ben": fe["pl_v5"]["ben"],
                "hc_rate_tax": base * fe["hc_rates"]["tax"], "hc_rate_ben": base * fe["hc_rates"]["ben"]}
fe["burden"]["diff_tax"] = fe["burden"]["sd_tax"] - fe["burden"]["hc_rate_tax"]
fe["burden"]["diff_ben"] = fe["burden"]["sd_ben"] - fe["burden"]["hc_rate_ben"]
fe["burden"]["diff_total"] = fe["burden"]["diff_tax"] + fe["burden"]["diff_ben"]
mb = sum(e["sd_2027"] for e in fe_rows if e["hc"])
fe["burden"]["matched_base"] = mb
fe["burden"]["matched_diff_total"] = mb * (fe["sd_rates"]["tax"] + fe["sd_rates"]["ben"] - fe["hc_rates"]["tax"] - fe["hc_rates"]["ben"])
fe["coo_book"] = {k: tie["FE"]["coo_book"][k] for k in ("sal", "tax", "ben")}
fe["coo_book_gap_vs_hc"] = hc["FE"]["z"]["sal"] - fe["coo_book"]["sal"]
fe["coo_book_gap_rows"] = [p["id"] for p in fehc if p["salary"] and abs(p["sal_2027"] - fe["coo_book_gap_vs_hc"]) < 0.01]
fe["not_on_hc_cost_sd_rates"] = fe["not_on_hc_2027"] * (1 + fe["sd_rates"]["tax"] + fe["sd_rates"]["ben"])

# ------------------------------------------------------------------ 6. CO / PE mapping, PE transfer row
for d in ("CO", "PE"):
    for p in people:
        if p["roster"] == f"{d} HC" and p["salary"]:
            p["_mapped"] = f"{d} 6610-6640 (typed 2027 values = {d} HC rows 67-69)"
pe_tr = [p for p in people if p["roster"] == "PE HC" and "transfer" in (p["flag_col_a"] or "").lower()]
pe_transfer = []
for p in pe_tr:
    t = p["sal_2027"] * hc["PE"]["rate_tax"]; b = p["sal_2027"] * hc["PE"]["rate_ben"]
    others = [q["id"] for q in people if q is not p and q["_name"] and name_match(q["_name"], p["_name"])]
    pe_transfer.append({"id": p["id"], "flag": p["flag_col_a"], "salary": p["salary"], "start": p["start"], "end": p["end"],
                        "sal_2027": p["sal_2027"], "tax_2027": t, "ben_2027": b, "total_2027": p["sal_2027"] + t + b,
                        "elsewhere_by_name": others,
                        "title_elsewhere": [q["id"] for q in people if q is not p and tnorm(q["title"]) == tnorm(p["title"])],
                        "in_pe_pl": tie["PE"]["v5"]["max_monthly_diff_vs_hc"] < 0.01})
    p.setdefault("_also", []).append("flagged 'transfer?' in column A")

# ------------------------------------------------------------------ 7. I-28 duplicate scan across every roster
srcs = []
for p in people:
    srcs.append({"src": p["roster"], "id": p["id"], "name": p["_name"], "title": p["title"], "salary": p["salary"], "start": p["start"]})
for r in range(13, 22):
    lbl = feb.cell(r, 1).value; parts = [x.strip() for x in lbl.split("–")]
    srcs.append({"src": "SD Fld Eng Budget", "id": f"Fld Eng Budget r{r} {parts[0]}",
                 "name": parts[1] if len(parts) > 1 and parts[1].lower() not in PLACEHOLDER else None,
                 "title": parts[0], "salary": num(feb.cell(r, 2).value), "start": ym(d2(feb.cell(r, 3).value))})
for key, r, sal_cell in (("coord", 76, "H15"), ("mgr", 77, "H16")):
    nm = named_lbl[key].split("–")[0].strip()
    srcs.append({"src": "SD Fld Ops Payroll", "id": f"Fld Ops Payroll r{r} {'Operations Coordinator' if key == 'coord' else 'Manager'}",
                 "name": nm, "title": "Operations Coordinator" if key == "coord" else "Field Maintenance Manager",
                 "salary": num(fop[sal_cell].value), "start": "Sep-26 (on payroll)"})
for s in seats:
    srcs.append({"src": "SD Logistics&WH", "id": f"Logistics&WH {s['code']} {s['title']}", "name": s["_name"],
                 "title": s["title"], "salary": s["annual"], "start": s["start"]})
pairs = []
named_into = set()          # (entity id, other source) already matched by name
for i in range(len(srcs)):
    for j in range(len(srcs)):
        a, b = srcs[i], srcs[j]
        if i != j and a["src"] != b["src"] and a["name"] and b["name"] and name_match(a["name"], b["name"]):
            named_into.add((a["id"], b["src"]))
for i in range(len(srcs)):
    for j in range(i + 1, len(srcs)):
        a, b = srcs[i], srcs[j]
        if a["src"] == b["src"]:
            if a["name"] and b["name"] and name_match(a["name"], b["name"]):
                pairs.append({"a": a["id"], "b": b["id"], "basis": "name (same roster)"})
            continue
        if a["name"] and b["name"]:
            if name_match(a["name"], b["name"]):
                pairs.append({"a": a["id"], "b": b["id"], "basis": "name"})
            continue
        if (a["id"], b["src"]) in named_into or (b["id"], a["src"]) in named_into:
            continue        # that person is already matched by name to someone in the other source (one-to-one)
        if a["salary"] and b["salary"] and abs(a["salary"] - b["salary"]) < 0.5 and tnorm(a["title"]) == tnorm(b["title"]):
            pairs.append({"a": a["id"], "b": b["id"], "basis": "title + salary" + (" + start" if a["start"] == b["start"] else f" (start {a['start']} vs {b['start']})")})


def classify(pr):
    s = {pr["a"].split(" r")[0].split(" ")[0] + "|" + pr["b"].split(" r")[0].split(" ")[0]}
    a, b = pr["a"], pr["b"]
    if (a.startswith("FE HC") and b.startswith("Fld Eng Budget")) or (b.startswith("FE HC") and a.startswith("Fld Eng Budget")):
        return "same person, one P&L source (FE 6610-6640 via Fld Eng Budget; FE HC is the roster, not costed separately)"
    if (a.startswith("FO HC") and b.startswith("Fld Ops Payroll")) or (b.startswith("FO HC") and a.startswith("Fld Ops Payroll")):
        return "same person, one P&L source (FO 5510-5540 via Fld Ops Payroll)"
    if (a.startswith("FO HC") and b.startswith("Fld Eng Budget")) or (b.startswith("FO HC") and a.startswith("Fld Eng Budget")):
        return "DUPLICATE across P&L sources: FO 5510-5540 (Fld Ops Payroll current techs, by count) and FE 6610-6640 (Fld Eng Budget)"
    if "Logistics&WH" in a or "Logistics&WH" in b:
        return "duplicate if the Logistics&WH model is adopted (model not carried); excluded from the I-17 net increment"
    return "DUPLICATE across P&L sources: review"


for pr in pairs:
    pr["class"] = classify(pr)
fofe = []
for pr in pairs:
    if pr["class"].startswith("DUPLICATE across P&L sources: FO"):
        fid = pr["a"] if pr["a"].startswith("Fld Eng Budget") else pr["b"]
        hid = pr["b"] if fid == pr["a"] else pr["a"]
        fr = int(fid.split(" r")[1].split(" ")[0])
        e = [x for x in fe_rows if x["sd"].startswith(f"Fld Eng Budget r{fr} ")][0]
        hp = [p for p in people if p["id"] == hid][0]
        ct = fo["blocks"]["current_techs"]
        fofe.append({"hc": hid, "sd": fid, "fe_sal_2027": e["sd_2027"],
                     "fe_cost_2027": e["sd_2027"] * (1 + fe["sd_rates"]["tax"] + fe["sd_rates"]["ben"]),
                     "fo_model_one_tech_2027": ct["total"] / fo["inputs"]["techs_B11"],
                     "fo_model_one_tech_sal_2027": ct["sal"] / fo["inputs"]["techs_B11"],
                     "hc_salary": hp["salary"], "sd_salary": e["sd_salary"], "hc_sal_2027": hp["sal_2027"],
                     "fe_hc_open_row": e.get("possible_hc_row", [])})
hosd = [p for p in people if tnorm(p["title"]) == tnorm("Head of Service Delivery")]
hosd_chk = []
for p in hosd:
    hosd_chk.append({"id": p["id"],
                     "co_pe_name_hits": [q["id"] for q in people if q["roster"] in ("CO HC", "PE HC") and q["_name"] and name_match(q["_name"], p["_name"])],
                     "co_pe_title_hits": [q["id"] for q in people if q["roster"] in ("CO HC", "PE HC") and tnorm(q["title"]) == tnorm(p["title"])],
                     "fe_budget_row": [e["sd"] for e in fe_rows if e["hc"] == p["id"]],
                     "near_titles": [q["id"] + " (different name and salary)" for q in people if q["roster"] in ("CO HC", "PE HC")
                                     and "delivery" in tnorm(q["title"]) and not (q["_name"] and name_match(q["_name"], p["_name"]))]})
dup = {"pairs": pairs, "fo_fe": fofe, "n_cross_source_review": sum(1 for p in pairs if p["class"].startswith("DUPLICATE")),
       "n_lw": sum(1 for p in pairs if "Logistics&WH" in p["class"]), "hosd": hosd_chk,
       "n_same_fe": sum(1 for p in pairs if p["class"].startswith("same person, one P&L source (FE")),
       "n_same_fo": sum(1 for p in pairs if p["class"].startswith("same person, one P&L source (FO")),
       "same_name_across_hc_tabs": [p for p in pairs if p["a"].split(" ")[1] == "HC" and p["b"].split(" ")[1] == "HC"
                                    and p["a"].split(" ")[0] != p["b"].split(" ")[0]]}

# ------------------------------------------------------------------ 8. roster -> P&L source map (CSV, no names)
mapping = []
for p in people:
    mapping.append({"roster": p["roster"], "row": p["row"], "title": p["title"], "section": p["section"],
                    "annual_salary": p["salary"] if p["salary"] is not None else "", "start": p["start"], "end": p["end"],
                    "salary_2027": round(p["sal_2027"], 2), "pnl_source": p.get("_mapped", "UNMAPPED"),
                    "also_in": "; ".join(p.get("_also", [])), "col_a_flag": p["flag_col_a"]})
unmapped = [m for m in mapping if m["pnl_source"] == "UNMAPPED"]
assert not unmapped, unmapped
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=list(mapping[0].keys()), lineterminator="\n")
w.writeheader(); w.writerows(mapping)
csv_text = buf.getvalue()

# ------------------------------------------------------------------ output + privacy self-check
for p in people:
    for k in [k for k in p if k.startswith("_")]:
        if k not in ("_mapped", "_also"):
            p.pop(k)
for s in seats:
    s.pop("_name"); s.pop("_backfill_of")
out = {"hc": hc, "tie": tie, "fo": fo, "pp": pp, "lw": lwo, "po": po, "fe": fe, "pe_transfer": pe_transfer, "dup": dup,
       "mapping_summary": {"people": len(mapping), "by_roster": {d: sum(1 for m in mapping if m["roster"] == f"{d} HC") for d in DEPTS},
                           "with_also": sum(1 for m in mapping if m["also_in"]), "unmapped": len(unmapped)},
       "months": MONTHS}
text = json.dumps(out, indent=1, default=str)
bad = sorted({t for t in NAMES if re.search(rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z])", text + csv_text, re.I)})
COMMON = {"field", "manager", "lead", "new", "hire"}           # title words are not names
bad = [b for b in bad if b not in COMMON]
assert not bad, f"name tokens in output: {len(bad)}"
open(OUT_JSON, "w").write(text)
open(OUT_CSV, "w").write(csv_text)
for e in [fop["E15"].value, fop["E16"].value] + [feb.cell(r, 1).value for r in range(13, 22)] + \
        [lw.cell(r, 1).value for r in list(range(14, 23)) + [55, 56]]:
    for m in re.finditer(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+)", e or ""):
        if any(name_match(m.group(1), p_) for p_ in FULL):
            FULL.add(m.group(1))
json.dump({"tokens": sorted(NAMES), "full": sorted(FULL)}, open(OUT_JSON + ".names", "w"))   # scratch only (WORK dir)
print(f"recon: {len(mapping)} roster people mapped (unmapped 0); PP total {pp['total']:,.0f}, ramp {pp['ramp']:,.0f}; "
      f"L&WH net {lwo['net']:,.0f}; FO current {fo['current']['total']:,.0f} ramp {fo['ramp']['total']:,.0f}; "
      f"FE burden diff {fe['burden']['diff_total']:,.0f}; pairs {len(pairs)}; name tokens checked {len(NAMES)}")
