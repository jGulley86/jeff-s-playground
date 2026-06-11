#!/usr/bin/env python3
"""
Monte Carlo simulation: in-house tray fabrication at Slip Robotics.

100 stochastic scenario draws (common random numbers — every strategy sees the same
world), each evaluated against five capital strategies over a 60-month horizon at
monthly resolution, cash basis, vs. the continue-buying baseline. Anchors trace to
tray-fab-feasibility/04-data-basis.md (NetSuite POs/WOs, drawings, market benchmarks).

Calibration: in a flat-demand world at ~20-21/mo, strategy B reproduces the
deterministic Loop-49 P&L (~ +$155K/yr steady, trough ~ -$700K, 5-yr NPV ~ $0-150K).

Strategies:
  A  ultra_lean    (~$225K): platen-method fixture, used equipment, 2 welders, no ops tech
  C  lean_staged   (~$268K): modular hard fixture, 2-ton gantries, trigger-based hiring,
                             pre-engineered +$75K upgrade kit at sustained >20/mo
  B  base          (~$504K): Loop-25 plan (hard fixture, 5-ton gantry runs, 5 FTE day one)
  D  capacity_fwd  (~$660K): base + tack jig + 4th welder day one, sized for fast growth
  E  renegotiate   (~$0):    no build; should-cost-armed price negotiation with TEEMS
"""
import numpy as np

N_SIMS = 100
MONTHS = 60
DISC_M = 0.10 / 12

BUY0 = 5577.84            # TEEMS R03 price of record (PO10309, 5/19/2026)
WOOD_LEG_BUY = 122.71     # Starflex (PO10120)
WOOD_LEGS_MO = 60         # legs/mo at full 10 trays/mo wood ramp
DEMAND0 = 21.0            # heavy/mo, evidenced (WOs 21-22/mo)
WELDER_LOADED = 35.10     # $/hr loaded, Jun-2026
PAID_HR = 173.3           # 2080/12 paid hours
PROD_HR = 150.0           # productive hours
LEAD_YR, OPS_YR = 107e3, 70e3
CONSUM = 130.0

STRATEGIES = {
    "A_ultra_lean": dict(
        capex={1: 60e3, 2: 75e3, 3: 60e3, 4: 30e3}, total_capex=225e3,
        hours_pen=2.0, learn=0.08, fa_p=0.30, sop=6,
        ops="never", min_w=2, cap=18, fac_mo=8.0e3, coq_mo=0.9e3,
        upgrade=None, resale=0.45, used=True),
    "C_lean_staged": dict(
        capex={1: 70e3, 2: 80e3, 3: 70e3, 4: 48e3}, total_capex=268e3,
        hours_pen=0.0, learn=0.12, fa_p=0.18, sop=7,
        ops="trigger24", min_w=2, cap=22, fac_mo=9.5e3, coq_mo=0.9e3,
        upgrade=dict(thresh=20, cost=75e3, new_cap=27), resale=0.55, used=True),
    "B_base": dict(
        capex={1: 80e3, 2: 100e3, 3: 120e3, 4: 120e3, 5: 84e3}, total_capex=504e3,
        hours_pen=0.0, learn=0.12, fa_p=0.18, sop=7,
        ops="day1", min_w=3, cap=22, fac_mo=12.5e3, coq_mo=1.25e3,
        upgrade=dict(thresh=22, cost=45e3, new_cap=27), resale=0.60, used=False),
    "D_capacity_fwd": dict(
        capex={1: 100e3, 2: 140e3, 3: 160e3, 4: 160e3, 5: 100e3}, total_capex=660e3,
        hours_pen=-0.5, learn=0.13, fa_p=0.15, sop=7,
        ops="day1", min_w=4, cap=27, fac_mo=14.5e3, coq_mo=1.25e3,
        upgrade=dict(thresh=27, cost=60e3, new_cap=40), resale=0.60, used=False),
}


