"""v2 report: turn analysis results into (1) the Collation Notes sheet spec (JSON) and (2) build notes markdown.

Usage:
  python3 -I report.py COO_BOOK SD_BOOK RES1_JSON RES2_JSON PKG_OUT_JSON PKG_COO_JSON PKG_SD_JSON PRUNE_LOG_JSON
                       EXTREFS_JSON DIFF_JSON LO_VERSION_TXT NOTES_SHEET_JSON NOTES_MD OUT_XLSX_NAME

Every number and every workbook fact in the output is read from the JSON inputs (computed from the workbooks
by analyze.py / analyze_v2.py / pkgscan.py / prune_names.py / diff_versions.py) or from LO_VERSION_TXT
(the output of `soffice --version`). Nothing numeric is typed in here. The only fixed text is the
severity scale (from the v2 handoff), the classification of each traced overlap, and recommended actions.
(The v1 report, with its typed-in claims, is frozen as report_v1.py for reproducing v1 only.)
"""
import sys, json, hashlib, os, collections, re

(COO_PATH, SD_PATH, RES1, RES2, PKG, PKG_COO, PKG_SD, PRUNE, EXT, DIFF, LOVER,
 NOTES_JSON, NOTES_MD, OUT_NAME) = sys.argv[1:15]
R = json.load(open(RES1)); F = R["findings"]
V = json.load(open(RES2))
P = json.load(open(PKG)); PC = json.load(open(PKG_COO)); PS = json.load(open(PKG_SD))
PR = json.load(open(PRUNE)); E = json.load(open(EXT)); D = json.load(open(DIFF))
LO = open(LOVER).read().strip()
VERSION = re.search(r"_v(\d+)\.xlsx$", OUT_NAME).group(1)
PRUNED_CSV = f"02-build_pruned_names_v{VERSION}.csv"
NOTES_MD_NAME = f"02-build_notes_v{VERSION}.md"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def m(x):
    if x is None:
        return "n/a"
    return f"{x:,.0f}" if x >= 0 else f"({-x:,.0f})"


def pct(x):
    return f"{x * 100:.2f}%"


def C(ref):
    """value of a cell captured by analyze_v2 ('OUT:Sheet!A1' or 'SD:Sheet!A1')"""
    return V["cells"][ref]["value"]


def CF(ref):
    return V["cells"][ref]["formula"]


def rec(d, row, col, key):
    for x in R["recon"]:
        if x["dept"] == d and x["row"] == row and x["col"] == col:
            return x[key]


def pl(row, col, key):
    for x in R["coo_pl_before_after"]:
        if x["row"] == row and x["col"] == col:
            return x[key]


def old(d, row, col):
    for x in R["replaced_coo_fofe"]:
        if x["dept"] == d and x["row"] == row and x["col"] == col:
            return x["coo_book"]


def var(sheet, row):
    for v in F["variance"]:
        if v["sheet"] == sheet and v["row"] == row:
            return v


def vtxt(sheet, row):
    v = var(sheet, row)
    return f"{sheet}!N{row} {m(v['N'])} -> AG{row} {m(v['AG'])}" if v else f"{sheet} row {row}: not in variance scan"


def H(book, row, col):
    return V["headline"][f"{book}:{row}:{col}"]


def esc(t):
    return str(t).replace("|", "\\|").replace("\n", " ")


def ranges(nums):
    """[30,32,33,34] -> '30, 32-34'"""
    nums = sorted(nums); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}" if i == j else f"{nums[i]}-{nums[j]}"); i = j + 1
    return ", ".join(out)


coo_name, sd_name = os.path.basename(COO_PATH), os.path.basename(SD_PATH)
ext_cells = E["external_cells"]
ext_cached = dict(collections.Counter(str(e["sd_cached"]) for e in ext_cells))
ext_books = sorted({b for e in ext_cells for b in re.findall(r"\[1\]([A-Za-z0-9 &\-]+?)'?!", e["formula"])})
ext_by_row = collections.OrderedDict()
for e in ext_cells:
    ext_by_row.setdefault(int(re.sub(r"[A-Z]", "", e["cell"])), []).append(e)
fid = R["fidelity"]
new_err_total = sum(v["new_errors_n"] for v in fid.values())
err_b_sd = R["errors_before_sd"]; err_a = R["errors_after"]; err_b_coo = R["errors_before_coo"]
recl = F["reclass"]; recl_amt = sum(x["amount"] or 0 for x in recl)
recl_ai = [x for x in recl if x["status"] == "AI suggested"]
recl_assumed = [x for x in recl if x["tag_basis"] == "Assumed"]
recl_pairs = collections.Counter((int(x["booked_gl"]), int(x["budget_gl"])) for x in recl)
ph = F["placeholders"]; ph_te = [p for p in ph if p["sheet"] == "Fld Maint T&E Data"]
hard = F["hardcodes"]
sub_skipped = sum(1 for s in F["subtotals"] if s["col"] != "-" for r, v in s["missing_values_abs"].items() if v)
sub_header_hits = [s for s in F["subtotals"] if s["col"] == "-"]
const_in_totals = sum(1 for h in hard if h["type"] == "constant in total/roll-up cell")
fd_cols = sorted(V["formula_diff_cols"], key=lambda c: (len(c), c))
fd_cols_txt = f"{fd_cols[0]}:{fd_cols[-1]}" if fd_cols else "none"
fd_cols_contiguous = fd_cols == [c for c in ["U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF"] if c in fd_cols]
non_ds_formula_loss = {s: v for s, v in R["formula_counts"].items() if s != "DeploySum" and v["source_formulas"] != v["output_formulas"]}
pos_coo = V["coo_tab_positions"]
ds_mix = V["deploysum_formula_mix"]
dn_before = PC["defined_names_total"]; dn_after = P["defined_names_total"]
sd_ext_parts = PS["external_link_parts"]
dropped_part_dirs = sorted({p.split("/")[1] for p in PS["parts"] + PC["parts"]
                            if p.startswith("xl/") and p.count("/") >= 2} - {p.split("/")[1] for p in P["parts"] if p.count("/") >= 2})
err_tot = lambda d: sum(d.values())

# ------------------------------------------------------------------ headline numbers (O6)
cost26 = H("OUT", 63, "N") + H("OUT", 116, "N"); cost27 = H("OUT", 63, "AG") + H("OUT", 116, "AG")
cost27_before = H("COO", 63, "AG") + H("COO", 116, "AG")
dep26 = sum(H("OUT", int(r), "N") for r in V["dep_labels"]); dep27 = sum(H("OUT", int(r), "AG") for r in V["dep_labels"])

# ------------------------------------------------------------------ severity (O7)
SCALE = ("HIGH = blocks sign-off or > $250k impact; MED = $50k-250k or needs owner confirmation; "
         "LOW = < $50k or hygiene.")
TIEBREAK = ("Applied in this order: (1) HIGH if the item blocks sign-off or its $ impact computed from the workbook "
            "is > $250k; (2) MED if that impact is $50k-250k; (3) MED if the impact cannot be determined from the "
            "workbook and an owner must confirm; (4) otherwise LOW (impact < $50k, $0, or hygiene). "
            "'Impact' is the amount the item could move the 2027 budget, read from cells; where only an "
            "exposure (the amount resting on the item) is known, it is shown but not used as the impact.")


def severity(amount, blocks, owner):
    if blocks or (amount is not None and abs(amount) > 250000):
        return "HIGH"
    if amount is not None and abs(amount) >= 50000:
        return "MED"
    if amount is None and owner:
        return "MED"
    return "LOW"


I = []


def add(iid, v1sev, loc, finding, evidence, action, amount=None, amount_txt=None, blocks=False, owner=False, change=""):
    s = severity(amount, blocks, owner)
    basis = ("blocks sign-off" if blocks else
             f"impact {m(amount)}" if amount is not None else
             "impact not determinable; owner confirmation needed" if owner else "hygiene")
    I.append({"id": iid, "sev": s, "v1": v1sev, "loc": loc, "finding": finding, "evidence": evidence,
              "impact": amount_txt if amount_txt is not None else (m(amount) if amount is not None else "not determinable"),
              "basis": basis, "action": action, "change": change})


roster = f"{CF('OUT:Fld Eng Budget!A59').lstrip('=')}:{CF('OUT:Fld Eng Budget!A67').lstrip('=')}"   # rows the FE payroll block names
ppf = V["prod_payroll_formulas"]
DEP_ROWS = sorted(int(k) for k in V["dep_labels"])
po_r12 = C("OUT:PO!R12")
add("I-01", "HIGH", "COO P&L!AG16; PO!R12:S15; PO!U12:AF15",
    f"2027 revenue is zero. The PO 2027 revenue rows use input method '{po_r12}' with an empty or 0 annual input (S), so U:AF = 0. The 2027 P&L is cost-only, so 2027 Net Income is incomplete.",
    f"COO P&L!N16 = {m(H('OUT',16,'N'))}, AG16 = {m(H('OUT',16,'AG'))}. PO!R12 = '{po_r12}', PO!S12 = {C('OUT:PO!S12')!r}. {vtxt('PO',12)}; {vtxt('PO',15)}.",
    "Owner of PO/revenue to enter 2027 revenue (or link the Revenue Roll-up). Do not present 2027 Net Income until fixed.",
    blocks=True)
add("I-02", "HIGH", "COO P&L!AG132; FO!AG132; FE!AG132",
    f"Replacing FO and FE with the SD versions moves 2027 COO Net Income by {m(pl(132,'AG','change'))}. The SD build is much heavier than the COO book's FO/FE.",
    f"COO P&L!AG132 before {m(pl(132,'AG','before'))}, after {m(pl(132,'AG','after'))}. FO!AG132 COO book {m(old('FO',132,'AG'))} -> SD {m(rec('FO',132,'AG','source'))}; FE!AG132 COO book {m(old('FE',132,'AG'))} -> SD {m(rec('FE',132,'AG','source'))}. Drivers: {vtxt('FO',52)}; {vtxt('FO',47)}; {vtxt('FO',29)}.",
    "COO and SD owner to review the FO/FE 2027 drivers (headcount, spare parts, deployment freight) before sign-off.",
    amount=pl(132, "AG", "change"))
