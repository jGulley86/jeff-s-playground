"""Data ingestion connectors: turn live NetSuite + Google Drive data into a PlanningInput.

Both connectors are TRANSPORT-AGNOSTIC: they take an injected callable that actually fetches data,
so the same mapping code works whether the fetch happens over the NetSuite REST/SuiteQL API
(production, credential-driven) or via the NetSuite MCP connector (an agent pulls a live snapshot
and materializes it). This keeps the record->model mapping testable and in one place.
"""
