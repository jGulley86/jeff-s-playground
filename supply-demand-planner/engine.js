/* ═══════════════════════════════════════════════════════════════════
   Supply & Demand Planner — engine (pure functions, no React, no DOM)
   Everything the UI computes lives here so it can be unit-tested:
   seed data, saved-state migration, coverage projection, ATP.
   Week convention: build[t] = units completing (deployable) in week t.
   ═══════════════════════════════════════════════════════════════════ */
export const DAY = 86400000;
export const PRODUCTS = ["sl", "ht", "lt"];
/* ── Commitment stages: one hue, decreasing solidity = less locked in */
export const STAGES = {
  po:          { label: "PO in hand",      short: "PO",   pct: 100, order: 0, desc: "Purchase order received. Hard demand." },
  contract:    { label: "Contract signed", short: "CTR",  pct: 90,  order: 1, desc: "Contract in hand, PO pending. Hard demand; material released." },
  negotiation: { label: "Negotiation",     short: "NEG",  pct: 60,  order: 2, desc: "CRM stage = negotiation. Counted in coverage as a reservation." },
  soft:        { label: "Soft hold",       short: "SOFT", pct: 30,  order: 3, desc: "Sales placeholder from the availability check. Competes for units; collisions are flagged." },
  estimate:    { label: "Early estimate",  short: "EST",  pct: 10,  order: 4, desc: "Visibility only. Never counted in coverage." },
};
export const STAGE_ORDER = ["po", "contract", "negotiation", "soft", "estimate"];

export const REASONS = {
  absorb:     "Missed build target absorbed into next period",
  escalation: "Approved response to a demand escalation",
  strategic:  "Strategic rate change for a period",
  constraint: "Change in the constraint declaration",
};

export const toDate = (iso) => new Date(iso + "T00:00:00");
export const iso = (d) => new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10); // local calendar date
export const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n, d.getHours(), d.getMinutes()); // calendar days, DST-safe
export const uid = () => Math.random().toString(36).slice(2, 9);
export const zeros = (n) => Array.from({ length: n }, () => 0);
export const nulls = (n) => Array.from({ length: n }, () => null);
export const clampInt = (v, lo, hi) => Math.max(lo, Math.min(hi, Math.round(Number(v) || 0)));

/* ═══════════════════════════════════════════════════════════════════
   SEED — from "Demand Forecast and Fulfillment Confirmation",
   sheet "2026 Demand Forecast", plan as of week of Jun 29, 2026.
   Build rows are units completing (deployable) that week.
   ═══════════════════════════════════════════════════════════════════ */
export function seedState() {
  const N = 27;
  const asOf = "2026-06-29";
  const weeks = Array.from({ length: N }, (_, i) => iso(addDays(toDate(asOf), i * 7)));
  const wk = (isoStr) => weeks.indexOf(isoStr);
  const sl = [0,1,1,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,1];
  const ht = [0,5,4,9,5,5,5,5,10,10,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0];
  const lt = zeros(N);
  const dep = (customer, site, week, s, h, l, stage, extra) => ({
    id: uid(), customer, site, week: wk(week), sl: s, ht: h, lt: l, stage,
    source: "crm", review: "accepted", materialReleased: stage === "po" || stage === "contract",
    note: "", createdAt: asOf, ...extra,
  });
  return {
    meta: { asOf, weeks, seedNote: "Seed: 2026 Demand Forecast workbook, plan as of week of Jun 29, 2026." },
    products: {
      sl: { cost: 63759.91, opening: 0, buffer: 1, maxRate: 3 },
      ht: { cost: 8681.44, opening: 4, buffer: 2, maxRate: 12 },
      lt: { cost: 0, opening: 2, buffer: 2, maxRate: 6 },
    },
    plan: {
      version: "P-2026-06-24", approvedBy: "Jeff Gulley", approvedAt: "2026-06-24", supersedes: null,
      reasonType: "strategic", note: "Baseline carried over from the 2026 Demand Forecast workbook.",
      offCycle: false, builds: { sl, ht, lt },
    },
    draft: null,
    actuals: { sl: nulls(N), ht: nulls(N), lt: nulls(N) },
    adjust: { sl: zeros(N), ht: zeros(N), lt: zeros(N) },
    supply: { updatedAt: asOf, by: "Eric (Production)" },
    consensus: "",
    demand: [
      dep("Meta", "Prineville, OR", "2026-07-20", 3, 9, 0, "po"),
      dep("Home Depot", "Fontana, CA", "2026-07-27", 0, 12, 0, "po"),
      dep("Home Depot", "Fontana, CA", "2026-08-17", 2, 16, 0, "contract"),
      dep("Corning", "Corning, NY", "2026-08-24", 6, 18, 0, "contract"),
      dep("Home Depot", "Savannah, GA", "2026-09-28", 2, 16, 0, "contract"),
      dep("Space-X", "Hawthorne, CA", "2026-10-05", 3, 9, 0, "negotiation", { materialReleased: false }),
      dep("AMXL", "Nashville, TN", "2026-10-12", 2, 0, 12, "negotiation", { materialReleased: false }),
      dep("Home Depot", "Fontana, CA", "2026-11-09", 2, 16, 0, "contract"),
      dep("UPS", "Louisville, KY", "2026-11-09", 1, 0, 4, "negotiation", { materialReleased: false }),
      dep("Home Depot", "Savannah, GA", "2026-12-21", 2, 16, 0, "negotiation", { materialReleased: false }),
    ],
    gaps: [],
    ledger: [
      { id: uid(), at: "2026-06-24", who: "Jeff Gulley", what: "Approved plan P-2026-06-24 (baseline from workbook)." },
    ],
    acks: {},
    planHistory: [],
    user: "",
    params: { cap: 1000000, leadWeeks: 8, protectWeeks: 8, materialLeadWeeks: 10, holdDays: 14, purchaseGate: "contract", kitHeavy: 3, kitLight: 4, countSoft: true, countNegotiation: true },
  };
}

