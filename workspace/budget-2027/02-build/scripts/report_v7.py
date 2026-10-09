"""Write 02-build_notes_v7.md and the v7 Collation Notes content (JSON).

Usage:
  python3 -I report_v7.py V6_MD CN6_JSON V6_XLSX RECON_JSON FIG7_JSON LO_VERSION_TXT WORKFILE COO SD NEW OUT_NOTES_JSON OUT_MD
                          [ANALYZE_JSON]

v7 = v6 with notes and presentation fixes only (critic v6 B1-B3, O1-O8; verifier v6 V1). No budget value changes: the
workbook is v6 with a regenerated Collation Notes sheet.
Text is built from the v6 notes (the shipped md and the v6 Collation Notes, extracted byte-exactly by cnotes_v6.py); each
edit of carried text is a targeted replacement that must hit exactly once. Numbers: workbook cached values (V6_XLSX =
v7 values), RECON_JSON (recon_v6.py), FIG7_JSON (figures_v7.py; scen_v7.py inside it). Carried caveat rows take their
effect from the v6 Collation Notes, and the script checks that the contribution they act on is unchanged. No figure is
typed here.
PRIVACY: md only - every per-person amount for an identified employee is rounded to the nearest $5k ('~') by
paylist_v7.round_text after the text is assembled; the 'contribution after' of a per-person row is shown from the rounded
effect. The Collation Notes sheet keeps exact figures (the workbook already holds the named HC tabs) and carries the
CONFIDENTIAL banner. No names are read here.
Without ANALYZE_JSON the md has placeholders for the check sections (pass 1); the Collation Notes JSON does not depend on
ANALYZE_JSON, so both passes must give the same JSON.
"""
import sys, os, json, re, hashlib, copy, collections
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paylist_v7

(V6_MD, CN6, V6X, RECON, FIG7, LOV, WFILE, COO, SD, NEW, OUT_JSON, OUT_MD) = sys.argv[1:13]
AN = json.load(open(sys.argv[13])) if len(sys.argv) > 13 else None
R = json.load(open(RECON)); F = json.load(open(FIG7)); cn6 = json.load(open(CN6))
md6 = open(V6_MD).read()
lov = open(LOV).read().strip()
w = openpyxl.load_workbook(V6X, data_only=True)
BANNER = "CONFIDENTIAL – contains named compensation data (HC-* tabs); restrict distribution"


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
    return "| " + " | ".join(row) + " |"


def val(col, rows):
    return sum(float(w["COO P&L"][f"{col}{r}"].value or 0) for r in rows)


# ------------------------------------------------------------------ figures
C = val("AG", [132])
assert abs(C - F["contribution"]) < 1e-6
pp, po, lw, fo, fe, hc, dup = R["pp"], R["po"], R["lw"], R["fo"], R["fe"], R["hc"], R["dup"]
I05, I17 = po["net_i05"], po["net_i17"]
ev, cap, b2, ct, b3, o1, o2, v1, o5, o6 = (F[k] for k in ("b1_evidence", "b1_cap", "b2", "contrib", "b3", "o1", "o2", "v1", "o5", "o6"))
I05_7 = b2["I05_7"]; d9, d7 = cap["d9"]["dep"], cap["d7"]["dep"]
COMB9, COMB7, COMB6 = b2["combined_9_dedup"], b2["combined_7"], b2["combined_v6"]
fofe = dup["fo_fe"][0]
pet = R["pe_transfer"][0]
B11 = fo["inputs"]["techs_B11"]
FO_EFF, FE_EFF = v1["fo_effect"], v1["fe_effect"]
assert abs(v1["fo_payroll"] - fofe["fo_model_one_tech_2027"]) < 0.01
V6_FO = fofe["fo_model_one_tech_2027"]                      # the v6 figure (payroll only), corrected in v7
fe_b = fe["burden"]
cs_hire = [e for e in fe["rows"] if e.get("not_on_hc") and not e.get("on_other_roster_by_name")][0]
cs_hire_cost = cs_hire["sd_2027"] * (1 + fe["sd_rates"]["tax"] + fe["sd_rates"]["ben"])
FICA = o6["fica"]
MON = R["months"]
o6_ff = o6["fo_gap_at_fica"] + o6["fe_gap_at_fica"]

# ------------------------------------------------------------------ carried caveat rows (v6 Collation Notes)
cv6 = [s for s in cn6["sections"] if s["heading"].startswith("Caveats on the headline")][0]
carried = collections.OrderedDict()
for row in cv6["table"]["rows"]:
    carried.setdefault(row[0], []).append(row)
for k, rows in carried.items():
    for row in rows:
        if isinstance(row[3], (int, float)):
            assert abs(row[4] - (C + row[3])) < 0.01, ("carried row does not act on the v7 contribution", k)
i10 = carried["I-10"][0][3]; i31s = [r for r in carried["I-31"] if r[3] < 0][0][3]
i32full = max(r[3] for r in carried["I-32"])
i32tr = [r for r in carried["I-32"] if r[2].startswith("Trend alternative:")][0][3]
i32tr2 = [r for r in carried["I-32"] if r[2].startswith("Trend alternative continued")][0][3]
assert abs(carried["I-17"][0][3] + I17) < 0.01 and abs(carried["I-05"][0][3] + I05) < 0.01
v6_range = re.search(r"range from (\(?[\d,]+\)?) to (\(?[\d,]+\)?)", cv6["after"][-1] if cv6.get("after") else cv6["table"]["after"][-1])
V6R = f"{v6_range.group(1)} to {v6_range.group(2)}"
LB1 = C - COMB7 + i10 + i31s
LB1_9 = C - COMB9 + i10 + i31s
LB2 = C - I17 + i10 + i31s
LBC = C - d7 - I17 + i10 + i31s
UB = C + i32full
assert LB1 < LB1_9 < LBC < LB2 < C < UB

SRC_PP = "Prod Payroll!S81 (tray/supervisor rows evaluated per A-28); PO!AG33:AG36; 'HC-PO'!Z67:Z70"
SRC_CAP = "DeploySum!A47, rows 19-20, 24-25; 'Depreciation Schedule'!B6:B13, rows 38-62; Prod Payroll"
cav = []   # [item, direction, text, effect(number|str), after(number|str), source, person]
cav.append(["I-05 expensed, 9-overlap", "downside",
            f"Production payroll ramp (SD Prod Payroll) that PO 5110-5140 does not carry, if production labour is EXPENSED (Decision #1): model 2027 total {f0(pp['total'])} "
            f"(lift {f0(pp['lift_total'])}, tray {f0(pp['tray_total'])}, supervisors {f0(pp['sup_total'])}) less the model's cost of the {pp['current_hc']:.0f} current staff "
            f"({f0(pp['current_only']['total'])}), all 9 PO HC people counted as Prod Payroll's current staff (count match).", -I05, C - I05, SRC_PP, False])
cav.append(["I-05 expensed, 7-overlap", "downside",
            f"Same, with only the {b2['n_prod']} PO HC production staff as Prod Payroll's current staff (the {b2['n_mh']} material-handling roles are tied to Logistics&WH, B2): "
            f"+{b2['extra']['central']:,.0f} for the {b2['n_extra']:.0f} model seats no roster fills (model average current cost per head {b2['per_head']['avg']:,.0f}; "
            f"{b2['extra']['low']:,.0f} to {b2['extra']['high']:,.0f} as 2 tray or 2 lift seats).", -I05_7, C - I05_7, SRC_PP + "; 'HC-PO'!C14:C22", False])
cav.append(["I-05 sensitivity (O1)", "downside",
            f"9-overlap ramp with the PO HC burden rates ({pct(o1['po_rates'][0], 2)} tax / {pct(o1['po_rates'][1], 2)} benefits, {pct(o1['po_rate_pct'])} of salary) instead of the model's "
            f"({pct(o1['model_burden_pct_of_sal'])} of salary): +{o1['diff']:,.0f} on top of the ramp.", -o1["I05_at_po_rates"], C - o1["I05_at_po_rates"],
            "Prod Payroll!B6:C7, H6:H7; 'HC-PO'!D6:D7", False])
cav.append(["I-05 capitalised on top of the unit cost, 9-overlap", "downside",
            f"If production labour is CAPITALISED and added to the CapEx unit cost, only depreciation reaches 2027 (Depreciation Schedule logic: full month from go-live, "
            f"lifts {ev['lift_life']:.0f} / trays {ev['tray_life']:.0f} months; units built {cap['build_lag_months']} months before go-live). Labour per unit "
            f"{cap['d9']['labour_per_lift']:,.0f} per lift ({pct(cap['d9']['labour_pct_of_lift_cost'])} of {ev['lift_unit_cost']:,.0f}) and {cap['d9']['labour_per_tray']:,.0f} per tray; "
            f"{f0(cap['d9']['on_balance_sheet_end27'])} stays on the balance sheet at Dec-27.", -d9, C - d9, SRC_CAP, False])
cav.append(["I-05 capitalised on top of the unit cost, 7-overlap", "downside", "Same, 7-overlap ramp (lift / tray mix unchanged, A-34).", -d7, C - d7, SRC_CAP, False])
cav.append(["I-05 capitalised inside the unit cost", "none",
            f"If the 65,000 / 8,000 unit costs already include production labour, the ramp is already inside the budgeted depreciation of the 2027 go-lives and the "
            f"budget needs no change for it (the ramp is a CapEx / cash item).", 0.0, C, "DeploySum!A47; 'Depreciation Schedule'!B6, B8", False])
cav += carried["I-17"]
cav.append(["I-05 + I-17 expensed, 9-overlap", "downside",
            f"Both payroll ramps, deduplicated. v6 showed {f0(-COMB6)}, which takes PO HC r20 out twice: once inside I-05 (as one of Prod Payroll's 9, by count) and once inside "
            f"I-17 (as seat MH-01, by name). Keeping the count match, MH-01 becomes an unfilled seat: +{b2['mh01_cost']:,.0f}.", -COMB9, C - COMB9, "as above; Logistics&WH MH-01", False])
cav.append(["I-05 + I-17 expensed, 7-overlap", "downside",
            "Both payroll ramps with the 7-overlap: PO HC r20 = MH-01 (name) and r16 (material handling, backfilled by MH-02) sit with Logistics&WH, so no seat is taken out twice.",
            -COMB7, C - COMB7, "as above", False])
cav += carried["I-10"] + carried["I-26"]
cav.append(["I-28", "upside", f"Probable duplicate (name match only; title and salary differ; likely FO->FE move): FO HC r15 Field Technician = Fld Eng Budget r15 Field Engineer. "
            f"Remove from FO (Fld Ops Payroll B11 {B11:.0f} -> {B11 - 1:.0f}), recalculated: payroll +{v1['fo_payroll']:,.0f} and +{v1['knock_on']:,.0f} on 5330 (Fld Maint Budget!B29 "
            f"= B30 + Fld Ops Payroll!B11); supervisor headcount unchanged. Pro rata if the move happens mid-year.", FO_EFF, C + FO_EFF,
            "Fld Ops Payroll!B11, rows 20-24; Fld Maint Budget!B29", False])
