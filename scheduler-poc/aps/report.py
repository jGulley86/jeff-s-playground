"""Self-contained HTML report: KPIs + Gantt + promise dates + sourcing + exceptions (iteration 10).

Dependency-free (inline CSS, absolutely-positioned divs for the Gantt) so it opens in any browser
with no build step. Procurement lead times render as bars from day 0 to material-ready; builds render
on their stations; late finished-goods are flagged red.
"""

from __future__ import annotations

import html

from .model import PlanningInput
from .scheduler import ScheduleResult

try:
    from .connectors.writeback import WritebackPlan
except Exception:  # pragma: no cover
    WritebackPlan = None


_CSS = """
body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px;color:#1b1f24;background:#fafbfc}
h1{font-size:20px;margin:0 0 4px} h2{font-size:15px;margin:24px 0 8px;color:#374151}
.kpis{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}
.kpi{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:10px 14px;min-width:120px}
.kpi .v{font-size:22px;font-weight:600} .kpi .l{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.04em}
.kpi.bad .v{color:#dc2626} .kpi.good .v{color:#059669}
table{border-collapse:collapse;width:100%;background:#fff;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden}
th,td{text-align:left;padding:7px 10px;font-size:13px;border-bottom:1px solid #f0f1f3}
th{background:#f6f8fa;font-weight:600;color:#374151}
.late{color:#dc2626;font-weight:600}.ontime{color:#059669}
.gantt{position:relative;background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:8px 8px 8px 150px;overflow-x:auto}
.row{position:relative;height:26px;margin:3px 0}
.label{position:absolute;left:-148px;width:140px;font-size:12px;line-height:26px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#374151}
.bar{position:absolute;height:18px;top:4px;border-radius:4px;font-size:10px;color:#fff;line-height:18px;padding:0 5px;box-sizing:border-box;white-space:nowrap;overflow:hidden}
.build{background:#2563eb}.proc{background:#9ca3af}.proc.exp{background:#d97706}
.axis{position:relative;height:18px;border-top:1px solid #e5e7eb;margin-top:6px;color:#9ca3af;font-size:10px}
.tick{position:absolute;border-left:1px solid #eceef0;height:9999px;top:-9999px}
.exc{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:4px 0}
.exc .item{padding:6px 12px;border-bottom:1px solid #f0f1f3;font-size:13px}
.exc .critical{border-left:4px solid #dc2626}.exc .warn{border-left:4px solid #d97706}.exc .info{border-left:4px solid #2563eb}
.muted{color:#6b7280;font-size:12px}
"""


