# Final report v5 — 2027 COO Budget Collation
**CONFIDENTIAL. The workbook's HC-* and Logistics&WH tabs contain named employee compensation; the notes contain exact salaries for some unique roles. Restrict distribution.** Repo is private (user-confirmed).
Supersedes FINAL_REPORT_v4.md (v11-based). FINAL_v5 = build v14.

**Objective:** Collate the COO Dept P&Ls and the Service Delivery worksheets into one 2027 budget and flag issues. Scope grown by user decisions through 2026-10-12: resolved DeploySum 9/30/26; 2027 revenue; straight-line depreciation (SlipLift 7y → 5011, trays = carriers 10y → 5012); HoSD 205k; HC roster reconciliation; production labour capitalised per the file's formulas; Logistics & WH payroll in Central Operations; Facilities Manager 110k; CO GL 7700 +2,000/mo and 8600 +6,500/mo; the user's roster merge (11 hires/moves: 4 CO, 5 PE, 1 PO, 1 FE) with PE wired live, the Production Manager expensed to PO 6610, the Servando-backfill seat de-duplicated, and the FO/FE duplicate resolved.

**Specialists:** builder (v1–v14), critic (8 reviews), verifier (12 reports incl. the full v1–v9 sweep).

## Files
| File | What |
|---|---|
| `05-final/COO_2027_Budget_Collated_FINAL_v5.xlsx` | Final workbook (= build v14; engine-saved, Excel-safe) |
| `05-final/COO_2027_Budget_Notes_FINAL_v5.md` | Decisions, headline, caveats, assumptions (A-01..A-47), issues (I-01..I-42) |
| `03-review/`, `04-verify/` | All critic reviews and verifier reports |
| `02-build/scripts/run_build_v14.sh` | Reproducible build (chain v1→v14 all re-runnable) |

## Headline — 2027 COO contribution (company recognized revenue less COO costs; not company NI)
| | 2026 | 2027 |
|---|---:|---:|
| Revenue (9/30/26 sales plan, incl. unsigned bookings) | 7,423,940 | 15,563,646 |
| **COO contribution** | **(899,222)** | **(646,754)** |

Journey of the 2027 figure as decisions landed: (11.85M cost-only) → +393k (revenue+depreciation) → +139k (HoSD) → +687k (labour capitalised) → +159k (logistics→CO, Facilities Mgr) → **(646,754)** after the 7700/8600 additions (−102k), the roster merge (CO −71k, PE −555k, PO PM −157k) and the duplicate fix (+79k). Verified to the cent at every step; reverting all v13 changes reproduces +159,136.40 exactly.

## Policy switches (Depreciation Schedule tab; values on the shipped file)
- **B131** capitalise the current 8 PO production staff (default 1). 0 → (1,205,750.10).
- **B132** capitalise Sep–Dec-26 labour (default 0). 1 → (707,448.94).
- **B135** idle-month labour roll-forward (default 1). 0 → (773,662.29).

## Evidence / tests
Every version independently verified (own scripts, cache-stripped recalcs, scenario flips): roll-up identity to 5.8e-10; 0 error cells; recalc reproduces all 29,021 numeric cells with max diff 0.0; roster transcription equals the user's file cell-for-cell; payroll lines recomputed from raw roster inputs; seat de-dup composition checked live by H78:H81 = 0. Not tested in Microsoft Excel here (LibreOffice 24.2.7.2); the earlier Excel #REF! incident was the user's own row deletion severing a reference — v13 re-anchored those formulas so that failure mode cannot recur, and v12+ files are full engine saves.

## Decisions waiting on the user (each isolated and small)
1. **PO production freight R24:R26:** your edited file sets "YOY Growth" (adds 60,056.60 of COGS → ≈ (706,810)). Carry it?
2. **HC-PE "transfer?" flag cleared** in your file — is the ~255k transfer-out upside off?
3. **Material Handling Team Lead three-way:** (a) Nov-26 end, stays production (booked); (b) all-2027 CO role (+~70k CO AND remove from the capitalised base, else double-carried); (c) left the company (then the capitalised base drops to 518,256.91 under B131=0 and the model count needs −1).
4. **GL 7700** is labelled "Inventory Obsolescence-old" — confirm the account for the 2,000/mo.

## Standing owner items (unchanged)
Finance: capitalisation scope switches above; labour possibly already in the 65k/8k unit costs (up to +104k); SlipBot depreciation 1.35M flat (full run-off +1,353,574 → ≈ +706,820, the only single upside that turns 2027 positive). SD owner: I-10, 384,425 of 2026 lines at 0 for 2027 (alone → ≈ (1,031,179)). 2026 forecast owner: the rosters' Sep–Dec-26 starters and the SD models' Q4-26 ramp hires are in no 2026 book. Bounds (illustrative, asymmetric): (1,275,819) / (1,714,922) to +706,820; revenue must beat plan by ~4.2% to break even at booked costs.

## Known stale text (disclosed; no figure depends on it; fix rides the next build)
Collation Notes E346 (I-06 evidence still says 14 techs / 1,094,774; current 13 / 1,016,576) and E352 (I-12 says AG46 288,069; current 287,738.40); I-29 evidence rates stale since v10; D357 lacks a superseded pointer; two sign-convention/per-head wording nits in H381; $1 print truncation (3,036,558 vs 3,036,558.86).

## Actions waiting for approval
None.

## Final status: COMPLETED (open decisions above will move the number)
Verifier: all figures PASS on v13 and v14; the residual FIX FIRST items are the disclosed stale-text cells. Critic: v13's blocking wording issue fixed and verified in v14.
