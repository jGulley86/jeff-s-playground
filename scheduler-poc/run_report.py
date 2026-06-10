"""Iteration 10 demo: generate an HTML schedule report (Gantt + exceptions).

    python run_report.py [output.html]
"""

from __future__ import annotations

import sys

from aps.connectors.writeback import build_writeback
from aps.mrp import run_mrp
from aps.report import write_report
from aps.scheduler import schedule
from aps.seed import build_seed


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "schedule_report.html"
    pin = build_seed()
    sched = schedule(pin)
    wb = build_writeback(pin, sched, run_mrp(pin))
    path = write_report(out, pin, sched, wb, title="SlipBot Production Schedule")
    print(f"Wrote {path}  ({wb.summary()})")


if __name__ == "__main__":
    main()
