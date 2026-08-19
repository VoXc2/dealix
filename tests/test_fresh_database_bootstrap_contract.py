"""Safety contracts for the #1077 fresh-database bootstrap."""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import uuid
from pathlib import Path

import asyncpg
import pytest
from sqlalchemy import ForeignKeyConstraint, Integer, MetaData, Table
from sqlalchemy.engine import make_url
from sqlalchemy.sql.schema import Column

from auto_client_acquisition.proof_ledger.postgres_backend import ProofLedgerBase
from db.fresh_schema import (
    FreshSchemaCaptureError,
    FreshSchemaReport,
    _MigrationMetadataCapture,
    build_fresh_schema_metadata,
)
from db.model_registry import load_all_models
from db.models import Base
from scripts.ops.bootstrap_fresh_database import ACK_ENV, _database_url

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = (ROOT / "db" / "model_registry.py").read_text(encoding="utf-8")
FRESH_SCHEMA = (ROOT / "db" / "fresh_schema.py").read_text(encoding="utf-8")
ENV = (ROOT / "db" / "migrations" / "env.py").read_text(encoding="utf-8")
SESSION = (ROOT / "db" / "session.py").read_text(encoding="utf-8")
BOOTSTRAP = (ROOT / "scripts" / "ops" / "bootstrap_fresh_database.py").read_text(
    encoding="utf-8"
)
ROOT_0001 = (
    ROOT / "db" / "migrations" / "versions" / "0001_uuid_softdelete_indexes.py"
).read_text(encoding="utf-8")
ROOT_001 = (
    ROOT / "db" / "migrations" / "versions" / "20240101_001_auth_schema.py"
).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def fresh_schema_contract() -> tuple[MetaData, FreshSchemaReport]:
    return build_fresh_schema_metadata()


def _server_default_signature(column: Column[object]) -> str | None:
    if column.server_default is None:
        return None
    return str(column.server_default.arg)


def _assert_table_contract(source: Table, captured: Table, table_name: str) -> None:
    assert list(captured.c.keys()) == list(source.c.keys()), table_name
    for column_name in source.c.keys():
        source_column = source.c[column_name]
        captured_column = captured.c[column_name]
        assert type(captured_column.type) is type(source_column.type), (
            table_name,
            column_name,
        )
        assert str(captured_column.type) == str(source_column.type), (
            table_name,
            column_name,
        )
        assert captured_column.nullable == source_column.nullable, (
            table_name,
            column_name,
        )
        assert _server_default_signature(captured_column) == _server_default_signature(
            source_column
        ), (table_name, column_name)


def _foreign_key_for_local_column(table: Table, local_column: str) -> ForeignKeyConstraint:
    matches = [
        constraint
        for constraint in table.constraints
        if isinstance(constraint, ForeignKeyConstraint)
        and tuple(constraint.column_keys) == (local_column,)
    ]
    assert len(matches) == 1, (table.name, local_column, matches)
    return matches[0]


def _postgres_dsn(database: str) -> str:
    url = make_url(_database_url()).set(drivername="postgresql", database=database)
    return url.render_as_string(hide_password=False)


def _require_disposable_postgres() -> str:
    if os.getenv(ACK_ENV, "").strip() != "1":
        pytest.skip("dedicated fresh-PostgreSQL proof only")
    raw_database_url = os.getenv("DATABASE_URL", "").strip()
    if not raw_database_url.startswith(
        (
            "postgres://",
            "postgresql://",
            "postgresql+asyncpg://",
            "postgresql+psycopg://",
        )
    ):
        pytest.skip("PostgreSQL DATABASE_URL required")
    return raw_database_url


