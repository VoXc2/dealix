"""Widen an existing PostgreSQL Alembic version column after explicit approval.

This tool is intentionally never called automatically. It performs DDL and is
therefore guarded by both an environment acknowledgement and a CLI flag. The
Railway predeploy path only runs the read-only checker and fails closed.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine

from scripts.ops.check_alembic_version_capacity import (
    _database_url,
    required_revision_capacity,
)

ACK_ENV = "DEALIX_ALLOW_ALEMBIC_VERSION_WIDEN"
TARGET_CAPACITY = 255


def _widen_sync(connection, required: int) -> tuple[int | None, int | None, bool]:
    inspector = inspect(connection)
    if "alembic_version" not in inspector.get_table_names():
        raise RuntimeError("refusing widen: alembic_version table is absent")

    columns = {column["name"]: column for column in inspector.get_columns("alembic_version")}
    version_column = columns.get("version_num")
    if version_column is None:
        raise RuntimeError("refusing widen: alembic_version.version_num is absent")

    before = getattr(version_column["type"], "length", None)
    if before is None:
        return None, None, False
    if int(before) >= required:
        return int(before), int(before), False

    target = max(TARGET_CAPACITY, required)
    connection.execute(
        text(
            "ALTER TABLE alembic_version "
            f"ALTER COLUMN version_num TYPE VARCHAR({target})"
        )
    )

    after_columns = {
        column["name"]: column
        for column in inspect(connection).get_columns("alembic_version")
    }
    after = getattr(after_columns["version_num"]["type"], "length", None)
    if after is not None and int(after) < required:
        raise RuntimeError(
            f"version_num widening verification failed: required={required} actual={after}"
        )
    return int(before), None if after is None else int(after), True


async def widen() -> tuple[int | None, int | None, bool, int]:
    required = required_revision_capacity()
    engine = create_async_engine(_database_url(), pool_pre_ping=True)
    try:
        async with engine.begin() as connection:
            before, after, changed = await connection.run_sync(_widen_sync, required)
            return before, after, changed, required
    finally:
        await engine.dispose()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--confirm-existing-db-ddl",
        action="store_true",
        help="Acknowledge that this command alters an existing database table.",
    )
    args = parser.parse_args()

    if not args.confirm_existing_db_ddl:
        raise SystemExit("refusing DDL without --confirm-existing-db-ddl")
    if os.getenv(ACK_ENV, "").strip() != "1":
        raise SystemExit(f"refusing DDL unless {ACK_ENV}=1")

    before, after, changed, required = asyncio.run(widen())
    print(
        "ALEMBIC_VERSION_WIDEN=PASS "
        f"required={required} before={before} after={after} changed={str(changed).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
