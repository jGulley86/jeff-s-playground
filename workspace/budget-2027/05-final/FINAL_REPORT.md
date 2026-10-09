# Final report — 2027 COO Budget Collation

**Objective:** Collate the COO Dept P&Ls and the Service Delivery P&L worksheets into one 2027 budget and flag issues. Later scope (user decisions): bring in the resolved 9/30/26 DeploySum file; add 2027 revenue and straight-line depreciation (SlipLift 7y → 5011; trays = carriers, 10y → 5012).

**Specialists involved:** builder (v1–v4), critic (3 reviews), verifier (v1, v3). Research skipped because all sources were supplied.

## Files
| File | What |
|---|---|
| `05-final/COO_2027_Budget_Collated_FINAL.xlsx` | Final workbook (= build v4). Tabs: Collation Notes, COO P&L, FO, PO, CO, FE, PE, DeploySum, Depreciation Schedule, driver tabs |
| `05-final/COO_2027_Budget_Notes_FINAL.md` | Decisions pending, headline, caveats, assumptions register (A-01..A-25), issues (I-01..I-33) |
| `03-review/`, `04-verify/` | Critic and verifier reports |
| `02-build/scripts/run_build_v4.sh` | Reproducible build |

## Headline (COO P&L)
| | 2026 | 2027 |
|---|---:|---:|
| Revenue (company recognized, sales plan 9/30/26) | 7,423,940 | 15,563,646 |
| COGS (incl. depreciation 1.79M → 3.32M) | 4,478,016 | 12,152,017 |
| Opex | 3,929,957 | 3,018,142 |
| **COO contribution** (not company NI) | **(899,222)** | **393,486** |
| COO cost only (COGS + Opex) | 8,407,973 | 15,170,160 |

**The sign of 2027 is not established.** It turns negative on I-05 alone (production payroll model gap ~970k) or on I-17 alone (Logistics & WH payroll 547k). The range shown in the notes is illustrative, not a bound (critic N2).

## Evidence checked / tests performed
- COO P&L = FO+PO+CO+FE+PE on every additive cell (2,988 cells, max diff 3.8e-10).
- FO/FE match the SD book; PO/CO/PE match the COO book (0 diffs), except the PO revenue and depreciation rows added by request.
- Depreciation recomputed independently for all 48 GL-months. The CapEx reconciliation is $0.00 for every month Sep-26..Dec-27.
- Revenue = DeploySum recognized revenue ($0.00 difference). A full LibreOffice recalculation reproduces all 24,058 numeric cells.
- 0 new formula errors; 0 external links; 5,345 broken legacy names pruned.
- v4 vs v3: 0 value or formula diffs outside the Collation Notes tab.

## Assumptions (main ones)
- All 2027 revenue goes to 4100 (2026 had 1.06M on 4500/4900).
- The existing fleet is carried flat at the Dec-26 forecast rate.
- Full-month depreciation from the go-live month.
- Peripherals of $4,137.50 per lift go to 5020 over 84 months.
- Revenue includes unsigned forecast bookings.
- Not tested in Microsoft Excel (LibreOffice only).

## Unresolved issues (owner decisions)
1. **I-32 SlipBot depreciation 1.35M.** Options: continue flat, follow the 2026 trend (+276k, or about +127k more if the trend also ran through Q4-26, per critic N3), or stop it (+1.35M).
2. **I-17 Logistics & WH payroll 547k** is not linked into PO.
3. **I-05 production payroll model** shows 1.62M vs PO's typed 653k.
4. **I-31 Oct–Dec 26 go-lives.** Either a 39k shortfall or a 37k double count. The PO owner must confirm.
5. **I-33 peripherals GL and life; revenue split; I-26** Head of Service Delivery salary blank; **I-10** 384k of 2026 lines at 0 in 2027.
6. **Critic N1.** Text on the Depreciation Schedule tab (B17, D21, row 19 heading) is superseded by A-17, A-18, A-19 and I-31 in the notes.

## Actions waiting for approval
None. Nothing was sent, published or posted.

## Final status: COMPLETED
Deliverable done, critic 0 BLOCKING, verifier PASS. The numbers will move once the owner decisions above are made.
