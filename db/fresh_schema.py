"""Build the complete fresh-PostgreSQL schema without replaying legacy DML.

Dealix has three schema ownership layers:

* SQLAlchemy ORM tables registered on ``db.models.Base.metadata``;
* dedicated runtime ORM metadata that intentionally lives outside ``db.models``;
* historical Alembic revisions that create persistence tables used through raw
  SQL and therefore intentionally have no ORM mapper.

A new database cannot run the historical graph from zero because the two roots
start by altering pre-existing tables. This module derives a deterministic
fresh-install metadata snapshot with an explicit ownership boundary:

* current application ORM metadata is authoritative for tables and columns it owns;
* dedicated runtime ORM metadata is authoritative for its persistence tables;
* Alembic contributes migration-only tables plus explicit database indexes and
  constraints;
* historical data-changing statements are never replayed.

The only raw schema statements currently accepted are the idempotent pgcrypto and
vector extensions. Any unsupported migration operation fails closed until this capture
layer is updated and covered by the PostgreSQL proof.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import sqlalchemy as sa
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import MetaData, Table
from sqlalchemy.schema import (
    CheckConstraint,
    Constraint,
    DefaultClause,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    UniqueConstraint,
)

from auto_client_acquisition.proof_ledger.postgres_backend import ProofLedgerBase
from db.model_registry import load_all_models
from db.models import Base

REPO_ROOT = Path(__file__).resolve().parents[1]
_ALLOWED_DML_PREFIXES = ("DELETE ", "INSERT ", "UPDATE ")
_ALLOWED_EXTENSION_SQLS = frozenset(
    {
        "CREATE EXTENSION IF NOT EXISTS PGCRYPTO",
        "CREATE EXTENSION IF NOT EXISTS VECTOR",
    }
)


class FreshSchemaCaptureError(RuntimeError):
    """Raised when migration schema cannot be represented safely."""


@dataclass
class FreshSchemaReport:
    """Evidence emitted by the deterministic migration-schema capture."""

    revision_ids: list[str] = field(default_factory=list)
    migration_created_tables: set[str] = field(default_factory=set)
    orm_owned_tables: set[str] = field(default_factory=set)
    dedicated_orm_owned_tables: set[str] = field(default_factory=set)
    required_extensions: set[str] = field(default_factory=set)
    ignored_data_statements: int = 0
    ignored_orm_column_operations: int = 0
    preserved_foreign_key_actions: int = 0
    captured_operations: int = 0

    @property
    def authoritative_tables(self) -> set[str]:
        """Tables whose current runtime ORM contract wins over legacy migrations."""
        return self.orm_owned_tables | self.dedicated_orm_owned_tables

    @property
    def migration_only_tables(self) -> set[str]:
        return self.migration_created_tables - self.authoritative_tables


class _MigrationMetadataCapture:
    """Small Alembic ``op`` replacement that mutates an in-memory MetaData."""

    def __init__(self, metadata: MetaData, report: FreshSchemaReport) -> None:
        self.metadata = metadata
        self.report = report

    def _table(self, table_name: str, schema: str | None = None) -> Table:
        key = f"{schema}.{table_name}" if schema else table_name
        table = self.metadata.tables.get(key)
        if table is None:
            raise FreshSchemaCaptureError(f"migration references unknown table: {key}")
        return table

    def _is_orm_owned(self, table: Table) -> bool:
        return table.fullname in self.report.authoritative_tables

    def _ignore_orm_column_operation(self, table: Table) -> None:
        if not self._is_orm_owned(table):
            raise FreshSchemaCaptureError(
                f"internal ownership error for migration table {table.fullname}"
            )
        self.report.ignored_orm_column_operations += 1

    @staticmethod
    def _constraint_names(table: Table) -> set[str]:
        return {
            constraint.name
            for constraint in table.constraints
            if getattr(constraint, "name", None)
        }

    @staticmethod
    def _index_names(table: Table) -> set[str]:
        return {index.name for index in table.indexes if index.name}

    @staticmethod
    def _foreign_key_signature(
        constraint: ForeignKeyConstraint,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Return the local/remote column identity for a FK constraint."""
        return (
            tuple(constraint.column_keys),
            tuple(foreign_key.target_fullname for foreign_key in constraint.elements),
        )

    def _preserve_migration_foreign_key_actions(
        self,
        table: Table,
        elements: Iterable[Any],
    ) -> None:
        """Overlay missing FK actions when migration and ORM describe the same edge.

        Current ORM columns and relationships remain authoritative. Historical
        migrations are allowed to fill only an omitted ``ondelete``/``onupdate``
        action on an already-existing matching foreign key. An explicit action in
        current ORM metadata is never overwritten, and a migration-only FK is not
        resurrected on an ORM-owned table.
        """
        existing_foreign_keys = {
            self._foreign_key_signature(constraint): constraint
            for constraint in table.constraints
            if isinstance(constraint, ForeignKeyConstraint)
        }
        for element in elements:
            if not isinstance(element, ForeignKeyConstraint):
                continue
            matching = existing_foreign_keys.get(self._foreign_key_signature(element))
            if matching is None:
                continue

            changed = False
            for attribute in ("ondelete", "onupdate"):
                migration_value = getattr(element, attribute, None)
                current_value = getattr(matching, attribute, None)
                if migration_value is None or current_value is not None:
                    continue
                setattr(matching, attribute, migration_value)
                for foreign_key in matching.elements:
                    setattr(foreign_key, attribute, migration_value)
                changed = True
            if changed:
                self.report.preserved_foreign_key_actions += 1

    def create_table(self, table_name: str, *elements: Any, **kwargs: Any) -> Table:
        schema = kwargs.get("schema")
        key = f"{schema}.{table_name}" if schema else table_name
        self.report.migration_created_tables.add(key)
        self.report.captured_operations += 1

        existing = self.metadata.tables.get(key)
        if existing is None:
            return Table(table_name, self.metadata, *elements, **kwargs)

        # The final runtime ORM definition wins for any table it owns. Replaying
        # an old create-table shape on top of current metadata could resurrect
        # removed columns or regress their types. A matching migration FK may,
        # however, contribute an action that current ORM omitted (e.g. CASCADE or
        # SET NULL); preserve only that compatible action before ignoring the
        # historical table shape.
        if self._is_orm_owned(existing):
            self._preserve_migration_foreign_key_actions(existing, elements)
            self._ignore_orm_column_operation(existing)
            return existing

        existing_constraint_names = self._constraint_names(existing)
        for element in elements:
            if isinstance(element, sa.Column):
                if element.name not in existing.c:
                    existing.append_column(element)
                continue
            if not isinstance(element, Constraint):
                continue
            name = getattr(element, "name", None)
            if isinstance(element, PrimaryKeyConstraint) and list(
                existing.primary_key.columns
            ):
                continue
            if name and name in existing_constraint_names:
                continue
            existing.append_constraint(element)
            if name:
                existing_constraint_names.add(name)
        return existing

    def create_index(
        self,
        index_name: str,
        table_name: str,
        columns: Iterable[Any],
        **kwargs: Any,
    ) -> Index | None:
        table = self._table(table_name, kwargs.pop("schema", None))
        self.report.captured_operations += 1
        if index_name in self._index_names(table):
            return None

        expressions: list[Any] = []
        for column in columns:
            if isinstance(column, str):
                if column not in table.c:
                    # Current runtime ORM metadata is authoritative for an owned
                    # table. A historical index that depends on a removed column
                    # must not resurrect that column or block a fresh install.
                    # Migration-only tables remain fail-closed because no current
                    # runtime contract supersedes their historical schema.
                    if self._is_orm_owned(table):
                        self._ignore_orm_column_operation(table)
                        return None
                    raise FreshSchemaCaptureError(
                        f"index {index_name} references missing column "
                        f"{table.fullname}.{column}"
                    )
                expressions.append(table.c[column])
            else:
                expressions.append(column)
        return Index(index_name, *expressions, **kwargs)

    def add_column(
        self,
        table_name: str,
        column: sa.Column[Any],
        **kwargs: Any,
    ) -> None:
        table = self._table(table_name, kwargs.get("schema"))
        self.report.captured_operations += 1
        if self._is_orm_owned(table):
            self._ignore_orm_column_operation(table)
            return
        if column.name not in table.c:
            table.append_column(column)

    def alter_column(self, table_name: str, column_name: str, **kwargs: Any) -> None:
        table = self._table(table_name, kwargs.get("schema"))
        if column_name not in table.c:
            raise FreshSchemaCaptureError(
                f"alter_column references missing column {table.fullname}.{column_name}"
            )
        self.report.captured_operations += 1
        if self._is_orm_owned(table):
            self._ignore_orm_column_operation(table)
            return

        column = table.c[column_name]
        if kwargs.get("type_") is not None:
            column.type = kwargs["type_"]
        if kwargs.get("nullable") is not None:
            column.nullable = bool(kwargs["nullable"])
        if "server_default" in kwargs:
            value = kwargs["server_default"]
            if value is None or isinstance(value, DefaultClause):
                column.server_default = value
            else:
                column.server_default = DefaultClause(value)
        new_name = kwargs.get("new_column_name")
        if new_name and new_name != column_name:
            raise FreshSchemaCaptureError(
                "column rename requires explicit fresh-schema support: "
                f"{table.fullname}.{column_name}->{new_name}"
            )

    def create_unique_constraint(
        self,
        name: str,
        table_name: str,
        columns: Iterable[str],
        **kwargs: Any,
    ) -> None:
        table = self._table(table_name, kwargs.get("schema"))
        self.report.captured_operations += 1
        if name in self._constraint_names(table):
            return
        table.append_constraint(UniqueConstraint(*columns, name=name))

    def create_check_constraint(
        self,
        name: str,
        table_name: str,
        condition: Any,
        **kwargs: Any,
    ) -> None:
        table = self._table(table_name, kwargs.get("schema"))
        self.report.captured_operations += 1
        if name in self._constraint_names(table):
            return
        table.append_constraint(CheckConstraint(condition, name=name))

    def create_foreign_key(
        self,
        name: str,
        source_table: str,
        referent_table: str,
        local_cols: Iterable[str],
        remote_cols: Iterable[str],
        **kwargs: Any,
    ) -> None:
        table = self._table(source_table, kwargs.pop("source_schema", None))
        self.report.captured_operations += 1
        if name in self._constraint_names(table):
            return
        target_schema = kwargs.pop("referent_schema", None)
        prefix = f"{target_schema}." if target_schema else ""
        references = [f"{prefix}{referent_table}.{column}" for column in remote_cols]
        table.append_constraint(
            ForeignKeyConstraint(local_cols, references, name=name, **kwargs)
        )

    def create_primary_key(
        self,
        name: str,
        table_name: str,
        columns: Iterable[str],
        **kwargs: Any,
    ) -> None:
        table = self._table(table_name, kwargs.get("schema"))
        self.report.captured_operations += 1
        if list(table.primary_key.columns):
            return
        table.append_constraint(PrimaryKeyConstraint(*columns, name=name))

    def drop_table(self, table_name: str, **kwargs: Any) -> None:
        schema = kwargs.get("schema")
        key = f"{schema}.{table_name}" if schema else table_name
        self.report.captured_operations += 1
        table = self.metadata.tables.get(key)
        if table is None:
            return
        if self._is_orm_owned(table):
            self._ignore_orm_column_operation(table)
            return
        self.metadata.remove(table)
        self.report.migration_created_tables.discard(key)

    def drop_index(
        self,
        index_name: str,
        table_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.report.captured_operations += 1
        tables = (
            [self._table(table_name, kwargs.get("schema"))]
            if table_name
            else list(self.metadata.tables.values())
        )
        for table in tables:
            for index in list(table.indexes):
                if index.name == index_name:
                    table.indexes.discard(index)
                    return

    def drop_constraint(
        self,
        name: str,
        table_name: str,
        type_: str | None = None,
        **kwargs: Any,
    ) -> None:
        del type_
        table = self._table(table_name, kwargs.get("schema"))
        self.report.captured_operations += 1
        for constraint in list(table.constraints):
            if getattr(constraint, "name", None) == name:
                table.constraints.discard(constraint)
                return

    def drop_column(self, table_name: str, column_name: str, **kwargs: Any) -> None:
        table = self._table(table_name, kwargs.get("schema"))
        self.report.captured_operations += 1
        if self._is_orm_owned(table):
            self._ignore_orm_column_operation(table)
            return
        if column_name in table.c:
            table._columns.remove(table.c[column_name])  # noqa: SLF001

    def bulk_insert(self, table: Any, rows: Any, **kwargs: Any) -> None:
        del table, rows, kwargs
        self.report.captured_operations += 1
        self.report.ignored_data_statements += 1

    def execute(self, statement: Any, *args: Any, **kwargs: Any) -> None:
        del args, kwargs
        sql = " ".join(str(statement).strip().split())
        upper = sql.upper()
        self.report.captured_operations += 1
        if upper in _ALLOWED_EXTENSION_SQLS:
            if "PGCRYPTO" in upper:
                self.report.required_extensions.add("pgcrypto")
            elif "VECTOR" in upper:
                self.report.required_extensions.add("vector")
            return
        if upper.startswith(_ALLOWED_DML_PREFIXES):
            self.report.ignored_data_statements += 1
            return
        raise FreshSchemaCaptureError(
            "unsupported raw migration SQL in fresh-schema capture: " + sql[:180]
        )

    def __getattr__(self, name: str) -> Any:
        # Python's attribute protocol requires AttributeError here. The revision
        # capture loop wraps any unsupported Alembic operation in a
        # FreshSchemaCaptureError with the revision ID, preserving fail-closed
        # behavior without violating special-method semantics.
        raise AttributeError(
            f"unsupported Alembic operation in fresh-schema capture: op.{name}"
        )


def _script_directory() -> ScriptDirectory:
    config_path = REPO_ROOT / "alembic.ini"
    if not config_path.exists():
        raise FreshSchemaCaptureError("alembic.ini not found in repository root")
    return ScriptDirectory.from_config(Config(str(config_path)))


def build_fresh_schema_metadata() -> tuple[MetaData, FreshSchemaReport]:
    """Return complete fresh-install metadata and an auditable capture report."""
    load_all_models()
    metadata = MetaData()
    for table in Base.metadata.sorted_tables:
        table.to_metadata(metadata)
    orm_owned_tables = set(metadata.tables)

    for table in ProofLedgerBase.metadata.sorted_tables:
        table.to_metadata(metadata)
    dedicated_orm_owned_tables = set(metadata.tables) - orm_owned_tables

    report = FreshSchemaReport(
        orm_owned_tables=orm_owned_tables,
        dedicated_orm_owned_tables=dedicated_orm_owned_tables,
    )
    capture = _MigrationMetadataCapture(metadata, report)
    revisions = list(reversed(list(_script_directory().walk_revisions())))
    for revision in revisions:
        module = revision.module
        upgrade = getattr(module, "upgrade", None)
        if not callable(upgrade):
            raise FreshSchemaCaptureError(f"revision {revision.revision} has no upgrade()")
        original_op = getattr(module, "op", None)
        report.revision_ids.append(str(revision.revision))
        module.op = capture
        try:
            upgrade()
        except FreshSchemaCaptureError:
            raise
        except Exception as exc:
            raise FreshSchemaCaptureError(
                f"failed to capture revision {revision.revision}: {exc}"
            ) from exc
        finally:
            module.op = original_op

    missing_migration_tables = report.migration_created_tables - set(metadata.tables)
    if missing_migration_tables:
        raise FreshSchemaCaptureError(
            "captured migration tables missing from metadata: "
            + ", ".join(sorted(missing_migration_tables))
        )

    report.required_extensions.add("vector")

    return metadata, report


def migration_only_table_names() -> frozenset[str]:
    """Return tables that exist only in the Alembic persistence contract."""
    _, report = build_fresh_schema_metadata()
    return frozenset(report.migration_only_tables)
