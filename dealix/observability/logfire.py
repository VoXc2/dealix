"""
Pydantic Logfire — structured logs + spans. We ship a `setup_logfire()`
that adapts our structlog setup to Logfire's transport when configured.
"""

from __future__ import annotations

import os

from core.logging import get_logger

log = get_logger(__name__)


def is_configured() -> bool:
    return bool(os.getenv("LOGFIRE_TOKEN", "").strip())


def setup_logfire() -> bool:
    if not is_configured():
        return False
    try:
        import logfire  # type: ignore

        logfire.configure(
            token=os.getenv("LOGFIRE_TOKEN", "").strip(),
            service_name=os.getenv("LOGFIRE_SERVICE", "dealix-api"),
            service_version=os.getenv("APP_VERSION", "3.3.0"),
        )
        # Auto-instrument popular libraries when present.
        try:
            logfire.instrument_pydantic()
        except Exception:
            pass
        try:
            logfire.instrument_httpx()
        except Exception:
            pass
        try:
            logfire.instrument_sqlalchemy()
        except Exception:
            pass
        log.info("logfire_configured")
        return True
    except ImportError:
        log.info("logfire_sdk_not_installed")
        return False
