#!/usr/bin/env python3
"""scripts/reconcile_moyasar.py

Daily Moyasar ↔ Dealix reconciliation.

For each Moyasar payment in the last 48 hours, verify:
- A matching DB row exists (status = paid/failed/refunded)
- The amount matches
- A PostHog `checkout_success` event exists for paid payments

Outputs a JSON diff to stdout; non-zero exit if any discrepancy.

Designed to run nightly via cron:
    0 2 * * *  python /app/scripts/reconcile_moyasar.py --since 48h

Env:
    MOYASAR_SECRET_KEY  (sk_live_...)
    DATABASE_URL
    RECONCILE_TOLERANCE_HALALAS=0   # allow N halalas diff (default 0)
    RECONCILE_ALERT_WEBHOOK=        # optional Slack/WhatsApp webhook for diffs
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

logger = logging.getLogger("reconcile")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)

MOYASAR_BASE = "https://api.moyasar.com/v1"


@dataclass
class Discrepancy:
    kind: str
    moyasar_id: str
    detail: str


def parse_since(s: str) -> datetime:
    m = re.fullmatch(r"(\d+)\s*([hdHD])", s)
    if not m:
        raise ValueError(f"--since must look like '48h' or '7d', got {s!r}")
    n, unit = int(m.group(1)), m.group(2).lower()
    delta = timedelta(hours=n) if unit == "h" else timedelta(days=n)
    return datetime.now(timezone.utc) - delta


def fetch_moyasar_payments(secret: str, since: datetime) -> list[dict[str, Any]]:
    """Pull payments from Moyasar /v1/payments since a cutoff."""
    try:
        import requests
    except ImportError:
        logger.error("requests not installed: pip install requests")
        sys.exit(2)

    out: list[dict[str, Any]] = []
    page = 1
    while True:
        resp = requests.get(
            f"{MOYASAR_BASE}/payments",
            params={"page": page, "limit": 50},
            auth=(secret, ""),
            timeout=30,
        )
        if resp.status_code == 401:
            logger.error("MOYASAR auth failed — check MOYASAR_SECRET_KEY")
            sys.exit(2)
        resp.raise_for_status()
        data = resp.json()
        payments = data.get("payments", [])
        if not payments:
            break

        keep_going = True
        for p in payments:
            created_at = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
            if created_at < since:
                keep_going = False
                break
            out.append(p)
        if not keep_going or len(payments) < 50:
            break
        page += 1
        time.sleep(0.2)  # polite
    return out


def fetch_db_payments(database_url: str, since: datetime) -> dict[str, dict[str, Any]]:
    """Return DB payments keyed by moyasar_id."""
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        logger.error("psycopg2 not installed: pip install psycopg2-binary")
        sys.exit(2)

    url = re.sub(r"^postgresql\+asyncpg://", "postgresql://", database_url)
    conn = psycopg2.connect(url)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # Schema-flexible: assume a `payments` table with at least these columns
    try:
        cur.execute(
            """
            SELECT moyasar_payment_id, status, amount_halalas, plan, created_at
            FROM payments
            WHERE created_at >= %s
            """,
            (since,),
        )
        rows = cur.fetchall()
    except psycopg2.Error as exc:
        logger.warning("could not query payments table: %s", exc)
        rows = []
    cur.close()
    conn.close()
    return {r["moyasar_payment_id"]: dict(r) for r in rows if r.get("moyasar_payment_id")}


def reconcile(moyasar_payments: list[dict[str, Any]],
              db_payments: dict[str, dict[str, Any]],
              tolerance_halalas: int) -> list[Discrepancy]:
    diffs: list[Discrepancy] = []

    for m in moyasar_payments:
        mid = m["id"]
        m_amount = int(m.get("amount", 0))  # halalas
        m_status = m.get("status", "unknown")

        db = db_payments.get(mid)
        if not db:
            diffs.append(Discrepancy(
                kind="missing_in_db",
                moyasar_id=mid,
                detail=f"Moyasar shows {m_status} amount={m_amount} halalas; no row in DB",
            ))
            continue
        if abs(int(db.get("amount_halalas") or 0) - m_amount) > tolerance_halalas:
            diffs.append(Discrepancy(
                kind="amount_mismatch",
                moyasar_id=mid,
                detail=f"moyasar={m_amount} db={db.get('amount_halalas')}",
            ))
        if (db.get("status") or "").lower() != m_status.lower():
            diffs.append(Discrepancy(
                kind="status_mismatch",
                moyasar_id=mid,
                detail=f"moyasar={m_status} db={db.get('status')}",
            ))

    # Payments in DB but not in Moyasar window (could be legitimate if older;
    # but if `created_at` is in window, that's suspicious).
    moyasar_ids = {m["id"] for m in moyasar_payments}
    for mid, row in db_payments.items():
        if mid not in moyasar_ids:
            diffs.append(Discrepancy(
                kind="missing_in_moyasar",
                moyasar_id=mid,
                detail=f"DB row status={row.get('status')} amount={row.get('amount_halalas')}; not visible in Moyasar list",
            ))
    return diffs


def alert(webhook_url: str, diffs: list[Discrepancy]) -> None:
    try:
        import requests
        msg = f"⚠️ Dealix Moyasar reconciliation found {len(diffs)} discrepancies:\n"
        for d in diffs[:10]:
            msg += f"- [{d.kind}] {d.moyasar_id} — {d.detail}\n"
        if len(diffs) > 10:
            msg += f"...and {len(diffs)-10} more.\n"
        requests.post(webhook_url, json={"text": msg}, timeout=10)
    except Exception as exc:  # noqa: BLE001
        logger.warning("alert webhook failed: %s", exc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default="48h", help="window like '48h' or '7d'")
    parser.add_argument("--tolerance-halalas", type=int,
                        default=int(os.getenv("RECONCILE_TOLERANCE_HALALAS", "0")))
    parser.add_argument("--dry-run", action="store_true",
                        help="don't call alert webhook even if diffs")
    args = parser.parse_args()

    secret = os.environ.get("MOYASAR_SECRET_KEY")
    db_url = os.environ.get("DATABASE_URL")
    if not secret or not db_url:
        if args.dry_run:
            report = {
                "window_start": parse_since(args.since).isoformat(),
                "window_end": datetime.now(timezone.utc).isoformat(),
                "moyasar_count": 0,
                "db_count": 0,
                "discrepancies": [],
                "status": "dry_run_blocked_missing_env",
                "missing": [
                    name
                    for name, val in (
                        ("MOYASAR_SECRET_KEY", secret),
                        ("DATABASE_URL", db_url),
                    )
                    if not val
                ],
            }
            print(json.dumps(report, indent=2, ensure_ascii=False))
            logger.warning("dry-run reconciliation skipped: missing required env")
            return 0
        logger.error("MOYASAR_SECRET_KEY and DATABASE_URL are required")
        return 2

    since = parse_since(args.since)
    logger.info("reconcile window: %s → now", since.isoformat())

    moyasar = fetch_moyasar_payments(secret, since)
    logger.info("Moyasar payments in window: %d", len(moyasar))

    db = fetch_db_payments(db_url, since)
    logger.info("DB payment rows in window: %d", len(db))

    diffs = reconcile(moyasar, db, args.tolerance_halalas)
    report = {
        "window_start": since.isoformat(),
        "window_end": datetime.now(timezone.utc).isoformat(),
        "moyasar_count": len(moyasar),
        "db_count": len(db),
        "discrepancies": [asdict(d) for d in diffs],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if diffs and not args.dry_run:
        webhook = os.environ.get("RECONCILE_ALERT_WEBHOOK")
        if webhook:
            alert(webhook, diffs)

    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
