# NetSuite Direct-API Access — Governance One-Pager

*For review by cloud engineering. Scope: the APS scheduler's read pipeline
(`scheduler-poc/scripts/pull_netsuite.py`) and eventual plan write-back.*

## What this integration is

A scheduled job that pulls six read-only SuiteQL queries (items, BOMs, per-vendor sourcing,
inventory, open POs, open SOs) into a snapshot JSON consumed by the production scheduler, and —
later, behind an explicit dry-run gate — writes planned work orders / purchase orders back.

## Common objections, and how this design answers them

| Objection | Answer in this design |
|---|---|
| "Long-lived credentials" | Primary auth is **OAuth 2.0 client credentials (M2M)**: access tokens live ~60 minutes; the only long-lived material is a private key we control and can rotate at will (re-upload cert, no NetSuite user changes). TBA (non-expiring tokens) is supported only as a fallback and can be disabled. |
| "TBA is deprecated" | Agreed — NetSuite has announced no *new* TBA integrations as of 2027.1. That's why OAuth 2.0 M2M is the default path. |
| "Over-broad access" | The integration gets a **dedicated, least-privilege, read-only role** scoped to: items, BOM/BOM revision, item-vendor, inventory balances, purchase orders, sales orders. No PII-bearing records (employees, customers beyond SO headers), no write permissions in phase 1. |
| "Credential sprawl / who holds the secret" | One integration record, one keypair, stored in the team secret manager (or CI secret store). Never in the repo — `.gitignore` covers key files; the script reads from env/key-path only. |
| "No audit trail" | Every call is attributable to the dedicated integration record + role in NetSuite's login audit trail; the Concurrency Monitor and integration governance pages show usage. The script also logs row counts and failures per query. |
| "It'll hammer the API" | Read load is six paginated SuiteQL queries on a nightly cadence (plus on-demand replans), `Prefer: transient`, paged at 1000 rows — well inside account concurrency limits. No polling loops. |
| "Writes to the ERP from a script" | Write-back is a separate phase, **dry-run by default** (`aps/connectors/writeback.py`): it produces reviewable payloads; live writes require explicitly providing a create function and `dry_run=False`, and can use a second, separate role. |

## Requested from cloud engineering

1. Approve creation of one **Integration record** ("APS Scheduler — read") with OAuth 2.0
   client credentials, mapped to a service user + the least-privilege read role above.
2. The read role MUST include the **REST Web Services** feature/permission. Verified 2026-06-11:
   the role currently reachable via the MCP connector lacks it — full REST SuiteQL and the
   `metadata-catalog` return HTTP 403 `INSUFFICIENT_PERMISSION`. Without it, only NetSuite's
   restricted SuiteAnalytics *search* namespace is available (no `GROUP BY`, reduced field set);
   see `docs/netsuite-suiteql-findings.md`.
3. A home for the private key (secret manager entry) and a rotation cadence (e.g. 90 days).
4. (Phase 2, separate review) a write-scoped role for planned WO/PO creation.

**Data note for planners:** purchase **lead time is not a queryable field** in this account
(`item.leadtime` / `itemvendor.leadtime` don't exist). The sourcing optimizer needs it, so plan to
**maintain a per-vendor/per-item lead-time table** alongside the snapshot (or confirm a custom
field on the REST path). Details and the full verified schema are in the findings doc.

## Kill switch

Disable the integration record in NetSuite (Setup > Integration > Manage Integrations) — revokes
all access immediately without touching any user account.