cav.append(["I-28", "upside", "Same person: remove from FE instead (Fld Eng Budget row 15, at SD burden rates). Pro rata if the move happens mid-year.",
            FE_EFF, C + FE_EFF, "Fld Eng Budget!B15; rows 61, 69-70", True])
cav += carried["I-31"] + carried["I-32"] + carried["I-33"] + carried["I-34"]
cav.append(["I-34 with FE tax at 7.65%", "upside", f"The HC T&B tax rates are below the {pct(FICA, 2)} employer FICA and unverified (I-37). If FE payroll tax cannot be below "
            f"{pct(FICA, 2)}, the 6630 part of I-34 (+{o6['i34_tax_part']:,.0f}) goes and the SD 6.8% is short: upside benefits only.", o6["i34_if_tax_at_fica"],
            C + o6["i34_if_tax_at_fica"], "'HC-FE'!D6:D7; Fld Eng Budget!B22:B23", False])
cav.append(["I-37", "downside", f"PO, CO and PE payroll tax uses the HC T&B rates ({', '.join(d + ' ' + pct(o6['depts'][d]['hc_rate'], 2) for d in ('PO', 'CO', 'PE'))}), all below "
            f"{pct(FICA, 2)}. At {pct(FICA, 2)} on every salary dollar (upper bound: the Social Security wage base lowers it for high salaries).", -o6["po_co_pe_gap"],
            C - o6["po_co_pe_gap"], "'HC-PO'!D6; 'HC-CO'!D6; 'HC-PE'!D6; PO!AG34; CO!AG68; PE!AG68", False])
cav.append(["I-37", "downside", f"FO and FE payroll tax uses the SD field rate {pct(o6['sd_rate'])}, also below {pct(FICA, 2)} (same upper-bound basis; FO salary base "
            f"{f0(o6['fo_sal_budget'])} incl. the ramp, FE {f0(o6['fe_sal_budget'])}).", -o6_ff, C - o6_ff, "Fld Ops Payroll!B7; Fld Eng Budget!B22", False])
cav += [r + [True] if r[0] == "I-35" else r for r in carried["I-35"]]
cav += carried["I-36"]
cav.append(["I-39", "upside", f"FE HC r35 Field Engineer Manager is an open seat (HC-FE 'Open Positions'), not an employee; COO book _2 leaves it out and Fld Eng Budget r20 costs it "
            f"from Jan-27. If the seat stays open all of 2027 (salary + SD burden).", o5["sd_cost_2027"], C + o5["sd_cost_2027"], "'HC-FE'!B34:F35; Fld Eng Budget!A20:C20, row 66", False])
cav += carried["A-14"] + carried["A-22"]
cav = [r if len(r) == 7 else r + [False] for r in cav]


def cav_md_row(r):
    e, a, person = r[3], r[4], r[6]
    if isinstance(e, (int, float)) and person:
        es = ("+" if e > 0 else "-") + f"~{abs(r5(e)):,.0f}"
        as_ = f"~{r5(C + r5(e)):,.0f}"
        return [r[0], r[1], r[2] + " (per-person amount rounded to $5k)", es, as_, r[5]]
    es = eff(e) if isinstance(e, (int, float)) else e
    as_ = f0(a) if isinstance(a, (int, float)) else a
    return [r[0], r[1], r[2], es, as_, r[5]]


sf = []
sf.append(f"Sign-flip statement (computed, net increments, v7): The 2027 COO contribution of {f0(C)} changes sign on I-05 alone if production labour is expensed "
          f"({f0(C)} - {I05:,.0f} = {f0(C - I05)} at the 9-overlap; {f0(C - I05_7)} at the 7-overlap), on I-17 alone ({f0(C - I17)}) or on I-10 alone ({f0(C + i10)}). "
          f"If production labour is capitalised (Decision #1), I-05 alone leaves {f0(C - d9)} (9-overlap) or {f0(C - d7)} (7-overlap), or {f0(C)} if the unit cost already "
          f"includes it; the sign does not flip. I-31 alone leaves {f0(C + i31s)}.")
sf.append(f"Together, I-05 + I-17 (expensed, deduplicated) take it to {f0(C - COMB9)} (9-overlap) or {f0(C - COMB7)} (7-overlap); v6 showed {f0(C - COMB6)}, which took "
          f"PO HC r20 out twice. I-10 with the I-31 shortfall gives {f0(C + i10 + i31s)}.")
sf.append(f"Upside: I-32 can add up to {f0(i32full)} (contribution {f0(C + i32full)}); the trend alternative adds {f0(i32tr)} ({f0(C + i32tr)}), or {f0(i32tr2)} "
          f"({f0(C + i32tr2)}) if the decline also ran through Oct-Dec 26. Smaller: I-28 +{FO_EFF:,.0f} to +{FE_EFF:,.0f}, I-34 +{fe_b['diff_total']:,.0f} "
          f"(+{o6['i34_if_tax_at_fica']:,.0f} if the FE tax rate is at least {pct(FICA, 2)}), I-35 up to +{pet['total_2027']:,.0f}, I-36 +{cs_hire_cost:,.0f}, I-39 up to "
          f"+{o5['sd_cost_2027']:,.0f}. With costs held fixed, revenue {f0(C)} ({C / val('AG', [16]) * 100:.1f}%) below plan also takes the contribution to zero.")
sf.append(f"Range (v7): the range is asymmetric by construction. The lower end adds every quantified downside; the upper end adds only I-32 in full (the other upsides "
          f"A-14, I-28, I-31 double count, I-33, I-34, I-35, I-36 and I-39 are listed, not added). Lower bound 1, all quantified downsides with I-05 expensed (I-05 + I-17 "
          f"deduplicated at the 7-overlap, I-10, I-31 shortfall): {f0(LB1)}; at the 9-overlap {f0(LB1_9)}. Lower bound 2, excluding I-05 (production labour capitalised "
          f"into the unit cost, or the ramp not adopted; I-17, I-10, I-31 shortfall): {f0(LB2)}. With I-05 capitalised on top of the unit cost (depreciation only, "
          f"7-overlap): {f0(LBC)}. Upper end: {f0(UB)}. I-37 (tax rates, unverified upper bound) is not in the range. v6 range: {V6R}.")
sf.append(f"Conclusion: the sign of the 2027 COO contribution is not established by this budget, and Decision #1 moves it more than any other open item: expensed, "
          f"I-05 alone takes it to {f0(C - I05)} to {f0(C - I05_7)}; capitalised, the production ramp costs at most {d7:,.0f} of 2027 depreciation. Treat {f0(C)} as a "
          f"point estimate inside {f0(LB1)} to {f0(UB)} (lower bound 2: {f0(LB2)}) until Decisions #1, #6 and #2 (I-05, I-17, I-32) are answered.")

# ------------------------------------------------------------------ decisions pending
dp6 = cn6["sections"][0]
assert dp6["heading"].startswith("Decisions pending") and len(dp6["table"]["rows"]) == 8
DEC1 = ["1", "Production labour: expensed, or capitalised into the CapEx unit cost (65,000 per lift / 8,000 per tray)?", "I-05, I-23 (B1)",
        f"PO 5110-5140 ({f0(po['po_5100'])}, the current PO HC staff) is expensed. The production ramp is not in the budget at all (Decision #6), so the "
        f"{f0(C)} reads as if the ramp were capitalised inside the unit cost or not adopted.",
        f"Expensed: ramp ({I05:,.0f}) at the 9-overlap / ({I05_7:,.0f}) at the 7-overlap; contribution {f0(C - I05)} / {f0(C - I05_7)}. Capitalised on top of the "
        f"unit cost (2027 depreciation only, Depreciation Schedule logic, {ev['lift_life']:.0f} / {ev['tray_life']:.0f} months): ({d9:,.0f}) / ({d7:,.0f}); contribution "
        f"{f0(C - d9)} / {f0(C - d7)}. Already inside the 65,000 / 8,000 unit cost: 0 ({f0(C)}).",
        "User / Finance (capitalisation policy), with the PO owner"]
DEC = [DEC1]
for i, r in enumerate(dp6["table"]["rows"]):
    r = list(r); r[0] = str(i + 2)
    if r[2] == "I-05, I-17":
        r[4] = (f"Add the Prod Payroll ramp (if expensed, Decision #1): ({I05:,.0f}) at the 9-overlap, ({I05_7:,.0f}) at the 7-overlap. Add the 7 new Logistics&WH "
                f"seats: ({I17:,.0f}). Both, deduplicated: ({COMB9:,.0f}) (9-overlap) or ({COMB7:,.0f}) (7-overlap); v6 showed ({COMB6:,.0f}), which takes PO HC r20 out "
                f"twice. Keep as is: 0. (Net of the people already on PO HC and CO HC; not the model totals.)")
    if r[2] == "I-28":
        r[1] = "One person probably costed in both FO and FE"
        r[3] = ("Probably costed twice (name match only; title and salary differ; likely FO->FE move): one of the 14 current techs in Fld Ops Payroll and Fld Eng "
                "Budget row 15.")
        r[4] = (f"Remove from FO (B11 {B11:.0f} -> {B11 - 1:.0f}): +{FO_EFF:,.0f} (payroll +{v1['fo_payroll']:,.0f}, 5330 +{v1['knock_on']:,.0f}). Remove from FE (row 15): "
                f"+{FE_EFF:,.0f}. Pro rata if the move happens mid-year.")
    if r[2] == "I-34":
        r[4] = rep(r[4], "Keep: 0.", f"Keep: 0. Caveat: the HC T&B tax rates are below the {pct(FICA, 2)} employer FICA and unverified (I-37); with the FE tax rate at "
                   f"{pct(FICA, 2)}: +{o6['i34_if_tax_at_fica']:,.0f}.")
    DEC.append(r)

# ------------------------------------------------------------------ issue rows
iss6 = [s for s in cn6["sections"] if s["heading"].startswith("Issues (v6)")][0]
rows = collections.OrderedDict((r[0], list(r)) for r in iss6["table"]["rows"])
md_rows6 = collections.OrderedDict()
sec6 = collections.OrderedDict()
parts = re.split(r"(?m)^## ", md6)
for p in parts[1:]:
    t, _, b = p.partition("\n")
    sec6[t.strip()] = b
EXP = ["Decisions pending", "Headline: 2027 COO contribution", "Changes from v5", "Payroll reconciliation", "HC tabs added to the workbook",
       "Head of Service Delivery salary (I-26, resolved in v5)", "Build and sources", "Completion criteria (v6)", "Depreciation schedule summary",
       "Unit-cost reconciliation", "Revenue", "Assumptions register", "DeploySum refresh and tie-out (v3 build; unchanged in v4-v6)", "v5 -> v6 diff",
       "Error scan", "Package", "Sheets in the output", "Severity scale", "Issues (v6)",
       "Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; unchanged in v6)", "Decisions", "Not done / limits"]