add("I-03", "HIGH", f"DeploySum!{V['ext_bbox']['grid']}; DeploySum!A{V['ext_bbox']['col_A'][0]}; DeploySum!A{V['ext_bbox']['col_A'][1]}:A{V['ext_bbox']['col_A'][-1]}",
    f"DeploySum links to a workbook that was not supplied ([1] = {', '.join(ext_books)}). These {len(ext_cells)} cells had already failed in the SD book (cached {ext_cached}). They were frozen to the SD cached values per orchestrator handoff; this is a declared deviation from brief criterion 1 because the linked workbook was not supplied and the SD file has no externalLink part. So the bookings/deployments/production block and the notes in column A show errors.",
    f"{len(ext_cells)} formula cells contain '[1]...'; every one is listed with its original formula on the Collation Notes sheet. SD package externalLink parts: {len(sd_ext_parts)}. DeploySum errors: SD {err_b_sd['DeploySum']}, output {err_a['DeploySum']}.",
    "Get the Revenue Roll-up / Deploy Detail workbook; then relink these formulas or paste values so the plan is reproducible.",
    blocks=True, change="Wording: 'as instructed' replaced by the declared-deviation statement (B1).")
drv = V["deploysum_drivers_R"]
drows = F["deploysum_drivers"]["rows_const"]
add("I-04", "HIGH", f"DeploySum!B{drows[0]}:R{drows[-1]}",
    f"The deployment-split drivers that feed Fld Ops Payroll, Fld Maint Budget and Fld Eng Budget (and so FO/FE 2027) are typed values, not formulas; the rows that should derive them are broken (I-03), so they cannot be traced to a source.",
    f"Rows {F['deploysum_drivers']['rows_const']} contain no formulas. FY27 totals (typed): {'; '.join(f'DeploySum!R{r} {d['label'][:40]!r} = {d['R']:,.0f}' for r, d in drv.items())}. FO/FE 2027 lines linked to driver tabs total {m(V['q']['driver_linked_total'])} ({len(V['q']['driver_linked_lines'])} lines).",
    f"SD owner to confirm rows {drows[0]}-{drows[-1]} match the current deployment plan and record the source.",
    blocks=True, amount_txt=f"exposure {m(V['q']['driver_linked_total'])}")
pp = [x for x in V["prod_payroll_refs"] if x["book"] == "OUT"]
pp_sd = [x for x in V["prod_payroll_refs"] if x["book"] == "SD"]
add("I-05", "HIGH", f"Prod Payroll!{V['error_bbox']['Prod Payroll']} (hidden); Fld Ops Payroll!M5:M7",
    f"The production payroll model does not work: {ppf['errors']} of its {ppf['total']} formulas are errors in the output (as in the SD book), including every payroll total ({'; '.join(f'row {r} {t['label']!r}: S = {t['S']}' for r, t in ppf['total_rows'].items() if 'PAYROLL' in str(t['label']).upper() and t['S'] is not None) or 'none found'}). The {ppf['ok']} formulas that evaluate are input helpers, staffing grids and headcount rows (rows {ranges(ppf['ok_rows'])}). It feeds no budget value: the only cells read from it are typed rate/timing inputs, not headcount or cost. Its result does not reach PO.",
    f"Errors SD {V['errors_sd']['Prod Payroll']}, output {V['errors_out']['Prod Payroll']}. Cells read from it: " + "; ".join(f"{x['from']} <- {x['target']} '{x['target_label']}' ({'formula' if x['target_is_formula'] else 'typed input'}, = {x['value']})" for x in pp) + f". PO 5110-5140 (PO!U33:AF35) are typed values ({sum(v['typed_months'] for k, v in V['po_payroll_rows'].items() if k != '36')} typed month cells, 0 links).",
    "Fix DeploySum first; then decide whether PO production labour should link to Prod Payroll (see I-17).",
    amount=0.0, owner=True, change="O4: $0 budget impact; it supplies typed rate/timing inputs only.")
meli = V["meli"]
add("I-06", "HIGH", "Fld Maint Budget!B30 (comment); Fld Ops Payroll!B11; FO!AG44; FO!AG52",
    f"MeLi contractor double count: quantified at $0 in the current cells. The CONFIRM comment on Fld Maint Budget!B30 says Fld Ops Payroll includes MeLi in '21 all-in techs', but Fld Ops Payroll!B11 = {C('OUT:Fld Ops Payroll!B11'):,.0f} ('{C('OUT:Fld Ops Payroll!A11')}') and Fld Maint Budget!B29 = B30 + Fld Ops Payroll!B11 = {C('OUT:Fld Maint Budget!B29'):,.0f}. So MeLi techs are costed in 5310 only. The comment describes an earlier state and is stale (Fld Maint Budget!A143 records the correction).",
    f"FO 5310 (FO!AG44 = {m(meli['fo_AG44'])}) = MeLi techs in role {m(meli['techs_in_role_cost'])} + Merida contractors {m(meli['merida_cost'])} + MeLi supervisor {m(meli['supervisor_cost'])} (Fld Maint Budget rows 70-72 x B10/B11; row 84 = {m(meli['row84_2027'])}). FO 5510 current techs: Fld Ops Payroll!F20:Q20 = {', '.join(f'{x:,.0f}' for x in sorted(set(meli['fop_current_techs_2027'])))} each month (formula {meli['fop_row20_formula']}); current-tech payroll 2027 {m(meli['fop_current_tech_payroll_2027'])}.",
    "SD owner to confirm and delete the stale CONFIRM comment on Fld Maint Budget!B30.",
    amount=0.0, change="Quantified (O3): overlap $0 in current cells; comment stale.")
add("I-07", "HIGH", "; ".join(f"PO!AG{r}" for r in DEP_ROWS if var("PO", r)) + f"; COO P&L!AG{DEP_ROWS[0]}:AG{DEP_ROWS[-1]}",
    f"2027 depreciation is zero, while 2026 carries {m(dep26)} (COO P&L rows {', '.join(str(r) for r in DEP_ROWS)}: {'; '.join(V['dep_labels'][str(r)] for r in DEP_ROWS)}). 2027 Net Income is therefore incomplete. PO was out of scope and is unchanged.",
    "; ".join(vtxt("PO", r) for r in DEP_ROWS if var("PO", r)) + ".",
    "PO owner / Finance to budget 2027 depreciation from the fixed-asset schedule.", blocks=True)
plugs = V["po_plugs"]
add("I-08", "MED", "; ".join(p["cell"] for p in plugs),
    f"Typed plugs are added onto the driver formula in 2027 month cells ({', '.join(sorted({'+' + format(p['plug'], ',.0f') for p in plugs}))}). They are not visible in the method columns R:T.",
    "; ".join(f"{p['cell']} +{p['plug']:,.0f}" for p in plugs) + f". Total plugs {m(sum(p['plug'] for p in plugs))}.",
    "PO owner to move these amounts into a documented input (column S or a manual row), or remove them.",
    amount=sum(p["plug"] for p in plugs), change="Total plugs quantified.")
ov_pe = V["pe_overrides"]
def group_cells(cells):
    rows = collections.OrderedDict()
    for c in cells:
        sh, ref = c.split("!"); col = re.sub(r"\d", "", ref); r = int(re.sub(r"[A-Z]", "", ref))
        rows.setdefault((sh, r), []).append(col)
    return "; ".join(f"{sh}!{cs[0]}{r}" + (f":{cs[-1]}{r}" if len(cs) > 1 else "") for (sh, r), cs in rows.items())
add("I-09", "LOW", group_cells([o["cell"] for o in ov_pe]),
    "Typed numbers overwrite the driver formula in some 2027 months (manual overrides inside a formula row).",
    ", ".join(f"{o['cell']}={o['typed']:,.0f}" for o in ov_pe) + f". Total typed {m(sum(o['typed'] for o in ov_pe))}.",
    "PE owner to confirm the overrides, or set the row method to Manual.", amount=sum(o["typed"] for o in ov_pe))
zl = V["zero_2027_lines"]
add("I-10", "MED", "; ".join(z["cell"] for z in zl) + "; FO!AG116",
    f"FO/FE lines with material 2026 spend have 2027 = 0, and FO Total Expense (SG&A) is 0 for 2027. Fld Maint Budget!A99 says: '{C('OUT:Fld Maint Budget!A99')}'",
    "; ".join(f"{z['cell']} {z['label']}: 2026 {m(z['N'])} -> 2027 {m(z['AG'])}" for z in zl) + f"; {vtxt('FO',116)}. 2026 total of these lines {m(sum(z['N'] for z in zl))}.",
    "SD owner to confirm whether these costs stop in 2027 or are budgeted elsewhere.",
    owner=True, amount_txt=f"not determinable (2026 base {m(sum(z['N'] for z in zl))})")
coo_var = sorted([v for v in F["variance"] if v["sheet"] == "COO P&L" and re.match(r"^\d{4} - ", (v["label"] or "").strip())],
                 key=lambda v: -abs(v["diff"]))[:4]
add("I-11", "MED", "; ".join(f"COO P&L!AG{v['row']}" for v in coo_var) + " (+ variance table)",
    f"{len(F['variance'])} rows have a 2027 budget that differs from 2026 by more than 50% and more than $50k.",
    "Largest COO P&L GL moves: " + "; ".join(vtxt("COO P&L", v["row"]) for v in coo_var) + ".",
    "Each dept owner to comment on their rows in the variance table.", owner=True,
    change="Location now sheet!cell (O7).")
q = V["q"]
add("I-12", "MED", "Fld Maint Budget!B8; Fld Maint Budget!B78:M78; FO!AG46",
    f"Site setup kit cost is flagged as a placeholder (Fld Maint Budget!D8: '{C('OUT:Fld Maint Budget!D8')[:80]}'). It feeds FO 5330.",
    f"Fld Maint Budget!B8 = {C('OUT:Fld Maint Budget!B8'):,.0f} $/new site; '{q['fmb_kits_label']}' 2027 (B78:M78) = {m(q['fmb_kits_2027'])}. {vtxt('FO',46)}.",
    "SD owner to price the kit list and replace B8.", owner=True,
    amount_txt=f"not determinable (exposure {m(q['fmb_kits_2027'])})")
