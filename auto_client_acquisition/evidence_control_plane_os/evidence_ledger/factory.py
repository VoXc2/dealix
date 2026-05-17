"""Backend factory for the append-only Evidence Events ledger.

The file-backed JSONL ledger remains the default until the env flag
``EVIDENCE_LEDGER_BACKEND`` is set to ``postgres`` or ``dual``. Both
backends expose the same public API (``append``, ``list_events``,
``get``, ``verify``) so call sites do not need to know which one they
are talking to.

Mirrors ``auto_client_acquisition/proof_ledger/factory.py``.
"""
from __future__ import annotations

import logging
import os
from typing import Union

from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.file_backend import (
    FileEvidenceLedger,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.postgres_backend import (
    PostgresEvidenceLedger,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.schemas import (
    EvidenceEvent,
)

_LOG = logging.getLogger(__name__)


def _backend_name() -> str:
    """Resolve the configured backend, defaulting to ``"file"``."""
    return (os.getenv("EVIDENCE_LEDGER_BACKEND", "file") or "file").lower().strip()


def _ledger_sync_url() -> str | None:
    try:
        from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
        from core.config.settings import get_settings

        url = getattr(get_settings(), "database_url", "") or ""
        return sync_sqlalchemy_url(url) if url else None
    except Exception:  # noqa: BLE001
        return None


def _pg_should_autocreate(url: str) -> bool:
    return ":memory:" in url or url.startswith("sqlite:")


class DualEvidenceLedger:
    """File canonical reads; Postgres best-effort duplicate writes."""

    def __init__(self) -> None:
        self._file = FileEvidenceLedger()
        self._pg: PostgresEvidenceLedger | None = None
        url = _ledger_sync_url()
        if url:
            try:
                self._pg = PostgresEvidenceLedger(
                    database_url=url,
                    create_tables=_pg_should_autocreate(url),
                )
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("evidence_ledger_dual_pg_unavailable:%s", type(exc).__name__)

    def append(self, event: EvidenceEvent) -> EvidenceEvent:
        out = self._file.append(event)
        if self._pg is not None:
            try:
                self._pg.append(event)
            except Exception as exc:  # noqa: BLE001
                _LOG.debug("evidence_ledger_dual_pg_append_failed:%s", type(exc).__name__)
        return out

    def list_events(self, **kwargs: object) -> list[EvidenceEvent]:
        return self._file.list_events(**kwargs)  # type: ignore[arg-type]

    def get(self, event_id: str) -> EvidenceEvent | None:
        return self._file.get(event_id)

    def verify(self, event: EvidenceEvent) -> bool:
        return self._file.verify(event)


EvidenceLedger = Union[FileEvidenceLedger, PostgresEvidenceLedger, DualEvidenceLedger]

_FILE_DEFAULT: FileEvidenceLedger | None = None
_POSTGRES_DEFAULT: PostgresEvidenceLedger | None = None
_DUAL_DEFAULT: DualEvidenceLedger | None = None


def get_default_evidence_ledger() -> EvidenceLedger:
    """Return the configured evidence ledger singleton.

    Selects the backend based on ``EVIDENCE_LEDGER_BACKEND``:
      * ``"file"``  (default) → :class:`FileEvidenceLedger`
      * ``"postgres"``         → :class:`PostgresEvidenceLedger`
      * ``"dual"``             → :class:`DualEvidenceLedger`

    Misconfiguration falls back to the file backend.
    """
    global _FILE_DEFAULT, _POSTGRES_DEFAULT, _DUAL_DEFAULT
    backend = _backend_name()
    if backend == "dual":
        if _DUAL_DEFAULT is None:
            _DUAL_DEFAULT = DualEvidenceLedger()
        return _DUAL_DEFAULT
    if backend == "postgres":
        if _POSTGRES_DEFAULT is None:
            url = _ledger_sync_url()
            if not url:
                if _FILE_DEFAULT is None:
                    _FILE_DEFAULT = FileEvidenceLedger()
                return _FILE_DEFAULT
            try:
                _POSTGRES_DEFAULT = PostgresEvidenceLedger(
                    database_url=url,
                    create_tables=_pg_should_autocreate(url),
                )
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("evidence_ledger_postgres_unavailable:%s", type(exc).__name__)
                if _FILE_DEFAULT is None:
                    _FILE_DEFAULT = FileEvidenceLedger()
                return _FILE_DEFAULT
        return _POSTGRES_DEFAULT
    if _FILE_DEFAULT is None:
        _FILE_DEFAULT = FileEvidenceLedger()
    return _FILE_DEFAULT


def reset_default_evidence_ledger() -> None:
    """Test helper: drop cached singletons so the next call re-evaluates the env."""
    global _FILE_DEFAULT, _POSTGRES_DEFAULT, _DUAL_DEFAULT
    _FILE_DEFAULT = None
    _POSTGRES_DEFAULT = None
    _DUAL_DEFAULT = None


__all__ = [
    "DualEvidenceLedger",
    "EvidenceLedger",
    "get_default_evidence_ledger",
    "reset_default_evidence_ledger",
]