assert list(sec6) == EXP, list(sec6)
for l in sec6["Issues (v6)"].split("\n"):
    if l.startswith("| I-"):
        md_rows6[l.split("|")[1].strip()] = l
assert list(md_rows6) == list(rows)
CHANGED = ("I-05", "I-17", "I-23", "I-28", "I-34", "I-36")
for k in CHANGED:
    assert md_rows6[k] == md_issue(rows[k]), ("md and Collation Notes issue rows differ", k)
r = rows["I-05"]
r[3] += (f" v7 (B1, Decision #1): the net increment assumes the ramp is EXPENSED. DeploySum labels the unit costs 'Unit cost (CapEx)' "
         f"({ev['deploysum_unit_cost_cell']}), and 2026 has credits that fit capitalised labour (PO 6000 {f0(ev['po_6000_2026'])}, PE 5140 {f0(ev['pe_5140_2026'])}; I-23). "
         f"If production labour is capitalised, 2027 carries only its depreciation: ({d9:,.0f}) at the 9-overlap, ({d7:,.0f}) at the 7-overlap, or 0 if the "
         f"65,000 / 8,000 unit cost already includes it. v7 (B2): the 9 are a count match; by role only {b2['n_prod']} PO HC people are production staff (the other "
         f"{b2['n_mh']} are material handling, tied to Logistics&WH: r20 = MH-01 by name, r16 backfilled by MH-02). At {b2['n_prod']} of 9 the net increment is "
         f"{f0(I05_7)} (+{b2['extra']['central']:,.0f} for {b2['n_extra']:.0f} model seats at the model's average current cost).")
r[4] += (f" 2026 base: COO 5100 {f0(ev['coo_5100_2026'])} (PO {f0(ev['dept_5100_2026']['PO'])}, PE {f0(ev['dept_5100_2026']['PE'])}); 2027 budget {f0(ev['coo_5100_2027'])} "
         f"({ev['ratio_budget_vs_2026']:.1f}x); with the ramp expensed {f0(ev['coo_5100_2027_with_ramp'])} ({ev['ratio_ramp_vs_2026']:.1f}x). 2026 7200 Contractors "
         f"{f0(ev['coo_7200_2026'])} sits in FO ({f0(ev['dept_7200_2026']['FO'])}) and FE ({f0(ev['dept_7200_2026']['FE'])}), PO {f0(ev['dept_7200_2026']['PO'])}. "
         f"Sensitivity (O1): at PO HC burden rates the 9-overlap ramp is {f0(o1['I05_at_po_rates'])} (+{o1['diff']:,.0f}). The model's {o2['pp_hires_total']:.0f} Sep-Dec 26 "
         f"hires are on no HC roster (I-38).")
r[5] = (f"({I05:,.0f}) expensed at the 9-overlap; ({I05_7:,.0f}) at the 7-overlap; ({d9:,.0f}) to ({d7:,.0f}) if capitalised on top of the unit cost; 0 if inside it")
r[7] = "User / Finance: answer Decision #1 (expensed or capitalised) first. " + r[7]
r = rows["I-17"]
r[3] += (f" v7 (B2): v6's combined I-05 + I-17 ({f0(COMB6)}) took PO HC r20 out twice (inside I-05 by count, inside I-17 as MH-01 by name). Deduplicated: "
         f"{f0(COMB9)} (9-overlap; MH-01 then counts as a new seat, +{b2['mh01_cost']:,.0f}) or {f0(COMB7)} (7-overlap). Logistics&WH seats TL-01 (Dec-26) and MH-02 "
         f"(Oct-26) are dated before the roster file and are not on it (I-38).")
r = rows["I-23"]
r[7] += (" v7: the PO 6610 and PE 5140 credits are also evidence for Decision #1 (production labour capitalised, B1); Finance's answer settles both.")
r = rows["I-28"]
r[3] = rep(r[3], "One person is costed twice in the budget:", "One person is probably costed twice in the budget (name match only; title and salary differ; likely "
           "FO->FE move):")
r[4] = rep(r[4], f"FO side: one current tech at model rates {V6_FO:,.0f} (salary {f2(fofe['fo_model_one_tech_sal_2027'])}).",
           f"FO side, recalculated with Fld Ops Payroll B11 {B11:.0f} -> {B11 - 1:.0f} (v7): +{FO_EFF:,.0f} = payroll {v1['fo_payroll']:,.0f} (one current tech at model rates, "
           f"salary {f2(fofe['fo_model_one_tech_sal_2027'])}) + {v1['knock_on']:,.0f} on 5330 (Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11); supervisor headcount "
           f"unchanged in every month. v6 stated {V6_FO:,.0f} (payroll only).")
r[7] = rep(r[7], "No budget value changed in v6.", "No budget value changed in v6 or v7.")
r[5] = rep(r[5], f"+{V6_FO:,.0f} to +{FE_EFF:,.0f} (budget overstated by one person)",
           f"+{FO_EFF:,.0f} to +{FE_EFF:,.0f} (budget overstated by one person if the duplicate is confirmed; pro rata if the move happens mid-year)")
r = rows["I-34"]
r[3] += (f" v7 (O6): every HC T&B tax rate ({pct(min(d['hc_rate'] for d in o6['depts'].values()), 2)}-{pct(max(d['hc_rate'] for d in o6['depts'].values()), 2)}) is below "
         f"the {pct(FICA, 2)} employer FICA, so the T&B rates are unverified (I-37); the 6630 part of the upside may not exist.")
r[5] = rep(r[5], f"+{fe_b['diff_total']:,.0f} if the FE HC rates are right",
           f"+{fe_b['diff_total']:,.0f} if the FE HC rates are right; +{o6['i34_if_tax_at_fica']:,.0f} if the FE tax rate is at least {pct(FICA, 2)}")
r = rows["I-36"]
r[3] = rep(r[3], "Start months differ for every matched person (HC Sep-26, or Dec-26 for the Field Engineer Manager; Fld Eng Budget Jan-27), with no 2027 effect.",
           "Start months differ for every matched person (HC Sep-26; Fld Eng Budget Jan-27), with no 2027 effect. v7: the Field Engineer Manager row (FE HC r35, "
           "Dec-26) is an open seat, not a person (I-39).")
rows["I-37"] = ["I-37", "MED", "'HC-FO'!D6; 'HC-PO'!D6; 'HC-CO'!D6; 'HC-FE'!D6; 'HC-PE'!D6; PO!AG34; CO!AG68; PE!AG68; Fld Ops Payroll!B7; Fld Eng Budget!B22",
                f"The HC T&B employer payroll tax rates (A-30, stored values) are all below the {pct(FICA, 2)} employer FICA (6.2% Social Security + 1.45% Medicare): "
                + ", ".join(f"{d} {pct(o6['depts'][d]['hc_rate'], 3)}" for d in ("FO", "PO", "CO", "FE", "PE"))
                + f". A rate below {pct(FICA, 2)} is possible only if salaries above the Social Security wage base pull the average down, and the rates would normally also "
                f"carry unemployment taxes. They are unverified. PO, CO and PE payroll tax in the budget uses these rates, so it may be under-budgeted; FO and FE use the "
                f"SD rate {pct(o6['sd_rate'])}, also below {pct(FICA, 2)}. FE's I-34 upside rests on the FE rate.",
                f"At {pct(FICA, 2)} on every 2027 salary dollar (upper bound): PO +{o6['depts']['PO']['gap_at_fica_on_hc_salary']:,.0f}, CO "
                f"+{o6['depts']['CO']['gap_at_fica_on_hc_salary']:,.0f}, PE +{o6['depts']['PE']['gap_at_fica_on_hc_salary']:,.0f} = +{o6['po_co_pe_gap']:,.0f} of tax; FO "
                f"+{o6['fo_gap_at_fica']:,.0f} and FE +{o6['fe_gap_at_fica']:,.0f} against the SD {pct(o6['sd_rate'])}. I-34 at an FE tax rate of {pct(FICA, 2)}: "
                f"+{o6['i34_if_tax_at_fica']:,.0f} instead of +{fe_b['diff_total']:,.0f}.",
                f"up to ({o6['po_co_pe_gap']:,.0f}) PO/CO/PE; up to ({o6_ff:,.0f}) FO/FE", f"impact {o6['po_co_pe_gap']:,.0f} ($50k-250k)",
                "Finance: confirm what the T&B tax rates include (FICA, FUTA/SUTA, wage-base caps) and the rate to budget per department. Then reset 'HC-*'!D6 and, if "
                "needed, Fld Ops Payroll!B7 / Fld Eng Budget!B22."]
hires = o2["pp_hires_by_month"]
hires_txt = "; ".join(f"{m}: " + ", ".join(f"{hires[k][i]:.0f} {k}" for k in ("lift", "tray", "sup") if hires[k][i]) for i, m in enumerate(o2["months"])
                      if any(hires[k][i] for k in hires))
rows["I-38"] = ["I-38", "MED", "Prod Payroll!B31:E31, B52:E52, B71:E71; Logistics&WH Payroll (SD, not carried) TL-01, MH-02; 'HC-PO'",
                f"The SD payroll models hire people before 2027 that the HC rosters do not show: Prod Payroll {o2['pp_hires_total']:.0f} ({hires_txt}) and Logistics&WH "
                + ", ".join(f"{s} ({m})" for s, m in o2["lw_2026_seats"]) + f". None of them is on an HC roster; the workfile was last saved {o2['workfile_modified']}, "
                f"so at least the Sep-26 hires should be on it if they happened. The models may be older than the roster.",
                f"Workfile saved {o2['workfile_modified']} (file properties); the SD book's properties show {o2['sd_modified']} (a re-save, not the model date). The models' "
                f"Sep-Dec 26 hires set the 2027 opening ramp (Prod Payroll: {pp['ramp_hc_by_month'][0]:.0f} ramp staff in Jan-27).",
                "not determinable", "impact not determinable; owner confirmation needed",
                "SD / PO owners: when were Prod Payroll and Logistics&WH Payroll last updated? Were the Sep-Dec 26 hires made, deferred or dropped? Refresh the models "
                "before Decision #6."]
rows["I-39"] = ["I-39", "MED", "'HC-FE'!B34:F35; Fld Eng Budget!A20:C20, row 66; FE!AG67",
                f"FE HC r35 Field Engineer Manager sits under 'Open Positions' (HC-FE row {o5['section_row']}) with no employee: it is an open seat, not a person (v6 called it a "
                f"matched person). The match with {o5['sd_row']} is seat-to-seat on title + salary with the start month relaxed (A-29 amended). The sources disagree on "
                f"whether the seat is filled: the COO book _2 leaves it out (FE 6610 = FE HC less r35), FE HC starts it in {o5['hc_start']}, Fld Eng Budget costs it from "
                f"{o5['sd_start']}.",
                f"2027 cost in the budget (salary + SD burden): {f0(o5['sd_cost_2027'])}; COO book _2 gap vs FE HC: {f0(o5['coo_book_gap'])} of salary.",
                f"up to +{o5['sd_cost_2027']:,.0f} if the seat stays open all of 2027", f"impact {o5['sd_cost_2027']:,.0f} ($50k-250k)",
                "FE owner: is the Field Engineer Manager seat filled, and from when? Set Fld Eng Budget!C20 to the start month."]
