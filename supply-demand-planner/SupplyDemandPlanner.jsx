import React, { useMemo, useState, useEffect, useCallback, useRef } from "react";
import {
  ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ReferenceLine, ResponsiveContainer, Legend, Area,
} from "recharts";

/* ═══════════════════════════════════════════════════════════════════
   SUPPLY & DEMAND PLANNER — one page for Sales, Production, Supply Chain
   Replaces the "Robot Availability" mock at /mocks/demand-planner.

   What the org asked for (mock review 2026-09-03, Jeff's 8/4 vision,
   Demand Planner PRD 2026-08-05):
     • ONE landing page, spreadsheet-style calendar: every deployment,
       the build plan, and deployable inventory — not six screens.
     • Sales: "I need X lifts + Y trays — when?" → date → reserve it.
     • Levels of "locked in" (PO / contract / negotiation / soft hold /
       estimate) in one consistent visual language.
     • Soft commitments that show competing demand and flag collisions
       so Sales picks before a date goes hard.
     • Production keys actuals; plan-vs-actual is visible.
     • Supply chain sees when material is released to buy.
     • Governance: named plan versions, typed change reasons, Jeff
       approves, off-cycle overrides are flagged and counted, approval
       blocked on stale supply inputs or an unacknowledged capacity red.
     • Signals carry an owner, not just a negative cell.

   Model (one documented week convention):
     ending[t] = ending[t-1] + build[t] + adjust[t] − demand[t]
     build[t]  = actual (if keyed, past weeks) else plan
     ATP[w]    = max(0, min over t∈[w, w+protect] of ending[t]) − buffer
   Seed data is derived from the 2026 Demand Forecast workbook (plan as
   of week of Jun 29, 2026). Everything is editable; state autosaves to
   this browser and can be exported/imported as JSON.
   ═══════════════════════════════════════════════════════════════════ */

const STORE_KEY = "slip.sdp.v1";
const DAY = 86400000;

/* ── Theme (SlipOS dark tokens, matching the existing mock) ─────── */
const T = {
  canvas: "#0A0D13", panel: "#10141D", inset: "#0D1119", raise: "#151B27",
  border: "#232A3A", borderSoft: "#1B2130",
  text: "#E6EAF2", sub: "#9AA3B8", muted: "#6B7488",
  indigo: "#6E62F5", indigoSoft: "#A5A0FA",
  amber: "#F5A524", sky: "#38BDF8", pink: "#E879F9",
  green: "#34D399", red: "#F87171", warn: "#FBBF24",
};

/* ── Products ───────────────────────────────────────────────────── */
const PRODUCTS = ["sl", "ht", "lt"];
const PRODUCT_META = {
  sl: { name: "SlipLift", short: "Lift", plural: "SlipLifts", color: T.amber },
  ht: { name: "Heavy Tray", short: "HT", plural: "heavy trays", color: T.sky },
  lt: { name: "Light Tray", short: "LT", plural: "light trays", color: T.pink },
};

/* ── Commitment stages: one hue, decreasing solidity = less locked in */
const STAGES = {
  po:          { label: "PO in hand",      short: "PO",   pct: 100, order: 0, desc: "Purchase order received. Hard demand." },
  contract:    { label: "Contract signed", short: "CTR",  pct: 90,  order: 1, desc: "Contract in hand, PO pending. Hard demand; material released." },
  negotiation: { label: "Negotiation",     short: "NEG",  pct: 60,  order: 2, desc: "CRM stage = negotiation. Counted in coverage as a reservation." },
  soft:        { label: "Soft hold",       short: "SOFT", pct: 30,  order: 3, desc: "Sales placeholder from the availability check. Competes for units; collisions are flagged." },
  estimate:    { label: "Early estimate",  short: "EST",  pct: 10,  order: 4, desc: "Visibility only. Never counted in coverage." },
};
const STAGE_ORDER = ["po", "contract", "negotiation", "soft", "estimate"];

const REASONS = {
  absorb:     "Missed build target absorbed into next period",
  escalation: "Approved response to a demand escalation",
  strategic:  "Strategic rate change for a period",
  constraint: "Change in the constraint declaration",
};

const OWNERS = { mfg: "Manufacturing (plan owner)", sales: "Sales", supply: "Supply Chain", finance: "Finance", planner: "Planner", leadership: "Leadership" };

/* ── Dates ──────────────────────────────────────────────────────── */
const toDate = (iso) => new Date(iso + "T00:00:00");
const iso = (d) => d.toISOString().slice(0, 10);
const addDays = (d, n) => new Date(d.getTime() + n * DAY);
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const fmtWeek = (isoStr) => { const d = toDate(isoStr); return MONTHS[d.getMonth()] + " " + d.getDate(); };
const fmtWeekFull = (isoStr) => { const d = toDate(isoStr); return MONTHS[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear(); };
const fmt$ = (v) => "$" + Math.round(v).toLocaleString();
const fmt$k = (v) => (Math.abs(v) >= 1000000 ? "$" + (v / 1000000).toFixed(2) + "M" : "$" + Math.round(v / 1000) + "K");
const qtrOf = (isoStr) => { const d = toDate(isoStr); return "Q" + (Math.floor(d.getMonth() / 3) + 1); };
const uid = () => Math.random().toString(36).slice(2, 9);
const zeros = (n) => Array.from({ length: n }, () => 0);
const nulls = (n) => Array.from({ length: n }, () => null);
const clampInt = (v, lo, hi) => Math.max(lo, Math.min(hi, Math.round(Number(v) || 0)));

/* ═══════════════════════════════════════════════════════════════════
   SEED — from "Demand Forecast and Fulfillment Confirmation",
   sheet "2026 Demand Forecast", plan as of week of Jun 29, 2026.
   Build rows are units completing (deployable) that week.
   ═══════════════════════════════════════════════════════════════════ */
function seedState() {
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
    params: { cap: 1000000, leadWeeks: 8, protectWeeks: 8, materialLeadWeeks: 10, holdDays: 14, kitHeavy: 3, kitLight: 4, countSoft: true, countNegotiation: true },
  };
}

