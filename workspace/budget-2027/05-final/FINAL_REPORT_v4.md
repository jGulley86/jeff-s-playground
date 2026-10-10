# Final report v4 — 2027 COO Budget Collation
**CONFIDENTIAL. The workbook's HC-* tabs and the Logistics&WH Payroll tab contain named employee compensation, and the notes contain exact salaries for some unique roles. Restrict distribution.** The repo is private (user-confirmed 2026-10-10).
Supersedes FINAL_REPORT.md (v4-build-based) and FINAL_REPORT_v3.md (v9-based). Note: the superseded FINAL / FINAL_v3 notes carry a sentence about the SD book's save date that was later found to be unsupported and is retracted in the v4 package.

**Objective:** Collate the COO Dept P&Ls and the Service Delivery worksheets into one 2027 budget and flag issues. Scope extended by user decisions:
- resolved DeploySum 9/30/26; 2027 revenue
- straight-line depreciation (SlipLift 7y → 5011; trays = carriers 10y → 5012)
- Head of Service Delivery salary 205k
- HC roster reconciliation
- production labour capitalised ("the file's formula": Prod Payroll model + existing Depreciation Schedule logic)
- Logistics & Warehouse payroll booked in Central Operations (not PO); material handler moved PO → CO; new CO employee added at 110k (2026-10-10)

**Specialists:** builder (v1–v11), critic (v1, v3, v4, v6, v8, v9), verifier (v1, v3, v5, v6, v7, v8, v9, v10, v11 + full v1–v9 sweep).

## Files
| File | What |
|---|---|
| `05-final/COO_2027_Budget_Collated_FINAL_v4.xlsx` | Final workbook (= build v11) |
| `05-final/COO_2027_Budget_Notes_FINAL_v4.md` | Decisions, headline, caveats, assumptions, issues |
| `03-review/`, `04-verify/` | All critic reviews and verifier reports, incl. the full v1–v9 re-validation sweep |
| `02-build/scripts/run_build_v11.sh` | Reproducible, date-independent build (verified byte-identical under two frozen clocks) |

## Headline — 2027 COO contribution (company recognized revenue less COO costs; not company NI)
| | 2026 | 2027 |
|---|---:|---:|
| Revenue (9/30/26 sales plan, incl. unsigned bookings) | 7,423,940 | 15,563,646 |
| **COO contribution** | **(899,222)** | **+159,136** |

Bridge of the final number: v9 687,435 − 398,492 logistics & warehouse booked in CO (7 new seats + material handler; Logistics Manager excluded, already in CO) − 129,806 new CO employee (110k salary + CO burden + 3% Oct raise) = 159,136.
- The 2026→2027 change is not like-for-like: capitalising production labour is a policy effect.
- Capitalisation is a reclassification: the 2027 CapEx budget needs +2,592,894 for production payroll. Dec-27 balance sheet: 1,837,906 of labour in PP&E in service (net) + 650,571 in PP&E not yet placed in service (CIP).
- CO 2027 SG&A payroll: 618,961 → 1,147,260.

## Policy switches (Depreciation Schedule tab)
- **B131** capitalise the current 9 PO production staff (default 1). Set 0 → contribution (399,860).
- **B132** capitalise Sep–Dec 26 labour (default 0: stays a 2026 cost). Set 1 → 98,441.
- **B135** idle-month labour (default 1: roll forward). Set 0 → 32,228.

## Evidence / tests
- Every version v1–v11 verified: roll-up identity, 0 stray errors, full LibreOffice recalc reproduces all cached values (also from stripped caches).
- Full re-validation sweep (2026-10-10): inputs hash-checked, all nine then-existing builds re-run from committed predecessors (4 byte-identical, rest content-identical), every reported figure re-confirmed to the cent, independent Python replicas of the payroll model, depreciation and capitalisation.
- v10/v11: CO payroll recomputed independently from raw roster/seat inputs (4.4e-11); live-linkage probes pass; no double counts (Logistics Manager once; material handler in CO only on the expense lines).
- Not tested in Microsoft Excel (LibreOffice 24.2.7.2 only).

## Decisions resolved by the user
Revenue + depreciation (option 3); trays = carriers (5012); HoSD 205k; production labour capitalised per the file's formulas; logistics & warehouse → CO; material handler → CO; new CO employee 110k; repo private.

## Decisions still open (owners)
1. **Finance — capitalisation scope:** current 9 staff (switch B131; −559k expense/−399,860 contribution if expensed), idle-month labour (B135; −126,908), labour possibly already inside the 65k/8k unit costs (up to +104,417), rate-base gap (~22k).
2. **SD owner — I-10:** 384,425 of 2026 lines budgeted at 0 for 2027. Alone it flips the sign: (225,288).
3. **Finance — SlipBot depreciation (I-32):** 1,353,574 carried flat; trend alternatives +276k–404k; fully depreciated +1,353,574 (→ 1,512,711). Needs the fixed-asset register.
4. **People items:** probable FO/FE duplicate (+78,529 or +93,093); PE "transfer?" role (254,785); FE open seat (up to 173,774); I-41 material-handling lead overlap on the 7-of-9 reading (−72,061); HC tax rates below 7.65% FICA (unverified, I-37 ~62k).
5. **Small items:** Q4-26 go-lives (±39k), peripherals GL/life (63,836), revenue split 4100 vs 4500/4900.
6. **2026 forecast owner:** the SD model's Q4-26 ramp hires (~260k labour) are in no 2026 book.

## Risk picture
Single items that flip the +159,136 negative: the B131 sensitivity (→ −399,860) and I-10 (→ −225,288). Pairs: idle + I-41 (−39,833); idle + I-31 (−6,829). Illustrative, asymmetric range: **(469,929) to 1,512,711** (LB2 excluding nothing but with B131=0 basis: (909,032)).

## Reader notes
- HC-COO is the unedited roster roll-up: it still lists the material handler under PO and holds no logistics seats, so its CO payroll (748,768) intentionally differs from the CO P&L (1,147,260).
- The in-book Logistics&WH tab is an unedited SD copy whose banner still says "rolls up to Production Operations"; it is booked in CO per the 2026-10-10 user decision.
- Superseded text in earlier notes claiming an SD save date of 2026-10-09 is retracted: the SD file carries no document properties.

## Actions waiting for approval
None.

## Final status: COMPLETED
Verifier PASS on v10, v11 and the full v1–v9 sweep; critic 0 BLOCKING. The owner decisions above will move the number.
