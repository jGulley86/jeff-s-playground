# Building an Integrated Production Scheduler for Discrete Manufacturing

*A research-backed engineering guide — how inventory levels and raw-material lead times feed a
BOM-driven, capacity-aware schedule, how to model the cost-vs-lead-time tradeoff (multi-sourcing,
expediting, air-vs-ocean freight), how to answer make-to-order "can I hit this date?" quotes, and
how to build it in-house pulling data from NetSuite.*

> **Method & confidence note.** This guide was produced with a multi-agent deep-research pass
> (fan-out web search → claim extraction → adversarial cross-check → synthesis). Many sources
> blocked automated full-page fetching during research, so a number of claims rest on
> search-result extracts rather than verbatim reads. The core operations-management mechanics
> (MRP gross-to-net, lead-time offsetting, safety-stock/ROP/EOQ, the MPS→MRP→scheduling hierarchy)
> and the OR-Tools CP-SAT modeling patterns are mutually corroborated and/or fetched verbatim —
> **high confidence**. Items explicitly flagged *illustrative* (e.g. vendor benchmark percentages,
> freight cost multipliers) are directional, not audited. All **NetSuite** internal IDs / field
> names / numeric limits came from search snippets and must be verified against your account's
> Records Browser and the live REST metadata-catalog before coding.

---

## 0. The mental model (read this first)

There are **two coupled problems**, and conflating them is the #1 design mistake:

1. **Material planning — "do I have the stuff?"** Given demand and a BOM, work out *what* to
   make/buy and *when to release* each order so parts arrive in time. This is **MRP**. It is
   fundamentally about **time-phasing and lead-time offsetting**.
2. **Capacity scheduling — "can the shop actually do it, and in what order?"** Given finite
   machines/labor, sequence operations to hit dates. This is **finite-capacity scheduling / APS**,
   and it's a hard combinatorial optimization problem.

Classic MRP solves (1) and *assumes infinite capacity* — it will happily load 40 hours onto an
8-hour day [usersolutions.com/blog/finite-vs-infinite-capacity-scheduling]. **Advanced Planning &
Scheduling (APS)** optimizes materials *and* capacity simultaneously into one constraint-based
plan, rather than MRP's two-step material-then-capacity sequence
[sap.com/resources/what-is-material-resource-planning-mrp]. Your "integrated scheduler" is
essentially a small APS engine sitting on top of MRP logic — extended with **cost-aware sourcing**
(§7) and **order promising** (§8).

---

## 1. The planning frameworks and how they layer

The standard hierarchy, top to bottom [Springer 10.1007/978-3-030-72331-6_12; arkieva.com]:

| Layer | Horizon (typical) | Granularity | Question answered |
|---|---|---|---|
| **S&OP / IBP** | 2–3 years | product family | volume & mix |
| **MPS** (Master Production Schedule) | 6–12 months | finished SKU | what to build, when, how many |
| **MRP** (Material Requirements Planning) | 3–18 months | component/raw material | what to order/make & when to release |
| **Finite scheduling / shop floor control** | days–weeks | operation on a machine | exact sequence & timing |

- **MPS** is the anticipated build schedule — items in specific configs, quantities, dates — and it
  is *the input that drives MRP* [APICS instructor materials, apics.org].
- **MRP** uses BOM data, inventory data, and the MPS to calculate material requirements and
  recommend releasing (and *rescheduling*) replenishment orders [APICS]. Because it's time-phased,
  it flags open orders whose due dates are out of phase with need dates, not just new orders [APICS].
- **APS** evaluates all resources (machines, labor, tools, materials, sequencing rules) at once
  using mathematical optimization, where conventional planning passes output layer-to-layer with
  limited feedback [dualis-it.de].

**Capacity validation sits beside this:** *Rough-Cut Capacity Planning (RCCP)* sanity-checks the MPS
against key resources at an aggregate level *before* MRP; *Capacity Requirements Planning (CRP)*
loads the detailed MRP-generated orders against work-center hours [imperiascm.com]. **Closed-loop
MRP** is MRP + RCCP/CRP + feedback of actual shop/vendor performance back into planning
[usersolutions.com].

**Time buckets & horizon:** MRP is built on discrete time buckets — historically weekly,
increasingly daily [ifm.eng.cam.ac.uk; Oracle MRP docs]. **Critically, the planning horizon must be
at least as long as the *cumulative lead time* of your deepest BOM path** (see §4), which is why
horizons run 3–18 months [oliverwight-americas.com; fsm.how].

