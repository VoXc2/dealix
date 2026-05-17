"""Default Diagnostics store accessor.

Resolves a process-scoped :class:`PostgresDiagnosticStore` singleton.
Falls back to an in-memory SQLite engine when no database URL is set.
"""
from __future__ import annotations

import logging
import os

from auto_client_acquisition.diagnostic_engine.diagnostic_postgres import (
    PostgresDiagnosticStore,
)

_LOG = logging.getLogger(__name__)

_DEFAULT_STORE: PostgresDiagnosticStore | None = None


def _store_url() -> str:
    explicit = os.getenv("DEALIX_DIAGNOSTIC_STORE_DB_URL")
    if explicit:
        return explicit
    try:
        from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
        from core.config.settings import get_settings

        url = getattr(get_settings(), "database_url", "") or ""
        if url:
            return sync_sqlalchemy_url(url)
    except Exception:  # noqa: BLE001
        pass
    return "sqlite:///:memory:"


def _should_autocreate(url: str) -> bool:
    return ":memory:" in url or url.startswith("sqlite:")


def get_default_diagnostic_store() -> PostgresDiagnosticStore:
    """Return the process-scoped Diagnostics store singleton."""
    global _DEFAULT_STORE
    if _DEFAULT_STORE is None:
        url = _store_url()
        try:
            _DEFAULT_STORE = PostgresDiagnosticStore(
                database_url=url, create_tables=_should_autocreate(url)
            )
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("diagnostic_store_unavailable:%s", type(exc).__name__)
            _DEFAULT_STORE = PostgresDiagnosticStore(
                database_url="sqlite:///:memory:", create_tables=True
            )
    return _DEFAULT_STORE


def reset_default_diagnostic_store() -> None:
    """Test helper: drop the cached singleton."""
    global _DEFAULT_STORE
    _DEFAULT_STORE = None


__all__ = ["get_default_diagnostic_store", "reset_default_diagnostic_store"]