/* Merge a saved state onto the current seed shape so older saves never crash a newer build. */
function migrate(saved) {
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

function loadState() {
  try {
    const raw = window.localStorage.getItem(STORE_KEY);
    if (raw) { const s = JSON.parse(raw); if (s && s.meta && s.plan && s.demand) return migrate(s); }
  } catch (e) { /* storage unavailable or corrupt: fall through to seed */ }
  return seedState();
}

/* ═══════════════════════════════════════════════════════════════════
   Coverage engine
   ═══════════════════════════════════════════════════════════════════ */
function includedStages(params) {
  const s = ["po", "contract"];
  if (params.countNegotiation) s.push("negotiation");
  if (params.countSoft) s.push("soft");
  return s;
}

function demandByWeek(demand, N, stages, opts = {}) {
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

function effectiveBuilds(state, nowIdx) {
  const plan = state.draft ? state.draft.builds : state.plan.builds;
  const out = {};
  PRODUCTS.forEach((p) => {
    out[p] = plan[p].map((v, t) => (t < nowIdx && state.actuals[p][t] != null ? state.actuals[p][t] : v));
  });
  return out;
}

function project(state, nowIdx, stages, opts = {}) {
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
function atpInfo(ending, w, protect, buffer) {
  if (ending[w] < 0) return { qty: 0, cond: false, first: -1 };
  const end = Math.min(ending.length - 1, w + protect);
  let m = Infinity, first = -1;
  for (let t = w; t <= end; t++) {
    if (ending[t] < 0) { if (first < 0) first = t; continue; }
    m = Math.min(m, ending[t]);
  }
  return { qty: Math.max(0, Math.floor(m) - buffer), cond: first >= 0, first };
}
function atp(ending, w, protect, buffer) { return atpInfo(ending, w, protect, buffer).qty; }

/* ═══════════════════════════════════════════════════════════════════
   Small UI atoms
   ═══════════════════════════════════════════════════════════════════ */
function Stepper({ id, label, value, onChange, accent, max = 99 }) {
  const set = (v) => onChange(clampInt(v, 0, max));
  return (
    <div className="stepper" style={{ "--acc": accent }}>
      <label htmlFor={id}>{label}</label>
      <div className="stepper-row">
        <button type="button" aria-label={"Decrease " + label} onClick={() => set(value - 1)}>−</button>
        <input id={id} type="number" inputMode="numeric" min="0" max={max} value={value}
          onChange={(e) => set(e.target.value === "" ? 0 : parseInt(e.target.value, 10) || 0)}
          onFocus={(e) => e.target.select()} />
        <button type="button" aria-label={"Increase " + label} onClick={() => set(value + 1)}>+</button>
      </div>
    </div>
  );
}

function StageChip({ stage }) {
  const s = STAGES[stage];
  return <span className={"stage-chip st-" + stage} title={s.desc}>{s.label}</span>;
}

function Qty({ d }) {
  const parts = [];
  if (d.sl) parts.push(<span key="s" style={{ color: T.amber }}>{d.sl}</span>);
  if (d.ht) parts.push(<span key="h" style={{ color: T.sky }}>{d.ht}</span>);
  if (d.lt) parts.push(<span key="l" style={{ color: T.pink }}>{d.lt}</span>);
  return <span className="qty">{parts.length ? parts : <span style={{ color: T.muted }}>0</span>}</span>;
}

const tickStyle = { fontSize: 10, fill: T.sub };
const tooltipStyle = { fontSize: 12, borderRadius: 8, background: T.panel, border: "1px solid " + T.border, color: T.text };

/* ═══════════════════════════════════════════════════════════════════
   Main component
   ═══════════════════════════════════════════════════════════════════ */
export default function SupplyDemandPlanner() {
  const [state, setState] = useState(loadState);
  const [saved, setSaved] = useState(true);
  const [flash, setFlash] = useState("");
  const [editing, setEditing] = useState(null);   // deployment being edited (object) or "new"
  const [showSupply, setShowSupply] = useState(false);
  const [focus, setFocus] = useState("all"); // "all" | 8 | 13 weeks from now
  const [showAssumptions, setShowAssumptions] = useState(false);
  const [askMode, setAskMode] = useState("when");
  const [trayType, setTrayType] = useState("heavy");
  const [qLifts, setQLifts] = useState(1);
  const [qTrays, setQTrays] = useState(3);
  const [linkTrays, setLinkTrays] = useState(true);
  const [neededWeek, setNeededWeek] = useState("");
  const [targetWeek, setTargetWeek] = useState(null); // null → first realistic week (now + lead time)
  const [holdName, setHoldName] = useState("");
  const fileRef = useRef(null);

  /* autosave */
  useEffect(() => {
    try { window.localStorage.setItem(STORE_KEY, JSON.stringify(state)); setSaved(true); } catch (e) { setSaved(false); }
  }, [state]);

  const toast = useCallback((msg) => { setFlash(msg); window.setTimeout(() => setFlash(""), 2200); }, []);
  const update = useCallback((fn) => setState((s) => { const n = typeof fn === "function" ? fn(s) : fn; return n; }), []);
  const log = (s, who, what) => ({ ...s, ledger: [{ id: uid(), at: iso(new Date()), who: s.user ? `${s.user} · ${who}` : who, what }, ...s.ledger].slice(0, 200) });

  /* ── derived: calendar position ─────────────────────────────── */
  const { weeks } = state.meta;
  const N = weeks.length;
  const today = new Date();
  const nowIdxRaw = Math.floor((today.getTime() - toDate(weeks[0]).getTime()) / (7 * DAY));
  const nowIdx = Math.max(0, Math.min(N - 1, nowIdxRaw));
  const weekday = today.getDay(); // 0 Sun … 3 Wed
  const supplyAgeDays = Math.floor((today.getTime() - toDate(state.supply.updatedAt).getTime()) / DAY);
  const supplyStale = supplyAgeDays > 7;

  /* ── derived: coverage ──────────────────────────────────────── */
  const stages = useMemo(() => includedStages(state.params), [state.params]);
  const proj = useMemo(() => project(state, nowIdx, stages), [state, nowIdx, stages]);
  const projHard = useMemo(() => project(state, nowIdx, ["po", "contract"]), [state, nowIdx]);
  const projNoSoft = useMemo(() => project(state, nowIdx, stages.filter((s) => s !== "soft")), [state, nowIdx, stages]);
  const approvedProj = useMemo(() => (state.draft ? project(state, nowIdx, stages, { builds: PRODUCTS.reduce((o, p) => { o[p] = state.plan.builds[p].map((v, t) => (t < nowIdx && state.actuals[p][t] != null ? state.actuals[p][t] : v)); return o; }, {}) }) : null), [state, nowIdx, stages]);

  const { protectWeeks, leadWeeks } = state.params;
  const RATIO = trayType === "heavy" ? state.params.kitHeavy : state.params.kitLight;
  const trayKey = trayType === "heavy" ? "ht" : "lt";
  const trayLabel = PRODUCT_META[trayKey].plural;
  const trayAccent = PRODUCT_META[trayKey].color;
  const atpOf = useCallback((p, w) => atp(proj.ending[p], w, protectWeeks, state.products[p].buffer), [proj, protectWeeks, state.products]);
  const atpInfoOf = useCallback((p, w) => atpInfo(proj.ending[p], w, protectWeeks, state.products[p].buffer), [proj, protectWeeks, state.products]);

  /* ── ATP: forward ("when?") ─────────────────────────────────── */
  const ask = useMemo(() => {
    if (askMode !== "when" || (qLifts <= 0 && qTrays <= 0)) return null;
    let inv = -1;
    for (let w = nowIdx; w < N; w++) {
      if (atpOf("sl", w) >= qLifts && atpOf(trayKey, w) >= qTrays) { inv = w; break; }
    }
    const earliestSite = nowIdx + leadWeeks;
    const blockers = () => ["sl", trayKey].map((p) => {
      const e = proj.ending[p]; const first = e.findIndex((v, t) => t >= nowIdx && v < 0);
      if (first < 0) return null;
      const from = Math.min(first, Math.max(nowIdx, earliestSite));
      let free = Infinity; for (let t = from; t < first; t++) free = Math.min(free, e[t] - state.products[p].buffer);
      return { p, first, min: Math.min(...e.slice(nowIdx)), freeBefore: first > from ? Math.max(0, Math.floor(free)) : 0, from };
    }).filter(Boolean);
    if (inv === -1) return { status: "none", blockers: blockers() };
    let w2 = Math.max(inv, earliestSite);
    while (w2 < N && !(atpOf("sl", w2) >= qLifts && atpOf(trayKey, w2) >= qTrays)) w2++;
    if (w2 >= N) return { status: "none", blockers: blockers() };
    const gatedBy = inv >= earliestSite ? "inventory" : "leadtime";
    let status = w2 <= earliestSite + 1 ? "green" : w2 <= earliestSite + 5 ? "tight" : "later";
    // which product is the binding constraint at the week before?
    const constraint = inv > nowIdx ? (atpOf("sl", inv - 1) < qLifts ? "sl" : trayKey) : null;
    // does this promise deepen an existing shortfall inside the protect window?
    const deepens = [["sl", qLifts], [trayKey, qTrays]].map(([p, q]) => { const i = atpInfoOf(p, w2); return q > 0 && i.cond ? { p, week: i.first, by: q } : null; }).filter(Boolean);
    if (deepens.length && status === "green") status = "tight";
    return { status, invWeek: inv, shipWeek: w2, gatedBy, constraint, deepens };
  }, [askMode, qLifts, qTrays, nowIdx, N, leadWeeks, atpOf, atpInfoOf, trayKey]);

  /* ── ATP: reverse ("how much?") ─────────────────────────────── */
  const reverse = useMemo(() => {
    if (askMode !== "howmuch") return null;
    const tgt = targetWeek == null ? nowIdx + leadWeeks : targetWeek;
    const w = Math.max(tgt, nowIdx + leadWeeks);
    if (w >= N) return { maxLifts: 0, maxTrays: 0, kits: 0, week: N - 1, pushed: true };
    const maxLifts = atpOf("sl", w), maxTrays = atpOf(trayKey, w);
    return { maxLifts, maxTrays, kits: Math.min(maxLifts, Math.floor(maxTrays / RATIO)), week: w, pushed: w !== tgt };
  }, [askMode, targetWeek, nowIdx, leadWeeks, N, atpOf, trayKey, RATIO]);

  const neededIdx = neededWeek === "" ? null : +neededWeek;
  const gapWeeks = ask && ask.shipWeek != null && neededIdx != null ? ask.shipWeek - neededIdx : 0;

  /* ── Signals (each with an owner) ───────────────────────────── */
  const signals = useMemo(() => {
    const out = [];
    PRODUCTS.forEach((p) => {
      const e = proj.ending[p];
      const first = e.findIndex((v, t) => t >= nowIdx && v < 0);
      if (first >= 0) {
        const mag = Math.min(...e.slice(nowIdx));
        const hardOk = !projNoSoft.ending[p].slice(nowIdx).some((v) => v < 0);
        if (hardOk) {
          const softs = state.demand.filter((d) => d.stage === "soft" && d.review !== "rejected" && d.week >= first - protectWeeks && d.week <= first + 2 && (d[p] || 0) > 0);
          out.push({ id: "collision-" + p, sev: "red", owner: "sales", title: `${PRODUCT_META[p].name} soft holds collide`, body: `Hard + negotiation demand is covered, but soft holds push ${PRODUCT_META[p].plural} to ${mag} by ${fmtWeek(weeks[first])}. Sales picks which hold gets the slot: ${softs.map((d) => d.customer + " (" + (d[p] || 0) + ", " + fmtWeek(weeks[d.week]) + ")").join("; ") || "see calendar"}.` });
        } else {
          out.push({ id: "short-" + p, sev: "red", owner: "mfg", title: `${PRODUCT_META[p].name} shortfall from ${fmtWeek(weeks[first])}`, body: `Projected deployable inventory hits ${mag}. Options: pull a build forward, propose a rate change (new plan version), or Sales spreads the deployment to fit the standing plan.` });
        }
      } else {
        const bufIdx = e.findIndex((v, t) => t >= nowIdx && v < state.products[p].buffer);
        if (bufIdx >= 0) out.push({ id: "buffer-" + p, sev: "amber", owner: "mfg", title: `${PRODUCT_META[p].name} inside buffer ${fmtWeek(weeks[bufIdx])}`, body: `Balance drops below the ${state.products[p].buffer}-unit production buffer. Nothing new is promisable that week.` });
      }
      const builds = state.draft ? state.draft.builds[p] : state.plan.builds[p];
      const over = builds.findIndex((v, t) => t >= nowIdx && v > state.products[p].maxRate);
      if (over >= 0) out.push({ id: "cap-" + p, sev: "red", owner: "leadership", ack: true, title: `${PRODUCT_META[p].name} plan exceeds capacity ${fmtWeek(weeks[over])}`, body: `${builds[over]}/wk planned vs ${state.products[p].maxRate}/wk max. Leadership evaluates a rate change or an investment. Acknowledge before approving a plan.` });
    });
    const fg = weeks.map((_, i) => PRODUCTS.reduce((s, p) => s + Math.max(0, proj.ending[p][i]) * state.products[p].cost, 0));
    const capIdx = fg.findIndex((v, i) => i >= nowIdx && v > state.params.cap);
    if (capIdx >= 0) out.push({ id: "fg-cap", sev: "amber", owner: "finance", title: `Finished goods break the ${fmt$k(state.params.cap)} cap ${fmtWeek(weeks[capIdx])}`, body: `Peaks at ${fmt$k(Math.max(...fg))}. Either Sales fills the weeks near the cap or the plan owner defers builds. Exceeding the cap needs Finance approval.` });
    if (supplyStale) out.push({ id: "stale", sev: "red", owner: "mfg", title: `Supply inputs are ${supplyAgeDays} days old`, body: "Build actuals, returns, and catch-up are due Tuesday EOD. Plan approval is blocked while inputs are older than 7 days." });
    const proposed = state.demand.filter((d) => d.review === "proposed");
    if (proposed.length) out.push({ id: "queue", sev: "amber", owner: "planner", title: `${proposed.length} deployment${proposed.length > 1 ? "s" : ""} awaiting review`, body: "Accept, amend, or reject before Monday EOD so the queue is clear for Wednesday's consensus meeting.", queue: proposed });
    const release = state.demand.filter((d) => ["po", "contract"].includes(d.stage) && d.review !== "rejected" && !d.materialReleased && d.week - state.params.materialLeadWeeks <= nowIdx + 2);
    if (release.length) out.push({ id: "release", sev: "amber", owner: "supply", title: `Material release due for ${release.length} deployment${release.length > 1 ? "s" : ""}`, body: release.map((d) => `${d.customer} ${fmtWeek(weeks[d.week])}`).join(", ") + ` — contract in hand and inside the ${state.params.materialLeadWeeks}-week material lead time. Release the buy.`, release });
    const expired = state.demand.filter((d) => d.stage === "soft" && d.review !== "rejected" && d.expiresAt && toDate(d.expiresAt) < today);
    if (expired.length) out.push({ id: "expired", sev: "amber", owner: "planner", title: `${expired.length} soft hold${expired.length > 1 ? "s" : ""} past expiry`, body: `Holds last ${state.params.holdDays} days unless the deal moves to negotiation. Release the units or extend if the deal is alive.`, expired });
    const missing = PRODUCTS.some((p) => state.actuals[p].slice(Math.max(0, nowIdx - 4), nowIdx).some((v) => v == null));
    if (missing && nowIdx > 0) out.push({ id: "actuals", sev: "amber", owner: "mfg", title: "Build actuals missing for recent weeks", body: "Plan-vs-actual can't be read. Key actuals in the supply detail rows (toggle below the calendar)." });
    return out.sort((a, b) => (a.sev === b.sev ? 0 : a.sev === "red" ? -1 : 1));
  }, [proj, projNoSoft, state, nowIdx, weeks, protectWeeks, supplyStale, supplyAgeDays]);

  /* ── Charts ─────────────────────────────────────────────────── */
  const chartData = useMemo(() => {
    const e = askMode === "when" && ask && ask.shipWeek != null ? ask.shipWeek : -1;
    return weeks.map((wk, i) => {
      const row = { wk: fmtWeek(wk) };
      PRODUCTS.forEach((p) => { row[PRODUCT_META[p].name] = proj.ending[p][i]; });
      if (approvedProj) PRODUCTS.forEach((p) => { row["approved_" + p] = approvedProj.ending[p][i]; });
      row["Finished goods $"] = PRODUCTS.reduce((s, p) => s + Math.max(0, proj.ending[p][i]) * state.products[p].cost, 0);
      if (e >= 0 && i >= e) {
        row.simSl = proj.ending.sl[i] - qLifts;
        row.simTray = proj.ending[trayKey][i] - qTrays;
      }
      return row;
    });
  }, [weeks, proj, approvedProj, askMode, ask, qLifts, qTrays, trayKey, state.products]);

  /* ── Rollups by month ───────────────────────────────────────── */
  const rollup = useMemo(() => {
    const m = new Map();
    weeks.forEach((wk, i) => {
      const d = toDate(wk); const key = MONTHS[d.getMonth()] + " " + d.getFullYear();
      if (!m.has(key)) m.set(key, { key, dem: { sl: 0, ht: 0, lt: 0 }, build: { sl: 0, ht: 0, lt: 0 }, end: { sl: 0, ht: 0, lt: 0 } });
      const r = m.get(key);
      PRODUCTS.forEach((p) => { r.dem[p] += proj.dem[p][i]; r.build[p] += proj.builds[p][i]; r.end[p] = proj.ending[p][i]; });
    });
    return [...m.values()];
  }, [weeks, proj]);

  /* ── Governance ─────────────────────────────────────────────── */
  const draftDelta = useMemo(() => {
    if (!state.draft) return [];
    const out = [];
    PRODUCTS.forEach((p) => state.draft.builds[p].forEach((v, t) => { if (v !== state.plan.builds[p][t]) out.push({ p, t, from: state.plan.builds[p][t], to: v }); }));
    return out;
  }, [state.draft, state.plan]);
  const capacityRed = signals.filter((s) => s.ack && !state.acks[s.id]);
  const offCycle = weekday !== 3;
  const offCycleCount = state.ledger.filter((l) => /off-cycle/i.test(l.what) && qtrOf(l.at) === qtrOf(iso(today)) && l.at.slice(0, 4) === String(today.getFullYear())).length;
  const checklist = state.draft ? [
    { ok: draftDelta.length > 0, label: "Delta preview vs " + state.plan.version, detail: draftDelta.length + " cell" + (draftDelta.length === 1 ? "" : "s") + " changed" },
    { ok: state.consensus.trim().length > 0, label: "Signed consensus number on screen", detail: state.consensus.trim() || "enter it in the plan header" },
    { ok: true, label: "Coverage by product with buffer state", detail: "shown in the calendar" },
    { ok: capacityRed.length === 0, label: "Capacity signal green or acknowledged", detail: capacityRed.length ? capacityRed.length + " unacknowledged" : "ok" },
    { ok: !PRODUCTS.some((p) => state.actuals[p].slice(Math.max(0, nowIdx - 4), nowIdx).some((v) => v == null)) || nowIdx === 0, label: "Plan-vs-actual, last 4 weeks", detail: "actuals keyed" },
    { ok: !!state.draft.reasonType, label: "Typed change reason", detail: state.draft.reasonType ? REASONS[state.draft.reasonType] : "pick one" },
    { ok: !supplyStale, label: "Supply inputs fresh (≤ 7 days)", detail: supplyAgeDays + " days old" },
  ] : [];
  const canApprove = checklist.length > 0 && checklist.every((c) => c.ok);

  /* ── Mutations ──────────────────────────────────────────────── */
  const setBuild = (p, t, v) => update((s) => {
    const draft = s.draft ? { ...s.draft, builds: { ...s.draft.builds } } : { builds: { ...s.plan.builds }, reasonType: "", note: "" };
    draft.builds[p] = [...draft.builds[p]]; draft.builds[p][t] = clampInt(v, 0, 99);
    return { ...s, draft };
  });
  const setActual = (p, t, v) => update((s) => { const a = { ...s.actuals, [p]: [...s.actuals[p]] }; a[p][t] = v === "" ? null : clampInt(v, 0, 99); return { ...s, actuals: a }; });
  const setAdjust = (p, t, v) => update((s) => { const a = { ...s.adjust, [p]: [...s.adjust[p]] }; a[p][t] = clampInt(v, -99, 99); return { ...s, adjust: a }; });
  const markSupplyCurrent = () => update((s) => log({ ...s, supply: { updatedAt: iso(today), by: "you" } }, "Manufacturing", "Supply inputs keyed (actuals, returns, catch-up)."));
  const approve = () => update((s) => {
    if (!s.draft) return s;
    const ver = "P-" + iso(today) + (offCycle ? "-OC" : "");
    const plan = { version: ver, approvedBy: "Jeff Gulley", approvedAt: iso(today), supersedes: s.plan.version, reasonType: s.draft.reasonType, note: s.draft.note, offCycle: offCycle, builds: s.draft.builds };
    const what = `Approved plan ${ver} (supersedes ${s.plan.version}) — ${REASONS[s.draft.reasonType]}${offCycle ? " — OFF-CYCLE override" : ""}${s.draft.note ? ": " + s.draft.note : ""}. ${draftDelta.length} cell${draftDelta.length === 1 ? "" : "s"} changed.`;
    return log({ ...s, plan, draft: null }, "Jeff Gulley", what);
  });
  const discardDraft = () => update((s) => ({ ...s, draft: null }));
  const saveDeployment = (d) => update((s) => {
    const exists = s.demand.some((x) => x.id === d.id);
    const demand = exists ? s.demand.map((x) => (x.id === d.id ? d : x)) : [d, ...s.demand];
    return log({ ...s, demand }, "you", `${exists ? "Updated" : "Added"} deployment ${d.customer} · ${fmtWeek(weeks[d.week])} · ${STAGES[d.stage].label}.`);
  });
  const removeDeployment = (id) => update((s) => { const d = s.demand.find((x) => x.id === id); return log({ ...s, demand: s.demand.filter((x) => x.id !== id) }, "you", `Removed deployment ${d ? d.customer : id}.`); });
  const setReview = (id, review) => update((s) => { const d = s.demand.find((x) => x.id === id); return log({ ...s, demand: s.demand.map((x) => (x.id === id ? { ...x, review } : x)) }, "Planner", `${review === "accepted" ? "Accepted" : "Rejected"} ${d ? d.customer + " " + fmtWeek(weeks[d.week]) : id}.`); });
  const releaseMaterial = (id) => update((s) => { const d = s.demand.find((x) => x.id === id); return log({ ...s, demand: s.demand.map((x) => (x.id === id ? { ...x, materialReleased: true } : x)) }, "Supply Chain", `Material released for ${d ? d.customer + " " + fmtWeek(weeks[d.week]) : id}.`); });
  const ackSignal = (id) => update((s) => ({ ...s, acks: { ...s.acks, [id]: iso(today) } }));
  const extendHold = (id) => update((s) => { const d = s.demand.find((x) => x.id === id); return log({ ...s, demand: s.demand.map((x) => (x.id === id ? { ...x, expiresAt: iso(addDays(today, s.params.holdDays)) } : x)) }, "Planner", `Extended soft hold for ${d ? d.customer : id} by ${s.params.holdDays} days.`); });

  const placeHold = () => {
    if (!ask || ask.shipWeek == null) return;
    const d = { id: uid(), customer: holdName.trim() || "Unnamed prospect", site: "", week: ask.shipWeek, sl: qLifts, ht: trayType === "heavy" ? qTrays : 0, lt: trayType === "light" ? qTrays : 0, stage: "soft", source: "ask", review: "proposed", materialReleased: false, note: "Soft hold from availability check", createdAt: iso(today), expiresAt: iso(addDays(today, state.params.holdDays)) };
    update((s) => log({ ...s, demand: [d, ...s.demand] }, "Sales", `Soft hold: ${d.customer} — ${qLifts} lifts + ${qTrays} ${trayLabel}, week of ${fmtWeek(weeks[ask.shipWeek])}.`));
    setHoldName(""); toast("Soft hold placed — planner will review");
  };
  const logGap = () => {
    if (!ask || ask.shipWeek == null || neededIdx == null) return;
    const g = { id: uid(), customer: holdName.trim() || "Unnamed prospect", sl: qLifts, ht: trayType === "heavy" ? qTrays : 0, lt: trayType === "light" ? qTrays : 0, neededWeek: neededIdx, offeredWeek: ask.shipWeek, createdAt: iso(today), constraint: ask.constraint || (ask.gatedBy === "leadtime" ? "site readiness" : "inventory") };
    update((s) => log({ ...s, gaps: [g, ...s.gaps] }, "Sales", `Demand gap logged: ${g.customer} needed ${fmtWeek(weeks[neededIdx])}, offered ${fmtWeek(weeks[ask.shipWeek])}.`));
    toast("Demand gap logged for the plan owner");
  };

  const copyText = (text, label) => {
    const done = () => toast(label + " copied");
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
    else fallbackCopy(text, done);
  };
  const fallbackCopy = (text, done) => {
    const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); } catch (e) { /* ignore */ }
    document.body.removeChild(ta); done();
  };
  const promiseText = ask && ask.shipWeek != null
    ? `Availability confirmation — Slip Robotics\nConfiguration: ${qLifts} SlipLift${qLifts !== 1 ? "s" : ""} + ${qTrays} ${trayLabel}\nEarliest go-live: week of ${fmtWeekFull(weeks[ask.shipWeek])}\nSite qualification must be underway by ${fmtWeekFull(weeks[Math.max(0, ask.shipWeek - leadWeeks)])}.\nHonors all committed deployments${state.params.countSoft ? " and active soft holds" : ""}. Planning promise, subject to contract and planner acceptance.`
    : "";
  const weeklyPack = () => {
    const lines = [];
    lines.push(`Supply & Demand pack — week of ${fmtWeekFull(weeks[nowIdx])}`);
    lines.push(`Plan in force: ${state.plan.version} (approved ${state.plan.approvedAt} by ${state.plan.approvedBy})${state.draft ? " — DRAFT pending approval" : ""}`);
    lines.push(`Consensus: ${state.consensus || "not entered"}`);
    lines.push("");
    lines.push("Coverage (deployable, end of week):");
    PRODUCTS.forEach((p) => {
      const e = proj.ending[p]; const first = e.findIndex((v, t) => t >= nowIdx && v < 0);
      lines.push(`  ${PRODUCT_META[p].name}: now ${e[nowIdx]}, year-end ${e[N - 1]}${first >= 0 ? `, SHORT ${Math.min(...e.slice(nowIdx))} from ${fmtWeek(weeks[first])}` : ", no shortfall"}`);
    });
    lines.push("");
    lines.push("Next 4 weeks:");
    state.demand.filter((d) => d.review !== "rejected" && d.week >= nowIdx && d.week < nowIdx + 4).sort((a, b) => a.week - b.week)
      .forEach((d) => lines.push(`  ${fmtWeek(weeks[d.week])} ${d.customer} — ${d.sl || 0} lifts, ${d.ht || 0} HT, ${d.lt || 0} LT (${STAGES[d.stage].label})`));
    lines.push("");
    lines.push("Signals:");
    signals.forEach((s) => lines.push(`  [${s.sev.toUpperCase()}] ${s.title} → ${OWNERS[s.owner]}`));
    if (!signals.length) lines.push("  none");
    return lines.join("\n");
  };
  const exportJson = () => {
    const text = JSON.stringify(state, null, 2);
    try {
      const blob = new Blob([text], { type: "application/json" }); const url = URL.createObjectURL(blob);
      const a = document.createElement("a"); a.href = url; a.download = `sdp-${iso(today)}.json`; document.body.appendChild(a); a.click(); document.body.removeChild(a);
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (e) { /* fall through */ }
    copyText(text, "Plan JSON");
  };
  const importJson = (file) => {
    const r = new FileReader();
    r.onload = () => { try { const s = JSON.parse(String(r.result)); if (s && s.meta && s.plan && s.demand) { setState(migrate(s)); toast("Plan imported"); } else toast("Not a planner file"); } catch (e) { toast("Could not read file"); } };
    r.readAsText(file);
  };
  const resetSeed = () => { if (window.confirm("Replace everything in this browser with the seed plan from the workbook?")) { setState(seedState()); toast("Reset to seed"); } };

  /* ── Renders ────────────────────────────────────────────────── */
  const view = useMemo(() => weeks.map((_, i) => i).filter((i) => focus === "all" || (i >= Math.max(0, nowIdx - 1) && i < nowIdx + focus)), [weeks, focus, nowIdx]);
  const vweeks = useMemo(() => view.map((i) => [weeks[i], i]), [view, weeks]);
  const sortedDemand = useMemo(() => [...state.demand].filter((d) => d.review !== "rejected" && (focus === "all" || view.includes(d.week))).sort((a, b) => a.week - b.week || STAGES[a.stage].order - STAGES[b.stage].order), [state.demand, focus, view]);
  const cellClass = (v, buffer) => (v < 0 ? "neg" : v < buffer ? "buf" : "ok");
  const hardShort = PRODUCTS.map((p) => projHard.ending[p].slice(nowIdx).some((v) => v < 0));
  const fgNow = PRODUCTS.reduce((s, p) => s + Math.max(0, proj.ending[p][nowIdx]) * state.products[p].cost, 0);
  const cadence = [
    { d: 1, k: "Mon", t: "Demand refresh", who: "Commercial + planner clear the queue" },
    { d: 2, k: "Tue", t: "Supply reality check", who: "Manufacturing keys actuals" },
    { d: 3, k: "Wed", t: "Consensus meeting", who: "Plan version approved here" },
    { d: 4, k: "Thu", t: "Publish", who: "This page is the pack" },
  ];

  return (
    <div className="sdp">
      <style>{CSS}</style>

      {/* ══ Header ══ */}
      <header className="head">
        <div>
          <div className="brand">Slip Robotics</div>
          <div className="title">Supply &amp; Demand Planner <span className="dim">· Sales · Production · Supply Chain</span></div>
        </div>
        <div className="chips">
          <div className="chip" title={state.plan.note}>Plan <b>{state.plan.version}</b>{state.draft ? <span className="draft-dot" title="Draft edits pending approval"> draft</span> : null}</div>
          <div className={"chip " + (supplyStale ? "hot" : "ok")} title={"Last keyed by " + state.supply.by}>Supply inputs <b>{supplyAgeDays === 0 ? "today" : supplyAgeDays + "d old"}</b></div>
          <div className={"chip " + (fgNow > state.params.cap ? "hot" : "ok")}>Finished goods <b>{fmt$k(fgNow)}</b> / {fmt$k(state.params.cap)}</div>
          <div className="chip">Week of <b>{fmtWeek(weeks[nowIdx])}</b>{nowIdxRaw !== nowIdx ? <span className="dim"> (horizon edge)</span> : null}</div>
          <input className="who" value={state.user} placeholder="Your name (for the ledger)" aria-label="Your name" onChange={(e) => update((s) => ({ ...s, user: e.target.value }))} />
        </div>
      </header>

      <div className="wrap">
        {/* ══ Cadence strip ══ */}
        <div className="cadence" role="list" aria-label="Weekly planning cadence">
          {cadence.map((c) => (
            <div key={c.k} role="listitem" className={"cad" + (weekday === c.d ? " now" : "")}>
              <span className="cad-k">{c.k}</span><span className="cad-t">{c.t}</span><span className="cad-w">{c.who}</span>
            </div>
          ))}
          <div className="cad-actions">
            <button className="btn ghost" onClick={() => copyText(weeklyPack(), "Weekly pack")}>Copy weekly pack</button>
            <button className="btn ghost" onClick={markSupplyCurrent}>Mark supply inputs keyed</button>
          </div>
        </div>

        {/* ══ At a glance ══ */}
        <div className="kpis">
          {PRODUCTS.map((p) => {
            const e = proj.ending[p]; const first = e.findIndex((v, t) => t >= nowIdx && v < 0);
            const freeW = Math.min(N - 1, nowIdx + leadWeeks); const free = atpInfoOf(p, freeW);
            return (
              <div key={p} className={"kpi" + (first >= 0 ? " bad" : "")}>
                <div className="kpi-name" style={{ color: PRODUCT_META[p].color }}>{PRODUCT_META[p].name}</div>
                <div className="kpi-row"><span>On hand now</span><b>{e[nowIdx]}</b></div>
                <div className="kpi-row"><span>Free to promise {fmtWeek(weeks[freeW])}</span><b>{free.qty}{free.cond ? <small title="conditional — deepens a later shortfall">*</small> : null}</b></div>
                <div className="kpi-row"><span>First shortfall</span><b className={first >= 0 ? "hot-text" : ""}>{first >= 0 ? fmtWeek(weeks[first]) + " (" + Math.min(...e.slice(nowIdx)) + ")" : "none"}</b></div>
                <div className="kpi-row"><span>Year-end</span><b>{e[N - 1]}</b></div>
              </div>
            );
          })}
          <div className={"kpi" + (fgNow > state.params.cap ? " bad" : "")}>
            <div className="kpi-name">Finished goods</div>
            <div className="kpi-row"><span>Now</span><b>{fmt$k(fgNow)}</b></div>
            <div className="kpi-row"><span>Peak in plan</span><b>{fmt$k(Math.max(...chartData.slice(nowIdx).map((r) => r["Finished goods $"])))}</b></div>
            <div className="kpi-row"><span>Cap</span><b>{fmt$k(state.params.cap)}</b></div>
            <div className="kpi-row"><span>Open signals</span><b className={signals.some((x) => x.sev === "red") ? "hot-text" : ""}>{signals.length}</b></div>
          </div>
        </div>

        {/* ══ 1. Ask (ATP) ══ */}
        <section className="card ask">
          <div className="card-head">
            <div>
              <h2>Can I have robots by…?</h2>
              <p className="sub">Type what the customer needs. The answer honors every committed deployment{state.params.countNegotiation ? ", negotiations" : ""}{state.params.countSoft ? ", soft holds" : ""}, the production buffer, and the {leadWeeks}-week site-readiness lead time.</p>
            </div>
            <div className="mode" role="tablist" aria-label="Query mode">
              <button role="tab" aria-selected={askMode === "when"} className={askMode === "when" ? "on" : ""} onClick={() => setAskMode("when")}>I know the quantity → when?</button>
              <button role="tab" aria-selected={askMode === "howmuch"} className={askMode === "howmuch" ? "on" : ""} onClick={() => setAskMode("howmuch")}>I know the date → how much?</button>
            </div>
          </div>

          <div className="hero">
            {askMode === "when" ? (
              <>
                <div className="inputs">
                  <div className="slots" role="group" aria-label="Deployment size presets">
                    <span className="slots-k">Slot</span>
                    {[["S", 1], ["M", 2], ["L", 4]].map(([k, n]) => (
                      <button key={k} className={"slot" + (qLifts === n && qTrays === n * RATIO ? " on" : "")} title={`${k}: ${n} lift${n > 1 ? "s" : ""} + ${n * RATIO} ${trayLabel}`} onClick={() => { setQLifts(n); setQTrays(n * RATIO); setLinkTrays(true); }}>{k}<small>{n}+{n * RATIO}</small></button>
                    ))}
                  </div>
                  <Stepper id="ql" label="SlipLifts" value={qLifts} onChange={(v) => { setQLifts(v); if (linkTrays) setQTrays(v * RATIO); }} accent={T.amber} />
                  <div className="tray-col">
                    <div className="type-seg" role="group" aria-label="Tray type">
                      <button className={"h" + (trayType === "heavy" ? " on" : "")} onClick={() => { setTrayType("heavy"); if (linkTrays) setQTrays(qLifts * state.params.kitHeavy); }}>Heavy</button>
                      <button className={"l" + (trayType === "light" ? " on" : "")} onClick={() => { setTrayType("light"); if (linkTrays) setQTrays(qLifts * state.params.kitLight); }}>Light</button>
                    </div>
                    <Stepper id="qt" label={PRODUCT_META[trayKey].name + "s"} value={qTrays} onChange={(v) => { setQTrays(v); if (linkTrays && v !== qLifts * RATIO) setLinkTrays(false); }} accent={trayAccent} />
                  </div>
                  <div className="ask-side">
                    <label className="link-toggle" title="Typical kit: 3 heavy or 4 light trays per SlipLift">
                      <input type="checkbox" checked={linkTrays} onChange={(e) => { setLinkTrays(e.target.checked); if (e.target.checked) setQTrays(qLifts * RATIO); }} />
                      Keep {RATIO} trays per lift
                    </label>
                    <label className="small" htmlFor="need">Customer needs it by <span className="dim">(optional)</span></label>
                    <select id="need" value={neededWeek} onChange={(e) => setNeededWeek(e.target.value)}>
                      <option value="">— not stated —</option>
                      {weeks.map((w, i) => (i >= nowIdx ? <option key={w} value={i}>{fmtWeekFull(w)}</option> : null))}
                    </select>
                  </div>
                </div>

                {!ask && (
                  <div className="tag idle" role="status"><div className="verdict">Enter a quantity</div><div className="tag-detail">The earliest go-live week appears here.</div></div>
                )}
                {ask && ask.status !== "none" && (
                  <div className={"tag " + ask.status} role="status" aria-live="polite">
                    <div className="verdict">{ask.status === "green" ? "Green light" : ask.status === "tight" ? "Tight — but yes" : "Later this year"}</div>
                    <div className="stamp"><small>Earliest go-live week</small>{fmtWeekFull(weeks[ask.shipWeek])}</div>
                    <div className="tag-detail">
                      {qLifts} SlipLift{qLifts !== 1 ? "s" : ""} + {qTrays} {trayLabel}.
                      {ask.gatedBy === "leadtime"
                        ? ` Fleet is free earlier (week of ${fmtWeek(weeks[ask.invWeek])}); site readiness is the gate — start qualification now to lock this date.`
                        : ` The gate is ${ask.constraint ? PRODUCT_META[ask.constraint].name.toLowerCase() : "fleet"} availability; site readiness fits inside the wait.`}
                      {ask.deepens && ask.deepens.length > 0 ? <span className="gap-note"> Conditional: {ask.deepens.map((x) => `adds ${x.by} to the existing ${PRODUCT_META[x.p].plural} shortfall from ${fmtWeek(weeks[x.week])}`).join("; ")} — that gap is already flagged to Manufacturing and must be closed either way.</span> : null}
                      {gapWeeks > 0 ? <span className="gap-note"> That is {gapWeeks} week{gapWeeks > 1 ? "s" : ""} later than the customer needs.</span> : null}
                    </div>
                    <div className="tag-actions">
                      <input className="hold-name" placeholder="Customer / prospect…" value={holdName} onChange={(e) => setHoldName(e.target.value)} aria-label="Customer name for the soft hold" />
                      <button className="btn" onClick={placeHold}>Place soft hold</button>
                      <button className="btn ghost" onClick={() => copyText(promiseText, "Customer promise")}>Copy customer promise</button>
                      {gapWeeks > 0 && <button className="btn warn" onClick={logGap}>Log demand gap</button>}
                    </div>
                  </div>
                )}
                {ask && ask.status === "none" && (
                  <div className="tag none" role="status" aria-live="polite">
                    <div className="verdict">Not in this plan</div>
                    <div className="tag-detail">
                      {ask.blockers && ask.blockers.length > 0 ? (
                        <>
                          {ask.blockers.map((b) => (
                            <span key={b.p}>{PRODUCT_META[b.p].plural.charAt(0).toUpperCase() + PRODUCT_META[b.p].plural.slice(1)} already go <b className="hot-text">{b.min}</b> the week of {fmtWeek(weeks[b.first])} under plan {state.plan.version} — an existing shortfall (owner: {OWNERS.mfg}). Promising more {PRODUCT_META[b.p].plural} would deepen it.{b.freeBefore > 0 ? ` Physically free before the gap: up to ${b.freeBefore} from ${fmtWeek(weeks[b.from])}.` : ""} </span>
                          ))}
                          <span>Close the gap (restart builds, move the late deployment) and this ask clears. Log it as a demand gap so the plan owner has the evidence.</span>
                        </>
                      ) : (
                        <>The current build plan can't cover {qLifts} SlipLifts + {qTrays} {trayLabel} inside the horizon without touching a committed deployment.
                          {trayType === "light" && !state.plan.builds.lt.some((v) => v > 0) ? " Zero light-tray builds are planned — any light-tray deal needs a build decision first." : " Log it as a demand gap so the plan owner sees the demand we're turning away."}</>
                      )}
                    </div>
                    <div className="tag-actions">
                      <input className="hold-name" placeholder="Customer / prospect…" value={holdName} onChange={(e) => setHoldName(e.target.value)} aria-label="Customer name" />
                      <button className="btn warn" onClick={() => {
                        const g = { id: uid(), customer: holdName.trim() || "Unnamed prospect", sl: qLifts, ht: trayType === "heavy" ? qTrays : 0, lt: trayType === "light" ? qTrays : 0, neededWeek: neededIdx == null ? nowIdx + leadWeeks : neededIdx, offeredWeek: null, createdAt: iso(today), constraint: trayType === "light" ? "light tray builds" : "build plan" };
                        update((s) => log({ ...s, gaps: [g, ...s.gaps] }, "Sales", `Demand gap logged: ${g.customer} — not coverable in plan.`)); toast("Demand gap logged");
                      }}>Log demand gap</button>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <>
                <div className="inputs">
                  <div>
                    <label className="small" htmlFor="tw" style={{ margin: "0 0 6px" }}>Customer wants go-live the week of</label>
                    <select id="tw" value={targetWeek == null ? Math.min(N - 1, nowIdx + leadWeeks) : targetWeek} onChange={(e) => setTargetWeek(+e.target.value)}>
                      {weeks.map((w, i) => <option key={w} value={i}>{fmtWeekFull(w)}</option>)}
                    </select>
                  </div>
                  <div className="tray-col">
                    <label className="small" style={{ margin: "0 0 2px" }}>Tray type</label>
                    <div className="type-seg" role="group" aria-label="Tray type">
                      <button className={"h" + (trayType === "heavy" ? " on" : "")} onClick={() => setTrayType("heavy")}>Heavy</button>
                      <button className={"l" + (trayType === "light" ? " on" : "")} onClick={() => setTrayType("light")}>Light</button>
                    </div>
                  </div>
                </div>
                {reverse && (
                  <div className={"tag " + (reverse.kits >= 3 ? "green" : reverse.kits >= 1 ? "tight" : "later")} role="status" aria-live="polite">
                    <div className="verdict">{reverse.kits >= 1 ? "Biggest deal you can promise" : "Nothing free that week"}</div>
                    <div className="stamp"><small>By week of {fmtWeek(weeks[reverse.week])}</small>{reverse.kits} lift{reverse.kits !== 1 ? "s" : ""} + {reverse.kits * RATIO} {trayLabel}</div>
                    <div className="tag-detail">
                      Raw ceilings that week: {reverse.maxLifts} SlipLifts and {reverse.maxTrays} {trayLabel}, after commitments, holds, and buffer.
                      {reverse.pushed ? ` Your target sits inside the ${leadWeeks}-week site-readiness window, so this is the first realistic go-live.` : ""}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>

          {askMode === "when" && ask && ask.shipWeek != null && (
            <div className="miles" aria-label="Backward plan">
              {[
                { label: "Site qualification starts", week: ask.shipWeek - leadWeeks, owner: "Sales + customer" },
                { label: "Implementation kickoff", week: ask.shipWeek - Math.ceil(leadWeeks * 0.6), owner: "Ops" },
                { label: "Field tech + warehouse confirmed", week: ask.shipWeek - 3, owner: "Service Delivery" },
                { label: "Material complete / handoff", week: ask.shipWeek - 1, owner: "Production" },
                { label: "Dock pickup → go-live", week: ask.shipWeek, owner: "Logistics · Field Ops" },
              ].map((m, i) => {
                const wk = Math.max(nowIdx, Math.min(m.week, ask.shipWeek));
                return (
                  <div key={i} className={"mile" + (m.week <= nowIdx ? " due" : "")}>
                    <div className="mile-dot" />
                    <div className="mile-wk">{m.week <= nowIdx ? "Now" : fmtWeek(weeks[wk])}</div>
                    <div className="mile-label">{m.label}</div>
                    <div className="mile-owner">{m.owner}</div>
                  </div>
                );
              })}
            </div>
          )}

          {/* free-kits strip */}
          <div className="heat-scroll">
            <div className="heat">
              {weeks.map((wk, w) => {
                const li = atpInfoOf("sl", w), ti = atpInfoOf(trayKey, w);
                const l = li.qty, t = ti.qty;
                const kits = Math.min(l, Math.floor(t / RATIO));
                const cond = kits > 0 && (li.cond || ti.cond);
                const g = w < nowIdx ? "past" : kits <= 0 ? "g0" : kits === 1 ? "g1" : kits === 2 ? "g2" : kits <= 4 ? "g3" : "g4";
                const gated = w >= nowIdx && w < nowIdx + leadWeeks;
                return (
                  <div key={wk} className={"cell " + g + (gated ? " gated" : "") + (w === nowIdx ? " now" : "") + (cond ? " cond" : "")}
                    title={fmtWeekFull(wk) + (w < nowIdx ? " — past" : ` — up to ${kits} kits free (${l} lifts, ${t} ${trayLabel})` + (gated ? ". Inside site-readiness window." : "") + (cond ? ". Conditional: a promise here deepens an existing later shortfall." : ""))}>
                    <div className="k">{w < nowIdx ? "·" : kits}</div><div className="d">{fmtWeek(wk)}</div>
                  </div>
                );
              })}
            </div>
            <div className="heat-legend">
              <span>Free {trayType}-tray kits per week (1 lift + {RATIO} trays), after commitments, holds and buffer.</span>
              <span className="lg"><span className="sw" style={{ outline: "1.5px dashed #6B5320", outlineOffset: -1 }} /> inside site-readiness window</span>
              <span className="lg"><span className="sw" style={{ borderBottom: "2px dashed " + T.red }} /> conditional — deepens an existing later shortfall</span>
            </div>
          </div>
        </section>

        {/* ══ 2. Calendar ══ */}
        <section className="card">
          <div className="card-head">
            <div>
              <h2>Deployments, build plan &amp; deployable inventory</h2>
              <p className="sub">The whole plan on one grid, like the workbook — but every cell is a typed record. Click a row to edit. Build cells are editable by the plan owner and create a draft for approval.</p>
            </div>
            <div className="head-actions">
              <div className="seg" role="group" aria-label="Focus window">
                {[["all", "Full horizon"], [8, "Next 8 wks"], [13, "Next 13 wks"]].map(([k, l]) => <button key={k} className={focus === k ? "on" : ""} onClick={() => setFocus(k)}>{l}</button>)}
              </div>
              <button className="btn" onClick={() => setEditing("new")}>+ Add deployment</button>
              <label className="link-toggle"><input type="checkbox" checked={showSupply} onChange={(e) => setShowSupply(e.target.checked)} /> Supply detail rows</label>
            </div>
          </div>
          <div className="legend">
            {STAGE_ORDER.map((k) => <span key={k} className={"stage-chip st-" + k} title={STAGES[k].desc}>{STAGES[k].label}</span>)}
            <span className="lg dim">Qty colors:</span>
            <span className="lg" style={{ color: T.amber }}>lifts</span><span className="lg" style={{ color: T.sky }}>heavy trays</span><span className="lg" style={{ color: T.pink }}>light trays</span>
            <span className="lg dim">· counted in coverage:</span>
            <label className="link-toggle"><input type="checkbox" checked={state.params.countNegotiation} onChange={(e) => update((s) => ({ ...s, params: { ...s.params, countNegotiation: e.target.checked } }))} /> negotiation</label>
            <label className="link-toggle"><input type="checkbox" checked={state.params.countSoft} onChange={(e) => update((s) => ({ ...s, params: { ...s.params, countSoft: e.target.checked } }))} /> soft holds</label>
          </div>

          <div className="grid-scroll">
            <table className="grid">
              <thead>
                <tr>
                  <th className="sticky lbl">Week of</th>
                  {vweeks.map(([w, i]) => (
                    <th key={w} className={(i === nowIdx ? "now" : "") + (i < nowIdx ? " past" : "")}>
                      <div className="q">{(i === 0 || toDate(w).getMonth() !== toDate(weeks[i - 1]).getMonth()) ? MONTHS[toDate(w).getMonth()] : ""}</div>
                      <div>{toDate(w).getDate()}</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sortedDemand.map((d) => (
                  <tr key={d.id} className={"dep" + (d.review === "proposed" ? " proposed" : "")} onClick={() => setEditing(d)} tabIndex={0} onKeyDown={(e) => { if (e.key === "Enter") setEditing(d); }}>
                    <td className="sticky lbl">
                      <div className="cust">{d.customer}{d.review === "proposed" ? <span className="rev" title="Awaiting planner review">review</span> : null}</div>
                      <div className="site"><StageChip stage={d.stage} />{d.site ? <span className="dim"> {d.site}</span> : null}{d.stage === "soft" && d.expiresAt ? <span className={"dim" + (toDate(d.expiresAt) < today ? " hot-text" : "")}> · {toDate(d.expiresAt) < today ? "expired" : "expires " + fmtWeek(d.expiresAt)}</span> : null}</div>
                    </td>
                    {vweeks.map(([w, i]) => (
                      <td key={w} className={(i === nowIdx ? "now" : "") + (i < nowIdx ? " past" : "")}>
                        {i === d.week ? <span className={"pill st-" + d.stage} title={`${d.customer}: ${d.sl || 0} lifts, ${d.ht || 0} heavy, ${d.lt || 0} light — ${STAGES[d.stage].label}`}><Qty d={d} /></span> : null}
                      </td>
                    ))}
                  </tr>
                ))}
                {sortedDemand.length === 0 && <tr><td className="sticky lbl empty" colSpan={view.length + 1}>No deployments yet. Add one, or place a soft hold from the availability check above.</td></tr>}

                {PRODUCTS.map((p) => {
                  const meta = PRODUCT_META[p]; const prod = state.products[p];
                  const planB = state.draft ? state.draft.builds[p] : state.plan.builds[p];
                  return (
                    <React.Fragment key={p}>
                      <tr className="sep"><td className="sticky lbl" colSpan={view.length + 1}><span style={{ color: meta.color }}>{meta.name}</span> <span className="dim">· on hand {prod.opening} at start · buffer {prod.buffer} · max {prod.maxRate}/wk · demand counted: {stages.map((s) => STAGES[s].short).join(" ")}</span></td></tr>
                      <tr className="num">
                        <td className="sticky lbl">Build plan <span className="dim">{state.draft ? "(draft)" : state.plan.version}</span></td>
                        {vweeks.map(([w, i]) => {
                          const past = i < nowIdx; const actual = state.actuals[p][i];
                          const changed = state.draft && state.draft.builds[p][i] !== state.plan.builds[p][i];
                          return (
                            <td key={w} className={(i === nowIdx ? "now" : "") + (past ? " past" : "") + (changed ? " changed" : "")}>
                              {past ? (
                                <span className={"past-build" + (actual != null && actual !== planB[i] ? " miss" : "")} title={`Plan ${planB[i]}${actual != null ? `, actual ${actual}` : ", actual not keyed"}`}>{actual != null ? actual : planB[i]}{actual != null && actual !== planB[i] ? <small>/{planB[i]}</small> : null}</span>
                              ) : (
                                <input className={"cellin" + (planB[i] > prod.maxRate ? " over" : "")} type="number" min="0" max="99" value={planB[i]} aria-label={`${meta.name} build week of ${fmtWeek(w)}`} onChange={(e) => setBuild(p, i, e.target.value)} onFocus={(e) => e.target.select()} />
                              )}
                            </td>
                          );
                        })}
                      </tr>
                      {showSupply && (
                        <>
                          <tr className="num supply">
                            <td className="sticky lbl">Actual built <span className="dim">(past weeks)</span></td>
                            {vweeks.map(([w, i]) => (
                              <td key={w} className={(i === nowIdx ? "now" : "") + (i < nowIdx ? " past" : "")}>
                                {i < nowIdx ? <input className="cellin" type="number" min="0" max="99" placeholder="–" value={state.actuals[p][i] == null ? "" : state.actuals[p][i]} aria-label={`${meta.name} actual week of ${fmtWeek(w)}`} onChange={(e) => setActual(p, i, e.target.value)} onFocus={(e) => e.target.select()} /> : null}
                              </td>
                            ))}
                          </tr>
                          <tr className="num supply">
                            <td className="sticky lbl">Returns / catch-up <span className="dim">(±)</span></td>
                            {vweeks.map(([w, i]) => (
                              <td key={w} className={(i === nowIdx ? "now" : "") + (i < nowIdx ? " past" : "")}>
                                <input className="cellin" type="number" min="-99" max="99" value={state.adjust[p][i]} aria-label={`${meta.name} adjustment week of ${fmtWeek(w)}`} onChange={(e) => setAdjust(p, i, e.target.value)} onFocus={(e) => e.target.select()} />
                              </td>
                            ))}
                          </tr>
                          <tr className="num supply">
                            <td className="sticky lbl">Demand counted</td>
                            {vweeks.map(([w, i]) => <td key={w} className={(i === nowIdx ? "now" : "") + (i < nowIdx ? " past" : "")}>{proj.dem[p][i] ? <span className="dem">−{proj.dem[p][i]}</span> : <span className="dim">·</span>}</td>)}
                          </tr>
                        </>
                      )}
                      <tr className="num end">
                        <td className="sticky lbl">Deployable inventory</td>
                        {vweeks.map(([w, i]) => {
                          const v = proj.ending[p][i];
                          return <td key={w} className={(i === nowIdx ? "now" : "") + (i < nowIdx ? " past" : "")}><span className={"bal " + cellClass(v, prod.buffer)} title={`${meta.name}, end of week ${fmtWeek(w)}: ${v}${approvedProj ? ` (approved plan: ${approvedProj.ending[p][i]})` : ""}`}>{v}</span></td>;
                        })}
                      </tr>
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
          <div className="hint">Ending balance = prior + builds completing that week + returns/catch-up − demand counted. Red = short; amber = inside the production buffer. Past weeks use keyed actuals where present (actual/plan shown when they differ).</div>

          {/* rollups */}
          <div className="rollup-wrap">
            <table className="rollup">
              <thead><tr><th>Month</th>{PRODUCTS.map((p) => <th key={p} colSpan={3} style={{ color: PRODUCT_META[p].color }}>{PRODUCT_META[p].name}</th>)}</tr>
                <tr><th /> {PRODUCTS.map((p) => <React.Fragment key={p}><th>Demand</th><th>Built</th><th>End</th></React.Fragment>)}</tr></thead>
              <tbody>{rollup.map((r) => (
                <tr key={r.key}><td>{r.key}</td>{PRODUCTS.map((p) => <React.Fragment key={p}><td className="n">{r.dem[p] || "–"}</td><td className="n">{r.build[p] || "–"}</td><td className={"n " + (r.end[p] < 0 ? "neg" : "")}>{r.end[p]}</td></React.Fragment>)}</tr>
              ))}</tbody>
            </table>
          </div>
        </section>

        {/* ══ 3. Charts ══ */}
        <div className="two">
          <section className="card">
            <h3>Deployable inventory by week{state.draft ? " — draft (solid) vs approved (faint)" : ""}{askMode === "when" && ask && ask.shipWeek != null ? " — this deal overlaid (dashed)" : ""}</h3>
            <ResponsiveContainer width="100%" height={260}>
              <ComposedChart data={chartData} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
                <CartesianGrid stroke={T.borderSoft} vertical={false} />
                <XAxis dataKey="wk" tick={tickStyle} interval={2} stroke={T.border} />
                <YAxis tick={tickStyle} allowDecimals={false} stroke={T.border} />
                <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: T.text }} />
                <Legend wrapperStyle={{ fontSize: 12, color: T.sub }} />
                <ReferenceLine y={0} stroke={T.red} strokeWidth={1} />
                <ReferenceLine x={fmtWeek(weeks[nowIdx])} stroke={T.indigoSoft} strokeDasharray="3 3" label={{ value: "now", fill: T.indigoSoft, fontSize: 10, position: "insideTopLeft" }} />
                {approvedProj && PRODUCTS.map((p) => <Line key={p} type="stepAfter" dataKey={"approved_" + p} name={PRODUCT_META[p].name + " (approved)"} stroke={PRODUCT_META[p].color} strokeOpacity={0.35} strokeWidth={1.5} dot={false} legendType="none" />)}
                {PRODUCTS.map((p) => <Line key={p} type="stepAfter" dataKey={PRODUCT_META[p].name} stroke={PRODUCT_META[p].color} strokeWidth={2.5} dot={false} />)}
                {askMode === "when" && ask && ask.shipWeek != null && <Line type="stepAfter" dataKey="simSl" name="SlipLifts after deal" stroke={T.amber} strokeWidth={2} strokeDasharray="5 4" dot={false} />}
                {askMode === "when" && ask && ask.shipWeek != null && <Line type="stepAfter" dataKey="simTray" name={PRODUCT_META[trayKey].name + "s after deal"} stroke={trayAccent} strokeWidth={2} strokeDasharray="5 4" dot={false} />}
              </ComposedChart>
            </ResponsiveContainer>
          </section>
          <section className="card">
            <h3>Finished goods vs. the {fmt$k(state.params.cap)} exposure cap</h3>
            <ResponsiveContainer width="100%" height={260}>
              <ComposedChart data={chartData} margin={{ top: 8, right: 12, left: 4, bottom: 0 }}>
                <CartesianGrid stroke={T.borderSoft} vertical={false} />
                <XAxis dataKey="wk" tick={tickStyle} interval={2} stroke={T.border} />
                <YAxis tick={tickStyle} tickFormatter={fmt$k} stroke={T.border} />
                <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: T.text }} formatter={(v) => fmt$(v)} />
                <ReferenceLine y={state.params.cap} stroke={T.red} strokeWidth={1.5} strokeDasharray="6 4" label={{ value: "cap", fill: T.red, fontSize: 11, position: "insideTopRight" }} />
                <Area type="stepAfter" dataKey="Finished goods $" stroke={T.indigoSoft} strokeWidth={2} fill={T.indigo} fillOpacity={0.14} />
              </ComposedChart>
            </ResponsiveContainer>
            <div className="hint">Unit values: SlipLift {fmt$(state.products.sl.cost)}, heavy tray {fmt$(state.products.ht.cost)}, light tray {state.products.lt.cost ? fmt$(state.products.lt.cost) : "not set (edit in assumptions)"}.</div>
          </section>
        </div>

        {/* ══ 4. Signals + Governance ══ */}
        <div className="two">
          <section className="card">
            <div className="card-head"><div><h2>Signals</h2><p className="sub">Every alert names its owner. Nothing here is just a negative cell.</p></div></div>
            <div className="signals">
              {signals.length === 0 && <div className="signal ok"><span><b>All clear.</b> Coverage stays above buffer, plan is inside capacity, supply inputs are fresh, the review queue is empty.</span></div>}
              {signals.map((s) => (
                <div key={s.id} className={"signal " + s.sev + (s.ack && state.acks[s.id] ? " acked" : "")}>
                  <div className="sig-body">
                    <div className="sig-title"><b>{s.title}</b><span className="owner">{OWNERS[s.owner]}</span></div>
                    <div>{s.body}</div>
                    {s.queue && <div className="sig-actions">{s.queue.map((d) => (
                      <span key={d.id} className="queue-item"><span className="cust">{d.customer}</span> {fmtWeek(weeks[d.week])} <Qty d={d} /> <StageChip stage={d.stage} />
                        <button className="mini" onClick={() => setReview(d.id, "accepted")}>Accept</button>
                        <button className="mini" onClick={() => setEditing(d)}>Amend</button>
                        <button className="mini danger" onClick={() => setReview(d.id, "rejected")}>Reject</button></span>
                    ))}</div>}
                    {s.release && <div className="sig-actions">{s.release.map((d) => <button key={d.id} className="mini" onClick={() => releaseMaterial(d.id)}>Release material: {d.customer} {fmtWeek(weeks[d.week])}</button>)}</div>}
                    {s.expired && <div className="sig-actions">{s.expired.map((d) => (
                      <span key={d.id} className="queue-item"><span className="cust">{d.customer}</span> {fmtWeek(weeks[d.week])} <Qty d={d} /> <span className="dim">expired {d.expiresAt}</span>
                        <button className="mini" onClick={() => extendHold(d.id)}>Extend {state.params.holdDays}d</button>
                        <button className="mini danger" onClick={() => setReview(d.id, "rejected")}>Release</button></span>
                    ))}</div>}
                    {s.ack && !state.acks[s.id] && <div className="sig-actions"><button className="mini" onClick={() => ackSignal(s.id)}>Acknowledge (leadership)</button></div>}
                    {s.ack && state.acks[s.id] && <div className="dim small-note">Acknowledged {state.acks[s.id]}</div>}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="card gov">
            <div className="card-head"><div><h2>Build plan governance</h2><p className="sub">The plan owner edits build cells; a draft appears here. Jeff approves in the Wednesday consensus meeting. Anything else is an off-cycle override — allowed, flagged, counted.</p></div></div>
            <div className="plan-meta">
              <div><span className="k">In force</span><b>{state.plan.version}</b></div>
              <div><span className="k">Approved</span>{state.plan.approvedAt} · {state.plan.approvedBy}</div>
              <div><span className="k">Supersedes</span>{state.plan.supersedes || "—"}</div>
              <div><span className="k">Reason</span>{REASONS[state.plan.reasonType] || "—"}{state.plan.offCycle ? <span className="oc"> off-cycle</span> : null}</div>
              <div><span className="k">Off-cycle this quarter</span><b className={offCycleCount >= 3 ? "hot-text" : ""}>{offCycleCount}</b>{offCycleCount >= 3 ? " → constraint review" : ""}</div>
              <div className="consensus"><span className="k">Signed consensus number</span><input value={state.consensus} placeholder="e.g. Q4 2026: 20 SlipLifts / 60 HT / 16 LT" onChange={(e) => update((s) => ({ ...s, consensus: e.target.value }))} /></div>
            </div>

            {!state.draft && <div className="empty">No draft. Edit any future build cell in the calendar to propose a change.</div>}
            {state.draft && (
              <div className="draft">
                <div className="draft-head"><b>Draft plan</b>{offCycle ? <span className="oc">off-cycle override (today is not Wednesday)</span> : <span className="onc">on cadence</span>}</div>
                <div className="delta">
                  {draftDelta.length === 0 && <span className="dim">No cells differ from {state.plan.version}.</span>}
                  {draftDelta.slice(0, 12).map((d) => <span key={d.p + d.t} className="delta-item"><span style={{ color: PRODUCT_META[d.p].color }}>{PRODUCT_META[d.p].short}</span> {fmtWeek(weeks[d.t])}: {d.from} → <b>{d.to}</b></span>)}
                  {draftDelta.length > 12 && <span className="dim">+{draftDelta.length - 12} more</span>}
                </div>
                {approvedProj && (
                  <div className="ramif">Ramifications: {PRODUCTS.map((p) => {
                    const a = Math.min(...approvedProj.ending[p].slice(nowIdx)), b = Math.min(...proj.ending[p].slice(nowIdx));
                    return <span key={p}><span style={{ color: PRODUCT_META[p].color }}>{PRODUCT_META[p].short}</span> min {a} → <b className={b < 0 ? "hot-text" : ""}>{b}</b>, year-end {approvedProj.ending[p][N - 1]} → <b>{proj.ending[p][N - 1]}</b> </span>;
                  })}</div>
                )}
                <label className="small" htmlFor="reason">Typed change reason</label>
                <select id="reason" value={state.draft.reasonType} onChange={(e) => update((s) => ({ ...s, draft: { ...s.draft, reasonType: e.target.value } }))}>
                  <option value="">— pick a reason —</option>
                  {Object.entries(REASONS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                </select>
                <label className="small" htmlFor="note">Note for the ledger</label>
                <input id="note" className="text" value={state.draft.note} onChange={(e) => update((s) => ({ ...s, draft: { ...s.draft, note: e.target.value } }))} placeholder="What changed and why, in one line" />
                <ul className="checklist">
                  {checklist.map((c) => <li key={c.label} className={c.ok ? "ok" : "no"}><span className="tick">{c.ok ? "✓" : "✗"}</span><span>{c.label}</span><span className="dim">{c.detail}</span></li>)}
                </ul>
                <div className="tag-actions">
                  <button className="btn" disabled={!canApprove} onClick={approve} title={canApprove ? "Approve and publish as the plan in force" : "Approve is blocked until every checklist item passes"}>Approve as Jeff → new version</button>
                  <button className="btn ghost" onClick={discardDraft}>Discard draft</button>
                </div>
              </div>
            )}

            <h4>Plan vs actual — last 4 weeks</h4>
            <table className="pva"><thead><tr><th>Week</th>{PRODUCTS.map((p) => <th key={p} style={{ color: PRODUCT_META[p].color }}>{PRODUCT_META[p].short} plan / actual</th>)}</tr></thead>
              <tbody>{nowIdx === 0 ? <tr><td colSpan={4} className="dim">Horizon starts this week.</td></tr> : weeks.slice(Math.max(0, nowIdx - 4), nowIdx).map((w, j) => { const i = Math.max(0, nowIdx - 4) + j; return (
                <tr key={w}><td>{fmtWeek(w)}</td>{PRODUCTS.map((p) => { const a = state.actuals[p][i]; const pl = state.plan.builds[p][i]; return <td key={p} className={"n " + (a == null ? "dim" : a < pl ? "neg" : "")}>{pl} / {a == null ? "–" : a}</td>; })}</tr>
              ); })}</tbody></table>

            <h4>Ledger</h4>
            <ul className="ledger">{state.ledger.slice(0, 8).map((l) => <li key={l.id}><span className="mono">{l.at}</span> <b>{l.who}</b> {l.what}</li>)}</ul>
          </section>
        </div>

        {/* ══ 5. Demand-gap log ══ */}
        <section className="card">
          <div className="card-head"><div><h2>Demand we turned away</h2><p className="sub">Logged from the availability check when the offered date was later than the deal needed. This is the plan owner's evidence for a rate change.</p></div></div>
          {state.gaps.length === 0 ? <div className="empty">Nothing logged yet.</div> : (
            <table className="gaps"><thead><tr><th>Logged</th><th>Customer</th><th>Config</th><th>Needed</th><th>Offered</th><th>Constraint</th><th /></tr></thead>
              <tbody>{state.gaps.map((g) => (
                <tr key={g.id}><td className="mono">{g.createdAt}</td><td className="cust">{g.customer}</td><td><Qty d={g} /></td><td className="mono">{fmtWeek(weeks[g.neededWeek])}</td><td className="mono">{g.offeredWeek == null ? "not in plan" : fmtWeek(weeks[g.offeredWeek])}</td><td>{g.constraint}</td>
                  <td><button className="rm" aria-label="Remove" onClick={() => update((s) => ({ ...s, gaps: s.gaps.filter((x) => x.id !== g.id) }))}>×</button></td></tr>
              ))}</tbody></table>
          )}
        </section>

        {/* ══ 6. Assumptions & data ══ */}
        <section className="card">
          <div className="card-head" style={{ cursor: "pointer" }} onClick={() => setShowAssumptions(!showAssumptions)}>
            <div><h2>Assumptions &amp; data {showAssumptions ? "▾" : "▸"}</h2><p className="sub">Unit costs, buffers, capacity, lead times, cap. Export/import the plan as JSON. {saved ? "Autosaved in this browser." : "Autosave unavailable in this browser."}</p></div>
          </div>
          {showAssumptions && (
            <div className="assump">
              <div className="assump-grid">
                {PRODUCTS.map((p) => (
                  <div key={p} className="assump-card">
                    <h4 style={{ color: PRODUCT_META[p].color }}>{PRODUCT_META[p].name}</h4>
                    {[["opening", "On hand at start"], ["buffer", "Production buffer (held out of ATP)"], ["maxRate", "Max builds / week (capacity)"], ["cost", "Unit value $"]].map(([k, lbl]) => (
                      <label key={k} className="row"><span>{lbl}</span><input type="number" value={state.products[p][k]} onChange={(e) => update((s) => ({ ...s, products: { ...s.products, [p]: { ...s.products[p], [k]: Number(e.target.value) || 0 } } }))} /></label>
                    ))}
                  </div>
                ))}
                <div className="assump-card">
                  <h4>Policy</h4>
                  {[["leadWeeks", "Site-readiness lead time (weeks)"], ["protectWeeks", "Protect commitments for (weeks)"], ["materialLeadWeeks", "Material lead time (weeks)"], ["holdDays", "Soft hold expiry (days)"], ["kitHeavy", "Heavy trays per lift"], ["kitLight", "Light trays per lift"], ["cap", "Finished-goods exposure cap $"]].map(([k, lbl]) => (
                    <label key={k} className="row"><span>{lbl}</span><input type="number" value={state.params[k]} onChange={(e) => update((s) => ({ ...s, params: { ...s.params, [k]: Number(e.target.value) || 0 } }))} /></label>
                  ))}
                </div>
              </div>
              <div className="tag-actions">
                <button className="btn ghost" onClick={exportJson}>Export plan (JSON)</button>
                <button className="btn ghost" onClick={() => fileRef.current && fileRef.current.click()}>Import plan</button>
                <input ref={fileRef} type="file" accept="application/json" hidden onChange={(e) => { if (e.target.files && e.target.files[0]) importJson(e.target.files[0]); e.target.value = ""; }} />
                <button className="btn danger" onClick={resetSeed}>Reset to seed</button>
              </div>
              <div className="hint">{state.meta.seedNote} Build rows are units completing (deployable) in that week — one convention everywhere. Aux batteries, charge carts, and controllers follow the kit and are not gating today.</div>
            </div>
          )}
        </section>

        <div className="foot">
          Who this is for: <b>Sales</b> gets a date and reserves it in one place. <b>Production</b> sees the plan it builds to and keys actuals against a named version. <b>Supply Chain</b> sees when material is released. <b>Leadership</b> approves plan changes with the ramifications in view. Dates are planning promises, not contractual delivery dates.
        </div>
      </div>

      {editing && <DeploymentEditor key={editing === "new" ? "new" : editing.id} initial={editing === "new" ? null : editing} weeks={weeks} nowIdx={nowIdx}
        onClose={() => setEditing(null)}
        onSave={(d) => { saveDeployment(d); setEditing(null); toast("Deployment saved"); }}
        onDelete={(id) => { removeDeployment(id); setEditing(null); toast("Deployment removed"); }} />}

      {flash && <div className="toast" role="status">{flash}</div>}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════
   Deployment editor (guided entry — replaces editing a cell)
   ═══════════════════════════════════════════════════════════════════ */
function DeploymentEditor({ initial, weeks, nowIdx, onClose, onSave, onDelete }) {
  const [d, setD] = useState(initial || { id: uid(), customer: "", site: "", week: Math.min(weeks.length - 1, nowIdx + 8), sl: 2, ht: 6, lt: 0, stage: "negotiation", source: "manual", review: "accepted", materialReleased: false, note: "", createdAt: iso(new Date()) });
  const set = (k, v) => setD((x) => ({ ...x, [k]: v }));
  const valid = d.customer.trim().length > 0 && (d.sl > 0 || d.ht > 0 || d.lt > 0);
  useEffect(() => { const h = (e) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", h); return () => window.removeEventListener("keydown", h); }, [onClose]);
  return (
    <div className="modal-bg" onClick={onClose}>
      <div className="modal" role="dialog" aria-modal="true" aria-label="Deployment" onClick={(e) => e.stopPropagation()}>
        <h3>{initial ? "Edit deployment" : "New deployment"}</h3>
        <div className="form">
          <label>Customer<input value={d.customer} autoFocus onChange={(e) => set("customer", e.target.value)} placeholder="Customer or placeholder name" /></label>
          <label>Site<input value={d.site} onChange={(e) => set("site", e.target.value)} placeholder="City, ST" /></label>
          <label>Delivery week<select value={d.week} onChange={(e) => set("week", +e.target.value)}>{weeks.map((w, i) => <option key={w} value={i}>{fmtWeekFull(w)}{i < nowIdx ? " (past)" : ""}</option>)}</select></label>
          <label>Stage<select value={d.stage} onChange={(e) => set("stage", e.target.value)}>{STAGE_ORDER.map((k) => <option key={k} value={k}>{STAGES[k].label} · {STAGES[k].pct}%</option>)}</select></label>
          <div className="qty-row">
            <label style={{ color: T.amber }}>SlipLifts<input type="number" min="0" value={d.sl} onChange={(e) => set("sl", clampInt(e.target.value, 0, 99))} /></label>
            <label style={{ color: T.sky }}>Heavy trays<input type="number" min="0" value={d.ht} onChange={(e) => set("ht", clampInt(e.target.value, 0, 99))} /></label>
            <label style={{ color: T.pink }}>Light trays<input type="number" min="0" value={d.lt} onChange={(e) => set("lt", clampInt(e.target.value, 0, 99))} /></label>
          </div>
          <label>Source<select value={d.source} onChange={(e) => set("source", e.target.value)}><option value="crm">CRM opportunity</option><option value="manual">Manual / placeholder</option><option value="ask">Sales availability check</option></select></label>
          <label>Review<select value={d.review} onChange={(e) => set("review", e.target.value)}><option value="proposed">Proposed (awaiting planner)</option><option value="accepted">Accepted into plan</option><option value="rejected">Rejected</option></select></label>
          <label className="check"><input type="checkbox" checked={!!d.materialReleased} onChange={(e) => set("materialReleased", e.target.checked)} /> Material released to purchasing</label>
          <label>Note<input value={d.note} onChange={(e) => set("note", e.target.value)} placeholder="Spares composition, PO number, transfer order…" /></label>
          <div className="hint">{STAGES[d.stage].desc}</div>
        </div>
        <div className="tag-actions">
          <button className="btn" disabled={!valid} onClick={() => onSave({ ...d, customer: d.customer.trim() })}>Save</button>
          <button className="btn ghost" onClick={onClose}>Cancel</button>
          {initial && <button className="btn danger" style={{ marginLeft: "auto" }} onClick={() => onDelete(d.id)}>Remove</button>}
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════
   Styles (SlipOS dark; single theme like the existing mock)
   ═══════════════════════════════════════════════════════════════════ */
const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');
.sdp *{box-sizing:border-box;}
.sdp{min-height:100vh;background:${T.canvas};color:${T.text};font-family:'Inter',system-ui,sans-serif;padding:0 0 48px;font-size:13px;}
.sdp .mono{font-family:'JetBrains Mono',monospace;}
.sdp .dim{color:${T.muted};font-weight:400;}
.sdp .hot-text{color:${T.red};}
.head{padding:16px 28px;display:flex;flex-wrap:wrap;align-items:center;gap:14px;justify-content:space-between;border-bottom:1px solid ${T.border};}
.brand{font-weight:600;font-size:13px;letter-spacing:.42em;text-transform:uppercase;color:${T.sub};}
.title{font-size:17px;font-weight:700;margin-top:3px;letter-spacing:-.01em;}
.title .dim{font-size:12.5px;font-weight:500;}
.chips{display:flex;gap:8px;flex-wrap:wrap;}
.chip{font-size:12px;font-weight:500;padding:7px 12px;border-radius:8px;background:${T.panel};border:1px solid ${T.border};color:${T.sub};}
.chip b{color:${T.text};font-weight:600;}
.chip.ok{border-color:#1E4636;color:#7EDDB4;background:#0E1E18;}
.chip.hot{border-color:#4A2626;color:#F5A19B;background:#1E1112;}
.who{font:500 12px 'Inter';padding:7px 10px;border:1px solid ${T.border};border-radius:8px;background:${T.inset};color:${T.text};width:190px;}
.who::placeholder{color:${T.muted};}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin-top:12px;}
.kpi{background:${T.panel};border:1px solid ${T.border};border-radius:10px;padding:10px 14px;display:grid;gap:4px;}
.kpi.bad{border-color:#4A2626;}
.kpi-name{font:600 10.5px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2px;}
.kpi-row{display:flex;justify-content:space-between;gap:10px;font-size:12px;color:${T.sub};}
.kpi-row b{color:${T.text};font-variant-numeric:tabular-nums;font-weight:700;}
.kpi-row b small{color:${T.warn};margin-left:2px;}
.slots{display:flex;flex-direction:column;gap:5px;padding-bottom:6px;}
.slots-k{font:600 10px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:${T.muted};}
.slot{display:flex;gap:6px;align-items:baseline;font:700 12px 'Inter';padding:5px 9px;border-radius:7px;border:1px solid ${T.border};background:${T.inset};color:${T.sub};cursor:pointer;}
.slot small{font:500 10px 'JetBrains Mono',monospace;color:${T.muted};}
.slot.on{border-color:${T.indigo};color:${T.text};background:rgba(110,98,245,.14);}
.seg{display:inline-flex;border:1px solid ${T.border};border-radius:8px;overflow:hidden;background:${T.inset};padding:2px;gap:2px;}
.seg button{font:500 11.5px 'Inter';padding:6px 10px;border:none;background:transparent;cursor:pointer;color:${T.sub};border-radius:6px;}
.seg button.on{background:${T.indigo};color:#fff;font-weight:600;}
.miles{display:flex;gap:0;margin-top:14px;overflow-x:auto;padding:12px 0 4px;border-top:1px dashed ${T.borderSoft};}
.mile{flex:1;min-width:130px;position:relative;padding:0 10px 0 0;}
.mile::before{content:"";position:absolute;top:6px;left:14px;right:0;height:1.5px;background:${T.border};}
.mile:last-child::before{display:none;}
.mile-dot{width:13px;height:13px;border-radius:50%;background:${T.canvas};border:3px solid ${T.indigo};position:relative;z-index:1;}
.mile.due .mile-dot{background:${T.warn};border-color:${T.warn};}
.mile-wk{font:600 12px 'JetBrains Mono',monospace;margin-top:8px;color:${T.text};}
.mile-label{font-size:11px;font-weight:600;color:${T.sub};line-height:1.35;margin-top:2px;}
.mile-owner{font-size:10.5px;color:${T.muted};margin-top:2px;}
.draft-dot{color:${T.warn};font-weight:600;}
.wrap{max-width:1400px;margin:0 auto;padding:0 20px;}
.cadence{display:flex;gap:6px;margin:16px 0 0;flex-wrap:wrap;align-items:stretch;}
.cad{flex:1;min-width:150px;display:flex;flex-direction:column;gap:2px;padding:8px 12px;border:1px solid ${T.borderSoft};border-radius:8px;background:${T.panel};}
.cad.now{border-color:${T.indigo};background:#161634;}
.cad-k{font:600 10px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:${T.muted};}
.cad.now .cad-k{color:${T.indigoSoft};}
.cad-t{font-weight:600;font-size:12.5px;}
.cad-w{font-size:11px;color:${T.muted};}
.cad-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
.card{background:${T.panel};border:1px solid ${T.border};border-radius:12px;padding:18px 20px;margin-top:16px;}
.card h2{font-size:16px;font-weight:700;margin:0;letter-spacing:-.01em;}
.card h3{font-weight:700;font-size:14px;margin:0 0 8px;}
.card h4{font-weight:700;font-size:12px;margin:18px 0 8px;text-transform:uppercase;letter-spacing:.1em;color:${T.sub};}
.card .sub{font-size:12px;color:${T.muted};margin:4px 0 0;line-height:1.5;max-width:70ch;}
.card-head{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:flex-start;}
.head-actions{display:flex;gap:12px;align-items:center;flex-wrap:wrap;}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
@media(max-width:1000px){.two{grid-template-columns:1fr;}}
.mode{display:inline-flex;background:${T.inset};border:1px solid ${T.border};border-radius:10px;overflow:hidden;padding:3px;gap:3px;}
.mode button{font:500 12.5px 'Inter';padding:7px 14px;border:none;background:transparent;color:${T.sub};cursor:pointer;border-radius:7px;}
.mode button.on{background:${T.indigo};color:#fff;font-weight:600;}
.hero{display:grid;grid-template-columns:auto 1fr;gap:20px 28px;align-items:center;margin-top:16px;}
@media(max-width:980px){.hero{grid-template-columns:1fr;}}
.inputs{display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap;}
.ask-side{display:flex;flex-direction:column;gap:6px;padding-bottom:4px;}
.stepper label{display:block;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:6px;}
.stepper-row{display:flex;align-items:stretch;border:1.5px solid var(--acc);border-radius:10px;overflow:hidden;background:${T.inset};}
.stepper-row button{width:40px;font:600 20px 'Inter';border:none;background:${T.panel};color:${T.sub};cursor:pointer;}
.stepper-row button:hover{background:var(--acc);color:#0A0D13;}
.stepper-row input{width:80px;border:none;text-align:center;font:700 34px 'Inter';color:${T.text};background:${T.inset};padding:4px 0;-moz-appearance:textfield;}
.stepper-row input::-webkit-outer-spin-button,.stepper-row input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0;}
.stepper-row input:focus{outline:none;background:#141a28;}
.tray-col{display:flex;flex-direction:column;gap:8px;}
.type-seg{display:flex;border:1px solid ${T.border};border-radius:8px;overflow:hidden;background:${T.inset};padding:2px;gap:2px;}
.type-seg button{flex:1;font:600 11px 'Inter';letter-spacing:.06em;text-transform:uppercase;padding:6px 10px;border:none;background:transparent;cursor:pointer;color:${T.muted};border-radius:6px;}
.type-seg button.h.on{background:#0E2334;color:${T.sky};}
.type-seg button.l.on{background:#2A1230;color:${T.pink};}
.link-toggle{display:flex;align-items:center;gap:7px;font-size:12px;color:${T.sub};font-weight:500;cursor:pointer;user-select:none;}
.link-toggle input{accent-color:${T.indigo};width:15px;height:15px;}
.sdp select,.sdp input.text,.sdp .hold-name,.sdp .consensus input{font:500 13px 'Inter';padding:8px 10px;border:1px solid ${T.border};border-radius:8px;background:${T.inset};color:${T.text};}
.sdp select:focus,.sdp input:focus{outline:2px solid ${T.indigo};outline-offset:0;}
label.small{display:block;font-size:11.5px;font-weight:600;color:${T.sub};margin:10px 0 4px;}
.tag{position:relative;border:1px dashed ${T.border};border-radius:12px;padding:16px 20px 16px 48px;background:${T.inset};display:flex;flex-wrap:wrap;gap:6px 24px;align-items:center;}
.tag::before{content:"";position:absolute;left:18px;top:50%;transform:translateY(-50%);width:12px;height:12px;border-radius:50%;background:${T.canvas};border:2px solid ${T.border};}
.tag.green{border-color:#2A6A4E;background:#0D1F17;}.tag.green::before{border-color:${T.green};}
.tag.tight{border-color:#6B5320;background:#1D1810;}.tag.tight::before{border-color:${T.warn};}
.tag.later,.tag.none{border-color:#6B3030;background:#1F1213;}.tag.later::before,.tag.none::before{border-color:${T.red};}
.verdict{font-weight:700;font-size:18px;letter-spacing:-.01em;line-height:1.1;}
.tag.green .verdict{color:${T.green}}.tag.tight .verdict{color:${T.warn}}.tag.later .verdict,.tag.none .verdict{color:${T.red}}.tag.idle .verdict{color:${T.muted}}
.stamp{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.01em;}
.stamp small{display:block;font:600 10px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:${T.muted};margin-bottom:4px;}
.tag-detail{font-size:12px;color:${T.sub};max-width:420px;line-height:1.5;}
.gap-note{color:${T.warn};font-weight:600;}
.tag-actions{display:flex;gap:8px;flex-basis:100%;margin-top:8px;flex-wrap:wrap;align-items:center;}
.btn{font:600 12px 'Inter';padding:8px 14px;border-radius:8px;border:1px solid ${T.indigo};background:${T.indigo};color:#fff;cursor:pointer;}
.btn.ghost{background:transparent;color:${T.indigoSoft};}
.btn.warn{background:transparent;border-color:${T.warn};color:${T.warn};}
.btn.danger{background:transparent;border-color:#6B3030;color:${T.red};}
.btn:hover:not(:disabled){filter:brightness(1.15);}
.btn:disabled{opacity:.45;cursor:not-allowed;}
.btn:focus-visible,.mini:focus-visible{outline:2px solid ${T.text};}
.mini{font:600 11px 'Inter';padding:4px 9px;border-radius:6px;border:1px solid ${T.border};background:${T.raise};color:${T.text};cursor:pointer;}
.mini.danger{color:${T.red};border-color:#4A2626;}
.hold-name{width:190px;}
.hold-name::placeholder{color:${T.muted};}
.heat-scroll{overflow-x:auto;padding-bottom:4px;margin-top:16px;}
.heat{display:flex;gap:3px;min-width:900px;}
.cell{flex:1;border-radius:6px;padding:7px 2px 6px;text-align:center;cursor:default;border:1px solid transparent;}
.cell .k{font:700 16px 'Inter';line-height:1;}
.cell .d{font:500 8.5px 'JetBrains Mono',monospace;opacity:.8;margin-top:4px;letter-spacing:.02em;}
.cell.past{background:transparent;color:${T.muted};border-color:${T.borderSoft};opacity:.6;}
.cell.g0{background:#12161F;color:#525C72;border-color:${T.borderSoft};}
.cell.g1{background:#251A0C;color:#C98A2B;}
.cell.g2{background:#33230C;color:${T.amber};}
.cell.g3{background:#0E241C;color:#4EC393;}
.cell.g4{background:#0F3226;color:#6EE7B7;}
.cell.gated{outline:1.5px dashed #6B5320;outline-offset:-2px;}
.cell.now{box-shadow:inset 0 0 0 1.5px ${T.indigoSoft};}
.cell.cond{border-bottom:2px dashed ${T.red};}
.heat-legend{display:flex;gap:14px;font-size:11px;color:${T.muted};margin-top:8px;flex-wrap:wrap;}
.lg{display:flex;align-items:center;gap:5px;font-size:11.5px;}
.sw{width:12px;height:12px;border-radius:3px;display:inline-block;}
.legend{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:12px;font-size:11.5px;color:${T.sub};}
.stage-chip{font:600 9.5px 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:5px;border:1.5px solid ${T.indigo};color:${T.indigoSoft};white-space:nowrap;}
.st-po{background:${T.indigo};color:#fff;border-style:solid;}
.st-contract{background:rgba(110,98,245,.28);border-style:solid;}
.st-negotiation{background:transparent;border-style:dashed;}
.st-soft{background:transparent;border-style:dotted;border-color:${T.sub};color:${T.sub};}
.st-estimate{background:transparent;border-style:dotted;border-color:${T.muted};color:${T.muted};opacity:.8;}
.grid-scroll{overflow-x:auto;margin-top:12px;border:1px solid ${T.borderSoft};border-radius:8px;}
table.grid{border-collapse:separate;border-spacing:0;font-size:12px;min-width:100%;}
table.grid th,table.grid td{padding:0;border-bottom:1px solid ${T.borderSoft};border-right:1px solid ${T.borderSoft};text-align:center;min-width:54px;height:34px;vertical-align:middle;}
table.grid th{font:600 11px 'JetBrains Mono',monospace;color:${T.sub};background:${T.raise};position:sticky;top:0;z-index:2;padding:4px 2px;}
table.grid th .q{font-size:9px;color:${T.muted};height:11px;letter-spacing:.08em;text-transform:uppercase;}
table.grid .sticky{position:sticky;left:0;z-index:3;background:${T.panel};text-align:left;padding:4px 10px;min-width:230px;border-right:1px solid ${T.border};}
table.grid th.sticky{background:${T.raise};z-index:4;}
table.grid td.now,table.grid th.now{background:rgba(110,98,245,.10);}
table.grid td.past,table.grid th.past{background:rgba(255,255,255,.015);}
table.grid tr.dep{cursor:pointer;}
table.grid tr.dep:hover td{background:rgba(110,98,245,.06);}
table.grid tr.dep:focus-visible{outline:2px solid ${T.indigoSoft};}
table.grid tr.proposed .sticky{border-left:3px solid ${T.warn};}
.cust{font-weight:600;color:${T.text};display:flex;gap:6px;align-items:center;}
.rev{font:600 9px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:${T.warn};border:1px solid ${T.warn};border-radius:4px;padding:1px 5px;}
.site{margin-top:3px;display:flex;gap:6px;align-items:center;font-size:11px;}
.pill{display:inline-flex;gap:4px;align-items:center;padding:3px 7px;border-radius:6px;border:1.5px solid ${T.indigo};font:700 12px 'JetBrains Mono',monospace;background:${T.inset};}
.pill.st-po{background:${T.indigo};}
.pill.st-po span{color:#fff !important;}
.pill.st-contract{background:rgba(110,98,245,.22);}
.pill.st-soft,.pill.st-estimate{border-color:${T.sub};}
.qty{display:inline-flex;gap:4px;font-variant-numeric:tabular-nums;}
table.grid tr.sep td{background:${T.raise};font-size:11.5px;font-weight:600;height:28px;border-right:none;text-align:left;}
table.grid tr.num td{font-variant-numeric:tabular-nums;}
table.grid tr.num .sticky{font-weight:500;color:${T.sub};}
table.grid tr.end .sticky{font-weight:600;color:${T.text};}
table.grid tr.supply td{background:rgba(255,255,255,.02);}
.cellin{width:100%;height:32px;border:none;background:transparent;color:${T.text};text-align:center;font:600 12px 'JetBrains Mono',monospace;-moz-appearance:textfield;}
.cellin::-webkit-outer-spin-button,.cellin::-webkit-inner-spin-button{-webkit-appearance:none;margin:0;}
.cellin:focus{outline:2px solid ${T.indigo};outline-offset:-2px;background:#141a28;}
.cellin.over{color:${T.red};}
table.grid td.changed{background:rgba(251,191,36,.12);}
.past-build{font:600 12px 'JetBrains Mono',monospace;color:${T.sub};}
.past-build.miss{color:${T.warn};}
.past-build small{font-size:9px;color:${T.muted};}
.dem{color:${T.sub};font:600 11.5px 'JetBrains Mono',monospace;}
.bal{display:inline-block;min-width:34px;padding:3px 6px;border-radius:5px;font:700 12px 'JetBrains Mono',monospace;}
.bal.ok{color:${T.text};}
.bal.buf{color:${T.warn};background:rgba(251,191,36,.10);}
.bal.neg{color:#fff;background:#8B2F2F;}
.hint{font-size:11px;color:${T.muted};margin-top:8px;line-height:1.55;}
.rollup-wrap{overflow-x:auto;margin-top:14px;}
table.rollup,table.pva,table.gaps{border-collapse:collapse;font-size:12px;width:100%;}
table.rollup th,table.pva th,table.gaps th{font:600 10px 'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.08em;color:${T.muted};text-align:left;padding:5px 8px;border-bottom:1px solid ${T.border};}
table.rollup td,table.pva td,table.gaps td{padding:6px 8px;border-bottom:1px solid ${T.borderSoft};color:${T.sub};}
table.rollup th{text-align:center;}
td.n{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;color:${T.text};}
td.n.neg{color:${T.red};}
table.gaps td.cust{color:${T.text};font-weight:600;}
.signals{display:grid;gap:10px;margin-top:12px;}
.signal{display:flex;gap:10px;font-size:12.5px;line-height:1.55;color:${T.sub};background:${T.inset};border:1px solid ${T.borderSoft};border-left:3px solid ${T.indigo};padding:11px 13px;border-radius:8px;}
.signal.red{border-left-color:${T.red};}
.signal.amber{border-left-color:${T.warn};}
.signal.ok{border-left-color:${T.green};}
.signal.acked{opacity:.7;}
.sig-body{flex:1;min-width:0;}
.sig-title{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:2px;}
.sig-title b{color:${T.text};}
.owner{font:600 10px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:${T.indigoSoft};border:1px solid ${T.border};border-radius:4px;padding:1px 6px;}
.sig-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;align-items:center;}
.queue-item{display:inline-flex;gap:6px;align-items:center;flex-wrap:wrap;padding:6px 8px;border:1px solid ${T.borderSoft};border-radius:6px;background:${T.panel};}
.small-note{font-size:11px;margin-top:6px;}
.plan-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px 18px;margin-top:12px;font-size:12.5px;}
.plan-meta .k{display:block;font:600 10px 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:${T.muted};margin-bottom:3px;}
.plan-meta .consensus{grid-column:1 / -1;}
.plan-meta .consensus input{width:100%;}
.oc{color:${T.warn};font-weight:600;}
.onc{color:${T.green};font-weight:600;}
.draft{margin-top:14px;padding:14px;border:1px dashed ${T.warn};border-radius:10px;background:rgba(251,191,36,.05);}
.draft-head{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;}
.delta{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;}
.delta-item{font:500 11.5px 'JetBrains Mono',monospace;padding:3px 7px;border-radius:5px;background:${T.inset};border:1px solid ${T.borderSoft};color:${T.sub};}
.delta-item b{color:${T.text};}
.ramif{font-size:12px;color:${T.sub};margin-top:8px;line-height:1.7;}
.ramif span{margin-right:10px;}
.checklist{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:5px;}
.checklist li{display:grid;grid-template-columns:18px 1fr auto;gap:8px;font-size:12px;align-items:baseline;}
.checklist li.ok .tick{color:${T.green};font-weight:700;}
.checklist li.no .tick{color:${T.red};font-weight:700;}
.checklist li.no{color:${T.text};}
.ledger{list-style:none;margin:0;padding:0;font-size:12px;color:${T.sub};display:grid;gap:5px;}
.ledger b{color:${T.text};}
.empty{font-size:12px;color:${T.muted};padding:10px 4px;line-height:1.5;}
.rm{border:none;background:none;color:${T.red};font-weight:700;cursor:pointer;font-size:14px;line-height:1;}
.assump{margin-top:12px;}
.assump-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;}
.assump-card{background:${T.inset};border:1px solid ${T.borderSoft};border-radius:8px;padding:12px;}
.assump-card h4{margin:0 0 8px;}
.assump-card .row{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12px;color:${T.sub};padding:4px 0;}
.assump-card .row input{width:110px;font:600 12px 'JetBrains Mono',monospace;padding:5px 8px;border:1px solid ${T.border};border-radius:6px;background:${T.panel};color:${T.text};text-align:right;}
.foot{margin-top:24px;font-size:11.5px;color:${T.muted};line-height:1.65;max-width:100ch;}
.foot b{color:${T.sub};}
.modal-bg{position:fixed;inset:0;background:rgba(5,7,12,.7);display:flex;align-items:center;justify-content:center;z-index:50;padding:16px;}
.modal{background:${T.panel};border:1px solid ${T.border};border-radius:12px;padding:20px;width:min(560px,100%);max-height:92vh;overflow:auto;}
.modal h3{margin:0 0 12px;font-size:15px;}
.form{display:grid;gap:10px;}
.form label{display:grid;gap:4px;font-size:11.5px;font-weight:600;color:${T.sub};}
.form input,.form select{font:500 13px 'Inter';padding:8px 10px;border:1px solid ${T.border};border-radius:8px;background:${T.inset};color:${T.text};}
.form .qty-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.form .check{display:flex;align-items:center;gap:8px;}
.form .check input{accent-color:${T.indigo};}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:${T.text};color:${T.canvas};font-weight:600;font-size:12.5px;padding:9px 14px;border-radius:8px;z-index:60;box-shadow:0 6px 24px rgba(0,0,0,.4);}
@media (prefers-reduced-motion: reduce){.sdp *{transition:none!important;animation:none!important;}}
`;