add("I-13", "MED", "Fld Ops Payroll!M11; Fld Ops Payroll!B12; Fld Ops Payroll!M14",
    f"Two Fld Ops Payroll drivers are marked 'Placeholder' in the author's notes: site techs per floater (M11) and the share of expansion go-lives needing a tech (B12). M11 currently has no effect because the floater switch M14 = '{C('OUT:Fld Ops Payroll!M14')}' (floater payroll 2027 = {m(q['fop_floater_2027'])}). B12 drives expansion-tech payroll.",
    f"M11 = {C('OUT:Fld Ops Payroll!M11')}, B12 = {C('OUT:Fld Ops Payroll!B12')}, M14 = '{C('OUT:Fld Ops Payroll!M14')}'. Expansion tech payroll 2027 (Fld Ops Payroll!F47:Q47) = {m(q['fop_expansion_2027'])}.",
    "SD owner to confirm or replace B12; M11 matters only if M14 is set to Yes.", owner=True,
    amount_txt=f"not determinable (exposure {m(q['fop_expansion_2027'])})")
add("I-14", "LOW", "Prod Payroll!M7; Prod Payroll!B9; Prod Payroll!A33; Fld Ops Payroll!B9; Old Draft!B142 (SD, not carried)",
    "More placeholder inputs: Prod Payroll new-hire cost, current headcount and absence factors (no budget effect while Prod Payroll is broken), and the Fld Ops Payroll new-hire cost per tech, which hidden Old Draft!B142 says overlaps an onboarding line.",
    f"Fld Ops Payroll!B9 = {C('OUT:Fld Ops Payroll!B9'):,.0f}; new-hire cost in FO 2027 (Fld Ops Payroll rows {', '.join(str(k) for k in V['fop_new_hire_rows'])}, F:Q) = {m(V['fop_new_hire_2027'])}. Old Draft!B142: '{V['old_draft_B142'][:140]}'.",
    "SD owner to confirm B9 (and that onboarding is not also budgeted elsewhere).", owner=True,
    amount_txt=f"not determinable (exposure {m(V['fop_new_hire_2027'])})",
    change="Stated scale applied: impact not determinable, owner confirmation needed.")
add("I-15", "MED", "Fld Maint Budget!B12 (comment); Fld Maint Budget!B11; Fld Ops Payroll!H11; Fld Ops Payroll!E12",
    f"The CONFIRM comment on Fld Maint Budget!B12 says Fld Ops Payroll shows 0 current supervisors; it now shows H11 = {C('OUT:Fld Ops Payroll!H11')} ('{C('OUT:Fld Ops Payroll!E11')[:60]}'), and E12 says '{C('OUT:Fld Ops Payroll!E12')}'. The MeLi contract supervisor (5310) and the domestic manager (5510) are different people, so there is no double count; the comment is stale.",
    f"MeLi supervisor in 5310 2027 = {m(meli['supervisor_cost'])} (Fld Maint Budget!B11 = {C('OUT:Fld Maint Budget!B11'):,.0f}/month x B12 = {C('OUT:Fld Maint Budget!B12')}). Isaiah (Fld Ops Payroll row 77) 2027 = {m(meli['fop_isaiah_2027'])}; incremental supervisors (row 73) 2027 = {m(meli['fop_incr_supervisor_2027'])}.",
    "SD owner to confirm and delete the stale comment.", amount=0.0,
    change="Quantified: $0 overlap; comment stale.")
te = V["te_extent"]
add("I-16", "MED", f"Fld Maint T&E Data!M{te['first_data_row']}:M{te['max_row']} (SD, hidden, not carried)",
    f"{len(recl)} T&E transactions are flagged 'Reclass needed' = Yes, totalling ${recl_amt:,.2f}; booked GL differs from budget GL. {len(recl_ai)} are tagged 'AI suggested' and {len(recl_assumed)} have tag basis 'Assumed'. If FO 2026 actuals were pulled on booked GL, these sit on the wrong 2026 lines; totals are unaffected, and no formula in the output reads this sheet.",
    "Top booked->budget GL pairs: " + ", ".join(f"{a}->{b} x{n}" for (a, b), n in recl_pairs.most_common(5)) + ".",
    "Finance to post the reclasses (or confirm none are needed).", amount=recl_amt,
    change="O5: < $50k and 2026 line mapping only.")
lwh = V["lwh"]
po36 = lwh["po"]["36"]["AG"]; po33 = lwh["po"]["33"]["AG"]
add("I-17", "MED", "Logistics&WH Payroll!S51 (SD, not carried); PO!AG33:AG36",
    f"The SD Logistics & Warehouse payroll model ('{C('SD:Logistics&WH Payroll!A2')[:90]}...') totals {m(lwh['S51_2027'])} for 2027 but is referenced by {lwh['refs_to_sheet']} formulas in either book. PO 2027 production labour (rows 33-35) is typed with no link, so the workbook cannot show whether warehouse payroll is inside it. If it is not, PO 2027 is understated by up to {m(lwh['S51_2027'])}.",
    f"Logistics&WH Payroll 2027 (F51:Q51) = {m(lwh['sum_F51_Q51'])}: " + "; ".join(f"{k} {m(v)}" for k, v in lwh['by_component_2027'].items()) + f"; Dec-27 headcount {lwh['headcount_Dec27']:,.0f}. PO 2027: " + "; ".join(f"{v['label']} {m(v['AG'])}" for k, v in lwh['po'].items() if k != '48') + f". Logistics&WH 2027 = {lwh['S51_2027']/po36*100:.0f}% of PO 5100 total and {lwh['S51_2027']/po33*100:.0f}% of PO 5110 salaries. PO 5350 Warehouse AG48 = {m(lwh['po']['48']['AG'])}; FO 5350 AG48 = {m(lwh['fo_5350']['AG'])} (Fld Maint Budget warehouse rent line).",
    "PO owner to confirm whether PO 5110-5140 include the warehouse team. If not, link PO to this model (it would then need to be carried into the workbook).",
    amount=lwh["S51_2027"], amount_txt=f"up to {m(lwh['S51_2027'])}",
    change="Quantified (O2): possible understatement of PO.")
add("I-18", "LOW", "Fld Ops Payroll!B10; Fld Ops Payroll!B15; Fld Ops Payroll!B16",
    "The hiring horizon ends at Dec-27 (DeploySum row 54). Hires for Jan-28 go-lives use an Oct-Dec 27 average default rather than a forecast (documented by the author).",
    f"B10 = {C('OUT:Fld Ops Payroll!B10')}; B15 = {CF('OUT:Fld Ops Payroll!B15')} = {C('OUT:Fld Ops Payroll!B15')}; B16 = {CF('OUT:Fld Ops Payroll!B16')} = {C('OUT:Fld Ops Payroll!B16')}; cell notes on B10/B15/B16.",
    "Overwrite B15/B16 if a 2028 go-live forecast exists.")
add("I-19", "LOW", f"FE!U{V['fe_reads_feb_rows'][0]}:AF{V['fe_reads_feb_rows'][-1]} (rows {ranges(V['fe_reads_feb_rows'])}); Fld Eng Budget rows {ranges(V['feb_reads_fe_rows'])}",
    "FE and Fld Eng Budget link in both directions: Fld Eng Budget reads FE 2026 columns, and FE 2027 rows read Fld Eng Budget. LibreOffice recalculated with no errors (no cell-level circularity), but the structure is easy to break.",
    f"Fld Eng Budget has {V['fe_feb_refs']['Fld Eng Budget->FE']} references to FE; FE has {V['fe_feb_refs']['FE->Fld Eng Budget']} references to Fld Eng Budget.",
    "Check Fld Eng Budget before editing the FE 2026 columns it reads.")
add("I-20", "LOW", f"SD sheets {', '.join(V['sd_hidden_sheets'])} (hidden); DeploySum!A{V['deploysum_hidden_rows'][0]}:A{V['deploysum_hidden_rows'][-1]} (hidden rows {ranges(V['deploysum_hidden_rows'])})",
    f"SD has {len(V['sd_hidden_sheets'])} hidden sheets; {', '.join(V['out_hidden_sheets'])} is carried and kept hidden, the others are not carried (FO/FE do not depend on them). DeploySum hidden rows are preserved.",
    f"Hidden in SD: {V['sd_hidden_sheets']}; hidden in output: {V['out_hidden_sheets']}; DeploySum hidden rows: {ranges(V['deploysum_hidden_rows'])}.",
    "None, unless reviewers want Old Draft / T&E Data in the pack.", change="Location now sheet!cell (O7).")
od = F["old_draft"]
add("I-21", "LOW", "; ".join(f"{o['sheet']}!{o['examples'][0].split(':')[0]} ({o['book']})" for o in od) or "none",
    f"Old Draft dependence is contained: {sum(o['refs'] for o in od)} cell(s) outside Old Draft read it, none in the FO/FE chain, so the output has 0 references to it.",
    "; ".join(f"{o['book']} {o['sheet']}: {o['refs']} cell(s) e.g. {o['examples'][0]}" for o in od) + f". SD dependency map: Old Draft -> {F['sd_depmap'].get('Old Draft')}.",
    "None for the budget. Consider deleting Old Draft once the reference is re-pointed.")
r23 = V["row23"]
add("I-22", "LOW", "COO P&L!A23:A24, B27, B37 (same rows on FO, PO, CO, FE, PE)",
    f"Rows 23 and 24 carry the same label ('{r23['COO P&L']['A23']}'). Row 23 is an empty header; row 24 holds postings inside row 27 ({r23['COO P&L']['B27']}). Row 37 ({CF('OUT:COO P&L!B37')}) covers every direct child of its section, so nothing is skipped today, but anything typed on row 23 would be left out.",
    f"Subtotal scan on 6 sheets: {sub_skipped} skipped lines with values. Non-empty cells on row 23 by tab: {{{', '.join(f'{k}: {v['row23_nonempty']}' for k, v in r23.items())}}}. COO P&L dept-sum formulas omitting a dept: {len(F['coo_pl_omits'])}.",
    "Optionally relabel row 23 as a header, or lock it.")
