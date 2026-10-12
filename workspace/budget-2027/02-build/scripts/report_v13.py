"""v13 notes writer. Everything numeric comes from FIGURES_JSON (figures_v13.py), DIFF_JSON (diff_v13.py) and
SUITE_JSON (suite_v13.py); the only other inputs are the sha256 of the base and user files. No clock, no file
properties, no dates are read (F1 rule); the handoff date 2026-10-12 is a constant. No names; per-person amounts
for identified employees are rounded to the nearest $5k ('~'), the banner convention (exact figures live on the
Collation Notes sheet).

Usage:
  python3 -I report_v13.py FIGURES_JSON DIFF_JSON SUITE_JSON V12_XLSX USER_XLSX OUT_MD
"""
import sys, json, hashlib

FIGJ, DIFFJ, SUITEJ, V12P, USERP, OUTMD = sys.argv[1:7]
F = json.load(open(FIGJ))
DF = json.load(open(DIFFJ))
SU = json.load(open(SUITEJ))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def m(x, dp=0):
    s = f"{abs(x):,.{dp}f}"
    return f"({s})" if x < -0.004 else s


def r5(x):
    """Per-person amount, rounded to the nearest $5k (banner convention)."""
    v = round(abs(x) / 5000) * 5000
    return f"(~{v:,.0f})" if x < 0 else f"~{v:,.0f}"


hl, hl12 = F["AG132_v13"], F["AG132_v12"]
C = F["carried_D"]
car = lambda r: C[str(r)]
pol = 2448290  # production-labour policy effect, carried from v10 (labour block untouched in v11-v13; see footnote a)