def draw_scenario(rng):
    s = {}
    s["growth"] = float(np.clip(rng.lognormal(np.log(1.10), 0.22), 0.65, 1.90))
    s["recession"] = rng.random() < 0.15
    s["rec_start"] = int(rng.integers(8, 36))
    s["kit0"] = float(rng.triangular(1850, 2035, 2550))
    s["steel"] = rng.normal(0, 0.08 / np.sqrt(12), MONTHS).cumsum()
    s["powder"] = float(rng.triangular(350, 425, 550))
    s["hours0"] = float(rng.triangular(14.5, 16.5, 22.0))
    s["wage_infl"] = float(rng.uniform(0.03, 0.05))
    s["buy_esc"] = float(rng.uniform(0.02, 0.05))
    s["rev"] = rng.poisson(2.0 / 12, MONTHS)
    s["rev_cost"] = rng.uniform(2e3, 8e3, MONTHS)
    s["fa_roll"] = rng.random()
    s["hire_lag"] = int(rng.integers(1, 4))            # months to land a welder
    s["eq_fail"] = rng.random() < 0.25                 # used-equipment repair event
    s["eq_fail_m"] = int(rng.integers(8, 30))
    s["ins_mo"] = float(rng.uniform(15e3, 25e3)) / 12
    s["wood_f"] = float(rng.triangular(0.1, 0.5, 1.0)) # wood ramp realization
    s["nego_win"] = rng.random() < 0.70
    s["nego_disc"] = float(rng.uniform(0.06, 0.12))
    return s


def demand_path(s):
    d = np.array([DEMAND0 * s["growth"] ** (m / 12) for m in range(MONTHS)])
    if s["recession"]:
        d[s["rec_start"]:s["rec_start"] + 12] *= 0.60
    return np.clip(d, 4, 60)


def run_strategy(cfg, s):
    d = demand_path(s)
    cash = np.zeros(MONTHS)
    sop = cfg["sop"] + (2 if s["fa_roll"] < cfg["fa_p"] else 0)
    if s["fa_roll"] < cfg["fa_p"]:
        cash[cfg["sop"]] -= 40e3
    if cfg["used"] and s["eq_fail"]:
        cash[s["eq_fail_m"]] -= 12e3

    cap, upgraded, sustain = cfg["cap"], False, 0
    welders, pending_hire, pending_t = cfg["min_w"], 0, 0
    ops_on = cfg["ops"] == "day1"
    low_run = 0

    for m in range(MONTHS):
        yr = m / 12
        infl = (1 + s["wage_infl"]) ** yr
        wage = WELDER_LOADED * infl
        buy = BUY0 * (1 + s["buy_esc"]) ** yr
        kit = s["kit0"] * (1 + 0.60 * s["steel"][m])
        hours = (s["hours0"] + cfg["hours_pen"]) * (1 - cfg["learn"] * min(1, max(0, (m - sop) / 18)))

        cash[m] -= cfg["capex"].get(m, 0.0)
        if m >= 2:
            cash[m] -= LEAD_YR / 12 * infl + cfg["fac_mo"] + cfg["coq_mo"] + s["ins_mo"]
        if m < sop - 4:
            continue

        # staffing: hire toward need with lag; downsize after 4 low months
        need = max(cfg["min_w"], int(np.ceil(min(d[m], cap) * hours / PROD_HR)))
        if need > welders and pending_hire == 0:
            pending_hire, pending_t = need - welders, m + s["hire_lag"]
        if pending_hire and m >= pending_t:
            welders += pending_hire
            pending_hire = 0
        low_run = low_run + 1 if need < welders else 0
        if low_run >= 4 and welders > cfg["min_w"]:
            welders -= 1
            low_run = 0
        cash[m] -= welders * PAID_HR * wage
        if cfg["ops"] == "trigger24" and not ops_on and m > sop and d[m] > 24:
            ops_on = True
        if ops_on:
            cash[m] -= OPS_YR / 12 * infl

        if m < sop - 1:
            continue
        cap_labor = (welders * PROD_HR + 40) / hours
        units = min(d[m], cap, cap_labor)
        if m == sop - 1:
            units = min(units, 3)          # first articles
        elif m == sop:
            units = min(units, d[m] * 0.5)  # half-rate ramp month

        cash[m] += units * (buy - kit - s["powder"] - CONSUM)
        slack = welders * PROD_HR + 40 - units * hours
        legs = min(WOOD_LEGS_MO * s["wood_f"], max(0.0, slack) / 1.25)
        cash[m] += legs * (WOOD_LEG_BUY - 48 - 12 - 10)   # leg margin; labor already paid
        if m >= sop and s["rev"][m]:
            cash[m] -= s["rev"][m] * s["rev_cost"][m]      # fixture-block/nest update
        if m == sop + 1:
            cash[m] += 100e3                               # working-capital release

        if cfg["upgrade"] and not upgraded and m > sop:
            sustain = sustain + 1 if d[m] > cfg["upgrade"]["thresh"] else 0
            if sustain >= 2:
                cash[m] -= cfg["upgrade"]["cost"]
                cap = cfg["upgrade"]["new_cap"]
                upgraded = True

    salvage = cfg["total_capex"] * cfg["resale"] * 0.5
    disc = (1 + DISC_M) ** -np.arange(MONTHS)
    npv = float((cash * disc).sum() + salvage * disc[-1])
    cum = cash.cumsum()
    pay = next((m for m in range(MONTHS) if cum[m] > 0), None)
    return npv, float(cum.min()), pay


