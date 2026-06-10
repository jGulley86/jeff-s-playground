# Data Basis — Extracted Source Data

All numbers in the feasibility plan trace back to this file. Sources: uploaded drawing
packages (106901-R02 Heavy Tray, 107455-R01 Wood Tray), NetSuite BoM Metrics exports,
and live NetSuite item-cost queries run 2026-06-10.

## 1. Build plan (given by Jeff)

| Family | Volume | Top-level item |
|---|---|---|
| Heavy Tray | 20 / month | 106901-R02 ASSEMBLY, HEAVY TRAY |
| Light (Wood) Tray | 10 / month | 107455-R01 ASSEMBLY, WOOD TRAY |

Note: NetSuite also carries 106997-R01 "ASSEMBLY, LIGHT TRAY" at $6,593.75. The uploaded
light-family data package is the Wood Tray (107455-R01), which appears to be the current
production light design. The plan treats Wood Tray = light family (logged as assumption A-1).

## 2. NetSuite purchased costs (queried 2026-06-10)

| Item | Description | Avg cost | Last purchase |
|---|---|---|---|
| 106900-R02 | WELDMENT, HEAVY TRAY | $5,221.32 | $5,221.32 |
| 106900-R03 | WELDMENT, HEAVY TRAY | — (no PO yet) | $0 |
| 106901-R01 | ASSEMBLY, HEAVY TRAY | $7,449.61 | $7,452.20 |
| 106901-R02 | ASSEMBLY, HEAVY TRAY | $5,997.92 | $2,618.23 (anomalous — likely partial) |
| 106911-R01 | WELDMENT, LEG, HEAVY TRAY | $79.71 | $79.71 |
| 106997-R01 | ASSEMBLY, LIGHT TRAY | $6,593.75 | $6,593.75 |
| 107508-R02 | WELDMENT, LEG, SlipCarrier 6 (wood tray leg) | $122.71 | $122.71 |
| 107049-R02 | DECK 1, HEAVY TRAY, PAINTED, CENTER | $138.84 | $141.09 |
| 107305-R02 | DECK 3, HEAVY TRAY, PAINTED, RIGHT | $72.55 | $72.55 |
| 107563-R01 | DECK 4, HEAVY TRAY | $74.80 | $77.05 |
| 107178-R02 | BENT SHEET, LEG HOLE COVER | $28.32 | $28.32 |
| 107179-R02 | PLATE, LEG HOLE COVER | $12.46 | $8.95 |
| 107084-R01 | TAILHOOK GRABBER, BENT, TRAY | $12.04 | $12.04 |
| 100235-R00 | FRONT/BACK EDGE GUARD | $35.76 | $40.51 |
| 107457/58/59/60-R01 | WOOD TRAY BRACKETS (all four) | $29.16 each | $29.16 |
| 107578-R01 | TAILHOOK GRABBER, BENT, WOOD TRAY | $29.16 | $29.16 |
| 107581-R01 | PLATE, LEG HOLE COVER, WOOD TRAY | $29.16 | $29.16 |
| 107582-R01 | BENT SHEET, LEG HOLE COVER, WOOD TRAY | $29.16 | $29.16 |
| 107350-R01 / 107456-R01 | BEAM 1 / BEAM 2, WOOD TRAY | — missing | — missing |
| 107565..107569-R01 | WOOD DECKS 1–5 | $153.36 / $85.94 / $88.75 / $38.07 / $20.92 | same |
| 106158-R01 | EDGE EXTENSION, ALUMINUM, TRAY | $212.00 | (BoM metrics PDF) |
| 101450-R01 | DeckOver Paint (per tray kit) | $213.00 | (BoM metrics PDF) |

Data quality flags: the uniform $29.16 across all wood-tray steel piece parts looks like a
placeholder/flat quote, not a real should-cost; wood beam prices are missing entirely;
106901-R02 last-purchase of $2,618.23 contradicts its $5,997.92 average.

## 3. Heavy Tray weldment 106900-R03 (from drawing PDF)

Total weldment weight: **1,178.672 lbs**. Finish: **powder coat RAL 9003 signal white, gloss**.
Weld spec: MIG/laser with ER70S-6 or ER70S-3 filler (or TIG ER70S-2); default fillet
0.25" ± 0.125"; all square/rect tube welded all-around at all joints; quarter symmetry;
tube fit-up into cut-outs locates members (i.e., tubes carry laser/plasma-cut slots).

