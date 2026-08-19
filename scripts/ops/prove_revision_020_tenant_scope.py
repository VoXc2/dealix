"""Disposable PostgreSQL proof for tenant-scope revision 020.

The proof operates only on the database URL supplied by CI. It creates a small
representative pre-revision schema, inserts legacy rows, applies the revision
through Alembic Operations, and verifies upgrade, downgrade, and re-upgrade
semantics. An explicit ephemeral guard prevents accidental use as a production
migration command.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.exc import IntegrityError

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REVISION_PATH = (
    ROOT
    / "db"
    / "migrations"
    / "versions"
    / "20260812_020_tenant_scope_conversations_tasks.py"
)
EPHEMERAL_GUARD = "DEALIX_REVISION_020_PROOF_EPHEMERAL"


def _database_url() -> str:
    url = os.getenv("PROOF_DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("PROOF_DATABASE_URL is required")
    if not url.startswith(("postgresql://", "postgresql+psycopg://")):
        raise RuntimeError("revision 020 proof supports disposable PostgreSQL only")
    return url


def _load_revision() -> Any:
    spec = importlib.util.spec_from_file_location("dealix_revision_020", REVISION_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load migration: {REVISION_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if module.revision != "20260812_020_tenant_scope_conversations_tasks":
        raise RuntimeError(f"unexpected revision loaded: {module.revision}")
    return module


def _bind_revision(module: Any, connection: sa.Connection) -> None:
    module.op = Operations(MigrationContext.configure(connection))


def _base_metadata() -> sa.MetaData:
    metadata = sa.MetaData()
    sa.Table(
        "tenants",
        metadata,
        sa.Column("id", sa.String(64), primary_key=True),
    )
    sa.Table(
        "conversations",
        metadata,
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    sa.Table(
        "tasks",
        metadata,
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("status", sa.String(32), nullable=True),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
    )
    return metadata


def _index_map(inspector: sa.Inspector, table: str) -> dict[str, dict[str, Any]]:
    return {
        str(index["name"]): index
        for index in inspector.get_indexes(table)
        if index.get("name")
    }


def _fk_map(inspector: sa.Inspector, table: str) -> dict[str, dict[str, Any]]:
    return {
        str(foreign_key["name"]): foreign_key
        for foreign_key in inspector.get_foreign_keys(table)
        if foreign_key.get("name")
    }


def _assert_upgraded(connection: sa.Connection) -> None:
    inspector = sa.inspect(connection)
    for table in ("conversations", "tasks"):
        columns = {column["name"]: column for column in inspector.get_columns(table)}
        tenant_column = columns.get("tenant_id")
        if tenant_column is None:
            raise AssertionError(f"{table}.tenant_id missing after upgrade")
        if tenant_column["nullable"] is not True:
            raise AssertionError(
                f"{table}.tenant_id must remain nullable pending governed backfill"
            )
        if getattr(tenant_column["type"], "length", None) != 64:
            raise AssertionError(f"{table}.tenant_id must be VARCHAR(64)")

    conversation_fk = _fk_map(inspector, "conversations").get(
        "fk_conversations_tenant_id_tenants"
    )
    task_fk = _fk_map(inspector, "tasks").get("fk_tasks_tenant_id_tenants")
    for table, foreign_key in (
        ("conversations", conversation_fk),
        ("tasks", task_fk),
    ):
        if foreign_key is None:
            raise AssertionError(f"{table} tenant foreign key missing")
        if foreign_key["referred_table"] != "tenants":
            raise AssertionError(f"{table} tenant foreign key targets wrong table")
        if foreign_key["constrained_columns"] != ["tenant_id"]:
            raise AssertionError(f"{table} tenant foreign key targets wrong column")
        if (foreign_key.get("options") or {}).get("ondelete") != "CASCADE":
            raise AssertionError(f"{table} tenant foreign key must cascade on delete")

    conversation_index = _index_map(inspector, "conversations").get(
        "ix_conversations_tenant_created"
    )
    task_index = _index_map(inspector, "tasks").get(
        "ix_tasks_tenant_status_due"
    )
    if not conversation_index or conversation_index["column_names"] != [
        "tenant_id",
        "created_at",
    ]:
        raise AssertionError("conversation tenant chronology index is incorrect")
    if not task_index or task_index["column_names"] != [
        "tenant_id",
        "status",
        "due_at",
    ]:
        raise AssertionError("task tenant status/due index is incorrect")


def _assert_downgraded(connection: sa.Connection) -> None:
    inspector = sa.inspect(connection)
    for table in ("conversations", "tasks"):
        columns = {column["name"] for column in inspector.get_columns(table)}
        if "tenant_id" in columns:
            raise AssertionError(f"{table}.tenant_id remains after downgrade")
    if "ix_conversations_tenant_created" in _index_map(inspector, "conversations"):
        raise AssertionError("conversation tenant index remains after downgrade")
    if "ix_tasks_tenant_status_due" in _index_map(inspector, "tasks"):
        raise AssertionError("task tenant index remains after downgrade")


def _seed_legacy_rows(connection: sa.Connection) -> None:
    connection.execute(
        sa.text("INSERT INTO tenants (id) VALUES ('tenant-a'), ('tenant-b')")
    )
    connection.execute(
        sa.text(
            "INSERT INTO conversations (id, created_at) "
            "VALUES ('legacy-conversation', now())"
        )
    )
    connection.execute(
        sa.text(
            "INSERT INTO tasks (id, status, due_at) "
            "VALUES ('legacy-task', 'pending', now())"
        )
    )


def _assert_legacy_rows_preserved(connection: sa.Connection) -> None:
    conversation = connection.execute(
        sa.text(
            "SELECT tenant_id FROM conversations "
            "WHERE id = 'legacy-conversation'"
        )
    ).scalar_one()
    task = connection.execute(
        sa.text("SELECT tenant_id FROM tasks WHERE id = 'legacy-task'")
    ).scalar_one()
    if conversation is not None or task is not None:
        raise AssertionError("legacy rows must remain unassigned after upgrade")


def _assert_valid_tenant_writes(connection: sa.Connection) -> None:
    connection.execute(
        sa.text(
            "INSERT INTO conversations (id, created_at, tenant_id) "
            "VALUES ('tenant-conversation', now(), 'tenant-a')"
        )
    )
    connection.execute(
        sa.text(
            "INSERT INTO tasks (id, status, due_at, tenant_id) "
            "VALUES ('tenant-task', 'pending', now(), 'tenant-a')"
        )
    )


def _assert_invalid_tenant_rejected(engine: sa.Engine) -> None:
    try:
        with engine.begin() as connection:
            connection.execute(
                sa.text(
                    "INSERT INTO conversations (id, created_at, tenant_id) "
                    "VALUES ('invalid-tenant-conversation', now(), 'missing-tenant')"
                )
            )
    except IntegrityError:
        return
    raise AssertionError("tenant foreign key accepted an unknown tenant")


def _assert_tenant_delete_cascades(connection: sa.Connection) -> None:
    connection.execute(sa.text("DELETE FROM tenants WHERE id = 'tenant-a'"))
    conversation_count = connection.execute(
        sa.text("SELECT count(*) FROM conversations WHERE id = 'tenant-conversation'")
    ).scalar_one()
    task_count = connection.execute(
        sa.text("SELECT count(*) FROM tasks WHERE id = 'tenant-task'")
    ).scalar_one()
    if conversation_count != 0 or task_count != 0:
        raise AssertionError("tenant delete did not cascade to owned records")


def run_proof() -> None:
    if os.getenv(EPHEMERAL_GUARD) != "1":
        raise RuntimeError(f"refusing proof unless {EPHEMERAL_GUARD}=1")

    engine = sa.create_engine(_database_url())
    metadata = _base_metadata()
    revision = _load_revision()
    try:
        metadata.drop_all(engine)
        metadata.create_all(engine)
        with engine.begin() as connection:
            _seed_legacy_rows(connection)
            _bind_revision(revision, connection)
            revision.upgrade()
            _assert_upgraded(connection)
            _assert_legacy_rows_preserved(connection)
            _assert_valid_tenant_writes(connection)
        _assert_invalid_tenant_rejected(engine)
        with engine.begin() as connection:
            _assert_tenant_delete_cascades(connection)
            _bind_revision(revision, connection)
            revision.downgrade()
            _assert_downgraded(connection)
            if connection.execute(
                sa.text(
                    "SELECT count(*) FROM conversations "
                    "WHERE id = 'legacy-conversation'"
                )
            ).scalar_one() != 1:
                raise AssertionError("legacy conversation was lost during downgrade")
            if connection.execute(
                sa.text("SELECT count(*) FROM tasks WHERE id = 'legacy-task'")
            ).scalar_one() != 1:
                raise AssertionError("legacy task was lost during downgrade")
        with engine.begin() as connection:
            _bind_revision(revision, connection)
            revision.upgrade()
            _assert_upgraded(connection)
            _assert_legacy_rows_preserved(connection)
    finally:
        metadata.drop_all(engine)
        engine.dispose()


def main() -> int:
    run_proof()
    print("P0_1070_REVISION_020_UPGRADE=PASS")
    print("P0_1070_REVISION_020_LEGACY_ROWS=PASS")
    print("P0_1070_REVISION_020_FOREIGN_KEY=PASS")
    print("P0_1070_REVISION_020_CASCADE=PASS")
    print("P0_1070_REVISION_020_DOWNGRADE=PASS")
    print("P0_1070_REVISION_020_REUPGRADE=PASS")
    print("P0_1070_POSTGRES_MIGRATION_PROOF=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
