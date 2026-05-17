"""Default Risk Register accessor.

Resolves a process-scoped :class:`PostgresRiskRegister` singleton. Falls
back to an in-memory SQLite engine when no database URL is configured.
"""
from __future__ import annotations

import logging
import os

from auto_client_acquisition.risk_resilience_os.risk_postgres import (
    PostgresRiskRegister,
    RiskValidationError,
)

_LOG = logging.getLogger(__name__)

_DEFAULT_REGISTER: PostgresRiskRegister | None = None


def _register_url() -> str:
    explicit = os.getenv("DEALIX_RISK_REGISTER_DB_URL")
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


def get_default_risk_register() -> PostgresRiskRegister:
    """Return the process-scoped Risk Register singleton."""
    global _DEFAULT_REGISTER
    if _DEFAULT_REGISTER is None:
        url = _register_url()
        try:
            _DEFAULT_REGISTER = PostgresRiskRegister(
                database_url=url, create_tables=_should_autocreate(url)
            )
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("risk_register_unavailable:%s", type(exc).__name__)
            _DEFAULT_REGISTER = PostgresRiskRegister(
                database_url="sqlite:///:memory:", create_tables=True
            )
    return _DEFAULT_REGISTER


def reset_default_risk_register() -> None:
    """Test helper: drop the cached singleton."""
    global _DEFAULT_REGISTER
    _DEFAULT_REGISTER = None


__all__ = [
    "RiskValidationError",
    "get_default_risk_register",
    "reset_default_risk_register",
]
