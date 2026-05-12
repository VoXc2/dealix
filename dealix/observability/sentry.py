"""
Sentry error reporting — captures unhandled exceptions + performance traces.
تقارير الأخطاء عبر Sentry.

PII scrubbing rules (PDPL-aligned):
- Auth/cookie/API-key headers stripped
- Query strings on /admin/* and /auth/* paths replaced with <redacted>
- Request bodies on /checkout and /webhooks/* paths replaced with <redacted>
- Events originating in tests/ paths are dropped entirely
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any

log = logging.getLogger(__name__)


_SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-admin-api-key",
    "x-moyasar-signature",
    "x-hub-signature",
    "x-hub-signature-256",
    "x-calendly-webhook-signature",
}

_SENSITIVE_PATH_PREFIXES = (
    "/api/v1/admin",
    "/api/v1/auth",
    "/api/v1/webhooks",
    "/api/v1/checkout",
)

# Field names whose values must never be sent to Sentry, regardless of location.
_SENSITIVE_FIELD_NAMES = {
    "password", "passwd", "secret", "token", "api_key", "apikey",
    "access_token", "refresh_token", "authorization",
    "national_id", "iqama", "iban", "card_number", "cvv", "cvc",
    "ssn", "email", "phone", "mobile", "phone_number",
}

_REDACTED = "<redacted>"


def _scrub_headers(headers: Any) -> Any:
    if not isinstance(headers, dict):
        return headers
    return {
        k: (_REDACTED if k.lower() in _SENSITIVE_HEADERS else v)
        for k, v in headers.items()
    }


def _scrub_mapping(obj: Any) -> Any:
    """Recursively redact values whose key is in _SENSITIVE_FIELD_NAMES."""
    if isinstance(obj, dict):
        return {
            k: (_REDACTED if isinstance(k, str) and k.lower() in _SENSITIVE_FIELD_NAMES
                else _scrub_mapping(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_scrub_mapping(item) for item in obj]
    return obj


def _path_is_sensitive(path: str) -> bool:
    return any(path.startswith(p) for p in _SENSITIVE_PATH_PREFIXES)


def _scrub_event(event: dict[str, Any], _hint: dict[str, Any]) -> dict[str, Any] | None:
    """before_send hook — applied to every Sentry event before transmission."""
    # Drop events from test runs entirely
    culprit = event.get("culprit") or ""
    if "tests/" in culprit or "/test_" in culprit:
        return None

    request = event.get("request") or {}
    url = request.get("url") or ""
    path = ""
    try:
        from urllib.parse import urlparse
        path = urlparse(url).path or ""
    except Exception:
        path = ""

    # Strip auth/signature headers everywhere
    if request.get("headers"):
        request["headers"] = _scrub_headers(request["headers"])

    # On sensitive paths, blow away query string + body entirely
    if path and _path_is_sensitive(path):
        if "query_string" in request:
            request["query_string"] = _REDACTED
        if "data" in request:
            request["data"] = _REDACTED
        if "cookies" in request:
            request["cookies"] = _REDACTED

    # Deep-redact any obvious PII field in extras/contexts
    if "extra" in event:
        event["extra"] = _scrub_mapping(event["extra"])
    if "contexts" in event:
        event["contexts"] = _scrub_mapping(event["contexts"])

    event["request"] = request
    return event


def setup_sentry() -> None:
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        log.info("sentry_not_configured")
        return
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    except ImportError:
        log.warning("sentry_sdk not installed — skipping Sentry setup")
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=os.getenv("APP_ENV", "production"),
        release=os.getenv("APP_VERSION", "3.0.0"),
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
        profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.05")),
        send_default_pii=False,
        before_send=_scrub_event,
        integrations=[FastApiIntegration(), SqlalchemyIntegration()],
    )
    log.info("sentry_enabled", extra={"env": os.getenv("APP_ENV")})
