#!/usr/bin/env python3
"""scripts/export_subject_data.py

Export all personal data Dealix holds about a single data subject (DSAR — PDPL Art. 12).

Usage:
    DATABASE_URL=postgresql://... python scripts/export_subject_data.py \
        --email subject@example.com \
        --output dsar_subject_2026_05_12.zip

    DATABASE_URL=postgresql://... python scripts/export_subject_data.py \
        --phone "+966500000000" \
        --output dsar_<request_id>.zip

The ZIP contains one JSON file per source table where the subject appears,
plus a manifest.json that lists every row's source. The ZIP is encrypted
with a password the operator must supply via --password or the
DSAR_EXPORT_PASSWORD env var (sent to the subject via a separate channel).

Identity verification is OUT OF SCOPE — that's done manually before this
script is run. See docs/ops/PDPL_RETENTION_POLICY.md §4.

The script is read-only. For erasure, use the erasure endpoint or a
separate scripted SQL with explicit row review.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from typing import Any

# Tables likely to contain personal data, paired with the column used for lookup.
# Some may not exist in every deployment — we skip-on-error gracefully.
TABLES = [
    ("accounts", ["email", "primary_email", "company_email"]),
    ("contacts", ["email", "phone"]),
    ("contact_records", ["email", "phone"]),
    ("demo_requests", ["email", "phone"]),
    ("customers", ["email", "phone"]),
    ("users", ["email"]),
    ("user_records", ["email"]),
    ("outreach_queue", ["recipient_email", "recipient_phone"]),
    ("email_send_log", ["recipient", "to_email"]),
    ("gmail_drafts", ["recipient_email"]),
    ("data_suppression_list", ["email", "phone"]),
    ("audit_log", ["user_email", "subject_email"]),
    ("audit_log_records", ["user_email", "subject_email"]),
    ("dsar_requests", ["email", "phone"]),
]


def normalize_db_url(url: str) -> str:
    return re.sub(r"^postgresql\+asyncpg://", "postgresql://", url)


def find_subject_rows(cur: Any, email: str | None, phone: str | None) -> dict[str, list[dict[str, Any]]]:
    """For each known table, search for rows matching the subject."""
    import psycopg2
    out: dict[str, list[dict[str, Any]]] = {}
    for table, candidate_cols in TABLES:
        # Discover which candidate columns actually exist
        cur.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_name = %s AND table_schema = 'public'
            """,
            (table,),
        )
        existing_cols = {row[0] for row in cur.fetchall()}
        match_cols = [c for c in candidate_cols if c in existing_cols]
        if not match_cols:
            continue

        clauses = []
        params: list[Any] = []
        if email and any(c.endswith("email") for c in match_cols):
            for c in match_cols:
                if c.endswith("email"):
                    clauses.append(f"LOWER({c}) = LOWER(%s)")
                    params.append(email)
        if phone and any(c.endswith("phone") or c == "recipient_phone" or c == "mobile" for c in match_cols):
            for c in match_cols:
                if c.endswith("phone") or c == "mobile":
                    clauses.append(f"{c} = %s")
                    params.append(phone)

        if not clauses:
            continue

        sql = f"SELECT * FROM {table} WHERE " + " OR ".join(clauses)
        try:
            cur.execute(sql, params)
            rows = cur.fetchall()
            if rows:
                # Convert any datetime/Decimal to JSON-friendly via str()
                out[table] = [
                    {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in r.items()}
                    for r in rows
                ]
        except psycopg2.Error as exc:
            print(f"[warn] could not query {table}: {exc}", file=sys.stderr)
            cur.connection.rollback()
            continue
    return out


def build_manifest(email: str | None, phone: str | None,
                   data: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "dsar_export_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject": {"email": email, "phone": phone},
        "tables": {t: len(rows) for t, rows in data.items()},
        "total_rows": sum(len(rows) for rows in data.values()),
        "notes": (
            "This export covers personal data identified in Dealix operational stores. "
            "It does NOT include backup files (encrypted at rest) or analytics aggregates "
            "(anonymised). For deletion requests, see PDPL_RETENTION_POLICY §4."
        ),
    }


def make_zip(output_path: str, manifest: dict[str, Any],
             data: dict[str, list[dict[str, Any]]], password: str | None) -> None:
    """Write a ZIP of per-table JSONs + manifest. If a password is given, encrypt with pyzipper."""
    if password:
        try:
            import pyzipper
        except ImportError:
            print("pyzipper not installed; install with: pip install pyzipper", file=sys.stderr)
            sys.exit(2)
        with pyzipper.AESZipFile(output_path, "w",
                                 compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode("utf-8"))
            zf.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
            for table, rows in data.items():
                zf.writestr(f"{table}.json", json.dumps(rows, indent=2, ensure_ascii=False, default=str))
    else:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
            for table, rows in data.items():
                zf.writestr(f"{table}.json", json.dumps(rows, indent=2, ensure_ascii=False, default=str))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", help="subject email (case-insensitive)")
    parser.add_argument("--phone", help="subject phone in E.164 (e.g. +966500000000)")
    parser.add_argument("--output", required=True, help="output zip path")
    parser.add_argument("--password", default=os.environ.get("DSAR_EXPORT_PASSWORD"),
                        help="ZIP encryption password (or env DSAR_EXPORT_PASSWORD)")
    parser.add_argument("--no-password", action="store_true",
                        help="produce an UNENCRYPTED zip (NOT recommended)")
    args = parser.parse_args()

    if not args.email and not args.phone:
        print("Either --email or --phone is required", file=sys.stderr)
        return 2

    if not args.no_password and not args.password:
        print("Refusing to produce an unencrypted DSAR export. "
              "Pass --password or DSAR_EXPORT_PASSWORD, or explicitly --no-password.",
              file=sys.stderr)
        return 2

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL is required", file=sys.stderr)
        return 2

    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("psycopg2 is required: pip install psycopg2-binary", file=sys.stderr)
        return 2

    conn = psycopg2.connect(normalize_db_url(db_url))
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    data = find_subject_rows(cur, args.email, args.phone)
    manifest = build_manifest(args.email, args.phone, data)
    cur.close()
    conn.close()

    make_zip(args.output, manifest, data,
             None if args.no_password else args.password)

    print(json.dumps({
        "output": args.output,
        "tables_found": list(data.keys()),
        "total_rows": manifest["total_rows"],
        "encrypted": not args.no_password,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
