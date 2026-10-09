"""Write 02-build_notes_v6.md and the v6 Collation Notes content (JSON).

Usage:
  python3 -I report_v6.py V5_MD CN5_JSON V5_XLSX V6_XLSX RECON_JSON BUILD_INFO_JSON LO_VERSION_TXT WORKFILE COO SD NEW
                          OUT_NOTES_JSON OUT_MD [ANALYZE_JSON]

v6 = v5 + HC tabs (supporting, read-only provenance) + payroll reconciliation against the HC rosters. No budget value
changes. Text is built from the v5 notes (md sections and the v5 Collation Notes, extracted byte-exactly by
cnotes_v6.py); each edit of carried text is a targeted replacement that must hit exactly once.
Numbers: workbook cached values (V6_XLSX / V5_XLSX), RECON_JSON (recon_v6.py) and BUILD_INFO_JSON (build_v6.py); the
carried caveat rows (I-10, I-26, I-31, I-32, I-33, A-14, A-22) take their effect from the v5 Collation Notes, and the
script checks that the contribution they act on is unchanged. No figure is typed here.
PRIVACY: carried v5 text that quoted employee names (I-15, I-26, one cross-department line) is rewritten with
dept + title + roster row; privacy_v6.py checks the outputs.
Without ANALYZE_JSON the md has placeholders for the check sections (pass 1); the Collation Notes JSON does not
depend on ANALYZE_JSON, so both passes must give the same JSON.
"""
import sys, json, re, hashlib, copy, collections
import openpyxl

(V5_MD, CN5, V5X, V6X, RECON, BINFO, LOV, WFILE, COO, SD, NEW, OUT_JSON, OUT_MD) = sys.argv[1:14]
AN = json.load(open(sys.argv[14])) if len(sys.argv) > 14 else None
R = json.load(open(RECON)); B = json.load(open(BINFO)); cn5 = json.load(open(CN5))
md5 = open(V5_MD).read()
lov = open(LOV).read().strip()
w6 = openpyxl.load_workbook(V6X, data_only=True); w5 = openpyxl.load_workbook(V5X, data_only=True)
MON = R["months"]


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


def pct_nm(new, base):
    if base is None or base <= 0 or new < 0:
        return "n/m"
    return f"{(new - base) / base * 100:.0f}%"


def rep(text, old, new, count=1):
    n = text.count(old)
    assert n == count, (n, old[:90])
    return text.replace(old, new)


def resub(text, pat, new, count=1):
    n = len(re.findall(pat, text))
    assert n == count, (n, pat)
    return re.sub(pat, new, text)


def ints(xs):
    return ", ".join(f"{x:,.0f}" for x in xs)


def mdtable(header, rows, align=None):
    align = align or ["---"] * len(header)
    out = "| " + " | ".join(header) + " |\n|" + "|".join(align) + "|\n"
    for r in rows:
        out += "| " + " | ".join("" if v is None else str(v) for v in r) + " |\n"
    return out


# ------------------------------------------------------------------ privacy rewrites of carried v5 text (no names typed)
def scrub(t):
    t = re.sub(r"ratio \(Sep-26\) – [A-Z][a-z]+'", "ratio (Sep-26) – [name; FO HC r25 Field Maintenance Manager]'", t)
    t = re.sub(r"\. [A-Z][a-z]+ \(Fld Ops Payroll row 77\)", ". FO HC r25 Field Maintenance Manager (Fld Ops Payroll row 77)", t)
    t = re.sub(r"'Head of Service Delivery – [A-Z][a-z]+ [A-Z][a-z]+'", "'Head of Service Delivery – [name]' (FE HC r16)", t)
    t = re.sub(r"\([A-Z][a-z]+ is excluded from Logistics&WH", "(FO HC r21 Operations Coordinator is excluded from Logistics&WH", t)
    return t


# ------------------------------------------------------------------ headline (workbook values; v6 = v5)
HL = [("Revenue (company recognized revenue, 9/30/26 sales plan)", "16", [16]),
      ("COGS (COO departments)", "63", [63]),
      ("  of which depreciation (in COGS)", "19-22", [19, 20, 21, 22]),
      ("Gross Profit", "64", [64]),
      ("Opex (COO departments)", "116", [116]),
      ("COO contribution before other income (workbook label 'Net Ordinary Income')", "117", [117]),
      ("Net Other Income", "131", [131]),
      ("**COO contribution** (workbook label 'Net Income')", "132", [132])]


def val(wb, col, rows):
    return sum(float(wb["COO P&L"][f"{col}{r}"].value or 0) for r in rows)


C = val(w6, "AG", [132]); C5 = val(w5, "AG", [132])
assert C == C5, "contribution changed between v5 and v6"
hl_rows = []
for lab, rr, rows in HL:
    n, ag, ag5 = val(w6, "N", rows), val(w6, "AG", rows), val(w5, "AG", rows)
    hl_rows.append([lab, rr, f0(n), f0(ag), f0(ag - n), pct_nm(ag, n), f0(ag5), f0(ag - ag5)])
COGS = val(w6, "AG", [63]); OPEX = val(w6, "AG", [116])

# ------------------------------------------------------------------ reconciliation figures
fo, pp, lw, po, fe, dup, hc, tie = R["fo"], R["pp"], R["lw"], R["po"], R["fe"], R["dup"], R["hc"], R["tie"]
pet = R["pe_transfer"][0]
fofe = dup["fo_fe"][0]
I05, I17, I0517 = po["net_i05"], po["net_i17"], po["net_combined"]
fe_b = fe["burden"]
cs_hire = [e for e in fe["rows"] if e.get("not_on_hc") and not e.get("on_other_roster_by_name")][0]
cs_hire_cost = cs_hire["sd_2027"] * (1 + fe["sd_rates"]["tax"] + fe["sd_rates"]["ben"])
fe75 = [e for e in fe["rows"] if e.get("on_other_roster_by_name")][0]
B11 = fo["inputs"]["techs_B11"]
v5_range = re.search(r"range from (\(?[\d,]+\)?) to (\(?[\d,]+\)?)", (lambda s_: (s_["table"].get("after", []) + s_.get("after", []))[-1])([s for s in cn5["sections"] if s["heading"].startswith("Caveats")][0]))
V5R = f"{v5_range.group(1)} to {v5_range.group(2)}"
MO = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def titles(d):
    return ", ".join(f"{n} {t}" for t, n in hc[d]["titles"].items())
def secs(d):
    return ", ".join(f"{n} {k}" for k, n in hc[d]["sections"].items())
n_fe_name = sum(1 for e in fe["rows"] if e["basis"] == "name"); n_fe_ts = sum(1 for e in fe["rows"] if e["basis"] == "title + salary")
bf = po["backfilled"][0]
ovl = [e for e in lw["seats"] if e["overlap"]]
newseats = [e for e in lw["seats"] if not e["overlap"]]

# ------------------------------------------------------------------ caveat table (v5 rows carried, payroll rows net)
cv5 = [s for s in cn5["sections"] if s["heading"].startswith("Caveats on the headline")][0]
carried = {}
for row in cv5["table"]["rows"]:
    carried.setdefault(row[0], []).append(row)
for k in ("I-10", "I-26", "I-31", "I-32", "I-33", "A-14", "A-22"):
    for row in carried[k]:
        if isinstance(row[3], (int, float)):
            assert abs(row[4] - (C + row[3])) < 0.01, ("carried row does not act on the v6 contribution", k)
cav = []   # [item, direction, text, effect(number|str), after(number|str), source]
cav.append(["I-05", "downside", f"Production payroll ramp (SD Prod Payroll) that PO 5110-5140 does not carry: model 2027 total {f0(pp['total'])} "
            f"(lift {f0(pp['lift_total'])}, tray {f0(pp['tray_total'])}, supervisors {f0(pp['sup_total'])}) less the model's cost of the "
            f"{pp['current_hc']:.0f} current staff already in PO ({f0(pp['current_only']['total'])}). Net of PO HC (v5 showed the gross lift-only gap, {f0(po['pp_lift_gap_v5'])}).",
            -I05, C - I05, "Prod Payroll!S81 (tray/supervisor rows evaluated per A-28); PO!AG33:AG36; 'HC-PO'!Z67:Z70"])
cav.append(["I-17", "downside", f"Logistics & warehouse seats (SD model, not carried) that no HC roster holds: 7 seats, net of the 2 seats that are "
            f"already on CO HC r17 and PO HC r20 ({f0(lw['overlap_cost'])} of the model's {f0(lw['total'])}).",
            -I17, C - I17, "SD Logistics&WH Payroll!S51 less LOG-01 and MH-01 (not carried)"])
cav.append(["I-05 + I-17", "downside", "Both payroll ramps together. No person-level overlap is left between them: the two models size different teams "
            "(production builders and supervisors vs warehouse seats) and the people already on HC rosters are taken out of each.",
            -I0517, C - I0517, "as above"])
cav += [r for r in carried["I-10"]]
cav += [[r[0], r[1], scrub(r[2]), r[3], r[4], r[5]] for r in carried["I-26"]]
cav.append(["I-28", "upside", f"One person costed twice (FO HC r15 Field Technician = Fld Eng Budget r15 Field Engineer, same name): remove from FO "
            f"(Fld Ops Payroll B11 {B11:.0f} -> {B11 - 1:.0f}; one current tech at model rates).", fofe["fo_model_one_tech_2027"], C + fofe["fo_model_one_tech_2027"],
            "Fld Ops Payroll!B11, rows 20-24"])
cav.append(["I-28", "upside", f"Same person: remove from FE instead (Fld Eng Budget row 15, {fofe['sd_salary']:,.0f} at SD burden rates).",
            fofe["fe_cost_2027"], C + fofe["fe_cost_2027"], "Fld Eng Budget!B15; rows 61, 69-70"])
cav += carried["I-31"] + carried["I-32"] + carried["I-33"]
cav.append(["I-34", "upside", f"FE payroll tax and benefits at the FE HC rates ({pct(fe['hc_rates']['tax'], 3)} / {pct(fe['hc_rates']['ben'], 3)}) instead of the SD rates "
            f"({pct(fe['sd_rates']['tax'])} / {pct(fe['sd_rates']['ben'])}) on the same FE salary base.", fe_b["diff_total"], C + fe_b["diff_total"],
            "Fld Eng Budget!B22:B23; 'HC-FE'!D6:D7; FE!AG68:AG69"])
cav.append(["I-35", "upside", "PE HC r22 Head of Production and Delivery ('transfer?') leaves COO from Jan-27. 0 if the role moves to another COO department and is budgeted there once.",
            pet["total_2027"], C + pet["total_2027"], "'HC-PE'!A22, Z22; PE!AG67:AG69"])
cav.append(["I-36", "upside", f"The {cs_hire['sd_start']} Customer Support Specialist hire on Fld Eng Budget (not on FE HC) is not approved.",
            cs_hire_cost, C + cs_hire_cost, "Fld Eng Budget!B19:C19, row 65"])
