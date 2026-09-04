import { test } from "node:test";
import assert from "node:assert/strict";
import { seedState, migrate, project, includedStages, demandByWeek, atpInfo, atp, iso, toDate, PRODUCTS, STAGES } from "../engine.js";

/* Projected deployable inventory rows from the 2026 Demand Forecast workbook
   (as carried in the previous mock). The engine must reproduce them exactly
   from on-hand + builds − committed deployments. */
const WB_SL = [0,1,2,1,3,5,7,5,1,3,5,7,9,9,8,8,10,12,14,13,15,17,19,20,22,22,23];
const WB_HT = [4,9,13,13,6,11,16,5,-3,7,17,27,37,31,22,22,22,22,22,6,6,6,6,6,6,-10,-10];
const WB_LT = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,-10,-10,-10,-10,-14,-14,-14,-14,-14,-14,-14,-14];

test("seed reproduces the workbook's deployable inventory rows", () => {
  const s = seedState();
  const stages = includedStages(s.params); // po, contract, negotiation, soft
  const { ending } = project(s, 0, stages);
  assert.deepEqual(ending.sl, WB_SL);
  assert.deepEqual(ending.ht, WB_HT);
  assert.deepEqual(ending.lt, WB_LT);
});

test("estimates and rejected deployments never count; toggles drop negotiation/soft", () => {
  const s = seedState();
  s.demand.push({ id: "e", customer: "X", week: 3, sl: 50, ht: 50, lt: 50, stage: "estimate", review: "accepted" });
  s.demand.push({ id: "r", customer: "Y", week: 3, sl: 50, ht: 50, lt: 50, stage: "po", review: "rejected" });
  const dem = demandByWeek(s.demand, 27, includedStages(s.params));
  assert.equal(dem.sl[3], 3); // Meta only
  const hardOnly = demandByWeek(s.demand, 27, includedStages({ countNegotiation: false, countSoft: false }));
  assert.equal(hardOnly.sl[14], 0); // Space-X (negotiation) excluded
  assert.equal(hardOnly.ht[3], 9);
});

test("keyed actuals replace the plan for past weeks only", () => {
  const s = seedState();
  s.actuals.ht[1] = 0; // planned 5, built 0
  s.actuals.ht[20] = 99; // future: ignored
  const { ending } = project(s, 5, includedStages(s.params));
  assert.equal(ending.ht[1], WB_HT[1] - 5);
  assert.equal(ending.ht[26], WB_HT[26] - 5);
});

test("returns / catch-up adjustments flow into the balance", () => {
  const s = seedState();
  s.adjust.sl[2] = 3;
  const { ending } = project(s, 0, includedStages(s.params));
  assert.equal(ending.sl[2], WB_SL[2] + 3);
  assert.equal(ending.sl[26], WB_SL[26] + 3);
});

test("a draft plan projects instead of the approved plan", () => {
  const s = seedState();
  s.draft = { builds: { ...s.plan.builds, lt: s.plan.builds.lt.map((v, t) => (t >= 12 ? 4 : v)) }, reasonType: "", note: "" };
  const { ending } = project(s, 0, includedStages(s.params));
  assert.ok(ending.lt[26] > WB_LT[26]);
  assert.equal(ending.lt[11], WB_LT[11]);
});

test("ATP: min over the protect window minus buffer; zero when the week itself is short", () => {
  const e = [5, 4, 6, 8, 3, 10];
  assert.equal(atp(e, 0, 3, 1), 3);   // min(5,4,6,8)=4 − 1
  assert.equal(atp(e, 2, 10, 0), 3);  // window clipped to horizon: min(6,8,3,10)
  assert.equal(atp([-1, 5], 0, 1, 0), 0);
});

test("ATP: an existing later shortfall makes a promise conditional, not impossible", () => {
  const e = [10, 10, 10, -4, -4];
  const i = atpInfo(e, 0, 4, 2);
  assert.equal(i.qty, 8);
  assert.equal(i.cond, true);
  assert.equal(i.first, 3);
  const j = atpInfo([3, 3, 3], 0, 2, 0);
  assert.equal(j.cond, false);
});

test("migrate: an older save without new fields loads on the current shape", () => {
  const old = seedState();
  delete old.acks; delete old.gaps; delete old.planHistory; delete old.consensus; delete old.user; delete old.params.holdDays; delete old.params.purchaseGate;
  old.demand.forEach((d) => { delete d.site; delete d.review; delete d.materialReleased; });
  old.actuals = { sl: [1, 2] }; // wrong length / missing products
  const m = migrate(JSON.parse(JSON.stringify(old)));
  assert.deepEqual(m.acks, {}); assert.deepEqual(m.gaps, []); assert.deepEqual(m.planHistory, []);
  assert.equal(m.params.holdDays, 14); assert.equal(m.params.purchaseGate, "contract");
  PRODUCTS.forEach((p) => { assert.equal(m.actuals[p].length, 27); assert.equal(m.adjust[p].length, 27); assert.equal(m.plan.builds[p].length, 27); });
  assert.equal(m.actuals.sl[0], 1); assert.equal(m.actuals.sl[5], null);
  assert.ok(m.demand.every((d) => d.review === "accepted" && d.site === ""));
  const { ending } = project(m, 0, includedStages(m.params));
  assert.deepEqual(ending.ht, WB_HT);
});

test("iso() returns the local calendar date, not the UTC one", () => {
  const late = new Date(2026, 8, 4, 23, 30); // Sep 4, 23:30 local
  assert.equal(iso(late), "2026-09-04");
  assert.equal(iso(toDate("2026-06-29")), "2026-06-29");
});

test("stage order encodes how locked-in a deployment is", () => {
  assert.ok(STAGES.po.order < STAGES.contract.order && STAGES.contract.order < STAGES.negotiation.order && STAGES.negotiation.order < STAGES.soft.order && STAGES.soft.order < STAGES.estimate.order);
});
