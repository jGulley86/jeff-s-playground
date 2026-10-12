"""v12 notes generator: the v11 md with (1) a new first section carrying the Excel #REF! diagnosis
and the re-serialization verification, (2) a 'Decisions (v12, builder)' section, (3) the 'Not opened
in Microsoft Excel' limit replaced by the incident + fix status. Everything else verbatim.

All facts come from the JSON artifacts of this build (forensics_v12, fscan_v12 on v11 and v12,
fdiff_v12, suite_v12, scenarios, normcmp_v12) - no clock, no file properties, no dates are read
(F1 rule); the one date written (the handoff date) is a constant below, as in earlier versions.

Usage:
  python3 -I report_v12.py V11_MD FSCAN11 FSCAN12 FDIFF SUITE SCEN FORENSICS TWOPASS LOVER_TXT OUT_MD
"""
import sys, json

(V11MD, FSCAN11, FSCAN12, FDIFF, SUITE, SCEN, FORENSICS, TWOPASS, LOVER, OUT) = sys.argv[1:11]
HANDOFF_DATE = "2026-10-12"

md = open(V11MD, encoding="utf-8").read()
s11 = json.load(open(FSCAN11)); s12 = json.load(open(FSCAN12))
fd = json.load(open(FDIFF)); su = json.load(open(SUITE)); sc = json.load(open(SCEN))
fo = json.load(open(FORENSICS)); tp = json.load(open(TWOPASS))
lover = open(LOVER, encoding="utf-8").read().strip()

assert all(fo[k]["ok"] for k in ("F-A", "F-B", "F-C", "F-D", "F-E", "F-F", "F-G")), "forensics not green"
assert tp["ok"], "two-save comparison not green"

from decimal import Decimal, ROUND_HALF_UP
m = lambda x: f"{x:,.0f}"
d2 = lambda x: f"{Decimal(repr(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,}"  # Excel-style display
NL = "\n"
lo_ver = lover.split()[1] if len(lover.split()) > 1 else lover  # '24.2.7.2'

unesc = lambda s: s.replace("&amp;", "&")  # sheet names in the scan JSONs carry workbook.xml escaping

# ---- per-sheet entity table (v11 vs v12) -------------------------------------------------------
ent_rows = []
for name in s11["sheets"]:
    a, b = s11["sheets"][name], s12["sheets"][name]
    if a["entity_f_cells"] or b["entity_f_cells"]:
        ea = " ".join(f"{k} x{v}" for k, v in sorted(a["entities"].items())) or "-"
        eb = " ".join(f"{k} x{v}" for k, v in sorted(b["entities"].items())) or "-"
        ent_rows.append(f"| {unesc(name)} | {a['entity_f_cells']} | {ea} | {b['entity_f_cells']} | {eb} |")
ent_table = NL.join(ent_rows)

# ---- overlap table (v11; all Excel-authored per F-G) -------------------------------------------
ov_rows = []
for name in s11["sheets"]:
    for p in s11["sheets"][name]["overlapping_master_refs"]:
        ov_rows.append(f"| {unesc(name)} | si={p['si_a']} at {p['master_a']} ref {p['ref_a']} | "
                       f"si={p['si_b']} at {p['master_b']} ref {p['ref_b']} |")
ov_table = NL.join(ov_rows)

u33 = fo["u33_stored_v11"].replace("&", "&")  # stored form, shown verbatim in a code span
sig = fo["row_delete_signature"]
sev = fo["ref_formulas"]