cav += carried["A-14"] + carried["A-22"]


def cav_md_row(r):
    e = r[3]; a = r[4]
    es = eff(e) if isinstance(e, (int, float)) else e
    as_ = f0(a) if isinstance(a, (int, float)) else a
    return [r[0], r[1], r[2], es, as_, r[5]]


# sign-flip statement
i10 = carried["I-10"][0][3]; i31s = [r for r in carried["I-31"] if r[3] < 0][0][3]
i32 = carried["I-32"]; i32full = max(r[3] for r in i32)
i32tr = [r for r in i32 if r[2].startswith("Trend alternative:")][0][3]
i32tr2 = [r for r in i32 if r[2].startswith("Trend alternative continued")][0][3]
down_all = -I05 - I17 + i10 + i31s
flip_alone = [(k, v) for k, v in (("I-05", -I05), ("I-17", -I17), ("I-10", i10)) if C + v < 0]
sf = []
sf.append(f"Sign-flip statement (computed, net increments): The 2027 COO contribution of {f0(C)} changes sign on "
          + " or ".join(f"{k} alone ({f0(C)} - {f0(-v)} = {f0(C + v)})" for k, v in flip_alone)
          + f". I-31 alone leaves {f0(C + i31s)}.")
sf.append(f"Together, I-05 + I-17 (net) take it to {f0(C - I0517)}. I-10 with the I-31 shortfall gives {f0(C + i10 + i31s)}. "
          f"All quantified downsides together (I-05 net, I-17 net, I-10, I-31 shortfall): {f0(C + down_all)}.")
sf.append(f"Upside: I-32 can add up to {f0(i32full)} (contribution {f0(C + i32full)}); the trend alternative adds {f0(i32tr)} ({f0(C + i32tr)}), or "
          f"{f0(i32tr2)} ({f0(C + i32tr2)}) if the decline also ran through Oct-Dec 26. New in v6 and smaller: I-28 +{fofe['fo_model_one_tech_2027']:,.0f} to "
          f"+{fofe['fe_cost_2027']:,.0f}, I-34 +{fe_b['diff_total']:,.0f}, I-35 up to +{pet['total_2027']:,.0f}, I-36 +{cs_hire_cost:,.0f}. "
          f"With costs held fixed, revenue {f0(C)} ({C / val(w6, 'AG', [16]) * 100:.1f}%) below plan also takes the contribution to zero.")
sf.append(f"Conclusion: the sign of the 2027 COO contribution is not established by this budget, and the production payroll question (I-05) now "
          f"dominates it. Treat {f0(C)} as a point estimate inside a range from {f0(C + down_all)} to {f0(C + i32full)} (illustrative extremes of "
          f"quantified items; excludes I-02, A-22; lower end = all four quantified downsides added: I-05 net, I-17 net, I-10, I-31 shortfall; I-05 and "
          f"I-17 are net of the people already on HC rosters, so they no longer overlap; upper end = I-32 full only, the other upsides A-14, I-28, I-31 "
          f"double count, I-33, I-34, I-35 and I-36 are not added) until I-05, I-17 and I-32 are answered. v5 range: {V5R}.")
assert f0(C + down_all).startswith("(")
RANGE = (C + down_all, C + i32full)

# ------------------------------------------------------------------ issue rows (new / replaced)
ramp_hc = pp["ramp_hc_by_month"]
ISS = {}
ISS["I-05"] = ["I-05", "HIGH", "Prod Payroll!B24:S81 (hidden); Prod Payroll!S41, S62, S79, S81; PO!AG33:AG36; 'HC-PO'!B14:Z22, Z67:Z70",
               f"PO 5110-5140 ({f0(po['po_5100'])}) is the {po['hc_people']} current staff on PO HC, flat all year with no hires ('HC-PO' rows 14-22; PO!U33:AF35 "
               f"equal 'HC-PO'!M67:X69). The production payroll model holds the same {po['pp_current']:.0f} as its current staff ({pp['inputs']['B9']:.0f} lift + "
               f"{pp['inputs']['C9']:.0f} tray on payroll Sep-26; the model has no names or titles, so the match is by headcount) and adds the hires the build plan "
               f"needs. v6 evaluates the whole model, tray and supervisor rows included (A-28): {f0(pp['total'])} for 2027 (lift {f0(pp['lift_total'])}, tray "
               f"{f0(pp['tray_total'])}, supervisors {f0(pp['sup_total'])}). Of that, {f0(pp['current_only']['total'])} is the model's cost of the {pp['current_hc']:.0f} current "
               f"staff, already in PO. Net increment that PO lacks: {f0(I05)} (ramp hires only). It is larger than the v5 gap ({f0(po['pp_lift_gap_v5'])}) because v5 "
               f"compared lift payroll only. The model also hires {po['sd_hires_sep_dec26']['lift']:.0f} lift, {po['sd_hires_sep_dec26']['tray']:.0f} tray and "
               f"{po['sd_hires_sep_dec26']['sup']:.0f} supervisor staff in Sep-Dec 26, which PO HC does not show either.",
               f"Ramp headcount Jan..Dec 27: {ints(ramp_hc)} (plus the {pp['current_hc']:.0f} current staff). Hires in 2027: lift {pp['hires_2027']['lift']:.0f}, tray "
               f"{pp['hires_2027']['tray']:.0f}, supervisors {pp['hires_2027']['sup']:.0f}. Ramp cost: salary {f0(pp['ramp_parts']['sal'])}, absence coverage "
               f"{f0(pp['ramp_parts']['abs'])}, payroll tax {f0(pp['ramp_parts']['tax'])}, benefits {f0(pp['ramp_parts']['ben'])}, new-hire cost {f0(pp['ramp_parts']['nh'])}. "
               f"Model cost of the {pp['current_hc']:.0f} vs PO 5100: {f0(pp['current_only']['total'])} vs {f0(po['po_5100'])} ({f0(po['pp_current_vs_po_hc']['diff'])}: model average salary "
               f"{pp['inputs']['B5']:,.2f} vs PO HC {po['pp_current_vs_po_hc']['hc_avg_salary']:,.2f}; model tax {pct(pp['inputs']['B6'])}, benefits "
               f"{pct(pp['inputs']['B7'])} / {pct(pp['inputs']['C7'])} plus absence coverage vs PO HC {pct(hc['PO']['rate_tax'], 2)} / {pct(hc['PO']['rate_ben'], 2)}). "
               f"Python replica of the model vs LibreOffice: max difference {max(pp['check_max_abs_diff'].values()):.1e}.",
               f"({I05:,.0f}) on the contribution if the model is right (net of the {pp['current_hc']:.0f} already in PO)",
               f"impact {I05:,.0f} (> $250k; on its own turns the contribution negative)",
               "PO owner / user: is PO 2027 payroll the 9 current staff only (as budgeted) or the build-plan staffing in Prod Payroll? If the model is right, "
               "add the ramp (net increment), not the model total, to PO 5110-5140. Severity raised from MED (v5) because the net amount is now quantified."]
ISS["I-17"] = ["I-17", "HIGH", "Logistics&WH Payroll!A14:S51 (SD, not carried); PO!AG33:AG36; 'HC-PO'!B16:C20; 'HC-CO'!B17:C17",
               f"The SD Logistics & Warehouse payroll model ({f0(lw['total'])} for 2027, referenced by no formula) names two people who are already on HC "
               f"rosters: its Logistics Manager seat (LOG-01) is CO HC r17 Field Logistics Manager (costed in CO 6610-6640; the model's own note classifies the seat "
               f"as Central Operations) and its first Material Handler seat (MH-01) is PO HC r20 Material Handler (costed in PO 5110-5140). Net of those two seats "
               f"({f0(lw['overlap_cost'])} at model rates), the model adds {f0(I17)} that no roster or P&L line carries: "
               f"{len(newseats)} seats ({', '.join(e['seat'].split()[1] for e in newseats)}), all hires from {min((e['start'] for e in newseats), key=lambda x: (x[-2:], MO.index(x[:3])))} on. MH-02 is described as the backfill for PO HC r16 Material Handling Team Lead, who stays on PO HC for all "
               f"of 2027.",
               "Seats (2027 cost at model rates, start): " + "; ".join(f"{e['seat'].replace('Logistics&WH ', '')} {f0(e['cost_2027'])} ({e['start']})" for e in lw["seats"])
               + f". Net seats headcount Jan..Dec 27: {ints(lw['net_hc_by_month'])}. The two overlapping people cost {f0(sum(e['hc_side_2027_cost'] for e in ovl))} "
               f"on their HC rosters (already in the budget). Seats the model itself excludes: LOG-02 (= FO HC r21, budgeted in FO) and MH-05 (in no model, I-27). "
               f"PO HC r16 2027 cost {f0(bf['cost_2027'])} at PO rates.",
               f"({I17:,.0f}) on the contribution (net); v5 showed the gross {f0(lw['total'])}",
               f"impact {I17:,.0f} (> $250k)",
               f"PO owner to confirm the warehouse team plan. If adopted, add the {len(newseats)} new seats ({f0(I17)}), not the model total. Confirm whether PO HC r16 leaves "
               f"the role MH-02 backfills; if so PO HC is overstated by up to {f0(bf['cost_2027'])}."]
pairs_txt = (f"{dup['n_same_fe'] + dup['n_same_fo']} same-person pairs inside one P&L source (FE HC <-> Fld Eng Budget {dup['n_same_fe']}, FO HC <-> Fld Ops "
             f"Payroll {dup['n_same_fo']}); {dup['n_cross_source_review']} duplicate across P&L sources; {dup['n_lw']} with the not-carried Logistics&WH model (I-17)")
hosd = dup["hosd"][0]
ISS["I-28"] = ["I-28", "MED", "'HC-FO'!B15:D15; Fld Eng Budget!A15:C15, row 61; Fld Ops Payroll!B11; 'HC-FE'!B41:D41; 'HC-CO'; 'HC-PE'",
               f"v6 answers the person-level question with the HC rosters. Every person on FE HC, CO HC, PE HC, PO HC, FO HC, SD Fld Eng Budget, SD Fld Ops Payroll, "
               f"SD Logistics&WH and SD Prod Payroll was compared by name where present, otherwise by title + salary + start (A-29). CO and PE: no person on the FE "
               f"roster is on CO HC or PE HC (0 name matches, 0 title + salary matches). The Head of Service Delivery is on FE HC r16 and Fld Eng Budget r21 only "
               f"(nearest title elsewhere: PE HC r22 Head of Production and Delivery, a different person at a different salary; I-35). One person is costed twice in "
               f"the budget: Fld Eng Budget r15 Field Engineer ({fofe['sd_salary']:,.0f}, 'current employee') has the same full name as FO HC r15 Field Technician "
               f"({fofe['hc_salary']:,.0f}), one of the {B11:.0f} current techs Fld Ops Payroll costs by count (B11 = {B11:.0f}). FE HC has no salary for this person; its r41 "
               f"'Field Engineer' row is open (no name, salary or start).",
               f"FE side 2027: salary {f2(fofe['fe_sal_2027'])}, with SD burden {f0(fofe['fe_cost_2027'])}. FO side: one current tech at model rates {f0(fofe['fo_model_one_tech_2027'])} "
               f"(salary {f2(fofe['fo_model_one_tech_sal_2027'])}). Pair scan: {pairs_txt}. Roster-to-P&L map: 02-build_roster_map_v6.csv (no names).",
               f"+{fofe['fo_model_one_tech_2027']:,.0f} to +{fofe['fe_cost_2027']:,.0f} (budget overstated by one person)",
               f"impact {fofe['fe_cost_2027']:,.0f} ($50k-250k)",
               f"SD / FO owners: confirm whether this person moved from FO to FE. Then remove them from one side (Fld Ops Payroll B11 {B11:.0f} -> {B11 - 1:.0f}, or Fld Eng Budget "
               "row 15) and, if the move is real, give FE HC r41 the salary and start month. No budget value changed in v6."]