def _run_bootstrap_cli(database: str) -> subprocess.CompletedProcess[str]:
    target_async_url = make_url(_database_url()).set(database=database).render_as_string(
        hide_password=False
    )
    env = os.environ.copy()
    env["DATABASE_URL"] = target_async_url
    env[ACK_ENV] = "1"
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "ops" / "bootstrap_fresh_database.py"),
            "--confirm-empty-bootstrap",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _assert_bootstrap_rejects_database_object(
    *,
    setup_sql: str,
    expected_label: str,
    cleanup_sql: str | tuple[str, ...] | None = None,
) -> None:
    _require_disposable_postgres()
    target_database = f"dealix_occupancy_{uuid.uuid4().hex[:12]}"
    admin_dsn = _postgres_dsn("postgres")
    target_dsn = _postgres_dsn(target_database)

    async def prepare() -> None:
        admin = await asyncpg.connect(admin_dsn)
        try:
            await admin.execute(f'DROP DATABASE IF EXISTS "{target_database}" WITH (FORCE)')
            await admin.execute(f'CREATE DATABASE "{target_database}"')
        finally:
            await admin.close()

        target = await asyncpg.connect(target_dsn)
        try:
            await target.execute(setup_sql)
        finally:
            await target.close()

    async def cleanup() -> None:
        cleanup_statements = (
            (cleanup_sql,) if isinstance(cleanup_sql, str) else cleanup_sql
        )
        if cleanup_statements:
            target = await asyncpg.connect(target_dsn)
            try:
                for statement in cleanup_statements:
                    await target.execute(statement)
            finally:
                await target.close()
        admin = await asyncpg.connect(admin_dsn)
        try:
            await admin.execute(f'DROP DATABASE IF EXISTS "{target_database}" WITH (FORCE)')
        finally:
            await admin.close()

    asyncio.run(prepare())
    try:
        result = _run_bootstrap_cli(target_database)
        combined = result.stdout + "\n" + result.stderr
        assert result.returncode != 0, combined
        assert "refusing fresh bootstrap on non-empty database" in combined
        assert expected_label in combined
    finally:
        asyncio.run(cleanup())


def test_model_registry_covers_every_side_effect_db_model_module() -> None:
    for module in (
        "db.models_revenue_events",
        "db.models_company_targeting",
        "db.models_commercial_intelligence",
        "db.models_erp",
        "db.models_subscription",
    ):
        assert f'"{module}"' in REGISTRY
    assert "def load_all_models" in REGISTRY


def test_alembic_and_dev_schema_creation_share_one_registry_path() -> None:
    assert "from db.model_registry import load_all_models" in SESSION
    assert "load_all_models()" in SESSION
    assert "from db.model_registry import load_all_models" in FRESH_SCHEMA
    assert "load_all_models()" in FRESH_SCHEMA
    assert (
        "from auto_client_acquisition.proof_ledger.postgres_backend import ProofLedgerBase"
        in FRESH_SCHEMA
    )
    assert "ProofLedgerBase.metadata.sorted_tables" in FRESH_SCHEMA
    assert "from db.fresh_schema import build_fresh_schema_metadata" in ENV
    assert "target_metadata, _fresh_schema_report = build_fresh_schema_metadata()" in ENV


def test_bootstrap_is_empty_database_only_and_double_confirmed() -> None:
    assert 'ACK_ENV = "DEALIX_ALLOW_FRESH_DB_BOOTSTRAP"' in BOOTSTRAP
    assert "--confirm-empty-bootstrap" in BOOTSTRAP
    assert "refusing fresh bootstrap on non-empty database" in BOOTSTRAP
    assert "inspect(connection).get_table_names()" in BOOTSTRAP
    assert "build_fresh_schema_metadata()" in BOOTSTRAP
    assert "metadata.create_all(connection)" in BOOTSTRAP
    assert 'migration.stamp(script, "heads")' in BOOTSTRAP
    assert "pg_catalog.pg_publication" in BOOTSTRAP
    assert "pg_catalog.pg_subscription" in BOOTSTRAP
    assert "subconninfo" not in BOOTSTRAP


def test_bootstrap_proves_schema_and_alembic_heads_match() -> None:
    assert "compare_metadata(compare_context, metadata)" in BOOTSTRAP
    assert "current_heads != script_heads" in BOOTSTRAP
    assert "metadata tables missing after bootstrap" in BOOTSTRAP
    assert "migration-owned tables missing after bootstrap" in BOOTSTRAP


def test_fresh_schema_preserves_every_orm_owned_column_contract(
    fresh_schema_contract: tuple[MetaData, FreshSchemaReport],
) -> None:
    metadata, report = fresh_schema_contract
    load_all_models()
    assert report.ignored_orm_column_operations > 0

    for table_name in sorted(report.orm_owned_tables):
        _assert_table_contract(
            Base.metadata.tables[table_name],
            metadata.tables[table_name],
            table_name,
        )


def test_fresh_schema_preserves_compatible_migration_fk_actions(
    fresh_schema_contract: tuple[MetaData, FreshSchemaReport],
) -> None:
    metadata, report = fresh_schema_contract
    expected = {
        ("refresh_tokens", "user_id"): "CASCADE",
        ("user_invites", "tenant_id"): "CASCADE",
        ("payments", "tenant_id"): "SET NULL",
    }
    for (table_name, local_column), ondelete in expected.items():
        constraint = _foreign_key_for_local_column(
            metadata.tables[table_name],
            local_column,
        )
        assert constraint.ondelete == ondelete, (table_name, local_column)
        assert all(foreign_key.ondelete == ondelete for foreign_key in constraint.elements)

    assert report.preserved_foreign_key_actions >= len(expected)