ISS_NEW = ("I-37", "I-38", "I-39")
sev = collections.Counter(r[1] for r in rows.values())

# ------------------------------------------------------------------ assumptions
ASR_A29_ADD = (". v7: start month relaxed for FE HC r35, an open seat ('Open Positions', no employee), matched seat-to-seat with Fld Eng Budget r20 "
               f"(HC {o5['hc_start']}, SD {o5['sd_start']}; I-39).")
ASR_NEW = [
    ["A-31", f"Employer FICA reference rate {pct(FICA, 2)} (6.2% Social Security + 1.45% Medicare), used only to test the HC T&B tax rates (I-37)",
     f"PO/CO/PE gap up to {f0(o6['po_co_pe_gap'])}; FO/FE up to {f0(o6_ff)}", "figures_v7.py", "statutory rates; wage base not modelled (upper bound)"],
    ["A-32", "Capitalised case (Decision #1): ramp split to lifts and trays from the model (lift / tray ramp = model total less its current-staff cost); supervisors "
     "allocated pro rata to the lift : tray ramp cost", f"lift {f0(cap['alloc']['lift'])}, tray {f0(cap['alloc']['tray'])} (supervisors {pct(cap['sup_share_to_lift'])} to lifts); "
     f"check with the model-total split: depreciation {f0(cap['d9_fallback']['dep'])} vs {f0(d9)}", "Prod Payroll rows 41, 62, 79", "builder assumption (v7, handoff fallback shown)"],
    ["A-33", "Capitalised case: 2027 ramp labour spread evenly over the units built in 2027; units go live "
     f"{cap['build_lag_months']} months after build; depreciation per the Depreciation Schedule (full month from go-live, {ev['lift_life']:.0f} / {ev['tray_life']:.0f} months); "
     "units built Nov-Dec 27 (2028 go-lives) carry labour but no 2027 depreciation",
     f"units built {cap['units_built_2027']['lift']:.0f} lifts / {cap['units_built_2027']['tray']:.0f} trays; live in 2027 {cap['units_live_2027_built_2027']['lift']:.0f} / "
     f"{cap['units_live_2027_built_2027']['tray']:.0f}; depreciation {f0(d9)} (9) / {f0(d7)} (7)", "DeploySum rows 19-20, 24-25, 33-34; 'Depreciation Schedule' rows 38-62",
     "builder assumption (v7); lag checked on the DeploySum rows (DeploySum note 1)"],
    ["A-34", f"7-overlap reading (B2): the {b2['n_extra']:.0f} Prod Payroll current seats no PO HC production person fills are costed at the model's average current cost per head; "
     "capitalised case keeps the 9-overlap lift / tray mix", f"+{b2['extra']['central']:,.0f} ({b2['extra']['low']:,.0f} to {b2['extra']['high']:,.0f} as tray or lift seats)",
     "Prod Payroll B9, C9, H10; 'HC-PO'!C14:C22", "builder assumption (v7)"],
    ["A-35", "md privacy: per-person amounts for identified employees rounded to the nearest $5k ('~'); Collation Notes keeps exact figures (restricted workbook)",
     "md only", "paylist_v7.py", "critic v6 O8 / handoff"],
]

# ------------------------------------------------------------------ v7 analysis tables (md and Collation Notes)
B1_ROWS = [
    ["DeploySum unit-cost label", f"'{ev['deploysum_unit_cost_text']}'", f"DeploySum!{ev['deploysum_unit_cost_cell']}"],
    ["PO 6000 Labour - SG&A, 2026", f"{f0(ev['po_6000_2026'])} (6610 {f0(ev['po_6610_2026'])}: " + ", ".join(f"{m} {f0(v)}" for m, v in ev["po_6610_neg_months"]) + ")", "PO!N67, N73; B67:M67"],
    ["PE 5140 Benefits - Production, 2026", f"{f0(ev['pe_5140_2026'])} (" + ", ".join(f"{m} {f0(v)}" for m, v in ev["pe_5140_neg_months"]) + ")", "PE!N35; B35:M35"],
    ["COO 5100 Labour - Production: 2026 / 2027 budget / 2027 with the ramp expensed",
     f"{f0(ev['coo_5100_2026'])} / {f0(ev['coo_5100_2027'])} ({ev['ratio_budget_vs_2026']:.1f}x) / {f0(ev['coo_5100_2027_with_ramp'])} ({ev['ratio_ramp_vs_2026']:.1f}x)",
     "COO P&L!N36, AG36; + I-05 net"],
    ["7200 Contractors, 2026 (2027 budget)", f"{f0(ev['coo_7200_2026'])} ({f0(ev['coo_7200_2027'])}): FO {f0(ev['dept_7200_2026']['FO'])}, FE {f0(ev['dept_7200_2026']['FE'])}, "
     f"PO {f0(ev['dept_7200_2026']['PO'])}", "COO P&L!N91; FO!N91; FE!N91; PO!N91"],
    ["Ramp by model (9-overlap)", f"lift {f0(cap['ramp_by_model']['lift'])}, tray {f0(cap['ramp_by_model']['tray'])}, supervisors {f0(cap['ramp_by_model']['sup'])} = {f0(I05)}",
     "Prod Payroll rows 41, 62, 79 less current staff"],
    ["Allocated to units (A-32)", f"lifts {f0(cap['alloc']['lift'])} / {cap['units_built_2027']['lift']:.0f} built = {cap['d9']['labour_per_lift']:,.0f} per lift "
     f"({pct(cap['d9']['labour_pct_of_lift_cost'])} of {ev['lift_unit_cost']:,.0f}); trays {f0(cap['alloc']['tray'])} / {cap['units_built_2027']['tray']:,.0f} = "
     f"{cap['d9']['labour_per_tray']:,.0f} per tray ({pct(cap['d9']['labour_pct_of_tray_cost'])} of {ev['tray_unit_cost']:,.0f})", "DeploySum!R24:R25"],
    ["2027 depreciation of capitalised ramp (9 / 7-overlap)", f"{f0(d9)} (lifts {f0(cap['d9']['dep_lift'])}, trays {f0(cap['d9']['dep_tray'])}) / {f0(d7)}",
     f"go-live vintages {cap['vintages_built_in_2027'][0]}-{cap['vintages_built_in_2027'][-1]} of 2027 ('Depreciation Schedule' rows 40-49, 53-62)"],
    ["Model-total split check (handoff fallback)", f"lift share {pct(pp['lift_total'] / (pp['lift_total'] + pp['tray_total']))}: depreciation {f0(cap['d9_fallback']['dep'])}",
     "Prod Payroll S41, S62, S79"],
    ["On the balance sheet at Dec-27 (9-overlap)", f0(cap["d9"]["on_balance_sheet_end27"]), "capitalised less 2027 depreciation"],
]
CONTRIB_ROWS = [
    ["Budget as built (ramp not in the budget)", f0(C), f0(C), "-"],
    ["Ramp expensed", f0(ct["expensed_9"]), f0(ct["expensed_7"]), f"I-05 ({I05:,.0f}) / ({I05_7:,.0f})"],
    ["Ramp capitalised on top of the 65,000 / 8,000 unit cost (depreciation only)", f0(ct["capitalised_on_top_9"]), f0(ct["capitalised_on_top_7"]), f"({d9:,.0f}) / ({d7:,.0f})"],
    ["Ramp capitalised, already inside the unit cost", f0(ct["capitalised_in_unit_cost"]), f0(ct["capitalised_in_unit_cost"]), "0"],
]
B2_ROWS = [
    ["9 of 9 by count (v6)", f"all 9 PO HC people = Prod Payroll's 9 current staff (7 lift + 2 tray, no names in the model)", f0(I05), f0(I17),
     f"{f0(COMB6)} as shipped in v6: PO HC r20 taken out twice (in I-05 by count, in I-17 as MH-01 by name). Deduplicated, MH-01 counts as a new seat: {f0(COMB9)}"],
    [f"{b2['n_prod']} of 9 by role (critic B2)", f"the {b2['n_prod']} production staff ({', '.join(f'{n} {t}' for t, n in hc['PO']['titles'].items() if t not in b2['mh_titles'])}) "
     f"are Prod Payroll current staff; r20 Material Handler = MH-01 (name) and r16 Material Handling Team Lead (backfilled by MH-02) belong with Logistics&WH",
     f"{f0(I05_7)} (+{b2['extra']['central']:,.0f}: {b2['n_extra']:.0f} model seats at {b2['per_head']['avg']:,.0f} each)", f0(I17), f"{f0(COMB7)} (no seat taken out twice)"],
]
O_ROWS = [
    ["O1", "I-05 at PO HC burden rates", f"PO HC {pct(o1['po_rate_pct'])} of salary vs the model's {pct(o1['model_burden_pct_of_sal'])}: +{o1['diff']:,.0f}; ramp "
     f"{f0(o1['I05_at_po_rates'])} (9-overlap)", "'HC-PO'!D6:D7; Prod Payroll B6:C7, H6:H7"],
    ["O2", "SD models may be older than the roster", f"Prod Payroll Sep-Dec 26 hires {o2['pp_hires_total']:.0f} ({hires_txt}); Logistics&WH "
     + ", ".join(f"{s} {m}" for s, m in o2["lw_2026_seats"]) + f"; none on the HC rosters (workfile saved {o2['workfile_modified']}). Question: when were the models last updated? (I-38)",
     "Prod Payroll rows 31, 52, 71; HC tabs"],
    ["O3", "FO/FE person", "Probable duplicate (name match only; title/salary differ; likely FO->FE move); upside pro rata to the months after the move "
     f"(about {v1['fo_per_month_avg']:,.0f} per month on the FO side)", "I-28; Decision #7"],
    ["O4 / V1", "I-28 FO side with knock-ons", f"Fld Ops Payroll B11 {B11:.0f} -> {B11 - 1:.0f}, LibreOffice recalculation: +{FO_EFF:,.2f} = payroll +{v1['fo_payroll']:,.2f} + 5330 "
     f"+{v1['knock_on']:,.2f} (Fld Maint Budget!B29); supervisor headcount unchanged ({v1['sup_hc_unchanged']}); after {f0(v1['after'])} (v6: +{V6_FO:,.0f}, {f0(v1['v6_after'])})",
     "scen_v7.py; COO P&L!AG46, AG52:AG54"],
    ["O5", "FE HC r35 is an open seat", f"'Open Positions' (HC-FE row {o5['section_row']}), no employee; A-29 amended (start relaxed); _2 excludes it, SD costs it from "
     f"{o5['sd_start']}: up to +{o5['sd_cost_2027']:,.0f} (I-39)", "'HC-FE'!B34:F35; Fld Eng Budget r20"],
    ["O6", "HC T&B tax rates below FICA", f"all five below {pct(FICA, 2)} ({pct(min(d['hc_rate'] for d in o6['depts'].values()), 2)}-"
     f"{pct(max(d['hc_rate'] for d in o6['depts'].values()), 2)}); PO/CO/PE up to ({o6['po_co_pe_gap']:,.0f}); I-34 +{o6['i34_if_tax_at_fica']:,.0f} if FE tax at "
     f"{pct(FICA, 2)} (I-37)", "'HC-*'!D6"],
    ["O7", "Range asymmetry", f"lower bound 1 {f0(LB1)} (9-overlap {f0(LB1_9)}); lower bound 2 (excl. I-05) {f0(LB2)}; I-05 capitalised on top {f0(LBC)}; upper {f0(UB)}",
     "Sign-flip statement"],
    ["O8", "Privacy", "CONFIDENTIAL banner (md and Collation Notes); per-person amounts rounded to $5k in the md (A-35); no per-person CSV written in v7; scratch name lists deleted",
     "md; Collation Notes; run_build_v7.sh"],
]
CHG = [
    ["Budget values", "Unchanged", "Collation Notes regenerated; every other part of the v6 workbook copied byte for byte; 0 formula and 0 value differences vs v6 on every "
     "other sheet.", "v6 -> v7 diff"],
    ["B1", "Capitalisation not tested", f"Decision #1 added (expensed or capitalised into the 65,000 / 8,000 unit cost?), with the 2026 evidence and the contribution under "
     f"each treatment: expensed {f0(C - I05)} / {f0(C - I05_7)}; capitalised on top {f0(C - d9)} / {f0(C - d7)}; inside the unit cost {f0(C)}.",
     "Decisions pending #1; 'Production labour' section; caveat table; I-05"],
    ["B2", "Overlap 9 by count vs 7 by role", f"Both readings shown; I-05 at 7 of 9: {f0(I05_7)}. v6's combined {f0(COMB6)} took PO HC r20 out twice; deduplicated "
     f"{f0(COMB9)} (9) / {f0(COMB7)} (7). The v6 wording that no overlap was left between the two models is removed.", "'Prod Payroll overlap' section; caveat table; I-05, I-17; Decision #6"],
    ["B3", "Ramp asymmetry not headlined", f"Headline caveat: FO ramp {f0(b3['fo_ramp'])} in the budget, PO ramp {f0(I05)} not, same deployment plan; read with Decision #1.",
     "Headline"],
    ["V1", "I-28 FO side", f"+{V6_FO:,.0f} -> +{FO_EFF:,.0f} (Fld Maint Budget!B29 also reads Fld Ops Payroll!B11); after {f0(v1['v6_after'])} -> {f0(v1['after'])}. Fixed in "
     f"every place.", "Decision #7; caveat table; I-28; sign-flip"],
    ["O1", "PO burden sensitivity", f"+{o1['diff']:,.0f} on I-05 at PO HC rates.", "caveat table; I-05"],
    ["O2", "Stale model hires", "Question on the model date; new I-38.", "I-38"],
    ["O3", "Duplicate wording", "'Probable duplicate (name match only; title/salary differ; likely FO->FE move)'; pro rata note.", "I-28; Decision #7; duplicate scan"],
    ["O4", "FO knock-ons", "Recomputed by recalculation (V1): 5330 +331; supervisor ratio unchanged.", "I-28"],
    ["O5", "FE HC r35 open seat", "A-29 amended; new I-39 (sources disagree on whether the seat is filled).", "A-29; I-39; FE section"],
    ["O6", "T&B rates below FICA", f"I-34 caveated (+{o6['i34_if_tax_at_fica']:,.0f} at {pct(FICA, 2)}); new I-37 for PO/CO/PE under-budget risk (up to {f0(o6['po_co_pe_gap'])}).",
     "I-34; I-37; HC tabs section"],
    ["O7", "Asymmetric range", f"Stated; second lower bound excluding I-05: {f0(LB2)}.", "Sign-flip statement"],
    ["O8", "Privacy", "Banner on the md and Collation Notes; per-person amounts rounded to $5k in the md; scratch name lists deleted after the build.", "top of md; Collation Notes"],
]

