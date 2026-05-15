"""Backend factory for the proof ledger.

The file-backed JSONL ledger remains the default until a founder env flag
flips ``PROOF_LEDGER_BACKEND=postgres``. Both backends expose the same
public API (``record``, ``list_events``, ``record_unit``, ``list_units``)
so call sites do not need to know which one they are talking to.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Union

from auto_client_acquisition.proof_ledger.file_backend import FileProofLedger
from auto_client_acquisition.proof_ledger.postgres_backend import (
    PostgresProofLedger,
)

ProofLedger = Union[FileProofLedger, PostgresProofLedger]

# Process-scoped singletons — created lazily.
_FILE_DEFAULT: FileProofLedger | None = None
_POSTGRES_DEFAULT: PostgresProofLedger | None = None


def _backend_name() -> str:
    """Resolve the configured backend, defaulting to ``"file"``.

    Imported lazily so this module stays cheap at import time and avoids
    pulling pydantic-settings into hot paths that only need the storage
    classes.
    """
    try:
        from core.config.settings import get_settings
    except Exception:
        return "file"
    try:
        return getattr(get_settings(), "proof_ledger_backend", "file") or "file"
    except Exception:
        return "file"


def get_default_ledger() -> ProofLedger:
    """Return the configured ledger singleton.

    Selects the backend based on ``settings.proof_ledger_backend``:
      * ``"file"``  (default) → :class:`FileProofLedger`
      * ``"postgres"``         → :class:`PostgresProofLedger`

    Anything else falls back to the file backend so a misconfigured env
    never silently data-loses into a non-existent table.
    """
    global _FILE_DEFAULT, _POSTGRES_DEFAULT
    backend = _backend_name().lower().strip()
    if backend == "postgres":
        if _POSTGRES_DEFAULT is None:
            _POSTGRES_DEFAULT = PostgresProofLedger()
        return _POSTGRES_DEFAULT
    if _FILE_DEFAULT is None:
        _FILE_DEFAULT = FileProofLedger()
    return _FILE_DEFAULT


def reset_default_ledger() -> None:
    """Test helper: drop cached singletons so the next call re-evaluates settings."""
    global _FILE_DEFAULT, _POSTGRES_DEFAULT
    _FILE_DEFAULT = None
    _POSTGRES_DEFAULT = None


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
    "ProofLedger",
    "get_default_ledger",
    "recent_events",
    "reset_default_ledger",
]
