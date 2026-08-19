"""Bootstrap a brand-new Dealix PostgreSQL database from canonical contracts.

This is intentionally not a repair tool for existing databases. Historical
Alembic roots predate a formal baseline and begin with ALTER operations, so a
clean database cannot traverse them. For a genuinely empty database we build a
complete metadata snapshot from the current ORM plus migration-owned tables,
create that schema without replaying historical commercial/customer DML, add
only the runtime-required empty structural snapshot rows, and stamp the
checkout's Alembic heads. Future upgrades then use normal migrations.

Safety invariants:
- refuses any non-empty database, including user schemas and non-table objects;
- rejects pre-existing logical-replication publications/subscriptions;
- rejects pre-existing PostgreSQL large objects;
- normalizes managed-provider ``sslmode`` URLs for SQLAlchemy asyncpg safely;
- requires an explicit operator acknowledgement environment flag + CLI flag;
- never seeds customers, tenants, users, plans, prices, or commercial claims;
- seeds only the empty snapshot rows required for first-write locking semantics;
- fails closed on unsupported historical schema operations;
- never runs automatically at application startup.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import Column, MetaData, String, Table, inspect, text
from sqlalchemy.ext.asyncio import create_async_engine

from db.fresh_schema import build_fresh_schema_metadata

ACK_ENV = "DEALIX_ALLOW_FRESH_DB_BOOTSTRAP"
ALEMBIC_VERSION_LENGTH = 255
_ALLOWED_EXTENSIONS = frozenset({"pgcrypto"})
_ALLOWED_SSL_MODES = frozenset(
    {"disable", "allow", "prefer", "require", "verify-ca", "verify-full"}
)


def _database_connection_settings() -> tuple[str, dict[str, str]]:
    """Normalize a managed PostgreSQL URL and asyncpg connection arguments.

    SQLAlchemy's asyncpg dialect forwards URL query keys as keyword arguments
    to ``asyncpg.connect``. ``sslmode`` is valid inside a libpq-style asyncpg
    DSN, but the direct keyword argument is named ``ssl``. Convert only that
    well-defined option and preserve unrelated query parameters verbatim.
    """
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
        raise RuntimeError("fresh bootstrap supports PostgreSQL asyncpg URLs only")

    parsed = urlsplit(url)
    kept_query: list[tuple[str, str]] = []
    ssl_mode: str | None = None
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if key not in {"sslmode", "ssl"}:
            kept_query.append((key, value))
            continue
        if ssl_mode is not None and ssl_mode != value:
            raise RuntimeError("DATABASE_URL contains conflicting ssl/sslmode values")
        ssl_mode = value

    connect_args: dict[str, str] = {}
    if ssl_mode is not None:
        if ssl_mode not in _ALLOWED_SSL_MODES:
            raise RuntimeError(
                "fresh bootstrap received unsupported sslmode: " + ssl_mode
            )
        connect_args["ssl"] = ssl_mode

    normalized = urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(kept_query, doseq=True),
            parsed.fragment,
        )
    )
    return normalized, connect_args


def _database_url() -> str:
    """Return the normalized SQLAlchemy asyncpg URL without DSN-only sslmode."""
    return _database_connection_settings()[0]


def _database_connect_args() -> dict[str, str]:
    """Return explicit asyncpg keyword arguments derived from the database URL."""
    return _database_connection_settings()[1]


def _script_directory() -> ScriptDirectory:
    config_path = REPO_ROOT / "alembic.ini"
    if not config_path.exists():
        raise RuntimeError("alembic.ini not found in repository root")
    return ScriptDirectory.from_config(Config(str(config_path)))


def _ensure_extensions(connection, extensions: set[str]) -> None:
    unsupported = extensions - set(_ALLOWED_EXTENSIONS)
    if unsupported:
        raise RuntimeError(
            "fresh bootstrap refuses unsupported extensions: "
            + ", ".join(sorted(unsupported))
        )
    if "pgcrypto" in extensions:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))


def _ensure_wide_alembic_version_table(connection) -> None:
    """Create Alembic's version table with room for Dealix revision IDs."""
    metadata = MetaData()
    Table(
        "alembic_version",
        metadata,
        Column(
            "version_num",
            String(ALEMBIC_VERSION_LENGTH),
            primary_key=True,
            nullable=False,
        ),
    ).create(connection, checkfirst=True)


