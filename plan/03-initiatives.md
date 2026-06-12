# 03 — H2 2026 Initiatives

Seven initiatives across three objectives. Every milestone is month-granularity with buffer held at the end of the chain, not padded into each step. Kill criteria are pre-decided so nobody has to be brave in November.

## Objective 1 — Cut Tray's bill of materials in half

### 1A. Should-cost and resourcing program — Owner: Anjana
The full Tray bill gets a should-cost, parts are ranked by cost leverage, and everything winnable through resourcing, volume agreements, and spec relaxation gets won.
- **July:** should-cost complete across the full bill; parts ranked; each part tagged *negotiate*, *resource*, *redesign*, or *fabricate in-house*.
- **August:** quotes out and negotiations running on the first wave.
- **September–October:** agreements signed on resourced parts; Lan transitions purchase orders; Marques qualifies new suppliers.
- **November:** buffer.
- **December:** every part of the bill covered by an executed path to its target cost.
- **Handoffs:** Anjana → Lan (agreements to purchase orders), Anjana → Marques (new-supplier qualification). Spec-relaxation requests go to Engineering through 1B's channel — one front door, not two.
- **Kill criteria:** any part where resourcing can't reach target by September moves to redesign (1B) or fabrication (3B) — no part stays in negotiation past September hoping.

### 1B. Redesign-to-cost with Engineering — Owner: Anjana
Engineering outside ops owns Tray's design. There is no separate integrator seat: the work runs as a standing Engineering–supply-chain collaboration, with Anjana accountable on the ops side — cost targets and design trade-offs live in one place.
- **July:** joint target-setting with Engineering; subsystems chosen from 1A's ranking; Engineering staffing committed in writing.
- **August–October:** design releases in monthly batches, each pre-signed by Marques at release rather than qualified after — quality is in the review, not behind it.
- **November:** production-intent Tray units built at the new cost; buffer for late releases.
- **December:** done means built units, not released drawings.
- **Handoffs:** Anjana ↔ Engineering (targets in, releases out), Engineering → Eric (build). Two handoffs; Marques embedded, not appended.
- **Kill criteria:** if Engineering hasn't staffed the program by end of August, Jeff escalates to Chris — this initiative cannot be willed into existence from inside ops. Any subsystem whose redesign saves less than its qualification cost gets dropped back to 1A.

## Objective 2 — Make every customer site a reference

### 2A. Installed-base health to zero watch-list — Owner: Rasheen
Every account reviewed, a watch list named honestly, every flagged site remediated — Tray's early units held to the same bar as the established product.
- **July:** account-by-account health review done; watch list named.
- **August–September:** remediation at every flagged site; Eric's manufacturing engineers supply product fixes; Marques runs root-cause on repeat field failures.
- **October:** watch list at zero; reference enablement (site visits, call list) live for the sales team.
- **November–December:** hold it there through peak season.
- **Handoffs:** Rasheen → Eric (product fixes), Rasheen → Marques (root-cause).
- **Kill criteria:** any account unrecoverable for product reasons gets an exit-or-replace decision by October — field capacity stops being spent on it indefinitely.

### 2B. Field service system, scope-frozen — Owner: Rasheen
The inherited rollout finishes, justified strictly by cost-to-serve and response time.
- **July:** scope freeze — every remaining feature justified by cost-to-serve or response time, or cut from H2.
- **August–September:** deployed to all field teams.
- **October:** legacy tools retired — running two systems is a cost increase, not a rollout.
- **November:** buffer.
- **Handoffs:** integrations stay inside Rasheen's org with vendor support, Rasheen → Gaby (service data into finance for cost-to-serve reporting).
- **Kill criteria:** any feature that misses the freeze gate stays cut until 2027 — no quiet scope return.

## Objective 3 — Stand up the Fabrication Organization

### 3C. Factory consolidation, redirected — Owner: Eric
The inherited move completes end of September, with the layout designed around the cheaper Tray build and reserved fabrication floor space — one disruption, not two.
- **July:** layout locked, including fab footprint and Tray line flow.
- **August–September:** move executed; production protected via build-ahead on customer-committed units.
- **September:** consolidated factory operating.
- **Kill criteria:** none — this is committed. Slippage past September triggers the risk response in 07, not debate.

### 3A. Make-versus-buy and the capital case — Owner: Eric
Fabrication scope is chosen by cost leverage, not by what's fun to own. Sheet metal, weldments, and machining are the candidate envelope; the part list comes from the analysis.
- **July:** make-versus-buy run on 1A's top-leverage parts.
- **August:** fabricated-part list and equipment list decided; capital case with payback to Jeff and Gaby; **long-lead equipment ordered by end of August** even if the part list is still settling at the edges — equipment lead time, not analysis, is the critical path.
- **Kill criteria:** if in-house doesn't beat buy by a margin that survives honest overhead allocation, the shop shrinks to the parts that clear the bar — or doesn't get built. The org exists to cut Tray cost, not to justify itself.

### 3B. Fabrication shop build-out — Owner: Eric
- **October:** equipment installed in the consolidated factory; fab team hired per 04-org.
- **November:** first parts off the line; Marques qualifies fab processes.
- **December:** the agreed part set shipping at or below target cost. Buffer is thin here by design — the kill criteria in 3A, not padding, protect this date.
- **Handoffs:** Eric → Marques (process qualification), Anjana → Eric (supplier transition on parts moving in-house).
- **Kill criteria:** any part the fab line can't hit cost or quality on by December reverts to its 1A supplier — no stranded parts.

## Dependency map

```
1A should-cost (Jul)
 ├─→ 1B subsystem selection (Jul) → Engineering releases (Aug–Oct) → built units (Nov–Dec)
 └─→ 3A make-vs-buy (Jul) → equipment order (Aug) ─┐
3C consolidation (Jul–Sep) ────────────────────────┴─→ 3B install (Oct) → parts at cost (Nov–Dec)
2A and 2B run parallel to everything above; they share Eric's engineers and Marques, not milestones.
```

**Critical path:** should-cost → make-versus-buy → equipment order → consolidated factory → install → parts at cost. The buffer protecting it is the August equipment-order date.

**Constraint candidates from load:**
- **Marques is on the critical path of four initiatives** (1A supplier qualification, 1B release sign-off, 2A root-cause, 3B process qualification). Quality is the plan's hidden constraint candidate — addressed in 04-org.
- **Anjana carries both of the largest cost levers** (1A and 1B) and feeds 3A. The cost engineer hire in 04-org is her relief valve; if that seat is empty past July, she is the constraint.
- **Eric carries the consolidation, the fabrication build, and product fixes for the installed base.** His manufacturing engineering bench is the watch item.
- **Engineering outside ops** gates the single largest cost lever and answers to neither Jeff nor this plan — the plan's biggest external dependency, escalation pre-agreed in 1B.
