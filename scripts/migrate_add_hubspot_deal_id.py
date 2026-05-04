#!/usr/bin/env python3
"""
Idempotent migration: add nullable `hubspot_deal_id` column to `deals`.

Why:
    Production Postgres is missing `deals.hubspot_deal_id` while the
    deploy-branch role-briefs query (and downstream WhatsApp brief)
    selects it. This produces 500s on `/api/v1/role-briefs/daily?role=sales_manager`
    and `/api/v1/whatsapp/brief?role=sales_manager`.

Safety:
    - Idempotent. Checks information_schema first.
    - Nullable. No backfill. No data drop. No table recreate.
    - Aborts on any unexpected error. Never silently ignores.
    - Works against Postgres (asyncpg) AND SQLite (aiosqlite).
    - Reads `DATABASE_URL` from env. Refuses to run if unset.

Usage:
    DATABASE_URL=postgres://... python scripts/migrate_add_hubspot_deal_id.py
    DATABASE_URL=sqlite+aiosqlite:////tmp/dealix_test.db python scripts/migrate_add_hubspot_deal_id.py

Exit codes:
    0   → MIGRATION_OK (column already present, or just added)
    2   → MIGRATION_FAIL (config/connection error)
    3   → MIGRATION_SKIPPED (deals table missing — bigger problem; do not auto-create here)
"""

from __future__ import annotations

import asyncio
import os
import sys


COLUMN_NAME = "hubspot_deal_id"
TABLE_NAME = "deals"


async def _async_main(url: str) -> int:
    # SQLAlchemy async engine — supports both Postgres and SQLite.
    try:
        from sqlalchemy import text
        from sqlalchemy.ext.asyncio import create_async_engine
    except Exception as e:  # noqa: BLE001
        print(f"MIGRATION_FAIL  sqlalchemy unavailable: {e}", file=sys.stderr)
        return 2

    engine = create_async_engine(url, echo=False)

    try:
        async with engine.connect() as conn:
            dialect = conn.dialect.name
            print(f"MIGRATION_INFO  dialect={dialect}")

            # 1. Confirm `deals` exists
            if dialect == "postgresql":
                table_check = await conn.execute(text(
                    "SELECT 1 FROM information_schema.tables "
                    "WHERE table_schema='public' AND table_name=:t"
                ), {"t": TABLE_NAME})
            elif dialect == "sqlite":
                table_check = await conn.execute(text(
                    "SELECT 1 FROM sqlite_master "
                    "WHERE type='table' AND name=:t"
                ), {"t": TABLE_NAME})
            else:
                print(f"MIGRATION_FAIL  unsupported dialect={dialect}", file=sys.stderr)
                return 2

            if table_check.first() is None:
                print(
                    f"MIGRATION_SKIPPED  table {TABLE_NAME!r} not present — "
                    "the model may not be initialized in this database. "
                    "Run app once with auto-create-tables enabled, then re-run.",
                    file=sys.stderr,
                )
                return 3

            # 2. Confirm column does NOT already exist
            if dialect == "postgresql":
                col_check = await conn.execute(text(
                    "SELECT 1 FROM information_schema.columns "
                    "WHERE table_schema='public' AND table_name=:t AND column_name=:c"
                ), {"t": TABLE_NAME, "c": COLUMN_NAME})
                exists = col_check.first() is not None
            else:
                pragma = await conn.execute(text(f"PRAGMA table_info({TABLE_NAME})"))
                cols = [row[1] for row in pragma.fetchall()]
                exists = COLUMN_NAME in cols

            if exists:
                print(f"MIGRATION_OK  column {COLUMN_NAME!r} already present")
                return 0

            # 3. Add the column (nullable, no default, no backfill)
            if dialect == "postgresql":
                ddl = f"ALTER TABLE {TABLE_NAME} ADD COLUMN IF NOT EXISTS {COLUMN_NAME} VARCHAR NULL"
            else:
                ddl = f"ALTER TABLE {TABLE_NAME} ADD COLUMN {COLUMN_NAME} VARCHAR NULL"

            await conn.execute(text(ddl))
            await conn.commit()
            print(f"MIGRATION_OK  added {TABLE_NAME}.{COLUMN_NAME} (nullable)")
            return 0
    finally:
        await engine.dispose()


def _coerce_async_url(url: str) -> str:
    """Coerce common sync URL forms to their async-driver equivalents."""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://") and "+asyncpg" not in url:
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("sqlite://") and "aiosqlite" not in url:
        url = url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url


async def run_migration_if_needed(url: str | None = None) -> int:
    """Importable wrapper for the FastAPI startup hook.

    Returns the same exit codes as the CLI:
        0 = MIGRATION_OK (column already present, or just added)
        2 = MIGRATION_FAIL (config/connection error)
        3 = MIGRATION_SKIPPED (deals table missing)

    Never raises. Caller (api.main lifespan) must log + ignore non-zero
    so a migration hiccup never blocks app startup.
    """
    src = (url or os.getenv("DATABASE_URL", "")).strip()
    if not src:
        return 2
    try:
        return await _async_main(_coerce_async_url(src))
    except Exception as exc:  # noqa: BLE001 — startup hook must NEVER raise
        print(f"MIGRATION_FAIL  unexpected: {exc}", file=sys.stderr)
        return 2


def main() -> int:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        print("MIGRATION_FAIL  DATABASE_URL not set", file=sys.stderr)
        return 2
    return asyncio.run(_async_main(_coerce_async_url(url)))


if __name__ == "__main__":
    raise SystemExit(main())