> ⚠️ *Illustrative figure:* one vendor claims infinite-capacity planning yields ~60–75% on-time
> delivery and 25–40% higher WIP [usersolutions.com]. Directionally plausible, not independently
> audited — don't quote it as fact.

---

## 2. The data model (master data you must build first)

This is the foundation. "Garbage in, garbage out" is the canonical MRP failure: wrong inventory,
BOM, or MPS data ⇒ wrong output [en-academic.com MRP]. SAP's four core PP master-data objects are a
good template: **material master, BOM, routing, work center** [tutorialspoint SAP PP].

**Core entities and how they relate:**

```
Item (material master)
 ├─ planning attrs: make/buy, lead_time, lot_size_rule, safety_stock, reorder_point, demand_type(indep/dep)
 ├─ BOM (parent → children, qty per, multi-level / indented)
 ├─ Routing (ordered Operations)
 │     └─ Operation → Work Center (+ setup_time, run_time/unit, queue/wait/move time)
 ├─ Inventory record (on-hand, by lot/location, allocations, quality status)
 └─ Supplier(s) (lead_time, MOQ, price breaks)

PurchaseOrder line → scheduled receipt (qty, due date)  → nets against requirements
WorkOrder        → scheduled receipt for made items
```

Key facts to encode correctly:

- **BOM** is a hierarchical, version-controlled structure; multi-level/indented BOMs repeat
  parent→child for self-produced subassemblies [netsuite.com]. **Explosion** breaks a finished
  product into all components across all levels [cofactr.com]. Line fields: part #, revision, qty,
  UoM, make/buy, alternates, lifecycle state [cofactr.com].
- **Routing** defines the *sequence of operations*, *where* (work center) and the *times*, and is
  defined after the BOM [Oracle JD Edwards docs]. **Number operations in increments of 10**
  (10, 20, 30…) so you can insert later without renumbering [Oracle].
- **Operation time elements** (SAP S/4HANA model): queue, setup, processing, teardown, wait, move.
  Operation lead time = sum of all except move [learning.sap.com]. **Setup time is fixed per order;
  run time is per unit × order qty** — that product is the work-center capacity load
  [olofsimren.com]. **Queue time doesn't consume capacity but can be >90% of actual shop lead time**
  [olofsimren.com] — a huge, counterintuitive driver of real lead time.
- **Independent vs dependent demand:** independent = sold items (forecast-driven); dependent =
  derived from parent BOMs [32soft.com]. This distinction decides *what gets a forecast/ROP vs what
  gets exploded from MRP*.
- **Scheduled receipts** = open orders placed before the first bucket, not yet delivered, expected
  in a specific period [APICS-aligned; Oracle]. MRP nets demand against on-hand + scheduled receipts
  + open POs [brahmin-solutions.com].
- **Lot-sizing rules per item:** Lot-for-Lot, Fixed Order Quantity, Period Order Quantity, EOQ
  [usersolutions.com].

---

## 3. The scheduling / optimization algorithms

Pick by problem size and how much "optimality" actually matters. The relevant problem classes —
**job shop, flow shop, flexible job shop, parallel machines** — are **NP-hard**; minimizing total
(weighted) tardiness is NP-hard, and permutation flow-shop makespan is *strongly* NP-hard for ≥3
machines (Garey–Johnson–Sethi) [researchgate 356971184; rairo-ro.org]. So exact optimization
doesn't scale indefinitely; you trade optimality for speed.

**The toolbox, weakest→strongest (and slowest):**

1. **Dispatching / priority rules** — O(n log n), instant, no global optimization:
   - **SPT** (shortest processing time) → minimizes mean flow time [researchgate 356971184].
   - **EDD** (earliest due date) → minimizes maximum lateness/tardiness [researchgate 356971184].
   - **Johnson's rule** is *optimal* for the 2-machine flow shop makespan, O(n log n)
     [sciencedirect S0925527309001078] — but not for 3+ machines.
   - *Use for:* real-time dispatch, very large shops, or as a fast warm-start / fallback.
2. **Constraint Programming (CP / CP-SAT)** — the sweet spot for discrete scheduling. Finds good
   solutions for **small *and* large** instances and guarantees hard-constraint satisfaction, making
   it more practical than MILP as size grows [sciencedirect S0360835220300814].