Parts list (item, material, unit weight, qty):

| # | P/N | Title | Material | Unit lb | Qty | Ext lb |
|---|---|---|---|---|---|---|
| 1 | 106892 | BEAM 1 | A500 rect tube 6×3×0.125 | 112.707 | 2 | 225.4 |
| 2 | 106893 | BEAM 2 | A500 6×3×0.125 | 95.761 | 2 | 191.5 |
| 3 | 106894 | BEAM 3 | A500 4×2×0.125 | 29.456 | 8 | 235.6 |
| 4 | 106895 | BEAM 4 | A500 5×2×0.125 | 37.881 | 4 | 151.5 |
| 5 | 106896 | BEAM 5 | A500 6×3×0.125 | 41.366 | 2 | 82.7 |
| 6 | 106897 | BEAM 6 | A500 6×3×0.125 | 43.968 | 2 | 87.9 |
| 7 | 106898 | BEAM 7 | A500 4×2×0.125 | 6.298 | 4 | 25.2 |
| 8 | 106917 | PLATE, LIFTING INTERFACE | A36/CS-B 0.25" | 20.561 | 2 | 41.1 |
| 9 | 106919 | PLATE, BEAM REINFORCEMENT | A36 0.25" | 4.675 | 4 | 18.7 |
| 10 | 106920 | PLATE, FOOT MOUNTING | A36 0.25" | 11.192 | 4 | 44.8 |
| 11/12 | 106921/22 | PLATE, COSMETIC L/R | A36 0.105", formed | 3.462 | 2+2 | 13.8 |
| 13 | 106918 | PLATE, CENTER REINFORCEMENT | A36 0.105" | 54.299 | 2 | 108.6 |
| 14 | 106952 | TAB, DECK SUPPORT | A36 0.25" | 0.427 | 8 | 3.4 |
| 15 | 107046 | BEAM 9 | A500 4×2×0.125 | 6.918 | 1 | 6.9 |
| 16 | 107290 | SUPPORT, BENT, DECK CENTER | A36 0.105", formed | 0.895 | 6 | 5.4 |
| 17 | 107562 | PLATE, FOOT MOUNTING, 90° | plain carbon 0.25" | 11.139 | 4 | 44.6 |

Tube content ≈ 1,007 lb (25 pieces); plate/sheet content ≈ 181 lb (28 pieces). Component
sum ≈ 1,287 lb vs. 1,179 lb drawing total — the drawing CAD weight governs; the delta is
treated as quantity/rev noise (logged, issue I-21). Beam 1 at 112.7 lb of ~7.3 lb/ft tube
implies ~15.4 ft — the tray is roughly 15.5 ft long; longest stock need is 24-ft tube.

Revision history shows R01 (01/2026) → R02 (03/2026) → R03 (04/2026): active design churn.

## 4. Wood Tray 107455-R01 steel content (from BoM)

Steel fab parts: 2× BEAM 1 (107350, tube), 2× BEAM 2 (107456), 12 brackets
(107457×2, 107458×6, 107459×2, 107460×2), 8× tailhook grabber, 10× leg-hole plate,
6× bent sheet, 6× leg weldment 107508 (purchased today at $122.71). Decking is SPF
lumber (2×4s, wood deck panels) fastened with 648 deck screws — assembly scope, not steel fab.
No weights on hand for wood-tray steel; estimated total ≈ 450 lb/tray (assumption A-7).

## 5. Candidate facility (from repo: "1275 Oakbrook Drive — Decision Analysis")

1275 Oakbrook Drive (Norcross, GA): 43,790 SF leasable, base rent $7.50/SF, NNN est.
$2.50/SF, TI $10/SF amortized 3 yrs, 3-yr term modeled. Fab would occupy a portion of
this building alongside existing operations.

## 6. Current purchased fab-scope spend (buy baseline)

Heavy Tray steel-fab content per tray (buy): weldment $5,221.32 + 4 legs $318.84 +
decks $587.36 (2×$136.59 + 2×$84.54 + 2×$72.55, per BoM metrics) + bent sheets $138.32 +
plates $99.64 + tailhooks $96.28 + edge guards $81.02 = **$6,542.78**.

