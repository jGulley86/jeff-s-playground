#!/usr/bin/env python3
"""Pull a planning snapshot directly from NetSuite via SuiteQL REST (no MCP required).

Authenticates with Token-Based Authentication (TBA / OAuth 1.0, HMAC-SHA256) — NetSuite's standard
server-to-server method that needs no browser. Dumps a snapshot JSON consumable by:

    python run.py --snapshot netsuite_snapshot.json

One-time NetSuite setup (admin, ~10 minutes):
  1. Setup > Company > Enable Features > SuiteCloud: check "Token-Based Authentication"
     and "REST Web Services".
  2. Setup > Integration > Manage Integrations > New:
     name it (e.g. "APS Scheduler"), check "Token-Based Authentication", save.
     COPY the Consumer Key / Consumer Secret (shown once).
  3. Setup > Users/Roles > Access Tokens > New:
     pick the integration, a user, and a role with read access to items, BOMs, transactions,
     vendors, inventory. COPY the Token ID / Token Secret (shown once).
  4. Your account ID is in your NetSuite URL, e.g. 7233773 (use 7233773_SB1 style for sandbox,
     with the underscore replaced by a hyphen in the domain: 7233773-sb1.suitetalk.api.netsuite.com).

Then:
    pip install requests requests-oauthlib
    export NS_ACCOUNT=7233773
    export NS_CONSUMER_KEY=...    NS_CONSUMER_SECRET=...
    export NS_TOKEN_ID=...        NS_TOKEN_SECRET=...
    python scripts/pull_netsuite.py netsuite_snapshot.json

The SuiteQL queries come from aps/connectors/netsuite.py and use field names from research that MUST
be verified against your account (Records Browser / metadata-catalog). On the first run this script
REPORTS any query that fails and continues, so you get a findings list instead of a crash.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import requests  # noqa: E402
from requests_oauthlib import OAuth1  # noqa: E402

from aps.connectors.netsuite import SuiteQL  # noqa: E402


def make_session(account: str, ck: str, cs: str, tid: str, ts: str) -> tuple[requests.Session, str]:
    host_acct = account.lower().replace("_", "-")
    base = f"https://{host_acct}.suitetalk.api.netsuite.com"
    auth = OAuth1(
        client_key=ck, client_secret=cs,
        resource_owner_key=tid, resource_owner_secret=ts,
        signature_method="HMAC-SHA256",
        realm=account.upper(),
    )
    s = requests.Session()
    s.auth = auth
    s.headers.update({"Content-Type": "application/json", "Prefer": "transient"})
    return s, base


def suiteql_all(session: requests.Session, base: str, sql: str, page_size: int = 1000) -> list[dict]:
    """Run a SuiteQL query, following pagination (limit/offset) until exhausted."""
    rows: list[dict] = []
    offset = 0
    while True:
        url = f"{base}/services/rest/query/v1/suiteql?limit={page_size}&offset={offset}"
        r = session.post(url, data=json.dumps({"q": " ".join(sql.split())}), timeout=120)
        r.raise_for_status()
        body = r.json()
        items = body.get("items", [])
        rows.extend(items)
        if not body.get("hasMore"):
            return rows
        offset += page_size


QUERIES = {
    "items": SuiteQL.ITEMS,
    "bom_lines": SuiteQL.BOM_LINES,
    "vendor_sourcing": SuiteQL.VENDOR_SOURCING,
    "inventory": SuiteQL.INVENTORY,
    "open_po": SuiteQL.OPEN_PO,
    "open_so": SuiteQL.OPEN_SO,
}


def main() -> None:
    out_path = sys.argv[1] if len(sys.argv) > 1 else "netsuite_snapshot.json"
    try:
        account = os.environ["NS_ACCOUNT"]
        ck, cs = os.environ["NS_CONSUMER_KEY"], os.environ["NS_CONSUMER_SECRET"]
        tid, ts = os.environ["NS_TOKEN_ID"], os.environ["NS_TOKEN_SECRET"]
    except KeyError as e:
        sys.exit(f"Missing env var {e}. See the docstring for setup steps.")

    session, base = make_session(account, ck, cs, tid, ts)
    snapshot: dict = {}
    findings: list[str] = []

    for name, sql in QUERIES.items():
        try:
            rows = suiteql_all(session, base, sql)
            snapshot[name] = rows
            print(f"  {name:<16} {len(rows):>6} rows")
        except requests.HTTPError as err:
            detail = ""
            try:
                detail = err.response.json().get("o:errorDetails", [{}])[0].get("detail", "")
            except Exception:
                detail = err.response.text[:200] if err.response is not None else str(err)
            snapshot[name] = []
            findings.append(f"{name}: HTTP {err.response.status_code if err.response is not None else '?'} — {detail}")
            print(f"  {name:<16} FAILED — recorded in findings, continuing")

    with open(out_path, "w") as f:
        json.dump(snapshot, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    if findings:
        print("\nFINDINGS (queries that need field-name fixes for your account):")
        for f_ in findings:
            print(f"  - {f_}")
        print("\nFix the corresponding SQL in aps/connectors/netsuite.py (use the Records Browser\n"
              "or GET /services/rest/record/v1/metadata-catalog to find the right names) and rerun.")
    else:
        print("All queries succeeded. Next: python run.py --snapshot " + out_path)


if __name__ == "__main__":
    main()