def run_negotiate(s):
    d = demand_path(s)
    disc_won = s["nego_disc"] if s["nego_win"] else 0.03
    cash = np.zeros(MONTHS)
    cash[1] -= 15e3
    for m in range(3, MONTHS):
        cash[m] += d[m] * BUY0 * (1 + s["buy_esc"]) ** (m / 12) * disc_won
    disc = (1 + DISC_M) ** -np.arange(MONTHS)
    cum = cash.cumsum()
    return float((cash * disc).sum()), float(cum.min()), next((m for m in range(MONTHS) if cum[m] > 0), None)


def main():
    rng = np.random.default_rng(20260611)
    scenarios = [draw_scenario(rng) for _ in range(N_SIMS)]
    names = list(STRATEGIES) + ["E_renegotiate"]
    res = {n: [] for n in names}
    for s in scenarios:
        for n, cfg in STRATEGIES.items():
            res[n].append(run_strategy(cfg, s))
        res["E_renegotiate"].append(run_negotiate(s))

    print(f"{'strategy':<16}{'meanNPV':>8}{'P10':>8}{'P50':>8}{'P90':>8}{'%>0':>6}"
          f"{'trough50':>10}{'trough10':>10}{'payback50':>10}")
    for n in names:
        npv = np.array([r[0] for r in res[n]]) / 1e3
        tr = np.array([r[1] for r in res[n]]) / 1e3
        pb = [r[2] for r in res[n] if r[2] is not None]
        print(f"{n:<16}{npv.mean():>8.0f}{np.percentile(npv,10):>8.0f}{np.percentile(npv,50):>8.0f}"
              f"{np.percentile(npv,90):>8.0f}{(npv>0).mean()*100:>5.0f}%{np.percentile(tr,50):>10.0f}"
              f"{np.percentile(tr,10):>10.0f}{(str(int(np.median(pb))) if pb else '—'):>10}")

    mat = np.array([[res[n][i][0] for n in names] for i in range(N_SIMS)])
    best = mat.argmax(axis=1)
    print("\nWins (best NPV on the same world-draw):")
    for j, n in enumerate(names):
        print(f"  {n:<16}{(best == j).sum():>4} /{N_SIMS}")

    print("\nMedian NPV ($K) by realized 5-yr demand-growth regime:")
    g = np.array([s["growth"] for s in scenarios])
    bands = {"shrink <1.0": g < 1.0, "flat 1.0-1.1": (g >= 1.0) & (g < 1.10),
             "grow 1.1-1.35": (g >= 1.10) & (g < 1.35), "fast >1.35": g >= 1.35}
    hdr = "".join(f"{b:>16}" for b in bands)
    print(f"{'strategy':<16}{hdr}")
    for n in names:
        npv = np.array([r[0] for r in res[n]]) / 1e3
        print(f"{n:<16}" + "".join(f"{np.median(npv[msk]):>16.0f}" for msk in bands.values()))
    print(f"{'n in band':<16}" + "".join(f"{int(m.sum()):>16}" for m in bands.values()))

    print("\nRegret vs best choice per draw, median/P90 ($K):")
    for j, n in enumerate(names):
        regret = (mat.max(axis=1) - mat[:, j]) / 1e3
        print(f"  {n:<16} median {np.median(regret):>6.0f}   P90 {np.percentile(regret,90):>6.0f}")


if __name__ == "__main__":
    main()