def _is_user_namespace_sql(alias: str) -> str:
    """Return the literal PostgreSQL namespace predicate used by guard queries."""
    return (
        f"{alias}.nspname NOT IN ('pg_catalog', 'information_schema') "
        f"AND LEFT({alias}.nspname, 8) NOT IN ('pg_toast', 'pg_temp_')"
    )


def _allowed_extension_routine_oids(connection) -> set[int]:
    """Return routine OIDs owned by explicitly allowlisted PostgreSQL extensions.

    Managed PostgreSQL providers may preinstall an extension such as ``pgcrypto``
    before Dealix receives the database. Its functions then live in ``public``,
    but they are not user application occupancy. We trust catalog ownership only:
    an object is exempted here only when PostgreSQL records it as an extension
    member through ``pg_depend``/``pg_extension`` and that extension is already in
    Dealix's explicit allowlist. Function names are never used as an exemption.
    """
    rows = connection.execute(
        text(
            """
            SELECT e.extname, d.objid
            FROM pg_catalog.pg_depend AS d
            JOIN pg_catalog.pg_extension AS e ON e.oid = d.refobjid
            WHERE d.classid = 'pg_proc'::regclass
              AND d.refclassid = 'pg_extension'::regclass
              AND d.deptype = 'e'
            """
        )
    ).all()
    return {
        int(objid)
        for extension_name, objid in rows
        if str(extension_name) in _ALLOWED_EXTENSIONS
    }


