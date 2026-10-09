# LOG — budget-2027
| Time | Stage | Owner | Status | Note |
|---|---|---|---|---|
| T0 | brief | orchestrator | done | 00-brief/brief_v1.md; inputs copied; pre-scan complete |
| T1 | build | builder | started | collate workbook v1 |
| T2 | build | builder | done | 02-build/02-build_COO_2027_Budget_Collated_v1.xlsx + notes_v1; NI 2027 -5.28M -> -11.85M; 25 issues |
| T3 | review | critic | started | read-only review of v1 |
| T3 | verify | verifier | started | independent recompute of v1 (parallel with critic) |
| T4 | verify | verifier | done | PASS — 04-verify/04-verify_report_v1.md |
| T5 | review | critic | done | 3 BLOCKING / 10 OPTIONAL — 03-review/03-review_critic_v1.md; B1 partly overruled (handoff did instruct freeze) |
| T6 | build | builder | started | v2 fixes: B1–B3 + optionals 1–8,10 |
| T7 | brief | orchestrator | done | brief_v2.md: third input (resolved DeploySum 9/30/26); v3 build queued after v2 |
| T8 | brief | orchestrator | done | brief_v3.md: user chose Option 3 (revenue + SL depreciation, Lift 7y / Tray 10y); v3 build queued after v2 returns |