# ------------------------------------------------------------------ Collation Notes JSON (from v6)
cn = copy.deepcopy(cn6)
cn["title"] = rep(cn["title"], "build v6", "build v7")
cn["sections"].insert(0, {"heading": BANNER, "style": "highlight",
                          "lines": ["This workbook holds employee names and salaries on the HC-* tabs (copied from the COO HC & PL workfile). Share it only with people "
                                    "cleared to see compensation. The notes file (02-build_notes_v7.md) rounds per-person amounts to $5k; this sheet keeps exact figures."]})
dp = cn["sections"][1]
dp["table"]["rows"] = DEC
hl = cn["sections"][2]; assert hl["heading"].startswith("Headline")
hl["table"]["header"][-1] = "2027 in v6 (value)"
cvs = cn["sections"][3]; assert cvs["heading"].startswith("Caveats")
B3_LINE = (f"(0) Headline caveat (B3, read with Decision #1): the FO ramp ({f0(b3['fo_ramp'])} of ramp hires on Fld Ops Payroll) is in the budget; the PO production "
           f"ramp ({f0(I05)} net; {f0(I05_7)} at the 7-overlap) is not. Both come from the same 9/30/26 deployment plan (Fld Ops Payroll reads DeploySum rows "
           f"{', '.join(k for k in b3['deploysum_links']['Fld Ops Payroll'] if k != '53')}; Prod Payroll reads rows "
           f"{', '.join(k for k in b3['deploysum_links']['Prod Payroll'] if k != '4')}). If production labour is expensed, the budget is not internally consistent and the "
           f"like-for-like contribution is {f0(C - I05)} to {f0(C - I05_7)}. If it is capitalised, 2027 carries only depreciation ({f0(C - d9)} to {f0(C - d7)}), or nothing "
           f"if the unit cost already includes it ({f0(C)}).")
assert cvs["lines"][2].startswith("(3) Open exposures")
cvs["lines"] = [B3_LINE] + cvs["lines"][:2] + [
    "(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. I-05 is shown expensed and capitalised (Decision #1) and "
    "at both overlap readings (9 by count, 7 by role); the I-05 + I-17 rows are deduplicated (v6's combined row took PO HC r20 out twice)."]
cvs["table"]["rows"] = [[r[0], r[1], r[2], round(r[3], 2) if isinstance(r[3], float) else r[3], round(r[4], 2) if isinstance(r[4], float) else r[4], r[5]] for r in cav]
cvs["table"]["after"] = []
cvs["after"] = sf
src = [s for s in cn["sections"] if s["heading"] == "Source and build"][0]
src["lines"] = [f"Base: v6 collated workbook. v7 regenerates this sheet only (notes and presentation fixes for critic v6 B1-B3, O1-O8 and verifier v6 V1); every other "
                f"part of the v6 file is copied byte for byte, so every other sheet has 0 formula and 0 value differences vs v6. No budget value changed.",
                "Full notes: 02-build/02-build_notes_v7.md. New figures: figures_v7.py (B1, B2, O1, O2, O5, O6) and scen_v7.py (I-28 FO side by recalculation); numbers "
                "on this sheet are live formulas (headline) or values computed by those scripts, recon_v6.py and report_v7.py."]
chg = [s for s in cn["sections"] if s["heading"] == "Changes from v5"][0]
chg["heading"] = "Changes from v6"
chg["table"] = {"header": ["Item", "Point", "What v7 did", "Where"], "rows": CHG, "after": []}
idx = cn["sections"].index(chg) + 1
cn["sections"][idx:idx] = [
    {"heading": "Decision #1 evidence: production labour expensed or capitalised (B1)", "table": {"header": ["Item", "Value", "Source"], "rows": B1_ROWS, "after": []}},
    {"heading": "2027 COO contribution under each treatment (9-overlap / 7-overlap)",
     "table": {"header": ["Treatment of the production ramp", "9-overlap", "7-overlap", "Effect"], "rows": CONTRIB_ROWS, "after": []}},
    {"heading": "Prod Payroll overlap with PO HC: two readings (B2)",
     "table": {"header": ["Reading", "Who overlaps", "I-05 net", "I-17 net", "I-05 + I-17"], "rows": B2_ROWS, "after": []}},
    {"heading": "Other v7 checks (critic v6 O1-O8, verifier V1)", "table": {"header": ["Item", "Point", "Finding", "Source"], "rows": O_ROWS, "after": []}},
]
rec = [s for s in cn["sections"] if s["heading"].startswith("Payroll reconciliation (v6)")][0]
po_line = [i for i, l in enumerate(rec["lines"]) if l.startswith("PO: PO HC")][0]
rec["lines"][po_line] = rep(rec["lines"][po_line], f"together {f0(COMB6)}.",
                            f"together {f0(COMB6)} as summed in v6, which takes PO HC r20 out twice; deduplicated {f0(COMB9)} (9 of 9 by count) or {f0(COMB7)} "
                            f"(7 of 9 by role; I-05 {f0(I05_7)}), v7 B2.")
dsec = [s for s in cn["sections"] if s["heading"].startswith("Duplicate scan (I-28)")][0]
nprob = 0
for row in dsec["table"]["rows"]:
    if row[3].startswith("DUPLICATE across P&L sources: FO"):
        row[3] = row[3].replace("DUPLICATE across P&L sources:", "PROBABLE DUPLICATE (name match only; title and salary differ; likely FO->FE move) across P&L sources:"); nprob += 1
    if row[0].startswith("FE HC r35"):
        row[3] = "same seat (open position, no employee; start month relaxed, A-29), one P&L source (FE 6610-6640 via Fld Eng Budget)"
assert nprob == 1
asr = [s for s in cn["sections"] if s["heading"] == "Assumptions register"][0]
for row in asr["table"]["rows"]:
    if row[0] == "A-29":
        row[1] += ASR_A29_ADD
asr["table"]["rows"] += ASR_NEW
iss = [s for s in cn["sections"] if s["heading"].startswith("Issues (v6)")][0]
iss["heading"] = iss["heading"].replace("Issues (v6)", "Issues (v7)")
iss["table"]["rows"] = list(rows.values())
cnj = json.dumps(cn, indent=1, ensure_ascii=False)


def v6_fo_left(text):
    """Occurrences of the v6 I-28 FO figure (or its 'after' value) outside the explicit v6 references in 'Changes from v6' / O4."""
    s6, a6 = re.escape(f"{V6_FO:,.0f}"), re.escape(f0(v1["v6_after"]))
    t = re.sub(rf"(v6 stated |v6: \+|payroll \+?){s6}(\.\d\d)?|\+{s6} -> |after {a6} -> |, {a6}\)", "", text)
    return len(re.findall(rf"(?<![\d,])({s6}|{a6})(?![\d]|,\d)", t))