ISS["I-34"] = ["I-34", "MED", "Fld Eng Budget!B22:B23; Fld Ops Payroll!B7:B8; 'HC-FE'!D6:D7; FE!AG68:AG69",
               f"Payroll tax and benefits on FE salaries use the SD field rates ({pct(fe['sd_rates']['tax'])} / {pct(fe['sd_rates']['ben'])}, Fld Eng Budget!B22:B23 = "
               f"Fld Ops Payroll!B7:B8). FE HC uses the FE rates from the T&B file, {pct(fe['hc_rates']['tax'], 3)} / {pct(fe['hc_rates']['ben'], 3)} ('HC-FE'!D6:D7, stored "
               f"as values, A-30). On the 2027 FE salary base {f0(fe['pl_v5']['sal'])} the budget carries 6630 {f0(fe_b['sd_tax'])} and 6640 {f0(fe_b['sd_ben'])}; at FE HC "
               f"rates they would be {f0(fe_b['hc_rate_tax'])} and {f0(fe_b['hc_rate_ben'])}. Not changed in v6 (no budget change without a user decision).",
               f"Difference 2027: 6630 +{fe_b['diff_tax']:,.0f}, 6640 +{fe_b['diff_ben']:,.0f}, total +{fe_b['diff_total']:,.0f} more in the budget than at FE HC rates "
               f"(on the matched people only, {f0(fe_b['matched_base'])} of salary: +{fe_b['matched_diff_total']:,.0f}). Other departments: FO HC rates "
               f"{pct(hc['FO']['rate_tax'], 3)} / {pct(hc['FO']['rate_ben'], 3)} are within {max(abs(hc['FO']['rate_tax'] - fo['inputs']['tax_B7']), abs(hc['FO']['rate_ben'] - fo['inputs']['ben_B8'])) * 100:.3f} points of the SD rates; PO, CO and PE payroll already use their HC rates.",
               f"+{fe_b['diff_total']:,.0f} if the FE HC rates are right", f"impact {fe_b['diff_total']:,.0f} ($50k-250k)",
               "User / Finance: choose the FE burden rates (FE HC T&B rates or the SD field rates). If FE HC, set Fld Eng Budget B22:B23 to the FE rates."]
ISS["I-35"] = ["I-35", "MED", "'HC-PE'!A22:Z22; PE!AG67:AG69",
               f"PE HC r22 Head of Production and Delivery ({pet['salary']:,.0f}, {pet['start']} to {pet['end']}) is marked '{pet['flag']}' in column A. The row is costed in "
               f"PE 6610-6640 for all of 2027 (PE 2027 payroll equals PE HC). The person is on no other roster (0 name and 0 title matches), so there is no double "
               f"count today. If the transfer happens, the cost leaves PE, and leaves COO if the receiving department is outside the five COO departments.",
               f"2027 cost: salary {f0(pet['sal_2027'])} + payroll tax {f0(pet['tax_2027'])} ({pct(hc['PE']['rate_tax'], 2)}) + benefits {f0(pet['ben_2027'])} "
               f"({pct(hc['PE']['rate_ben'], 2)}) = {f0(pet['total_2027'])}. The HC tabs have Transfers In/Out blocks (rows 51-64) for such moves; none is filled.",
               f"up to +{pet['total_2027']:,.0f} (leaves COO from Jan-27); 0 if it moves within COO and is budgeted once",
               f"impact not determinable; owner confirmation needed (exposure {pet['total_2027']:,.0f})",
               "PE owner to confirm the transfer, the month and the receiving department; record it in the Transfers Out / In blocks so it is budgeted once."]
ISS["I-36"] = ["I-36", "LOW", "Fld Eng Budget!A15:C15, A19:C19; 'HC-FE'!B41:F41; FE!AG67",
               f"Fld Eng Budget costs two rows that FE HC does not: r15 Field Engineer {fe75['sd_salary']:,.0f} (the same person as FO HC r15; I-28) and r19 Customer Support Specialist, "
               f"a new hire from {cs_hire['sd_start']} at {cs_hire['sd_salary']:,.0f} (links to r18). FE HC instead has an open 'Field Engineer' row (r41) with no salary or start. Together the two rows "
               f"explain the whole gap between FE HC salary {f0(fe['hc_total_sal'])} and the budget's FE 6610 {f0(fe['sd_total_sal'])}. Start months differ for every "
               f"matched person (HC Sep-26, or Dec-26 for the Field Engineer Manager; Fld Eng Budget Jan-27), with no 2027 effect.",
               f"Gap {f0(fe['sd_total_sal'] - fe['hc_total_sal'])} = r15 {f2(fe75['sd_2027'])} + r19 {f2(cs_hire['sd_2027'])}. Matched people: 2027 monthly salary "
               f"identical (max difference {fe['matched_max_monthly_diff']:.2f}). The COO book's FE 6610 ({f0(fe['coo_book']['sal'])}) is FE HC less "
               f"{', '.join(fe['coo_book_gap_rows'])} ({f0(fe['coo_book_gap_vs_hc'])}, from Dec-26).",
               f"+{cs_hire_cost:,.0f} if the {cs_hire['sd_start']} hire is not approved (salary {f0(cs_hire['sd_2027'])} + SD burden)",
               f"impact {cs_hire_cost:,.0f} (< $50k)",
               "FE owner to confirm the Aug-27 Customer Support Specialist hire and add it to FE HC if approved; the r15 row is handled under I-28."]

# ------------------------------------------------------------------ v5 issues table (md) -> v6
sec5 = collections.OrderedDict()
parts = re.split(r"(?m)^## ", md5)
head5 = parts[0]
for p in parts[1:]:
    t, _, b = p.partition("\n")
    sec5[t.strip()] = b
exp = ["Decisions pending", "Headline: 2027 COO contribution", "Changes from v4", "Head of Service Delivery salary (I-26, resolved in v5)",
       "Build and sources", "Completion criteria (v5)", "Depreciation schedule summary", "Unit-cost reconciliation", "Revenue",
       "Assumptions register", "DeploySum refresh and tie-out (v3 build; unchanged in v4 and v5)", "v4 -> v5 diff", "Error scan", "Package",
       "Sheets in the output", "Severity scale", "Issues (v5)", "Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5)",
       "Decisions", "Not done / limits"]
assert list(sec5) == exp, list(sec5)
iss_body = sec5["Issues (v5)"]
iss_tab_lines = [l for l in iss_body.split("\n") if l.startswith("| I-")]
iss_md = collections.OrderedDict()
for l in iss_tab_lines:
    iss_md[l.split("|")[1].strip()] = l
assert len(iss_md) == 33


def md_issue(row):
    return "| " + " | ".join(row) + " |"


for k in ("I-05", "I-17", "I-28"):
    iss_md[k] = md_issue(ISS[k])
iss_md["I-15"] = scrub(iss_md["I-15"])
iss_md["I-26"] = rep(scrub(iss_md["I-26"]), "None. Confirm at sign-off that the Head of Service Delivery is not also budgeted on CO or PE (I-28).",
                     "None. v6: the Head of Service Delivery is on FE HC r16 and Fld Eng Budget r21 only, not on CO HC or PE HC (I-28).")
for k in ("I-34", "I-35", "I-36"):
    iss_md[k] = md_issue(ISS[k])
sev = collections.Counter(l.split("|")[2].strip() for l in iss_md.values())

# ------------------------------------------------------------------ Collation Notes JSON (from v5)
cn = copy.deepcopy(cn5)
cn["title"] = rep(cn["title"], "build v5", "build v6")
S = {s["heading"].split(" (")[0].split(" -")[0]: s for s in cn["sections"]}
dp = cn["sections"][0]; assert dp["heading"].startswith("Decisions pending")
DEC_NEW = [
    ["5", "Production and warehouse payroll (PO 5110-5140)", "I-05, I-17",
     f"PO 5110-5140 = the {po['hc_people']} current PO HC staff, flat ({f0(po['po_5100'])}); no ramp hires.",
     f"Add the Prod Payroll ramp: ({I05:,.0f}). Add the 7 new Logistics&WH seats: ({I17:,.0f}). Both: ({I0517:,.0f}). Keep as is: 0. "
     f"(Net of the people already on PO HC and CO HC; not the model totals.)", "User, with the PO owner"],
    ["6", "One person costed in both FO and FE", "I-28",
     "Costed twice: one of the 14 current techs in Fld Ops Payroll and Fld Eng Budget row 15.",
     f"Remove from FO (B11 {B11:.0f} -> {B11 - 1:.0f}): +{fofe['fo_model_one_tech_2027']:,.0f}. Remove from FE (row 15): +{fofe['fe_cost_2027']:,.0f}.", "SD / FO owners"],
    ["7", "FE payroll tax and benefit rates", "I-34",
     f"SD field rates {pct(fe['sd_rates']['tax'])} / {pct(fe['sd_rates']['ben'])} on FE salaries.",
     f"FE HC (T&B) rates {pct(fe['hc_rates']['tax'], 3)} / {pct(fe['hc_rates']['ben'], 3)}: +{fe_b['diff_total']:,.0f}. Keep: 0.", "User / Finance"],
    ["8", "PE 'transfer?' row (Head of Production and Delivery)", "I-35",
     f"In PE 6610-6640 for all of 2027 ({f0(pet['total_2027'])}).",
     f"Leaves COO from Jan-27: +{pet['total_2027']:,.0f}. Moves within COO: 0 (budget it once, on the receiving department). Stays: 0.", "PE owner"]]
dp["table"]["rows"] += DEC_NEW
hl = cn["sections"][1]; assert hl["heading"].startswith("Headline")
assert hl["table"]["header"][-1] == "2027 in v4 (value)"
hl["table"]["header"][-1] = "2027 in v5 (value)"
for row in hl["table"]["rows"]:
    rr = [int(x) for x in re.findall(r"\d+", row[1])]
    rows = list(range(rr[0], rr[-1] + 1))
    row[-1] = round(val(w5, "AG", rows), 2)
