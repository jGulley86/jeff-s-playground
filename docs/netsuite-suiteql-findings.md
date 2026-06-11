# NetSuite SuiteQL — Live Schema Findings (SlipRobotics account)

*Verified live on 2026-06-11 against the production account via the NetSuite MCP
SuiteQL tool. These are empirical results from the real account, replacing the
research-based field-name guesses in `scheduler-poc/aps/connectors/netsuite.py`.*

## TL;DR — two different SuiteQL namespaces

There are **two** ways this project reaches SuiteQL, and they expose **different schemas**:

| | MCP tool (`ns_runCustomSuiteQL`) | Production REST (`pull_netsuite.py`) |
|---|---|---|
| Endpoint | NetSuite SuiteAnalytics **search** layer | `/services/rest/query/v1/suiteql` (full SuiteQL) |
| Field set | **Restricted, flat** — only search-exposed fields | Full record schema |
| `GROUP BY` / CTEs | **Not supported** (returns "search error") | Supported |
| `metadata-catalog` | **403** — role lacks *REST Web Services* feature | Available with the feature |
| Good for | **Validating connectivity + reading core data** | **Production pulls** |

**Conclusion:** use the MCP connection to *validate and spot-check* live data; build the
*production* pull on the OAuth2 M2M REST path (`pull_netsuite.py`) with a role that has the
**REST Web Services** feature enabled. The connector's `query()` is transport-agnostic, but
field availability is not — queries verified below note which namespace confirmed them.

## Account shape (verified)

- Single subsidiary.
- ~2,658 `item` records; **574** `itemtype='Assembly'` (MAKE), the rest mostly `'InvtPart'` (BUY).
- **443** `bom` records, **498** `bomrevision` records (multiple revisions per BOM).
- 2,481 `itemvendor` rows (multiple vendors per item).
- 2,736 `inventorybalance` rows (multi-location: 8, 10, 11, 21, 22, …).
- Transactions include `PurchOrd` and `SalesOrd`; only ~30 sales orders total.

## Verified columns (MCP search namespace)

Unknown columns return: `Unknown identifier 'X'. Available identifiers are: {table=table}`
(the error lists table aliases, **not** columns — so discovery is by probing).

| Table | Confirmed-usable columns | Confirmed **absent** here |
|---|---|---|
| `item` | `id, itemid, itemtype, displayname, cost, totalquantityonhand, purchasedescription, isinactive` | `leadtime`, `leadtimedays`, `reorderpoint`, `baseprice`, `billofmaterials` |
| `bom` | `id, name` (name encodes the assembly, e.g. `106136_BOM1`) | `assembly`, `masterproduction` |
| `bomrevision` | `id, name, billofmaterials` (→ `bom.id`) | `bom`, `iscurrentrevision`, `effectivestartdate` |
| `bomrevisioncomponent` | `id, bomrevision` (→`bomrevision.id`), `item` (→`item.id`), `quantity, componentyield, itemsource` | `billofmaterials` |
| `itemvendor` | `item` (→`item.id`), `vendor` (→`vendor.id`), `purchaseprice, preferredvendor` | `leadtime`, `schedulebcost` |
| `inventorybalance` | `item, location, quantityonhand, quantityavailable` | (use this, **not** `aggregateitemlocation`) |
| `transaction` | `id, type, status, trandate, duedate, tranid, entity` | — |
| `transactionline` | `transaction, item, quantity, mainline, expectedshipdate, quantitybilled` | — |

Enumerated values seen: `itemtype` ∈ {`Assembly`, `InvtPart`, …}; `transaction.type` ∈
{`PurchOrd`, `SalesOrd`}; single-char `status` (PO `H`; SO `G`,`F`) — **not** the
`PurchOrd:B` form. Dates render `M/D/YYYY` (e.g. `5/29/2026`).

## Joins / relationships (verified shape)

```
bomrevisioncomponent.bomrevision  → bomrevision.id
bomrevision.billofmaterials       → bom.id
bomrevisioncomponent.item         → item.id      (translate to item.itemid!)
itemvendor.item                   → item.id
itemvendor.vendor                 → vendor.id
inventorybalance.item             → item.id
transactionline.transaction       → transaction.id
transactionline.item              → item.id
```

**Latent bug this revealed:** every `*.item` reference is an internal **id**, but the engine
keys items by **`itemid`** (the SKU string). All queries that emit a `sku`/`component_sku` from a
non-`item` table MUST join `item` and select `item.itemid`, or the rows silently fail to match.

## Open items / modeling decisions

1. **Purchase lead time is not a queryable field** in this namespace (`item.leadtime`,
   `item.leadtimedays`, `itemvendor.leadtime` all absent). Options: (a) verify on the REST path
   with a role that exposes it / a custom field; (b) **maintain a per-vendor/per-item lead-time
   table** alongside the snapshot (recommended — feeds the sourcing optimizer directly). Until
   then the connector defaults missing lead time and the optimizer still runs.
2. **Assembly → BOM link** has no foreign key here; `bom.name`/`bomrevision.name` encode the
   assembly part number, but inconsistently: item `106136-R04` → bom `106136_BOM1` (revision
   dropped) while item `106901-R02` → bom `106901-R02_BOM1` (revision kept). Resolver strategy:
   prefer a bom whose name starts with the **full itemid**, else fall back to the **base part
   number** (chars before the first `-`/`_`). The REST schema should expose the real link.
3. **Current revision:** no `iscurrentrevision` here → take the **max `bomrevision.id`** per BOM.
   REST exposes the flag; prefer it when available.
4. **Sales-order due dates are null** on the SO header → independent-demand timing must come from
   the Drive forecast (existing `gdrive` connector) or `transactionline.expectedshipdate`, not the
   SO header.
5. **Build times are not in NetSuite** → supplied by a maintained per-product config (as intended).

## Pilot anchors (SlipLift, Heavy Tray, Light Tray)

| Product line | Assembly item (id) | BOM (id) | Current revision (max id) |
|---|---|---|---|
| SlipLift | `106136-R04` (17002) | `106136_BOM1` (326) | `106136_REV12` (575) |
| Heavy Tray | `106901-R02` (16573) | `106901-R02_BOM1` (443) | `106901-R02_REV1` (541) |
| Light Tray | `106997-R01` (14276) | `106997-R01_BOM1` (357) | `106997-R01_REV1` (472) |