for bad in ("person-level overlap is left", "No person-level overlap"):
    assert bad not in cnj, bad
assert v6_fo_left(cnj) == 0, "an uncorrected v6 I-28 FO figure is left in the Collation Notes"
open(OUT_JSON, "w").write(cnj)

# ------------------------------------------------------------------ md
L = []
A = L.append
A("# 02-build notes v7 - 2027 COO budget collation\n")
A(f"> **{BANNER}.** The workbook's HC-* tabs hold employee names and salaries; share the workbook and these notes only with people cleared to see "
  "compensation. In this file every per-person amount for an identified employee is rounded to the nearest $5k (shown with '~') or aggregated; the "
  "Collation Notes sheet keeps exact figures. A department total compared across versions can still reveal one person's cost.\n")
A("## Decisions pending\n")
A(f"{len(DEC)} user decisions are open. #1 is new in v7 and comes first because it decides how to read I-05 and the headline; v6's #1-#8 are now #2-#9. "
  "The builder has not resolved them; the budget carries the 'current treatment' column. Effects are on the 2027 COO contribution, each on its own.\n")
A(mdtable(dp6["table"]["header"], DEC))
A(f"Evidence for #1 (B1): DeploySum labels the unit costs 'Unit cost (CapEx)' ({ev['deploysum_unit_cost_cell']}). 2026 has credits that fit a capitalised-labour "
  f"credit: PO 6000 Labour - SG&A {f0(ev['po_6000_2026'])} (6610 credits in " + " and ".join(m for m, _ in ev["po_6610_neg_months"]) + f") and PE 5140 "
  f"{f0(ev['pe_5140_2026'])}. COO 5100 production labour was {f0(ev['coo_5100_2026'])} in 2026, against {f0(ev['coo_5100_2027'])} budgeted for 2027 "
  f"({ev['ratio_budget_vs_2026']:.1f}x) and {f0(ev['coo_5100_2027_with_ramp'])} with the ramp expensed ({ev['ratio_ramp_vs_2026']:.1f}x). 2026 7200 Contractors "
  f"({f0(ev['coo_7200_2026'])}) is another possible home for build labour, but it sits in FO and FE, not PO (PO {f0(ev['dept_7200_2026']['PO'])}). Details: "
  "'Production labour: expensed or capitalised'.\n")
# Headline
A("## Headline: 2027 COO contribution\n")
HL = [("Revenue (company recognized revenue, 9/30/26 sales plan)", "16", [16]), ("COGS (COO departments)", "63", [63]),
      ("  of which depreciation (in COGS)", "19-22", [19, 20, 21, 22]), ("Gross Profit", "64", [64]), ("Opex (COO departments)", "116", [116]),
      ("COO contribution before other income (workbook label 'Net Ordinary Income')", "117", [117]), ("Net Other Income", "131", [131]),
      ("**COO contribution** (workbook label 'Net Income')", "132", [132])]


def pct_nm(new, base):
    if base is None or base <= 0 or new < 0:
        return "n/m"
    return f"{(new - base) / base * 100:.0f}%"