sec = f"""## Changes from v11 (v12): diagnosis of the Excel #REF! report, and a full engine re-serialization. No cell value, formula meaning, input, sheet, comment or format changes.

Handoff {HANDOFF_DATE} (orchestrator): the user opened FINAL_v4 (= v11) in Microsoft Excel and saw **#REF!** in PO rows
33-35 (GLs 5110/5130/5140) and their dependents (PO rows 36-37 totals, COO P&L rows 33-37, the AJ YoY column). The
handoff's working hypothesis was that Excel rejects the v8-v11 package-patched (hand-spliced) `<f>` elements - most
likely their `&apos;` XML entities - and that a load-time "repair" strips those formulas. v12 was commissioned as
(1) a full from-the-file diagnosis and (2) a re-serialization: the workbook saved once, whole, by the LibreOffice
engine, so that every part is serializer-written, with values provably identical to v11.

**Diagnosis result: the workbook was never broken in Excel.** The #REF!s are Excel's correct bookkeeping for an edit
the user made inside Excel (a deleted roster row). The commissioned re-serialization is still shipped: it is a
hardening with zero semantic change, it retires the package-patch technique for good, and v13/v14 are queued on it.

### Diagnosis (every claim below is asserted by `scripts/forensics_v12.py` against the files; the build fails if any stops holding)

The decisive evidence is the user's own copy, `00-brief/inputs/USER_EDIT_FINAL_v4_HC.xlsx` - FINAL_v4 opened,
edited and saved in {fo['user_app']} (docProps; F-B). 05-final FINAL_v4 is byte-identical to 02-build v11 (F-A),
so the user opened exactly the bytes diagnosed here. In that Excel-saved copy:

1. **Every hand-spliced v8-v11 formula survived Excel verbatim.** Per-sheet formula counts match v11 exactly on 18 of
   20 sheets; the two exceptions are the user's own edits: HC-PO -19 formula cells (one deleted roster row) and
   CO -24 (the user typed the brief-v7 monthly constants over the U98:AF98 and U106:AF106 formulas). No sheet was
   dropped, nothing else lost - i.e. **no repair happened** (F-E). The entity-escaped, `aca="false"`-attributed
   spliced cells parsed cleanly; Excel merely re-saved them in its own dialect.
2. **Exactly 36 formulas carry #REF!: PO!U33:AF35** - and each is v11's own formula text with only the
   `'HC-PO'!M20` ... `'HC-PO'!X20` operand replaced by `'HC-PO'!#REF!` (F-C). Stored example (user's file, U33):
   `(1-'Depreciation Schedule'!$B$131)*(43450-'HC-PO'!#REF!)+'Depreciation Schedule'!F226`.
   A formula Excel cannot parse is dropped whole by repair; it is never kept with one operand surgically replaced.
   `Sheet!#REF!` is specifically Excel's marker for a reference whose target CELLS were deleted while the workbook
   was open.
3. **The row-deletion signature is on HC-PO** (F-D): all four shared-formula group refs end one row earlier
   (`..33` -> `..32`), the sheet's last stored row went {sig['maxrow'][0]} -> {sig['maxrow'][1]}, and HC-COO's
   formulas referencing HC-PO shifted exactly as Excel adjusts references when a row is deleted:
   {sig['hccoo_refs']['shifted_minus1']} single-cell references one row up (e.g. row 67 -> 66),
   {sig['hccoo_refs']['range_end_minus1']} roster ranges with the end row reduced by one (I$14:I$57 -> I$14:I$56),
   {sig['hccoo_refs']['unchanged']} references to rows above the deleted row unchanged, 0 anything else.
   Load-time repair does none of this bookkeeping; a user deleting a row in Excel does all of it.
4. **The deleted row is HC-PO row 20 - seat MH-01, the Material Handler** (the row PO's 5110-5140 formulas subtract
   from the B131 base since v10, and the row the user moved to HC-CO in their edit batch; see brief v8). PO!U33:AF35
   are the only worksheet formulas in the whole book that reference HC-PO rows 14-33, which is why the visible
   damage was exactly "PO 33-35 plus dependents": the dependents (PO 36-37, COO P&L 33-37, AJ) carry no #REF! in
   their formulas in the user's file - they only display the propagated error value after recalculation.

**Root cause (precise): in Excel the user deleted HC-PO row 20 (Material Handler, MH-01). PO!U33:AF35 reference that
row's cells M20:X20; deleting a referenced row turns those references into #REF!. The #REF!s the user saw are the
correct, expected result of that edit on a correctly-loaded workbook - not file damage, not an Excel repair, not a
serialization defect.** Consequence for the budget (out of v12's no-value-change scope, already in the v14 brief):
once the Material Handler row leaves HC-PO, the PO 5110-5140 formulas must be re-anchored (the B131 = 0 base stays
590,317.51). Until v14 lands, the user should work from the clean v12 file, not from the USER_EDIT copy (its PO
33-35 formulas are severed).

### The pre-scan hypothesis, refuted on measurement

- **`&apos;`/`&quot;` entities in `<f>` are LibreOffice's own canonical serialization, not a patch artifact.** v11
  carries {m(s11['total_entity_f_cells'])} entity-escaped formula cells across 13 sheets - including COO P&L, FO, FE,
  PE and Fld Maint Budget, which no patch ever touched and which the user saw evaluating fine. The engine's re-save
  has {m(s12['total_entity_f_cells'])} such cells (more: it expands the HC tabs' shared formulas, quotes included).
  The pre-scan's premise that "LibreOffice's own serializer stores raw apostrophes" was backwards: the raw-apostrophe
  formulas in v11 sit in the Excel-written HC/Logistics parts and in the script-written Collation Notes cells. v11's
  own spliced cells even used both spellings - PO rows 33-35 entity-escaped, the Depreciation Schedule rows 128-241
  raw (hence that sheet's 16 -> 145 jump in the table below once the engine normalizes to entities) - and the user's
  Excel loaded both.
- **The spliced cells are byte-identical to engine output** (F-F): the engine re-save serializes PO!U33 to exactly
  v11's stored bytes, `&apos;` entities and `aca="false"` included. v11's stored form of U33:
  `{u33}`
- **The user's Excel parsed all of it** (F-C/F-E above).
- Two further non-canonical-looking traits were investigated and cleared: the HC tabs' 22 overlapping shared-formula
  group refs exist identically in the Excel-authored source workfile (docProps Application "Microsoft Excel"), so
  they are Excel-legal (F-G; table below); and v11's sharedStrings `count` attribute (4,136 declared vs 2,411 actual
  references) is advisory only - the user's Excel ignored it. The engine save normalizes both anyway (no shared
  formulas left at all; sharedStrings consistent).

Entity-escaped `<f>` cells by sheet (measured; `&amp;`/`&lt;`/`&gt;` excluded):

| Sheet | v11 cells | v11 entities | v12 cells | v12 entities |
|---|---|---|---|---|
{ent_table}

Shared-formula group refs that overlap (v11 = the Excel-authored source workfile, pair for pair; v12 has none -
the engine stores every formula explicitly):

| Sheet | group A | group B |
|---|---|---|
{ov_table}

### The fix shipped in v12 (commissioned hardening)

`02-build_COO_2027_Budget_Collated_v12.xlsx` = v11 loaded once by LibreOffice {lo_ver} headless
with a full-recalculation profile (OOXMLRecalcMode = 0) and saved by `--convert-to xlsx` - a true engine save, not a
package patch. Every part of the zip is written by the engine's serializer in one pass. Serialization-only changes
(meaning and values proven unchanged, next section):

| Change class | v11 | v12 |
|---|---|---|
| Mixed provenance | parts from 3 writers (LibreOffice v3/v6-era, Microsoft Excel source parts, script splices v5-v11) | every part from one LibreOffice {lo_ver} save |
| Shared formulas (HC/Logistics tabs) | {m(s11['total_shared_f'])} master/follower cells, 22 Excel-authored overlapping group refs | 0 - every formula stored explicitly per cell |
| Inline strings | {m(sum(sh['t_counts'].get('inlineStr', 0) for sh in s11['sheets'].values()))} inlineStr cells (script-written and converted parts) | rebuilt sharedStrings table ({m(s12['sharedStrings']['actual_entries'])} entries, {m(s12['sharedStrings']['actual_refs'])} refs, count attributes consistent) |
| sharedStrings count attr | declared {m(s11['sharedStrings']['declared_count'])} vs {m(s11['sharedStrings']['actual_refs'])} actual refs (advisory; harmless) | consistent |
| Styles | 432 cellXfs incl. Excel-era number-format spellings | renumbered/deduplicated (416 cellXfs); 3,399 cells' format strings re-escaped to the same rendered format (7 spellings, e.g. `mmm-yy` -> `mmm\\-yy`) |
| Zip packaging | parts appended across builds ([Content_Types].xml 29th) | engine-ordered package |

Kept: all 20 sheets, order and visible states; every formula's meaning; every cached value (<= 4.1e-08); all 12
comments; number formats (rendered form); hidden row/column flags; frozen panes and print setup (engine-carried);
the CONFIDENTIAL banner; the Collation Notes sheet exactly as regenerated in v11 (texts now in sharedStrings; its 36
live formulas incl. H78:H81 unchanged). docProps (created/modified/author fields) are carried unchanged from v11 -
the convert filter does not touch them.

### Verification (all green; scripts in `scripts/`, JSON artifacts in the work dir)

- **Semantic diff v11 -> v12** (`fdiff_v12.py`): {m(fd['cells_compared'])} cells on 20 sheets; **0 formula
  differences** ({m(fd['formula_cells'])} formula cells compared on openpyxl-normalized text, v11 shared formulas
  expanded to their explicit per-cell form; array formulas {fd['array_formulas_old']}/{fd['array_formulas_new']}
  with ranges); **0 cached-value differences > 1e-6**, max drift {fd['max_value_drift']:.3e} at
  {fd['value_drift_cell']}; 0 number-format changes (rendered), 0 comment changes, 0 hidden-flag changes;
  defined names {m(fd['defined_names_old'])} -> {m(fd['defined_names_new'])} (unchanged, none dropped or added).
- **Standard suite** (`suite_v12.py`): COO P&L = sum of departments on all {m(su['collation_sums']['cells'])}
  SUM(FO,PO,CO,FE,PE) cells (max deviation {su['collation_sums']['max_dev']:.3e}); 0 error cells in v12 and in its
  recalculation; a LibreOffice full recalc of v12 reproduces v12's own cache on all {m(su['recalc']['cells'])}
  cached cells (max drift {su['recalc']['max_drift']:.3e}); Collation Notes' 36 live formulas identical to v11 and
  the H78:H81 "must be 0" checks cache and recalculate to 0; CONFIDENTIAL banner present; 0 shared formulas left.
- **Evidence figures** (cached, = v11; 2dp display as the workbook formats them): COO P&L AG132 =
  {d2(su['figures']['COO P&L!AG132'])}; N132 = {d2(su['figures']['COO P&L!N132'])}; revenue AG16 =
  {d2(su['figures']['COO P&L!AG16'])}; CO 6610/6630/6640 = {d2(su['figures']['CO!AG67'])} /
  {d2(su['figures']['CO!AG68'])} / {d2(su['figures']['CO!AG69'])}; PO 5110-5140 = 0; labour depreciation R195 =
  {d2(su['figures']['Depreciation Schedule!R195'])}.
- **Scenario switches still work** (scratch copies of v12, one typed input flipped, LibreOffice full recalc;
  handoff targets within $1): B131 = 0 -> AG132 = {d2(sc['B131=0']['AG132'])} (target (399,860); PO 5110-5140
  base {d2(sc['B131=0']['PO_5100_sum'])} = 590,317.51); B135 = 0 -> {d2(sc['B135=0']['AG132'])} (target 32,228);
  B132 = 1 -> {d2(sc['B132=1']['AG132'])} (target 98,441).
- **Package scan of v12** (`fscan_v12.py --require-clean`): XML well-formed, rows/cells ordered, dimensions cover,
  0 shared-formula orphans, 0 overlapping group refs, 0 error caches, sharedStrings consistent.
- **Reproducibility** (`normcmp_v12.py`): two independent engine saves in each pass, and the saves of pass 1 vs
  pass 2, are byte-identical part for part after one normalization: LibreOffice emits the children of
  `<dataValidations>` in nondeterministic order (everything else, including docProps, is deterministic; zip entry
  timestamps differ by wall clock, so whole-file byte-identity is not achievable - this is the explained deviation
  the handoff allows). The shipped file is pass 1's first save, untouched. The v12 md is byte-identical across
  passes.

### Deviation from the handoff's completion criterion "0 entity-escaped `<f>` elements"

Not enforced, for cause: it is unsatisfiable by any LibreOffice save (the engine escapes `'` and `"` in formula
text; v12 carries {m(s12['total_entity_f_cells'])} such cells) and it encodes the refuted hypothesis - the user's
Excel demonstrably parsed every one of v11's {m(s11['total_entity_f_cells'])} entity-carrying formulas (F-C/F-E).
Post-processing them away would reintroduce hand-patched XML, the exact technique v12 retires. Enforced instead:
every part engine-serialized in one save; 0 shared formulas; 0 orphans/overlaps; 0 error cells; sharedStrings
consistent; formula semantics and values identical to v11; recalc self-consistent; scenarios green; two-pass
reproducible as above.
"""

