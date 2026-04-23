"""
API key authentication middleware.
وسيط مصادقة مفتاح API.

Policy:
  * Requests to /health* and /docs*, /openapi.json, / are public.
  * Webhook endpoints use webhook signatures (see webhook_signatures.py).
  * All other /api/* endpoints require a valid X-API-Key header
    that matches one of the secrets in settings.api_keys (comma separated).
"""

from __future__ import annotations

import hmac
import os
from collections.abc import Awaitable, Callable, Iterable

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from core.logging import get_logger

logger = get_logger(__name__)

# Paths that are always public — no API key required
PUBLIC_PATHS: set[str] = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/health/live",
    "/health/ready",
    "/health/deep",
}
PUBLIC_PREFIXES: tuple[str, ...] = (
    "/docs",
    "/redoc",
    "/static",
    "/api/v1/webhooks/",  # webhooks use signatures instead
)


def _configured_keys() -> list[str]:
    raw = os.getenv("API_KEYS", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


def verify_api_key(key: str | None, allowed: Iterable[str] | None = None) -> bool:
    if not key:
        return False
    allowed_keys = list(allowed) if allowed is not None else _configured_keys()
    if not allowed_keys:
        # No keys configured → allow (dev mode). Production MUST set API_KEYS.
        return True
    return any(hmac.compare_digest(k, key) for k in allowed_keys)


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path
        if path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES):
            return await call_next(request)

        # Enforce key only when API_KEYS is configured
        allowed = _configured_keys()
        if not allowed:
            return await call_next(request)

        provided = request.headers.get("X-API-Key")
        if not verify_api_key(provided, allowed):
            logger.warning("api_key_invalid", path=path, has_key=bool(provided))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing X-API-Key",
            )

        return await call_next(request)
