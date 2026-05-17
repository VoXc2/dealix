"""
API key authentication middleware and dependency.
وسيط مصادقة مفتاح API.

Policy:
  * Requests to /health* and /docs*, /openapi.json, / are public.
  * Webhook endpoints use webhook signatures (see webhook_signatures.py).
  * All other /api/* endpoints require a valid X-API-Key header
    that matches one of the secrets in settings.api_keys (comma separated).
  * Admin endpoints (/api/v1/admin/*) additionally require a valid
    X-Admin-API-Key header from the ADMIN_API_KEYS env var.
    مسارات الإدارة تتطلب مفتاح X-Admin-API-Key منفصل.
"""

from __future__ import annotations

import hmac
import os
from collections.abc import Awaitable, Callable, Iterable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

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
    # Public pricing list — prospects need to see plans without an API key.
    # Checkout + plan-specific tampering protection stays on /api/v1/checkout.
    "/api/v1/pricing/plans",
}
PUBLIC_PREFIXES: tuple[str, ...] = (
    "/docs",
    "/redoc",
    "/static",
    "/api/v1/webhooks/",  # webhooks use signatures instead
    "/api/v1/public/",   # public landing endpoints (demo-request, health)
    "/api/v1/auth/",     # auth endpoints use JWT — no API key required
    "/api/v1/affiliates/",  # partner-facing endpoints; admin routes here
                            # self-gate with require_admin_key at route level
)

# FastAPI security scheme header (for OpenAPI schema generation)
_admin_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


def _configured_keys() -> list[str]:
    raw = os.getenv("API_KEYS", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


def _configured_admin_keys() -> list[str]:
    """Return the list of valid admin API keys from ADMIN_API_KEYS env var."""
    raw = os.getenv("ADMIN_API_KEYS", "")
    return [k.strip() for k in raw.split(",") if k.strip()]


def verify_api_key(key: str | None, allowed: Iterable[str] | None = None) -> bool:
    if not key:
        return False
    allowed_keys = list(allowed) if allowed is not None else _configured_keys()
    if not allowed_keys:
        # No keys configured → allow (dev mode). Production MUST set API_KEYS.
        return True
    return any(hmac.compare_digest(k, key) for k in allowed_keys)


def verify_admin_key(key: str | None) -> bool:
    """Constant-time comparison against ADMIN_API_KEYS.
    Returns True in dev mode (no admin keys configured).
    تحقق ثابت الوقت من مفتاح الإدارة.
    """
    if not key:
        return False
    admin_keys = _configured_admin_keys()
    if not admin_keys:
        # No admin keys configured → allow (dev mode).
        return True
    return any(hmac.compare_digest(k, key) for k in admin_keys)


async def require_admin_key(
    request: Request,
    admin_key: str | None = Depends(_admin_key_header),
) -> None:
    """
    FastAPI dependency — enforce X-Admin-API-Key on admin routes.
    Raises HTTP 403 if the key is invalid or missing in production.
    تبعية FastAPI: تفرض مفتاح X-Admin-API-Key على مسارات الإدارة.
    """
    if not verify_admin_key(admin_key):
        logger.warning(
            "admin_key_invalid",
            path=request.url.path,
            has_key=bool(admin_key),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing X-Admin-API-Key",
        )


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
            # Return a proper JSONResponse instead of raising HTTPException —
            # BaseHTTPMiddleware does not route exceptions through FastAPI's
            # exception handlers, so raising here produces a bare 500 at the
            # edge. Returning a Response gives clients a clean 401.
            return JSONResponse(
                {"detail": "Invalid or missing X-API-Key"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return await call_next(request)
