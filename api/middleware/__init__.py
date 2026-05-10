"""API middleware package exports.

Contains runtime FastAPI middleware classes used by ``api.main`` plus
tenant-isolation and BOPLA helpers from Wave 12.6.
"""

from __future__ import annotations

import hashlib
import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.logging import get_logger

logger = get_logger(__name__)

# ── Path prefixes that involve personal data (PDPL Article 18) ──
_PERSONAL_DATA_PREFIXES: tuple[str, ...] = (
    "/api/v1/leads",
    "/api/v1/contacts",
    "/api/v1/prospect",
    "/api/v1/customer",
    "/api/v1/crm",
    "/api/v1/outreach",
    "/api/v1/email",
    "/api/v1/whatsapp",
    "/api/v1/sales",
    "/api/v1/data",
    "/api/v1/admin",
    "/api/v1/agent",
    "/api/v1/delivery",
    "/api/v1/support",
    "/api/v1/finance",
)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to each request and bind it to logs."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception("request_unhandled_error", error=str(e))
            raise
        duration_ms = (time.perf_counter() - start) * 1000

        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Inject enterprise-grade HTTP security headers on every response."""

    _CSP = (
        "default-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'none'; "
        "base-uri 'none';"
    )

    _PERMISSIONS = (
        "camera=(), microphone=(), geolocation=(), "
        "payment=(), usb=(), magnetometer=()"
    )

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)

        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains; preload",
        )
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Referrer-Policy", "strict-origin-when-cross-origin"
        )
        response.headers.setdefault("Permissions-Policy", self._PERMISSIONS)
        response.headers.setdefault("Content-Security-Policy", self._CSP)
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        for key in ("server", "Server"):
            if key in response.headers:
                del response.headers[key]

        return response


class AuditLogMiddleware(BaseHTTPMiddleware):
    """PDPL Article 18 audit log for personal-data access paths."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path
        is_personal_data_path = path.startswith(_PERSONAL_DATA_PREFIXES)

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        if is_personal_data_path:
            api_key = request.headers.get("X-API-Key", "")
            tenant_id = api_key[:16] if api_key else "anonymous"
            client_ip = (
                request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
                or (request.client.host if request.client else "unknown")
            )
            user_agent = request.headers.get("User-Agent", "")[:256]

            logger.info(
                "personal_data_access",
                audit_event=True,
                request_id=request.headers.get("X-Request-ID", ""),
                method=request.method,
                path=path,
                tenant_id=tenant_id,
                client_ip=client_ip,
                user_agent=user_agent,
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

        return response


class ETagMiddleware(BaseHTTPMiddleware):
    """Add ETag + Last-Modified and honor conditional requests."""

    _CACHEABLE_METHODS = frozenset({"GET", "HEAD"})
    _SKIP_PATHS = frozenset({"/health", "/docs", "/redoc", "/openapi.json"})

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if (
            request.method not in self._CACHEABLE_METHODS
            or request.url.path in self._SKIP_PATHS
        ):
            return await call_next(request)

        response = await call_next(request)

        content_type = response.headers.get("content-type", "")
        if response.status_code < 200 or response.status_code >= 300 or "json" not in content_type:
            return response

        body = b""
        async for chunk in response.body_iterator:  # type: ignore[attr-defined]
            body += chunk if isinstance(chunk, bytes) else chunk.encode()

        etag = f'"{hashlib.md5(body, usedforsecurity=False).hexdigest()}"'
        response.headers["ETag"] = etag
        response.headers.setdefault(
            "Last-Modified",
            time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
        )
        response.headers.setdefault("Cache-Control", "no-cache")

        if_none_match = request.headers.get("If-None-Match", "")
        if if_none_match and etag in if_none_match:
            from starlette.responses import Response as StarletteResponse

            not_modified = StarletteResponse(status_code=304)
            not_modified.headers["ETag"] = etag
            return not_modified

        from starlette.responses import Response as StarletteResponse

        return StarletteResponse(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )


class RateLimitHeadersMiddleware(BaseHTTPMiddleware):
    """Inject informational X-RateLimit headers on every response."""

    import os as _os

    _GLOBAL_LIMIT: int = int(_os.getenv("RL_GLOBAL", "1000/minute").split("/")[0])
    _WINDOW_SECONDS: int = 60

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)

        now = int(time.time())
        reset_at = now - (now % self._WINDOW_SECONDS) + self._WINDOW_SECONDS

        limit = self._GLOBAL_LIMIT
        response.headers.setdefault("X-RateLimit-Limit", str(limit))
        response.headers.setdefault("X-RateLimit-Reset", str(reset_at))

        if response.status_code == 429:
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers.setdefault("Retry-After", str(self._WINDOW_SECONDS))
        else:
            response.headers.setdefault(
                "X-RateLimit-Remaining", str(int(limit * 0.8))
            )

        return response


from .bopla_redaction import (  # noqa: E402
    SENSITIVE_FIELD_CATEGORIES,
    RedactionResult,
    Role,
    assert_no_sensitive_field_in_response,
    fields_blocked_for_role,
    redact_dict_for_role,
)
from .tenant_isolation import (  # noqa: E402
    CrossTenantAccessDenied,
    TenantContext,
    assert_tenant_match,
    filter_tenant_scoped_list,
    resolve_tenant_context,
)

__all__ = [
    "SENSITIVE_FIELD_CATEGORIES",
    "AuditLogMiddleware",
    "CrossTenantAccessDenied",
    "ETagMiddleware",
    "RateLimitHeadersMiddleware",
    "RedactionResult",
    "RequestIDMiddleware",
    "Role",
    "SecurityHeadersMiddleware",
    "TenantContext",
    "assert_no_sensitive_field_in_response",
    "assert_tenant_match",
    "fields_blocked_for_role",
    "filter_tenant_scoped_list",
    "redact_dict_for_role",
    "resolve_tenant_context",
]
