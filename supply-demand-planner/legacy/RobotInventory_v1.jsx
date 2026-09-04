import React, { useMemo, useState, useCallback } from "react";
import {
  ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ReferenceLine, ResponsiveContainer, Legend, Area,
} from "recharts";

/* ═══════════════════════════════════════════════════════════════
   DATA — from "Demand Forecast and Fulfillment Confirmation"
   Sheet: 2026 Demand Forecast. Week 0 = Mon Jun 29, 2026.
   Inventory rows are PROJECTED DEPLOYABLE INVENTORY (already net
   of every committed customer deployment below).
   ═══════════════════════════════════════════════════════════════ */
const WEEKS = ["2026-06-29","2026-07-06","2026-07-13","2026-07-20","2026-07-27","2026-08-03","2026-08-10","2026-08-17","2026-08-24","2026-08-31","2026-09-07","2026-09-14","2026-09-21","2026-09-28","2026-10-05","2026-10-12","2026-10-19","2026-10-26","2026-11-02","2026-11-09","2026-11-16","2026-11-23","2026-11-30","2026-12-07","2026-12-14","2026-12-21","2026-12-28"];
const SL_INV = [0,1,2,1,3,5,7,5,1,3,5,7,9,9,8,8,10,12,14,13,15,17,19,20,22,22,23];
const HT_INV = [4,9,13,13,6,11,16,5,-3,7,17,27,37,31,22,22,22,22,22,6,6,6,6,6,6,-10,-10];
const LT_INV = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,-10,-10,-10,-10,-14,-14,-14,-14,-14,-14,-14,-14];
const HT_BUILD = [5,4,9,5,5,5,5,10,10,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
const LT_BUILD_TOTAL = 0; // zero light tray builds planned for rest of 2026
const SL_COST = 63759.91;
const HT_COST = 8681.44;
const CAP = 1000000;

const COMMITMENTS = [
  { customer: "Meta",       lifts: 3, trays: 9,  type: "H", week: "2026-07-20" },
  { customer: "Home Depot", lifts: 0, trays: 12, type: "H", week: "2026-07-27" },
  { customer: "Home Depot", lifts: 2, trays: 16, type: "H", week: "2026-08-17" },
  { customer: "Corning",    lifts: 6, trays: 18, type: "H", week: "2026-08-24" },
  { customer: "Home Depot", lifts: 2, trays: 16, type: "H", week: "2026-09-28" },
  { customer: "Space-X",    lifts: 3, trays: 9,  type: "H", week: "2026-10-05" },
  { customer: "AMXL",       lifts: 2, trays: 12, type: "L", week: "2026-10-12" },
  { customer: "Home Depot", lifts: 2, trays: 16, type: "H", week: "2026-11-09" },
  { customer: "UPS",        lifts: 1, trays: 4,  type: "L", week: "2026-11-09" },
  { customer: "Home Depot", lifts: 2, trays: 16, type: "H", week: "2026-12-21" },
];

/* ── SlipOS dark theme tokens ────────────────────────────────── */
const T = {
  canvas: "#0A0D13", panel: "#10141D", inset: "#0D1119",
  border: "#232A3A", borderSoft: "#1B2130",
  text: "#E6EAF2", sub: "#9AA3B8", muted: "#6B7488",
  indigo: "#6E62F5", indigoSoft: "#A5A0FA",
  amber: "#F5A524",   // SlipLifts
  sky: "#38BDF8",     // Heavy Trays
  pink: "#E879F9",    // Light Trays
  green: "#34D399", red: "#F87171",
};

const fmtWeek = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" });
const fmtWeekFull = (iso) => new Date(iso + "T00:00:00").toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
const fmt$ = (v) => "$" + Math.round(v).toLocaleString();
const fmt$k = (v) => (v >= 1000000 ? "$" + (v / 1000000).toFixed(2) + "M" : "$" + Math.round(v / 1000) + "K");

/* Available-to-Promise at week w: units pullable at w without breaking
   any committed deployment inside the protection window. */
function atp(inv, w, horizon) {
  const end = Math.min(inv.length - 1, w + horizon);
  let m = Infinity;
  for (let t = w; t <= end; t++) m = Math.min(m, inv[t]);
  return Math.max(0, Math.floor(m));
}

function Stepper({ id, label, value, onChange, accent }) {
  const set = (v) => onChange(Math.max(0, Math.min(99, v)));
  return (
    <div className="stepper" style={{ "--acc": accent }}>
      <label htmlFor={id}>{label}</label>
      <div className="stepper-row">
        <button type="button" aria-label={"Decrease " + label} onClick={() => set(value - 1)}>−</button>
        <input id={id} type="number" inputMode="numeric" min="0" max="99" value={value}
          onChange={(e) => set(e.target.value === "" ? 0 : parseInt(e.target.value, 10) || 0)}
          onFocus={(e) => e.target.select()} />
        <button type="button" aria-label={"Increase " + label} onClick={() => set(value + 1)}>+</button>
      </div>
    </div>
  );
}

const tickStyle = { fontSize: 10, fill: T.sub };
const tooltipStyle = { fontSize: 12, borderRadius: 8, background: T.panel, border: "1px solid " + T.border, color: T.text };

/* ═══════════════════════════════════════════════════════════════ */
export default function RobotAvailability() {
  const [mode, setMode] = useState("when");
  const [trayType, setTrayType] = useState("heavy"); // "heavy" | "light"
  const [qLifts, setQLifts] = useState(3);
  const [qTrays, setQTrays] = useState(9);
  const [linkTrays, setLinkTrays] = useState(true);
  const [targetWeek, setTargetWeek] = useState(12);
  const [leadWeeks, setLeadWeeks] = useState(8);
  const [protect, setProtect] = useState("8");
  const [holds, setHolds] = useState([]);
  const [holdName, setHoldName] = useState("");
  const [copied, setCopied] = useState(false);

  const horizon = protect === "full" ? WEEKS.length : 8;
  const RATIO = trayType === "heavy" ? 3 : 4; // typical kit: 3 heavy or 4 light per lift
  const trayLabel = trayType === "heavy" ? "heavy tray" : "light tray";
  const trayAccent = trayType === "heavy" ? T.sky : T.pink;

  /* Effective inventory = plan minus everything reps have soft-held */
  const effSl = useMemo(() => {
    const a = [...SL_INV];
    holds.forEach((h) => { for (let t = h.week; t < a.length; t++) a[t] -= h.lifts; });
    return a;
  }, [holds]);
  const effHt = useMemo(() => {
    const a = [...HT_INV];
    holds.filter((h) => h.type === "heavy").forEach((h) => { for (let t = h.week; t < a.length; t++) a[t] -= h.trays; });
    return a;
  }, [holds]);
  const effLt = useMemo(() => {
    const a = [...LT_INV];
    holds.filter((h) => h.type === "light").forEach((h) => { for (let t = h.week; t < a.length; t++) a[t] -= h.trays; });
    return a;
  }, [holds]);
  const effTray = trayType === "heavy" ? effHt : effLt;

  const switchType = (t) => {
    setTrayType(t);
    if (linkTrays) setQTrays(qLifts * (t === "heavy" ? 3 : 4));
  };
  const setLifts = (v) => { setQLifts(v); if (linkTrays) setQTrays(v * RATIO); };
  const setTrays = (v) => { setQTrays(v); if (linkTrays && v !== qLifts * RATIO) setLinkTrays(false); };

  const result = useMemo(() => {
    if (mode !== "when" || (qLifts <= 0 && qTrays <= 0)) return null;
    let inv = -1;
    for (let w = 0; w < WEEKS.length; w++) {
      if (atp(effSl, w, horizon) >= qLifts && atp(effTray, w, horizon) >= qTrays) { inv = w; break; }
    }
    if (inv === -1) return { status: "none" };
    let w2 = Math.max(inv, leadWeeks);
    while (w2 < WEEKS.length && !(atp(effSl, w2, horizon) >= qLifts && atp(effTray, w2, horizon) >= qTrays)) w2++;
    if (w2 >= WEEKS.length) return { status: "none" };
    const gatedBy = inv >= leadWeeks ? "inventory" : "leadtime";
    const status = w2 <= leadWeeks + 1 ? "green" : w2 <= leadWeeks + 5 ? "tight" : "later";
    return { status, invWeek: inv, shipWeek: w2, gatedBy };
  }, [mode, qLifts, qTrays, leadWeeks, horizon, effSl, effTray]);

  const reverse = useMemo(() => {
    if (mode !== "howmuch") return null;
    const w = Math.max(targetWeek, leadWeeks);
    if (w >= WEEKS.length) return { maxLifts: 0, maxTrays: 0, kits: 0, week: WEEKS.length - 1, pushed: true };
    const maxLifts = atp(effSl, w, horizon);
    const maxTrays = atp(effTray, w, horizon);
    const kits = Math.min(maxLifts, Math.floor(maxTrays / RATIO));
    return { maxLifts, maxTrays, kits, week: w, pushed: w !== targetWeek };
  }, [mode, targetWeek, leadWeeks, horizon, effSl, effTray, RATIO]);

  const heat = useMemo(() => WEEKS.map((wk, w) => {
    const l = atp(effSl, w, horizon);
    const t = atp(effTray, w, horizon);
    return { wk, kits: Math.min(l, Math.floor(t / RATIO)), lifts: l, trays: t, gated: w < leadWeeks };
  }), [effSl, effTray, horizon, leadWeeks, RATIO]);

  const milestones = useMemo(() => {
    if (!result || result.shipWeek == null) return null;
    const s = result.shipWeek;
    const clamp = (x) => Math.max(0, Math.min(x, s));
    return [
      { label: "Start site qualification", week: clamp(s - leadWeeks), owner: "Sales + customer" },
      { label: "Implementation kickoff", week: clamp(s - Math.ceil(leadWeeks * 0.6)), owner: "Ops" },
      { label: "Field tech hired", week: clamp(s - 3), owner: "Service Delivery" },
      { label: "Field warehouse booked", week: clamp(s - 3), owner: "Service Delivery" },
      { label: "Dock pickup", week: s, owner: "Logistics" },
      { label: "Go-live on site", week: s, owner: "Field Ops" },
    ];
  }, [result, leadWeeks]);

  const chartData = useMemo(() => {
    const e = mode === "when" && result && result.shipWeek != null ? result.shipWeek : -1;
    return WEEKS.map((wk, i) => {
      const baseUsd = Math.max(0, effSl[i]) * SL_COST + Math.max(0, effHt[i]) * HT_COST;
      return {
        wk: fmtWeek(wk),
        SlipLifts: effSl[i],
        "Heavy Trays": effHt[i],
        "Light Trays": effLt[i],
        simSl: e >= 0 && i >= e ? effSl[i] - qLifts : null,
        simTray: e >= 0 && i >= e ? (trayType === "heavy" ? effHt[i] : effLt[i]) - qTrays : null,
        "Finished goods $": baseUsd,
        simUsd: e >= 0 && i >= e
          ? Math.max(0, effSl[i] - qLifts) * SL_COST + Math.max(0, effHt[i] - (trayType === "heavy" ? qTrays : 0)) * HT_COST
          : null,
      };
    });
  }, [mode, result, qLifts, qTrays, trayType, effSl, effHt, effLt]);

  const capBreachIdx = WEEKS.findIndex((_, i) => Math.max(0, effSl[i]) * SL_COST + Math.max(0, effHt[i]) * HT_COST > CAP);
  const peakUsd = Math.max(...WEEKS.map((_, i) => Math.max(0, effSl[i]) * SL_COST + Math.max(0, effHt[i]) * HT_COST));
  const yearEndUsd = Math.max(0, effSl[effSl.length - 1]) * SL_COST + Math.max(0, effHt[effHt.length - 1]) * HT_COST;
  const htGapIdx = effHt.findIndex((v) => v < 0);
  const ltGapIdx = effLt.findIndex((v) => v < 0);
  const htBuildEndIdx = (() => { let last = -1; HT_BUILD.forEach((v, i) => { if (v > 0) last = i; }); return last; })();
  const currentUsd = Math.max(0, effSl[0]) * SL_COST + Math.max(0, effHt[0]) * HT_COST;

  const promiseText = useMemo(() => {
    if (!result || result.shipWeek == null) return "";
    const wk = WEEKS[result.shipWeek];
    return `Availability confirmation — Slip Robotics\n` +
      `Configuration: ${qLifts} SlipLift${qLifts !== 1 ? "s" : ""} + ${qTrays} ${trayLabel}${qTrays !== 1 ? "s" : ""}\n` +
      `Earliest go-live: week of ${fmtWeekFull(wk)}\n` +
      `To hold this date we need site qualification underway by ${fmtWeekFull(WEEKS[Math.max(0, result.shipWeek - leadWeeks)])}, ` +
      `with implementation kickoff, field tech, and field warehouse confirmed on the standard schedule.\n` +
      `This date honors all previously committed deployments and is a planning promise, subject to contract.`;
  }, [result, qLifts, qTrays, trayLabel, leadWeeks]);

  const copyPromise = useCallback(() => {
    const done = () => { setCopied(true); setTimeout(() => setCopied(false), 1800); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(promiseText).then(done).catch(() => {
        const ta = document.createElement("textarea");
        ta.value = promiseText; document.body.appendChild(ta); ta.select();
        document.execCommand("copy"); document.body.removeChild(ta); done();
      });
    }
  }, [promiseText]);

  const reserve = () => {
    if (!result || result.shipWeek == null) return;
    setHolds([...holds, { id: Date.now(), name: holdName.trim() || "Unnamed prospect", lifts: qLifts, trays: qTrays, type: trayType, week: result.shipWeek }]);
    setHoldName("");
  };

  return (
    <div className="ra-root">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');
        *{box-sizing:border-box;}
        .ra-root{min-height:100vh;background:${T.canvas};color:${T.text};font-family:'Inter',system-ui,sans-serif;padding:0 0 48px;}
        .ra-head{background:${T.canvas};padding:18px 28px;display:flex;flex-wrap:wrap;align-items:center;gap:16px;justify-content:space-between;border-bottom:1px solid ${T.border};}
        .ra-brand{font-weight:600;font-size:15px;letter-spacing:.42em;text-transform:uppercase;color:${T.text};}
        .ra-sub{font-size:12.5px;color:${T.sub};margin-top:3px;}
        .ra-sub b{color:${T.indigoSoft};font-weight:600;}
        .ra-chips{display:flex;gap:10px;flex-wrap:wrap;}
        .chip{font-size:12px;font-weight:500;padding:7px 12px;border-radius:8px;background:${T.panel};border:1px solid ${T.border};color:${T.sub};}
        .chip b{color:${T.text};font-weight:600;}
        .chip.rope-ok{border-color:#1E4636;color:#7EDDB4;background:#0E1E18;}
        .chip.rope-hot{border-color:#4A2626;color:#F5A19B;background:#1E1112;}
        .wrap{max-width:1240px;margin:0 auto;padding:0 20px;}
        .mode{display:inline-flex;background:${T.panel};border:1px solid ${T.border};border-radius:10px;overflow:hidden;margin:20px 0 0;padding:3px;gap:3px;}
        .mode button{font:500 13px 'Inter';padding:8px 16px;border:none;background:transparent;color:${T.sub};cursor:pointer;border-radius:7px;}
        .mode button.on{background:${T.indigo};color:#fff;font-weight:600;}
        .mode button:focus-visible{outline:2px solid ${T.indigoSoft};}
        .hero{background:${T.panel};border:1px solid ${T.border};border-radius:12px;padding:22px 24px;display:grid;grid-template-columns:auto 1fr;gap:24px 32px;align-items:center;margin-top:12px;}
        @media(max-width:980px){.hero{grid-template-columns:1fr;}}
        .inputs{display:flex;gap:18px;align-items:flex-end;flex-wrap:wrap;}
        .stepper label{display:block;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:7px;}
        .stepper-row{display:flex;align-items:stretch;border:1.5px solid var(--acc);border-radius:10px;overflow:hidden;background:${T.inset};}
        .stepper-row button{width:44px;font:600 22px 'Inter';border:none;background:${T.panel};color:${T.sub};cursor:pointer;}
        .stepper-row button:hover{background:var(--acc);color:#0A0D13;}
        .stepper-row button:focus-visible{outline:2px solid ${T.text};outline-offset:-2px;}
        .stepper-row input{width:88px;border:none;text-align:center;font:700 38px 'Inter';color:${T.text};background:${T.inset};padding:6px 0;-moz-appearance:textfield;}
        .stepper-row input::-webkit-outer-spin-button,.stepper-row input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0;}
        .stepper-row input:focus{outline:none;background:#141a28;}
        .tray-col{display:flex;flex-direction:column;gap:8px;}
        .type-seg{display:flex;border:1px solid ${T.border};border-radius:8px;overflow:hidden;background:${T.inset};padding:2px;gap:2px;}
        .type-seg button{flex:1;font:600 11px 'Inter';letter-spacing:.06em;text-transform:uppercase;padding:6px 10px;border:none;background:transparent;cursor:pointer;color:${T.muted};border-radius:6px;}
        .type-seg button.h.on{background:#0E2334;color:${T.sky};}
        .type-seg button.l.on{background:#2A1230;color:${T.pink};}
        .link-toggle{display:flex;align-items:center;gap:7px;font-size:12px;color:${T.sub};font-weight:500;cursor:pointer;user-select:none;padding-bottom:12px;}
        .link-toggle input{accent-color:${T.indigo};width:15px;height:15px;}
        select{font:500 14px 'Inter';padding:10px 12px;border:1px solid ${T.border};border-radius:10px;background:${T.inset};color:${T.text};}
        select:focus{outline:2px solid ${T.indigo};}
        .tag{position:relative;border:1px dashed ${T.border};border-radius:12px;padding:16px 22px 16px 52px;background:${T.inset};display:flex;flex-wrap:wrap;gap:6px 26px;align-items:center;}
        .tag::before{content:"";position:absolute;left:18px;top:50%;transform:translateY(-50%);width:14px;height:14px;border-radius:50%;background:${T.canvas};border:2px solid ${T.border};}
        .tag.green{border-color:#2A6A4E;background:#0D1F17;}
        .tag.tight{border-color:#6B5320;background:#1D1810;}
        .tag.later,.tag.none{border-color:#6B3030;background:#1F1213;}
        .tag.idle{border-color:${T.border};}
        .verdict{font-weight:700;font-size:19px;letter-spacing:-.01em;line-height:1.1;}
        .tag.green .verdict{color:${T.green}}.tag.tight .verdict{color:${T.amber}}.tag.later .verdict,.tag.none .verdict{color:${T.red}}.tag.idle .verdict{color:${T.muted}}
        .stamp{font-weight:800;font-size:28px;line-height:1;color:${T.text};letter-spacing:-.01em;}
        .stamp small{display:block;font:600 10px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:${T.muted};margin-bottom:4px;}
        .tag-detail{font-size:12px;color:${T.sub};max-width:340px;line-height:1.5;}
        .tag-actions{display:flex;gap:8px;flex-basis:100%;margin-top:6px;flex-wrap:wrap;}
        .mini-btn{font:600 12px 'Inter';padding:8px 14px;border-radius:8px;border:1px solid ${T.indigo};background:${T.indigo};color:#fff;cursor:pointer;}
        .mini-btn.ghost{background:transparent;color:${T.indigoSoft};}
        .mini-btn:hover{filter:brightness(1.15);}
        .mini-btn:focus-visible{outline:2px solid ${T.text};}
        .hold-name{font:500 12.5px 'Inter';padding:8px 10px;border:1px solid ${T.border};border-radius:8px;width:170px;background:${T.inset};color:${T.text};}
        .hold-name::placeholder{color:${T.muted};}
        .miles{display:flex;gap:0;margin-top:18px;overflow-x:auto;padding-bottom:4px;}
        .mile{flex:1;min-width:120px;position:relative;padding:0 10px 0 0;}
        .mile::before{content:"";position:absolute;top:7px;left:16px;right:0;height:1.5px;background:${T.border};}
        .mile:last-child::before{display:none;}
        .mile-dot{width:15px;height:15px;border-radius:50%;background:${T.canvas};border:3px solid ${T.indigo};position:relative;z-index:1;}
        .mile.done .mile-dot{background:${T.indigo};}
        .mile-wk{font:600 13px 'JetBrains Mono',monospace;margin-top:9px;color:${T.text};}
        .mile-label{font-size:11.5px;font-weight:600;color:${T.sub};line-height:1.35;margin-top:3px;}
        .mile-owner{font-size:10.5px;color:${T.muted};margin-top:2px;}
        .heat-scroll{overflow-x:auto;padding-bottom:6px;}
        .heat{display:flex;gap:4px;min-width:900px;}
        .cell{flex:1;border-radius:6px;padding:8px 2px 7px;text-align:center;cursor:default;border:1px solid transparent;}
        .cell .k{font:700 17px 'Inter';line-height:1;}
        .cell .d{font:500 8.5px 'JetBrains Mono',monospace;opacity:.8;margin-top:4px;letter-spacing:.02em;}
        .cell.g0{background:#12161F;color:#525C72;border-color:${T.borderSoft};}
        .cell.g1{background:#251A0C;color:#C98A2B;}
        .cell.g2{background:#33230C;color:${T.amber};}
        .cell.g3{background:#0E241C;color:#4EC393;}
        .cell.g4{background:#0F3226;color:#6EE7B7;}
        .cell.gated{outline:1.5px dashed #6B5320;outline-offset:-2px;}
        .heat-legend{display:flex;gap:14px;font-size:11px;color:${T.muted};margin-top:10px;flex-wrap:wrap;}
        .lg{display:flex;align-items:center;gap:5px;}
        .sw{width:12px;height:12px;border-radius:3px;display:inline-block;}
        .ra-grid{display:grid;grid-template-columns:340px 1fr;gap:20px;margin-top:20px;}
        @media(max-width:900px){.ra-grid{grid-template-columns:1fr;}}
        .card{background:${T.panel};border:1px solid ${T.border};border-radius:12px;padding:18px 20px;}
        .card h3{font-weight:700;font-size:14.5px;color:${T.text};margin:0 0 4px;letter-spacing:-.01em;}
        .card .sub{font-size:12px;color:${T.muted};margin:0 0 14px;}
        label.small{display:block;font-size:12px;font-weight:600;color:${T.sub};margin:14px 0 6px;}
        .hint{font-size:11px;color:${T.muted};margin-top:6px;line-height:1.55;}
        .seg{display:flex;border:1px solid ${T.border};border-radius:8px;overflow:hidden;background:${T.inset};padding:3px;gap:3px;}
        .seg button{flex:1;font-size:12px;font-weight:500;padding:7px 4px;border:none;background:transparent;cursor:pointer;color:${T.sub};border-radius:6px;}
        .seg button.on{background:${T.indigo};color:#fff;font-weight:600;}
        .range-val{font:700 16px 'Inter';color:${T.indigoSoft};}
        input[type=range]{width:100%;accent-color:${T.indigo};}
        .charts{display:grid;gap:20px;}
        .signals{display:grid;gap:10px;}
        .signal{display:flex;gap:10px;font-size:12.5px;line-height:1.55;color:${T.sub};background:${T.inset};border:1px solid ${T.borderSoft};border-left:3px solid ${T.indigo};padding:11px 13px;border-radius:8px;}
        .signal b{color:${T.text};}
        .signal.red{border-left-color:${T.red};}
        .signal.amber{border-left-color:${T.amber};}
        table{width:100%;border-collapse:collapse;font-size:12.5px;}
        th{font:600 10.5px 'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.1em;color:${T.muted};text-align:left;padding:6px 8px;border-bottom:1px solid ${T.border};}
        td{padding:8px;border-bottom:1px solid ${T.borderSoft};color:${T.sub};}
        td .cust{color:${T.text};font-weight:500;}
        td.n{font-weight:600;text-align:right;font-variant-numeric:tabular-nums;color:${T.text};}
        td.wkcode{font:500 11.5px 'JetBrains Mono',monospace;color:${T.indigoSoft};}
        .tt{font:600 9.5px 'JetBrains Mono',monospace;padding:2px 5px;border-radius:4px;margin-left:5px;}
        .tt.H{background:#0E2334;color:${T.sky};}
        .tt.L{background:#2A1230;color:${T.pink};}
        .rm{border:none;background:none;color:${T.red};font-weight:700;cursor:pointer;font-size:14px;line-height:1;}
        .empty{font-size:12px;color:${T.muted};padding:10px 4px;line-height:1.5;}
        .foot{margin-top:24px;font-size:11.5px;color:${T.muted};line-height:1.65;}
        @media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important;}}
      `}</style>

      <header className="ra-head">
        <div>
          <div className="ra-brand">Slip Robotics</div>
          <div className="ra-sub"><b>Robot Availability</b> — SlipLifts, Heavy &amp; Light Trays · Sales</div>
        </div>
        <div className="ra-chips">
          <div className="chip">Plan as of <b>week of Jun 29, 2026</b></div>
          <div className="chip">Soft holds active: <b>{holds.length}</b></div>
          <div className={"chip " + (currentUsd > CAP ? "rope-hot" : "rope-ok")}>
            Finished goods today: <b>{fmt$k(currentUsd)}</b> / $1.0M cap
          </div>
        </div>
      </header>

      <div className="wrap">
        <div className="mode" role="tablist" aria-label="Query mode">
          <button role="tab" aria-selected={mode === "when"} className={mode === "when" ? "on" : ""} onClick={() => setMode("when")}>I know the quantity → when?</button>
          <button role="tab" aria-selected={mode === "howmuch"} className={mode === "howmuch" ? "on" : ""} onClick={() => setMode("howmuch")}>I know the date → how much?</button>
        </div>

        {/* ══ HERO ══ */}
        <div className="hero">
          {mode === "when" ? (
            <>
              <div className="inputs">
                <Stepper id="ql" label="SlipLifts" value={qLifts} onChange={setLifts} accent={T.amber} />
                <div className="tray-col">
                  <div className="type-seg" role="group" aria-label="Tray type">
                    <button className={"h" + (trayType === "heavy" ? " on" : "")} onClick={() => switchType("heavy")}>Heavy</button>
                    <button className={"l" + (trayType === "light" ? " on" : "")} onClick={() => switchType("light")}>Light</button>
                  </div>
                  <Stepper id="qt" label={trayType === "heavy" ? "Heavy Trays" : "Light Trays"} value={qTrays} onChange={setTrays} accent={trayAccent} />
                </div>
                <label className="link-toggle" title="Typical kit: 3 heavy or 4 light trays per SlipLift">
                  <input type="checkbox" checked={linkTrays}
                    onChange={(e) => { setLinkTrays(e.target.checked); if (e.target.checked) setQTrays(qLifts * RATIO); }} />
                  Keep {RATIO} trays per lift
                </label>
              </div>

              {!result && (
                <div className="tag idle" role="status">
                  <div className="verdict">Enter a quantity</div>
                  <div className="tag-detail">The earliest go-live date appears here the moment you type what the customer needs.</div>
                </div>
              )}
              {result && result.status !== "none" && (
                <div className={"tag " + result.status} role="status" aria-live="polite">
                  <div className="verdict">
                    {result.status === "green" ? "Green light" : result.status === "tight" ? "Tight — but yes" : "Later this year"}
                  </div>
                  <div className="stamp">
                    <small>Earliest go-live week</small>
                    {fmtWeekFull(WEEKS[result.shipWeek])}
                  </div>
                  <div className="tag-detail">
                    {qLifts} SlipLift{qLifts !== 1 ? "s" : ""} + {qTrays} {trayLabel}{qTrays !== 1 ? "s" : ""}, honoring every committed deployment{holds.length > 0 ? " and " + holds.length + " soft hold" + (holds.length > 1 ? "s" : "") : ""}.
                    {result.gatedBy === "leadtime"
                      ? " Fleet clears earlier (week of " + fmtWeek(WEEKS[result.invWeek]) + ") — site readiness is the gate, so starting qualification now locks this date."
                      : " Fleet availability is the gate; site readiness fits inside the wait."}
                  </div>
                  <div className="tag-actions">
                    <button className="mini-btn" onClick={copyPromise}>{copied ? "Copied ✓" : "Copy customer promise"}</button>
                    <input className="hold-name" placeholder="Prospect name…" value={holdName}
                      onChange={(e) => setHoldName(e.target.value)} aria-label="Prospect name for soft hold" />
                    <button className="mini-btn ghost" onClick={reserve}>Place soft hold</button>
                  </div>
                </div>
              )}
              {result && result.status === "none" && (
                <div className="tag none" role="status" aria-live="polite">
                  <div className="verdict">Not in this year's plan</div>
                  <div className="tag-detail">
                    The current build schedule can't cover {qLifts} SlipLifts + {qTrays} {trayLabel}s without touching a committed deployment{holds.length > 0 ? " or an active soft hold" : ""}.
                    {trayType === "light"
                      ? " Light trays are the blocker: zero light tray builds are planned for the rest of 2026 and existing stock is already claimed. Any light tray deal needs a build decision first — flag it to Ops."
                      : " A deal this size needs a production re-plan — bring it to the weekly consensus meeting rather than promising a date."}
                  </div>
                </div>
              )}
            </>
          ) : (
            <>
              <div className="inputs">
                <div>
                  <label className="small" htmlFor="tw" style={{ margin: "0 0 6px" }}>Customer wants go-live the week of</label>
                  <select id="tw" value={targetWeek} onChange={(e) => setTargetWeek(+e.target.value)}>
                    {WEEKS.map((w, i) => <option key={w} value={i}>{fmtWeekFull(w)}</option>)}
                  </select>
                </div>
                <div className="tray-col" style={{ paddingBottom: 2 }}>
                  <label className="small" style={{ margin: "0 0 2px" }}>Tray type</label>
                  <div className="type-seg" role="group" aria-label="Tray type">
                    <button className={"h" + (trayType === "heavy" ? " on" : "")} onClick={() => switchType("heavy")}>Heavy</button>
                    <button className={"l" + (trayType === "light" ? " on" : "")} onClick={() => switchType("light")}>Light</button>
                  </div>
                </div>
              </div>
              {reverse && (
                <div className={"tag " + (reverse.kits >= 3 ? "green" : reverse.kits >= 1 ? "tight" : "later")} role="status" aria-live="polite">
                  <div className="verdict">{reverse.kits >= 1 ? "Biggest deal you can promise" : "Nothing free that week"}</div>
                  <div className="stamp">
                    <small>By week of {fmtWeek(WEEKS[reverse.week])}</small>
                    {reverse.kits} lift{reverse.kits !== 1 ? "s" : ""} + {reverse.kits * RATIO} {trayLabel}s
                  </div>
                  <div className="tag-detail">
                    Raw ceilings that week: {reverse.maxLifts} SlipLifts and {reverse.maxTrays} {trayLabel}s, honoring all commitments{holds.length > 0 ? " and soft holds" : ""}.
                    {reverse.pushed ? " Your target lands inside the " + leadWeeks + "-week site readiness window, so the date shown is the first realistic go-live." : ""}
                    {reverse.kits === 0 && trayType === "light" ? " Light tray stock is fully claimed and no builds are planned — a light tray deal needs a build decision first." : ""}
                    {reverse.kits === 0 && trayType === "heavy" && reverse.maxTrays > 0 ? " Trays exist but no free lift pairs with them — check a later week on the strip below." : ""}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* ══ Milestones ══ */}
        {mode === "when" && result && result.shipWeek != null && milestones && (
          <div className="card" style={{ marginTop: 14 }}>
            <h3>Backward plan to hit {fmtWeek(WEEKS[result.shipWeek])}</h3>
            <div className="miles">
              {milestones.map((m, i) => (
                <div key={i} className={"mile" + (m.week <= 0 ? " done" : "")}>
                  <div className="mile-dot" />
                  <div className="mile-wk">{m.week <= 0 ? "Now" : fmtWeek(WEEKS[m.week])}</div>
                  <div className="mile-label">{m.label}</div>
                  <div className="mile-owner">{m.owner}</div>
                </div>
              ))}
            </div>
            <div className="hint">Dates derive from the fulfillment checklist in the demand workbook (site qualification → kickoff → field tech → field warehouse → dock pickup). If the first milestone says "Now," the clock is already running.</div>
          </div>
        )}

        {/* ══ Browsable capacity strip ══ */}
        <div className="card" style={{ marginTop: 14 }}>
          <h3>What's free, week by week — {trayType} tray kits</h3>
          <p className="sub">Standard kit: 1 lift + {RATIO} {trayLabel}s, clear to promise after commitments and holds. Switch tray type above to flip this view.</p>
          <div className="heat-scroll">
            <div className="heat">
              {heat.map((h, i) => {
                const g = h.kits <= 0 ? "g0" : h.kits === 1 ? "g1" : h.kits === 2 ? "g2" : h.kits <= 4 ? "g3" : "g4";
                return (
                  <div key={i} className={"cell " + g + (h.gated ? " gated" : "")}
                    title={fmtWeekFull(h.wk) + " — up to " + h.kits + " kits (" + h.lifts + " lifts, " + h.trays + " " + trayLabel + "s free)" + (h.gated ? ". Inside the site-readiness window — new sites can't go live yet." : "")}>
                    <div className="k">{h.kits}</div>
                    <div className="d">{fmtWeek(h.wk)}</div>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="heat-legend">
            <span className="lg"><span className="sw" style={{ background: "#12161F", border: "1px solid #1B2130" }} />0 kits</span>
            <span className="lg"><span className="sw" style={{ background: "#251A0C" }} />1</span>
            <span className="lg"><span className="sw" style={{ background: "#33230C" }} />2</span>
            <span className="lg"><span className="sw" style={{ background: "#0E241C" }} />3–4</span>
            <span className="lg"><span className="sw" style={{ background: "#0F3226" }} />5+</span>
            <span className="lg"><span className="sw" style={{ outline: "1.5px dashed #6B5320", outlineOffset: -1 }} />inside site-readiness window</span>
          </div>
        </div>

        <div className="ra-grid">
          {/* ── Left rail ── */}
          <div style={{ display: "grid", gap: 20, alignContent: "start" }}>
            <div className="card">
              <h3>Assumptions</h3>
              <label className="small" htmlFor="lead">Site readiness lead time — <span className="range-val">{leadWeeks} weeks</span></label>
              <input id="lead" type="range" min="4" max="14" value={leadWeeks} onChange={(e) => setLeadWeeks(+e.target.value)} />
              <div className="hint">Covers site qualification, kickoff, field tech hire, and field warehouse. Robots can't go live before this even if they're sitting on the dock.</div>
              <label className="small">Protect committed deployments through</label>
              <div className="seg" role="group" aria-label="Protection window">
                <button className={protect === "8" ? "on" : ""} onClick={() => setProtect("8")}>Next 8 weeks</button>
                <button className={protect === "full" ? "on" : ""} onClick={() => setProtect("full")}>Full year</button>
              </div>
              <div className="hint">Full year is the strict promise: nothing is offered that the current build plan can't cover through December. Next 8 weeks assumes production can re-plan beyond that window.</div>
            </div>

            <div className="card">
              <h3>Soft holds</h3>
              <p className="sub">First come, first served.</p>
              {holds.length === 0 && <div className="empty">No holds yet. Check a deal, then "Place soft hold" to claim robots so two reps can't promise the same units.</div>}
              {holds.length > 0 && (
                <table>
                  <thead><tr><th>Prospect</th><th>Week</th><th style={{textAlign:"right"}}>Lifts</th><th style={{textAlign:"right"}}>Trays</th><th /></tr></thead>
                  <tbody>
                    {holds.map((h) => (
                      <tr key={h.id}>
                        <td><span className="cust">{h.name}</span></td>
                        <td className="wkcode">{fmtWeek(WEEKS[h.week])}</td>
                        <td className="n">{h.lifts || "–"}</td>
                        <td className="n">{h.trays || "–"}<span className={"tt " + (h.type === "heavy" ? "H" : "L")}>{h.type === "heavy" ? "H" : "L"}</span></td>
                        <td><button className="rm" aria-label={"Release hold for " + h.name} onClick={() => setHolds(holds.filter((x) => x.id !== h.id))}>×</button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
              {holds.length > 0 && <div className="hint">Every date and chart on this page already accounts for these holds. Release a hold if the deal dies.</div>}
            </div>

            <div className="card">
              <h3>Committed deployments</h3>
              <table>
                <thead><tr><th>Week</th><th>Customer</th><th style={{textAlign:"right"}}>Lifts</th><th style={{textAlign:"right"}}>Trays</th></tr></thead>
                <tbody>
                  {COMMITMENTS.map((c, i) => (
                    <tr key={i}>
                      <td className="wkcode">{fmtWeek(c.week)}</td>
                      <td><span className="cust">{c.customer}</span></td>
                      <td className="n">{c.lifts || "–"}</td>
                      <td className="n">{c.trays || "–"}{c.trays ? <span className={"tt " + c.type}>{c.type}</span> : null}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="hint">H = heavy trays, L = light trays.</div>
            </div>
          </div>

          {/* ── Charts + signals ── */}
          <div className="charts">
            <div className="card">
              <h3>Uncommitted fleet by week {mode === "when" && result && result.shipWeek != null ? "— with this deal overlaid (dashed)" : ""}</h3>
              <ResponsiveContainer width="100%" height={270}>
                <ComposedChart data={chartData} margin={{ top: 8, right: 12, left: -18, bottom: 0 }}>
                  <CartesianGrid stroke={T.borderSoft} vertical={false} />
                  <XAxis dataKey="wk" tick={tickStyle} interval={2} stroke={T.border} />
                  <YAxis tick={tickStyle} allowDecimals={false} stroke={T.border} />
                  <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: T.text }} />
                  <Legend wrapperStyle={{ fontSize: 12, color: T.sub }} />
                  <ReferenceLine y={0} stroke={T.red} strokeWidth={1} />
                  <Line type="stepAfter" dataKey="SlipLifts" stroke={T.amber} strokeWidth={2.5} dot={false} />
                  <Line type="stepAfter" dataKey="Heavy Trays" stroke={T.sky} strokeWidth={2.5} dot={false} />
                  <Line type="stepAfter" dataKey="Light Trays" stroke={T.pink} strokeWidth={2.5} dot={false} />
                  {mode === "when" && result && result.shipWeek != null && <Line type="stepAfter" dataKey="simSl" name="SlipLifts after deal" stroke={T.amber} strokeWidth={2} strokeDasharray="5 4" dot={false} />}
                  {mode === "when" && result && result.shipWeek != null && <Line type="stepAfter" dataKey="simTray" name={(trayType === "heavy" ? "Heavy" : "Light") + " trays after deal"} stroke={trayAccent} strokeWidth={2} strokeDasharray="5 4" dot={false} />}
                </ComposedChart>
              </ResponsiveContainer>
              <div className="hint">Anything above zero is free to sell after all committed deployments and soft holds ship. Below zero means the current build plan is short — note light trays go 14 short by November with no builds planned.</div>
            </div>

            <div className="card">
              <h3>Finished goods vs. the $1M inventory cap</h3>
              <ResponsiveContainer width="100%" height={230}>
                <ComposedChart data={chartData} margin={{ top: 8, right: 12, left: 4, bottom: 0 }}>
                  <CartesianGrid stroke={T.borderSoft} vertical={false} />
                  <XAxis dataKey="wk" tick={tickStyle} interval={2} stroke={T.border} />
                  <YAxis tick={tickStyle} tickFormatter={fmt$k} stroke={T.border} />
                  <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: T.text }} formatter={(v) => fmt$(v)} />
                  <Legend wrapperStyle={{ fontSize: 12, color: T.sub }} />
                  <ReferenceLine y={CAP} stroke={T.red} strokeWidth={1.5} strokeDasharray="6 4"
                    label={{ value: "$1.0M cap", fill: T.red, fontSize: 11, position: "insideTopRight" }} />
                  <Area type="stepAfter" dataKey="Finished goods $" stroke={T.indigoSoft} strokeWidth={2} fill={T.indigo} fillOpacity={0.14} />
                  {mode === "when" && result && result.shipWeek != null && <Line type="stepAfter" dataKey="simUsd" name="After this deal" stroke={T.green} strokeWidth={2.5} strokeDasharray="5 4" dot={false} />}
                </ComposedChart>
              </ResponsiveContainer>
              <div className="hint">Tracks SlipLift + heavy tray finished goods (the workbook doesn't carry a light tray unit value). Every deal you close pulls this curve down — the weeks near the red line are exactly when sales wins matter most.</div>
            </div>

            <div className="card">
              <h3>Ops signals from the current plan</h3>
              <div className="signals" style={{ marginTop: 12 }}>
                {ltGapIdx >= 0 && (
                  <div className="signal red">
                    <span><b>Light trays are sold out for the year:</b> only 2 free today, zero light tray builds planned, and the committed AMXL and UPS deployments already push the plan {Math.abs(Math.min(...effLt))} trays short by {fmtWeek(WEEKS[19])}. Any new light tray deal — and even the existing commitments — needs a build or buy decision now.</span>
                  </div>
                )}
                {capBreachIdx >= 0 && (
                  <div className="signal red">
                    <span><b>Sell-by pressure:</b> without new deals, finished goods break the $1M cap the week of {fmtWeek(WEEKS[capBreachIdx])}, peaking at {fmt$k(peakUsd)}. Roughly {Math.max(0, Math.ceil((yearEndUsd - CAP) / SL_COST))} SlipLifts of Q4 demand keeps production at full rate.</span>
                  </div>
                )}
                {htGapIdx >= 0 && (
                  <div className="signal amber">
                    <span><b>Heavy tray plan gaps:</b> the plan dips {Math.abs(Math.min(...effHt))} trays short in late December (first gap the week of {fmtWeek(WEEKS[htGapIdx])}). Heavy tray builds currently stop after {fmtWeek(WEEKS[htBuildEndIdx])} — December commitments need a build restart or an earlier material pull.</span>
                  </div>
                )}
                <div className="signal">
                  <span><b>The system in one line:</b> the build rate is the drum (~2 SlipLifts/week), deployable inventory is the buffer you sell from, and the $1M cap is the rope that stops us building robots nobody has bought. This tool only promises what the buffer covers.</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="foot">
          Source: Demand Forecast &amp; Fulfillment Confirmation workbook, 2026 Demand Forecast sheet. Unit values: SlipLift {fmt$(SL_COST)}, heavy tray {fmt$(HT_COST)}; light trays carry no unit value in the workbook and are excluded from the cap chart. Typical kits: 3 heavy or 4 light trays per lift — both editable. Soft holds live only in this session — they reset on reload. Dates here are planning promises, not contractual delivery dates. Aux batteries, charge carts, and controllers follow the kit automatically and are not gating today.
        </div>
      </div>
    </div>
  );
}