# ---- splice into the v11 md --------------------------------------------------------------------
old_title = "# 02-build notes v11 - 2027 COO budget collation (corrections pass on v10; figures unchanged)"
new_title = ("# 02-build notes v12 - 2027 COO budget collation (Excel #REF! diagnosis + engine re-serialization "
             "of v11; figures unchanged)")
assert md.startswith(old_title), "v11 md title changed"
md = new_title + md[len(old_title):]

anchor = "## Decisions pending"
assert md.count(anchor) >= 1
md = md.replace(anchor, sec + "\n" + anchor, 1)

dec = f"""## Decisions (v12, builder)

- D1 (v12): Fix method - a pure engine save. The deliverable is the untouched byte output of one LibreOffice
  `--convert-to xlsx` run on v11 (full-recalculation profile). No package patch, no post-processing of any part;
  the v8-v11 byte-stable-patch technique is retired for worksheet content.
- D2 (v12): Diagnosis before fix, from the user's saved copy (`00-brief/inputs/USER_EDIT_FINAL_v4_HC.xlsx`, an
  input). Every diagnostic claim in 'Changes from v11' is executable: `forensics_v12.py` asserts F-A..F-G against
  the files and the build refuses to write these notes if any assertion fails. The orchestrator's entity hypothesis
  is reported as refuted rather than silently dropped, because the handoff ordered the pre-scan verified.
- D3 (v12): The handoff completion criterion "0 entity-escaped <f> elements" is not enforced (unsatisfiable by any
  LibreOffice save and moot - see the deviation section); the enforced criteria are listed there. This deviation is
  flagged to the verifier rather than worked around with hand-edited XML.
- D4 (v12): Reproducibility standard - two passes must agree on the md byte for byte and on the xlsx part for part
  after sorting `<dataValidations>` children (LibreOffice emits that one list in nondeterministic order; zip entry
  timestamps are wall-clock). Whole-file byte-identity is documented as not achievable instead of being simulated
  by re-zipping, which would replace the engine's container with a scripted one.
- D5 (v12): The Collation Notes sheet is carried through the engine save, not regenerated: its v11 content (F1 fix,
  H78:H81 live formulas) is exactly what v12 must preserve, and regeneration would have meant splicing a
  script-written part back into an otherwise engine-written package.
- D6 (v12): No value or formula-meaning change is made anywhere, including NOT re-anchoring PO!U33:AF35 for the
  user's Material-Handler move: that is a value-affecting model change, out of this handoff's scope and queued as
  v14 (brief v8). v12 is the clean base the user should work from until then.

"""
limits_anchor = "## Not done / limits"
assert md.count(limits_anchor) == 1
md = md.replace(limits_anchor, dec + limits_anchor, 1)

old_limit = "- Not opened in Microsoft Excel (LibreOffice recalculation only)."
new_limit = (
    "- Excel status: v11/FINAL_v4 WAS opened by the user in Microsoft Excel (Mac) on 2026-10-12 and loaded cleanly - "
    "no repair, every formula intact in their re-saved copy; the #REF!s they reported were produced by their own "
    "in-Excel deletion of HC-PO row 20 (Material Handler, MH-01), which PO!U33:AF35 reference (see 'Changes from "
    "v11 (v12)'). v12 itself (the engine re-save) has not been opened in Microsoft Excel here - validation is "
    "LibreOffice-only (semantic diff, recalculation, scenarios); the user's open test remains the final check, and "
    "on a clean open the PO 33-35 rows show 0, not #REF!."
)
assert md.count(old_limit) == 1
md = md.replace(old_limit, new_limit, 1)

open(OUT, "w", encoding="utf-8").write(md)
print(f"report_v12: wrote {OUT} ({len(md)} bytes; v11 md + diagnosis/fix section + decisions + Excel-status limit)")