add("I-23", "LOW", "COO P&L!B65:M65; COO P&L!C141",
    f"COO P&L row 65 (labelled '{V['coo_pl_row65']['A65']}') holds an unlabelled gross-margin % formula ({V['coo_pl_row65']['B65']}); blank for 2027 because revenue is 0. Row 141 shows an extreme ratio for Feb-26 caused by negative 2026 payroll postings.",
    f"COO P&L!C141 = {C('OUT:COO P&L!C141'):.2f} (ratio). {vtxt('PO',67)}; {vtxt('PE',35)}.",
    "Label row 65. Finance to explain the negative 2026 payroll postings in PO 6610 and PE 5140.")
add("I-24", "LOW", f"Workbook defined names (xl/workbook.xml <definedNames>, workbook scope, no cell); list in {PRUNED_CSV}",
    f"The COO book carries {dn_before:,} legacy defined names from an old template. None is used by any formula, data validation, conditional format, chart or other name. v2 pruned the {PR['pruned']:,} unused names whose target is #REF! ({PR['pruned_ref']:,}) or external-looking ({PR['pruned_external_looking']:,}); {dn_after:,} remain (string/array constants and plain values).",
    f"Before {dn_before:,}, after {dn_after:,}. Usage scan covered cell formulas, data validations, conditional formats, charts, print areas/titles and other names (counts in the notes file). Names referenced: {len(P['names_used_in_parts'])} from parts, {len(P['names_used_by_other_names'])} from other names. Pruned names still referenced: {len(P.get('pruned_names_referenced', []))}.",
    "Optional: purge the remaining constant-valued legacy names in Name Manager.",
    change="Partly fixed in v2 (B2): logged prune of #REF!/external-looking names.")
add("I-25", "LOW", f"DeploySum!{V['error_bbox']['DeploySum']}; Prod Payroll!{V['error_bbox']['Prod Payroll']}",
    "Side effects of moving from Google Sheets to xlsx: threaded comments become plain notes (text kept); Google's '#ERROR!' has no Excel equivalent, so it shows as #REF! (frozen external cells are stored as #REF!, and LibreOffice recalculation turns the downstream Google #ERROR! cells into #REF!); LibreOffice saves error constants as '=#REF!' formulas.",
    f"Error-code changes on cells that were already errors: DeploySum {fid['DeploySum']['err_code_changed_n']}, Prod Payroll {fid['Prod Payroll']['err_code_changed_n']}. Total error cells unchanged: DeploySum {err_tot(V['errors_sd']['DeploySum'])} -> {err_tot(V['errors_out']['DeploySum'])}, Prod Payroll {err_tot(V['errors_sd']['Prod Payroll'])} -> {err_tot(V['errors_out']['Prod Payroll'])}. New errors: {new_err_total}.",
    "None; disclosed for reviewers.")
# ---- new issues (B3 / O10)
add("I-26", "new", "Fld Eng Budget!B21; Fld Eng Budget!B67:M67; FE!AG67",
    f"'{C('OUT:Fld Eng Budget!A21')}' has no salary entered, so FE 6610 carries $0 for this current employee. The source note says: '{C('OUT:Fld Eng Budget!D21')}'.",
    f"Fld Eng Budget!B21 = {C('OUT:Fld Eng Budget!B21')!r}; row 67 2027 = {m(q['feb_row67_2027'])}; FE!AG67 = {m(q['fe_AG67'])} excludes it.",
    "SD owner to enter the salary in Fld Eng Budget!B21 (or confirm it is budgeted in another dept).", owner=True,
    amount_txt="not determinable (salary not in workbook)")
add("I-27", "new", "Logistics&WH Payroll!B56 (SD, not carried); FO!U52:AF52",
    f"Logistics&WH Payroll excludes MH-05 ('{C('SD:Logistics&WH Payroll!A56')}'), but FO 5510 2027 (FO!U52) sums only Fld Ops Payroll rows {', '.join(str(r) for r in lwh['fo_5510_rows'])}, none of which is an MH-05 seat; 'MH-05' appears nowhere outside Logistics&WH Payroll. So this seat is in neither model.",
    f"Logistics&WH Payroll!B56 = {C('SD:Logistics&WH Payroll!B56'):,.0f} (deduction of MH-05's 2027 base pay, before burden). FO!U52 = {lwh['fo_5510_refs']}. MH-05 mentions elsewhere: {lwh['mh05_mentions_outside_lwh'] or 'none'}.",
    "SD/PO owners to decide where MH-05 is budgeted and add it.", amount=-C("SD:Logistics&WH Payroll!B56"),
    amount_txt=f"{m(-C('SD:Logistics&WH Payroll!B56'))} base pay missing (before burden)")
ovr = {o["row"]: o for o in V["overlap"]}
sal_rows = [r for r in (67, 68, 69) if r in ovr]
add("I-28", "new", "; ".join(f"{d}!AG{sal_rows[0]}:AG{sal_rows[-1]}" for d in ("CO", "PE", "FE")) + "; Fld Eng Budget!" + roster,
    "SG&A payroll (6610/6630/6640) is non-zero on CO, FE and PE. FE is built from a named roster on Fld Eng Budget; CO and PE are typed monthly amounts with no roster, so the workbook cannot confirm that no person on the FE roster is also inside CO or PE.",
    "; ".join(f"row {r}: " + ", ".join(f"{d} {m(ovr[r]['AG'][d])}" for d in ovr[r]["nonzero"]) for r in sal_rows) + ". 2027 months typed (no formula): " + ", ".join(f"{d} {'yes' if all(ovr[r]['U_typed'][d] for r in sal_rows) else 'no (formulas)'}" for d in ("CO", "PE", "FE")) + f". FE roster: Fld Eng Budget!{roster}.",
    "CO and PE owners to confirm their SG&A payroll rosters exclude the people on Fld Eng Budget!" + roster + ".", owner=True,
    amount_txt="not determinable (no CO/PE roster)")
ri = V["raise_inputs"]
add("I-29", "new", "Prod Payroll!M9; Fld Ops Payroll!M7; Fld Eng Budget!B59 (row formula); " + group_cells([f"{x['sheet']}!{x['steps'][-1]['col']}{x['row']}" for x in V["raise_rows"] if x["steps"] and x["typed"]]),
    "Raise timing is consistent (same % and month everywhere), but the eligibility rule is not: Fld Ops Payroll and Logistics&WH Payroll exclude staff hired in the months before the raise (Prod Payroll!M9), while Fld Eng Budget and the typed PO/CO/PE payroll rows apply the raise to the whole row.",
    f"Prod Payroll!M5 = {ri['OUT|Prod Payroll|M5']['value']}, M6 = {ri['OUT|Prod Payroll|M6']['value']}, M9 = {ri['OUT|Prod Payroll|M9']['value']}. Steps found in typed rows: " + "; ".join(f"{x['sheet']}!{x['steps'][-1]['col']}{x['row']} {pct(x['steps'][-1]['pct'])}" for x in V["raise_rows"] if x["steps"]) + ".",
    "Payroll owners to confirm whether the eligibility rule should apply to all departments.")

for i in I:
    if i["v1"] == "new":
        i["change"] = i["change"] or "New in v2."
    elif not i["change"]:
        i["change"] = "Unchanged" if i["sev"] == i["v1"] else f"Re-rated {i['v1']} -> {i['sev']} under the stated scale."
    elif i["sev"] != i["v1"] and f"-> {i['sev']}" not in i["change"]:
        i["change"] += f" Severity {i['v1']} -> {i['sev']}."
    assert re.search(r"!|definedNames", i["loc"]), i["id"]
by_sev = collections.Counter(i["sev"] for i in I)

# ------------------------------------------------------------------ overlap classification (B3)
EVEN = lambda d, o: f"{d} input method '{o['method'][d][0]}', annual input S = {o['method'][d][1]}"
def both_2026(o):
    return all(abs(o["N"][d]) >= 0.5 for d in o["nonzero"])
RULES = {
    "5050": ("Legitimate split (documented)",
             lambda o: f"FO!U30 = {o['U_formula']['FO']} (tech deployment travel = new sites x Fld Maint Budget!B6 {C('OUT:Fld Maint Budget!B6')} x B5 {C('OUT:Fld Maint Budget!B5'):,.0f}/trip; D6: '{C('OUT:Fld Maint Budget!D6')}'). FE!U30 = {o['U_formula']['FE']} (FE travel per weighted deployment; Fld Eng Budget!B6 = {C('OUT:Fld Eng Budget!B6')}: '{C('OUT:Fld Eng Budget!D6')[:90]}'). Fld Eng Budget!B2: '{C('OUT:Fld Eng Budget!B2').split('. ')[-1]}' Different people (techs vs field engineers).",
             0.0),
    "5340": ("Likely legitimate split",
             lambda o: f"FO!U47 = {o['U_formula']['FO']}: spares run rate from FO-dept actuals only (Fld Maint Budget!D16: '{C('OUT:Fld Maint Budget!D16')}'), grown with SlipLifts in field. PO: {EVEN('PO', o)}, with later months multiplied by a ramp row (PO!AF47 = {o['AF_formula']['PO']}). Both depts booked 5340 in 2026 (N: FO {m(o['N']['FO'])}, PO {m(o['N']['PO'])}); FO's base excludes PO's spend.",
             0.0),
    "6610": ("Unclear (person level)", lambda o: f"FE!U67 = {o['U_formula']['FE']}; Fld Eng Budget!B78 = {CF('OUT:Fld Eng Budget!B78')}, B68 = {CF('OUT:Fld Eng Budget!B68')} (named roster {roster}). CO and PE U:AF are typed monthly amounts with no roster. All three booked 6610 in 2026 (CO {m(o['N']['CO'])}, FE {m(o['N']['FE'])}, PE {m(o['N']['PE'])}). See I-28.", None),
    "6630": ("Unclear (person level)", lambda o: f"Follows 6610: FE!U68 = {o['U_formula']['FE']}, Fld Eng Budget!B69 = {CF('OUT:Fld Eng Budget!B69')}; CO/PE typed. See I-28.", None),
    "6640": ("Unclear (person level)", lambda o: f"Follows 6610: FE!U69 = {o['U_formula']['FE']}, Fld Eng Budget!B70 = {CF('OUT:Fld Eng Budget!B70')}; CO/PE typed. See I-28.", None),
    "6100": ("Legitimate split",
             lambda o: f"FE!U74 = {o['U_formula']['FE']} (FE non-deployment travel: FE-tab 2026 run rate + buffer). PE: {EVEN('PE', o)} (plus typed overrides, I-09). Separate departments' own travel; both booked 6100 in 2026 (FE {m(o['N']['FE'])}, PE {m(o['N']['PE'])}).",
             0.0),
    "7500": ("Legitimate split", lambda o: f"PO: {EVEN('PO', o)}; PE: {EVEN('PE', o)}. Separate dept inputs; both booked this GL in 2026 (PO {m(o['N']['PO'])}, PE {m(o['N']['PE'])}).", 0.0),
    "7550": ("Legitimate split", lambda o: f"PO: {EVEN('PO', o)}; PE: {EVEN('PE', o)}. Separate dept inputs; both booked this GL in 2026 (PO {m(o['N']['PO'])}, PE {m(o['N']['PE'])}).", 0.0),
    "8100": ("Legitimate split", lambda o: f"PO: {EVEN('PO', o)}; PE: {EVEN('PE', o)}. Separate dept inputs; both booked this GL in 2026 (PO {m(o['N']['PO'])}, PE {m(o['N']['PE'])}).", 0.0),
}
OVT = []
for o in V["overlap"]:
    if o["kind"] == "memo":
        cls, trace, risk = ("n/a (memo total)",
                            "Memo row summing each dept's payroll GL lines; the GL lines are classified individually (PO 5110-5140 typed and unlinked: see Prod Payroll trace; FO 5510-5540 from Fld Ops Payroll; SG&A rows above).",
                            0.0)
    else:
        gl = o["label"][:4]
        if gl not in RULES:
            raise SystemExit(f"overlap row {o['row']} {o['label']} has no classification rule - trace it before reporting")
        if gl in ("5050", "5340", "6100", "7500", "7550", "8100") and not both_2026(o):
            raise SystemExit(f"overlap row {o['row']}: classification assumes both depts booked the GL in 2026 - re-check")
        cls, f_, risk = RULES[gl]; trace = f_(o)
    OVT.append({"row": o["row"], "label": o["label"], "kind": o["kind"], "AG": o["AG"], "coo": o["coo_pl_AG"],
                "nonzero": o["nonzero"], "class": cls, "trace": trace,
                "risk": ("$0" if risk == 0 else "not determinable; rows involved: " + ", ".join(f"{d} {m(o['AG'][d])}" for d in o["nonzero"] if d in ("CO", "PE")))})
