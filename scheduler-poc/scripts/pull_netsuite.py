#!/usr/bin/env python3
"""Pull a planning snapshot directly from NetSuite via SuiteQL REST (no MCP required).

Two auth methods, picked automatically from the environment:

  PREFERRED — OAuth 2.0 client credentials (M2M, certificate-based). NetSuite's modern
  server-to-server method: short-lived access tokens, rotatable keypair, no non-expiring
  shared secrets. Setup steps are in make_session_oauth2's docstring.

      pip install requests PyJWT cryptography
      export NS_ACCOUNT=7233773
      export NS_CLIENT_ID=...  NS_CERT_ID=...  NS_PRIVATE_KEY_PATH=ns_key.pem
      python scripts/pull_netsuite.py netsuite_snapshot.json

  FALLBACK — Token-Based Authentication (TBA / OAuth 1.0 HMAC-SHA256). Works today but tokens
  never expire and NetSuite has announced no NEW TBA integrations as of 2027.1.

      pip install requests requests-oauthlib
      export NS_ACCOUNT=7233773
      export NS_CONSUMER_KEY=... NS_CONSUMER_SECRET=... NS_TOKEN_ID=... NS_TOKEN_SECRET=...
      python scripts/pull_netsuite.py netsuite_snapshot.json

Governance posture (see docs/netsuite-access-governance.md):
  read-only least-privilege role, dedicated integration record, secrets in a secret manager
  (never committed), short-lived tokens (OAuth2), NetSuite-side audit via the integration record.

The snapshot feeds the engine:
    python run.py --snapshot netsuite_snapshot.json

Account ID note: it's in your NetSuite URL, e.g. 7233773 (sandbox 7233773_SB1 becomes
7233773-sb1.suitetalk.api.netsuite.com in the domain).

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

from aps.connectors.netsuite import SuiteQL  # noqa: E402


def _base_url(account: str) -> str:
    return f"https://{account.lower().replace('_', '-')}.suitetalk.api.netsuite.com"


def make_session_tba(account: str, ck: str, cs: str, tid: str, ts: str) -> tuple[requests.Session, str]:
    """Token-Based Authentication (OAuth 1.0 HMAC-SHA256). Simple, but tokens never expire and
    NetSuite has announced no NEW TBA integrations as of 2027.1 — prefer OAuth 2.0 M2M below."""
    from requests_oauthlib import OAuth1
    auth = OAuth1(
        client_key=ck, client_secret=cs,
        resource_owner_key=tid, resource_owner_secret=ts,
        signature_method="HMAC-SHA256",
        realm=account.upper(),
    )
    s = requests.Session()
    s.auth = auth
    s.headers.update({"Content-Type": "application/json", "Prefer": "transient"})
    return s, _base_url(account)


def make_session_oauth2(account: str, client_id: str, cert_id: str,
                        private_key_path: str) -> tuple[requests.Session, str]:
    """OAuth 2.0 client credentials (machine-to-machine), certificate-based — NetSuite's modern
    recommended server-to-server auth. No browser, no non-expiring shared secret; access tokens
    are short-lived (~60 min) and the keypair can be rotated without touching NetSuite users.

    NetSuite setup (Setup > Integration > OAuth 2.0 Client Credentials Setup):
      1. Integration record with OAuth 2.0 client credentials enabled -> Client ID.
      2. Generate a keypair locally:
           openssl req -x509 -newkey rsa:4096 -keyout ns_key.pem -out ns_cert.pem -days 365 -nodes
         Upload ns_cert.pem in the Client Credentials mapping (pick the integration, user, role)
         -> Certificate ID (the `kid`).
      3. Role: least-privilege, read-only on the record types queried here.
    """
    import time
    import jwt  # PyJWT, with `cryptography` for RS/PS signing

    base = _base_url(account)
    token_url = f"{base}/services/rest/auth/oauth2/v1/token"
    now = int(time.time())
    with open(private_key_path) as f:
        private_key = f.read()
    assertion = jwt.encode(
        {"iss": client_id, "scope": ["rest_webservices"], "aud": token_url,
         "iat": now, "exp": now + 300},
        private_key, algorithm="PS256", headers={"kid": cert_id},
    )
    r = requests.post(token_url, data={
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": assertion,
    }, timeout=60)
    r.raise_for_status()
    access_token = r.json()["access_token"]

    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {access_token}",
                      "Content-Type": "application/json", "Prefer": "transient"})
    return s, base


def make_session() -> tuple[requests.Session, str]:
    """Pick auth from the environment: OAuth 2.0 M2M if NS_CLIENT_ID is set, else TBA."""
    account = os.environ["NS_ACCOUNT"]
    if os.environ.get("NS_CLIENT_ID"):
        return make_session_oauth2(
            account, os.environ["NS_CLIENT_ID"], os.environ["NS_CERT_ID"],
            os.environ["NS_PRIVATE_KEY_PATH"],
        )
    return make_session_tba(
        account, os.environ["NS_CONSUMER_KEY"], os.environ["NS_CONSUMER_SECRET"],
        os.environ["NS_TOKEN_ID"], os.environ["NS_TOKEN_SECRET"],
    )


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
        session, base = make_session()
    except KeyError as e:
        sys.exit(f"Missing env var {e}. Set either the OAuth 2.0 M2M vars (NS_ACCOUNT, NS_CLIENT_ID,"
                 f" NS_CERT_ID, NS_PRIVATE_KEY_PATH) or the TBA vars (NS_ACCOUNT, NS_CONSUMER_KEY,"
                 f" NS_CONSUMER_SECRET, NS_TOKEN_ID, NS_TOKEN_SECRET). See the docstring.")
    except FileNotFoundError as e:
        sys.exit(f"Private key not found: {e}")
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
