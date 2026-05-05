"""Backend factory for the proof ledger.

The file-backed JSONL ledger remains the default until a founder env flag
flips ``PROOF_LEDGER_BACKEND=postgres``. Both backends expose the same
public API (``record``, ``list_events``, ``record_unit``, ``list_units``)
so call sites do not need to know which one they are talking to.
"""
from __future__ import annotations

from typing import Union

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
    except Exception:  # noqa: BLE001 — settings import never blocks ledger
        return "file"
    try:
        return getattr(get_settings(), "proof_ledger_backend", "file") or "file"
    except Exception:  # noqa: BLE001
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


__all__ = [
    "ProofLedger",
    "get_default_ledger",
    "reset_default_ledger",
]