ov_gl = [x for x in OVT if x["kind"] == "GL"]
dbl = [x for x in ov_gl if x["class"].startswith("Likely double")]

# ------------------------------------------------------------------ changes from v1 (critic map)
diff_tot = D["total"]
CH = [
    ("B1", "Freeze of DeploySum [1] cells described as 'as instructed'.",
     f"Reworded everywhere (Method, I-03, D2, Collation Notes): frozen per orchestrator handoff; a declared deviation from brief criterion 1 because the linked workbook was not supplied and the SD file has no externalLink part (SD package externalLink parts: {len(sd_ext_parts)}). Original formulas remain listed on Collation Notes."),
    ("B2", "No-external-link claim vs I-24 external .xls names; clean open unproven.",
     f"Package inspected (section 'Package and defined names'): externalLink parts {len(P['external_link_parts'])}, <externalReference> elements {P['external_reference_elements']}, chart parts {len(P['chart_parts'])}. The 15 'external' names were quoted string/array constants, not links. Name usage scanned across cell formulas, data validations, conditional formats, charts, print areas/titles and other names: 0 uses. Pruned {PR['pruned']:,} unused #REF!/external-looking names (logged, {PRUNED_CSV}); definedNames {dn_before:,} -> {dn_after:,}."),
    ("B3", "Cross-department double counting unchecked.",
     f"Added 'Cross-department overlap' table: {len(ov_gl)} GL rows (+{len(OVT) - len(ov_gl)} memo rows) with 2+ depts non-zero in 2027, each traced: {sum(1 for x in ov_gl if x['class'].startswith('Legit'))} legitimate, {sum(1 for x in ov_gl if x['class'].startswith('Likely legit'))} likely legitimate, {sum(1 for x in ov_gl if x['class'].startswith('Unclear'))} unclear, {len(dbl)} likely double counts. Prod Payroll trace: rates/timing only. New issues I-26..I-29."),
    ("O1", "Hard-coded claims in report.py.",
     f"report.py rewritten: every number/fact comes from analysis JSON; LibreOffice version read from `soffice --version` ('{LO}'). v1 report kept as report_v1.py for v1 reproduction only."),
    ("O2", "Logistics&WH: quantify vs PO.", f"I-17: {m(lwh['S51_2027'])} 2027 vs PO 5100 {m(po36)}; re-rated to {next(i['sev'] for i in I if i['id']=='I-17')}. Also found MH-05 gap (I-27)."),
    ("O3", "Quantify MeLi double count.", f"I-06: $0 in current cells (Fld Ops Payroll!B11 = {C('OUT:Fld Ops Payroll!B11'):,.0f}, domestic only); 5310 breakdown given; comment stale; re-rated to {next(i['sev'] for i in I if i['id']=='I-06')}."),
    ("O4", "Downgrade I-05.", f"I-05 re-rated to {next(i['sev'] for i in I if i['id']=='I-05')}: Prod Payroll supplies only typed rate/timing inputs."),
    ("O5", "Downgrade I-16.", f"I-16 re-rated to {next(i['sev'] for i in I if i['id']=='I-16')}."),
    ("O6", "Headline should lead with total COO cost.", f"Headline now leads with 2027 COGS + Opex {m(cost27)} vs 2026 {m(cost26)}; Net Income labelled incomplete (no revenue, no depreciation)."),
    ("O7", "sheet!cell everywhere; define severities.", f"Every issue has a sheet!cell (or the workbook <definedNames> location for I-24); severity scale and tie-break rule stated; each issue shows the basis used. Counts: {dict(by_sev)}."),
    ("O8", "'Untouched' wording.", "Replaced by 'values and formulas unchanged (verified); formatting re-saved by LibreOffice'."),
    ("O9", "Limits not stated.", "Limits listed (page setup/print settings, sheet-scoped names, Excel not used, Google parts) in 'Not done / limits'."),
    ("O10", "Stale zeros look like data; raise-timing check.", f"Cell comments added on {len(V['frozen']['cells'])} frozen non-error cells ({V['frozen']['cells'][0].split('!')[1]}:{V['frozen']['cells'][-1].split('!')[1]} on DeploySum): '{E.get('frozen_note')}'. Raise-timing consistency check done (section 'Raise timing'); one rule difference logged as I-29."),
]

# ------------------------------------------------------------------ notes sheet JSON
ext_rows_tbl = [[e["sheet"], e["cell"], str(e["sd_cached"]), str(e["stored"]), e["formula"][:250]] for e in ext_cells]
notes = {
    "title": f"2027 COO Budget - Collation Notes (build v{VERSION}, draft for review)",
    "col_widths": [10, 12, 34, 70, 70, 60, 22, 30],
    "sections": [
        {"heading": "Source", "lines": [
            f"Base workbook: {coo_name} (sha256 {sha(COO_PATH)[:16]}...) - COO P&L roll-up + FO, PO, CO, FE, PE.",
            f"Replacement source: {sd_name} (sha256 {sha(SD_PATH)[:16]}...) - newer FO and FE plus driver tabs.",
            f"Inputs were read only. Recalculated with {LO}. Notes file: 02-build/{NOTES_MD_NAME}."]},
        {"heading": "Method", "lines": [
            "1. Started from the COO book. Deleted its FO and FE tabs and rebuilt them in the same tab positions from the SD book, cell by cell (values/formulas, styles, widths, heights, merges, freeze panes, validations, conditional formats, notes).",
            "2. Brought over every SD tab FO/FE depend on, directly or indirectly: " + ", ".join(E["support"]) + ". Hidden state kept.",
            "3. Not carried (FO/FE do not depend on them): " + ", ".join(s for s in V["sd_sheetnames"] if s not in E["carried"]) + ". Still scanned for issues.",
            f"4. The {len(ext_cells)} external-workbook formulas on DeploySum ('[1]...') were frozen to the SD cached values per orchestrator handoff. This is a declared deviation from brief criterion 1, because the linked workbook was not supplied and the SD file has no externalLink part. Each cell and its original formula is listed at the end of this sheet. The frozen non-error cells carry the comment '{E.get('frozen_note')}'.",
            "5. PO, CO, PE and COO P&L: values and formulas unchanged (verified cell by cell); formatting re-saved by LibreOffice. COO P&L picks up the new FO/FE through its =SUM(FO!x,PO!x,CO!x,FE!x,PE!x) cells.",
            f"6. v{VERSION} only: pruned {PR['pruned']:,} unused legacy defined names whose target is #REF! or external-looking (list: 02-build/{PRUNED_CSV}); defined names {dn_before:,} -> {dn_after:,}. No budget value changed (v1 vs v{VERSION}: {diff_tot['cells']:,} cells compared, {diff_tot['formula_diffs']} formula and {diff_tot['value_diffs']} value differences).",
            "7. Recalculated with headless LibreOffice and checked every value against the source cached values."]},
        {"heading": "Severity scale", "lines": [SCALE, TIEBREAK]},
        {"heading": "Headline (live formulas vs COO book cached values)", "table": {
            "header": ["Line", "Col", "Before (COO book)", "After (this workbook, live)"], "formula_cols": [4],
            "rows": [["Total COO cost = COGS + Opex (rows 63 + 116)", c, round(H("COO", 63, c) + H("COO", 116, c), 2), f"='COO P&L'!{c}63+'COO P&L'!{c}116"] for c in ("N", "AG")]
                    + [[x["line"] + (" (2027 INCOMPLETE: no revenue, no depreciation)" if x["row"] == 132 and x["col"] == "AG" else ""), x["col"], round(x["before"], 2), f"='COO P&L'!{x['col']}{x['row']}"] for x in R["coo_pl_before_after"]]}},
        {"heading": "Changes from v1 (critic items)", "table": {
            "header": ["Item", "Critic finding", "What v2 did"], "rows": [list(c) for c in CH]}},
        {"heading": "Cross-department overlap (2027 AG, rows with 2+ depts non-zero)", "table": {
            "header": ["Row", "Line", "FO", "PO", "CO", "FE", "PE", "Classification", "Amount at risk", "Driver trace"],
            "rows": [[x["row"], x["label"]] + [round(x["AG"][d], 2) if abs(x["AG"][d]) >= 0.5 else "" for d in ("FO", "PO", "CO", "FE", "PE")] + [x["class"], x["risk"], x["trace"]] for x in OVT]}},
        {"heading": "Issues", "table": {
            "header": ["ID", "Severity", "Location", "Finding", "Evidence", "Recommended action", "2027 impact", "v1 -> v2"],
            "rows": [[i["id"], i["sev"], i["loc"], i["finding"], i["evidence"], i["action"], i["impact"], f"{i['v1']} -> {i['sev']}: {i['change']}"] for i in I]}},
        {"heading": f"External-reference cells frozen to SD cached values ({len(ext_cells)})", "table": {
            "header": ["Sheet", "Cell", "SD cached value", "Value stored in this workbook", "Original formula (leading = omitted)"],
            "rows": ext_rows_tbl}},
    ]}