def test_fresh_schema_preserves_dedicated_proof_ledger_contract(
    fresh_schema_contract: tuple[MetaData, FreshSchemaReport],
) -> None:
    metadata, report = fresh_schema_contract
    expected = {"proof_events", "proof_revenue_work_units"}
    assert set(ProofLedgerBase.metadata.tables) == expected
    assert report.dedicated_orm_owned_tables == expected
    assert expected <= report.authoritative_tables
    assert expected <= set(metadata.tables)
    assert "proof_events" not in report.migration_only_tables

    for table_name in sorted(expected):
        _assert_table_contract(
            ProofLedgerBase.metadata.tables[table_name],
            metadata.tables[table_name],
            table_name,
        )

    proof_columns = set(metadata.tables["proof_events"].c.keys())
    assert {"id", "summary_ar", "summary_en", "payload_json", "created_at"} <= proof_columns
    assert "event_id" not in proof_columns
    assert "claim" not in proof_columns


def test_fresh_schema_materializes_migration_owned_runtime_tables(
    fresh_schema_contract: tuple[MetaData, FreshSchemaReport],
) -> None:
    metadata, report = fresh_schema_contract
    table_names = set(metadata.tables)
    required_runtime_tables = {
        "proof_events",
        "proof_revenue_work_units",
        "workflow_runs",
        "control_events",
        "approval_tickets",
        "agent_mesh_agents",
        "assurance_contracts",
        "runtime_safety_kill_switches",
        "value_metrics",
        "improvement_proposals",
    }
    migration_only_required = required_runtime_tables - report.dedicated_orm_owned_tables
    assert required_runtime_tables <= table_names
    assert migration_only_required <= report.migration_only_tables
    assert report.migration_created_tables <= table_names


def test_fresh_schema_keeps_migration_owned_indexes_on_orm_tables(
    fresh_schema_contract: tuple[MetaData, FreshSchemaReport],
) -> None:
    metadata, _ = fresh_schema_contract
    lead_indexes = {index.name for index in metadata.tables["leads"].indexes}
    assert "ix_leads_status_created" in lead_indexes
    assert "ix_leads_tenant_status" in lead_indexes


def test_fresh_schema_skips_stale_index_for_removed_orm_column() -> None:
    metadata = MetaData()
    Table("current_table", metadata, Column("id", Integer, primary_key=True))
    report = FreshSchemaReport(orm_owned_tables={"current_table"})
    capture = _MigrationMetadataCapture(metadata, report)

    result = capture.create_index(
        "ix_current_table_deleted_at",
        "current_table",
        ["deleted_at"],
    )

    assert result is None
    assert report.ignored_orm_column_operations == 1
    assert "ix_current_table_deleted_at" not in {
        index.name for index in metadata.tables["current_table"].indexes
    }


def test_fresh_schema_rejects_missing_index_column_on_migration_owned_table() -> None:
    metadata = MetaData()
    Table("migration_table", metadata, Column("id", Integer, primary_key=True))
    capture = _MigrationMetadataCapture(metadata, FreshSchemaReport())

    with pytest.raises(
        FreshSchemaCaptureError,
        match=(
            "index ix_migration_table_deleted_at references missing column "
            "migration_table.deleted_at"
        ),
    ):
        capture.create_index(
            "ix_migration_table_deleted_at",
            "migration_table",
            ["deleted_at"],
        )


def test_unknown_alembic_operation_uses_attribute_protocol() -> None:
    capture = _MigrationMetadataCapture(MetaData(), FreshSchemaReport())

    with pytest.raises(
        AttributeError,
        match="unsupported Alembic operation in fresh-schema capture: op.unsupported_op",
    ):
        _ = capture.unsupported_op