def _database_occupancy(connection) -> list[str]:
    """Return user-owned PostgreSQL objects that make a DB non-empty.

    A table-only inspection is insufficient: a used database may contain only a
    view, function, procedure, enum, domain, range, composite type, collation,
    logical-replication publication/subscription, large object, or objects in a
    non-default schema. Fresh bootstrap is deliberately conservative and rejects
    all such occupancy before creating or stamping anything. A publication using
    ``FOR ALL TABLES`` is especially unsafe because tables created by bootstrap
    would become publishable immediately.

    PostgreSQL temporary/toast namespaces use literal ``pg_temp_`` and
    ``pg_toast`` prefixes. Prefix comparisons are literal; SQL LIKE is avoided so
    a user schema such as ``pgdata`` cannot be hidden by underscore wildcards.

    Routines that PostgreSQL itself records as members of an explicitly
    allowlisted extension are not treated as user occupancy. This allows managed
    providers to preinstall ``pgcrypto`` without weakening the guard for ordinary
    user-created functions or procedures.
    """
    custom_schemas = {
        str(value)
        for value in connection.execute(
            text(
                """
                SELECT nspname
                FROM pg_catalog.pg_namespace
                WHERE nspname NOT IN ('public', 'information_schema', 'pg_catalog')
                  AND LEFT(nspname, 8) NOT IN ('pg_toast', 'pg_temp_')
                ORDER BY nspname
                """
            )
        ).scalars()
    }
    relations = {
        str(value)
        for value in connection.execute(
            text(
                """
                SELECT n.nspname || '.' || c.relname || ':relation:' || c.relkind::text
                FROM pg_catalog.pg_class AS c
                JOIN pg_catalog.pg_namespace AS n ON n.oid = c.relnamespace
                WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
                  AND LEFT(n.nspname, 8) NOT IN ('pg_toast', 'pg_temp_')
                  AND c.relkind IN ('r', 'p', 'v', 'm', 'f', 'S', 'c')
                ORDER BY n.nspname, c.relname, c.relkind
                """
            )
        ).scalars()
    }
    allowed_extension_routine_oids = _allowed_extension_routine_oids(connection)
    routines = {
        str(label)
        for oid, label in connection.execute(
            text(
                """
                SELECT
                    p.oid,
                    n.nspname || '.' || p.proname || ':routine:' || p.prokind::text
                FROM pg_catalog.pg_proc AS p
                JOIN pg_catalog.pg_namespace AS n ON n.oid = p.pronamespace
                WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
                  AND LEFT(n.nspname, 8) NOT IN ('pg_toast', 'pg_temp_')
                ORDER BY n.nspname, p.proname, p.oid
                """
            )
        ).all()
        if int(oid) not in allowed_extension_routine_oids
    }
    standalone_types = {
        str(value)
        for value in connection.execute(
            text(
                """
                SELECT n.nspname || '.' || t.typname || ':type:' || t.typtype::text
                FROM pg_catalog.pg_type AS t
                JOIN pg_catalog.pg_namespace AS n ON n.oid = t.typnamespace
                WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
                  AND LEFT(n.nspname, 8) NOT IN ('pg_toast', 'pg_temp_')
                  AND t.typtype IN ('d', 'e', 'r', 'm')
                ORDER BY n.nspname, t.typname, t.oid
                """
            )
        ).scalars()
    }
    collations = {
        str(value)
        for value in connection.execute(
            text(
                """
                SELECT n.nspname || '.' || c.collname || chr(58) || 'collation'
                FROM pg_catalog.pg_collation AS c
                JOIN pg_catalog.pg_namespace AS n ON n.oid = c.collnamespace
                WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
                  AND LEFT(n.nspname, 8) NOT IN ('pg_toast', 'pg_temp_')
                ORDER BY n.nspname, c.collname, c.oid
                """
            )
        ).scalars()
    }
    publications = {
        f"{name!s}:publication:{'all_tables' if bool(all_tables) else 'explicit'}"
        for name, all_tables in connection.execute(
            text(
                """
                SELECT pubname, puballtables
                FROM pg_catalog.pg_publication
                ORDER BY pubname
                """
            )
        ).all()
    }
    subscriptions = {
        f"{name!s}:subscription"
        for name in connection.execute(
            text(
                """
                SELECT subname
                FROM pg_catalog.pg_subscription
                WHERE subdbid = (
                    SELECT oid
                    FROM pg_catalog.pg_database
                    WHERE datname = current_database()
                )
                ORDER BY subname
                """
            )
        ).scalars()
    }
    large_objects = {
        f"{oid!s}:large_object"
        for oid in connection.execute(
            text(
                """
                SELECT oid
                FROM pg_catalog.pg_largeobject_metadata
                ORDER BY oid
                """
            )
        ).scalars()
    }
    return sorted(
        custom_schemas
        | relations
        | routines
        | standalone_types
        | collations
        | publications
        | subscriptions
        | large_objects
    )


def _seed_structural_snapshot_rows(connection) -> int:
    """Create only the empty lock rows required by snapshot-backed stores.

    Historical migrations 018/019 seeded these rows so ``SELECT ... FOR UPDATE``
    always locks an existing primary-key row. Fresh bootstrap does not replay
    historical DML, so the same non-commercial invariant is expressed explicitly
    here. No customer, tenant, lead, plan, price, or outcome data is inserted.
    """
    communication = connection.execute(
        text(
            """
            INSERT INTO communication_hub_snapshots (collection, data)
            VALUES ('contact_log', '[]'::jsonb), ('sequences', '[]'::jsonb)
            ON CONFLICT (collection) DO NOTHING
            RETURNING collection
            """
        )
    ).scalars().all()
    knowledge = connection.execute(
        text(
            """
            INSERT INTO knowledge_accumulator_snapshots (collection, data)
            VALUES ('entries', '[]'::jsonb)
            ON CONFLICT (collection) DO NOTHING
            RETURNING collection
            """
        )
    ).scalars().all()
    inserted = len(communication) + len(knowledge)
    if inserted != 3:
        raise RuntimeError(
            f"fresh bootstrap structural snapshot seed mismatch: inserted={inserted}"
        )
    return inserted