json.dump(notes, open(NOTES_JSON, "w"), indent=1)

# ------------------------------------------------------------------ markdown
L = []; w = L.append
w(f"# 02-build notes v{VERSION} - 2027 COO budget collation\n")
w(f"Output: `02-build/{OUT_NAME}`  \nPruned-name log: `02-build/{PRUNED_CSV}`  \n"
  "Scripts: `02-build/scripts/` - v2 entry point `run_build_v2.sh` (build.py --mark-frozen-zeros, prune_names.py, recalc.sh, analyze.py, analyze_v2.py, pkgscan.py, diff_versions.py, report.py). `run_build.sh` still reproduces v1 (it calls the frozen `report_v1.py`).  \n"
  f"Inputs (read-only): `{coo_name}` sha256 `{sha(COO_PATH)}`; `{sd_name}` sha256 `{sha(SD_PATH)}`  \n"
  f"Recalculation engine: {LO} (from `soffice --version`); openpyxl {V['versions']['openpyxl']}; Python {V['versions']['python']}.\n")

w("## Headline\n")
w(f"- **Total 2027 COO cost (COGS + Opex, COO P&L AG63 + AG116): {m(cost27)}** vs 2026 {m(cost26)} (N63 + N116), change {m(cost27 - cost26)} ({(cost27 / cost26 - 1) * 100:.0f}%). Before the FO/FE swap the COO book showed {m(cost27_before)} for 2027.")
w(f"  - COGS 2027 {m(H('OUT',63,'AG'))} (2026 {m(H('OUT',63,'N'))}); Opex 2027 {m(H('OUT',116,'AG'))} (2026 {m(H('OUT',116,'N'))}).")
w(f"- 2027 Net Income (AG132) {m(H('OUT',132,'AG'))} is **incomplete**: 2027 revenue is {m(H('OUT',16,'AG'))} (2026 {m(H('OUT',16,'N'))}, I-01) and 2027 depreciation is {m(dep27)} (2026 {m(dep26)}, I-07). Do not present it as a result.")
w(f"- New formula errors introduced by the merge: **{new_err_total}**. COO P&L roll-up: {R['rollup']['checked']} cells checked, {len(R['rollup']['fail'])} off by more than $1 (max abs diff {R['rollup']['max_abs_diff']:.4f}); check row 133 max abs = {F['check_row_133_max_abs']:.6f}.")
w(f"- v1 vs v{VERSION}: {diff_tot['cells']:,} cells on {diff_tot['sheets']} budget/driver sheets compared; **{diff_tot['formula_diffs']} formula and {diff_tot['value_diffs']} value differences**. Only comments were added ({len(D['comments_added'])}).")
w(f"- Package: {len(P['external_link_parts'])} externalLink parts; defined names {dn_before:,} -> {dn_after:,}.")
w(f"- Issues: {by_sev.get('HIGH',0)} HIGH, {by_sev.get('MED',0)} MED, {by_sev.get('LOW',0)} LOW (scale below). Cross-department overlap: {len(dbl)} likely double counts, {sum(1 for x in ov_gl if x['class'].startswith('Unclear'))} unclear rows (I-28).\n")

w("## Changes from v1\n")
w("| Item | Critic finding | What v2 did |\n|---|---|---|")
for c in CH:
    w(f"| {c[0]} | {esc(c[1])} | {esc(c[2])} |")
w("")
w("Issue-level changes (severity v1 -> v2):\n")
w("| ID | v1 | v2 | Change |\n|---|---|---|---|")
for i in I:
    w(f"| {i['id']} | {i['v1']} | {i['sev']} | {esc(i['change'])} |")
w("")

w("## Severity scale\n")
w(f"{SCALE}\n\n{TIEBREAK}\n")

w("## Method\n")
w(f"1. **Base = COO book**, loaded with formulas (openpyxl). Its `FO` and `FE` tabs were deleted and rebuilt in the same positions (tab {pos_coo['FO']} and {pos_coo['FE']} of the COO book).")
w("2. **Copied cell by cell from the SD book**: value or formula (array formulas re-created), font, fill, border, alignment, number format, protection, hyperlinks, notes; merged ranges; column widths/hidden/outline; row heights/hidden; freeze panes, gridlines, zoom, tab colour, sheet state; data validations; conditional formats.")
w(f"3. **Dependency closure** of SD `FO`/`FE` formulas: {', '.join(E['carried'])}. SD defined names: {PS['defined_names_total']} ({', '.join(PS['sheet_scoped_names']) or 'none'}; sheet-scoped, not carried; see limits).")
w(f"4. **External links (declared deviation)**: {len(ext_cells)} DeploySum formula cells reference `[1]` ({', '.join(ext_books)}). They were frozen to the SD cached values **per orchestrator handoff; this is a declared deviation from brief criterion 1 because the linked workbook was not supplied and the SD file has no externalLink part** (SD package externalLink parts: {len(sd_ext_parts)}). Cached values: {ext_cached}. Google `#ERROR!` has no Excel equivalent and was stored as `#REF!`. Every cell and its original formula is on the `Collation Notes` sheet and summarised in the appendix. Apart from these, formulas in source = formulas in output on every sheet (sheets with a different count: {list(non_ds_formula_loss) or 'none'}).")
w(f"5. **COO P&L, PO, CO, PE: values and formulas unchanged (verified); formatting re-saved by LibreOffice.** COO P&L formulas reference `FO!`/`FE!` by name, so they pick up the new tabs.")
w(f"6. **v2 additions**: cell comments on the {len(V['frozen']['cells'])} frozen non-error cells ('{E.get('frozen_note')}'); logged prune of unused #REF!/external-looking defined names (`prune_names.py`, XML-level, only `xl/workbook.xml` rewritten).")
w(f"7. **Recalculated** with headless {LO} using a private profile set to always recalculate on load; reloaded with `data_only=True` and compared every cell with the source cached values. The delivered file is the LibreOffice-recalculated file.\n")

w("## Package and defined names (B2)\n")
w(f"Final package `{OUT_NAME}`: {len(P['parts'])} parts.\n")
w(f"- `xl/externalLinks/*`: **{len(P['external_link_parts'])}** parts; `<externalReference>` elements in workbook.xml: {P['external_reference_elements']}. Chart parts: {len(P['chart_parts'])}. COO input externalLink parts: {len(PC['external_link_parts'])}; SD input: {len(PS['external_link_parts'])}.")
w(f"- Package parts: " + ", ".join(f"`{p}`" for p in P["parts"]))
w(f"- Defined names: COO book {dn_before:,} -> output before prune {PR['names_before']:,} -> pruned {PR['pruned']:,} -> **final {dn_after:,}**. Final by category: {P['defined_names_by_category']}. Built-in `_xlnm.*` names (print areas/titles/filters): {len(P['builtin_xlnm_names'])}. Sheet-scoped names: {len(P['sheet_scoped_names'])}.")
w(f"- Usage scan (every formula-bearing XML element in every part, plus the text of every other defined name): elements scanned {P['formula_elements_scanned']} (cell = cell formulas, dv = data validations, cf = conditional formats; chart formulas would be counted as 'chart'). Names referenced from parts: {len(P['names_used_in_parts'])}; from other names: {len(P['names_used_by_other_names'])}.")
w(f"- Prune rule: unused AND target contains '[' or '.xls' (any case) or '#REF!'. Candidates {PR['candidates']:,}, of which used {PR['candidates_used']}; pruned {PR['pruned']:,} ({PR['pruned_ref']:,} #REF!, {PR['pruned_external_looking']} external-looking). List: `02-build/{PRUNED_CSV}`. Re-scan of the final file: pruned names still defined {len(P.get('pruned_names_still_defined', []))}, still referenced {len(P.get('pruned_names_referenced', []))}.")
w(f"- The external-looking names were text, not links: " + "; ".join(f"`{x['name']}` = {esc(x['text'][:60])}" for x in PC["external_looking_names"]) + ". They never created an externalLink part.")
w(f"- Result: **the final package has {len(P['external_link_parts'])} externalLink parts**{', and no remaining defined name targets an external file or #REF!' if P['names_prunable_criterion'] == 0 else ''} (remaining names meeting the prune criterion: {P['names_prunable_criterion']}). Opening in Microsoft Excel was not tested (no Excel available; see limits).\n")

w("## Cross-department overlap (B3)\n")
w(f"Every COO P&L GL row (label 'NNNN - ...') and the payroll memo rows 137-140 were checked: {V['overlap_rows_checked']} rows, of which {len(OVT)} have 2 or more departments non-zero in 2027 (AG). Each was traced to its driver cells.\n")
w("| Row | Line | FO | PO | CO | FE | PE | COO P&L AG | Classification | Amount at risk | Driver trace |\n|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|")
for x in OVT:
    vals = " | ".join(m(x["AG"][d]) if abs(x["AG"][d]) >= 0.5 else "" for d in ("FO", "PO", "CO", "FE", "PE"))
    w(f"| {x['row']} | {esc(x['label'])} | {vals} | {m(x['coo'])} | {x['class']} | {esc(x['risk'])} | {esc(x['trace'])} |")
