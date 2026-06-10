"""aps — an integrated, cost-aware, finite-capacity production scheduler.

Package layout (built incrementally over 5 iterations):

    model.py         core dataclasses (items, BOM, sourcing, inventory, demand, build specs)
    mrp.py           multi-level BOM explosion + gross-to-net + lead-time offsetting   [iter 1]
    scheduler.py     CP-SAT finite-capacity scheduling + sourcing choice               [iter 2]
    promising.py     CTP rush-order quoting (sandbox test-plan) + accept/reject         [iter 4]
    safety_stock.py  safety-stock / reorder-point computation                          [iter 5]
    connectors/      NetSuite (SuiteQL) + Google Drive ingestion                       [iter 3]
    seed.py          sample SlipBot-flavored dataset (fallback when no live data)

See ../../docs/production-scheduler-research.md for the research backing every design choice.
"""

__all__ = ["model", "mrp"]