def render_html(pin: PlanningInput, sched: ScheduleResult, writeback=None,
                title: str = "Production Schedule") -> str:
    e = html.escape
    # horizon for scaling = a bit past the last activity
    max_day = max([sched.makespan] + [s.ready_day for s in sched.sourcing]
                  + [d.completion_day for d in sched.demand_results] + [1])
    px_per_day = max(900 // max(max_day, 1), 2)

    def bar(x0, x1, cls, label):
        left = x0 * px_per_day
        width = max((x1 - x0) * px_per_day, 6)
        return f'<div class="bar {cls}" style="left:{left}px;width:{width}px" title="{e(label)}">{e(label)}</div>'

    # KPIs
    late = sum(1 for d in sched.demand_results if d.tardiness > 0)
    n_exc = len(writeback.exceptions) if writeback else 0
    kpis = [
        ("Status", e(sched.status), ""),
        ("Total tardiness", f"{sched.total_tardiness}d", "bad" if sched.total_tardiness else "good"),
        ("Sourcing cost", f"${sched.total_cost:,}", ""),
        ("Makespan", f"{sched.makespan}d", ""),
        ("Late orders", str(late), "bad" if late else "good"),
        ("Exceptions", str(n_exc), "bad" if n_exc else "good"),
    ]
    kpi_html = "".join(
        f'<div class="kpi {c}"><div class="v">{v}</div><div class="l">{e(l)}</div></div>'
        for l, v, c in kpis)

    # Gantt rows: procurement (gray/orange) then builds (blue)
    rows = []
    for s in sorted(sched.sourcing, key=lambda s: s.ready_day):
        exp = "exp" if ("air" in s.mode_label.lower() or "prem" in s.mode_label.lower()) else ""
        rows.append(f'<div class="row"><span class="label">{e(s.sku)}</span>'
                    + bar(0, s.ready_day, f"proc {exp}", f"{s.mode_label} {s.lead_time_days}d") + "</div>")
    for b in sched.builds:
        rows.append(f'<div class="row"><span class="label">{e(b.sku)} ({e(b.uid.split("/")[0])})</span>'
                    + bar(b.start, b.end, "build", f"{b.station} {b.start}-{b.end}") + "</div>")
    # axis ticks every ~ max_day/10 days
    step = max(max_day // 10, 1)
    ticks = "".join(f'<span class="tick" style="left:{d*px_per_day}px"></span>'
                    f'<span style="position:absolute;left:{d*px_per_day}px">{d}</span>'
                    for d in range(0, max_day + 1, step))
    gantt = f'<div class="gantt">{"".join(rows)}<div class="axis">{ticks}</div></div>'

    # Promise dates
    pr_rows = "".join(
        f'<tr><td>{e(d.order_id)}</td><td>{e(d.sku)}</td><td>{d.qty}</td><td>{d.due_day}</td>'
        f'<td>{d.completion_day}</td><td class="{"late" if d.tardiness else "ontime"}">'
        f'{"LATE " + str(d.tardiness) + "d" if d.tardiness else "on time"}</td></tr>'
        for d in sched.demand_results)
    promise = (f'<table><tr><th>Order</th><th>SKU</th><th>Qty</th><th>Due</th><th>Done</th>'
               f'<th>Status</th></tr>{pr_rows}</table>')

    # Sourcing
    src_rows = "".join(
        f'<tr><td>{e(s.sku)}</td><td>{s.qty}</td><td>{e(s.mode_label)}</td><td>{e(s.supplier)}</td>'
        f'<td>{s.lead_time_days}d</td><td>day {s.ready_day}</td><td>${s.cost:,}</td></tr>'
        for s in sorted(sched.sourcing, key=lambda s: s.sku))
    sourcing = (f'<table><tr><th>Part</th><th>Qty</th><th>Mode</th><th>Vendor</th><th>Lead</th>'
                f'<th>Ready</th><th>Cost</th></tr>{src_rows}</table>')

    # Exceptions
    if writeback and writeback.exceptions:
        exc_items = "".join(
            f'<div class="item {e(x.severity)}"><b>{e(x.kind)}</b> · {e(x.ref)} — {e(x.detail)}</div>'
            for x in writeback.exceptions)
        exceptions = f'<div class="exc">{exc_items}</div>'
    else:
        exceptions = '<p class="muted">No exceptions — plan is clean.</p>'

    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{e(title)}</title>
<style>{_CSS}</style></head><body>
<h1>{e(title)}</h1>
<p class="muted">{len(pin.items)} items · {len(pin.demand)} demand lines · horizon {pin.horizon_days}d</p>
<div class="kpis">{kpi_html}</div>
<h2>Schedule (Gantt — procurement lead times in gray/orange, builds in blue)</h2>{gantt}
<h2>Promise dates</h2>{promise}
<h2>Sourcing decisions</h2>{sourcing}
<h2>Exceptions</h2>{exceptions}
</body></html>"""


def write_report(path: str, pin: PlanningInput, sched: ScheduleResult, writeback=None,
                 title: str = "Production Schedule") -> str:
    htmls = render_html(pin, sched, writeback, title)
    with open(path, "w") as f:
        f.write(htmls)
    return path