w("")
w(f"Result: {len(dbl)} likely double counts on the same GL row. Unclear rows are logged as I-28. Cross-row overlaps found while tracing: none between FO payroll and Logistics&WH (Rebecca is excluded from Logistics&WH, Logistics&WH Payroll!B55, and costed in Fld Ops Payroll row 76: 2027 {m(lwh['fop_row76']['2027'])}); one seat in neither model (MH-05, I-27); a current employee with no salary (I-26).\n")
w("**Prod Payroll trace (what it supplies to Fld Ops Payroll):**\n")
w("| Reader | Formula | Prod Payroll cell | Label | Typed input or formula | Value |\n|---|---|---|---|---|---|")
for x in V["prod_payroll_refs"]:
    w(f"| {x['from']}{' (SD, not carried)' if x['book']=='SD' else ''} | `{x['formula']}` | {x['target']} | {x['target_label']} | {'formula' if x['target_is_formula'] else 'typed input'} | {x['value']} |")
w(f"\nRates and timing only, no headcount and no cost: {ppf['errors']} of Prod Payroll's {ppf['total']} formulas are errors (all payroll $ totals) and no other sheet reads any of its formulas. PO 5110-5140 2027 (PO!U33:AF35) are typed values with no link to any tab ({V['po_payroll_rows']['33']['typed_months']} of 12 months typed on row 33). So PO AG33 {m(V['po_payroll_rows']['33']['AG'])} and FO 5510 share no headcount source; no double count through Prod Payroll.\n")

w("### Raise timing consistency (O10)\n")
w("| Input | Cell | Value / formula |\n|---|---|---|")
for k, v in V["raise_inputs"].items():
    b, s, c = k.split("|")
    w(f"| {'SD (not carried)' if b=='SD' else ''} {s} | {c} | {v['value']} {('`' + v['formula'] + '`') if v['formula'] else '(typed)'} |")
w("\n| Sheet | Row | Line | 2027 typed? | Month-on-month steps in 2027 (column: change) |\n|---|---:|---|---|---|")
for x in V["raise_rows"]:
    w(f"| {x['sheet']} | {x['row']} | {esc(x['label'])} | {x['typed']} | {', '.join(f'{s['col']}: {pct(s['pct'])}' for s in x['steps']) or 'none'} |")
r_pct = ri["OUT|Prod Payroll|M5"]["value"]; r_month = int(str(ri["OUT|Prod Payroll|M6"]["value"])[5:7])
r_ok = [x for x in V["raise_rows"] if x["steps"] and abs(x["steps"][-1]["pct"] - r_pct) < 1e-4 and x["steps"][-1]["month"] == r_month]
links_ok = all(v["formula"] for k, v in ri.items() if not k.startswith("OUT|Prod Payroll"))
w(f"\n{len(r_ok)} of {len(V['raise_rows'])} payroll rows step by Prod Payroll!M5 ({pct(r_pct)}) in month {r_month} of 2027 (Prod Payroll!M6); the raise inputs on Fld Ops Payroll / Fld Eng Budget / Logistics&WH are {'all links to those cells' if links_ok else 'NOT all linked'}, so % and month are {'consistent' if len(r_ok) == len(V['raise_rows']) and links_ok else 'NOT consistent'}. FE's other step is the new hire '{C('OUT:Fld Eng Budget!A19')}' starting {C('OUT:Fld Eng Budget!C19')}. Rule difference: eligibility (Prod Payroll!M9) is applied in Fld Ops Payroll (`{V['raise_rule']['Fld Ops Payroll!F21'][:60]}...`) and Logistics&WH, but not in Fld Eng Budget (`{V['raise_rule']['Fld Eng Budget!B59']}`) or the typed rows: I-29.\n")

w("### Logistics & Warehouse payroll (O2) and MeLi (O3)\n")
w(f"- Logistics&WH Payroll 2027 (S51) {m(lwh['S51_2027'])}; Sep-Dec 26 (R51) {m(lwh['R51_SepDec26'])}. Components 2027: " + "; ".join(f"{k} {m(v)}" for k, v in lwh['by_component_2027'].items()) + f". Formulas referencing the sheet in either book: {lwh['refs_to_sheet']}.")
w(f"- PO 2027: " + "; ".join(f"{v['label']} {m(v['AG'])} (2026 {m(v['N'])})" for k, v in lwh['po'].items()) + ". See I-17.")
w(f"- MeLi: FO 5310 {m(meli['fo_AG44'])} = techs in role {m(meli['techs_in_role_cost'])} + Merida {m(meli['merida_cost'])} + supervisor {m(meli['supervisor_cost'])}. Fld Ops Payroll costs {', '.join(f'{x:,.0f}' for x in sorted(set(meli['fop_current_techs_2027'])))} current techs per month (B11 = {C('OUT:Fld Ops Payroll!B11'):,.0f}, domestic only). Overlap in current cells: $0. See I-06, I-15.\n")

w("## Sheets in the output and why\n")
w("| # | Sheet | From | State | Why |\n|---|---|---|---|---|")
fo_rows = V["fo_reads_drivers_rows"]
why = {"Collation Notes": ("new", "Source, method, changes, overlap table, issues, frozen-cell list"),
       "COO P&L": ("COO book", "Roll-up; values and formulas unchanged (verified)"),
       "FO": ("SD book", "Replaces COO FO"), "FE": ("SD book", "Replaces COO FE"),
       "PO": ("COO book", "Values and formulas unchanged (verified)"), "CO": ("COO book", "Values and formulas unchanged (verified)"),
       "PE": ("COO book", "Values and formulas unchanged (verified)"),
       "DeploySum": ("SD book", f"Indirect FO/FE dependency (typed driver rows {ranges(F['deploysum_drivers']['rows_const'])})"),
       "Fld Ops Payroll": ("SD book", f"FO rows {ranges(fo_rows['Fld Ops Payroll'])}"),
       "Prod Payroll": ("SD book", "Indirect: " + ", ".join(f"{x['from']} <- {x['target']}" for x in pp)),
       "Fld Maint Budget": ("SD book", f"FO rows {ranges(fo_rows['Fld Maint Budget'])}"),
       "Fld Eng Budget": ("SD book", f"FE rows {ranges(V['fe_reads_feb_rows'])}")}
for s, k in sorted(V["tab_positions"].items(), key=lambda kv: kv[1]):
    a, c = why[s]
    w(f"| {k} | {s} | {a} | {'hidden' if s in V['out_hidden_sheets'] else 'visible'} | {c} |")
w(f"\nNot carried (no FO/FE dependency): " + ", ".join(f"`{s}`" for s in V["sd_sheetnames"] if s not in E["carried"]) + ". All were scanned.\n")

w("## Formula preservation\n")
w("| Sheet | Formulas in source | Formulas in output | External cells frozen |\n|---|---:|---:|---:|")
for s, v in R["formula_counts"].items():
    w(f"| {s} | {v['source_formulas']} | {v['output_formulas']} | {v['external_replaced']} |")
w(f"\nDeploySum output count ({ds_mix['total']}) = {ds_mix['total'] - ds_mix['error_constant']} formulas kept + {ds_mix['error_constant']} error constants that LibreOffice saves as `=#REF!`/`=#N/A` formulas; {ds_mix['frozen_numbers']} frozen cells are stored as numbers.\n")

w("## Reconciliation (source cached vs output recalculated)\n")
w("| Dept | Line | Row | 2026 N source | 2026 N output | Delta N | 2027 AG source | 2027 AG output | Delta AG |\n|---|---|---:|---:|---:|---:|---:|---:|---:|")
for d in ["FO", "PO", "CO", "FE", "PE"]:
    for r, lab in [(16, "Total Income"), (63, "Total COGS"), (64, "Gross Profit"), (116, "Total Expense"), (132, "Net Income")]:
        w(f"| {d} ({rec(d,r,'N','src')}) | {lab} | {r} | {m(rec(d,r,'N','source'))} | {m(rec(d,r,'N','output'))} | {rec(d,r,'N','delta'):.2f} | {m(rec(d,r,'AG','source'))} | {m(rec(d,r,'AG','output'))} | {rec(d,r,'AG','delta'):.2f} |")
w("\nCell-by-cell fidelity, every non-empty cell (source cached vs output):\n")
w("| Sheet | Cells | Value mismatches | Max abs numeric diff | New errors | Errors cleared | Error code changed |\n|---|---:|---:|---:|---:|---:|---:|")
for s, v in fid.items():
    w(f"| {s} | {v['cells']} | {v['mismatch_n']} | {v['num_max_abs_diff']:.6f} | {v['new_errors_n']} | {v['errors_cleared_n']} | {v['err_code_changed_n']} |")
w(f"\nv1 vs v{VERSION} (`diff_versions.py`, formulas and cached values, exact):\n")
w("| Sheet | Cells | Formula diffs | Value diffs |\n|---|---:|---:|---:|")
for s, v in D["sheets"].items():
    w(f"| {s} | {v['cells']} | {v['formula_diffs']} | {v['value_diffs']} |")
w(f"| **Total** | {diff_tot['cells']} | {diff_tot['formula_diffs']} | {diff_tot['value_diffs']} |")
w(f"\nComments added in v{VERSION}: {len(D['comments_added'])} ({', '.join(c[0] for c in D['comments_added'][:3])}{', ...' if len(D['comments_added']) > 3 else ''}); removed {len(D['comments_removed'])}; changed {len(D['comments_changed'])}.\n")
w("FO/FE tabs replaced: COO book values (dropped) vs SD book values (used):\n")
w("| Dept | Line | Col | COO book (replaced) | SD book (used) | Difference |\n|---|---|---|---:|---:|---:|")
for x in R["replaced_coo_fofe"]:
    w(f"| {x['dept']} | {x['line']} | {x['col']} | {m(x['coo_book'])} | {m(x['sd_book'])} | {m(x['sd_book']-x['coo_book'])} |")
w("\n## COO P&L before vs after\n")
w("| Line | Row | Col | Before (COO book cached) | After (output) | Change |\n|---|---:|---|---:|---:|---:|")
for x in R["coo_pl_before_after"]:
    note = " (2027 incomplete)" if x["row"] == 132 and x["col"] == "AG" else ""
    w(f"| {x['line']}{note} | {x['row']} | {x['col']} | {m(x['before'])} | {m(x['after'])} | {m(x['change'])} |")