A(mdtable(["Line", "COO P&L row", "2026 (N)", "2027 v7 (AG)", "Change", "%", "2027 v6 (AG)", "v7 - v6"],
          [[lab, rr, f0(val("N", rws)), f0(val("AG", rws)), f0(val("AG", rws) - val("N", rws)), pct_nm(val("AG", rws), val("N", rws)), f0(val("AG", rws)), "0"]
           for lab, rr, rws in HL], ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:"]))
A(f"- **2027 COO contribution (COO P&L AG132): {f0(C)}**, unchanged from v6 (v7 changes no budget value). Revenue {f0(val('AG', [16]))} (all to 4100, orchestrator "
  f"assumption); COGS + Opex {f0(val('AG', [63]) + val('AG', [116]))}.")
A(f"- Issues: {sev['HIGH']} HIGH, {sev['MED']} MED, {sev['LOW']} LOW open; {sev['RESOLVED']} RESOLVED. v7 adds I-37, I-38 and I-39 (MED) and rewrites I-05, I-17, "
  f"I-28 and I-34.\n")
A(f"**Headline caveat: the two payroll ramps are treated differently (B3; read with Decision #1).** The FO ramp, {f0(b3['fo_ramp'])} of ramp hires on Fld Ops "
  f"Payroll, is in the budget. The PO production ramp, {f0(I05)} net ({f0(I05_7)} at the 7-overlap), is not. Both are driven by the same 9/30/26 deployment plan: "
  f"Fld Ops Payroll reads DeploySum rows {', '.join(k for k in b3['deploysum_links']['Fld Ops Payroll'] if k != '53')} (deployments by month) and Prod Payroll reads "
  f"rows {', '.join(k for k in b3['deploysum_links']['Prod Payroll'] if k != '4')} (units to build).\n")
A(mdtable(["If production labour is (Decision #1)", "What the asymmetry means", "Like-for-like 2027 COO contribution (9-overlap / 7-overlap)"],
          [["expensed", "The budget is not internally consistent: it pays the field team for the deployments but not the production team that builds the units.",
            f"{f0(C - I05)} / {f0(C - I05_7)}"],
           ["capitalised, on top of the 65,000 / 8,000 unit cost", "Mostly an accounting difference: production labour becomes fleet cost and reaches 2027 only as depreciation; "
            "field labour stays an operating cost.", f"{f0(C - d9)} / {f0(C - d7)}"],
           ["capitalised, already inside the unit cost", "No P&L gap: the ramp is already in the budgeted depreciation; it is a CapEx and cash item.", f"{f0(C)} / {f0(C)}"]]))
hb = sec6["Headline: 2027 COO contribution"]
A(hb[hb.index("### Caveats on the headline"):hb.index("(3) Open exposures")].rstrip() + "\n")
A("(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. I-05 is shown **expensed and capitalised** (Decision #1) and "
  "at **both overlap readings** (9 of 9 by count, 7 of 9 by role); the 'I-05 + I-17' rows are deduplicated (v6's combined row took PO HC r20 out twice).\n")
A(mdtable(["Item", "Direction", "What could happen", "Effect on 2027 COO contribution", "Contribution after this item alone", "Source cells"],
          [cav_md_row(r) for r in cav], ["---", "---", "---", "---:", "---:", "---"]))
A("**" + sf[0].split(":")[0] + ":**" + sf[0].split(":", 1)[1] + " " + " ".join(sf[1:3]) + "\n")
A("**" + sf[3].split(":")[0] + ":**" + sf[3].split(":", 1)[1] + "\n")
A(mdtable(["Bound", "What it adds to the headline", "2027 COO contribution"],
          [["Lower bound 1 (all quantified downsides)", "I-05 expensed + I-17, deduplicated at the 7-overlap; I-10; I-31 shortfall", f0(LB1)],
           ["  same, 9-overlap", "I-05 + I-17 deduplicated at the 9-overlap; I-10; I-31 shortfall", f0(LB1_9)],
           ["  same, I-05 capitalised on top of the unit cost", "I-05 depreciation only (7-overlap); I-17; I-10; I-31 shortfall", f0(LBC)],
           ["Lower bound 2 (excludes I-05)", "I-17; I-10; I-31 shortfall", f0(LB2)],
           ["Point estimate", "-", f0(C)],
           ["Upper end", "I-32 in full only", f0(UB)]], ["---", "---", "---:"]))
A("**" + sf[4].split(":")[0] + ":**" + sf[4].split(":", 1)[1] + "\n")
# Changes from v6
A("## Changes from v6\n")
A(mdtable(["Item", "Point", "What v7 did", "Where"], CHG))
A("Every critic v6 item (B1-B3, O1-O8) and the verifier's one fix (V1) is addressed; none is declined. v6's own changes from v5 are listed in "
  "`02-build_notes_v6.md` and still apply.\n")
# v7 analysis sections
A("## Production labour: expensed or capitalised (B1, Decision #1)\n")
A("The budget's I-05 net increment assumes the production ramp is expensed. The evidence below points the other way in places, so the treatment is a user / "
  "Finance decision. The builder has not chosen.\n")
A(mdtable(["Item", "Value", "Source"], B1_ROWS))
A("**2027 COO contribution under each treatment**\n")
A(mdtable(["Treatment of the production ramp", "9-overlap", "7-overlap", "Effect"], CONTRIB_ROWS, ["---", "---:", "---:", "---"]))
A(f"Method for the capitalised case (A-32, A-33): the 2027 ramp is split into lifts and trays from the model itself (lift and tray ramp = model total less the "
  f"model's cost of the current staff); supervisors, who serve both lines, are allocated pro rata to the lift : tray ramp ({pct(cap['sup_share_to_lift'])} to lifts). "
  f"Each line's labour is spread evenly over the units built in 2027 (DeploySum R24:R25), and those units go live {cap['build_lag_months']} months after the "
  f"build (DeploySum note 1, checked on rows 19-20 vs 24-25). Depreciation then follows the Depreciation Schedule unchanged: full month from the go-live month "
  f"(B13 = {ev['dep_start_offset']:.0f}), lifts {ev['lift_life']:.0f} months, trays {ev['tray_life']:.0f} months, no salvage. Only the go-lives of "
  f"{MON[cap['vintages_built_in_2027'][0] - 1]}-{MON[cap['vintages_built_in_2027'][-1] - 1]} 27 "
  f"are built in 2027 ({cap['units_live_2027_built_2027']['lift']:.0f} lifts, {cap['units_live_2027_built_2027']['tray']:.0f} trays); the "
  f"{cap['units_built_2027_live_2028']['lift']:.0f} lifts and {cap['units_built_2027_live_2028']['tray']:.0f} trays built for 2028 go-lives carry labour but no 2027 "
  f"depreciation, and the Jan-Feb 27 go-lives were built with 2026 labour. The handoff's fallback split (model totals: lift {f0(pp['lift_total'])} / tray "
  f"{f0(pp['tray_total'])}, supervisors pro rata) gives {f0(cap['d9_fallback']['dep'])}, within {abs(cap['d9_fallback']['dep'] - d9):,.0f} of the derived figure. "
  f"Not quantified: whether the {f0(po['po_5100'])} already in PO 5110-5140 would also be capitalised under the same policy (it would raise the budget's contribution "
  f"by most of that amount).\n")
A("## Prod Payroll overlap: 9 by count vs 7 by role (B2)\n")
A(f"Prod Payroll has no names or titles. Its 'current staff on payroll (Sep-26)' is {pp['inputs']['B9']:.0f} lift + {pp['inputs']['C9']:.0f} tray = "
  f"{pp['current_hc']:.0f}, which equals the PO HC headcount. But PO HC's 9 are {b2['n_prod']} production staff and {b2['n_mh']} material-handling roles "
  f"({', '.join(f'{n} {t}' for t, n in b2['mh_titles'].items())}). Both material-handling roles are tied to the Logistics&WH model: PO HC r20 is seat MH-01 by "
  f"name, and seat MH-02 backfills PO HC r16. v6 used the count match only.\n")
A(mdtable(["Reading", "Who overlaps", "I-05 net", "I-17 net", "I-05 + I-17"], B2_ROWS, ["---", "---", "---:", "---:", "---"]))
A(f"**Which seats v6 subtracted twice.** v6's combined {f0(COMB6)} is I-05 + I-17 as computed separately. I-05 takes all 9 PO HC people out of Prod Payroll by count, "
  f"PO HC r20 included. I-17 takes PO HC r20 out of Logistics&WH again, as seat MH-01 by name, so one person is subtracted twice. One person fills one seat. Keeping "
  f"the count match (9 reading), MH-01 is an unfilled seat and comes back into I-17: {f0(COMB9)} (+{b2['mh01_cost']:,.0f}). On the 7 reading, r20 is MH-01 and r16 sits with "
  f"Logistics&WH, so Prod Payroll's 9 current seats hold the 7 production staff plus {b2['n_extra']:.0f} seats no roster fills. Those 2 seats are costed at the "
  f"model's average current cost per head ({b2['per_head']['avg']:,.0f}; {b2['per_head']['lift']:,.0f} lift, {b2['per_head']['tray']:,.0f} tray; A-34): I-05 "
  f"{f0(I05_7)} and combined {f0(COMB7)}, with nothing subtracted twice. PO HC r16 itself stays budgeted in PO all of 2027 under both readings (I-17: if r16 leaves "
  f"the role MH-02 backfills, PO HC is overstated).\n")
A("## Other v7 checks (critic v6 O1-O8, verifier V1)\n")
A(mdtable(["Item", "Point", "Finding", "Source"], O_ROWS))
A(mdtable(["Dept", "HC T&B tax rate", "Below 7.65%?", "Rate used in the budget", "2027 tax gap at 7.65% (upper bound)"],
          [[d, pct(o6["depts"][d]["hc_rate"], 3), "yes" if o6["depts"][d]["below_fica"] else "no",
            "HC rate" if d in o6["budget_uses_hc_rate"] else f"SD {pct(o6['sd_rate'])}",
            f0(o6["depts"][d]["gap_at_fica_on_hc_salary"]) if d in o6["budget_uses_hc_rate"] else f0(o6["fo_gap_at_fica"] if d == "FO" else o6["fe_gap_at_fica"])]
           for d in ("FO", "PO", "CO", "FE", "PE")], ["---", "---:", "---", "---", "---:"]))
A(f"The tax-gap column is the 2027 salary base times (7.65% less the rate used); PO, CO and PE on the HC salaries ({f0(o6['po_co_pe_gap'])} together), FO and FE on the "
  "SD salary base. It ignores the Social Security wage base, which lowers the true rate for salaries above it, so it is an upper bound (I-37, A-31).\n")
# carried sections, edited
pr = sec6["Payroll reconciliation"]
pr = rep(pr, "names were used only inside recon_v6.py to match people.", "names were used only inside recon_v6.py to match people. v7: per-person amounts are "
         "rounded to the nearest $5k in this file (A-35).")
pr = rep(pr, f"9 of 9 in Prod Payroll (count); r20 = Logistics&WH MH-01 (name); r16 backfilled by MH-02 | {f0(COMB6)} (I-05 {f0(I05)}, I-17 {f0(I17)}) |",
         f"9 of 9 in Prod Payroll by count, or {b2['n_prod']} of 9 by role (B2); r20 = Logistics&WH MH-01 (name); r16 backfilled by MH-02 | {f0(COMB9)} (9, deduplicated) "
         f"or {f0(COMB7)} (7); v6 summed {f0(COMB6)}, which takes r20 out twice |")
pr = rep(pr, f"7 of 7 matched ({sum(1 for e in fe['rows'] if e['basis'] == 'name')} name, 1 title + salary)",
         f"7 of 7 matched ({sum(1 for e in fe['rows'] if e['basis'] == 'name')} people by name, 1 open seat r35 by title + salary)")
named = fo["match"]["named"]
pr = rep(pr, f"The coordinator and manager match to the dollar ({f2(named[0]['sd_2027'])} and {f2(named[1]['sd_2027'])}).",
         f"The coordinator and manager match to the dollar (2 people, combined 2027 salary {f2(named[0]['sd_2027'] + named[1]['sd_2027'])}, differences "
         f"{f2(named[0]['diff_2027'])} and {f2(named[1]['diff_2027'])}).")
pr = rep(pr, "If the 9 are Prod Payroll's current staff, PO HC r20 sits in both SD models; the net increments below take each person out once.",
         "If the 9 are Prod Payroll's current staff, PO HC r20 sits in both SD models, and the 'Both models' column below, as summed in v6, takes r20 out twice "
         "(inside I-05 by count, inside I-17 as MH-01). See 'Prod Payroll overlap: 9 by count vs 7 by role' for the two readings and the deduplicated figures (B2).")
pr = rep(pr, f"7 seats | **{f0(COMB6)}** |\n", f"7 seats | **{f0(COMB6)}** (r20 out twice; deduplicated {f0(COMB9)} / {f0(COMB7)}, B2) |\n")
pr = rep(pr, f"| **{f0(COMB6)}** |\n", f"| **{f0(COMB6)}** (9 reading as summed in v6; see B2) |\n")
pr = rep(pr, f"so 2027 opens with {pp['ramp_hc_by_month'][0]:.0f} ramp staff.",
         f"so 2027 opens with {pp['ramp_hc_by_month'][0]:.0f} ramp staff. None of these {o2['pp_hires_total']:.0f}, nor Logistics&WH "
         + " and ".join(f"{s.split(' ')[0]} ({m})" for s, m in o2["lw_2026_seats"]) + f", is on the HC rosters (workfile saved {o2['workfile_modified']}): the models may "
         "predate the roster (I-38).")
pr = rep(pr, "| title + salary | Dec-26 |", "| title + salary (open seat, start relaxed; A-29) | Dec-26 |")
pr = rep(pr, "FE HC r41 'Field Engineer' (new-hire block) has no name, salary or start (0 in FE HC); it may be the seat for Fld Eng Budget r15.",
         f"FE HC r41 'Field Engineer' (new-hire block) has no name, salary or start (0 in FE HC); it may be the seat for Fld Eng Budget r15. FE HC r35 Field Engineer "
         f"Manager sits under 'Open Positions' (HC-FE row {o5['section_row']}) with no employee: it is an open seat, not a person, so its match with Fld Eng Budget r20 is "
         f"seat-to-seat (A-29 amended). The COO book _2 leaves it out, FE HC starts it in {o5['hc_start']} and Fld Eng Budget costs it from {o5['sd_start']} (I-39).")
pr = rep(pr, "(Field Engineer Manager from Dec-26)", "(the open Field Engineer Manager seat from Dec-26)")
pr = rep(pr, "| name | DUPLICATE across P&L sources: FO", "| name | PROBABLE DUPLICATE (name match only; title and salary differ; likely FO->FE move) across P&L sources: FO")
pr = rep(pr, "| title + salary (start Dec-26 vs Jan-27) | same person, one P&L source",
         "| title + salary (start Dec-26 vs Jan-27) | same seat (open position, no employee; start month relaxed, A-29), one P&L source")
pr = rep(pr, f"Prod Payroll's {pp['current_hc']:.0f} current staff = PO HC {po['hc_people']} (count).",
         f"Prod Payroll's {pp['current_hc']:.0f} current staff = PO HC {po['hc_people']} (count), or {b2['n_prod']} by role (B2).")
pr = rep(pr, "(model overlaps, the FO/FE duplicate, the PE 'transfer?' row, the open FE row).",
         "(model overlaps, the FO/FE duplicate, the PE 'transfer?' row, the open FE row). The CSV is v6's and is unchanged; v7 writes no per-person CSV.")
A("## Payroll reconciliation\n"); A(pr.strip() + "\n")
hct = sec6["HC tabs added to the workbook"]
hct = rep(hct, "The 10 cells keep the workfile's cached values:\n",
          f"The 10 cells keep the workfile's cached values. v7 (O6): every stored tax rate (D6) is below the {pct(FICA, 2)} employer FICA, so these rates are unverified "
          "(I-37):\n")
if AN:
    hct = hct[:hct.index("Checks: LibreOffice recalculation of v6")] + (
        f"Checks (v6, unchanged in v7): HC tabs copied byte for byte from v6; v7 recalculation of the HC tabs: errors {AN['hc_tabs']['errors']}, cached vs recalculated "
        f"max difference {AN['hc_tabs']['max_diff']:.1e} over {AN['hc_tabs']['cells']:,} cells.\n")
A("## HC tabs added to the workbook (v6; unchanged in v7)\n"); A(hct.strip() + "\n")
A("## Head of Service Delivery salary (I-26, resolved in v5)\n"); A(sec6["Head of Service Delivery salary (I-26, resolved in v5)"].strip() + "\n")
A("## Build and sources\n")
A(f"Output: `02-build/02-build_COO_2027_Budget_Collated_v7.xlsx` and this file (v1-v6 files unchanged; no v7 CSV).  \n"
  f"Scripts: `02-build/scripts/` - v7 entry point `run_build_v7.sh`: prodpay_v6.py + recalc.sh (scratch Prod Payroll evaluation of v6) -> recon_v6.py (on v6) -> "
  f"scen_v7.py make + recalc.sh (scratch copy with Fld Ops Payroll B11 - 1, and v6 itself) -> scen_v7.py compare -> figures_v7.py -> cnotes_v6.py (extracts the v6 "
  f"Collation Notes, byte-exact round trip) -> report_v7.py pass 1 (Collation Notes JSON) -> build_v7.py (v6 + regenerated Collation Notes) -> diff_versions.py "
  f"v6 -> v7, recalc.sh, recon_v6.py on v7 (must equal the v6 run), analyze_v7.py -> report_v7.py pass 2 (JSON must equal pass 1) -> privacy_v6.py (names) and "
  f"paylist_v7.py (per-person amounts) -> scratch name lists deleted. `run_build_v6.sh` ... `run_build.sh` still reproduce v6 ... v1.  \n"
  f"Inputs (read-only): `COO_HC_and_PL_workfile.xlsx` sha256 `{sha(WFILE)}`; `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `{sha(COO)}`; "
  f"`Service_Delivery_PL_worksheets.xlsx` sha256 `{sha(SD)}`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `{sha(NEW)}`.  \n"
  f"Recalculation engine: {lov}.  \n"
  f"Base: v6 workbook sha256 `{sha(V6X)}`.\n")
A("## Completion criteria (v7)\n")
if AN:
    c = AN
    A(mdtable(["Criterion", "Result"], [
        ["0 diffs vs v6 outside Collation Notes", f"diff_versions.py on {c['diff']['total']['sheets']} sheets ({c['diff']['total']['cells']:,} cells, every sheet except Collation Notes): "
         f"formula diffs {c['diff']['total']['formula_diffs']}, value diffs {c['diff']['total']['value_diffs']}; comments added / removed / changed "
         f"{c['diff']['comments'][0]} / {c['diff']['comments'][1]} / {c['diff']['comments'][2]}; sheets only in one file: {len(c['diff']['only_new']) + len(c['diff']['only_old'])}."],
        ["Package", f"{c['package']['identical']} of {c['package']['v6_parts']} v6 parts byte-identical; changed: {', '.join(c['package']['changed'])}; added / removed "
         f"{len(c['package']['added'])} / {len(c['package']['removed'])}; external links {c['package']['external_links']}."],
        ["Cached values are what the formulas give", f"LibreOffice recalculation of v7 vs stored values, every sheet except Collation Notes: {c['recalc']['n_diff']} cells differ, "
         f"max {c['recalc']['max_diff']:.1e}; non-numeric mismatches {c['recalc']['text_mismatch']}; new errors vs v6 {c['errors']['new']}."],
        ["Collation Notes live formulas", f"{c['cn']['formulas']} formulas; recalc vs stored max diff {c['cn']['max_diff']:.1e}, text mismatches {c['cn']['text_mismatch']}; "
         f"first section is the CONFIDENTIAL banner: {c['cn']['banner_first']}."],
        ["Figures recompute from the final file", f"recon_v6.py with the v7 workbook in place of v6: identical output {c['recon_same']}."],
        ["Every critic and verifier item addressed", "B1-B3, O1-O8, V1: see 'Changes from v6' (none declined)."],
        ["V1 fixed everywhere", f"Uncorrected v6 I-28 FO figure in md / Collation Notes outside the 'v6 stated' references: {c['v1_left']}; v6 wording that no overlap was left between the models: {c['phrase_left']}."],
        ["No names", f"privacy_v6.py on the md, the Collation Notes JSON and sheet: {c['privacy']}. The return message is checked the same way."],
        ["Per-person amounts rounded in the md", f"paylist_v7.py: {c['paylist']}."],
    ]))
else:
    A("[pass 1: pending]\n")
for t in ("Depreciation schedule summary", "Unit-cost reconciliation", "Revenue"):
    body = sec6[t].strip()
    if t == "Depreciation schedule summary":
        body = rep(body, "user decision (Decisions pending #2).", "user decision (Decisions pending #3).")
    A(f"## {t}\n"); A(body + "\n")
A("## Assumptions register\n")
asr6 = sec6["Assumptions register"]
a29 = [l for l in asr6.split("\n") if l.startswith("| A-29 |")][0]
a29_cn = md_issue([str(x) for x in [r for r in [s for s in cn6["sections"] if s["heading"] == "Assumptions register"][0]["table"]["rows"] if r[0] == "A-29"][0]])
assert a29 == a29_cn
asr6 = rep(asr6, a29, md_issue([str(y) for y in [r for r in asr["table"]["rows"] if r[0] == "A-29"][0]]))   # row[1] already carries ASR_A29_ADD
asr6 = rep(asr6, "A-27..A-30 are new in v6;", "A-27..A-30 are new in v6; A-31..A-35 are new in v7 and A-29 was amended in v7 (critic O5);")
tab_end = asr6.index("\n\nA-22..A-25")
A(asr6[:tab_end].strip() + "\n" + "\n".join(md_issue(r) for r in ASR_NEW) + "\n" + asr6[tab_end:].rstrip() + "\n")
A("## DeploySum refresh and tie-out (v3 build; unchanged in v4-v7)\n"); A(sec6["DeploySum refresh and tie-out (v3 build; unchanged in v4-v6)"].strip() + "\n")
A("## v6 -> v7 diff\n")
if AN:
    A("`diff_versions.py` (exact: formulas as text, cached values with no tolerance) on every sheet present in both files except Collation Notes:\n")
    A(mdtable(["Sheet", "Cells", "Formula diffs", "Value diffs"], [[k, f"{v['cells']:,}", v["formula_diffs"], v["value_diffs"]] for k, v in AN["diff"]["sheets"].items()]
              + [["**Total**", f"{AN['diff']['total']['cells']:,}", AN["diff"]["total"]["formula_diffs"], AN["diff"]["total"]["value_diffs"]]], ["---", "---:", "---:", "---:"]))
    A(f"Package: {AN['package']['identical']} of {AN['package']['v6_parts']} v6 parts byte-identical; changed: {', '.join(AN['package']['changed'])} (Collation Notes).\n")
    A("## Error scan\n")
    A(mdtable(["Sheet", "v6", "v7"], [[k, v[0], v[1]] for k, v in AN["errors"]["by_sheet"].items()]))
    A(f"New errors in v7: **{AN['errors']['new']}**. Prod Payroll's #NAME? cells are the XLOOKUP rows LibreOffice cannot evaluate (I-05, I-25; evaluated for the analysis per A-28).\n")
    A("## Package\n")
    A(f"Parts {AN['package']['v7_parts']} (v6 {AN['package']['v6_parts']}); `xl/externalLinks/*` **{AN['package']['external_links']}**; defined names "
      f"{AN['package']['defined_names']:,} (v6: {AN['package']['defined_names_v6']:,}).\n")
    A("## Sheets in the output\n")
    A(mdtable(["#", "Sheet", "State"], [[i + 1, s, st] for i, (s, st) in enumerate(AN["sheets"])]))
else:
    A("[pass 1: pending]\n")
A("## Severity scale\n"); A(sec6["Severity scale"].strip() + "\n")
A("## Issues (v7)\n")
A(f"Severity per the scale above. Open: {sev['HIGH']} HIGH, {sev['MED']} MED, {sev['LOW']} LOW; {sev['RESOLVED']} RESOLVED. v7: I-05 adds the capitalisation question "
  f"(B1) and the 7-overlap reading (B2); I-17 shows the deduplicated combined figure; I-28 is a probable duplicate with the FO side recalculated (V1); I-34 is "
  f"caveated (O6); I-23 and I-36 get a cross-reference; I-37, I-38 and I-39 are new. No other severity changed.\n")
ib = sec6["Issues (v6)"]
iss_rest = ib[ib.index("| ID | Sev"):]
A("\n".join(iss_rest.split("\n")[:2]) + "\n" + "\n".join(md_issue(r) if (k in CHANGED or k in ISS_NEW) else md_rows6[k] for k, r in rows.items()) + "\n")
var = ib[ib.index("### Variance scan"):]
var = rep(var, "(v5 workbook; unchanged in v6: 0 value diffs)", "(v5 workbook; unchanged in v6 and v7: 0 value diffs)")
A(var.strip() + "\n")
A("## Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; unchanged in v6 and v7)\n")
A(sec6["Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; unchanged in v6)"].strip() + "\n")
A("## Decisions\n")
A(sec6["Decisions"].strip())
DEC7 = [
    "D1 (v7): Notes and presentation only. build_v7.py copies every v6 part byte for byte and renders only the Collation Notes part, so no budget cell can move.",
    "D2 (v7): Decision #1 (expensed or capitalised) is placed first and v6's decisions are renumbered #2-#9, as the handoff asked; cross-references in carried text "
    "were updated.",
    "D3 (v7): Capitalised case = depreciation only, by the existing Depreciation Schedule logic. The lift / tray split is derived from the model (lift and tray ramp), "
    "so the handoff's fallback split is shown as a check, not used. Supervisors are allocated pro rata to the lift : tray ramp, labelled as an assumption (A-32). "
    "Labour is spread per unit built in 2027 (A-33). A third case, labour already inside the 65,000 / 8,000 unit cost (effect 0), is shown because the handoff's "
    "question names that unit cost.",
    "D4 (v7): 7-overlap: the 2 Prod Payroll current seats that no PO HC production person fills are costed at the model's average current cost per head; the "
    "lift-only / tray-only range is shown (A-34). The deduplicated 9-overlap combined figure adds MH-01 back, because the name match (r20 = MH-01) is firmer than the "
    "count match.",
    "D5 (v7): Lower bound 1 now uses the deduplicated 7-overlap combined figure (the most adverse consistent reading); lower bound 2 excludes I-05; the upper end "
    "keeps v6's convention (I-32 only) so the versions compare. I-37 is not added to the range because the rates are unverified and the figure is an upper bound.",
    "D6 (v7): The I-28 FO side is computed by LibreOffice recalculation of a scratch copy with Fld Ops Payroll B11 reduced by one (scen_v7.py), so every knock-on "
    "(Fld Maint Budget!B29 -> 5330; the supervisor ratio, unchanged) is included.",
    "D7 (v7): Privacy. Per-person amounts for identified employees are rounded to $5k in the md only (paylist_v7.py). The Collation Notes sheet keeps exact "
    "figures because the same workbook holds the named HC tabs, and it carries the CONFIDENTIAL banner. A planned hire (Fld Eng Budget r19, I-36) and open seats "
    "(FE HC r35, I-39) are not people and stay exact. No per-person CSV is written in v7; the scratch name lists of the v6 and v7 builds are deleted after the "
    "build.",
    "D8 (v7): The O6 test uses the statutory 7.65% (A-31) and ignores the Social Security wage base, so the gaps are upper bounds; Finance is asked for the real rates.",
]
A("\n".join(f"- {d}" for d in DEC7) + "\n")
A("## Not done / limits\n")
A(sec6["Not done / limits"].strip())
A("- v7: no budget value was changed. Decision #1, the 7-overlap reading, the T&B rates (I-37), the model date (I-38) and the open FE seat (I-39) are questions for the "
  "user, Finance and the owners; the notes quantify each answer.")
A("- v7: the capitalised case is an approximation at the budget's level of detail (labour per unit built, depreciation by go-live vintage). It does not model a cost "
  "roll per build month, the capitalisation of the current staff already in PO 5110-5140, or the 2026 labour in the Jan-Feb 27 go-lives.")
A("- v7: the SD book's file date is a re-save, so the models' own update date cannot be read from the files (I-38).\n")
md = "\n".join(L)
assert "Decisions pending #2)" not in md and "no person-level overlap" not in md.lower()
assert v6_fo_left(md) == 0, "an uncorrected v6 I-28 FO figure is left in the md"
am = paylist_v7.amounts(V6X, RECON)
md, n_round = paylist_v7.round_text(md, am)
hits, skipped = paylist_v7.find(md, am)
assert not hits, f"exact per-person amounts left in the md: {len(hits)}"
open(OUT_MD, "w").write(md)
print(f"report_v7: md {len(md):,} chars ({n_round} per-person amounts rounded, {skipped} coincidences left in non-people sections); Collation Notes JSON "
      f"{len(cnj):,} chars; issues {dict(sev)}; contribution {f0(C)}; I-05 9 {f0(I05)} / 7 {f0(I05_7)}; capitalised {f0(C - d9)} / {f0(C - d7)}; "
      f"LB1 {f0(LB1)}, LB2 {f0(LB2)}, UB {f0(UB)}; pass {'2' if AN else '1'}")
