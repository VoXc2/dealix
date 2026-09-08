"""
Rate limiting via slowapi.
تحديد المعدل عبر slowapi.

Default policy (per route):
  POST /api/v1/leads          → 10/min
  POST /api/v1/sales/*        → 30/min
  POST /api/v1/webhooks/wa    → 100/min
  Other API routes            → 60/min
  Global (per key/IP)         → 1000/min

Per-tenant isolation:
  Authenticated requests bucket by the first 16 chars of X-API-Key.
  Unauthenticated requests bucket by client IP.
  The "moving-window" strategy smooths burst traffic better than fixed-window.

Storage:
  Defaults to memory:// (single-process). For multi-worker production set
  RL_STORAGE_URI=redis://:<password>@host:6379/1 (separate DB from main Redis).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.config.settings import get_settings

# Patch Starlette's Config reader so .env files are read as UTF-8 on Windows.
# Keep the signature compatible with modern Starlette, which passes an
# explicit encoding argument to Config._read_file().
try:
    from starlette import config as _starlette_config

    _original_read_file = _starlette_config.Config._read_file

    def _read_file_utf8(
        self,
        file_name: str | Path,
        encoding: str | None = None,
    ) -> dict[str, str]:
        file_values: dict[str, str] = {}
        with open(file_name, encoding=encoding or "utf-8") as input_file:
            for line in input_file.readlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    file_values[key] = value
        return file_values

    _starlette_config.Config._read_file = _read_file_utf8
except Exception:  # pragma: no cover
    pass

try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from slowapi.middleware import SlowAPIMiddleware
    from slowapi.util import get_remote_address

    _HAS_SLOWAPI = True
except ImportError:  # pragma: no cover
    _HAS_SLOWAPI = False
    Limiter = None  # type: ignore
    RateLimitExceeded = Exception  # type: ignore


# ── Bucket key: per-API-key (tenant isolation) or per-IP ────────

def _key_func(request: Request) -> str:
    """
    Primary bucket = first 16 chars of X-API-Key (per-tenant).
    Fallback bucket = client IP address (unauthenticated callers).

    Using a prefix keeps key material out of logs while still giving
    each tenant an isolated counter.
    مفتاح الحاوية: مفتاح API أو عنوان IP.
    """
    key = request.headers.get("X-API-Key", "").strip()
    if key:
        # Truncate to 16 chars — enough for uniqueness, avoids storing full key
        return f"tenant:{key[:16]}"
    if _HAS_SLOWAPI:
        ip = get_remote_address(request)
    else:
        ip = request.client.host if request.client else "anon"
    return f"ip:{ip}"


def _admin_key_func(request: Request) -> str:
    """Separate bucket for admin endpoints — stricter limit."""
    key = request.headers.get("X-Admin-API-Key", "").strip()
    if key:
        return f"admin:{key[:16]}"
    return _key_func(request)


# ── Configurable limits ──────────────────────────────────────────

DEFAULT_GLOBAL_LIMIT = os.getenv("RL_GLOBAL", "1000/minute")
DEFAULT_ADMIN_LIMIT = os.getenv("RL_ADMIN", "120/minute")

limiter: Any = None
admin_limiter: Any = None

if _HAS_SLOWAPI:
    _storage_uri = os.getenv("RL_STORAGE_URI", "memory://")

    limiter = Limiter(
        key_func=_key_func,
        default_limits=[DEFAULT_GLOBAL_LIMIT],
        storage_uri=_storage_uri,
        # moving-window smooths bursty traffic; fixed-window would allow a
        # full burst at the boundary of each window.
        strategy="moving-window",
    )

    admin_limiter = Limiter(
        key_func=_admin_key_func,
        default_limits=[DEFAULT_ADMIN_LIMIT],
        storage_uri=_storage_uri,
        strategy="moving-window",
    )


# Per-route limits (applied via decorators in routers)
LIMITS = {
    "leads_create": os.getenv("RL_LEADS", "10/minute"),
    "sales_any": os.getenv("RL_SALES", "30/minute"),
    "whatsapp_webhook": os.getenv("RL_WA_WEBHOOK", "100/minute"),
    "generic_api": os.getenv("RL_GENERIC", "60/minute"),
    "admin_any": os.getenv("RL_ADMIN", "120/minute"),
}


def setup_rate_limit(app: FastAPI) -> None:
    """Wire slowapi into the FastAPI app.

    Missing slowapi is tolerated in dev/test and refused in production.

    The silent no-op it replaces was the dangerous half of a pair:
    ``RateLimitHeadersMiddleware`` advertises ``X-RateLimit-*`` on every
    response and defers enforcement to this function, so a deployment without
    slowapi served rate-limit headers that nothing honoured — while
    ``/api/v1/auth/login`` sits behind ``PUBLIC_PREFIXES`` and skips the API
    key middleware entirely. An unthrottled login endpoint that announces a
    throttle is worse than one that announces nothing.

    slowapi is pinned in ``requirements.txt``, so this should be unreachable
    in production; raising is how it stays that way, matching
    ``api/main.py:_validate_production_secrets``, which also refuses to start
    rather than run insecure.
    """
    if not _HAS_SLOWAPI or limiter is None:
        # Use the canonical Settings aliases (APP_ENV, ENVIRONMENT,
        # VERCEL_ENV). Reading APP_ENV directly would fail open on Railway or
        # Vercel deployments that set only their platform-standard alias.
        if get_settings().is_production:
            raise RuntimeError(
                "SECURITY: slowapi is not installed, so no rate limiting is "
                "enforced while X-RateLimit-* headers claim otherwise. "
                "/api/v1/auth/login is public and would be unthrottled. "
                "Install slowapi (it is pinned in requirements.txt)."
            )
        return

    app.state.limiter = limiter

    async def _rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
        return JSONResponse(
            status_code=429,
            content={
                "error": "RateLimitExceeded",
                "detail": f"Too many requests: {exc.detail}",
                "ar": "تجاوزت الحد المسموح، يرجى المحاولة لاحقاً.",
            },
            headers={"Retry-After": "60"},
        )

    app.add_exception_handler(RateLimitExceeded, _rate_limit_handler)
    app.add_middleware(SlowAPIMiddleware)