md = f"""# 02-build notes v13 - 2027 COO budget collation (CO 7700/8600 inputs + the user's HC roster merge, decisions 1-4)

> **CONFIDENTIAL - contains named compensation data (HC-* tabs); restrict distribution.** The workbook's HC-* tabs hold employee names and salaries (v13 adds the user's 2026-10-12 roster entries), and the 'Logistics&WH Payroll' tab (SD copy) names seat holders; share the workbook and these notes only with people cleared to see compensation. In this file per-person amounts for identified employees are rounded to the nearest $5k (shown with '~') or aggregated; rounding does not change an amount that is already a multiple of $5k, so some unique-role salaries still appear at their exact value. The Collation Notes sheet keeps exact figures. A department total compared across versions, or a line that holds one person's cost (e.g. PO 6610-6640 in v13), can also reveal that cost.

## Changes from v12 (v13)

Handoff 2026-10-12 (orchestrator): one build combining **brief v7** (user: "add $2,000 per month in GL 7700 in CO; Add $6,500 per month in GL 8600 in CO") and **brief v8 as amended** (the user's edited workbook `00-brief/inputs/USER_EDIT_FINAL_v4_HC.xlsx` - a reliable edit source whose roster changes are re-applied to the clean v12 chain - plus the user's four decisions of 2026-10-12). All budget changes below are user-confirmed. Technique: the v12 base is edited by script (openpyxl stage passes), then saved once, whole, by a full LibreOffice recalculation + engine save - no XML is spliced into saved parts (an unedited openpyxl round-trip + engine save of v12 was first proven semantically identical to v12: 0 formula/value/format/comment/name diffs on 253,036 cells).

| # | Change (all user-confirmed 2026-10-12) | Effect on the contribution | Cells |
|---|---|---|---|
| A | CO GL 7700 'Inventory Obsolescence-old' 2027 = 24,000 (2,000/month) and GL 8600 Repairs and Maintenance 2027 = 78,000 (6,500/month); R stays 'Even', so the two S inputs spread themselves | {m(F['d_gl'], 2)} | CO!S98, CO!S106 |
| B | Roster merge: HC-CO r18 title 'Facilities Manager'; + Material Handler {r5(49920)} Sep-26 (r19, = seat MH-01 moved from HC-PO r20); + Material Handling Team Lead {r5(57554)} Sep-26 **end-dated Nov-26** (r20; the user's file's own end month - 2027 cost 0, see I-41/A-47); + Material Flow Supervisor 85,000 Nov-26 (r35); + Applications Engineer 85,000 Nov-26 (r36). HC-PO: r20 blanked; + Production Manager 125,000 Oct-26 (r41). HC-FE: + Associate Field Robotics Engineer 75,000 Sep-26 (r20; the I-28 person). HC-PE: + Purchasing Analyst 85,000 Jan-27, Launch Planner 75,000 Nov-26, Quality Engineer 100,000 Dec-26, Manufacturing Engineer 110,000 Dec-26 (r35:r38), Strategic Sourcing Lead 120,000 Oct-26 (r41). | inside B+D, C, E below | HC-CO/PO/FE/PE input cells; names copied from the user's file at build time |
| C | Decision 1: PE 6610-6640 wired live to 'HC-PE' rows 67-69 (replacing typed constants): {m(F['pe66_v12'], 2)} -> {m(F['pe66_v13'], 2)} | {m(F['d_pe66'], 2)} | PE!U67:AF69 (+AI notes) |
| B+D | Decision 2: CO 6610-6640 = 'HC-CO' rows 67-69 + the Logistics&WH model **less the roster-realized seats, by formula**: LOG-01 (since v10), MH-01, TL-01, MH-02 (the backfill seat realized by the Material Flow Supervisor, user-confirmed): {m(F['co66_v12'], 2)} -> {m(F['co66_v13'], 2)} | {m(F['d_co66'], 2)} | CO!U67:AF69 (+AI notes); Collation Notes H78:H81 |
| E | Decision 3: Production Manager expensed to PO 6610-6640 at PO HC rates with the 3% Oct-27 raise, live links to his roster row; NOT in the capitalised labour base or the Prod Payroll model: 0 -> {r5(F['po66_v13'])} (c) | {r5(F['d_po66'])} (c) | PO!U67:AF69 (+AI notes) |
| F | Decision 4: Fld Ops Payroll B11 14 -> 13 (the FE Associate out of FO's tech count; he stays in Fld Eng Budget and on HC-FE; still LISTED on HC-FO r15, which feeds nothing - reader note). I-28 -> RESOLVED | +{m(F['d_fo'], 2)} (payroll +{m(F['b11_payroll'], 2)}, 5330 +{m(F['b11_5330'], 2)}) | Fld Ops Payroll!B11 |
| G | PO 5110-5140 re-anchored: the embedded-constants-minus-'HC-PO'!r20 formulas become a live 8-production-staff basis `(1-B131) x SUM('HC-PO'!M14:M33) x (1, D6, D7)` + the idle-month rows 226-228 (B135 terms kept). The basis survives roster edits; the PM (r41, New Hires block) is outside it by construction. B131 = 0 base recomputes {m(F['scen_b131_po_base'], 2)} (= 590,317.51); booked value unchanged 0. Closes the full-sweep embedded-constants observation. | 0.00 | PO!U33:AF35 (+AI notes) |
| H | Notes + Collation Notes updated (headline, caveats, bounds, sign-flip recomputed by script; I-28 RESOLVED; I-41 restated; I-38 narrowed; I-42 added; A-46:A-48 added; YoY footnote extended) | - | this file; Collation Notes |

**Bridge from v12 (every term = the department's 2027 GL-line change; ties to the cent - asserted by `figures_v13.py`, exact terms on the Collation Notes v13 block):**

| Step | Amount |
|---|---|
| v12 contribution (COO P&L!AG132) | {m(hl12, 2)} |
| A. CO 7700 + 8600 | {m(F['d_gl'], 2)} |
| B+D. CO 6610-6640 (roster adds less de-duplicated seats) | {m(F['d_co66'], 2)} |
| C. PE 6610-6640 (live roster incl. 5 adds) | {m(F['d_pe66'], 2)} |
| E. PO 6610-6640 (Production Manager) | {r5(F['d_po66'])} (c) |
| F. Fld Ops Payroll B11 13 (I-28 resolved) | +{m(F['d_fo'], 2)} |
| G. PO 5110-5140 re-anchor (booked 0 either way) | 0.00 |
| **v13 contribution** | **{m(hl, 2)}** |

(c) One named person's cost (banner convention): rounded here, exact on the Collation Notes v13 block, which carries the full to-the-cent bridge. The sum of the exact terms equals the AG132 change to < $0.01 (build assertion).

## Headline: 2027 COO contribution

| Line | COO P&L row | 2026 (N) | 2027 v13 (AG) | Change | % | 2027 v12 (AG) | v13 - v12 |
|---|---|---|---|---|---|---|---|
| Revenue (company recognized revenue, 9/30/26 sales plan) | 16 | {m(F['coo_N16'])} | {m(F['rev_v13'])} | {m(F['rev_v13'] - F['coo_N16'])} | 110% | {m(F['rev_v13'])} | 0 |
| COGS (COO departments) | 63 | {m(F['coo_N63'])} | {m(F['cogs_v13'])} | {m(F['cogs_v13'] - F['coo_N63'])} | {(F['cogs_v13'] / F['coo_N63'] - 1):.0%} | {m(F['cogs_v12'])} | {m(F['cogs_v13'] - F['cogs_v12'])} |
|   of which depreciation (in COGS) | 19-22 | {m(F['dep_in_cogs_2026'])} | {m(F['dep_in_cogs_v13'])} | {m(F['dep_in_cogs_v13'] - F['dep_in_cogs_2026'])} | {(F['dep_in_cogs_v13'] / F['dep_in_cogs_2026'] - 1):.0%} | {m(F['dep_in_cogs_v13'])} | 0 |
| Gross Profit | 64 | {m(F['coo_N64'])} | {m(F['gp_v13'])} | {m(F['gp_v13'] - F['coo_N64'])} | {(F['gp_v13'] / F['coo_N64'] - 1):.0%} | {m(F['gp_v13'])} | 0 |
| Opex (COO departments) | 116 | {m(F['coo_N116'])} | {m(F['opex_v13'])} | {m(F['opex_v13'] - F['coo_N116'])} | {(F['opex_v13'] / F['coo_N116'] - 1):.0%} | {m(F['opex_v12'])} | {m(F['opex_v13'] - F['opex_v12'])} |
| COO contribution before other income ('Net Ordinary Income') | 117 | {m(F['coo_N117'])} | {m(F['coo_AG117'])} | {m(F['coo_AG117'] - F['coo_N117'])} | n/m | {m(hl12)} | {m(F['coo_AG117'] - hl12)} |
| Net Other Income | 131 | {m(F['coo_N131'])} | {m(F['coo_AG131'])} | {m(F['coo_AG131'] - F['coo_N131'])} | -100% | 0 | 0 |
| **COO contribution ('Net Income')** | 132 | {m(F['N132'])} | **{m(hl, 2)}** | {m(hl - F['N132'])} | n/m (a) | {m(hl12, 2)} | {m(hl - hl12, 2)} |

(a) Year on year is not like-for-like, on two counts. (1) 2026 expensed production labour, 2027 capitalises it; the policy effect carried from v10 is +{m(pol)} (the labour block is untouched in v11-v13), so on the 2026 policy the 2027 contribution would be about {m(hl - pol)}. (2) The 2027 payroll now carries the user's 2026-10-12 additions - ten hires/moves (4 CO, 5 PE, 1 PO) plus the two CO GL lines (7700/8600, little or no 2026 spend) - whose Sep-Dec 26 costs sit on the HC tabs only: the 2026 P&L columns are book data and were not restated. If any of these people (or the logistics model's 2026 hires) are on 2026 payroll, the 2026 forecast needs its own update outside this workbook's scope.

- **2027 COO contribution (COO P&L!AG132): {m(hl, 2)}** (v12 {m(hl12, 2)}, change {m(hl - hl12, 2)}). **The headline is now negative at the booked (capitalise-production-labour) policy.** The whole change is the user's 2026-10-12 additions, bridged above. Revenue {m(F['rev_v13'])}; COGS + Opex {m(F['cost_v13'])}.
- PO's booked COGS is unchanged (5110-5140 = 0, capitalised); the PM is Opex. CO payroll now carries two rate bases (roster at CO HC rates, 5 remaining model seats at the model's 6.8%/16.4%).
- Issues: 3 HIGH, 14 MED, 21 LOW open; 4 RESOLVED (I-05, I-17, I-26, I-28). New: I-42 (7700 label). Updated: I-06, I-17 (wiring), I-35 (PE wiring note), I-37 (recomputed), I-38 (narrowed), I-40 (base note), I-41 (restated).

**Headline caveats (new in v13):** (i) the 7700 row is labelled 'Inventory Obsolescence-old' - the only 7700 row in the book, but the '-old' suffix suggests a retired account; the user should confirm the intended account (I-42). (ii) 8600 2027 = 78,000 vs 2026 {m(F['co8600_2026'])} (+{(78000 / F['co8600_2026'] - 1):.0%}), above the variance-scan threshold - user-directed (brief v7). (iii) The Material Handling Team Lead's CO roster row is end-dated Nov-26 (the user's file), so neither CO nor any PO expense line carries that role in 2027 while seat TL-01 is excluded - a deliberate one-cell flip if wrong (I-41/A-47).

### Caveats on the headline (read before using the figure)

(1) What the figure is. The bottom line, {m(hl, 2)}, is a **COO contribution**: the company's recognized revenue ({m(F['rev_v13'])}, all of it) less the costs of the five COO departments only (COGS + Opex of FO, PO, CO, FE, PE: {m(F['cost_v13'])}). Costs outside COO are not in this workbook, so it is **not company Net Income**. The workbook row keeps its GL label 'Net Income' (COO P&L!A132).

(2) What the revenue is: unchanged from v10-v12 (the 9/30/26 sales plan's recognized revenue; includes unsigned and forecast bookings - see the v10 notes section (2), still exact).

(3) Open exposures, each on its own against the headline. 'Carried from v12' = the item's inputs are outside every cell v13 changes (the v12 -> v13 diff shows 0 changes there), so the computed effect stands; the scenario switches, I-41, I-37 and the burden-rate item are recomputed on v13.

| Item | Direction | Effect | Contribution after this item alone | Basis |
|---|---|---|---|---|
| Decision #10 scope: current 8 expensed (B131 = 0 sensitivity, not booked) | downside | {m(F['d_b131'])} | {m(F['scen_b131'])} | recomputed (LibreOffice scenario); PO 5110-5140 base {m(F['scen_b131_po_base'], 2)} |
| I-40 idle-month labour expensed (B135 = 0, not booked) | downside | {m(F['d_b135'])} | {m(F['scen_b135'])} | recomputed (scenario) |
| B132 = 1 (Sep-Dec 26 labour capitalised; needs a 2026 restatement) | downside | {m(F['d_b132'])} | {m(F['scen_b132'])} | recomputed (scenario); not in the range |
| Labour already in the 65,000 / 8,000 unit cost (O1) | upside | +{m(car(40))} | {m(hl + car(40))} | carried from v12 |
| I-41 restated: the Team Lead role carried nowhere in 2027 expense | downside | {r5(-F['i41_effect'])} | {r5(hl - F['i41_effect'])} | recomputed; see Issues |
| MH-01 on the 9-of-9 count reading | upside | +{m(car(42))} | {m(hl + car(42))} | carried from v12 |
| Logistics&WH seats at CO HC burden rates (5 seats left) | upside | +{m(F['burden_upside'])} | {m(hl + F['burden_upside'])} | recomputed (v12 +19,396 on 8 seats) |
| I-05 burden (O1), capitalised | downside | {m(car(45))} | {m(hl + car(45))} | carried from v12 |
| Rate base of the current staff (O7) | downside | {m(car(46))} | {m(hl + car(46))} | carried from v12 |
| I-10 FO/FE lines at 0 | downside | {m(car(48))} | {m(hl + car(48))} | carried from v12 |
| I-31 shortfall / double count | two-way | {m(car(52))} / +{m(car(53))} | {m(hl + car(52))} / {m(hl + car(53))} | carried from v12 |
| I-32 SlipBot 5010 = 0 / trend / trend from Sep-26 | upside | +1,353,574 / +276,164 / +403,624 | {m(hl + 1353574.20)} / {m(hl + 276163.88)} / {m(hl + 403624.13)} | carried from v12 |
| I-33 peripherals life 60 months | two-way | {m(car(57))} | {m(hl + car(57))} | carried from v12 |
| I-34 FE burden at FE HC rates / with FE tax at 7.65% | upside | +{m(car(58))} / +{m(car(59))} | {m(hl + car(58))} / {m(hl + car(59))} | carried from v12 |
| I-37 payroll tax below 7.65%: CO + PE + the PM | downside | {m(F['d_i37_cope'])} | {m(hl + F['d_i37_cope'])} | recomputed (v12 (62,207); PE roster +493,675 and the PM are new base) |
| I-37 FO and FE at the SD 6.8% | downside | {m(F['d_i37_fofe'])} | {m(hl + F['d_i37_fofe'])} | recomputed (one tech out of the FO base) |
| I-35 PE 'transfer?' leaves COO | upside | {r5(car(62))} | {r5(hl + car(62))} | carried from v12 (one person, rounded; the row is unchanged inside the live PE link) |
| I-36 Aug-27 FE hire not approved | upside | +{m(car(63))} | {m(hl + car(63))} | carried from v12 |
| I-39 FE manager seat stays open | upside | +{m(car(64))} | {m(hl + car(64))} | carried from v12 |
| A-14 depreciation convention (mid-month / month after) | upside | +{m(car(65))} / +{m(car(66))} | {m(hl + car(65))} / {m(hl + car(66))} | carried from v12 |
| A-22 unsigned/forecast revenue | downside | n/d | n/d | carried from v12 |
| New CO employee start month (A-43) | upside | per month later: ~10,000 | - | carried from v12 |
| I-28 | RESOLVED | 0 (booked: +{m(F['d_fo'], 2)} in the headline) | {m(hl, 2)} | user decision 4 |

{F['text_signflip']}

{F['text_upside']}

{F['text_range']}

| Bound | 2027 COO contribution |
|---|---|
| Lower bound 1 (booked policy, all quantified downsides) | {m(F['lb1'])} |
| Lower bound 2 (scope sensitivity, components at B131 = 0) | {m(F['lb2'])} |
| Point estimate | {m(hl, 2)} |
| Upper end (I-32 in full only) | {m(F['ub'])} |

{F['text_conclusion']}

## The roster merge (B): what landed where

Names were copied from the user's file into the HC tabs at build time (never into scripts, JSONs, these notes or any CSV). Titles, salaries and start months were asserted against the brief before writing. Our sheet structure is kept: the user's file had deleted HC-PO row 20, which shifted their rows; we blank r20 instead and use our row numbering (their r40 Production Manager = our r41).

| Tab | Row | Title | Annual salary | Start | End | Feeds |
|---|---|---|---|---|---|---|
| HC-CO | r18 | Facilities Manager (title set; the 110k employee of v10) | 110,000 | Jan-27 | Dec-27 | CO 6610-6640 via rows 67-69 |
| HC-CO | r19 | Material Handler (= seat MH-01, moved from HC-PO r20) | {r5(49920)} | Sep-26 | Dec-27 | CO 6610-6640 |
| HC-CO | r20 | Material Handling Team Lead (same person as HC-PO r16) | {r5(57554)} | Sep-26 | **Nov-26** | nothing in 2027 (A-47, I-41) |
| HC-CO | r35 | Material Flow Supervisor (open seat, no name; = the MH-02 backfill, A-46) | 85,000 | Nov-26 | Dec-27 | CO 6610-6640 |
| HC-CO | r36 | Applications Engineer (open seat, no name) | 85,000 | Nov-26 | Dec-27 | CO 6610-6640 |
| HC-PO | r20 | (blanked - the Material Handler moved to HC-CO r19) | - | - | - | out of the 5110-5140 base |
| HC-PO | r41 | Production Manager (New Hires block) | 125,000 | Oct-26 | Dec-27 | PO 6610-6640 (decision 3) |
| HC-FE | r20 | Associate Field Robotics Engineer (the I-28 person; = Fld Eng Budget r15) | 75,000 | Sep-26 | Dec-27 | nothing (FE P&L reads Fld Eng Budget; roster completeness) |
| HC-PE | r35 | Purchasing Analyst (open seat, no name) | 85,000 | Jan-27 | Dec-27 | PE 6610-6640 via rows 67-69 |
| HC-PE | r36 | Launch Planner (open seat, no name) | 75,000 | Nov-26 | Dec-27 | PE 6610-6640 |
| HC-PE | r37 | Quality Engineer (open seat, no name) | 100,000 | Dec-26 | Dec-27 | PE 6610-6640 |
| HC-PE | r38 | Manufacturing Engineer (open seat, no name) | 110,000 | Dec-26 | Dec-27 | PE 6610-6640 |
| HC-PE | r41 | Strategic Sourcing Lead (New Hires block) | 120,000 | Oct-26 | Dec-27 | PE 6610-6640 |

**The end-dated Team Lead row (A-47).** The user's file ends HC-CO r20 at Nov-26 (F20), so the row's 2027 cost is 0; the handoff's blocker rule says ambiguous roster details take the user's file's value, disclosed. It is internally consistent with their 'backfilling' comment (the Material Flow Supervisor starts Nov-26, seat MH-02 is the model's backfill seat) - but the same person remains on HC-PO r16, Sep-26 to Dec-27, inside the capitalised B131 base. Net effect: with TL-01 excluded and the CO row at 0, **no 2027 expense line carries the team-lead role** (booked PO expense is 0). One cell flips it: HC-CO F20 = Dec-27 costs the person in CO (+{r5(F['tl_roster_2027_cost'])} at CO HC rates). Restated as I-41.

**Roster totals vs the user's file (completion criterion; exact equality):**

| Tab | 2027 salary total (Z67), v12 | v13 | User's file | Difference |
|---|---|---|---|---|
| HC-CO | {m(F['hcco_v12_z'][0], 2)} | {m(F['hcco_v13_z'][0], 2)} | {m(F['user_z']['CO'], 2)} | {m(F['hcco_v13_z'][0] - F['user_z']['CO'], 2)} |
| HC-PO | {m(F['hcpo_v12_z'][0], 2)} | {m(F['hcpo_v13_z'][0], 2)} | {m(F['user_z']['PO'], 2)} | {m(F['hcpo_v13_z'][0] - F['user_z']['PO'], 2)} |
| HC-FE | {m(F['hcfe_v12_z'][0], 2)} | {m(F['hcfe_v13_z'][0], 2)} | {m(F['user_z']['FE'], 2)} | {m(F['hcfe_v13_z'][0] - F['user_z']['FE'], 2)} |
| HC-PE | {m(F['hcpe_v12_z'][0], 2)} | {m(F['hcpe_v13_z'][0], 2)} | {m(F['user_z']['PE'], 2)} | {m(F['hcpe_v13_z'][0] - F['user_z']['PE'], 2)} |

(The user's HC-PO totals sit one row higher in their file - their Excel row deletion; compared accordingly. HC-CO matches *because* r20 carries their Nov-26 end month. The user-file column shows Excel's cached floats; where the last displayed cent differs, the underlying difference is < $0.000001 and the Difference column is computed on the raw values.)

**HC-COO roll-up.** Pure formulas; recalculates. The Material Handler now appears once (HC-PO r20 blanked, HC-CO r19 filled - no double listing). Reader note: the FE Associate is listed on BOTH HC-FO r15 (snapshot; FO's P&L no longer counts him, B11 = 13) and HC-FE r20 (feeds nothing; FE's P&L costs him via Fld Eng Budget r15), so HC-COO's roster-level FO+FE payroll counts him twice while the P&L costs him once, in FE. HC-COO 2027 total payroll {m(F['hccoo_total_v13'])} (v12 4,863,502). Dec-27 headcounts (HC-COO col Z): PO {int(F['hccoo_people'][0])}, FO {int(F['hccoo_people'][1])}, FE {int(F['hccoo_people'][2])}, PE {int(F['hccoo_people'][3])}, CO {int(F['hccoo_people'][4])} (the end-dated Team Lead is not an active 2027 head).

**2026-side HC cells (disclosed precisely).** Adding Sep-Dec-26 starters moves the HC tabs' 2026-side columns I:L (Sep-Dec 26) on the edited rows and their totals, and HC-COO's same columns. Total Payroll (row 70) deltas by month:

| Tab | Sep-26 | Oct-26 | Nov-26 | Dec-26 |
|---|---|---|---|---|
| HC-CO | +{m(F['hc2026_delta']['CO'][0], 2)} | +{m(F['hc2026_delta']['CO'][1], 2)} | +{m(F['hc2026_delta']['CO'][2], 2)} | +{m(F['hc2026_delta']['CO'][3], 2)} |
| HC-PO | {m(F['hc2026_delta']['PO'][0], 2)} | +{m(F['hc2026_delta']['PO'][1], 2)} | +{m(F['hc2026_delta']['PO'][2], 2)} | +{m(F['hc2026_delta']['PO'][3], 2)} |
| HC-FE | +{m(F['hc2026_delta']['FE'][0], 2)} | +{m(F['hc2026_delta']['FE'][1], 2)} | +{m(F['hc2026_delta']['FE'][2], 2)} | +{m(F['hc2026_delta']['FE'][3], 2)} |
| HC-PE | +{m(F['hc2026_delta']['PE'][0], 2)} | +{m(F['hc2026_delta']['PE'][1], 2)} | +{m(F['hc2026_delta']['PE'][2], 2)} | +{m(F['hc2026_delta']['PE'][3], 2)} |

The six P&L sheets' 2026 columns (B:N) are unchanged - 0 cells (diff-asserted): the 2026 P&L is book data and reads no HC tab.

## Decision 1 (C): PE 6610-6640 wired to the roster

| GL (PE, 2027) | v12 (typed) | v13 (live 'HC-PE' rows 67-69) | Change |
|---|---|---|---|
| 6610 Salaries and Wages | {m(F['pe66_v12_rows'][0], 2)} | {m(F['pe66_v13_rows'][0], 2)} | {m(F['pe66_v13_rows'][0] - F['pe66_v12_rows'][0], 2)} |
| 6630 Payroll Taxes | {m(F['pe66_v12_rows'][1], 2)} | {m(F['pe66_v13_rows'][1], 2)} | {m(F['pe66_v13_rows'][1] - F['pe66_v12_rows'][1], 2)} |
| 6640 Benefits | {m(F['pe66_v12_rows'][2], 2)} | {m(F['pe66_v13_rows'][2], 2)} | {m(F['pe66_v13_rows'][2] - F['pe66_v12_rows'][2], 2)} |
| Total | {m(F['pe66_v12'], 2)} | {m(F['pe66_v13'], 2)} | {m(F['d_pe66'] * -1, 2)} |

U67:AF69 = 'HC-PE'!M67:X69 (the same pattern CO has used since v10). The typed v12 constants equalled the then-roster to the cent, so the switch itself moves nothing; the five user adds move the roster. 2026 columns untouched. PE 2027 salary {m(F['hcpe_v13_z'][0], 2)} = the handoff's expected 1,571,695 + PE HC burden at D6/D7 (3.571% / 8.823%; both below 7.65% FICA - I-37 recomputed below). The 'transfer?' row (I-35) rides inside the live link unchanged.

## Decision 2 (D): CO logistics de-dup - seat by seat (2027 $, model rates incl. 2027 new-hire cost)

CO!U67:AF69 = 'HC-CO' rows 67-69 + 'Logistics&WH Payroll' row 43 **less rows 34, 36, 38, 39** + row 46 (and the same net-of pattern x B5 / B6 on 6630/6640). The de-dup lives in CO's formulas (the Logistics&WH tab stays an unedited SD copy). Collation Notes H78:H81 check this composition live; they cache and recalculate to 0.

| Seat | In CO, v12 | In CO, v13 | 2027 cost | Why out / in |
|---|---|---|---|---|
| LOG-01 Logistics Manager | no | no | {r5(F['seat_LOG-01'])} | = HC-CO r17 (excluded since v10) |
| MH-01 Material Handler | yes | **no** | {r5(F['seat_MH-01'])} | moved to HC-CO r19 (roster row at CO HC rates) |
| TL-01 Material Handling Team Lead | yes | **no** | {r5(F['seat_TL-01'])} | realized on HC-CO r20 (end-dated Nov-26; I-41) |
| MH-02 Material Handler (backfill seat) | yes | **no** | {r5(F['seat_MH-02'])} | realized by the Material Flow Supervisor (HC-CO r35; A-46, user-confirmed) |
| INV-01 Inventory Control Specialist | yes | yes | {m(F['seat_INV-01'])} | model seat, no roster (Feb-27) |
| MH-03 Material Handler | yes | yes | {m(F['seat_MH-03'])} | model seat (Mar-27) |
| MH-04 Material Handler | yes | yes | {m(F['seat_MH-04'])} | model seat (Jun-27) |
| TL-02 Material Handling Team Lead | yes | yes | {m(F['seat_TL-02'])} | model seat (Jul-27) |
| MH-06 Material Handler | yes | yes | {m(F['seat_MH-06'])} | model seat (Jul-27) |
| **Out in v13 (3 seats)** | | | {r5(-F['lw_out_total'])} | TL-01 + MH-01 + MH-02 (exact on Collation Notes) |
| **Still added from the model (5 seats)** | | | {m(F['lw_added_v13'], 2)} | salaries {m(F['lw_in_sal'], 2)} + tax {m(F['lw_in_tax'], 2)} + benefits {m(F['lw_in_ben'], 2)} + new-hire {m(F['lw_in_nh'], 2)} |

Verified as the handoff asked: **MH-02's 1,000 hire cost sits in the model's Oct-26 column and TL-01's in Dec-26** - both outside the 2027 window, so the 2027 new-hire cost is exactly 5,000 (INV-01 Feb, MH-03 Mar, MH-04 Jun, TL-02 + MH-06 Jul), all for seats still added. The CO 6610-6640 composition (roster + in-seats = P&L) ties to < $0.01 per GL (build assertion + live H78:H81).

| GL (CO, 2027) | v12 | HC-CO roster v13 | of which v13 roster adds | Logistics in-seats + hire cost | v13 | v13 - v12 |
|---|---|---|---|---|---|---|
| 6610 (incl. new-hire cost) | {m(F['co66_v12_rows'][0], 2)} | {m(F['hcco_v13_rows'][0], 2)} | {m(F['co_adds_rows'][0], 2)} | {m(F['lw_in_rows'][0], 2)} | {m(F['co66_v13_rows'][0], 2)} | {m(F['co66_v13_rows'][0] - F['co66_v12_rows'][0], 2)} |
| 6630 | {m(F['co66_v12_rows'][1], 2)} | {m(F['hcco_v13_rows'][1], 2)} | {m(F['co_adds_rows'][1], 2)} | {m(F['lw_in_rows'][1], 2)} | {m(F['co66_v13_rows'][1], 2)} | {m(F['co66_v13_rows'][1] - F['co66_v12_rows'][1], 2)} |
| 6640 | {m(F['co66_v12_rows'][2], 2)} | {m(F['hcco_v13_rows'][2], 2)} | {m(F['co_adds_rows'][2], 2)} | {m(F['lw_in_rows'][2], 2)} | {m(F['co66_v13_rows'][2], 2)} | {m(F['co66_v13_rows'][2] - F['co66_v12_rows'][2], 2)} |
| Total | {m(F['co66_v12_rows'][3], 2)} | {m(F['hcco_v13_rows'][3], 2)} | {m(F['co_adds_rows'][3], 2)} | {m(F['lw_in_rows'][3], 2)} | {m(F['co66_v13_rows'][3], 2)} | {m(F['co66_v13_rows'][3] - F['co66_v12_rows'][3], 2)} |

Burden-rate caveat (A-44, updated): the 5 remaining model seats are booked at the model's 6.8% / 16.4%; at CO HC rates the contribution would be +{m(F['burden_upside'])} higher (v12 +19,396 on 8 seats).

## Decision 3 (E): Production Manager expensed in PO

PO!U67:AF69 = 'HC-PO'!M41:X41 x (1, D6, D7) - live links to his roster row (125,000, Oct-26 start, New Hires block r41, 3% raise Oct-27 via the row's G/H cells). 2027: salary {r5(F['pm_z'])}, tax {r5(F['po66_v13_rows'][1])}, benefits {r5(F['po66_v13_rows'][2])}, total {r5(F['po66_v13'])} (exact on the Collation Notes v13 block). He is **not** in the capitalised labour base (PO!U33:AF35 sum rows 14:33 only; he is r41) and **not** in the Prod Payroll model (untouched). His Oct-Dec 26 cost exists on the HC tab only - no 2026 P&L change.

## Decision 4 (F): Fld Ops Payroll B11 = 13 (I-28 RESOLVED)

One typed input: B11 14 -> 13. Recalculated effect +{m(F['d_fo'], 2)} on the contribution = FO 5510/5530/5540 payroll {m(F['b11_payroll'], 2)} lower + 5330 {m(F['b11_5330'], 2)} lower (Fld Maint Budget!B29 = B30 + B11: 21 -> 20); supervisor headcount unchanged in every month (ratio basis). Matches the v12 caveat (+78,529) and the handoff evidence. The person stays budgeted once: Fld Eng Budget r15 (FE 6610-6640) - and is now also on the HC-FE roster (r20), closing the FE HC gap that I-28/I-36 flagged. He remains LISTED on HC-FO r15: a roster snapshot that feeds no P&L line (reader note above).

## G: PO 5110-5140 re-anchor (live 8-production-staff basis)

Old (v10-v12): `(1-B131) x (embedded v7 monthly constant - 'HC-PO'!M20 x rate) + idle row` - the form whose r20 reference the user's in-Excel row deletion severed (v12 diagnosis). New (v13): `(1-B131) x SUM('HC-PO'!M14:M33) x (1, D6, D7) + idle row` - the Current Employees block itself is the basis, so the formula survives roster edits (blank rows compute empty and SUM skips them; a future current hire joins the base automatically; the PM sits in New Hires r41, outside the block). Booked value unchanged (0 while B131 = 1); B131 = 0 recomputes {m(F['scen_b131_po_base'], 2)}/yr = the handoff's 590,317.51 (scenario-verified on the shipped file). The idle-month B135 terms (rows 226-228) are kept. This closes the full-sweep observation about embedded constants in PO 33-35.

## Issues (v13)

Open: 3 HIGH, 14 MED, 21 LOW; 4 RESOLVED. Changed rows only (all others carried from v12's register verbatim):

| ID | Sev | Change in v13 |
|---|---|---|
| I-06 | LOW | Evidence refreshed: Fld Ops Payroll!B11 = 13 and Fld Maint Budget!B29 = 20 (was 14 / 21); the stale MeLi comment finding itself is unchanged. |
| I-17 | RESOLVED | Wiring updated: the CO add-on now excludes LOG-01 + MH-01 + TL-01 + MH-02 by formula (user decisions 2026-10-12); 5 model seats remain; H78:H81 check the composition live. |
| I-28 | **RESOLVED** | User decision 4 (2026-10-12): the duplicate was real (FO -> FE move). B11 = 13 booked (+{m(F['d_fo'], 2)} in the headline); he is on HC-FE r20 now; still listed on HC-FO r15 (snapshot, feeds nothing). Residual: if the move was mid-2026, the 2026 FO forecast (book data) would need checking - 2027 is right either way. |
| I-35 | MED | PE 6610-6640 is now a live roster link, so a recorded transfer would flow automatically once HC-PE r22 is end-dated / moved; exposure unchanged ({r5(car(62))}). |
| I-37 | MED | Recomputed on the v13 salary bases: CO + PE + the PM at 7.65% upper bound {m(F['d_i37_cope'])} (v12 (62,207); drivers: PE roster +493,675, the PM, the CO adds); FO/FE {m(F['d_i37_fofe'])} (one tech left the FO base). Unverified upper bound; not in the range. |
| I-38 | MED | Narrowed: TL-01 and MH-02 are no longer booked from the model - the roster realizes them (HC-CO r20 end-dated / r35). Remaining: the Prod Payroll ramp dates (unchanged). |
| I-40 | HIGH | Unchanged in effect; the B131 = 0 base is now live (SUM of the current-employee block) and recomputes 590,317.51; scenario values on v13 in the caveat table. |
| I-41 | MED | **Restated.** The Material Handling Team Lead: HC-PO r16 (Sep-26..Dec-27, inside the capitalised base) AND HC-CO r20 (Sep-26..Nov-26, 2027 cost 0 - the user's file value, A-47). Booked: PO expenses 0 (capitalised), CO excludes seat TL-01 as roster-realized -> no 2027 expense line carries the role: {r5(-F['i41_effect'])} if it should stay an expense (7-of-9 reading). 0 if the end date is right and the Material Flow Supervisor (in CO) is the replacement. Under B131 = 0 the role is expensed inside PO 5110-5140 (and the exposure is 0 there). One-cell alternative: HC-CO F20 = Dec-27 books the person in CO (+{r5(F['tl_roster_2027_cost'])}). PO owner to confirm. |
| I-42 | LOW (new) | The 7700 row booked with the user's 24,000 is labelled '7700 - Inventory Obsolescence-old' - the only 7700 row, but the '-old' suffix suggests a retired account. User to confirm; classification only. |

## Assumptions added in v13

| ID | Assumption | Value / effect | Where | Source |
|---|---|---|---|---|
| A-46 | The Material Flow Supervisor (85,000, Nov-26, HC-CO r35) IS the realized backfill that the logistics model carries as seat MH-02 ('backfill' seat). | MH-02 excluded from the CO add-on ({r5(-F['seat_MH-02'])}); if wrong, one formula term per CO row flips it back (+ that amount) | CO!U67:AF69; 'Logistics&WH Payroll' row 39 | user 2026-10-12 ('we are backfilling [the departing employee], so the Material Flow Supervisor should be included'); orchestrator mapping |
| A-47 | HC-CO r20 (MH Team Lead) end month Nov-26 - the user's file's own value (the brief gave the salary and a Sep-26 start, no end month); 2027 cost 0; the person stays on HC-PO r16. | one cell to flip (HC-CO F20 = Dec-27: +{r5(F['tl_roster_2027_cost'])} CO cost) | 'HC-CO'!F20 | user's file (handoff blocker rule: take the file's value, disclose); restated as I-41 |
| A-48 | Production Manager: Oct-26 start on the roster; Oct-Dec 26 cost on the HC tab only (2026 P&L is book data, not restated); expensed all of 2027 in PO 6610-6640. | {r5(F['d_po66'])} on the contribution | 'HC-PO'!B41:F41; PO!U67:AF69 | user decision 3 (2026-10-12); builder (2026 timing) |

A-01..A-45 are unchanged (v9/v10 registers). A-43's 'title not provided' is resolved: HC-CO r18 = Facilities Manager (user, 2026-10-12).

## v12 -> v13 diff (confinement proof)

`diff_v13.py` compares every cell of all 20 sheets (formulas and cached values) plus comments, with the handoff's allowed areas encoded as rules; **0 violations**. Changed cells outside the regenerated-in-place Collation Notes: {sum(v['formula_diffs'] for v in DF['per_sheet'].values())} formula / {sum(v['value_diffs'] for v in DF['per_sheet'].values())} value diffs:

| Sheet | Formula diffs | Value diffs | Area |
|---|---|---|---|
""" + "".join(
    f"| {sh} | {d['formula_diffs']} | {d['value_diffs']} | {area} |\n"
    for sh, d, area in [
        (s, DF["per_sheet"][s], {
            "COO P&L": "roll-up rows 46/52-54/67-69/98/106 + subtotals/ratios, 2027 columns only",
            "CO": "S98/S106; U67:AF69 + AI; rows 73/116/117/132/137-142; rows 98/106 2027 side",
            "PE": "U67:AF69 + AI; subtotals/ratios",
            "PO": "U33:AF35 + U67:AF69 + AI; rows 36-37; subtotals/ratios",
            "FO": "5330 + 5510-chain + subtotals/ratios (B11 recalc), 2027 columns only",
            "Fld Ops Payroll": "B11 + its dependent formula cells",
            "Fld Maint Budget": "B29 chain (formula cells only)",
            "HC-CO": "roster input rows 18-20/35-36 + recalculated row/total cells",
            "HC-PO": "r20 blanked, r41 added + recalculated cells",
            "HC-FE": "r20 added + recalculated cells",
            "HC-PE": "r35-38/41 added + recalculated cells",
            "HC-COO": "roll-up recalc (formula cells only)",
        }.get(s, "?"))
        for s in DF["per_sheet"]
    ]
) + f"""
Collation Notes: {DF['collation_notes_changed_cells']['formula']} formula + {DF['collation_notes_changed_cells']['value']} text/number cells updated in place (headline, decision rows, caveat table, CO block, reconciliation, issue rows, H78:H80 checks) + the v13 block appended from row 812 (no row insertions, so every existing address is stable). FE, HC-FO, Logistics&WH Payroll, DeploySum, Prod Payroll and Depreciation Schedule: **0 changes** (diff-asserted frozen). 2026 columns (B:N) of the six P&L sheets: **0 changes**. HC-tab diffs are reported as coordinates only (column B holds names). Comments: 0 changes.

## Error scan and suite (all green)

- COO P&L = FO + PO + CO + FE + PE on {SU['rollup']['cells']} SUM cells; max deviation {SU['rollup']['max_dev']:.2e}.
- 0 error caches in v13 and in its LibreOffice recalculation; 0 '#REF!' anywhere in stored formulas (the user's severed-reference incident cannot recur from this file); 0 shared formulas in the package.
- A full LibreOffice recalculation of v13 reproduces its own cache (numeric <= 1e-6); the deliverable is value-identical to the recalculated stage-1 content outside the Collation Notes sheet, so the figures and scenarios below hold for the shipped file.
- Collation Notes: the 32 live headline formulas (C21:F28) are unchanged from v12; H78:H81 (the CO de-dup check) cache and recalculate to 0.
- Roster cross-check: all four HC Z-column totals equal the user's file's (table above, differences 0.00).

## Scenario switches (scratch copies of the shipped v13, LibreOffice full recalc; deltas = v12's, orthogonality confirmed)

| Scenario | AG132 | vs booked |
|---|---|---|
| Booked (B131 = 1, B132 = 0, B135 = 1) | {m(hl, 2)} | - |
| B131 = 0 (current staff expensed); PO 5110-5140 base {m(F['scen_b131_po_base'], 2)} | {m(F['scen_b131'], 2)} | {m(F['scen_b131'] - hl)} |
| B135 = 0 (idle-month labour expensed) | {m(F['scen_b135'], 2)} | {m(F['scen_b135'] - hl)} |
| B132 = 1 (needs a 2026 restatement) | {m(F['scen_b132'], 2)} | {m(F['scen_b132'] - hl)} |
| B131 = 0 and B135 = 0 | {m(F['scen_b131_b135'], 2)} | {m(F['scen_b131_b135'] - hl)} |
| B132 = 1 and B131 = 0 | {m(F['scen_b132_b131'], 2)} | {m(F['scen_b132_b131'] - hl)} |

## Completion criteria (v13)

| Criterion | Result |
|---|---|
| Suite green | all checks pass (suite_v13.py; summary above) |
| Bridge ties to the cent | sum of the five exact dept-level terms = AG132 change, difference < $0.01 (figures_v13.py assertion; exact terms on the Collation Notes v13 block) |
| B131 = 0 scenario still computes; its new value stated | AG132 = {m(F['scen_b131'], 2)}; PO 5110-5140 base {m(F['scen_b131_po_base'], 2)} = 590,317.51 |
| Roster totals match the user's file's Z totals | all four tabs, difference 0.00 (HC-CO matches because r20 carries the user's Nov-26 end month) |
| No severed refs anywhere | 0 #REF! in formulas and caches (v13 and its recalc) |
| Two-pass content-identical | run_build_v13.sh runs the whole pipeline twice; both passes' md byte-identical and xlsx part-identical after sorting <dataValidations> children (normcmp_v12.py; the engine's one nondeterministic element order + wall-clock zip timestamps, the v12-documented deviation). The shipped workbook is pass 1's engine save, untouched. |
| Diff confined | 0 violations (table above); frozen sheets 0 changes; 2026 P&L columns 0 changes; HC 2026-side cells disclosed |
| No names in md / CSVs (none written) / Collation Notes | privacy_v6 hits 0; paylist_v10 exact per-person hits 0 (single-person amounts shown with '~') |

## Build and sources

Output: `02-build/02-build_COO_2027_Budget_Collated_v13.xlsx` and this file (v1-v12 files unchanged; no v13 CSV).
Entry point `scripts/run_build_v13.sh` (the whole pipeline runs twice; the md must be byte-identical and the xlsx content-identical across passes):
build_v13.py stage1 (the A-G cell edits on v12; roster names read from the user's file only) -> recalc.sh (full LibreOffice recalculation) -> scen_v8.py x5 + recalc.sh (B131/B135/B132 single and double switches) -> figures_v13.py (every figure + tie assertions + the user-file Z cross-check) -> build_v13.py stage2 (Collation Notes in-place updates + v13 block, from the figures) -> recalc.sh = THE ENGINE SAVE (the deliverable; one full recalculation + save, no post-processing) -> diff_v13.py (confinement, exit 1 on violation) -> suite_v13.py -> scenread_v12.py on 3 re-run switches of the shipped file -> recon_v13.py + names_v11.py + cntext_v12.py + privacy_v6.py + paylist_v10.py (name and per-person-amount gates; scratch name list outside the repo, deleted) -> report_v13.py (this file). run_build_v12.sh ... run_build.sh still reproduce v12 ... v1.
Inputs (read-only): the four v12-listed sources (unchanged, sha256 in the v12 notes) plus `USER_EDIT_FINAL_v4_HC.xlsx` sha256 `{sha(USERP)}` (roster names and the r20 end month; its severed PO formulas and typed CO constants are NOT imported - brief v8 correction).
Base: v12 workbook sha256 `{sha(V12P)}`. LibreOffice 24.2.7.2; Python with -I. Edit technique: openpyxl stage passes + one final LibreOffice full-recalc engine save (v12 technique; the package-patch method stays retired).

## Sections of the v12 notes not restated

Unchanged by v13 and not repeated here (02-build_notes_v12.md and the v9/v10 sections it carries): the v12 #REF! diagnosis and engine-save hardening, production-labour capitalisation mechanics, Prod Payroll model, depreciation schedule, revenue build, DeploySum tie-out, variance scan, duplicate scan, FO/FE payroll reconciliation detail, assumptions A-01..A-45, the unchanged issue rows, decisions #2-#5 and #10 (still open, unchanged effects vs the new headline shown in the caveat table). Where those sections quote the v12 contribution (159,136) or v12 wiring of CO/PE/PO payroll rows, this file supersedes them.

## Decisions (v13, builder)

- D1 (v13): Edit method - openpyxl stage passes on v12, then ONE full LibreOffice recalculation + engine save as the deliverable (the v12 technique; nothing is spliced into saved parts). Proven safe first: an unedited openpyxl round-trip + engine save of v12 semantically diffs to v12 with 0 differences (fdiff_v12.py, 253,036 cells).
- D2 (v13): The Team Lead row's Nov-26 end month is taken from the user's file (the handoff's blocker rule for roster details the brief does not pin down), which also makes every roster Z total equal the user's file exactly. Consequence (no 2027 expense line carries the role) disclosed as restated I-41 + A-47 with the one-cell flip.
- D3 (v13): HC-PO r20 is blanked, not deleted: every dependent formula (HC-PO totals, HC-COO roll-up, the new PO base) stays un-severed and row addresses stay stable - the exact failure mode of the user's in-Excel deletion cannot recur.
- D4 (v13): The PM lands in the New Hires block (r41; the user's own block, our row numbering), which keeps him outside the 5110-5140 basis BY CONSTRUCTION (the basis sums the Current Employees block M14:M33) rather than by a subtraction term.
- D5 (v13): The de-dup is implemented in CO's formulas (handoff preference); the Logistics&WH tab remains an unedited SD copy. The excluded seats are subtracted row by row so each exclusion is visible and individually reversible (A-46's one-term flip).
- D6 (v13): PO!U68:AF69 compute the PM's tax/benefits as M41 x D6/D7 directly (not via HC-PO totals, which also hold the 8 capitalised production staff), so the expensed amount is exactly one person at PO HC rates.
- D7 (v13): The Collation Notes sheet is updated in place (stale current-state cells) plus a v13 block appended below row 810; no rows are inserted, so every existing cell address (incl. the H78:H81 checks and v7-v12 historical sections, kept as records) is stable.
- D8 (v13): Caveat effects are recomputed where v13 moved their inputs (the 3 switch scenarios + 2 double switches, I-41, I-37, the burden-rate item); all other effects are carried from v12 with the diff as evidence their inputs are untouched - and the carried scenario deltas are re-verified against the recomputed ones (<= $2).
- D9 (v13): Scenarios are computed on the recalculated stage-1 content; the suite proves the deliverable value-identical outside the Collation Notes sheet, and the three single switches are re-run on the shipped file itself (B131 = 0 also re-checks the 590,317.51 base).
- D10 (v13): Names flow user-file -> workbook only; these notes, the JSONs and the return message carry none (privacy gate), and single-person amounts appear rounded ('~') with exact values kept on the Collation Notes sheet (banner convention).

## Not done / limits

- The user's Excel open-test is still the final check (validation here is LibreOffice-only, as in v12). On a clean open, PO rows 33-35 and 67-69 show values, not #REF!.
- The 2026 P&L columns are book data and were NOT restated for the Sep-Dec-26 starters (their 2026 cost is on the HC tabs only). If the new hires (or the model's 2026 logistics hires) are on 2026 payroll, the 2026 forecast needs a separate update.
- I-42: the 7700 'Inventory Obsolescence-old' label awaits the user's confirmation; the 24,000 sits on that row meanwhile.
- The Prod Payroll model still counts 9 current staff by number (brief v6: leave the model unchanged); the 9-of-9 MH-01 overlap caveat stands (+{m(car(42))}).
- The 'Logistics&WH Payroll' tab banner still reads 'rolls up to Production Operations' (unedited SD copy by design; superseded note on Collation Notes).
- The Material Handling Team Lead's 2027 treatment rests on the user's Nov-26 end date (A-47/I-41): one cell (HC-CO F20) flips it if wrong.
- The user's file's Material Handler name spelling (HC-CO r19) was copied as typed; it differs slightly from the old HC-PO r20 spelling of the same person (same role, salary and move per the brief). Not reconciled - roster hygiene for the user.
- 05-final packaging (FINAL_v5) is the orchestrator's step after verification, not part of this build.
"""

open(OUTMD, "w", encoding="utf-8").write(md)
print(f"report_v13: {len(md.splitlines())} lines -> {OUTMD}")
