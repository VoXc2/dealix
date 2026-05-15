#!/usr/bin/env python3
"""scripts/test_moyasar_webhook_local.py

Simulate a Moyasar webhook end-to-end against a running Dealix API,
without needing a real Moyasar account or sk_live_ key.

What it does:
  1. Builds a payment_paid (or _failed / _refunded / _authorized) payload that
     looks exactly like Moyasar's real shape.
  2. Computes the secret_token field using the local MOYASAR_WEBHOOK_SECRET
     env var so the webhook accepts it (the live verifier in
     dealix/payments/moyasar.py:verify_webhook).
  3. POSTs it to /api/v1/webhooks/moyasar.
  4. Reads back the response.
  5. Optionally queries the DB and confirms the payment row was upserted.

Use it before launch to validate the wiring without real Moyasar traffic.

Usage:
    # Against local dev API
    MOYASAR_WEBHOOK_SECRET=shared-secret-xyz \\
        python scripts/test_moyasar_webhook_local.py \\
        --base-url http://localhost:8000 \\
        --event-type payment_paid \\
        --amount 100

    # With DB verification (asserts payments row exists)
    MOYASAR_WEBHOOK_SECRET=shared-secret-xyz \\
    DATABASE_URL=postgresql://... \\
        python scripts/test_moyasar_webhook_local.py --verify-db

Exit codes:
    0  webhook accepted + DB row present (if --verify-db)
    1  webhook rejected
    2  DB verification failed
    3  config error
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid


EVENT_TYPES = ("payment_authorized", "payment_paid", "payment_failed", "payment_refunded")


_REDACTED = "<redacted>"


def _redact(d: dict) -> dict:
    """Return a copy of `d` with any sensitive top-level fields masked.
    Used before logging so secret_token never flows into stdout."""
    if not isinstance(d, dict):
        return d
    out = {}
    for k, v in d.items():
        if isinstance(k, str) and k.lower() in {"secret_token", "secret", "signature", "x-moyasar-signature"}:
            out[k] = _REDACTED
        elif isinstance(v, dict):
            out[k] = _redact(v)
        else:
            out[k] = v
    return out


def build_payload(event_type: str, amount: int, plan: str, email: str) -> dict:
    """Build a Moyasar-shaped event payload WITHOUT the secret_token.
    The secret is injected at request-build time in post_webhook so it
    never enters any dict that might be logged or stringified."""
    payment_id = f"pay_test_{uuid.uuid4().hex[:16]}"
    status = {
        "payment_authorized": "authorized",
        "payment_paid": "paid",
        "payment_failed": "failed",
        "payment_refunded": "refunded",
    }[event_type]

    return {
        "id": f"evt_test_{uuid.uuid4().hex[:12]}",
        "type": event_type,
        "data": {
            "object": "payment",
            "id": payment_id,
            "status": status,
            "amount": amount,
            "currency": "SAR",
            "metadata": {"plan": plan, "email": email},
        },
    }


def post_webhook(base_url: str, payload: dict) -> tuple[int, str]:
    """POST the payload after injecting secret_token at the boundary.
    The secret is read here (not in build_payload) so it never enters
    a dict that might be logged elsewhere in this script."""
    secret = os.environ.get("MOYASAR_WEBHOOK_SECRET")
    if not secret:
        print("[error] MOYASAR_WEBHOOK_SECRET must be set", file=sys.stderr)
        sys.exit(3)
    body_dict = dict(payload)
    body_dict["secret_token"] = secret
    body = json.dumps(body_dict).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/api/v1/webhooks/moyasar",
        data=body, method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, (exc.read().decode("utf-8") if exc.fp else "")


def verify_in_db(provider_payment_id: str, expected_status: str) -> bool:
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("[error] --verify-db requires DATABASE_URL", file=sys.stderr)
        return False
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("[error] psycopg2 required: pip install psycopg2-binary", file=sys.stderr)
        return False
    url = re.sub(r"^postgresql\+asyncpg://", "postgresql://", db_url)
    conn = psycopg2.connect(url)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # Tolerant of timing: poll for up to 5 seconds
    for _ in range(10):
        try:
            cur.execute(
                "SELECT status, amount_halalas, plan, email FROM payments "
                "WHERE provider_payment_id = %s",
                (provider_payment_id,),
            )
            row = cur.fetchone()
            if row:
                conn.close()
                if row["status"] == expected_status:
                    print(f"[db] ✓ row found: {dict(row)}")
                    return True
                else:
                    print(f"[db] ✗ row found but status={row['status']!r} != {expected_status!r}",
                          file=sys.stderr)
                    return False
        except Exception as exc:
            # Table may not exist (graceful fallback path) — record and move on
            print(f"[db] query error: {exc}", file=sys.stderr)
            conn.rollback()
        time.sleep(0.5)
    conn.close()
    print(f"[db] ✗ no row found for {provider_payment_id} after 5s", file=sys.stderr)
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=os.environ.get("BASE_URL", "http://localhost:8000"))
    parser.add_argument("--event-type", choices=EVENT_TYPES, default="payment_paid")
    parser.add_argument("--amount", type=int, default=100, help="halalas (1 SAR = 100)")
    parser.add_argument("--plan", default="pilot_1sar")
    parser.add_argument("--email", default="preflight@dealix.sa")
    parser.add_argument("--verify-db", action="store_true",
                        help="query DATABASE_URL and confirm payments row was upserted")
    args = parser.parse_args()

    payload = build_payload(args.event_type, args.amount, args.plan, args.email)
    print(f"[sim] POST {args.base_url}/api/v1/webhooks/moyasar  payment_id={payload['data']['id']}")

    code, body = post_webhook(args.base_url, payload)
    print(f"[sim] response: HTTP {code}")
    print(f"[sim] body: {body[:300]}")

    if code != 200:
        print(f"[sim] FAIL — webhook returned {code}, expected 200", file=sys.stderr)
        return 1
    print("[sim] ✓ webhook accepted")

    if args.verify_db:
        expected_status = payload["data"]["status"]
        if not verify_in_db(payload["data"]["id"], expected_status):
            return 2
        print("[sim] ✓ DB row persisted")

    print("[sim] PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
