"""Default Decision Passport store accessor.

Resolves a process-scoped :class:`PostgresPassportStore` singleton. The
store is append-only — there is no update or delete path. When no
database URL is configured the store falls back to an in-memory SQLite
engine so tests and local development work without a live database.

Path / backend selection:
  * ``DEALIX_DECISION_PASSPORT_DB_URL`` — explicit SQLAlchemy sync URL.
  * otherwise the app database URL (via ``core.config.settings``).
  * otherwise ``sqlite:///:memory:``.
"""
from __future__ import annotations

import logging
import os

from auto_client_acquisition.decision_passport.passport_postgres import (
    PassportPersistenceError,
    PostgresPassportStore,
)

_LOG = logging.getLogger(__name__)

_DEFAULT_STORE: PostgresPassportStore | None = None


def _store_url() -> str:
    explicit = os.getenv("DEALIX_DECISION_PASSPORT_DB_URL")
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


def get_default_passport_store() -> PostgresPassportStore:
    """Return the process-scoped Decision Passport store singleton."""
    global _DEFAULT_STORE
    if _DEFAULT_STORE is None:
        url = _store_url()
        try:
            _DEFAULT_STORE = PostgresPassportStore(
                database_url=url,
                create_tables=_should_autocreate(url),
            )
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("decision_passport_store_unavailable:%s", type(exc).__name__)
            _DEFAULT_STORE = PostgresPassportStore(
                database_url="sqlite:///:memory:", create_tables=True
            )
    return _DEFAULT_STORE


def reset_default_passport_store() -> None:
    """Test helper: drop the cached singleton."""
    global _DEFAULT_STORE
    _DEFAULT_STORE = None


__all__ = [
    "PassportPersistenceError",
    "get_default_passport_store",
    "reset_default_passport_store",
]