/* Merge a saved state onto the current seed shape so older saves never crash a newer build. */
export function migrate(saved) {
  const seed = seedState();
  const N = (saved.meta && saved.meta.weeks && saved.meta.weeks.length) || seed.meta.weeks.length;
  const arr = (a, fill) => (Array.isArray(a) && a.length === N ? a : Array.from({ length: N }, (_, i) => (Array.isArray(a) && a[i] != null ? a[i] : fill)));
  const s = { ...seed, ...saved };
  s.meta = { ...seed.meta, ...(saved.meta || {}) };
  s.params = { ...seed.params, ...(saved.params || {}) };
  s.products = {}; PRODUCTS.forEach((p) => { s.products[p] = { ...seed.products[p], ...((saved.products || {})[p] || {}) }; });
  s.plan = { ...seed.plan, ...(saved.plan || {}), builds: {} };
  PRODUCTS.forEach((p) => { s.plan.builds[p] = arr(((saved.plan || {}).builds || {})[p], 0); });
  if (saved.draft) { s.draft = { reasonType: "", note: "", ...saved.draft, builds: {} }; PRODUCTS.forEach((p) => { s.draft.builds[p] = arr((saved.draft.builds || {})[p], 0); }); }
  s.actuals = {}; s.adjust = {};
  PRODUCTS.forEach((p) => { s.actuals[p] = arr((saved.actuals || {})[p], null); s.adjust[p] = arr((saved.adjust || {})[p], 0); });
  s.supply = { ...seed.supply, ...(saved.supply || {}) };
  s.demand = (saved.demand || []).map((d) => ({ site: "", source: "manual", review: "accepted", materialReleased: false, note: "", ...d }));
  s.gaps = saved.gaps || []; s.ledger = saved.ledger || []; s.acks = saved.acks || {}; s.planHistory = saved.planHistory || [];
  s.consensus = saved.consensus || ""; s.user = saved.user || "";
  return s;
}

/* ═══════════════════════════════════════════════════════════════════
   Coverage engine
   ═══════════════════════════════════════════════════════════════════ */
export function includedStages(params) {
  const s = ["po", "contract"];
  if (params.countNegotiation) s.push("negotiation");
  if (params.countSoft) s.push("soft");
  return s;
}

export function demandByWeek(demand, N, stages, opts = {}) {
  const out = { sl: zeros(N), ht: zeros(N), lt: zeros(N) };
  demand.forEach((d) => {
    if (d.review === "rejected") return;
    if (!stages.includes(d.stage)) return;
    if (opts.excludeId && d.id === opts.excludeId) return;
    if (d.week < 0 || d.week >= N) return;
    out.sl[d.week] += d.sl || 0; out.ht[d.week] += d.ht || 0; out.lt[d.week] += d.lt || 0;
  });
  return out;
}

export function effectiveBuilds(state, nowIdx) {
  const plan = state.draft ? state.draft.builds : state.plan.builds;
  const out = {};
  PRODUCTS.forEach((p) => {
    out[p] = plan[p].map((v, t) => (t < nowIdx && state.actuals[p][t] != null ? state.actuals[p][t] : v));
  });
  return out;
}

export function project(state, nowIdx, stages, opts = {}) {
  const N = state.meta.weeks.length;
  const dem = demandByWeek(state.demand, N, stages, opts);
  const builds = opts.builds || effectiveBuilds(state, nowIdx);
  const ending = {};
  PRODUCTS.forEach((p) => {
    const arr = [];
    let bal = state.products[p].opening;
    for (let t = 0; t < N; t++) {
      bal = bal + (builds[p][t] || 0) + (state.adjust[p][t] || 0) - dem[p][t];
      arr.push(bal);
    }
    ending[p] = arr;
  });
  return { ending, dem, builds };
}

/* ATP at week w: units on hand at w that no funded commitment inside the
   protect window needs. Weeks that are ALREADY negative are an existing
   shortfall (owned by the plan owner, shown in Signals); they don't block a
   promise, they make it conditional — the promise deepens that gap. */
export function atpInfo(ending, w, protect, buffer) {
  if (ending[w] < 0) return { qty: 0, cond: false, first: -1 };
  const end = Math.min(ending.length - 1, w + protect);
  let m = Infinity, first = -1;
  for (let t = w; t <= end; t++) {
    if (ending[t] < 0) { if (first < 0) first = t; continue; }
    m = Math.min(m, ending[t]);
  }
  return { qty: Math.max(0, Math.floor(m) - buffer), cond: first >= 0, first };
}
export function atp(ending, w, protect, buffer) { return atpInfo(ending, w, protect, buffer).qty; }
