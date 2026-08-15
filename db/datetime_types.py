"""Runtime datetime compatibility for Dealix's legacy PostgreSQL schema.

Dealix currently has two intentional datetime contracts:

* legacy annotation-inferred ``datetime`` columns on the canonical
  ``db.models.Base`` compile to ``TIMESTAMP WITHOUT TIME ZONE`` and are read by
  existing code as naive UTC;
* newer explicitly declared ``DateTime(timezone=True)`` columns are genuinely
  timezone-aware and must remain untouched.

``UTCNaiveDateTime`` preserves the legacy physical/read contract while making
writes safe:

* aware input -> convert to UTC and strip timezone before DBAPI binding;
* naive input -> preserve as already-normalized legacy UTC;
* database result -> preserve legacy naive UTC semantics.

The SQLAlchemy listener is deliberately scoped to ``db.models.Base.metadata``.
Dealix contains other independent DeclarativeBase registries; they must not be
silently rewritten by this compatibility layer.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import Column, DateTime, event
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.types import TypeDecorator


class UTCNaiveDateTime(TypeDecorator[datetime]):
    """Normalize datetime writes to naive UTC while preserving legacy reads."""

    impl = DateTime(timezone=False)
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect: Any) -> datetime | None:
        if value is None:
            return None
        if not isinstance(value, datetime):
            raise TypeError("UTCNaiveDateTime accepts datetime values only")
        if value.tzinfo is None:
            return value
        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(self, value: datetime | None, dialect: Any) -> datetime | None:
        if value is None:
            return None
        if not isinstance(value, datetime):
            raise TypeError("UTCNaiveDateTime received a non-datetime DB value")
        if value.tzinfo is None:
            return value
        # Defensive only: timezone=False PostgreSQL columns normally return
        # naive values. Preserve the legacy Python contract even if a driver
        # unexpectedly supplies an aware value.
        return value.astimezone(UTC).replace(tzinfo=None)


def normalize_legacy_datetime_column(column: Column[Any]) -> bool:
    """Apply write normalization to one legacy timezone-naive datetime column."""
    column_type = column.type
    if isinstance(column_type, UTCNaiveDateTime):
        return False
    if isinstance(column_type, DateTime) and not bool(column_type.timezone):
        column.type = UTCNaiveDateTime()
        return True
    return False


def normalize_legacy_datetime_metadata(metadata: MetaData) -> int:
    """Normalize all currently registered legacy datetime columns in metadata."""
    changed = 0
    for table in metadata.tables.values():
        for column in table.columns:
            changed += int(normalize_legacy_datetime_column(column))
    return changed


def _canonical_metadata() -> MetaData | None:
    """Resolve db.models.Base.metadata without importing db.models recursively."""
    module = sys.modules.get("db.models")
    base = getattr(module, "Base", None) if module is not None else None
    metadata = getattr(base, "metadata", None)
    return metadata if isinstance(metadata, MetaData) else None


def _normalize_after_attach(column: Column[Any], parent: Any) -> None:
    """Normalize only columns attached to the canonical Dealix model metadata."""
    metadata = _canonical_metadata()
    if metadata is None or getattr(parent, "metadata", None) is not metadata:
        return
    normalize_legacy_datetime_column(column)


def install_legacy_datetime_listener() -> None:
    """Idempotently normalize canonical timezone-naive columns after attach."""
    if event.contains(Column, "after_parent_attach", _normalize_after_attach):
        return
    event.listen(
        Column,
        "after_parent_attach",
        _normalize_after_attach,
        propagate=True,
    )
