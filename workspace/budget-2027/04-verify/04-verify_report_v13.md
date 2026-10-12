# Verifier report v13 — VERDICT: FIX FIRST (text only; every number reproduces)
Own scripts (scratch verify13/). Workspace untouched.

CONFIRMED (all independently recomputed): AG132 = (646,753.85), also from a cache-stripped full recalc. Bridge A (102,000.00) / B+D (71,048.29) / C (554,864.53) / E (156,506.51) / F +78,529.08 / G 0.00; completeness proven by reverting all six groups → back to 159,136.40 exactly. CO 1,218,308.22; PE 1,766,501.82 (wiring itself moves nothing: v12 constants = roster recompute to 7e-12); PO 6610–6640 156,506.51. Seats OUT MH-01/TL-01/MH-02 (188,469.90) with LOG-01; IN 5 seats 210,022.54; hire costs correctly 2026. Roster transcription: 0 differences vs the user's file (names, titles, salaries, dates). Scenarios: B131=0 (1,205,750.10) with base 590,317.51; B135=0 (773,662.29); B132=1 (707,448.94); deltas = v12's to the cent. Suite: roll-up 5.8e-10; 0 error caches; recalc max diff 0.0; H78:H81 = 0; 0 shared formulas; parts/names/comments identical to v12 except Collation Notes; 2026 B:N unchanged on the six P&L sheets. Bounds (1,275,819)/(1,714,922)/+706,820 and the 4.2% break-even statement check out.

FAILED (fix in v14; no values change):
- md headline Gross Profit row: v12 column shows 4,038,561 / change 0; true 3,960,032 / +78,529.
- Collation Notes stale v12-era text in the current-state areas: E17, A32, A33, C43, C60, C61, F357, row 377, D380, A35 (details in the verifier message; scripted sweep of rows 8–71, 357, 375–381 recommended).
- "0 #REF! anywhere" is literally false: 6 historical text mentions (harmless).

USER CONFIRMATIONS NEEDED (not changed):
1. PO!R24:R26 (production freight 5025/5026/5027) is "YOY Growth" in the user's edited file vs "Even"/0 in every version since v1. Carrying it adds 60,056.60 of 2027 COGS → AG132 ≈ (706,810.44).
2. HC-PE!A22 "transfer?" flag is blank in the user's file (present since the workfile). No number changes; I-35's ~255k upside rests on it.
3. (Critic) the TL three-way (end-date/role/left-company) — asked.

Note: a recalc cannot restore v12's PO 5110–5140 once HC-PO r20 is blank (#VALUE!), supporting the G re-anchor.
