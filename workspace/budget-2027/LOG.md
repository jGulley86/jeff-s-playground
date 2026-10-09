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
