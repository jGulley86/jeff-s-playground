"""Google Drive / Sheets -> PlanningInput overlays (transport-agnostic).

Your Drive holds operational data the ERP may not: a Demand Forecast sheet, a Robot Inventory sheet,
a Run Out Sheet. These often lead or correct NetSuite for planning. This module maps tabular sheet
rows (list[dict] keyed by header) onto demand / inventory overlays, given an injected reader.

    def read_sheet(file_id: str, tab: str | None = None) -> list[dict]:
        # production: Sheets API;  or (agent): Drive MCP read -> rows
        ...

    overlay = DriveIngestor(read_sheet).demand_from_forecast("<file_id>")
"""

from __future__ import annotations

from typing import Callable

from ..model import DemandLine, InventoryRecord

ReadSheetFn = Callable[..., list[dict]]


def _first(row: dict, *names: str, default=None):
    """Fetch a column by any of several possible header spellings (sheets are messy)."""
    lowered = {k.strip().lower(): v for k, v in row.items()}
    for n in names:
        if n.lower() in lowered and lowered[n.lower()] not in ("", None):
            return lowered[n.lower()]
    return default


class DriveIngestor:
    def __init__(self, read_sheet: ReadSheetFn):
        self.read_sheet = read_sheet

    def demand_from_forecast(self, file_id: str, tab: str | None = None,
                             day0=None) -> list[DemandLine]:
        """Map a 'Demand Forecast and Fulfillment Confirmation'-style sheet to DemandLines."""
        from .netsuite import _to_days
        out: list[DemandLine] = []
        for row in self.read_sheet(file_id, tab):
            sku = _first(row, "sku", "item", "product", "model")
            qty = _first(row, "qty", "quantity", "units", "bots")
            due = _first(row, "due", "due date", "need date", "ship date", "date")
            if not sku or not qty:
                continue
            out.append(DemandLine(
                sku=str(sku), qty=int(float(qty)),
                due_day=_to_days(str(due), day0) if due else 0,
                order_id=str(_first(row, "order", "order id", "so", default="")),
            ))
        return out

    def inventory_from_sheet(self, file_id: str, tab: str | None = None) -> list[InventoryRecord]:
        """Map a 'Robot Inventory & Disposition' / 'Run Out Sheet'-style sheet to InventoryRecords."""
        out: list[InventoryRecord] = []
        for row in self.read_sheet(file_id, tab):
            sku = _first(row, "sku", "item", "part", "component", "model")
            qty = _first(row, "on hand", "on_hand", "qty", "quantity", "available", "stock")
            if not sku or qty in (None, ""):
                continue
            out.append(InventoryRecord(
                sku=str(sku), on_hand=int(float(qty)),
                location=str(_first(row, "location", "warehouse", "site", default="MAIN")),
            ))
        return out