cvs = cn["sections"][2]; assert cvs["heading"].startswith("Caveats")
assert cvs["lines"][2].startswith("(3) Open exposures")
cvs["lines"][2] = ("(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. v6: I-05 and I-17 are "
                   "net increments (SD model ramp less the people already on HC rosters), so they no longer overlap; the I-05 + I-17 row shows both together.")
cvs["table"]["rows"] = [[r[0], r[1], r[2], round(r[3], 2) if isinstance(r[3], float) else r[3], round(r[4], 2) if isinstance(r[4], float) else r[4], r[5]] for r in cav]
cvs["table"]["after"] = []
cvs["after"] = sf
src = [s for s in cn["sections"] if s["heading"] == "Source and build"][0]
src["lines"] = [f"Base: v5 collated workbook. v6 adds six supporting tabs copied from COO_HC_and_PL_workfile.xlsx (HC-FO, HC-PO, HC-CO, HC-FE, HC-PE, "
                f"HC-COO, after Fld Eng Budget) and changes no budget value: 0 formula and 0 value differences on the 12 existing sheets vs v5 (Collation Notes "
                f"regenerated). The HC tabs' T&B rate links (D6:D7 on each dept tab, external workbook) are stored as values (list below). Inputs unchanged; "
                f"COO book _2 stays the P&L source (newer than the workfile).",
                "Full notes: 02-build/02-build_notes_v6.md (section 'Payroll reconciliation'). Roster-to-P&L map without names: 02-build/02-build_roster_map_v6.csv. "
                "Numbers on this sheet: live formulas (headline) or values computed by recon_v6.py / report_v6.py from this workbook and the inputs."]
chg = [s for s in cn["sections"] if s["heading"] == "Changes from v4"][0]
CHG = [
    ["HC tabs", "Supporting rosters (provenance, read-only)", "HC-FO, HC-PO, HC-CO, HC-FE, HC-PE, HC-COO copied cell by cell with styles from the workfile, after Fld Eng Budget; "
     "formulas re-pointed to the new tab names; 10 T&B rate links stored as values; 0 errors after recalculation.", "HC-* tabs; 'HC tabs' section of the md"],
    ["Budget values", "Unchanged", "0 formula and 0 value differences vs v5 on the 12 existing sheets; contribution " + f0(C) + " (v5 " + f0(C5) + ").", "v5 -> v6 diff"],
    ["I-05", "Production payroll, net of PO HC", f"MED -> HIGH. Net increment {f0(I05)} (model {f0(pp['total'])} less its cost of the 9 current staff); v5 gross lift-only gap {f0(po['pp_lift_gap_v5'])}.", "I-05; caveat table"],
    ["I-17", "Warehouse payroll, net of HC overlaps", f"HIGH. Net {f0(I17)} (model {f0(lw['total'])} less the 2 seats already on CO HC r17 and PO HC r20).", "I-17; caveat table"],
    ["I-28", "Person-level overlap check", f"Answered from the rosters: Head of Service Delivery not on CO or PE; 1 person costed in both FO and FE (+{fofe['fo_model_one_tech_2027']:,.0f} to +{fofe['fe_cost_2027']:,.0f}).", "I-28; Decisions pending #6"],
    ["New issues", "I-34, I-35, I-36", f"FE burden rates (+{fe_b['diff_total']:,.0f}); PE 'transfer?' row ({f0(pet['total_2027'])}); FE roster differences (+{cs_hire_cost:,.0f}).", "Issues; Decisions pending #7-8"],
    ["Sign flip", "Recomputed with net increments", f"v5 range {V5R}; v6 {f0(RANGE[0])} to {f0(RANGE[1])}.", "Sign-flip statement"],
    ["Privacy", "Employee names removed from carried text", "I-15, I-26 and one cross-department line now refer to dept + title + roster row.", "Issues; md"],
]
chg["heading"] = "Changes from v5"
chg["table"] = {"header": ["Item", "Point", "What v6 did", "Where"], "rows": CHG, "after": []}
# new sections after 'Changes from v5'
idx = cn["sections"].index(chg) + 1
REC_SUM = []
for d in ("FO", "PO", "CO", "FE", "PE"):
    t = tie[d]
    REC_SUM.append([d, "/".join(t["gl"]), hc[d]["n_people"], round(hc[d]["z"]["tot"], 2),
                    round(sum(t["v5"][k] for k in ("sal", "tax", "ben")), 2), round(sum(t["coo_book"][k] for k in ("sal", "tax", "ben")), 2)])
NOTE_REC = [
    f"FO: SD Fld Ops Payroll = current {fo['current_hc_by_month'][0]:.0f} (= FO HC {hc['FO']['n_people']}: {B11:.0f} techs by count, coordinator and manager by name) {f0(fo['current']['total'])} + ramp {f0(fo['ramp']['total'])} "
    f"= {f0(fo['total'])} (FO 5510-5540). Current salary {f0(fo['current']['sal'])} vs FO HC / COO book 5510 {f0(hc['FO']['z']['sal'])} ({f0(fo['current_vs_hc']['diff_sal'])}: "
    f"model average tech salary).",
    f"PO: PO HC {po['hc_people']} = PO 5110-5140 ({f0(po['po_5100'])}). Of the {po['hc_people']}, {po['in_pp_by_count']} match Prod Payroll's current staff by headcount, "
    f"{len(po['in_lw_by_name'])} (r20) is Logistics&WH MH-01 by name. "
    f"Net increments not in the budget: Prod Payroll ramp {f0(I05)} (I-05), Logistics&WH {len(newseats)} seats {f0(I17)} (I-17); together {f0(I0517)}.",
    f"Net ramp headcount Jan..Dec 27 (Prod Payroll + Logistics&WH): {ints(po['net_combined_hc_by_month'])}.",
    f"CO: CO HC {hc['CO']['n_people']} = CO 6610-6640. PE: PE HC {hc['PE']['n_people']} = PE 6610-6640; r22 'transfer?' {f0(pet['total_2027'])} (I-35). FE: budget = Fld Eng Budget; FE HC + r15 (I-28) + "
    f"{cs_hire['sd_start']} hire (I-36); burden +{fe_b['diff_total']:,.0f} vs FE HC rates (I-34).",
]
new_secs = [
    {"heading": "Payroll reconciliation (v6): HC roster vs P&L payroll lines (2027, salary + tax + benefits)", "lines": NOTE_REC,
     "table": {"header": ["Dept", "GL", "HC people", "HC roster total", "v6 P&L (= v5)", "COO book _2"], "rows": REC_SUM, "after": []}},
    {"heading": "Duplicate scan (I-28): person matches across rosters (names not shown)",
     "table": {"header": ["Person A", "Person B", "Match basis", "Classification"],
               "rows": [[p["a"], p["b"], p["basis"], p["class"]] for p in dup["pairs"]], "after": []}},
    {"heading": "HC tabs: external-link formulas in the workfile, stored as cached values",
     "table": {"header": ["Tab", "Cell", "Original formula (text)", "Stored value"],
               "rows": [[e["sheet"], e["cell"], e["formula"], float(e["value"])] for e in B["external_cells"]], "after": []}},
]
cn["sections"][idx:idx] = new_secs
asr = [s for s in cn["sections"] if s["heading"] == "Assumptions register"][0]
ASR_NEW = [
    ["A-27", "Net increment of an SD payroll model = model 2027 total less the model's own cost of the people already on an HC roster (same model rates)",
     f"I-05 {f0(I05)}; I-17 {f0(I17)}", "Prod Payroll; SD Logistics&WH Payroll", "builder definition (v6, handoff: 'model total minus the overlap already in PO')"],
    ["A-28", "Prod Payroll tray and supervisor rows evaluated by replacing XLOOKUP (match_mode 1) with an equivalent SMALL/COUNTIF formula in a scratch copy only",
     f"model 2027 {f0(pp['total'])}; Python replica agrees to {max(pp['check_max_abs_diff'].values()):.0e}", "Prod Payroll!B48:Q48 (workbook unchanged)", "builder method (v6)"],
    ["A-29", "Person match: name where present (all tokens of the shorter name in the longer, same first token); otherwise title + salary + start; one-to-one",
     f"{len(dup['pairs'])} pairs; anonymous model rows (Prod Payroll current staff, Fld Ops Payroll current techs) matched by headcount only", "recon_v6.py", "handoff rule"],
    ["A-30", "HC tab tax/benefit rates (D6:D7) linked to an external T&B workbook are kept as the workfile's cached values",
     "10 cells", "'HC-*'!D6:D7", "builder (as DeploySum in v3)"],
]
asr["table"]["rows"] += ASR_NEW
iss = [s for s in cn["sections"] if s["heading"].startswith("Issues (v5)")][0]
iss["heading"] = iss["heading"].replace("Issues (v5)", "Issues (v6)")
rows = collections.OrderedDict((r[0], r) for r in iss["table"]["rows"])
for k in ("I-05", "I-17", "I-28"):
    rows[k] = ISS[k]
rows["I-15"] = [scrub(x) if isinstance(x, str) else x for x in rows["I-15"]]
rows["I-26"] = [scrub(x) if isinstance(x, str) else x for x in rows["I-26"]]
rows["I-26"][7] = rep(rows["I-26"][7], "None. Confirm at sign-off that the Head of Service Delivery is not also budgeted on CO or PE (I-28).",
                      "None. v6: the Head of Service Delivery is on FE HC r16 and Fld Eng Budget r21 only, not on CO HC or PE HC (I-28).")
for k in ("I-34", "I-35", "I-36"):
    rows[k] = ISS[k]
iss["table"]["rows"] = list(rows.values())
cn["stale_checked"] = []
cnj = json.dumps(cn, indent=1, ensure_ascii=False)
open(OUT_JSON, "w").write(cnj)

# ------------------------------------------------------------------ md
L = []
A = L.append
A("# 02-build notes v6 - 2027 COO budget collation\n")
# Decisions pending
dp5 = sec5["Decisions pending"]
dp_tab = [l for l in dp5.split("\n") if l.startswith("|")]      # header, separator, rows
A("## Decisions pending\n")
A(f"{len(dp_tab) - 2 + len(DEC_NEW)} user decisions are open ({len(DEC_NEW)} new in v6: #{len(dp_tab) - 1}-#{len(dp_tab) - 2 + len(DEC_NEW)}). The builder has not resolved them; the budget carries the 'current treatment' column. "
  f"Effects are on the 2027 COO contribution, each on its own.\n")