def _public_table_names(metadata: MetaData) -> set[str]:
    return {
        table.name
        for table in metadata.tables.values()
        if table.schema in (None, "public")
    }


def _include_bootstrap_object(
    object_: object,
    name: str | None,
    type_: str,
    reflected: bool,
    compare_to: object | None,
) -> bool:
    """Exclude only Alembic's control table from fresh-schema drift checks."""
    del object_
    return not (
        type_ == "table"
        and reflected
        and compare_to is None
        and name == "alembic_version"
    )


def _bootstrap_sync(connection) -> dict[str, object]:
    existing = _database_occupancy(connection)
    if existing:
        raise RuntimeError(
            "refusing fresh bootstrap on non-empty database: "
            + ", ".join(existing[:20])
        )

    metadata, capture = build_fresh_schema_metadata()
    _ensure_extensions(connection, capture.required_extensions)
    metadata.create_all(connection)
    structural_seed_rows = _seed_structural_snapshot_rows(connection)
    _ensure_wide_alembic_version_table(connection)

    script = _script_directory()
    migration = MigrationContext.configure(connection)
    migration.stamp(script, "heads")

    expected_tables = _public_table_names(metadata)
    actual_tables = set(inspect(connection).get_table_names())
    missing = sorted(expected_tables - actual_tables)
    if missing:
        raise RuntimeError("metadata tables missing after bootstrap: " + ", ".join(missing))

    missing_migration_tables = sorted(capture.migration_only_tables - actual_tables)
    if missing_migration_tables:
        raise RuntimeError(
            "migration-owned tables missing after bootstrap: "
            + ", ".join(missing_migration_tables)
        )

    current_heads = set(MigrationContext.configure(connection).get_current_heads())
    script_heads = set(script.get_heads())
    if current_heads != script_heads:
        raise RuntimeError(
            f"Alembic stamp mismatch: database={sorted(current_heads)} "
            f"script={sorted(script_heads)}"
        )

    compare_context = MigrationContext.configure(
        connection,
        opts={
            "compare_type": True,
            "compare_server_default": True,
            "include_object": _include_bootstrap_object,
        },
    )
    diffs = compare_metadata(compare_context, metadata)
    if diffs:
        preview = "; ".join(str(item) for item in diffs[:10])
        raise RuntimeError(f"fresh schema drift after bootstrap: {preview}")

    return {
        "tables": len(expected_tables),
        "migration_only_tables": len(capture.migration_only_tables),
        "captured_operations": capture.captured_operations,
        "ignored_data_statements": capture.ignored_data_statements,
        "structural_seed_rows": structural_seed_rows,
        "heads": sorted(script_heads),
    }


async def bootstrap() -> dict[str, object]:
    database_url, connect_args = _database_connection_settings()
    engine = create_async_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
    )
    try:
        async with engine.begin() as connection:
            return await connection.run_sync(_bootstrap_sync)
    finally:
        await engine.dispose()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--confirm-empty-bootstrap",
        action="store_true",
        help="Acknowledge that the target must be a brand-new empty database.",
    )
    args = parser.parse_args()

    if not args.confirm_empty_bootstrap:
        raise SystemExit("refusing bootstrap without --confirm-empty-bootstrap")
    if os.getenv(ACK_ENV, "").strip() != "1":
        raise SystemExit(f"refusing bootstrap unless {ACK_ENV}=1")

    result = asyncio.run(bootstrap())
    print(
        "FRESH_DB_BOOTSTRAP=PASS "
        f"tables={result['tables']} "
        f"migration_only_tables={result['migration_only_tables']} "
        f"captured_operations={result['captured_operations']} "
        f"ignored_data_statements={result['ignored_data_statements']} "
        f"structural_seed_rows={result['structural_seed_rows']} "
        f"heads={','.join(result['heads'])} commercial_seed=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