def test_fresh_schema_never_replays_historical_data_seeds(
    fresh_schema_contract: tuple[MetaData, FreshSchemaReport],
) -> None:
    _, report = fresh_schema_contract
    assert report.ignored_data_statements >= 1
    assert report.required_extensions == {"pgcrypto"}
    assert "bulk_insert" in FRESH_SCHEMA
    assert "unsupported raw migration SQL" in FRESH_SCHEMA


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "postgres://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
        (
            "postgresql://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
        (
            "postgresql+psycopg://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
        (
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
            "postgresql+asyncpg://user:pass@example.invalid:5432/dealix",
        ),
    ],
)
def test_fresh_bootstrap_accepts_supported_postgres_provider_urls(
    monkeypatch: pytest.MonkeyPatch,
    raw: str,
    expected: str,
) -> None:
    monkeypatch.setenv("DATABASE_URL", raw)
    assert _database_url() == expected


def test_fresh_bootstrap_rejects_preexisting_publication() -> None:
    _assert_bootstrap_rejects_database_object(
        setup_sql="CREATE PUBLICATION bootstrap_guard_publication FOR ALL TABLES",
        expected_label="bootstrap_guard_publication:publication:all_tables",
    )


def test_fresh_bootstrap_rejects_preexisting_subscription() -> None:
    _assert_bootstrap_rejects_database_object(
        setup_sql=(
            "CREATE SUBSCRIPTION bootstrap_guard_subscription "
            "CONNECTION 'host=127.0.0.1 port=1 dbname=postgres user=dealix_test' "
            "PUBLICATION bootstrap_guard_publication WITH (connect = false)"
        ),
        expected_label="bootstrap_guard_subscription:subscription",
        cleanup_sql=(
            "ALTER SUBSCRIPTION bootstrap_guard_subscription DISABLE",
            "ALTER SUBSCRIPTION bootstrap_guard_subscription SET (slot_name = NONE)",
            "DROP SUBSCRIPTION IF EXISTS bootstrap_guard_subscription",
        ),
    )


def test_fresh_bootstrap_accepts_preinstalled_allowlisted_pgcrypto() -> None:
    """Prove the managed-provider case on disposable PostgreSQL.

    This test intentionally runs only in the dedicated #1077 PostgreSQL proof,
    where the acknowledgement flag is present and the service user can create a
    disposable database. It installs pgcrypto before Dealix touches the target,
    then requires the real bootstrap CLI to finish successfully.
    """
    _require_disposable_postgres()

    target_database = f"dealix_pgcrypto_{uuid.uuid4().hex[:12]}"
    admin_dsn = _postgres_dsn("postgres")
    target_dsn = _postgres_dsn(target_database)

    async def prepare() -> None:
        admin = await asyncpg.connect(admin_dsn)
        try:
            await admin.execute(f'DROP DATABASE IF EXISTS "{target_database}" WITH (FORCE)')
            await admin.execute(f'CREATE DATABASE "{target_database}"')
        finally:
            await admin.close()

        target = await asyncpg.connect(target_dsn)
        try:
            await target.execute("CREATE EXTENSION pgcrypto")
            installed = await target.fetchval(
                "SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pgcrypto')"
            )
            assert installed is True
        finally:
            await target.close()

    async def cleanup() -> None:
        admin = await asyncpg.connect(admin_dsn)
        try:
            await admin.execute(f'DROP DATABASE IF EXISTS "{target_database}" WITH (FORCE)')
        finally:
            await admin.close()

    asyncio.run(prepare())
    try:
        result = _run_bootstrap_cli(target_database)
        assert result.returncode == 0, result.stdout + "\n" + result.stderr
        assert "FRESH_DB_BOOTSTRAP=PASS" in result.stdout
        assert "commercial_seed=none" in result.stdout
    finally:
        asyncio.run(cleanup())


def test_bootstrap_does_not_seed_stale_commercial_pricing() -> None:
    assert "commercial_seed=none" in BOOTSTRAP
    for stale_price in ("199", "599", "1499", "plan_starter", "plan_growth"):
        assert stale_price not in BOOTSTRAP


def test_alembic_compares_the_complete_combined_contract() -> None:
    assert "build_fresh_schema_metadata" in ENV
    assert "target_metadata, _fresh_schema_report" in ENV
    assert "include_object" not in ENV
    assert "target_metadata=target_metadata" in ENV


def test_historical_roots_are_not_fresh_database_baselines() -> None:
    assert 'revision: str = "0001"' in ROOT_0001
    assert "down_revision: str | None = None" in ROOT_0001
    assert "op.add_column(" in ROOT_0001
    assert '"agent_runs"' in ROOT_0001

    assert 'revision: str = "001"' in ROOT_001
    assert "down_revision: Union[str, None] = None" in ROOT_001
    assert "op.alter_column(" in ROOT_001
    assert '"users"' in ROOT_001