A("\n".join(dp_tab) + "\n" + "\n".join(md_issue(r) for r in DEC_NEW) + "\n")
A(f"v6 changes **no budget value**. It brings the six HC tabs of the COO HC & PL workfile into the workbook as supporting tabs and reconciles every "
  f"payroll source against those employee-level rosters. The 2027 COO contribution stays **{f0(C)}** (v5 {f0(C5)}). What changes is the reading of it: "
  f"net of the people already on PO HC, the production payroll ramp the budget does not carry is {f0(I05)} (I-05), and the warehouse seats add "
  f"{f0(I17)} (I-17). Diff vs v5: " + (f"{AN['diff']['total']['formula_diffs']} formula and {AN['diff']['total']['value_diffs']} value differences on "
  f"{AN['diff']['total']['sheets']} existing sheets ({AN['diff']['total']['cells']:,} cells)" if AN else "[pass 1: diff pending]") + "; see 'v5 -> v6 diff'.\n")
# Headline
A("## Headline: 2027 COO contribution\n")
A(mdtable(["Line", "COO P&L row", "2026 (N)", "2027 v6 (AG)", "Change", "%", "2027 v5 (AG)", "v6 - v5"], hl_rows,
          ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:"]))
A(f"- **2027 COO contribution (COO P&L AG132): {f0(C)}**, unchanged from v5. Revenue {f0(val(w6, 'AG', [16]))} (all to 4100, orchestrator assumption); "
  f"COGS + Opex {f0(COGS + OPEX)}.")
A(f"- Issues: {sev['HIGH']} HIGH, {sev['MED']} MED, {sev['LOW']} LOW open; {sev['RESOLVED']} RESOLVED. v6 raises I-05 to HIGH and adds I-34 (MED), "
  f"I-35 (MED) and I-36 (LOW).\n")
hb = sec5["Headline: 2027 COO contribution"]
cav_head = hb[hb.index("### Caveats on the headline"):hb.index("(3) Open exposures")]
A(cav_head.rstrip() + "\n")
A("(3) Open exposures, each on its own against the headline. 'n/d' = not determinable from the workbook. v6: I-05 and I-17 are **net increments** "
  "(SD model ramp less the people already on HC rosters, A-27), so they no longer overlap; the 'I-05 + I-17' row shows both together.\n")
A(mdtable(["Item", "Direction", "What could happen", "Effect on 2027 COO contribution", "Contribution after this item alone", "Source cells"],
          [cav_md_row(r) for r in cav], ["---", "---", "---", "---:", "---:", "---"]))
A("**" + sf[0].split(":")[0] + ":**" + sf[0].split(":", 1)[1] + " " + " ".join(sf[1:]) + "\n")
# Changes from v5
A("## Changes from v5\n")
A(mdtable(["Item", "Point", "What v6 did", "Where"], CHG))
A("No budget value was changed; every new figure is a reading of existing cells, the HC tabs or the SD models. v5's own changes from v4 are listed in "
  "`02-build_notes_v5.md` and still apply.\n")
# Payroll reconciliation
A("## Payroll reconciliation\n")
A("Sources: the HC tabs of `COO_HC_and_PL_workfile.xlsx` (now HC-FO ... HC-COO in the workbook; one row per person, 2027 = columns M:X), the P&L payroll "
  "lines of the v6 workbook (= v5), the COO book _2, and the SD payroll models (Fld Ops Payroll, Fld Eng Budget and Prod Payroll in the workbook; "
  "Logistics&WH Payroll in the SD book, not carried). People are identified by roster + row + title; names were used only inside recon_v6.py to match "
  "people. 'Current' = on payroll before 2027 and on an HC roster; 'ramp' = hires the SD models add. All amounts are 2027 (Jan-Dec), salary + payroll "
  "tax + benefits unless stated.\n")
A("### Summary by department\n")
A(mdtable(["Dept", "GL", "HC roster: people, 2027 total", "v6 P&L line (= v5)", "COO book _2", "SD model 2027", "Current staff in the SD model", "Ramp in the SD model", "Overlaps found", "Net increment not in the budget"],
          [["FO", "5510-5540", f"{hc['FO']['n_people']}; {f0(hc['FO']['z']['tot'])}", f0(sum(tie['FO']['v5'][k] for k in ('sal', 'tax', 'ben'))), f0(sum(tie['FO']['coo_book'][k] for k in ('sal', 'tax', 'ben'))),
            f"Fld Ops Payroll {f0(fo['total'])}", f"{fo['current_hc_by_month'][0]:.0f} = FO HC {hc['FO']['n_people']}; {f0(fo['current']['total'])}", f0(fo["ramp"]["total"]), "FO HC r15 also on Fld Eng Budget r15 (I-28)", "0 (the SD model is the budget)"],
           ["PO", "5110-5140", f"{hc['PO']['n_people']}; {f0(hc['PO']['z']['tot'])}", f0(po["po_5100"]), f0(sum(tie['PO']['coo_book'][k] for k in ('sal', 'tax', 'ben'))),
            f"Prod Payroll {f0(pp['total'])}; Logistics&WH {f0(lw['total'])}", f"Prod Payroll {pp['current_hc']:.0f} (count) {f0(pp['current_only']['total'])}; Logistics&WH {len(ovl)} seats {f0(lw['overlap_cost'])}",
            f"Prod Payroll {f0(I05)}; Logistics&WH {f0(I17)}", f"{po['in_pp_by_count']} of {po['hc_people']} in Prod Payroll (count); r20 = Logistics&WH MH-01 (name); r16 backfilled by MH-02", f"{f0(I0517)} (I-05 {f0(I05)}, I-17 {f0(I17)})"],
           ["CO", "6610-6640", f"{hc['CO']['n_people']}; {f0(hc['CO']['z']['tot'])}", f0(sum(tie['CO']['v5'][k] for k in ('sal', 'tax', 'ben'))), f0(sum(tie['CO']['coo_book'][k] for k in ('sal', 'tax', 'ben'))),
            "none (r17 is Logistics&WH LOG-01)", "-", "-", "r17 = Logistics&WH LOG-01 (name)", "0"],
           ["FE", "6610-6640", f"{hc['FE']['n_people']} + {hc['FE']['n_open_no_salary']} open row; {f0(hc['FE']['z']['tot'])}", f0(sum(tie['FE']['v5'][k] for k in ('sal', 'tax', 'ben'))), f0(sum(tie['FE']['coo_book'][k] for k in ('sal', 'tax', 'ben'))),
            f"Fld Eng Budget {f0(sum(tie['FE']['v5'][k] for k in ('sal', 'tax', 'ben')))}", f"{n_fe_name + n_fe_ts} of {hc['FE']['n_people']} matched ({n_fe_name} name, {n_fe_ts} title + salary)", f"{cs_hire['sd_start']} hire {f0(cs_hire_cost)} (I-36)",
            "Fld Eng Budget r15 = FO HC r15 (I-28)", "0 (the SD model is the budget)"],
           ["PE", "6610-6640", f"{hc['PE']['n_people']}; {f0(hc['PE']['z']['tot'])}", f0(sum(tie['PE']['v5'][k] for k in ('sal', 'tax', 'ben'))), f0(sum(tie['PE']['coo_book'][k] for k in ('sal', 'tax', 'ben'))),
            "none", "-", "-", "none; r22 'transfer?' (I-35)", "0"]],
          ["---"] * 10))
A(f"HC roster vs P&L line, monthly: PO, CO and PE 2027 P&L payroll equal their HC rows 67-69 in every month (max difference: PO {tie['PO']['v5']['max_monthly_diff_vs_hc']:.2f}, "
  f"CO {tie['CO']['v5']['max_monthly_diff_vs_hc']:.2f}, PE {tie['PE']['v5']['max_monthly_diff_vs_hc']:.2f}). FO and FE P&L come from the SD models (I-02); the COO book _2 "
  f"equals FO HC exactly and equals FE HC less the Field Engineer Manager row.\n")
# FO
A("### FO: Fld Ops Payroll (FO 5510-5540) split into current staff and ramp\n")
b = fo["blocks"]
A(mdtable(["Block (Fld Ops Payroll rows)", "Who", "Salary", "New-hire cost", "Payroll tax", "Benefits", "Total 2027", "Headcount Jan-27 -> Dec-27"],
          [["Current techs (20-24)", f"{B11:.0f} = FO HC field technicians {fo['match']['techs_hc']} (count; model average {fo['inputs']['avg_tech_salary_B6']:,.0f})", f0(b['current_techs']['sal']), "0", f0(b['current_techs']['tax']), f0(b['current_techs']['ben']), f0(b['current_techs']['total']), f"{b['current_techs']['hc_by_month'][0]:.0f} -> {b['current_techs']['hc_by_month'][-1]:.0f}"],
           ["Management & coordination (76-80)", "FO HC r21 Operations Coordinator, r25 Field Maintenance Manager (name + salary)", f0(b['current_named']['sal']), "0", f0(b['current_named']['tax']), f0(b['current_named']['ben']), f0(b['current_named']['total']), f"{b['current_named']['hc_by_month'][0]:.0f} -> {b['current_named']['hc_by_month'][-1]:.0f}"],
           [f"**Current staff (= FO HC {hc['FO']['n_people']})**", "", f0(fo['current']['sal']), "0", f0(fo['current']['tax']), f0(fo['current']['ben']), f"**{f0(fo['current']['total'])}**", f"{fo['current_hc_by_month'][0]:.0f} -> {fo['current_hc_by_month'][-1]:.0f}"],
           ["New-logo techs (26-35)", "ramp", f0(b['ramp_new_logo_techs']['sal']), f0(b['ramp_new_logo_techs']['nh']), f0(b['ramp_new_logo_techs']['tax']), f0(b['ramp_new_logo_techs']['ben']), f0(b['ramp_new_logo_techs']['total']), f"{b['ramp_new_logo_techs']['hc_by_month'][0]:.0f} -> {b['ramp_new_logo_techs']['hc_by_month'][-1]:.0f}"],
           ["Expansion techs (37-47)", "ramp", f0(b['ramp_expansion_techs']['sal']), f0(b['ramp_expansion_techs']['nh']), f0(b['ramp_expansion_techs']['tax']), f0(b['ramp_expansion_techs']['ben']), f0(b['ramp_expansion_techs']['total']), f"{b['ramp_expansion_techs']['hc_by_month'][0]:.0f} -> {b['ramp_expansion_techs']['hc_by_month'][-1]:.0f}"],
           ["Floaters (49-60)", "ramp (switch M14 = No)", f0(b['ramp_floaters']['sal']), f0(b['ramp_floaters']['nh']), f0(b['ramp_floaters']['tax']), f0(b['ramp_floaters']['ben']), f0(b['ramp_floaters']['total']), "0 -> 0"],
           ["Incremental supervisors (62-73)", "ramp", f0(b['ramp_supervisors']['sal']), f0(b['ramp_supervisors']['nh']), f0(b['ramp_supervisors']['tax']), f0(b['ramp_supervisors']['ben']), f0(b['ramp_supervisors']['total']), f"{b['ramp_supervisors']['hc_by_month'][0]:.0f} -> {b['ramp_supervisors']['hc_by_month'][-1]:.0f}"],
           ["**Ramp hires**", "", f0(fo['ramp']['sal']), f0(fo['ramp']['nh']), f0(fo['ramp']['tax']), f0(fo['ramp']['ben']), f"**{f0(fo['ramp']['total'])}**", f"{fo['ramp_hc_by_month'][0]:.0f} -> {fo['ramp_hc_by_month'][-1]:.0f}"],
           ["**Total = FO 5510 + 5530 + 5540**", "", f0(fo['current']['sal'] + fo['ramp']['sal']), f0(fo['ramp']['nh']), f0(fo['current']['tax'] + fo['ramp']['tax']), f0(fo['current']['ben'] + fo['ramp']['ben']), f"**{f0(fo['total'])}**", ""]],
          ["---", "---", "---:", "---:", "---:", "---:", "---:", "---"]))
A(f"FO ramp headcount Jan..Dec 27: {ints(fo['ramp_hc_by_month'])}. FO 5510 {f0(fo['pl_5510_5540']['5510'])} = salaries + new-hire cost (rows 21, 31, 34, 43, 46, 56, 59, 69, 72, 76, 77); "
  f"the split ties to FO!U52:AF54 in every month (checked to 1e-6).\n")
A(f"Reconciliation with the COO book's old FO (5510 {f0(fo['current_vs_hc']['coo_book_5510'])} = FO HC salary; 5510-5540 {f0(fo['current_vs_hc']['coo_book_total'])} = FO HC total): the SD current-staff block "
  f"has salary {f0(fo['current']['sal'])} ({f0(fo['current_vs_hc']['diff_sal'])}) and total {f0(fo['current']['total'])} ({f0(fo['current']['total'] - fo['current_vs_hc']['coo_book_total'])}). "
  f"The coordinator and manager match to the dollar ({f2(fo['match']['named'][0]['sd_2027'])} and {f2(fo['match']['named'][1]['sd_2027'])}). The techs differ only because the model uses "
  f"{B11:.0f} x {fo['inputs']['avg_tech_salary_B6']:,.0f} = {f0(fo['match']['techs_model_salary'])} where FO HC has {f0(fo['match']['techs_hc_salary'])} (2027 with the Oct-27 raise: "
  f"{f0(fo['match']['techs_model_2027'])} vs {f0(fo['match']['techs_hc_2027'])}), and the burden rates differ slightly (SD {pct(fo['inputs']['tax_B7'])} / {pct(fo['inputs']['ben_B8'])}, "
  f"FO HC {pct(hc['FO']['rate_tax'], 3)} / {pct(hc['FO']['rate_ben'], 3)}). So the old FO was the current 16 only; the SD build = the same 16 + "
  f"{f0(fo['ramp']['total'])} of ramp hires. One of the {B11:.0f} techs (FO HC r15) is also costed on Fld Eng Budget r15 (I-28).\n")
# PO
A("### PO: PO HC vs Prod Payroll and Logistics&WH Payroll (I-05, I-17)\n")
A(f"PO 5110-5140 ({f0(po['po_5100'])}) is exactly PO HC: {po['hc_people']} current staff ({titles('PO')}); headcount every 2027 month "
  f"{min(hc['PO']['hc_by_month_2027']):.0f} (min) to {max(hc['PO']['hc_by_month_2027']):.0f} (max), no hires, raise from Oct-27 like every roster.\n")
A(f"**How many of the {po['hc_people']} appear in the SD models?** Prod Payroll: **{po['in_pp_by_count']} of {po['hc_people']} by headcount** (its 'current staff on payroll (Sep-26)' is {pp['inputs']['B9']:.0f} lift + "
  f"{pp['inputs']['C9']:.0f} tray = {pp['current_hc']:.0f}, 0 supervisors; the model has no names or titles, so this is a count match, not a person match). "
  f"Logistics&WH: **1 of 9 by name** (PO HC r20 Material Handler = seat MH-01); PO HC r16 Material Handling Team Lead is named as the person seat MH-02 backfills "
  f"(from Oct-26), but r16 stays on PO HC through Dec-27. The Logistics&WH model also holds CO HC r17 Field Logistics Manager (seat LOG-01, by name). "
  f"If the {po['hc_people']} are Prod Payroll's current staff, PO HC r20 sits in both SD models; the net increments below take each person out once.\n")
A(mdtable(["", "PO HC / PO 5110-5140", "Prod Payroll (SD)", "Logistics&WH Payroll (SD, not carried)", "Both models"],
          [["Model 2027 total", "-", f0(pp["total"]) + f" (lift {f0(pp['lift_total'])}, tray {f0(pp['tray_total'])}, supervisors {f0(pp['sup_total'])})", f0(lw["total"]), f0(pp["total"] + lw["total"])],
           ["People already on an HC roster", f"{po['hc_people']} ({f0(po['po_5100'])})", f"{pp['current_hc']:.0f} current staff (count): model cost {f0(pp['current_only']['total'])}", f"{len(ovl)} seats: MH-01 (PO HC r20) {f0([e for e in ovl if 'MH-01' in e['seat']][0]['cost_2027'])}, LOG-01 (CO HC r17) {f0([e for e in ovl if 'LOG-01' in e['seat']][0]['cost_2027'])}", f0(pp["current_only"]["total"] + lw["overlap_cost"])],
           ["**Net increment (ramp) not in the budget**", "0", f"**{f0(I05)}** (I-05)", f"**{f0(I17)}** (I-17): {len(newseats)} seats", f"**{f0(I0517)}**"],
           ["Ramp headcount Jan-27 -> Dec-27", "0 -> 0", f"{ramp_hc[0]:.0f} -> {ramp_hc[-1]:.0f}", f"{lw['net_hc_by_month'][0]:.0f} -> {lw['net_hc_by_month'][-1]:.0f}", f"{po['net_combined_hc_by_month'][0]:.0f} -> {po['net_combined_hc_by_month'][-1]:.0f}"],
           [f"Gross gap vs PO 5100 (model total - {f0(po['po_5100'])})", "-", f0(po["pp_gross_gap"]), "n/a (different team)", "-"]],
          ["---", "---:", "---:", "---:", "---:"]))
A("Net increment = model total less the model's own cost of the people already on HC rosters (A-27), so it is the cost of the ramp hires at the model's rates. "
  f"The model costs the 9 current staff at {f0(pp['current_only']['total'])}, {f0(-po['pp_current_vs_po_hc']['diff'])} below PO 5100 ({f0(po['po_5100'])}): average salary "
  f"{pp['inputs']['B5']:,.2f} vs {po['pp_current_vs_po_hc']['hc_avg_salary']:,.2f}, and different burden (model tax {pct(pp['inputs']['B6'])}, benefits {pct(pp['inputs']['B7'])} lift / "
  f"{pct(pp['inputs']['C7'])} tray, plus the monthly absence coverage of Prod Payroll rows 33/54; PO HC {pct(hc['PO']['rate_tax'], 2)} / {pct(hc['PO']['rate_ben'], 2)}). That difference is not part of the net increment. "
  f"Ramp cost by component: salary {f0(pp['ramp_parts']['sal'])}, absence coverage {f0(pp['ramp_parts']['abs'])}, payroll tax {f0(pp['ramp_parts']['tax'])}, benefits "
  f"{f0(pp['ramp_parts']['ben'])}, new-hire cost {f0(pp['ramp_parts']['nh'])}. The model already has {po['sd_hires_sep_dec26']['lift']:.0f} lift, {po['sd_hires_sep_dec26']['tray']:.0f} tray and "
  f"{po['sd_hires_sep_dec26']['sup']:.0f} supervisor hires in Sep-Dec 26, so 2027 opens with {ramp_hc[0]:.0f} ramp staff.\n")
A("**Net ramp by month (2027)**\n")
mrows = [["Prod Payroll ramp headcount"] + [f"{x:.0f}" for x in ramp_hc] + [""],
         ["Prod Payroll ramp cost"] + [f0(x) for x in pp["ramp_by_month"]] + [f0(sum(pp["ramp_by_month"]))],
         ["Logistics&WH new seats (headcount)"] + [f"{x:.0f}" for x in lw["net_hc_by_month"]] + [""],
         ["Logistics&WH new seats cost"] + [f0(x) for x in lw["net_by_month"]] + [f0(sum(lw["net_by_month"]))],
         ["**Net ramp headcount, both**"] + [f"{x:.0f}" for x in po["net_combined_hc_by_month"]] + [""],
         ["**Net ramp cost, both**"] + [f0(x) for x in po["net_combined_by_month"]] + [f"**{f0(sum(po['net_combined_by_month']))}**"],
         ["Prod Payroll total headcount (incl. the 9)"] + [f"{x:.0f}" for x in pp["hc_total_by_month"]] + [""],
         ["  of which lift / tray / supervisors (Dec-27)", f"{pp['hc_by_month']['lift'][-1]:.0f} / {pp['hc_by_month']['tray'][-1]:.0f} / {pp['hc_by_month']['sup'][-1]:.0f}"] + [""] * 12]
A(mdtable(["Row"] + MON + ["2027"], mrows, ["---"] + ["---:"] * 13))
A("**Logistics&WH seats**\n")
A(mdtable(["Seat", "Team", "Start", "Annual base", "2027 cost (model rates)", "On an HC roster?", "In net increment"],
          [[e["seat"].replace("Logistics&WH ", ""), e["team"], e["start"], f0(e["annual"]), f0(e["cost_2027"]),
            (e.get("overlap_with", "") + " (name)") if e["overlap"] else ("; ".join(["backfills " + x for x in e["backfill_of"]] + ["title only: " + x for x in e["title_match_only"]]) or "no"),
            "no" if e["overlap"] else "yes"] for e in lw["seats"]],
          ["---", "---", "---", "---:", "---:", "---", "---"]))
A(f"Seats the model's own check block excludes: LOG-02 (Logistics&WH Payroll!A55; = FO HC r21 Operations Coordinator, budgeted in FO) and MH-05 (A56; in no model, I-27). "
  f"Model rates: tax {pct(lw['rates']['tax'])}, benefits {pct(lw['rates']['ben'])}; Python replica of the seat costs vs the SD cached values: max difference {lw['check_max_abs_diff']:.1e}.\n")
# CO
A("### CO\n")
A(f"CO 6610-6640 ({f0(sum(tie['CO']['v5'][k] for k in ('sal', 'tax', 'ben')))}) = CO HC: {hc['CO']['n_people']} people ({secs('CO')}), CO HC rates {pct(hc['CO']['rate_tax'], 2)} / {pct(hc['CO']['rate_ben'], 2)}. "
  "No SD model; CO HC r17 Field Logistics Manager is also seat LOG-01 of the not-carried Logistics&WH model (excluded from the I-17 net). Net increment 0.\n")
# FE
A("### FE: FE HC vs Fld Eng Budget (FE 6610-6640)\n")
A(mdtable(["Fld Eng Budget row", "Salary", "Start (SD)", "FE HC row", "Match", "Start (HC)", "2027 salary SD", "2027 salary HC", "Difference"],
          [[e["sd"].replace("Fld Eng Budget ", ""), f0(e["sd_salary"]), e["sd_start"], (e["hc"] or "-").replace("FE HC ", ""), e["basis"] or
            ("not on FE HC; same name as " + ", ".join(e["on_other_roster_by_name"]) if e.get("on_other_roster_by_name") else "not on FE HC"),
            e.get("hc_start", "-"), f2(e["sd_2027"]), f2(e["hc_2027"]) if e["hc"] else "-", f2(e["diff_2027"]) if e["hc"] else f2(e["sd_2027"])] for e in fe["rows"]]
          + [["Total", "", "", "", "", "", f2(fe["sd_total_sal"]), f2(fe["hc_total_sal"]), f2(fe["sd_total_sal"] - fe["hc_total_sal"])]],
          ["---", "---:", "---", "---", "---", "---", "---:", "---:", "---:"]))
A(f"FE HC r41 'Field Engineer' (new-hire block) has no name, salary or start (0 in FE HC); it may be the seat for Fld Eng Budget r15. Start months: FE HC has every current person "
  f"in seat from Sep-26 (Field Engineer Manager from Dec-26) and Fld Eng Budget starts everyone in Jan-27; for the matched people the 2027 monthly salary is identical "
  f"(max difference {fe['matched_max_monthly_diff']:.2f}), so the start months have no 2027 effect. COO book FE 6610 {f0(fe['coo_book']['sal'])} = FE HC {f0(fe['hc_total_sal'])} less "
  f"{', '.join(fe['coo_book_gap_rows'])} ({f0(fe['coo_book_gap_vs_hc'])}).\n")
A("**Burden rates (I-34)**\n")
A(mdtable(["FE 2027", "Salary base", "6630 payroll tax", "6640 benefits", "Total burden"],
          [[f"Budget: SD rates {pct(fe['sd_rates']['tax'])} / {pct(fe['sd_rates']['ben'])}", f0(fe["pl_v5"]["sal"]), f0(fe_b["sd_tax"]), f0(fe_b["sd_ben"]), f0(fe_b["sd_tax"] + fe_b["sd_ben"])],
           [f"At FE HC rates {pct(fe['hc_rates']['tax'], 3)} / {pct(fe['hc_rates']['ben'], 3)}", f0(fe["pl_v5"]["sal"]), f0(fe_b["hc_rate_tax"]), f0(fe_b["hc_rate_ben"]), f0(fe_b["hc_rate_tax"] + fe_b["hc_rate_ben"])],
           ["**Difference (budget higher)**", "", f"+{fe_b['diff_tax']:,.0f}", f"+{fe_b['diff_ben']:,.0f}", f"**+{fe_b['diff_total']:,.0f}**"]],
          ["---", "---:", "---:", "---:", "---:"]))
A(f"On the matched people only ({f0(fe_b['matched_base'])} of salary) the difference is +{fe_b['matched_diff_total']:,.0f}. FE HC's own burden on its {f0(hc['FE']['z']['sal'])} is "
  f"{f0(hc['FE']['z']['tax'])} + {f0(hc['FE']['z']['ben'])}.\n")
# PE
A("### PE\n")
A(f"PE 6610-6640 ({f0(sum(tie['PE']['v5'][k] for k in ('sal', 'tax', 'ben')))}) = PE HC: {hc['PE']['n_people']} people, PE HC rates {pct(hc['PE']['rate_tax'], 2)} / {pct(hc['PE']['rate_ben'], 2)}. No SD model. "
  f"PE HC r22 Head of Production and Delivery is marked '{pet['flag']}' in column A: 2027 cost {f0(pet['total_2027'])} (salary {f0(pet['sal_2027'])}, tax {f0(pet['tax_2027'])}, "
  f"benefits {f0(pet['ben_2027'])}), on no other roster (I-35).\n")
# duplicates
A("### Duplicate scan across all rosters (I-28)\n")
A("Rosters compared: FE HC, CO HC, PE HC, PO HC, FO HC, SD Fld Eng Budget, SD Fld Ops Payroll (named rows), SD Logistics&WH (seats), SD Prod Payroll (anonymous counts). "
  "Rule (A-29): name where present, otherwise title + salary + start; one-to-one. Names are not shown.\n")
A(mdtable(["Person A", "Person B", "Match basis", "Classification"], [[p["a"], p["b"], p["basis"], p["class"]] for p in dup["pairs"]]))
A(f"Head of Service Delivery: FE HC r16 and Fld Eng Budget r21 only; CO HC / PE HC name matches {len(hosd['co_pe_name_hits'])}, title matches {len(hosd['co_pe_title_hits'])}; "
  f"nearest title: {', '.join(hosd['near_titles'])}. No person appears on two HC tabs. Anonymous rows: Fld Ops Payroll's 14 current techs = the 14 FO HC field technicians "
  f"(count); Prod Payroll's {pp['current_hc']:.0f} current staff = PO HC {po['hc_people']} (count).\n")
A("### Roster-to-P&L map\n")
ms = R["mapping_summary"]
A(f"`02-build/02-build_roster_map_v6.csv` (no names): {ms['people']} roster rows ({', '.join(f'{k} {v}' for k, v in ms['by_roster'].items())}); each is mapped to exactly one P&L source "
  f"(unmapped: {ms['unmapped']}). The FE HC r41 open row maps to no cost. {ms['with_also']} rows carry a flag in 'also_in' (model overlaps, the FO/FE duplicate, the PE "
  f"'transfer?' row, the open FE row).\n")
# HC tabs
A("## HC tabs added to the workbook\n")
A(mdtable(["Tab", "From (workfile)", "Cells", "Formulas", "Part"], [[k, v["from"], f"{v['cells']:,}", f"{v['formulas']:,}", v["part"]] for k, v in B["sheets"].items()]))
A(f"Placed after Fld Eng Budget, in the order of the handoff. Copied cell by cell at the XML level with values, formulas (shared formulas kept), cached values, styles, "
  f"column widths, row heights, frozen panes, data validations and cell notes. Sheet references re-pointed ('PO HC'! -> 'HC-PO'!, ...); HC-COO reads only the other "
  f"five HC tabs. Shared strings were inlined (sharedStrings.xml untouched). Styles: {B['styles_appended']['cellXfs']} cell formats, {B['styles_appended']['fonts']} fonts, "
  f"{B['styles_appended']['fills']} fills, {B['styles_appended']['borders']} borders and {B['styles_appended']['numFmts']} number formats appended to styles.xml (existing "
  f"entries unchanged, so no existing cell changes format); {B['colours_resolved']['theme']} theme colours resolved to RGB because the workfile theme (Aptos) differs from v5's. "
  f"The hidden 'Claude Log' tab and the workfile P&L tabs were not copied (_2 stays the P&L source).\n")
A("External links stored as values (A-30): each dept HC tab reads its payroll tax and benefits rates (D6:D7) from an external T&B workbook ([1], not supplied). "
  "The 10 cells keep the workfile's cached values:\n")
A(mdtable(["Tab", "Cell", "Original formula (text)", "Stored value"], [[e["sheet"], e["cell"], "`" + e["formula"] + "`", f"{float(e['value']):.6%}"] for e in B["external_cells"]]))
if AN:
    h = AN["hc_tabs"]
    A(f"Checks: LibreOffice recalculation of v6, HC tabs: errors {h['errors']}, cached vs recalculated max difference {h['max_diff']:.1e} over {h['cells']:,} cells, "
      f"text mismatches {h['text_mismatch']}; formulas referencing a sheet outside the HC tabs {h['foreign_refs']}; external references {h['external_refs']}.\n")
else:
    A("Checks: [pass 1: pending]\n")
# HoSD (carried)
A("## Head of Service Delivery salary (I-26, resolved in v5)\n")
A(scrub(sec5["Head of Service Delivery salary (I-26, resolved in v5)"]).strip() + "\n- v6: the HC rosters confirm the person is on FE HC r16 (205,000, in seat from Sep-26) and "
  "nowhere else; Fld Eng Budget starts the row in Jan-27, which gives the same 2027 cost.\n")
# Build and sources
A("## Build and sources\n")
A(f"Output: `02-build/02-build_COO_2027_Budget_Collated_v6.xlsx` (v1-v5 files unchanged) and `02-build/02-build_roster_map_v6.csv`.  \n"
  f"Scripts: `02-build/scripts/` - v6 entry point `run_build_v6.sh`: prodpay_v6.py (scratch copy with the Prod Payroll XLOOKUP row replaced, analysis only) -> recalc.sh -> "
  f"recon_v6.py (reconciliation, roster map CSV) -> cnotes_v6.py (extracts the v5 Collation Notes, byte-exact round trip) -> build_v6.py (stage 1: v5 + HC tabs) -> "
  f"report_v6.py pass 1 (Collation Notes JSON) -> build_v6.py (final) -> diff_versions.py, recalc.sh, analyze_v6.py, recon_v6.py on v6 (figures must be identical) -> "
  f"report_v6.py pass 2 (JSON must equal pass 1) -> privacy_v6.py. Every v5 part other than workbook.xml, its rels, [Content_Types].xml, styles.xml (append only) and "
  f"Collation Notes is copied byte for byte. `run_build_v5.sh` ... `run_build.sh` still reproduce v5 ... v1.  \n"
  f"Inputs (read-only): `COO_HC_and_PL_workfile.xlsx` sha256 `{sha(WFILE)}` (new); `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `{sha(COO)}`; "
  f"`Service_Delivery_PL_worksheets.xlsx` sha256 `{sha(SD)}`; `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `{sha(NEW)}`.  \n"
  f"Recalculation engine: {lov}.  \n"
  f"Base: v5 workbook sha256 `{sha(V5X)}` (under verification in parallel when v6 was built).\n")
# Completion criteria
A("## Completion criteria (v6)\n")
if AN:
    c = AN
    A(mdtable(["Criterion", "Result"], [
        ["0 value diffs on the existing sheets vs v5", f"diff_versions.py on {c['diff']['total']['sheets']} sheets ({c['diff']['total']['cells']:,} cells): formula diffs {c['diff']['total']['formula_diffs']}, value diffs {c['diff']['total']['value_diffs']}; comments added / removed / changed {c['diff']['comments'][0]} / {c['diff']['comments'][1]} / {c['diff']['comments'][2]}. Collation Notes regenerated (excluded)."],
        ["Existing parts untouched", f"{c['package']['identical']} of {c['package']['v5_parts']} v5 parts byte-identical; changed: {', '.join(c['package']['changed'])}; styles.xml append-only: {c['package']['styles_append_only']}."],
        ["HC tabs present with 0 errors", f"{', '.join(c['hc_tabs']['names'])} after Fld Eng Budget: {c['hc_tabs']['order_ok']}; errors after recalculation {c['hc_tabs']['errors']}; cached vs recalculated max difference {c['hc_tabs']['max_diff']:.1e}; external references {c['hc_tabs']['external_refs']}; references outside the HC tabs {c['hc_tabs']['foreign_refs']}."],
        ["HC tabs tie to the P&L", f"HC-PO / HC-CO / HC-PE rows 67-69 vs PO / CO / PE payroll rows, every 2027 month: max difference {c['hc_tie']:.2e}."],
        ["Every roster person mapped to one P&L source, or flagged", f"{R['mapping_summary']['people']} rows mapped, unmapped {R['mapping_summary']['unmapped']}; flagged {R['mapping_summary']['with_also']}."],
        ["No new errors on existing sheets", f"New errors vs v5: {c['errors']['new']}."],
        ["Cached values are what the formulas give", f"LibreOffice recalculation of v6 vs stored values, existing sheets except Collation Notes: {c['recalc']['n_diff']} cells differ, max {c['recalc']['max_diff']:.1e}; non-numeric mismatches {c['recalc']['text_mismatch']}."],
        ["Collation Notes live formulas", f"{c['cn']['formulas']} formulas; recalc vs stored max diff {c['cn']['max_diff']:.1e}, text mismatches {c['cn']['text_mismatch']}."],
        ["Figures recompute from the final file", f"recon_v6.py with the v6 workbook in place of v5: identical output {c['recon_same']}."],
        ["No employee names in md, Collation Notes, CSV, message", f"privacy_v6.py on the pass-1 notes, the Collation Notes JSON and sheet, and the CSV: {c['privacy']}. It runs again on this file before it is copied; the build stops on any hit. The return message is checked the same way."],
    ]))
else:
    A("[pass 1: pending]\n")
# carried sections
for t in ("Depreciation schedule summary", "Unit-cost reconciliation", "Revenue"):
    A(f"## {t}\n"); A(sec5[t].strip() + "\n")
A("## Assumptions register\n")
asr5 = sec5["Assumptions register"]
asr5 = rep(asr5, "A-22..A-25 are new in v4; A-26 is new in v5;", "A-22..A-25 are new in v4; A-26 is new in v5; A-27..A-30 are new in v6;")
tab_end = asr5.index("\n\nA-22..A-25")
A(asr5[:tab_end].strip() + "\n" + "\n".join(md_issue(r) for r in ASR_NEW) + "\n" + asr5[tab_end:].rstrip() + "\n")
A("## DeploySum refresh and tie-out (v3 build; unchanged in v4-v6)\n")
A(sec5["DeploySum refresh and tie-out (v3 build; unchanged in v4 and v5)"].strip() + "\n")
A("## v5 -> v6 diff\n")
if AN:
    A(f"`diff_versions.py` (exact: formulas as text, cached values with no tolerance) on every sheet present in both files except Collation Notes:\n")
    A(mdtable(["Sheet", "Cells", "Formula diffs", "Value diffs"], [[k, f"{v['cells']:,}", v["formula_diffs"], v["value_diffs"]] for k, v in AN["diff"]["sheets"].items()]
              + [["**Total**", f"{AN['diff']['total']['cells']:,}", AN["diff"]["total"]["formula_diffs"], AN["diff"]["total"]["value_diffs"]]],
              ["---", "---:", "---:", "---:"]))
    A(f"Sheets only in v6: {', '.join(AN['diff']['only_new'])}. Sheets only in v5: {', '.join(AN['diff']['only_old']) or 'none'}. Package: {AN['package']['identical']} of {AN['package']['v5_parts']} v5 parts "
      f"byte-identical; changed: {', '.join(AN['package']['changed'])}; added: {len(AN['package']['added'])} parts (6 worksheets, their rels, 6 comment parts, 6 VML drawings).\n")
    A("## Error scan\n")
    A(mdtable(["Sheet", "v5", "v6"], [[k, v[0], v[1]] for k, v in AN["errors"]["by_sheet"].items()]))
    A(f"New errors in v6: **{AN['errors']['new']}**. Prod Payroll's #NAME? cells are the XLOOKUP rows LibreOffice cannot evaluate (I-05, I-25; evaluated for the analysis per A-28).\n")
    A("## Package\n")
    A(f"Parts {AN['package']['v6_parts']} (v5 {AN['package']['v5_parts']}); `xl/externalLinks/*` **{AN['package']['external_links']}**; defined names {AN['package']['defined_names']:,} (v5: {AN['package']['defined_names_v5']:,}).\n")
    A("## Sheets in the output\n")
    A(mdtable(["#", "Sheet", "State"], [[i + 1, s, st] for i, (s, st) in enumerate(AN["sheets"])]))
else:
    A("[pass 1: pending]\n")
A("## Severity scale\n"); A(sec5["Severity scale"].strip() + "\n")
A("## Issues (v6)\n")
A(f"Severity per the scale above. Open: {sev['HIGH']} HIGH, {sev['MED']} MED, {sev['LOW']} LOW; {sev['RESOLVED']} RESOLVED. v6: I-05 rewritten with the net increment and raised "
  f"to HIGH; I-17 and I-28 rewritten from the HC rosters; I-34, I-35 and I-36 new; I-15 and I-26 refer to people by dept + title + roster row. No other severity changed.\n")
iss_rest = iss_body[iss_body.index("| ID | Sev"):]
hdr = "\n".join(iss_rest.split("\n")[:2])
A(hdr + "\n" + "\n".join(iss_md.values()) + "\n")
var = iss_body[iss_body.index("### Variance scan"):]
var = rep(var, "### Variance scan: rows with |AG-N| > $50k and > 50% (recomputed from the v5 workbook)",
          "### Variance scan: rows with |AG-N| > $50k and > 50% (v5 workbook; unchanged in v6: 0 value diffs)")
A(var.strip() + "\n")
cd = scrub(sec5["Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5)"])
cd = rep(cd, "Result: 0 likely double counts on the same GL row. Unclear rows are logged as I-28.",
         "Result: 0 likely double counts on the same GL row. Unclear rows are logged as I-28. v6: the HC rosters answer the person-level question for "
         "rows 67-69 (no FE person on CO HC or PE HC); the one person costed twice sits on two different GL rows (FO 5510 and FE 6610), see I-28.")
A("## Cross-department, payroll and T&E checks (first built in v2; FE amounts recomputed in v5; unchanged in v6)\n")
A(cd.strip() + "\n")
A("## Decisions\n")
A(sec5["Decisions"].strip())
DEC6 = [
    "D1 (v6): Patch the v5 package, do not round-trip it. The HC tabs are transplanted at the XML level; every v5 part except workbook.xml, its rels, "
    "[Content_Types].xml, styles.xml (append only) and Collation Notes keeps its bytes, so the v5 -> v6 diff on the existing sheets is exactly 0.",
    "D2 (v6): HC tabs keep the workfile's own formulas and cached values; sheet references are renamed to the new tab names. The 10 T&B rate links are "
    "external and are stored as values (A-30), as DeploySum's external links were in v3. Theme colours are resolved to RGB because the two workbooks have different themes.",
    "D3 (v6): COO book _2 stays the P&L source (brief v4); the workfile's P&L tabs are not imported. PO, CO and PE payroll are identical anyway; FO and FE come from the SD models.",
    f"D4 (v6): Net increment = model total less the model's own cost of the people already on HC rosters (A-27). Both sides use the model's rates, so the net is the "
    f"ramp alone. The model-vs-PO HC cost difference on the same 9 people ({f0(po['pp_current_vs_po_hc']['diff'])}) is shown, not netted.",
    "D5 (v6): The Logistics Manager seat (LOG-01) is taken out of the I-17 net although it overlaps CO, not PO: the model's own note classifies it as Central "
    "Operations and the person is on CO HC.",
    "D6 (v6): Prod Payroll's 9 current staff are matched to the 9 PO HC people by headcount only (the model has no names or titles); stated as a count match.",
    "D7 (v6): The Field Engineer Manager is matched on title + salary although the start month differs (HC Dec-26; Fld Eng Budget!D20 calls its Jan-27 a placeholder); "
    "the 2027 cost is identical. Matching is one-to-one: a person matched by name is not matched again on title + salary (this keeps the four new Material Handler "
    "seats from matching PO HC r20, who is seat MH-01).",
    "D8 (v6): The FO/FE duplicate person (I-28) is not resolved in the budget (no budget change); both resolutions are quantified.",
    "D9 (v6): The range keeps v5's convention (lower end = quantified downsides added; upper end = I-32 full only) so v5 and v6 compare; the new upsides are listed, not added.",
    "D10 (v6): Carried v5 text that quoted employee names (I-15, I-26, one cross-department line) is rewritten with dept + title + roster row; the meaning is unchanged.",
    "D11 (v6): A roster-to-P&L map is written as a CSV with no names (roster, row, title, salary, start, P&L source, flags); per-person salaries appear there "
    "because the match rule uses them. The notes quote per-person amounts only where a finding needs them (I-28, I-35, the FO/FE and PO match evidence).",
]
A("\n".join(f"- {d}" for d in DEC6) + "\n")
A("## Not done / limits\n")
nd = sec5["Not done / limits"].strip()
nd = rep(nd, "- v5: the workbook cannot confirm the Head of Service Delivery is not also inside CO or PE typed SG&A payroll (I-28 open); the salary is assumed to be the current rate, raised from Oct-27 like the rest of the roster.",
         "- v5: the workbook could not confirm the Head of Service Delivery is not also inside CO or PE typed SG&A payroll; v6 confirms it from the HC rosters (I-28). The salary is the current rate, raised from Oct-27 like the rest of the roster.")
A(nd)
A("- v6: no budget value was changed. The payroll findings (I-05, I-17, I-28, I-34, I-35, I-36) are exposures and decisions for the owners and the user.")
A("- v6: Prod Payroll has no names or titles, so its overlap with PO HC is a headcount match; Fld Ops Payroll's 14 current techs are matched to FO HC the same way.")
A("- v6: the HC tabs' T&B rates are the workfile's cached values (the T&B workbook was not supplied). The HC tabs are provenance only: no budget cell reads them.")
A("- v6: not opened in Microsoft Excel. The HC tabs keep the workfile's formulas and were recalculated in LibreOffice with 0 errors; the Prod Payroll tray / supervisor "
  "figures come from the scratch evaluation (A-28), not from cells in this workbook (which still show #NAME? in LibreOffice).")
A("- v6: whether the FO/FE person moved departments, whether the PE row transfers, and which burden rates FE should use are owner questions; the notes quantify each answer.\n")
md = "\n".join(L)
open(OUT_MD, "w").write(md)
print(f"report_v6: md {len(md):,} chars; Collation Notes JSON {len(cnj):,} chars; issues {dict(sev)}; contribution {f0(C)}; "
      f"I-05 net {f0(I05)}, I-17 net {f0(I17)}; range {f0(RANGE[0])} to {f0(RANGE[1])}; pass {'2' if AN else '1'}")
