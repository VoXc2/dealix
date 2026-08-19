"""Fail closed if an existing database cannot store Dealix Alembic revisions.

This is a read-only preflight. It never changes schema. Dealix has revision
identifiers longer than Alembic's default VARCHAR(32) version table, so running
`alembic upgrade` against an older database can otherwise fail only after a
migration has begun.
"""

from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine


@dataclass(frozen=True)
class CapacityResult:
    ok: bool
    required: int
    actual: int | None
    reason: str


def _database_url() -> str:
    """Normalize PostgreSQL provider URLs to SQLAlchemy's asyncpg form."""
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is required")
    if url.startswith("postgres://"):
        url = "postgresql+asyncpg://" + url.removeprefix("postgres://")
    elif url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url.removeprefix("postgresql://")
    elif url.startswith("postgresql+psycopg://"):
        url = "postgresql+asyncpg://" + url.removeprefix("postgresql+psycopg://")
    if not url.startswith("postgresql+asyncpg://"):
        raise RuntimeError("Alembic version-capacity preflight supports PostgreSQL only")
    return url


def required_revision_capacity() -> int:
    config = Config(str(REPO_ROOT / "alembic.ini"))
    script = ScriptDirectory.from_config(config)
    revisions = [revision.revision for revision in script.walk_revisions()]
    if not revisions:
        raise RuntimeError("no Alembic revisions found")
    return max(len(revision) for revision in revisions)


def _inspect_capacity_sync(connection, required: int) -> CapacityResult:
    inspector = inspect(connection)
    if "alembic_version" not in inspector.get_table_names():
        return CapacityResult(False, required, None, "alembic_version table is absent; use guarded fresh bootstrap for a brand-new database")
    columns = {column["name"]: column for column in inspector.get_columns("alembic_version")}
    version_column = columns.get("version_num")
    if version_column is None:
        return CapacityResult(False, required, None, "alembic_version.version_num is missing")
    actual = getattr(version_column["type"], "length", None)
    if actual is None:
        return CapacityResult(True, required, None, "unbounded version_num")
    if int(actual) >= required:
        return CapacityResult(True, required, int(actual), "capacity sufficient")
    return CapacityResult(False, required, int(actual), "version_num is too narrow for this checkout; run the separately approval-gated widening tool before alembic upgrade")


async def check_capacity() -> CapacityResult:
    required = required_revision_capacity()
    engine = create_async_engine(_database_url(), pool_pre_ping=True)
    try:
        async with engine.connect() as connection:
            return await connection.run_sync(_inspect_capacity_sync, required)
    finally:
        await engine.dispose()


def main() -> int:
    result = asyncio.run(check_capacity())
    actual = "unbounded" if result.actual is None and result.ok else str(result.actual)
    status = "PASS" if result.ok else "FAIL"
    print(f"ALEMBIC_VERSION_CAPACITY={status} required={result.required} actual={actual} reason={result.reason}")
    if not result.ok:
        print("Remediation: review and, only with production-change approval, run scripts/ops/widen_alembic_version_capacity.py with its explicit guards.", file=sys.stderr)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
