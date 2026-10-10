# Final report v3 — 2027 COO Budget Collation
**CONFIDENTIAL. The workbook HC-* tabs contain named employee compensation, and the notes contain exact salaries for some unique roles. Restrict distribution.** The repo is private (user-confirmed 2026-10-10).
Supersedes FINAL_REPORT.md (v4-based).

**Objective:** Collate the COO Dept P&Ls and the Service Delivery worksheets into one 2027 budget, and flag issues. Scope later extended by user decisions:
- resolved DeploySum 9/30/26
- 2027 revenue
- straight-line depreciation: SlipLift 7y → 5011; trays = carriers 10y → 5012
- HoSD salary 205k
- HC roster reconciliation
- production labour capitalised, using the file's formulas

**Specialists:** builder (v1–v9), critic (v1, v3, v4, v6, v8, v9), verifier (v1, v3, v5, v6, v7, v8, v9).

## Files
| File | What |
|---|---|
| `05-final/COO_2027_Budget_Collated_FINAL_v3.xlsx` | Final workbook (= v9) |
| `05-final/COO_2027_Budget_Notes_FINAL_v3.md` | Decisions, headline, caveats, assumptions, issues |
| `03-review/`, `04-verify/` | All reviews and verifications |
| `02-build/scripts/run_build_v9.sh` | Reproducible build |

## Headline — 2027 COO contribution (company revenue less COO costs; not company NI)
| | 2026 | 2027 |
|---|---:|---:|
| Revenue (9/30/26 sales plan, incl. unsigned bookings) | 7.42M | 15.56M |
| **COO contribution** | **(0.90M)** | **+0.69M (687,435)** |

- The 2026→2027 change is not like-for-like. Capitalising production labour is worth +2.51M of policy effect.
- The capitalisation is a reclassification. The 2027 CapEx budget needs +2.59M for production payroll.
- Dec-27 balance sheet: 1.84M of labour in PP&E in service (net), and 0.65M in PP&E not yet placed in service (CIP).
- Labour depreciation in 2027: 104,417 (5011 79,290; 5012 25,126).

## Evidence / tests
- **Integrity:** every version has COO P&L = Σ depts and 0 new errors. A full LibreOffice recalc reproduces the cached values (28,047 cells in v9).
- **Independent rebuilds:** the verifier rebuilt depreciation, revenue tie-out, Prod Payroll (Python replica), labour capitalisation, and 6 switch scenarios. All matched.
- **XLOOKUP replacement:** the 16 cells replaced with INDEX/MATCH were tested on exact, between, above-max and below-min cases.
- **Not tested in Excel.**

## Switches (Depreciation Schedule tab)
- **B131:** capitalise the current 9 PO staff. Default 1; set 0 for (621,499).
- **B132:** capitalise Sep–Dec 26 labour. Default 0, so it stays 2026.
- **B135:** idle-month labour. Default 1 rolls it forward; set 0 for (126,908).

## Decisions still open (owners)
1. **Finance — capitalisation scope:**
   - current 9 staff (−621k if expensed)
   - idle-month labour (−127k)
   - whether 65k/8k unit costs already include labour (up to +104k)
   - rate-base gap (22k)
2. **PO owner — Logistics & WH payroll:** 7 new seats, 336,530 net, not in budget.
3. **SD owner — I-10:** 384k of 2026 lines set to 0 in 2027.
4. **Finance — SlipBot depreciation:** 1.35M carried flat (trend +276k to +404k; stop +1.35M). Needs the asset register.
5. **People/payroll items:**
   - probable FO/FE duplicate (+78.5k or +93k)
   - PE "transfer?" role (255k)
   - FE open seat (up to 174k)
   - HC tax rates below FICA (unverified)
6. **Small items:** Q4-26 go-lives (±39k), peripherals GL/life, revenue split.

No single item turns 2027 negative. Some pairs do, e.g. the current 9 expensed + idle months → (14,467), or I-17 + I-10 → (33,520). Illustrative range: (340,662) to 2,041,009.

## Reader notes (critic v9, optional)
- **2026 forecast gap:** the Q4-26 ramp hires in the SD production model (~260k est.) are not in the 2026 PO forecast or anywhere else. Refer this to the 2026 forecast owner.
- **Memo B238 in the B132=1 scenario:** it excludes the Nov-26 vintage (~77k). The booked case is unaffected.
- **Decision #10:** "(14,467)" is a contribution; the combined effect is (701,902).

## Actions waiting for approval
None.

## Final status: COMPLETED
Critic 0 BLOCKING; verifier PASS. Owner decisions above will move the number.
