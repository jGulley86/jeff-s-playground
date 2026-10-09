"""Write 02-build_notes_v3.md and the Collation Notes content (JSON) from the v3 analysis.

Usage:
  python3 -I report_v3.py V2_MD RES_JSON EXT_JSON LO_VERSION_TXT COO SD NEW OUT_NOTES_JSON OUT_MD XLSX_NAME

Every number comes from RES_JSON / EXT_JSON (analyze_v3.py, build_v3.py). The v2 notes are read to carry the
unchanged v2 issues and the v2 sections that v3 does not touch (FO/FE/CO/PE and PO payroll are unchanged).
"""
import sys, json, re, hashlib, collections

(V2_MD, RES, EXT, LOV, COO, SD, NEW, OUT_JSON, OUT_MD, NAME) = sys.argv[1:11]
res = json.load(open(RES)); ext = json.load(open(EXT))
lov = open(LOV).read().strip()
v2md = open(V2_MD).read()
lay = ext["layout"]
dep = res["dep"]; H = res["headline"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def f0(x):
    if x is None: return ""
    x = float(x)
    if abs(x) < 0.5: return "0"
    return f"({abs(x):,.0f})" if x < 0 else f"{x:,.0f}"


def f2(x):
    if x is None: return ""
    x = float(x)
    return f"({abs(x):,.2f})" if x < 0 else f"{x:,.2f}"


def pct(a, b):
    return f"{(a - b) / abs(b) * 100:.0f}%" if b else "n/a"


R = lambda r: str(r)
gl_lab = {"19": "5010 SlipBot", "20": "5011 SlipLift", "21": "5012 SlipCarrier (SlipTray)", "22": "5020 Robot Peripherals"}
rv = res["revenue"]; cap = res["capex"]; q4 = dep["q4_gap"]; st = dep["steps"]
run = dep["runrate"]; fyc = dep["fy_calc"]; po26 = dep["po_2026_N"]
exist_fy = {k: 12 * v for k, v in run.items()}
new_fy = {"19": 0.0, "20": dep["new_fy"]["lift"], "21": dep["new_fy"]["tray"], "22": dep["new_fy"]["periph"]}
tot_dep = sum(fyc.values()); tot_exist = sum(exist_fy.values()); tot_new = sum(new_fy.values())
dec_new = {"19": 0.0, "20": dep["dec27_monthly"]["20"] - run["20"], "21": dep["dec27_monthly"]["21"] - run["21"],
           "22": dep["dec27_monthly"]["22"] - run["22"]}
delay_sens = sum(dec_new.values())        # one month of every 2027 vintage = Dec-27 new monthly total
periph = dep["periph"]
d = res["diff"]
NI = H["Net Income"]; REV = H["Revenue"]; COGS = H["COGS"]; GP = H["Gross Profit"]; OPEX = H["Opex"]
DEP = H["Depreciation (rows 19-22)"]; TC = H["Total cost (COGS+Opex)"]; CX = H["Cost excl. depreciation"]
sch = "Depreciation Schedule"
OUT = lay["out_row"]
cnt_ext = len(ext["ext"])
pp = res["errors"]["Prod Payroll"]

# ------------------------------------------------------------------ issues
v2_issues = collections.OrderedDict()
for line in v2md.splitlines():
    m = re.match(r"^\| (I-\d\d) \| (\w+) \|", line)
    if m:
        v2_issues[m.group(1)] = line
cells = lambda line: [c.strip() for c in line.strip().strip("|").split(" | ")]
iss = collections.OrderedDict((k, cells(v)) for k, v in v2_issues.items())
v2sev = {k: v[1] for k, v in iss.items()}


def setrow(i, sev, loc, finding, evidence, impact, basis, action):
    iss[i] = [i, sev, loc, finding, evidence, impact, basis, action]


setrow("I-01", "MED", "PO!U12:AF12; PO!R12; PO!U13:AF13; PO!U15:AF15; DeploySum!F40:Q40",
       f"Resolved by assumption in v3. 2027 revenue is now budgeted: PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27; row 39 in the 9/30/26 file), all to 4100 Subscription/Platform Fees (orchestrator assumption). PO!R12 set to 'Manual'. Still open: 4500 Implementation Fees and 4900 One-Time Revenue stay 0 in 2027, and the source does not say whether recognized revenue includes them.",
       f"PO!AG12 = {f2(rv['sum_po'])}; DeploySum FY27 recognized revenue (9/30/26 file R39) = {f2(rv['R39_newfile'])}; difference {f2(rv['diff'])}. 2026: 4500 {f0(res['po_2026_rev']['13'])}, 4900 {f0(res['po_2026_rev']['15'])}. Cross-check Sep-Dec 26: DeploySum recognized revenue {f0(sum(rv['sepdec26_deploysum']))} vs PO 4100 forecast (PO!J12:M12) {f0(sum(rv['sepdec26_po4100']))} (difference {f0(sum(rv['sepdec26_deploysum']) - sum(rv['sepdec26_po4100']))}), so the 4100 mapping is consistent with how PO forecasts 2026.",
       f"not determinable (2026 4500+4900 = {f0(res['po_2026_rev']['13'] + res['po_2026_rev']['15'])})",
       "impact not determinable; owner confirmation needed",
       "Finance/PO owner to confirm the 4100 mapping and whether 2027 implementation or one-time revenue should be budgeted on 4500/4900.")
setrow("I-03", "LOW", "DeploySum!A3:R49 (Collation Notes lists the formulas)",
       f"Resolved in v3. DeploySum rows 3-49 now hold the resolved values from 2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx. The {cnt_ext} cells that link to the external workbook '[1]' are stored as that file's cached values; their formula text is on Collation Notes. The links are still not live (the [1] workbook was not supplied), so the next plan update needs a new resolved export.",
       f"DeploySum errors: v2 {res['errors']['DeploySum']['v2']}, v3 {res['errors']['DeploySum']['v3'] or 'none'} ({res['resolved_errors'].get('DeploySum', 0)} resolved). Every mapped cell B:R equals the 9/30/26 cached value (mismatches: {len(res['deploysum_value_mismatch'])}). New-file sha256 {sha(NEW)[:16]}...",
       "0", "hygiene", "Refresh DeploySum from a new resolved export when the plan changes. Keep the row map (ARR row 39 kept).")
tr = res["tie_rows"]
setrow("I-04", "LOW", "DeploySum!B53:R66; DeploySum!A69:R76 (v3 check block)",
       "The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (rows 53-66) are still typed values. v3 adds a live check: they now tie to the resolved rows 16-21 in every month Sep-26..FY27. So the FO/FE drivers are consistent with the 9/30/26 plan; they are just not linked.",
       "; ".join(f"{k}: FY {f0(v['FY_top'])} vs {f0(v['FY_split'])}, max monthly diff {f0(v['max_abs_month'])}" for k, v in tr.items()) + f". DeploySum!A76 = '{res['tieout_status']}'.",
       "0", "hygiene", "Optional: replace rows 54-64 with formulas (or document the source) so they update with the plan.")
setrow("I-05", "MED", "Prod Payroll!B24:S81 (hidden); Prod Payroll!S41; PO!AG33:AG36",
       f"The production payroll model now partly computes. It reads DeploySum rows 4, 24, 25, 27 and 28, which v3 resolved. Errors fell from {sum(pp['v2'].values())} to {sum(pp['v3'].values())}. The remaining {sum(pp['v3'].values())} are #NAME?: {res['pp_name_xlookup']} cells use _xlfn.xlookup (row 48), which LibreOffice {lov.split()[1] if len(lov.split()) > 1 else ''} does not support, and the rest are in rows {res['pp_name_rows'][1]}-{res['pp_name_rows'][-1]} below them (#NAME? propagates). Excel may evaluate them; not tested. It still feeds no budget value: FO/FE/CO/PE show 0 diffs and PO payroll rows are typed. Now that it computes, 'Total lift payroll' 2027 is far above PO's typed production labour.",
       f"Prod Payroll!S41 'Total lift payroll' (F:Q = Jan-Dec 27) = {f0(res['pp_S41'])}; tray (row 62), supervisor (row 79) and total (row 81) are still #NAME? in LibreOffice. PO 'Total - 5100 - Labor Expense - Production' AG36 = {f0(res['po_5100_AG36'])} (typed rows 33-35). Cells read from Prod Payroll by other sheets: typed raise inputs only (M5, M6, M9), unchanged.",
       f"not determinable (exposure: lift payroll alone {f0(res['pp_S41'])} vs PO 5100 {f0(res['po_5100_AG36'])})",
       "impact not determinable; owner confirmation needed",
       "PO owner to say which production payroll is right: the typed PO 5110-5140, or this model (open it in Excel to evaluate the XLOOKUP rows). See also I-17.")
setrow("I-07", "MED", f"PO!U19:AF22; '{sch}'!A1:S{lay['r7'] + 5}; COO P&L!AG19:AG22",
       f"Resolved by assumption in v3. 2027 depreciation is now budgeted from the new '{sch}' tab: straight-line, SlipLift 84 months, SlipTray 120 months, no salvage, full month from the go-live month. Existing fleet = PO Dec-26 run rate, carried flat. New units = DeploySum 2027 go-lives (rows 19/20). PO!R19:R22 set to 'Manual'. The open parts are logged separately: I-31 (Q4-26 go-lives), I-32 (existing-fleet run rates, SlipBot) and I-33 (peripherals).",
       f"2027 depreciation {f0(tot_dep)} (2026 {f0(sum(po26.values()))}): existing fleet {f0(tot_exist)}, new 2027 go-lives {f0(tot_new)}. By GL: " + "; ".join(f"{gl_lab[k]} {f0(fyc[k])}" for k in ("19", "20", "21", "22")) + f". Python recompute from raw inputs vs workbook, all 48 GL-months: max diff {dep['max_abs_diff']:.2e}.",
       "not determinable (component decisions in I-31..I-33)", "impact not determinable; owner confirmation needed",
       "PO owner/Finance to confirm the run-rate approach against the fixed-asset register, and resolve I-31..I-33.")
var = res["variance"]
coo_var = sorted([v for v in var if v[0] == "COO P&L" and re.match(r"^\d{4} ", str(v[2] or ""))], key=lambda v: -abs(v[5]))[:4]
iss["I-11"][4] = f"v3 values: {len(var)} rows (v2: 98). Largest COO P&L GL moves: " + "; ".join(f"COO P&L!N{v[1]} {f0(v[3])} -> AG{v[1]} {f0(v[4])}" for v in coo_var) + "."
iss["I-11"][3] = f"{len(var)} rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k (v3 values; list below)."
iss["I-20"][3] = "SD has 3 hidden sheets; Prod Payroll is carried and kept hidden, the others are not carried (FO/FE do not depend on them). DeploySum row visibility for rows 3-49 now follows the 9/30/26 file."
iss["I-20"][4] = f"Hidden in output: ['Prod Payroll']. DeploySum hidden rows v2 {res['hidden_rows_v2']} -> v3 {res['hidden_rows_v3']} (rows 30, 32-36 and recognized revenue row 40 are now visible, as in the 9/30/26 file)."
iss["I-20"][2] = "SD sheets Prod Payroll, Old Draft, Fld Maint T&E Data (hidden); DeploySum!A41:A42 (hidden rows 41-42)"
iss["I-23"][3] = f"COO P&L row 65 (labelled 'Expense') holds an unlabelled gross-margin % formula (=IFERROR(B64/B16,\"\")). With 2027 revenue now budgeted, it shows a 2027 margin (AG65 = {res['coo_row65']['AG'] * 100:.1f}%). Row 141 shows an extreme ratio for Feb-26 caused by negative 2026 payroll postings."
iss["I-25"][3] = "Side effects of moving from Google Sheets to xlsx: threaded comments become plain notes (text kept); Google's '#ERROR!' has no Excel equivalent; LibreOffice saves error constants as '=#REF!' formulas. v3: DeploySum no longer has errors; Prod Payroll's remaining errors are now #NAME? (LibreOffice has no XLOOKUP), not #REF!."
iss["I-25"][4] = f"Errors v2 -> v3: DeploySum {res['errors']['DeploySum']['v2']} -> none; Prod Payroll {pp['v2']} -> {pp['v3']}. New errors: {len(res['new_errors'])}."
iss["I-25"][2] = "Prod Payroll!B24:S81; DeploySum!A1 (notes)"

relabel = res["relabel"]
setrow("I-30", "LOW", "DeploySum!" + ", ".join(x[0] for x in relabel),
       f"The source labels say '$000s', but the values are whole dollars. v3 relabelled the {len(relabel)} cells to '$' (A2 text: 'Dollars in $ (relabelled in v3; the source said $000s)'). Each cell has a comment quoting the original label, so the change is visible, not silent.",
       "E.g. DeploySum!R13 total bookings 29,452,766 and R29 Production CapEx 32,410,900 are dollars: CapEx = units x unit cost in dollars (section 'Unit-cost reconciliation'), and recognized revenue is the same order as PO's 2026 revenue in dollars.",
       "0", "hygiene", "Plan owner to fix the labels in the source (Revenue Roll-up / Deploy) so the next export is right.")
setrow("I-31", "LOW", f"'{sch}'!A{lay['m5'] - 2}:D{lay['m5'] + 7}; PO!J20:M22; DeploySum!C19:E20",
       f"Oct-Dec 26 go-lives are carried in the PO Dec-26 run rate (not added explicitly, so there is no double count). The PO forecast steps up for Q4-26 go-lives, but by fewer units than the 9/30/26 DeploySum: it covers {st['20']['dec_minus_sep'] / (65000 / 84):.0f} lifts and {st['21']['dec_minus_sep'] / (8000 / 120):.0f} trays, against DeploySum's {sum(dep['q4_deploysum']['lifts'])} lifts and {sum(dep['q4_deploysum']['trays'])} trays. The 5020 step-ups cannot be reproduced from DeploySum's peripheral cost.",
       f"PO 5011 monthly step-ups Oct/Nov/Dec: {', '.join(f2(x) for x in st['20']['steps'])} = {', '.join(f'{x:.0f}' for x in st['20']['units'])} lifts x 65,000/84. 5012: {', '.join(f2(x) for x in st['21']['steps'])} = {', '.join(f'{x:.0f}' for x in st['21']['units'])} trays x 8,000/120. 5020: {', '.join(f2(x) for x in st['22']['steps'])} = {', '.join(f'{x:.2f}' for x in st['22']['units'])} peripheral sets at {f2(periph)}/84 (not whole). DeploySum Oct/Nov/Dec lifts {dep['q4_deploysum']['lifts']}, trays {dep['q4_deploysum']['trays']}. Gap not budgeted: {q4['lifts']:.0f} lifts + {q4['trays']:.0f} trays = {f2(q4['monthly'])}/month, {f0(q4['annual'])} for 2027 (plus up to {f0(q4['periph_if_missing_annual'])} if Q4-26 lift peripherals are not in 5020).",
       f"{f0(q4['annual'])} (up to {f0(q4['annual'] + q4['periph_if_missing_annual'])} with peripherals)",
       f"impact {f0(q4['annual'])}",
       "User/PO owner to choose: keep the PO run rate (current), or replace the Q4-26 step-ups with DeploySum's Oct-Dec 26 go-lives (Sep-26 run rate + explicit vintages). Do not do both.")
setrow("I-32", "HIGH", f"'{sch}'!B21:B24; PO!M19:M22; PO!U19:AF19",
       f"Existing-fleet depreciation is carried flat at the PO Dec-26 run rate for all 12 months of 2027, as the handoff instructed. The workbook has no asset register, so it cannot show whether any of these assets reach the end of their life, or are retired, in 2027. The largest line is 5010 SlipBot: {f2(run['19'])}/month = {f0(exist_fy['19'])} in 2027. Whether the SlipBot fleet is fully depreciated, retired or ongoing is not in the files. DeploySum note 4 says no SlipBots are built and existing bots are redeployed, which suggests the fleet is in use. 5020's run rate basis is also unknown (I-31).",
       f"Dec-26 run rates (PO!M): 5010 {f2(run['19'])}, 5011 {f2(run['20'])}, 5012 {f2(run['21'])}, 5020 {f2(run['22'])}; 2027 existing total {f0(tot_exist)}. 5010 2026 actuals Jan-Aug {f2(dep['po2026']['19'][0])} -> {f2(dep['po2026']['19'][7])}, forecast Sep-Dec flat {f2(dep['po2026']['19'][8])}; 2026 total {f0(po26['19'])}.",
       f"up to {f0(exist_fy['19'])} (5010); {f0(tot_exist)} all existing lines",
       f"impact {f0(exist_fy['19'])}",
       "USER DECISION: confirm SlipBot fleet status (fully depreciated / retired / ongoing) and the end-of-life month for any existing asset group. Change the section 2 input on the schedule if the run rate stops.")
setrow("I-33", "MED", f"'{sch}'!B7, B11, B16; PO!U22:AF22",
       f"SlipLift peripherals ({f2(periph)} per lift, from DeploySum CapEx) are depreciated on 5020 Robot Peripherals over 84 months. Both the GL and the life are builder assumptions: the user gave lives for SlipLifts and SlipTrays only. 5020 was chosen because PO's 2026 forecast books 5011 at exactly $65,000/84 per lift, so PO keeps peripherals out of 5011.",
       f"2027 new-peripheral depreciation {f0(new_fy['22'])} (Dec-27 {f2(dec_new['22'])}/month). Moving it to 5011 changes the GL split only, not the total. A different life changes the amount in proportion (e.g. 60 months: {f0(new_fy['22'] * 84 / 60)}).",
       f0(new_fy['22']), f"impact {f0(new_fy['22'])}",
       "User to confirm the peripherals GL (5020 or 5011) and life; both are input cells.")

order = list(iss.keys())
order = sorted(order, key=lambda k: int(k[2:]))
sev_count = collections.Counter(iss[k][1] for k in order)

change_reason = {
    "I-01": "Resolved by assumption (revenue linked to DeploySum); residual 4500/4900 question. HIGH -> MED.",
    "I-03": "Resolved: DeploySum refreshed from the 9/30/26 resolved file; 0 errors. HIGH -> LOW.",
    "I-04": "Typed drivers now tie to resolved rows 16-21 (live check). HIGH -> LOW.",
    "I-05": "Prod Payroll now partly computes; lift payroll 2027 far above PO 5100. LOW -> MED.",
    "I-07": "Resolved by assumption (Depreciation Schedule); open parts split to I-31..I-33. HIGH -> MED.",
    "I-11": "Evidence refreshed with v3 values.",
    "I-20": "DeploySum hidden rows now follow the 9/30/26 file.",
    "I-23": "Row 65 now shows a 2027 margin.",
    "I-25": "DeploySum errors gone; Prod Payroll error code now #NAME?.",
}

# ------------------------------------------------------------------ markdown
L = []
A = L.append
A("# 02-build notes v3 - 2027 COO budget collation")
A("")
A(f"Output: `02-build/{NAME}` (v1 and v2 files are unchanged)  ")
A("Scripts: `02-build/scripts/` - v3 entry point `run_build_v3.sh` (build_v3.py, recalc.sh, analyze_v3.py, report_v3.py). It starts from the delivered v2 workbook; `run_build_v2.sh` still reproduces v2 and `run_build.sh` reproduces v1.  ")
A(f"Inputs (read-only): `COO_Dept_PLs_2027_Budget_2.xlsx` sha256 `{sha(COO)}`; `Service_Delivery_PL_worksheets.xlsx` sha256 `{sha(SD)}`; **new** `2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx` sha256 `{sha(NEW)}`  ")
A(f"Briefs: `00-brief/brief_v2.md`, `00-brief/brief_v3.md` (user decision 2026-10-09: Option 3, straight-line, SlipLift 7 yrs, SlipTray 10 yrs, 'Trays = carriers').  ")
A(f"Recalculation engine: {lov} (headless, recalc on load).")
A("")
A("## Headline")
A("")
A("| Line | COO P&L row | 2026 (N) | 2027 v3 (AG) | Change | % | 2027 v2 (AG) |")
A("|---|---|---:|---:|---:|---:|---:|")
for lab in ["Revenue", "COGS", "Depreciation (rows 19-22)", "Gross Profit", "Opex", "Net Ordinary Income", "Net Other Income", "Net Income"]:
    h = H[lab]
    nm = {"Depreciation (rows 19-22)": "  of which depreciation (in COGS)"}.get(lab, lab)
    A(f"| {'**' + nm + '**' if lab in ('Net Income',) else nm} | {h['row']} | {f0(h['N'])} | {f0(h['AG'])} | {f0(h['AG'] - h['N'])} | {pct(h['AG'], h['N'])} | {f0(h['AG_v2'])} |")
A("")
A(f"- **Full 2027 Net Income (COO P&L AG132): {f0(NI['AG'])}** vs 2026 {f0(NI['N'])}. This includes 2027 revenue of {f0(REV['AG'])} (orchestrator assumption: all to 4100) and depreciation of {f0(DEP['AG'])}.")
A(f"- **Cost-only view:** total COO cost (COGS + Opex, AG63 + AG116) {f0(TC['AG'])} vs 2026 {f0(TC['N'])} (change {f0(TC['AG'] - TC['N'])}, {pct(TC['AG'], TC['N'])}). Excluding depreciation: {f0(CX['AG'])} vs 2026 {f0(CX['N'])}. The v2 cost total was {f0(TC['AG_v2'])}, so the only cost change from v2 is the new depreciation, {f0(TC['AG'] - TC['AG_v2'])}.")
A(f"- 2027 gross margin (AG65) {res['coo_row65']['AG'] * 100:.1f}%. The 2027 Net Income is now complete in scope, but it rests on the assumptions below. Three need a user decision: SlipBot run rate (I-32), Q4-26 go-lives (I-31) and peripherals (I-33).")
A(f"- Checks: COO P&L roll-up {res['rollup']['cells']} cells, {res['rollup']['fails']} off by more than $1 (max {res['rollup']['max_abs_diff']:.1e}); FO/FE/CO/PE vs v2 **0 formula and 0 value diffs** (CO {d['CO']['float_noise_cells']} and PE {d['PE']['float_noise_cells']} cells differ by < 1e-9 from LibreOffice recalculation order; no input changed); revenue tie {f2(rv['diff'])}; depreciation recompute max diff {dep['max_abs_diff']:.1e}; new errors **{len(res['new_errors'])}**; externalLink parts **{res['package']['externalLink_parts']}**; defined names {res['package']['defined_names']:,}.")
A(f"- Issues: {sev_count['HIGH']} HIGH, {sev_count['MED']} MED, {sev_count['LOW']} LOW (v2: 6 HIGH, 7 MED, 16 LOW).")
A("")
A("## Changes from v2")
A("")
A("| # | Area | What v3 did | Where |")
A("|---|---|---|---|")
A(f"| 1 | DeploySum refresh | Rows 3-49 replaced from the 9/30/26 resolved file, mapped by label. The new file has no ARR row, so new rows 39-49 go to rows 40-50 and row 39 (ARR) is kept empty. {cnt_ext} '[1]' cells stored as cached values (formula text on Collation Notes); {ext['kept_formulas']} internal formulas kept. The 17 v2 'stale external-link value' comments on B17:R17 were removed. | DeploySum!A3:R50 |")
A(f"| 2 | Tie-out | Live check of rows 16-21 against split rows 54-64, every month: all 0, '{res['tieout_status']}'. | DeploySum!A69:R76 |")
A(f"| 3 | '$000s' labels | {len(relabel)} labels relabelled to '$', each with a comment quoting the source label (I-30). | DeploySum col A |")
A(f"| 4 | Revenue | PO!U12:AF12 = DeploySum!F40:Q40 (recognized revenue Jan-Dec 27). PO!R12 = 'Manual'; note in PO!AI12. 4500/4900 unchanged (0). | PO row 12 |")
A(f"| 5 | Depreciation | New visible tab '{sch}': inputs, existing-fleet lines, vintage calc by month (12 go-live months x lifts/trays/peripherals), output by GL, memo checks. PO!U19:AF22 link to output rows {OUT['19']}-{OUT['22']}; PO!R19:R22 = 'Manual'; notes in PO!AI19:AI22. | '{sch}'; PO rows 19-22 |")
A("| 6 | Collation Notes | Rebuilt for v3 (assumptions, live headline, issues, external-formula list). | Collation Notes |")
A(f"| 7 | Row visibility | DeploySum rows 3-49 follow the 9/30/26 file: v2 hidden {res['hidden_rows_v2']} -> v3 {res['hidden_rows_v3']}. Recognized revenue (row 40) is visible because it now feeds PO. | DeploySum |")
A("")
A("Issue-level changes (severity v2 -> v3):")
A("")
A("| ID | v2 | v3 | Change |")
A("|---|---|---|---|")
for k in order:
    if k in change_reason or k not in v2sev:
        A(f"| {k} | {v2sev.get(k, 'new')} | {iss[k][1]} | {change_reason.get(k, 'New in v3.')} |")
A("")
A("All other v2 issues are carried unchanged (FO, FE, CO, PE and the PO non-revenue, non-depreciation lines did not change).")
A("")
A("## Completion criteria")
A("")
A("| Criterion | Result |")
A("|---|---|")
A(f"| COO P&L = FO+PO+CO+FE+PE on all cells | {res['rollup']['cells']} additive cells (rows 9-141, B:N and U:AG; ratio formulas excluded), {res['rollup']['fails']} failures, max abs diff {res['rollup']['max_abs_diff']:.1e}. Check row 133 max abs {res['check_row_133_max']:.1e}. |")
A(f"| FO/FE/CO/PE and untouched PO rows: 0 diffs vs v2 | FO, FE, CO, PE: 0 formula / 0 value diffs (table below). PO: formula changes only in rows 12, 19-22 (R, U:AF, AI); value changes only in those rows, their subtotals (14, 16, 37, 63, 64, 117, 132) and the AH '% of total revenue' column. PO formula changes outside the edited rows: {len(res['po_formula_changes_outside_lines'])}. COO P&L formula changes: {len(res['coo_formula_changes'])}. |")
A(f"| PO row 12 2027 = DeploySum Jan-Dec 27 recognized revenue within $1 | PO!U12:AF12 sum {f2(rv['sum_po'])}; 9/30/26 file F39:Q39 sum {f2(rv['sum_src'])}, R39 {f2(rv['R39_newfile'])}; diff {f2(rv['diff'])}. |")
A(f"| Depreciation recomputes by hand for a sampled month | Jun-27 shown below; Python recompute of all 48 GL-months from raw inputs: max diff {dep['max_abs_diff']:.1e}. |")
A(f"| 0 new errors (excluding resolved DeploySum cells); 0 externalLink parts | New errors {len(res['new_errors'])}. Resolved: DeploySum {res['resolved_errors'].get('DeploySum', 0)}, Prod Payroll {res['resolved_errors'].get('Prod Payroll', 0)}. externalLink parts {res['package']['externalLink_parts']}, externalReference elements {res['package']['externalReference_elements']}. |")
A("| Every assumption registered | Assumptions register below (A-01..A-21), each with its source or 'user-confirmed' / 'orchestrator assumption' / 'builder assumption'. |")
A("")
A("## Depreciation schedule summary")
A("")
A(f"Tab `{sch}` (visible, after DeploySum). Method: straight-line, no salvage, full month of depreciation from the go-live month (input B13 = 0; set 1 to start the month after). New units = DeploySum rows 19/20 (units going live), Jan-Dec 27. Existing fleet = PO Dec-26 monthly run rate, carried flat. Output = SUMIF by GL over all calc lines, then PO!U19:AF22.")
A("")
A("**Inputs**")
A("")
A("| Input | Value | Cell | Source |")
A("|---|---:|---|---|")
A(f"| SlipLift unit cost | 65,000.00 | B6 | DeploySum!A46 note 3: 'SlipLift $65,000' |")
A(f"| SlipLift peripherals per lift | {f2(periph)} | B7 | Derived: (R29 {f0(cap['R29'])} - R25 {cap['R25']:,} x 8,000) / R24 {cap['R24']} - 65,000. Note 3 prints '$4,138' (TEXT format rounds to whole dollars). |")
A("| SlipTray unit cost | 8,000.00 | B8 | DeploySum!A46 note 3: 'SlipTray $8,000' |")
A("| SlipLift life | 84 months | B9 | user-confirmed (7 years) |")
A("| SlipTray life | 120 months | B10 | user-confirmed (10 years) |")
A("| Peripherals life | 84 months (=B9) | B11 | builder assumption (I-33) |")
A("| Salvage | 0% | B12 | user-confirmed / brief v3 |")
A("| Start delay after go-live month | 0 | B13 | brief v3 convention (labelled input) |")
A("| GL SlipLift / SlipTray / peripherals | 5011 / 5012 / 5020 | B14:B16 | user-confirmed / user-confirmed / builder assumption |")
A("")
A("**Units (DeploySum, 9/30/26)**: 2027 go-lives " + f"{dep['dec_units_lift']} SlipLifts and {dep['dec_units_tray']:,} SlipTrays (R19/R20; = SD rows 55+58+61 and 56+59+62). By month (Jan..Dec 27): lifts {dep['lifts_go']}; trays {dep['trays_go']}. Unit-months in service in 2027: lifts {dep['unit_months_lift']:,}, trays {dep['unit_months_tray']:,}. No SlipBots go live or are built (rows 21/26 = 0; note 4).")
A("")
A("**Depreciation by GL, existing vs new**")
A("")
A("| GL | 2026 (PO N) | Existing: Dec-26 run rate /month | Existing 2027 | New 2027 go-lives: 2027 | New: Dec-27 /month | Total 2027 | Jan-27 /month | Dec-27 /month |")
A("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for k in ("19", "20", "21", "22"):
    A(f"| {gl_lab[k]} (PO row {k}) | {f0(po26[k])} | {f2(run[k])} | {f0(exist_fy[k])} | {f0(new_fy[k])} | {f2(dec_new[k])} | {f0(fyc[k])} | {f2(dep['calc'][k][0])} | {f2(dep['calc'][k][11])} |")
A(f"| **Total** | {f0(sum(po26.values()))} | {f2(sum(run.values()))} | {f0(tot_exist)} | {f0(tot_new)} | {f2(sum(dec_new.values()))} | {f0(tot_dep)} | {f2(sum(dep['calc'][k][0] for k in dep['calc']))} | {f2(sum(dep['calc'][k][11] for k in dep['calc']))} |")
A("")
A("Monthly per unit: SlipLift 65,000/84 = 773.81; SlipTray 8,000/120 = 66.67; peripherals " + f"{f2(periph)}/84 = {f2(periph / 84)}.")
A("")
s = dep["sample"]
A(f"**Hand recompute, sampled month {s['month']}** (go-lives Jan-Jun 27 in service under the full-month rule: {s['lifts_in_service']} lifts = 20+8+0+22+14+20; {s['trays_in_service']} trays = 60+24+0+86+61+98):")
A("")
A("| GL | Existing run rate | New units | Hand total | Workbook PO!Z (Jun-27) |")
A("|---|---:|---|---:|---:|")
A(f"| 5010 | {f2(s['lines']['19'][0])} | none | {f2(s['lines']['19'][2])} | {f2(s['lines']['19'][3])} |")
A(f"| 5011 | {f2(s['lines']['20'][0])} | {s['lifts_in_service']} x 65,000 / 84 = {f2(s['lines']['20'][1])} | {f2(s['lines']['20'][2])} | {f2(s['lines']['20'][3])} |")
A(f"| 5012 | {f2(s['lines']['21'][0])} | {s['trays_in_service']} x 8,000 / 120 = {f2(s['lines']['21'][1])} | {f2(s['lines']['21'][2])} | {f2(s['lines']['21'][3])} |")
A(f"| 5020 | {f2(s['lines']['22'][0])} | {s['lifts_in_service']} x {f2(periph)} / 84 = {f2(s['lines']['22'][1])} | {f2(s['lines']['22'][2])} | {f2(s['lines']['22'][3])} |")
A("")
A("**Existing fleet: PO 2026 monthly depreciation (rows 19-22; B:I actual, J:M forecast)**")
A("")
A("| GL | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep F | Oct F | Nov F | Dec F | 2026 |")
A("|---|" + "---:|" * 13)
for k in ("19", "20", "21", "22"):
    A(f"| {gl_lab[k]} | " + " | ".join(f0(x) for x in dep["po2026"][k]) + f" | {f0(po26[k])} |")
A("")
A(f"Do J:M step up with the Sep-Dec 26 go-lives (DeploySum B:E)? Partly. DeploySum has Sep 0, Oct {dep['q4_deploysum']['lifts'][0]}, Nov {dep['q4_deploysum']['lifts'][1]}, Dec {dep['q4_deploysum']['lifts'][2]} lifts and Sep 0, Oct {dep['q4_deploysum']['trays'][0]}, Nov {dep['q4_deploysum']['trays'][1]}, Dec {dep['q4_deploysum']['trays'][2]} trays. The PO forecast steps up by exact multiples of the DeploySum unit cost over the user's lives: 5011 by {', '.join(f'{x:.0f}' for x in st['20']['units'])} lifts x 65,000/84 (Oct/Nov/Dec) and 5012 by {', '.join(f'{x:.0f}' for x in st['21']['units'])} trays x 8,000/120. So the forecast already holds Q4-26 go-lives at the same costs and lives, but fewer of them: October lifts match; the rest do not. 5020's steps ({', '.join(f2(x) for x in st['22']['steps'])}) are not whole multiples of the DeploySum peripheral cost, so their basis is unknown. 5010 is flat Sep-Dec at {f2(dep['po2026']['19'][8])}.")
A("")
A(f"**Decision: rely on the run rate.** Oct-Dec 26 go-lives are not added explicitly, so there is no double count. Why: the run rate is PO's own forecast and already contains Q4-26 step-ups priced like the schedule. Adding DeploySum's Q4 units on top would double count the {st['20']['dec_minus_sep'] / (65000 / 84):.0f} lifts and {st['21']['dec_minus_sep'] / (8000 / 120):.0f} trays already in it. The {q4['lifts']:.0f}-lift / {q4['trays']:.0f}-tray shortfall vs DeploySum ({f0(q4['annual'])} for 2027) is shown as a memo (schedule section 5) and logged as I-31 for a user decision.")
A("")
A(f"**SlipBot 5010:** carried at the Dec-26 run rate {f2(run['19'])}/month = {f0(exist_fy['19'])} for 2027 (2026: {f0(po26['19'])}). This carries the run rate through 2027 as instructed; it is not evidence that the fleet is still depreciating. Fleet status is unknown: **user to confirm** whether it is fully depreciated, retired or ongoing (I-32).")
A("")
A("## Unit-cost reconciliation")
A("")
A("CapEx ÷ units to build does not give a single per-unit price because CapEx is a two-product sum: **CapEx = SlipLifts to build x (65,000 + 4,137.50) + SlipTrays to build x 8,000**. Deployment freight ($5,000 per deployment, note 3) is expensed on its own row (30) and is not in CapEx. The DeploySum formula for row 35 (`=B33*([1]Deploy!$B$7+[1]Deploy!$B$14)+B34*[1]Deploy!$B$8`) has the same structure: lift cost + peripherals, plus tray cost. The note's '$4,138' is 4,137.50 rounded by `TEXT(...,\"$#,##0\")`.")
A("")
A("| Production month | Lifts | Trays | CapEx (row 29) | CapEx ÷ all units | Lifts x 69,137.50 + trays x 8,000 | Residual | Residual using note's $4,138 |")
A("|---|---:|---:|---:|---:|---:|---:|---:|")
for x in res["recon"]:
    A(f"| {x['month']} | {x['lifts']} | {x['trays']} | {f2(x['capex'])} | {f2(x['single_price']) if x['single_price'] else ''} | {f2(x['calc'])} | {f2(x['resid'])} | {f2(x['resid_rounded_note'])} |")
A("")
A(f"Max |residual| with 4,137.50: {f2(res['recon_max_resid'])} in every month. With the note's rounded $4,138 the gap is $0.50 per lift ({f2(sum(x['resid_rounded_note'] for x in res['recon']))} over Sep-26..Dec-27). Using the note's figure would overstate 2027 depreciable cost by {f2(0.5 * dep['dec_units_lift'])} (250 lifts x $0.50); the schedule uses the reconciling 4,137.50. Handoff examples: Sep-26 9 x 69,137.50 + 32 x 8,000 = 878,237.50; Nov-26 20 x 69,137.50 + 60 x 8,000 = 1,862,750.")
A("")
A(f"Depreciable cost of 2027 go-lives = 250 x 69,137.50 + 1,036 x 8,000 = {f0(cap['dep_base'])}. CapEx bridge: FY27 CapEx {f0(cap['R29'])} - CapEx for 2028 go-lives {f0(cap['R35'])} + Nov-Dec 26 builds for Jan-Feb 27 go-lives {f0(cap['D29'] + cap['E29'])} = {f0(cap['R29'] - cap['R35'] + cap['D29'] + cap['E29'])} (difference {f0(cap['dep_base'] - (cap['R29'] - cap['R35'] + cap['D29'] + cap['E29']))}). Builds for 2028 go-lives ({cap['R33']} lifts, {cap['R34']:,} trays) are not in service in 2027, so they are not depreciated.")
A("")
A("## Revenue")
A("")
A("| Month | " + " | ".join(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]) + " | 2027 |")
A("|---|" + "---:|" * 13)
A("| PO!U12:AF12 = DeploySum!F40:Q40 | " + " | ".join(f0(x) for x in rv["po_U12_AF12"]) + f" | {f0(rv['sum_po'])} |")
A("")
A(f"Every cell is a formula (`=DeploySum!F40` ... `=DeploySum!Q40`). 2026 revenue (PO N16) {f0(REV['N'])}: 4100 {f0(res['po_2026_rev']['12'])}, 4500 {f0(res['po_2026_rev']['13'])}, 4900 {f0(res['po_2026_rev']['15'])}. Sep-Dec 26 cross-check: DeploySum recognized revenue {', '.join(f0(x) for x in rv['sepdec26_deploysum'])} vs PO 4100 forecast {', '.join(f0(x) for x in rv['sepdec26_po4100'])}.")
A("")
A("## Assumptions register")
A("")
A("| ID | Assumption | Value / effect | Where | Source |")
A("|---|---|---|---|---|")
reg = [
    ("A-01", "2027 revenue = DeploySum recognized revenue Jan-Dec 27", f"{f0(rv['sum_po'])}", "PO!U12:AF12 <- DeploySum!F40:Q40", "DeploySum 9/30/26 (row 39 in that file)"),
    ("A-02", "All 2027 revenue maps to 4100 Subscription/Platform Fees", "4100 = 100%", "PO row 12", "orchestrator assumption (brief v3)"),
    ("A-03", "4500 Implementation and 4900 One-Time revenue stay 0 in 2027", "0", "PO rows 13, 15 (unchanged)", "orchestrator assumption (brief v3: source does not split them)"),
    ("A-04", "Straight-line depreciation, no salvage", "salvage 0%", f"'{sch}'!B12", "user-confirmed 2026-10-09"),
    ("A-05", "SlipLift useful life", "84 months", f"'{sch}'!B9", "user-confirmed 2026-10-09"),
    ("A-06", "SlipTray useful life", "120 months", f"'{sch}'!B10", "user-confirmed 2026-10-09"),
    ("A-07", "SlipLift unit cost", "65,000", f"'{sch}'!B6", "source: DeploySum!A46 note 3"),
    ("A-08", "SlipTray unit cost", "8,000", f"'{sch}'!B8", "source: DeploySum!A46 note 3"),
    ("A-09", "SlipLift peripherals cost per lift", f2(periph), f"'{sch}'!B7 (formula)", "source: derived from DeploySum R29/R24/R25; reconciles every month (note shows $4,138 rounded)"),
    ("A-10", "Peripherals life = SlipLift life", "84 months", f"'{sch}'!B11", "builder assumption (I-33)"),
    ("A-11", "Peripherals GL", "5020 Robot Peripherals", f"'{sch}'!B16", "builder assumption (I-33); alternative 5011"),
    ("A-12", "SlipLift GL", "5011 SlipLift Depreciation", f"'{sch}'!B14", "user-confirmed (handoff)"),
    ("A-13", "SlipTray GL", "5012 SlipCarrier Depreciation", f"'{sch}'!B15", "user-confirmed 2026-10-09 ('Trays = carriers')"),
    ("A-14", "In-service = go-live month (DeploySum rows 19/20); full month of depreciation in that month", f"start delay 0; sensitivity: 1-month delay lowers 2027 by {f0(delay_sens)}", f"'{sch}'!B13", "brief v3 convention (orchestrator; labelled; user may change)"),
    ("A-15", "Units built in 2027 for 2028 go-lives are not depreciated in 2027", f"CapEx {f0(cap['R35'])} excluded", f"'{sch}' section 7", "follows A-14 (not in service)"),
    ("A-16", "Existing fleet = PO Dec-26 monthly run rate", f"{f2(sum(run.values()))}/month", f"'{sch}'!B21:B24 = PO!M19:M22", "orchestrator instruction (handoff)"),
    ("A-17", "Existing run rates stay flat all of 2027 (no end-of-life, retirement or disposal)", f"{f0(tot_exist)}", f"'{sch}' rows {lay['calc'][0] + 1}-{lay['calc'][0] + 4}", "builder assumption: no asset register in the files (I-32)"),
    ("A-18", "Oct-Dec 26 go-lives covered by the run rate, not added explicitly", f"memo gap {f0(q4['annual'])}", f"'{sch}'!B17, section 5", "builder decision between the handoff's two options (I-31)"),
    ("A-19", "SlipBot 5010 continues at the Dec-26 run rate; no new SlipBots", f"{f0(exist_fy['19'])}", f"'{sch}'!B21", "orchestrator instruction to carry; status user to confirm (I-32); no builds per DeploySum note 4"),
    ("A-20", "'$000s' labels on DeploySum hold dollars; relabelled to '$' with comments", f"{len(relabel)} labels", "DeploySum col A", "orchestrator instruction; evidence in I-30"),
    ("A-21", "ARR row (39) kept empty to keep the SD row map", "no data", "DeploySum row 39", "brief v2 item 1"),
]
for x in reg:
    A("| " + " | ".join(x) + " |")
A("")
A("## DeploySum refresh and tie-out")
A("")
A("Row map (by label; verified: every label in the new file matches the mapped row after the '$000s' relabel, mismatches " + f"{len(res['labmap_bad'])}): new rows 1-38 -> same rows; new rows 39-49 -> rows 40-50. Row 39 'ARR - end of period' has no counterpart; B39:R39 cleared, comment on A39. Value check: every mapped cell B:R equals the 9/30/26 cached value (mismatches {len(res['deploysum_value_mismatch'])}).")
A("")
A("| v3 row | Label | '[1]' cells stored as values | Example original formula |")
A("|---:|---|---:|---|")
for k, v in res["ext_rows"].items():
    A(f"| {k} | {str(v['label'])[:70]} | {v['n']} | `{v['example'][:90]}` |")
A("")
A(f"Total external cells stored as values: {cnt_ext}. Comments removed: {len(res['v2_frozen_comments_removed'])} ({', '.join(res['v2_frozen_comments_removed'][:3])}, ...). Comments added: {len(res['comments']['added'])} (the relabels and A39).")
A("")
A("**Tie-out rows 16-21 vs 54-64** (live in DeploySum!A69:R76):")
A("")
A("| Check | FY27 top | FY27 split | Sep-Dec 26 top | Sep-Dec 26 split | Max abs monthly diff (B:R) |")
A("|---|---:|---:|---:|---:|---:|")
for k, v in tr.items():
    A(f"| {k} | {f0(v['FY_top'])} | {f0(v['FY_split'])} | {f0(v['SepDec26_top'])} | {f0(v['SepDec26_split'])} | {f0(v['max_abs_month'])} |")
A("")
A(f"Status cell DeploySum!A76: '{res['tieout_status']}'. FY27: deployments 67, SlipLifts 250 = 212+30+8, SlipTrays 1,036 = 636+375+25, matching the orchestrator pre-scan.")
A("")
A("## v2 -> v3 diff")
A("")
A("`analyze_v3.py`: formulas compared exactly, cached values exactly except numeric differences <= 1e-6 (recalculation-order float noise, counted separately).")
A("")
A("| Sheet | Cells | Formula diffs | Value diffs | Float-noise cells (max) |")
A("|---|---:|---:|---:|---:|")
for k, v in d.items():
    A(f"| {k} | {v['cells']:,} | {v['formula_diffs']} | {v['value_diffs']} | {v['float_noise_cells']} ({v['max_noise']:.1e}) |")
A("")
A(f"New sheet: {', '.join(res['sheets_only_in_v3'])}. Collation Notes was rebuilt (not compared).")
A("")
A("PO rows with any change:")
A("")
A("| Row | Line | Columns | Class |")
A("|---:|---|---|---|")
po_ratio = [x for x in res["po_changed_rows"] if x["class"].startswith("ratio")]
for x in res["po_changed_rows"]:
    if not x["class"].startswith("ratio"):
        A(f"| {x['row']} | {x['label']} | {', '.join(x['cols'])} | {x['class']} |")
A(f"| {len(po_ratio)} rows | every other PO line | AH only | AH '% Total Rev' = AG/AG$16; blank in v2 because 2027 revenue was 0 |")
A("")
A("Rows 13 and 15 change only in AH. Their budget values (U:AF) are unchanged, at 0. PO formula changes outside rows 12 and 19-22: " + f"{len(res['po_formula_changes_outside_lines'])}. COO P&L: {len(res['coo_formula_changes'])} formula changes; value changes on {len(res['coo_changed_rows'])} rows; outside the revenue/depreciation chain (rows 12-16, 19-22, 37, 63-65, 117, 132) only column AH changed (checked: {len(res['coo_changes_outside_chain'])} exceptions).")
A("")
A(f"DeploySum: {d['DeploySum']['formula_diffs']} formula / {d['DeploySum']['value_diffs']} value diffs are the refresh (rows 3-50) and the new check block (rows 69-76). Prod Payroll: 0 formula diffs and {d['Prod Payroll']['value_diffs']} value diffs, because it reads DeploySum rows 4/24/25/27/28 (I-05). Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget read only DeploySum rows 53-66, and show 0 diffs.")
A("")
A("## Error scan")
A("")
A("| Sheet | v2 | v3 |")
A("|---|---|---|")
for k, v in res["errors"].items():
    A(f"| {k} | {v['v2'] or 'none'} | {v['v3'] or 'none'} |")
A("")
A(f"New errors (a cell that is an error in v3 but not in v2): **{len(res['new_errors'])}**. Prod Payroll's remaining {sum(pp['v3'].values())} errors were errors in v2 too; the code changed from #REF! to #NAME? because the DeploySum inputs now resolve and LibreOffice then reaches the {res['pp_name_xlookup']} XLOOKUP cells (row 48), which it does not support; the other #NAME? cells are below them.")
A("")
A("## Package")
A("")
A(f"Final package: {res['package']['parts']} parts; `xl/externalLinks/*` **{res['package']['externalLink_parts']}**; `<externalReference>` {res['package']['externalReference_elements']}; defined names {res['package']['defined_names']:,} (v2: 8,965; none added or removed).")
A("")
A("## Sheets in the output")
A("")
A("| # | Sheet | State |")
A("|---|---|---|")
for i, (s_, st_) in enumerate(res["sheets_v3"], 1):
    A(f"| {i} | {s_} | {st_} |")
A("")
# carried v2 sections
def section(md, head):
    i = md.find(head)
    if i < 0: return ""
    j = md.find("\n## ", i + len(head))
    return md[i:j if j > 0 else len(md)].rstrip()
sev = section(v2md, "## Severity scale")
A(sev)
A("")
A("## Issues (v3)")
A("")
A("Severity per the scale above. 'Basis' shows which rule set the rating. v2 rows not listed under 'Issue-level changes' are carried verbatim.")
A("")
A("| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |")
A("|---|---|---|---|---|---|---|---|")
for k in order:
    A("| " + " | ".join(str(c).replace("|", "/") for c in iss[k]) + " |")
A("")
A("### Variance scan: rows with |AG-N| > $50k and > 50% (v3 values)")
A("")
A("| Sheet | Row | Line | 2026 N | 2027 AG | Change | % |")
A("|---|---:|---|---:|---:|---:|---:|")
for v in var:
    A(f"| {v[0]} | {v[1]} | {v[2]} | {f0(v[3])} | {f0(v[4])} | {f0(v[5])} | {(str(round(v[6] * 100)) + '%') if v[6] is not None else 'n/a'} |")
A("")
A("## Carried from v2 (still valid: FO, FE, CO, PE and PO payroll unchanged)")
A("")
for head in ("## Cross-department overlap (B3)",):
    A(section(v2md, head).replace("## Cross-department overlap (B3)", "### Cross-department overlap (from v2)"))
    A("")
i = v2md.find("### T&E rows with 'Reclass needed'")
j = v2md.find("### Appendix", i)
A(v2md[i:j].rstrip())
A("")
A("## Decisions")
A("")
dec = [
    "D1 (v3): Built v3 from the delivered v2 workbook (openpyxl edit + LibreOffice recalc), not from the original inputs again. v2 is reproducible with run_build_v2.sh, so the chain is reproducible. This keeps every v2 cell, comment, name and format that v3 does not touch.",
    "D2 (v3): DeploySum row map by label: rows 1-38 same, 39-49 -> +1; the SD ARR row 39 is kept empty (brief v2 item 1). Internal formulas copied (88, identical to v2's after mapping); '[1]' formulas stored as cached values and listed on Collation Notes.",
    "D3 (v3): Peripherals cost = 4,137.50, derived from DeploySum CapEx, rather than the note's rounded '$4,138'. It reconciles every month to $0.00. The note's figure leaves a $0.50/lift residual.",
    "D4 (v3): Peripherals go to 5020 with the SlipLift life. Both are inputs and flagged for the user (I-33).",
    "D5 (v3): Oct-Dec 26 go-lives: rely on the PO Dec-26 run rate, never both; gap shown as memo (I-31).",
    "D6 (v3): Existing-fleet run rates are links (=PO!M19:M22), so they trace to the PO 2026 forecast; carried flat (I-32).",
    "D7 (v3): PO!R12 and R19:R22 set to 'Manual' (allowed by the row's data validation) so the method column matches the linked rows; notes in column AI.",
    "D8 (v3): DeploySum row visibility follows the 9/30/26 file; recognized revenue row 40 is visible because it now feeds PO.",
    "D9 (v3): '$000s' labels relabelled to '$' with a comment on each cell (flagged, not silent; I-30).",
    "D10 (v3): v2 -> v3 value comparison treats numeric differences <= 1e-6 as recalculation noise (counted and shown). All are below 1.1e-9.",
    "D11 (v3): Severity scale and tie-break rule unchanged from v2. The full-month convention is a brief decision, so it sits in the register with its sensitivity, not in the issues list.",
    "Carried from v2: D1-D9 of v2 still apply to the parts v3 did not touch.",
]
for x in dec:
    A(f"- {x}")
A("")
A("## Not done / limits")
A("")
for x in [
    "The external workbook '[1]' is still not available: DeploySum holds the 9/30/26 cached values, not live links.",
    "No fixed-asset register was supplied, so existing-fleet depreciation is a run rate, not an asset-by-asset schedule. End-of-life dates are unknown (I-32).",
    "Not opened in Microsoft Excel. Prod Payroll's XLOOKUP rows show #NAME? in LibreOffice 24.2 and may evaluate in Excel (untested).",
    "No change made to FO, FE, CO, PE, or to PO lines other than 12 and 19-22 (and their subtotals/ratios). 4500/4900 stay 0 by assumption.",
    "v2 limits on page setup, sheet-scoped names and Google-specific parts still apply.",
]:
    A(f"- {x}")
md = "\n".join(L) + "\n"
open(OUT_MD, "w").write(md)

# ------------------------------------------------------------------ Collation Notes JSON
notes = {"title": "2027 COO Budget - Collation Notes (build v3, draft for review)", "sections": [],
         "col_widths": [12, 10, 40, 60, 60, 28, 30, 50]}
S = notes["sections"].append
S({"heading": "Source", "lines": [
    f"Base: v2 collated workbook (COO book + SD FO/FE). New input: 2027_Sales_Deploy_Prod_to_COO_as_of_093026.xlsx (sha256 {sha(NEW)[:16]}...).",
    f"Recalculated with {lov}. Full notes: 02-build/02-build_notes_v3.md."]})
S({"heading": "What v3 changed", "lines": [
    f"1. DeploySum rows 3-49 refreshed from the 9/30/26 resolved file (row map by label; ARR row 39 kept empty). {cnt_ext} external '[1]' cells stored as cached values (formulas listed below).",
    "2. PO 4100 (row 12) 2027 = DeploySum recognized revenue Jan-Dec 27 (row 40). Orchestrator assumption: all revenue to 4100.",
    f"3. PO 5010-5020 (rows 19-22) 2027 = '{sch}' tab (straight-line; SlipLift 84 mo, SlipTray 120 mo; existing fleet = PO Dec-26 run rate).",
    f"4. '$000s' labels on DeploySum relabelled to '$' (values are dollars), with comments. Tie-out rows 16-21 vs 54-64 added at DeploySum!A69:R76.",
    "5. No change to FO, FE, CO, PE, or PO lines other than 12 and 19-22 (verified: 0 formula / 0 value diffs vs v2)."]})
S({"heading": "Headline (live formulas; v2 2027 shown for comparison)", "table": {
    "header": ["Line", "Col", "v2 2027", "v3 (live)"],
    "formula_cols": [4],
    "rows": [[lab, c, (H[lab]["AG_v2"] if c == "AG" else H[lab]["N"]), f"='COO P&L'!{c}{H[lab]['row']}"]
             for lab in ("Revenue", "COGS", "Gross Profit", "Opex", "Net Income") for c in ("N", "AG")]
            + [["Depreciation (rows 19-22)", "AG", 0, "=SUM('COO P&L'!AG19:AG22)"],
               ["Total cost (COGS + Opex)", "AG", TC["AG_v2"], "='COO P&L'!AG63+'COO P&L'!AG116"]]}})
S({"heading": "Assumptions register", "table": {"header": ["ID", "Assumption", "Value / effect", "Where", "Source"],
                                                "rows": [list(x) for x in reg]}})
S({"heading": "Issues (v3) - severity: HIGH = blocks sign-off or > $250k; MED = $50k-250k or owner confirmation; LOW = < $50k or hygiene",
   "table": {"header": ["ID", "Sev", "Location", "Finding", "Evidence", "2027 impact", "Basis", "Recommended action"],
             "rows": [iss[k] for k in order]}})
S({"heading": "'$000s' relabel (DeploySum)", "table": {"header": ["Cell", "Source label", "v3 label"],
                                                       "rows": [list(x) for x in relabel]}})
S({"heading": "DeploySum external-link formulas in the 9/30/26 file, stored as cached values", "table": {
    "header": ["v3 cell", "New-file cell", "Original formula (text)", "Stored value"],
    "rows": [[a, b, f, (v if not isinstance(v, str) or not v.startswith("=") else "'" + v)] for a, b, f, v in ext["ext"]]}})
json.dump(notes, open(OUT_JSON, "w"), indent=1, default=str)
print(f"report_v3: wrote {OUT_MD} ({len(md):,} chars) and {OUT_JSON}; issues {dict(sev_count)}")
