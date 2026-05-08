"""
FastAPI middleware — request ID, structured logging, timing, security headers,
ETag caching, rate-limit headers, and audit logging for PDPL Article 18 compliance.
وسيط FastAPI — معرّف الطلب، التسجيل المنظم، التوقيت، ترويسات الأمان،
تخزين ETag مؤقت، ترويسات تحديد المعدل، وتسجيل البيانات الشخصية (PDPL).
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
# Requests to these paths are flagged as personal-data access events
# and written to the audit log in addition to the normal access log.
# المسارات التي تتضمن وصولاً إلى بيانات شخصية — تُسجَّل في سجل المراجعة.
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
    """
    Inject enterprise-grade HTTP security headers on every response.
    تضمين ترويسات أمان HTTP على كل استجابة.

    Covers:
      - Strict-Transport-Security (HSTS)
      - X-Content-Type-Options (nosniff)
      - X-Frame-Options (DENY — prevents clickjacking)
      - Referrer-Policy (strict-origin-when-cross-origin)
      - Permissions-Policy (disable dangerous browser features)
      - Content-Security-Policy (restrictive default for API)
      - X-XSS-Protection (legacy browsers)
    """

    # Content-Security-Policy suited for a pure API (no inline scripts/styles).
    # Frontend apps should override via their own CDN/reverse proxy.
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

        # HSTS — 1 year, include subdomains, allow preload
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains; preload",
        )
        # Prevent MIME-type sniffing
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        # Deny framing (clickjacking protection)
        response.headers.setdefault("X-Frame-Options", "DENY")
        # Referrer policy
        response.headers.setdefault(
            "Referrer-Policy", "strict-origin-when-cross-origin"
        )
        # Permissions Policy
        response.headers.setdefault("Permissions-Policy", self._PERMISSIONS)
        # CSP — tight default for API service
        response.headers.setdefault("Content-Security-Policy", self._CSP)
        # Legacy XSS protection
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        # Remove server fingerprinting
        for _key in ("server", "Server"):
            if _key in response.headers:
                del response.headers[_key]

        return response


class AuditLogMiddleware(BaseHTTPMiddleware):
    """
    PDPL Article 18 — Audit log for personal data access.
    نظام حماية البيانات الشخصية، المادة 18 — سجل مراجعة الوصول إلى البيانات.

    Writes a structured audit event for every request that touches a
    personal-data path. Fields captured:
      - event:        "personal_data_access"
      - request_id:   X-Request-ID propagated by RequestIDMiddleware
      - method:       HTTP verb
      - path:         URL path (no query string — avoids logging PII in params)
      - tenant_id:    First 16 chars of X-API-Key (tenant identifier)
      - client_ip:    Originating IP address
      - user_agent:   User-Agent header (truncated to 256 chars)
      - status_code:  HTTP response status
      - duration_ms:  Request processing time

    These events are written via structlog to the configured log sink
    (stdout JSON in production). A SIEM / log aggregator should index
    on audit_event=True for compliance queries.

    Note: For long-term immutable storage, route the structured logs to
    an append-only sink (e.g. CloudWatch, GCS, S3) and separately write
    to the db.models.AuditLogRecord table from sensitive endpoint handlers
    where full before/after diffs are available.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path

        # Only audit personal-data paths — skip health checks, docs, etc.
        is_personal_data_path = path.startswith(_PERSONAL_DATA_PREFIXES)

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        if is_personal_data_path:
            api_key = request.headers.get("X-API-Key", "")
            # Use only a prefix of the key as tenant identifier — avoids
            # storing credential material in logs.
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


# ── ETag / Last-Modified caching ──────────────────────────────────

class ETagMiddleware(BaseHTTPMiddleware):
    """
    Add ETag + Last-Modified headers to GET responses and honour
    If-None-Match / If-Modified-Since conditional requests.
    إضافة ترويسات ETag وLast-Modified، والاستجابة للطلبات الشرطية.

    Strategy:
      • ETag = MD5 of response body (weak — regenerated each time, no DB).
      • Last-Modified = current time when headers are written.
      • 304 Not Modified is returned when If-None-Match matches the ETag.
      • Only active for GET/HEAD requests with 2xx JSON responses.
    """

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

        # Only cache-tag successful JSON responses
        content_type = response.headers.get("content-type", "")
        if response.status_code < 200 or response.status_code >= 300 or "json" not in content_type:
            return response

        # Read body to compute ETag
        body = b""
        async for chunk in response.body_iterator:  # type: ignore[attr-defined]
            body += chunk if isinstance(chunk, bytes) else chunk.encode()

        etag = f'"{hashlib.md5(body, usedforsecurity=False).hexdigest()}"'  # noqa: S324
        response.headers["ETag"] = etag
        response.headers.setdefault(
            "Last-Modified",
            time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
        )
        response.headers.setdefault("Cache-Control", "no-cache")

        # Return 304 if ETag matches
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
    """
    Inject X-RateLimit-* and Retry-After headers on every response.
    حقن ترويسات X-RateLimit-* وRetry-After في كل استجابة.

    These are informational headers indicating the global rate limit window.
    Actual enforcement is handled by slowapi (SlowAPIMiddleware).
    Headers added:
      X-RateLimit-Limit     — max requests per window (from RL_GLOBAL env)
      X-RateLimit-Remaining — 429 responses get 0; others reflect approx state
      X-RateLimit-Reset     — unix epoch when the window resets (~+60s)
      Retry-After           — seconds to wait (only on 429 responses)
    """

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
