# Full re-validation sweep (v1–v9) — VERDICT: FIX FIRST (2 low, non-numeric items; all figures PASS)
Fresh audit by an independent verifier (own scripts in session scratch, since deleted). Workspace manifest identical before and after; HEAD unchanged.

## P1 — inputs, package, integrity (all PASS)
- Input sha256s match the recorded ones (COO a3264ef4, SD fedee8d1, workfile 01eca67d, DeploySum 9/30 645e3130, SD re-upload 14f74413; the re-upload is value-identical to the original).
- 05-final identity: FINAL_v3.xlsx = v9 build; FINAL.xlsx = v4 build (sha256); the notes files are byte-identical to their build sources.
- All nine versions: COO P&L = Σ depts (max diff 5.0e-8); error cells = the known sets only (v8/v9: 0); full forced recalc AND stripped-cache recalc reproduce every cached value (max diff 9.9e-8); 0 externalLink parts; defined names 8,965 from v2 on.
- Every reported headline figure re-confirmed to the cent in all nine versions (−11,851,351.34 → 393,486.04 → 139,031.84 → 638,813.73 → 687,435.11; N132 −899,222.05 throughout).
- v9 switch scenarios re-confirmed: B135=0 → 560,526.67; B131=0 and B135=0 → −14,467.29; B132=1 → 626,740.02; B131=0 → 65,936.42.
- Independent re-derivations: depreciation from the inputs (3e-9), Prod Payroll replica (5e-10), labour-capitalisation replica (to the cent in 7 switch cases), INDEX/MATCH vs XLOOKUP (32 cases, 0 mismatches), version bridges exact.

## P2/P3 — chain reproducibility (all PASS)
All nine builds re-run from committed predecessors: v4, v5, v8, v9 byte-identical; v1–v3, v6 content-identical (only LibreOffice save timestamps differ); v7 content-identical except one date string (see F1).

## Fixes (route to next build; no numbers change)
- **F1 (low):** the I-38 evidence sentence "the SD book's properties show 2026-10-09 (a re-save…)" is unsupported — the SD book has NO document properties, and openpyxl returned the build date. Present in notes v7–v9, Collation Notes v7!E254 / v8!E322 / v9!E347, and FINAL_v3. Fix the wording; stop reading `.modified` on that file. (The workfile's 2026-10-07 date IS correct.)
- **F2 (low):** run_build_v7.sh was committed non-executable (exit 126 when run directly; `bash run_build_v7.sh` works). Fix: chmod +x and commit.

## Observation (check in v10)
- v9 PO!U33:AF35 embed the HC-PO monthly amounts as constants (equal today to 1e-11) rather than linking HC-PO; this matters only when B131=0 and after roster edits.

NOT RUN: Microsoft Excel evaluation; notes-only component sizes (I-10 / I-31 / I-32 variants etc. — only their arithmetic combination was checked); anything v10 (separate verification in flight).
