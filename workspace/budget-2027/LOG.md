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
| T9 | brief | orchestrator | done | user confirmed Trays = Carriers → 5012 |
| T10 | build | builder | done | v2: 0 value diffs vs v1; names 14,310→8,965; 0 externalLink parts; overlap table (0 likely double counts); I-17 Logistics&WH up to 547,441 HIGH; new I-26..I-29 |
| T11 | build | builder | started | v3 per brief_v2 + brief_v3 (DeploySum refresh, revenue, depreciation). v2 verification folded into v3 verify |
| T12 | build | builder | done | v3: NI 2027 +393,486; rev 15.56M; dep 3.32M (existing 1.91M + new 1.41M); 4 user decisions open (I-01, I-31, I-32, I-33) |
| T13 | review+verify | critic, verifier | started | parallel on v3 |
| T14 | verify | verifier | done | v3 PASS — 04-verify/04-verify_report_v3.md |
| T15 | review | critic | done | v3: 1 BLOCKING (headline caveats) / 8 OPTIONAL — 03-review/03-review_critic_v3.md |
| T16 | build | builder | started | v4 notes-only fix (no value changes): B1 + O1–O8; Collation Notes sheet refresh |
| T17 | build | builder | done | v4: notes/Collation Notes only; 0 diffs vs v3 (27,700 cells); caveat table; sign-flip: negative on I-05 or I-17 alone |
| T18 | review | critic | started | re-check v4 vs critic v3 items |
| T19 | review | critic | done | v4: 0 BLOCKING / 3 OPTIONAL — 03-review/03-review_critic_v4.md |
| T20 | final | orchestrator | done | 05-final/ (FINAL xlsx = v4, notes, FINAL_REPORT.md). Status COMPLETED; owner decisions open |
| T21 | build | builder | started | v5: user-confirmed HoSD salary 205,000 → Fld Eng Budget!B21 (resolves I-26) + critic v4 N1–N3 |
| T22 | brief | orchestrator | done | brief_v4.md: 4th input COO HC & PL workfile (rosters); v6 reconciliation queued after v5 |
| T23 | build | builder | done | v5: HoSD 205k in Fld Eng Budget!B21; contribution 393,486 → 139,032 (−254,454 incl. SD burden 6.8%/16.4%); critic N1–N3 applied |
| T24 | verify | verifier | started | v5 |
| T24 | build | builder | started | v6 per brief_v4 (HC roster reconciliation), parallel with v5 verify |
| T25 | verify | verifier | done | v5 PASS — 04-verify/04-verify_report_v5.md |
| T26 | build | builder | done | v6: 0 diffs vs v5; HC tabs added; I-05 net 1,962,389; I-17 net 336,530; FO current 1,338,696 / ramp 2,618,543; 1 duplicate person (FE r15 = FO HC r15); FE burden +109,539; PE transfer 254,785. Roster CSV (per-person salaries) kept out of git |
| T27 | review+verify | critic, verifier | started | v6 parallel |
| T28 | review | critic | done | v6: 3 BLOCKING / 8 OPTIONAL — 03-review/03-review_critic_v6.md; awaiting verifier before v7 |
| T29 | verify | verifier | done | v6 FIX FIRST: I-28 FO figure +78,529 not +78,198; rest confirmed — 04-verify/04-verify_report_v6.md |
| T30 | build | builder | started | v7 notes-only fix: critic v6 B1–B3 + O1–O8, verifier fix |
| T31 | build | builder | done | v7 notes-only: 0 diffs vs v6; expensed (1,823,358)/(1,963,470) vs capitalised 74,297/69,674 vs in-unit-cost 139,032; dedup combined 2,360,882/2,439,031 |
| T32 | verify | verifier | started | v7 new figures |
| T35 | brief | orchestrator | done | brief_v5.md: production labour capitalised (Prod Payroll model → Depreciation Schedule); repo private |
| T36 | build | builder | started | v8 |
| T37 | build | builder | done | v8: prod labour capitalised; contribution 139,032 → 638,814; dep +153,038; PO 5100 → 0; CIP 650,571; sensitivity (9 expensed) 37,696 |
| T38 | review+verify | critic, verifier | started | v8 parallel |
| T39 | review | critic | done | v8: 2 BLOCKING (Q4-26 labour double count; idle-month unquantified) / 7 OPTIONAL — 03-review/03-review_critic_v8.md |
| T40 | verify | verifier | done | v8 PASS — 04-verify/04-verify_report_v8.md |
| T41 | build | builder | started | v9: B132=0 (2026 labour stays 2026 cost) + critic v8 B1/B2 + O1–O7 |
| T42 | build | builder | done | v9: contribution 687,435; labour dep 104,417; CIP 650,571; idle-month (126,908) not booked; departures accepted (idle switch B135; PO U33:AF35 formula edit, zero value change) |
| T43 | verify | verifier | started | v9 |
| T44 | verify | verifier | done | v9 PASS — 04-verify/04-verify_report_v9.md |
| T45 | review | critic | started | v9 re-check vs critic v8 items |
| T46 | review | critic | done | v9: 0 BLOCKING / 3 OPTIONAL — 03-review/03-review_critic_v9.md |
| T47 | final | orchestrator | done | 05-final/*_FINAL_v3 (= v9) + FINAL_REPORT_v3.md; COMPLETED |
| T48 | brief | orchestrator | done | brief_v6.md: Logistics&WH payroll → CO (excl LOG-01), material handler PO→CO, add CO employee 110k; SD re-upload identical in values |
| T49 | build | builder | started | v10 |
| T50 | verify | verifier | started | Full re-validation sweep of v1–v9 after model switch (v10 build still running in parallel) |
| T51 | build | builder | done | v10: Logistics&WH → CO (398,492 incl MH-01; LOG-01 excluded); new CO employee 129,806; contribution 687,435 → 159,136; HC-COO roll-up deviation accepted |
| T52 | verify | verifier | started | v10 (parallel with v1–v9 sweep) |
| T53 | verify | verifier | done | Full v1-v9 sweep: all figures, integrity, scenarios and 9/9 chain rebuilds PASS; F1 (unsupported SD-date sentence, notes v7+) routed to next build; F2 (v7 script mode) fixed — 04-verify/04-verify_report_fullsweep.md |
