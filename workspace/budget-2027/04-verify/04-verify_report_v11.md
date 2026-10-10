# Verifier report v11 — VERDICT: PASS
Own scripts (scratch verify11/). Workspace untouched (145-file sha256 manifest identical pre/post).

- **Only two workbook parts changed vs v10** (zip-level): Collation Notes and PO. PO differs in exactly the 3 text cells AI33:AI35 (no formula, no value); swapping those 3 cells into v10 reproduces v11 byte for byte.
- **AG132 byte-identical to v10:** 159,136.400508629 (recalc diff 0).
- **False SD-date sentence gone everywhere:** 8/8 fragments hit in v10 (positive control), 0 hits in v11 md and all 66 workbook parts; every remaining "2026-10-09" is a user-decision date, the labelled retraction, or the collated file's own save stamp. The replacement sentence's premise verified (SD books carry no docProps; workfile 2026-10-07 is real).
- **H78:H81 are live formulas computing 0:** verified from a cache-stripped recalc; negative control (forcing CO!U67=0) moves them, so they are live and sensitive.
- **No value changed anywhere:** 0 numeric diffs on Collation Notes' aligned rows; B:N v9→v11 unchanged on the six P&L sheets and every driver sheet.
- **Full recalc clean:** 28,173 numeric cells, max diff 9.3e-09, 0 errors; also from a stripped cache. COO P&L = Σ depts (max 5.0e-08; dept sum ties AG132 to 3e-08).
- **Build date-independent:** re-run under frozen clocks of 2026-10-10 and 2031-03-17 reproduces the delivered xlsx and md byte for byte.
- **Privacy:** no roster names in the new text.

Notes: the dated retraction line is intentional and kept; 05-final v3 files are stale (v9-based, carry the retracted sentence) — replaced by the FINAL_v4 package; one non-exhaustive parenthetical in fix 6a (HC-CO I18:L18 also went empty→0; the P&L claim is exact); Excel behaviour untested (LibreOffice only).