Wood Tray steel-fab content per tray (buy, partly estimated): 6 legs $736.26 + brackets
$349.92 + tailhooks $233.28 + plates $291.60 + bent sheets $174.96 + beams est. $740 (A-8)
+ RFID holder est. $60 = **≈ $2,586**.

Annual buy baseline at plan volume: 240 × $6,543 + 120 × $2,586 ≈ **$1.88M/yr** of
addressable fabricated-steel spend.

> Superseded by §7 (Loops 26–32): current weldment price is $5,577.84 → heavy fab-scope
> ≈ $6,899/tray and the baseline ≈ **$1.97M/yr**.

---

# Sections 7–10 added by Loops 26–31 (evidence phase)

## 7. Actual purchase-order history (NetSuite, queried 2026-06-10)

| PO | Date | Vendor | Item | Qty | Unit price |
|---|---|---|---|---|---|
| PO10108 | 3/13/2026 | Steel Materials, Inc. | 106911-R01 heavy leg | 68 | $79.71 |
| PO10118 | 3/16/2026 | TEEMS Fabrication | 106900-R02 weldment | 28 | $5,221.32 |
| PO10120 | 3/16/2026 | Starflex Fabrication | 107508-R02 wood leg | 18 | $122.71 |
| PO10191 | 4/6/2026 | Steel Materials, Inc. | 106911-R01 | 48 | $79.71 |
| PO10264 | 5/4/2026 | Steel Materials, Inc. | 106911-R01 | 50 | $79.71 |
| PO10280 | 5/11/2026 | TEEMS Fabrication | 106900-R03 weldment | 9 | **$5,868.33** |
| PO10309 | 5/19/2026 | TEEMS Fabrication | 106900-R03 weldment | 33 | **$5,577.84** |

Findings: heavy weldments are **single-sourced to TEEMS**; the R02→R03 revision repriced
at **+12.4%** initially, settling at **+6.8%** ($5,577.84 = current price of record);
weldment buy rate Mar–May ≈ 70 units / 10 weeks ≈ 28/mo ordered.

## 8. Receipt cadence and lead time (PO10118, 28 units)

Receipts: 4/6 (5), 4/10 (5), 4/17 (6), 4/24 (6), 4/30 (6) → PO-to-first-delivery
**3.0 weeks**, PO-to-last **6.5 weeks**; TEEMS demonstrated throughput **≈ 5–6
weldments/week (~24–26/mo)** — near parity with current demand, i.e., the buy path has
little headroom for growth without qualifying a second vendor.

## 9. Demand evidence (work orders, Mar–Jul 2026)

Heavy tray (106901) work orders run a steady **5/week (≈21–22/month)**, released and
scheduled through **7/27/2026**, with surge weeks of 9–10 (w/o 4/27, 6/29) and a 14-unit
customer-site batch (Denton, TX, 5/20). Weldment consumption mixes R01/R02/R03 stock.
Wood tray (107455): **3 work orders total (3/9/2026)**; wood beams never purchased —
the 10/mo wood volume is a ramp target, not a run rate.

## 10. External market benchmarks (June 2026 searches)

- **Atlanta welder wages:** average $22.76–24.64/hr (ZipRecruiter Feb 2026; Indeed);
  Georgia median ≈ $22.08/hr (BLS OEWS 51-4121, 2024). Plan band $24–29 ≈ 60th–85th
  percentile — validated. Sources: [BLS OEWS 51-4121](https://www.bls.gov/oes/2023/may/oes514121.htm),
  [Indeed Atlanta welder salaries](https://www.indeed.com/career/welder/salaries/Atlanta--GA),
  [ZipRecruiter Atlanta welder](https://www.ziprecruiter.com/Salaries/Welder-Salary-in-Atlanta,GA).
- **A500 Gr B rectangular tube, service-center pricing (Mar 2026):** 2×4×⅛ $0.85–0.92/lb;
  2×6×⅛ $0.93–1.00/lb → model uses **$0.90/lb** (supersedes the $0.72/lb assumption;
  A36 sheet/plate rebased to $0.74/lb). Sources:
  [Material Price Book 2×6×⅛](https://www.materialpricebook.com/prices/steel/a500-gr-b/rectangular-tube/2x6x0.125),
  [Material Price Book 2×4×⅛](https://www.materialpricebook.com/prices/steel/a500-gr-b/rectangular-tube/2x4x0.125),
  [Totten Tubes A500](https://www.tottentubes.com/structural-a500-rectangular-tubing).
