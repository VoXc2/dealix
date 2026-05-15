"""Backend factory for the proof ledger.

The file-backed JSONL ledger remains the default until a founder env flag
flips ``PROOF_LEDGER_BACKEND=postgres`` or ``dual``. Both backends expose the same
public API (``record``, ``list_events``, ``record_unit``, ``list_units``)
so call sites do not need to know which one they are talking to.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any, Union

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
from auto_client_acquisition.proof_ledger.file_backend import FileProofLedger
from auto_client_acquisition.proof_ledger.postgres_backend import (
    PostgresProofLedger,
)

_LOG = logging.getLogger(__name__)


def _backend_name() -> str:
    """Resolve the configured backend, defaulting to ``"file"``.

    Imported lazily so this module stays cheap at import time and avoids
    pulling pydantic-settings into hot paths that only need the storage
    classes.
    """
    try:
        from core.config.settings import get_settings
    except Exception:  # noqa: BLE001 — settings import never blocks ledger
        return "file"
    try:
        return getattr(get_settings(), "proof_ledger_backend", "file") or "file"
    except Exception:  # noqa: BLE001
        return "file"


def _ledger_sync_url() -> str | None:
    try:
        from core.config.settings import get_settings

        u = getattr(get_settings(), "database_url", "") or ""
        return sync_sqlalchemy_url(u) if u else None
    except Exception:  # noqa: BLE001
        return None


def _pg_should_autocreate(url: str) -> bool:
    return ":memory:" in url or url.startswith("sqlite:")


class DualProofLedger:
    """File canonical reads; Postgres best-effort duplicate writes."""

    def __init__(self) -> None:
        self._file = FileProofLedger()
        self._pg: PostgresProofLedger | None = None
        url = _ledger_sync_url()
        if url:
            try:
                self._pg = PostgresProofLedger(
                    database_url=url,
                    create_tables=_pg_should_autocreate(url),
                )
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("proof_ledger_dual_pg_unavailable:%s", type(exc).__name__)

    def record(self, event: Any) -> Any:
        out = self._file.record(event)
        if self._pg is not None:
            try:
                self._pg.record(event)
            except Exception as exc:  # noqa: BLE001
                _LOG.debug("proof_ledger_dual_pg_record_failed:%s", type(exc).__name__)
        return out

    def list_events(self, *args: Any, **kwargs: Any) -> Any:
        return self._file.list_events(*args, **kwargs)

    def record_unit(self, unit: Any) -> Any:
        out = self._file.record_unit(unit)
        if self._pg is not None:
            try:
                self._pg.record_unit(unit)
            except Exception as exc:  # noqa: BLE001
                _LOG.debug("proof_ledger_dual_pg_unit_failed:%s", type(exc).__name__)
        return out

    def list_units(self, *args: Any, **kwargs: Any) -> Any:
        return self._file.list_units(*args, **kwargs)


ProofLedger = Union[FileProofLedger, PostgresProofLedger, DualProofLedger]

_FILE_DEFAULT: FileProofLedger | None = None
_POSTGRES_DEFAULT: PostgresProofLedger | None = None
_DUAL_DEFAULT: DualProofLedger | None = None


def get_default_ledger() -> ProofLedger:
    """Return the configured ledger singleton.

    Selects the backend based on ``settings.proof_ledger_backend``:
      * ``"file"``  (default) → :class:`FileProofLedger`
      * ``"postgres"``         → :class:`PostgresProofLedger`
      * ``"dual"``             → :class:`DualProofLedger`

    Misconfiguration falls back to the file backend.
    """
    global _FILE_DEFAULT, _POSTGRES_DEFAULT, _DUAL_DEFAULT
    backend = _backend_name().lower().strip()
    if backend == "dual":
        if _DUAL_DEFAULT is None:
            _DUAL_DEFAULT = DualProofLedger()
        return _DUAL_DEFAULT
    if backend == "postgres":
        if _POSTGRES_DEFAULT is None:
            url = _ledger_sync_url()
            if not url:
                if _FILE_DEFAULT is None:
                    _FILE_DEFAULT = FileProofLedger()
                return _FILE_DEFAULT
            try:
                _POSTGRES_DEFAULT = PostgresProofLedger(
                    database_url=url,
                    create_tables=_pg_should_autocreate(url),
                )
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("proof_ledger_postgres_unavailable:%s", type(exc).__name__)
                if _FILE_DEFAULT is None:
                    _FILE_DEFAULT = FileProofLedger()
                return _FILE_DEFAULT
        return _POSTGRES_DEFAULT
    if _FILE_DEFAULT is None:
        _FILE_DEFAULT = FileProofLedger()
    return _FILE_DEFAULT


def reset_default_ledger() -> None:
    """Test helper: drop cached singletons so the next call re-evaluates settings."""
    global _FILE_DEFAULT, _POSTGRES_DEFAULT, _DUAL_DEFAULT
    _FILE_DEFAULT = None
    _POSTGRES_DEFAULT = None
    _DUAL_DEFAULT = None


def recent_events(*, since: datetime, limit: int = 200) -> list[dict[str, Any]]:
    """Events at or after ``since`` (UTC-aware), newest-first, as JSON dicts.

    Used by Personal Operator / weekly jobs. ``since`` may be naive UTC;
    normalized for comparison against ``ProofEvent.created_at``.
    """
    if since.tzinfo is None:
        since = since.replace(tzinfo=UTC)
    ledger = get_default_ledger()
    raw = ledger.list_events(limit=min(max(limit * 4, limit), 800))
    out: list[dict[str, Any]] = []
    for ev in raw:
        ca = getattr(ev, "created_at", None)
        if ca is None:
            continue
        if ca.tzinfo is None:
            ca = ca.replace(tzinfo=UTC)
        if ca < since:
            continue
        dumped = ev.model_dump(mode="json")
        pl = dumped.get("payload") or {}
        level = pl.get("evidence_level") or pl.get("level")
        if level:
            dumped["level"] = str(level).upper()
        out.append(dumped)
    out.sort(key=lambda d: d.get("created_at") or "", reverse=True)
    return out[:limit]


__all__ = [
    "DualProofLedger",
    "ProofLedger",
    "get_default_ledger",
    "recent_events",
    "reset_default_ledger",
]