3. **MILP / MIP** — solves small instances *to proven optimality* but has serious scalability limits
   on large ones [mdpi 13/10/6003].
4. **Metaheuristics** — genetic algorithms, simulated annealing, tabu search (often hybridized) are
   the principal approaches for the flexible job shop [ijcaonline 7348-0283]. Scale well, no
   optimality guarantee.
5. **Discrete-event simulation** — validate a schedule against stochastic reality; not an optimizer.

**Objective functions** to expose as configurable: makespan, total/weighted tardiness, lateness,
throughput, setup minimization [researchgate 356971184].

**Recommendation: start with CP-SAT (Google OR-Tools).** It's a constraint solver on a
clause-learning SAT base with Boolean/integer/**interval** variables and scheduling constraints
[Perron CMU slides]; it swept all gold medals in the 2024 MiniZinc Challenge and has medaled since
2017 [minizinc.org/challenge/2024]. The scheduling primitives map directly onto shop scheduling:

- **Interval variables**: `start + size == end` [OR-Tools scheduling.md].
- **`NoOverlap`**: a machine does one task at a time [OR-Tools].
- **`Cumulative`**: at any instant, sum of active task demands ≤ capacity — models a work center
  with N parallel units or a labor pool [OR-Tools].
- **Optional intervals** (presence literal): for machine-choice / alternatives; `NoOverlap`/
  `Cumulative` ignore absent intervals [OR-Tools].
- **Precedence** = linear inequalities on start/end [OR-Tools].
- Caveat: CP-SAT is **discrete only** — no continuous/fractional variables [mbrenndoerfer.com].
  Model time in integer minutes/buckets. OR-Tools ships a `flexible_job_shop_sat.py` example
  [github.com/google/or-tools].

---

## 4. How inventory & raw-material lead times feed and constrain the schedule

This is the heart of the "integrated" requirement. Two mechanisms: **(A) MRP time-phasing** decides
*when material must be ordered/available*, and **(B) material availability becomes a hard
constraint** on when production can be scheduled.

### A. MRP gross-to-net + lead-time offsetting (the core algorithm)

For each item, per time bucket:

```
Gross Requirements   = independent demand (forecast/orders) + dependent demand (from parent BOM)
Net Requirements     = Gross Requirements − Scheduled Receipts − Projected On-Hand + Safety Stock
Projected On-Hand[t] = On-Hand[t-1] + Scheduled Receipts + Planned Order Receipts − Gross Requirements
```

A **planned order receipt** is generated in any bucket where projected available balance would drop
below safety stock; its quantity comes from the lot-sizing rule [brahmin-solutions.com;
usersolutions.com; cleverence.com]. Then the key step:

> **Planned Order Release = Planned Order Receipt shifted earlier by the item's lead time**
> (lead-time offsetting / back-scheduling) [metricgate.com].
> Example: component needed day 100, 15-day lead time ⇒ release/order on **day 85** [fsm.how].

You run this **backward through the entire BOM** from the finished-good due date, applying each
level's lead time and dependencies [learning.sap.com]. For **purchased raw materials**, the "lead
time" is the **supplier procurement lead time** — that's exactly where the purchasing lead-time
input enters: it sets how far ahead a *planned purchase order* must be released to have material on
hand when production needs it.

**Cumulative (critical-path) lead time** = the longest summed-lead-time path through the BOM
[oliverwight-americas.com]. This is the true "how far ahead must I commit" number and **must fit
inside the planning horizon** [fsm.how].

### B. Inventory levels as a scheduling constraint

- In **MRP**, material availability is *assumed*. In **APS**, material availability is an
  **explicit constraint**: an operation can't be scheduled until a supply due date for its materials
  is established [Oracle MRP/SCP docs]. **Capable-to-Promise (CTP)** extends Available-to-Promise
  (ATP) by checking *both* material and capacity [Oracle].
- Practically: in the CP-SAT model, an operation's **earliest start** = max(predecessor finish,
  **material-available date**). The material-available date comes from current on-hand or from a
  scheduled/planned receipt date. This is how raw-material inventory + supplier lead time *directly
  bound* the schedule.

### C. The buffers against uncertainty (formulas)

- **Safety stock (demand varies, fixed LT):** `SS = Z · σ_D · √LT` [supplychainmath.com].
- **Safety stock (both vary):** `SS = Z · √(LT · σ_D² + D² · σ_L²)` — note `σ_L` (lead-time stdev)
  [supplychainmath.com].
- **Safety stock (only LT varies):** `SS = Z · σ_L · μ_D` [firgelliauto.com].
- **Service-level Z:** 1.28 (90%), 1.65 (95%), 1.96 (97.5%), 2.33 (99%) [netstock.com].
- **Reorder point:** `ROP = D_avg · LT_avg + SS` [firgelliauto.com].
- **EOQ (Wilson):** `Q* = √(2DS/H)` — D = annual demand, S = order/setup cost, H = holding cost/unit/yr;
  assumes constant known demand, constant LT, no price breaks, instantaneous receipt
  [mrpeasy.com; geeksforgeeks].
- **Cycle service level** (prob. of no stockout per cycle) vs **fill rate** (fraction of demand met
  from stock) differ; 95% cycle service often ⇒ 99%+ fill rate [APICS fill-rate PDF].

> **Lead-time variability matters more than people expect.** The `D² · σ_L²` term in the combined
> formula often dominates — variability in *supplier lead time* drives safety stock harder than
> demand variability. Capture `σ_L` per supplier, not just a mean lead time.

---

## 5. Reference architecture & build approach (in-house)

**Pattern: separate the system of record from the planning engine** — "ERP + specialist APS." The
transactional store (ERP/inventory/DB) holds master data and production orders; a separate engine
reads it, optimizes, and writes the plan back [usersolutions.com erp-scheduling-add-on-guide]. This
is also how the leading open-source APS, **frePPLe**, integrates with Odoo: Odoo owns all master
data/transactions, a connector syncs to frePPLe, which plans and pushes back [github.com/frePPLe
features.rst].

```
┌─────────────────────────────────────────────────────────────┐
│ System of record (NetSuite / Postgres)                       │
│  items, BOMs, routings, work centers, inventory, POs, vendors│
└───────────────┬───────────────────────────▲──────────────────┘
                │ extract (SuiteQL/ETL)      │ write back plan
                ▼                            │
┌─────────────────────────────┐   ┌──────────┴───────────────┐
│ Planning engine             │   │ Plan store / UI          │
│ 1. MRP: gross-to-net,       │──▶│ planned orders, Gantt,   │
│    BOM explosion, LT offset │   │ promise dates, exceptions│
│ 2. Scheduler: CP-SAT model  │   └──────────────────────────┘
│    (intervals, NoOverlap,   │
│     Cumulative, mat. date)  │
│ 3. Cost-aware sourcing (§7) │
│ 4. Order promising (§8)     │
└─────────────────────────────┘
```

**Build sequence (incremental, each step shippable):**

1. **Data model + ingestion** (Postgres + NetSuite extract, §9). Get inventory-record accuracy and
   BOM accuracy *first* — everything downstream depends on it.
2. **MRP engine** (pure code, no solver): BOM explosion → gross-to-net → lead-time offset → planned
   orders. Deterministic, fast, easy to test.
3. **Capacity scheduler** (OR-Tools CP-SAT): take MRP's planned work orders, model operations as
   intervals on work centers, add material-available dates as earliest-start bounds, optimize for
   tardiness/makespan. Start unconstrained, then turn on finite capacity.
4. **Cost-aware sourcing + order promising** (§7–8).
5. **Replanning loop + UI**: exceptions, Gantt, what-if.

**Build-vs-reuse for the engine:**
- **Google OR-Tools (CP-SAT)** — scheduler core; Apache-licensed, battle-tested.
- **frePPLe** — open-source APS that *already* does MRP + finite-capacity scheduling + forecasting,
  producing both unconstrained and fully-constrained plans [github.com/frePPLe]. **Evaluate before
  building from scratch** — it may be 80% of what you want.
- **Timefold** (Apache-2.0; OptaPlanner successor) — Java/Kotlin metaheuristic solver with built-in
  Job Shop Scheduling [github.com/TimefoldAI].
- **Pyomo** — BSD Python modeling layer if you go the MILP route (CBC/GLPK/Gurobi).

**Replanning cadence:** *regenerative MRP* replans everything; *net-change MRP* replans only items
with activity since last run, enabling daily/sub-daily runs [archerpoint.com; docs.infor.com].
**Recommendation:** nightly regenerative baseline + intraday net-change for disturbances + rolling
horizon (commit only the near-term, re-plan as forecasts update) [arXiv 2402.14506].

---

## 6. Pitfalls & handling uncertainty

1. **GIGO / data accuracy.** Wrong inventory, BOM, or MPS ⇒ wrong plan [en-academic.com]. Budget for
   cycle-counting and BOM governance.
2. **Infinite-capacity blindness.** Traditional MRP plans materials ignoring capacity
   [cleverence.com; sap.com]. The finite scheduler (§3) is the fix.
3. **Fixed lead times that ignore load.** MRP assumes fixed planned lead times, but flow time is
   highly variable and *nonlinearly* related to utilization (queueing theory)
   [sciencedirect S0925527315001656]. Recall queue time can be >90% of actual lead time.
4. **MRP / schedule nervousness.** Small demand changes ripple into large schedule churn until
   planners stop trusting the system [usersolutions.com]. Mitigations:
   - **Time fences**: frozen zone → "slushy" negotiated zone → liquid zone [amgimanagement.com].
     Oracle implements planning/demand/release time fences [Oracle MRP docs].
   - **Freezing the MPS** is an evidence-backed nervousness reducer [Univ. Houston working paper].
   - **Dampening strategies** are studied/quantified [Management Science 32(4):413].
5. **Uncertainty: safety stock vs safety time.** Safety *time* is preferable when you can forecast
   shipments over the lead time well; otherwise safety *stock* is more robust
   [Management Science 40(12):1678].
6. **Deterministic vs stochastic planning.** Deterministic + safety stock works at *low* utilization;
   at *high* utilization, stochastic optimization gives more robust plans [arXiv 2402.14506].

---

## 7. Modeling the cost ↔ lead-time tradeoff (sourcing, expediting, freight)

Lead time isn't a fixed number per material — it's a **menu of (supplier, freight mode, expedite
level) options, each with a cost and a transit time**. The model picks the cheapest combination that
still hits the date, and tells you cleanly when *no* combination can.

### 7.1 The key shift: lead time becomes a decision variable

Instead of `material.lead_time = 84 days`, model **sourcing modes** per material:

| Material | Mode | Supplier | Cost/unit | Lead time | Capacity/MOQ |
|---|---|---|---|---|---|
| Alloy-X | A1 | Vendor A, ocean | $100 | 84 d | cap 500 / MOQ 50 |
| Alloy-X | A2 | Vendor A, **air** | $140 | 21 d | cap 500 / MOQ 50 |
| Alloy-X | B1 | Vendor B (premium) | $185 | 35 d | cap 80 / MOQ 10 |

This unifies the three real cases:
- **"Pay more for shorter lead time from same supplier"** → modes A1 vs A2 (freight upgrade / crash).
- **"Different supplier, more money"** → mode B1.
- **"Single supplier, backlogged, genuinely can't go faster"** → only A1 exists, capacity exhausted
  ⇒ **hard infeasible** (§7.6).

### 7.2 Supplier selection / order allocation (MILP)

Multi-sourcing with per-supplier price, lead time, MOQ, capacity is a standard **MILP** minimizing
total procurement cost subject to capacity/quality [matec-conferences.org;
sciencedirect S0307904X1100713X]:

- Binary **mode-selection** `y_{i,m} ∈ {0,1}`, `Σ_m y_{i,m} = 1` per material *i*.
- MOQ/capacity bounds: `MOQ_s · y_s ≤ q_s ≤ capacity_s · y_s`.
- **Single vs multi-sourcing is itself a tradeoff:** single sourcing optimal mainly when one
  supplier's capacity dwarfs demand; otherwise multi-sourcing wins on delivery assurance & volume
  flexibility [sciencedirect S037722170600587X]. MOQ interacts non-intuitively with cost *and*
  reliability [same].

### 7.3 Expediting / "crashing" as a continuous decision

The classic **time-cost tradeoff (crashing)** — with a linear cost-vs-duration relation it's an LP
[Beasley OR notes, Brunel]:

- **Crash-cost slope** = `(Crash cost − Normal cost) / (Normal time − Crash time)` = $/day saved.
  *Example: 20 d/$10,000 → 14 d/$16,800 = $1,133/day, max 6 days crashable* [slm.mba].
- Precedence with crash var *c*: `start_succ ≥ start_pred + dur − c`, bounded
  `0 ≤ c ≤ (normal − crash_time)` [Beasley].
- Rule: crash the lowest-slope activity **on the current critical path** first [solvermax.com].

### 7.4 Freight mode (air vs ocean) as discrete choice

Mode selection = MILP with a weighted objective jointly minimizing freight cost & lead time
[sciencedirect S2092521226000106], or a discrete-choice (logit) model with cost and transit time as
the two dominant criteria [frontiersin.org].

> *Calibrate with real lane data:* air ≈ **8–16× per-kg cost** of ocean [freightos.com], buying a
> transit drop from ~2–8 weeks (ocean) to ~1–5 days (air) [exfreight.com]. Ranges, not constants.

### 7.5 The objective function that ties it together

```
minimize  Σ material/purchasing cost (chosen supplier × qty)
        + Σ freight/mode cost + expedite/crash premium
        + Σ wⱼ · Tⱼ                      ← tardiness penalty, Tⱼ = max(0, Cⱼ − dⱼ)

subject to: demand satisfaction
            MOQ_s·y_s ≤ q_s ≤ cap_s·y_s        (supplier bounds)
            Σ_m y_{i,m} = 1                     (exactly one mode/supplier per material)
            start_succ ≥ start_pred + dur − crash;  0 ≤ crash ≤ normal − crash_time
            finite work-center capacity (§3)
            Tⱼ ≤ T_max                          (HARD cap → §7.6)
```

The **expedite-vs-late logic falls out naturally**: the solver pays the freight/crash premium only
when doing so avoids a larger tardiness penalty `wⱼ·Tⱼ` — i.e., expedite exactly when the avoided
lateness cost exceeds the premium [gettransport.com; researchgate 227505381].

### 7.6 "Impossible date" vs "expensive date" (the single-supplier case)

Handled cleanly with the **hard vs soft constraint** distinction [slpscheduler.com]:

- **Soft (feasible-but-expensive):** lateness/expedite penalized via **big-M** `M·v`; solver always
  returns a solution, just costlier, reporting *"yes, but +$X via air / Vendor B"* [gams.com EMP].
- **Hard (infeasible):** a `T_max` cap or exhausted supplier capacity with no alternative ⇒ solver
  returns **infeasible** = *"no, you physically cannot get Alloy-X before week N"* [slpscheduler.com].

A quote engine runs the model and reads the result: feasible + low cost → promise normally;
feasible + high cost → promise *with* the surcharge; infeasible → decline and report the binding
constraint.

### 7.7 How to implement in OR-Tools CP-SAT (verified, copyable)

The load-bearing, verbatim-fetched part [OR-Tools scheduling.md; CP-SAT Primer]:

- One **optional interval per alternative** mode/supplier, sharing the task's start:
  `new_optional_interval_var(start, size, end, presence_literal, name)`. `NoOverlap`/`Cumulative`
  automatically ignore absent intervals.
- Force one choice: `model.add_exactly_one(presence_literals)`.
- Each alternative carries its own `size` (= that mode's lead time) and contributes its cost via its
  presence literal.
- Supplier/work-center capacity over time: `add_cumulative(intervals, demands, capacity)`.

Supplier choice, freight-mode choice, and crash-vs-normal are all the *same* "alternative optional
interval" pattern.

---

## 8. Order promising for make-to-order ("can I hit this rush date?")

The build-to-order rush-quote decision is the **ATP → CTP → PTP** progression.

### 8.1 The three levels

1. **ATP (Available-to-Promise)** — material only, infinite capacity.
   `ATP = on-hand + scheduled receipts − existing commitments` over the horizon
   [packsend; ETH Zurich opess.ethz.ch]. Fast; use first.
2. **CTP (Capable-to-Promise)** — adds **finite capacity**: earliest date the item can be
   *completed* given on-hand, capacity, **and transport times**, working backward and forward
   simultaneously, refusing to overload a work center [learn.microsoft.com CTP; usersolutions.com].
3. **PTP (Profitable-to-Promise)** — when multiple feasible options exist, pick the **lowest total
   fulfillment cost** (item + resource + transit) [Oracle Global Order Promising]. This is where
   §7's cost model plugs in: "*should* I, and at what margin?" [logility.com].

> If on-hand covers all demand, ATP and CTP return the same answer — run cheap ATP first, fall back
> to CTP only when stock is short [ETH Zurich].

### 8.2 The mechanism to implement: the sandbox "test plan"

How commercial APS engines answer a rush quote [Infor SyteLine docs lsm1454144402967]:

1. **Insert** the rush order into a *temporary copy* of the live plan.
2. **Pull-plan (backward)** from the requested due date. If every component fits between due date and
   today → feasible at the requested date.
3. If a component can't be pull-planned in that window, **push-plan (forward) from today** to find
   the ASAP date — never scheduling into the past [Infor].
4. Report **both** the achievable date *and which existing orders get displaced/delayed* so a planner
   (or the model) can decide [planettogether.com].

In your stack: re-run the §3 CP-SAT scheduler + §7 sourcing model on
`current_orders ∪ {rush_order}` and compare to the committed baseline.

### 8.3 The hard floor: cumulative lead time

No capacity solves a missing part. The **cumulative (critical-path) lead time** — the longest-summing
path through all BOM levels — is the floor on any promise when no expedite exists
[oliverwight-americas.com]. *99 available parts wait on the 1 missing item* [queenems.com]. §7's
expedite options *move* this floor, at a cost.

### 8.4 Accept/reject + rush pricing: the OR foundation

The decision "*should* I accept this rush order, and what should I charge?" is the **Order Acceptance
and Scheduling (OAS)** problem. Each job carries processing time, release date, due date, deadline,
revenue, and tardiness-penalty weight; the objective **maximizes total profit = Σ accepted revenue −
Σ weighted tardiness penalties** [sciencedirect S0925527310000514]. OAS is **NP-hard** (Slotnick &
Morton; Ghosh's FPTAS); the canonical survey is **Slotnick, "Order Acceptance and Scheduling: A
Taxonomy and Review," *EJOR* 212(1):1–11, 2011** [engagedscholarship.csuohio.edu] — frames
acceptance as revenue vs. (opportunity cost of capacity + tardiness penalty). NP-hard ⇒ expect
heuristics for large instances.

**Demand time fence:** inside it, forecast is dropped and only actual orders count; you can still
promise a rush order inside the fence *if* there's quantity ATP, but other schedule changes there
need senior approval [APICS Dictionary via apicsforum.com].

---

## 9. Pulling data from NetSuite

> **Sourcing caveat:** NetSuite/Oracle docs blocked automated fetching, so the record internal IDs,
> field names, and numeric limits below come from search snippets (many quoting Oracle docs).
> **Verify every internal ID and field against your account's Records Browser and the live REST
> metadata-catalog before coding.** Weakest claims are flagged.

### 9.1 Which API to use

NetSuite exposes three surfaces; **Oracle directs all new integrations to REST + OAuth 2.0**
[docs.oracle.com chapter_1540391670]:

| API | Use it for |
|---|---|
| **SuiteQL** (SQL over REST) | **Primary bulk-extraction path.** SQL `SELECT` POSTed to `/services/rest/query/v1/suiteql`, query in `q` body param; supports JOINs [section_157909186990; getknit.dev]. |
| **REST Record API** | Individual records; sublists inline with `?expandSubResources=true` [chapter_1540391670]. |
| **SuiteTalk SOAP** | Legacy — Oracle signaled **no new SOAP integrations as of 2027.1**; avoid for greenfield [medium/entech — *confirm in release notes*]. |

**Auth:** Token-Based Auth (TBA) or **OAuth 2.0** (preferred). TBA Token ID/Secret shown **once** at
creation, unrecoverable after [article_0605103340].

**Schema discovery:** hit the **metadata-catalog** at `/services/rest/record/v1/metadata-catalog`
(OpenAPI 3.0 / JSON Schema) for authoritative field names [section_1540810174].

### 9.2 The records you need to pull

| Planning concept | NetSuite record (internal ID) | Notes |
|---|---|---|
| Item / inventory item / assembly | item records | header-level planning fields live here |
| BOM | **BOM + BOM Revision** | *Advanced BoM* restructured these into separate customizable records; a BOM Revision is version-by-effective-date, 1:N under a BOM, no overlapping effective dates [section_1517399803] |
| Routing | `manufacturingrouting` | ordered operations by employee group; sublists for steps + component-per-operation [section_N3750659 — *verify ID*] |
| Work order | `workorder` | assembly qty to build + component qty required [section_N3697954 — *verify ID*] |
| Purchase order | PO record | open POs = scheduled receipts for §4 netting |
| Vendor / per-item vendor | `itemvendor` sublist on item | fields `vendor`, `preferredVendor`, `vendorCode`; needs **Multiple Vendors** feature [section_N3712676] |

### 9.3 Lead-time, safety-stock & the per-vendor gotcha

- On the item: **Lead Time** (avg days vendor-order→receipt), **Safety Stock**, **Preferred Stock
  Level**; Lead Time + Safety Stock auto-calculate the **Reorder Point** [section_1504284487]. Can be
  set **per location** [section_N2286205].
- ⚠️ **Important for this use case:** you can set a **Purchase Lead Time per vendor**, but reportedly
  NetSuite **aggregates lead times across an item's vendors for planning rather than fully
  independent per-vendor planning** [netsuiteprofessionals archive — *community-sourced, weakest
  claim, verify*]. **If true, this directly affects you:** NetSuite's native planning may not pick
  "Vendor B at higher cost for shorter lead time." Strong argument for pulling raw per-vendor data
  out and running your own §7 sourcing model. Capture per-vendor lead time + cost yourself.
- ⚠️ With **Multiple Locations** enabled, `quantityonhand`/`quantityavailable`/`quantityonorder` are
  **not** queryable on the item record in SuiteQL — read per-location quantities from the
  location-level table [oracle community 4473134 — *verify exact table name via metadata-catalog*].

### 9.4 Extraction pattern & governance

- **Incremental pulls** filtered on `lastmodifieddate` with `TO_DATE(...)`; for transaction lines
  filter `mainline='F'` (lines) vs `'T'` (header) [oracle community 4507689].
- SuiteQL caps at **100,000 results/query**; page with `limit`/`offset` + header `Prefer: transient`;
  beyond that use **SuiteAnalytics Connect** [section_157909186990 — *verify cap*].
- **Concurrency** governed at account level (base Service Tier 1 ≈ **15 concurrent**, +~10 per
  SuiteCloud Plus license); overage → HTTP **429** [section_1500275531 — *confirm tier numbers*].

### 9.5 Build vs. NetSuite-native

NetSuite **already ships** native supply/demand planning: MRP (Demand Planning module), a **Planning
Workbench**, and **Supply Allocation** [netsuite.com/.../mrp.shtml — *vendor marketing, verify
licensed features*]. Your external engine **replaces/augments** it. Justification for building
externally = exactly your requirement set: NetSuite native MRP assumes infinite capacity and (per
§9.3) likely won't do cost-vs-lead-time supplier selection, expedite/freight-mode optimization, or
CTP-style finite-capacity rush quoting.

**Recommended boundary:** NetSuite = system of record (master data, inventory, POs, work orders).
Your engine = pull via SuiteQL → run MRP + finite scheduling (§3–4) + cost-aware sourcing (§7) +
order promising (§8) → write planned orders / promise dates back via the REST Record API.

---

## Appendix A — Confidence summary

- **High (verbatim-fetched):** CP-SAT alternative-interval / `add_cumulative` / `add_exactly_one`
  modeling patterns (§3, §7.7); frePPLe/Timefold/Pyomo capabilities.
- **High (academic/standard):** MRP gross-to-net & lead-time offsetting (§4); safety-stock/ROP/EOQ
  formulas (§4C); OAS objective & NP-hardness + Slotnick 2011 (§8.4); ATP/CTP definitions (§8.1);
  supplier-selection MILP & crashing LP (§7.2–7.3); big-M soft constraints (§7.6).
- **Medium/illustrative:** horizon ranges; air-vs-ocean cost/time multipliers (calibrate to your
  lanes); profitable-to-promise behavior; vendor benchmark percentages.
- **Verify before coding:** all NetSuite internal IDs, field names, the 100k/concurrency limits, the
  per-vendor-lead-time aggregation behavior (§9.3 — weakest, most relevant to you), and the
  location-quantity table name.

## Appendix B — Primary sources worth re-pulling for a design doc

- Slotnick, S. A. (2011). *Order Acceptance and Scheduling: A Taxonomy and Review.* European Journal
  of Operational Research 212(1):1–11.
- *Management Science* 40(12):1678 — Safety Stock vs Safety Time in MRP.
- *Management Science* 32(4):413 — Strategies to Dampen Nervousness in MRP.
- *Int. J. Production Economics* S0925527315001656 — Optimizing planned lead times for MRP.
- Google OR-Tools scheduling docs + the CP-SAT Primer (d-krupke) — alternative-resource modeling.
- Oracle NetSuite REST/SuiteQL docs + your account's REST metadata-catalog — record/field schema.