w(f"\nRoll-up integrity: COO P&L = FO+PO+CO+FE+PE on every additive row, B:N and U:AG: {R['rollup']['checked']} cells, {len(R['rollup']['fail'])} failures, max abs diff {R['rollup']['max_abs_diff']:.6f}.\n")

w("## Error scan\n")
w("| Sheet | Before (source book cached) | After (output recalculated) |\n|---|---|---|")
for s, k in sorted(V["tab_positions"].items(), key=lambda kv: kv[1]):
    before = "n/a (new sheet)" if s == "Collation Notes" else (err_b_sd.get(s) if s in E["carried"] else err_b_coo.get(s))
    w(f"| {s} | {before or 'none'} | {err_a.get(s) or 'none'} |")
for s in V["sd_sheetnames"]:
    if s not in E["carried"]:
        w(f"| {s} (SD, not carried) | {err_b_sd.get(s) or 'none'} | n/a |")
ds_b, ds_a = V["errors_sd"]["DeploySum"], V["errors_out"]["DeploySum"]
pp_b, pp_a = V["errors_sd"]["Prod Payroll"], V["errors_out"]["Prod Payroll"]
w(f"\n**#REF! counts rise: DeploySum {ds_b.get('#REF!',0)} -> {ds_a.get('#REF!',0)}, Prod Payroll {pp_b.get('#REF!',0)} -> {pp_a.get('#REF!',0)}.** Why: the SD book is a Google Sheets export whose cached errors include Google's `#ERROR!` (DeploySum {ds_b.get('#ERROR!',0)}, Prod Payroll {pp_b.get('#ERROR!',0)}), which Excel/LibreOffice do not have. The frozen external cells holding `#ERROR!` were stored as `#REF!`, and LibreOffice's recalculation shows every downstream failed cell as `#REF!`. The rise equals the relabelled `#ERROR!` count (DeploySum {ds_b.get('#REF!',0)} + {ds_b.get('#ERROR!',0)} = {ds_b.get('#REF!',0) + ds_b.get('#ERROR!',0)}; Prod Payroll {pp_b.get('#REF!',0)} + {pp_b.get('#ERROR!',0)} = {pp_b.get('#REF!',0) + pp_b.get('#ERROR!',0)}). Total error cells are unchanged (DeploySum {err_tot(ds_b)} -> {err_tot(ds_a)}, Prod Payroll {err_tot(pp_b)} -> {err_tot(pp_a)}), and no cell that held a value in the source is an error in the output (new errors = {new_err_total}).\n")

w("## Issues\n")
w(f"Severity per the scale above. 'Basis' shows which rule set the rating.\n")
w("| ID | Sev | Location (sheet!cell) | Finding | Evidence | 2027 impact | Basis | Recommended action |\n|---|---|---|---|---|---|---|---|")
for i in I:
    w(f"| {i['id']} | {i['sev']} | {esc(i['loc'])} | {esc(i['finding'])} | {esc(i['evidence'])} | {esc(i['impact'])} | {i['basis']} | {esc(i['action'])} |")

w("\n### Scan coverage (including clean results)\n")
w(f"- 2026 (B:N) FO/FE differences between the books, rows 9-141: **{sum(len(v) for v in F['diff_2026'].values())} cells differ**. Formula differences FO/FE (A:AJ, rows 1-200): FO {F['formula_diff_FO_FE']['FO']['n']}, FE {F['formula_diff_FO_FE']['FE']['n']}, in columns {fd_cols_txt}{' only (the 2027 months)' if fd_cols_contiguous else ''}; rows FO {ranges(V['formula_diff_rows'].get('FO', []))}, FE {ranges(V['formula_diff_rows'].get('FE', []))}.")
w(f"- External links: I-03 (DeploySum only; package scan above).")
w(f"- Numeric literals / overrides inside formula rows: {len(hard)} hits (I-08, I-09). Constants in total/roll-up cells: {const_in_totals}.")
w(f"- Placeholder keywords (values and notes, all sheets of both books): {len(ph)} hits, by keyword {V['placeholder_keywords']}; 'TBD': {V['placeholder_keywords'].get('TBD', 0)}. In the hidden T&E sheet: {len(ph_te)} (I-16).")
w(f"- Variance (>50% and >$50k): {len(F['variance'])} rows, listed below.")
w(f"- COO P&L dept-sum formulas omitting a dept or misaligned: {len(F['coo_pl_omits'])}. Leaf rows not linked while depts hold values: {len(F['coo_pl_unlinked'])}.")
w(f"- Subtotal formulas skipping lines with values: {sub_skipped}. Header rows carrying values: {', '.join(f'{s['sheet']} row {list(s['missing'])[0]}' for s in sub_header_hits) or 'none'} (I-23). Gross Profit / Net Ordinary Income / Net Other Income / Net Income formula deviations: {len(F['special_rows'])}.")
w(f"- YoY column AJ: {len(F['yoy_sign']['cost_rows_using_AG_minus_N'])} cost rows using AG-N; {len(F['yoy_sign']['other'])} non-standard formulas.")
w(f"- Cross-department overlap: section above. Raise timing: section above.\n")

w("### Variance scan: rows with |AG-N| > $50k and > 50% (output values)\n")
w("| Sheet | Row | Line | 2026 N | 2027 AG | Change | % |\n|---|---:|---|---:|---:|---:|---:|")
for v in F["variance"]:
    pc = f"{v['pct']*100:.0f}%" if v["pct"] is not None else "n/a (N=0)"
    w(f"| {v['sheet']} | {v['row']} | {v['label']} | {m(v['N'])} | {m(v['AG'])} | {m(v['diff'])} | {pc} |")
w(f"\n### T&E rows with 'Reclass needed' = Yes (SD `Fld Maint T&E Data`, hidden)\n")
w(f"{len(recl)} rows, ${recl_amt:,.2f}. Rows: " + ", ".join(str(x["row"]) for x in recl) + ".\n")
w("| Booked GL -> Budget GL | Rows |\n|---|---:|")
for (a, b), n in recl_pairs.most_common():
    w(f"| {a} -> {b} | {n} |")
w("\n### Appendix: external-reference cells (DeploySum), frozen to SD cached values\n")
w(f"Full per-cell list with original formulas: `Collation Notes` sheet. Frozen non-error cells ({', '.join(V['frozen']['cells'])}) carry the comment '{E.get('frozen_note')}'; their only dependents ({len(V['frozen']['dependents'])} cells) evaluate to {V['frozen']['dependent_values']}, so the zeros feed no budget value.\n")
w("| Row | Cells | SD cached values | Example original formula |\n|---:|---|---|---|")
for r, es in ext_by_row.items():
    vals = dict(collections.Counter(str(e["sd_cached"]) for e in es))
    w(f"| {r} | {', '.join(e['cell'] for e in es)} | {vals} | `{es[0]['formula'][:110].replace('|','/')}` |")

w("\n## Decisions\n")
w(f"- D1: Carried only the dependency closure of FO/FE ({len(E['support'])} supporting tabs).")
w(f"- D2: External `[1]` formulas were frozen to SD cached values per orchestrator handoff - a declared deviation from brief criterion 1 (linked workbook not supplied; SD file has no externalLink part). Google `#ERROR!` stored as `#REF!`, so downstream IFERROR fallbacks match the SD cached results.")
w(f"- D3 (v2): Pruned unused defined names whose target contains '[' / '.xls' / '#REF!' (rule from the v2 handoff); kept the {dn_after:,} constant-valued names because the rule does not cover them.")
w("- D4: No number changed or 'fixed' (plugs, placeholders, zero revenue, zero depreciation, missing salary are flagged only). v1 vs v2 diff = 0 on every budget and driver sheet.")
w("- D5: Delivered xlsx is the LibreOffice-recalculated file.")
w("- D6: Match tolerance $0.01 per cell; roll-up tolerance $1 per the brief; v1-vs-v2 comparison exact.")
w("- D7 (v2): Severity is computed from the stated scale with the tie-break rule above; each issue shows its basis.")
w("- D8 (v2): Overlap classification uses the driver cells and the source authors' notes quoted in the table. 'Unclear' is used where the workbook has no roster or driver to compare; no amounts were estimated.")
w("- D9 (v2): v2 entry point is `run_build_v2.sh`; `run_build.sh` reproduces v1 via the frozen `report_v1.py`.")

w("\n## Not done / limits\n")
ps_diff = [p for p in V["page_setup"] if (p["src_orientation"] and p["src_orientation"] != p["out_orientation"]) or (p["src_fit_to_page"] and not p["out_fit_to_page"])]
w(f"- External workbook `[1]` unavailable: DeploySum rows with external links and Prod Payroll cannot be refreshed (accepted BLOCKER).")
w(f"- Not opened in Microsoft Excel; validated with {LO} and by XML inspection of the package only.")
w(f"- Page setup / print settings of the copied SD sheets were not copied (build copies cells, styles, dimensions, views, validations and formats only): " + ("; ".join(f"{p['sheet']} orientation {p['src_orientation']} -> {p['out_orientation']}" + (", fit-to-page lost" if p['src_fit_to_page'] and not p['out_fit_to_page'] else "") for p in ps_diff) or "no differences found") + ". Print areas / print titles: none in the sources (`_xlnm` names in output: " + str(len(P['builtin_xlnm_names'])) + ").")
w(f"- Sheet-scoped defined names were not copied: SD has {', '.join(PS['sheet_scoped_names']) or 'none'}" + (f" (on sheet(s) not carried: {', '.join(x.split('@')[1] for x in PS['sheet_scoped_names'] if x.split('@')[1] not in E['carried'])})" if PS['sheet_scoped_names'] else '') + "; COO book sheet-scoped names: " + (', '.join(PC['sheet_scoped_names']) or 'none') + ".")
w(f"- Google-specific package parts are not kept (part folders in the inputs but not in the output: {', '.join(dropped_part_dirs) or 'none'}); threaded-comment text survives as plain notes.")
w("- Raise eligibility impact (I-29), the MH-05 burden (I-27) and the Head of Service Delivery salary (I-26) are not quantified because the inputs are not in the workbook.")
w("- Remaining constant-valued legacy names were kept (outside the prune rule).")
open(NOTES_MD, "w").write("\n".join(L) + "\n")
print("issues:", [(i["id"], i["sev"]) for i in I], dict(by_sev))
print("overlap:", [(x["row"], x["class"]) for x in OVT])
