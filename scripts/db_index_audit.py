#!/usr/bin/env python3
"""scripts/db_index_audit.py

Pre-launch DB performance audit. Connects to the configured DATABASE_URL,
identifies sequential scans on large tables, missing primary-key indexes, and
slow queries from pg_stat_statements.

Outputs JSON to stdout. Non-zero exit if any P1 issues are found.

Usage:
    DATABASE_URL=postgresql://... python scripts/db_index_audit.py
    DATABASE_URL=postgresql://... python scripts/db_index_audit.py --strict
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

P1_SEQ_SCAN_MIN_ROWS = 10_000
P1_SLOW_QUERY_MS = 500.0


def normalize_url(url: str) -> str:
    return re.sub(r"^postgresql\+asyncpg://", "postgresql://", url)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero if any P1 issues found")
    args = parser.parse_args()

    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL is required", file=sys.stderr)
        return 2

    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("psycopg2 is required: pip install psycopg2-binary", file=sys.stderr)
        return 2

    conn = psycopg2.connect(normalize_url(url))
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    report: dict[str, Any] = {"p1": [], "p2": [], "info": []}

    # 1. Tables with high seq scans
    cur.execute(
        """
        SELECT schemaname, relname AS table_name,
               seq_scan, seq_tup_read, idx_scan,
               n_live_tup
        FROM pg_stat_user_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
          AND n_live_tup > %s
          AND seq_scan > COALESCE(idx_scan, 0) * 2
        ORDER BY seq_tup_read DESC
        LIMIT 20;
        """,
        (P1_SEQ_SCAN_MIN_ROWS,),
    )
    for row in cur.fetchall():
        report["p1"].append({
            "kind": "high_seq_scan",
            "table": f"{row['schemaname']}.{row['table_name']}",
            "seq_scan": row["seq_scan"],
            "idx_scan": row["idx_scan"],
            "rows": row["n_live_tup"],
            "hint": f"Consider adding an index on a frequently-filtered column of {row['table_name']}.",
        })

    # 2. Missing primary keys (P1)
    cur.execute(
        """
        SELECT n.nspname AS schema, c.relname AS table_name
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        LEFT JOIN pg_constraint con ON con.conrelid = c.oid AND con.contype = 'p'
        WHERE c.relkind = 'r'
          AND n.nspname NOT IN ('pg_catalog', 'information_schema')
          AND con.oid IS NULL
        ORDER BY 1, 2;
        """
    )
    for row in cur.fetchall():
        report["p1"].append({
            "kind": "missing_primary_key",
            "table": f"{row['schema']}.{row['table_name']}",
        })

    # 3. Slow queries (if pg_stat_statements available — P2)
    try:
        cur.execute(
            """
            SELECT query, calls, mean_exec_time, total_exec_time
            FROM pg_stat_statements
            WHERE mean_exec_time > %s
            ORDER BY mean_exec_time DESC
            LIMIT 10;
            """,
            (P1_SLOW_QUERY_MS,),
        )
        for row in cur.fetchall():
            report["p2"].append({
                "kind": "slow_query",
                "mean_ms": round(row["mean_exec_time"], 2),
                "calls": row["calls"],
                "query": (row["query"] or "")[:200],
            })
    except psycopg2.Error:
        report["info"].append("pg_stat_statements not enabled — slow query report skipped")
        conn.rollback()

    cur.close()
    conn.close()

    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))

    if args.strict and report["p1"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
