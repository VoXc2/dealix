"""
Per-tenant IP allowlist middleware.

Reads `TenantRecord.meta_json.ip_allowlist` (a list of CIDRs) and 403s
calls from outside the list. Enabled per-tenant; tenants without an
allowlist are unaffected.

We do the tenant lookup at request boundary via `request.state.tenant_id`
(set by TenantIsolationMiddleware earlier in the stack), so this
middleware should be added AFTER tenant resolution.
"""

from __future__ import annotations

import ipaddress
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from core.logging import get_logger

log = get_logger(__name__)


def _client_ip(request: Request) -> str | None:
    # Respect X-Forwarded-For from the load balancer.
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


class IPAllowlistMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Any
    ) -> Response:
        # Skip for unauthenticated paths (public health, demo, etc.).
        if request.url.path.startswith("/api/v1/public/"):
            return await call_next(request)
        if request.url.path.startswith("/healthz") or request.url.path.startswith("/health"):
            return await call_next(request)
        # Allowlist lives in tenant.meta_json — we read lazily via the
        # caller's tenant_id when the rule was already attached upstream.
        allowlist = getattr(request.state, "ip_allowlist", None)
        if not allowlist:
            return await call_next(request)
        ip = _client_ip(request)
        if ip is None:
            log.warning("ip_allowlist_no_client_ip", path=request.url.path)
            return JSONResponse(
                status_code=403, content={"detail": "ip_unknown"}
            )
        try:
            client = ipaddress.ip_address(ip)
        except ValueError:
            return JSONResponse(
                status_code=403, content={"detail": "ip_invalid"}
            )
        for cidr in allowlist:
            try:
                if client in ipaddress.ip_network(cidr, strict=False):
                    return await call_next(request)
            except ValueError:
                continue
        log.warning(
            "ip_allowlist_denied",
            tenant_id=getattr(request.state, "tenant_id", None),
            ip=ip,
        )
        return JSONResponse(
            status_code=403,
            content={"detail": "ip_not_allowlisted", "allowed_cidrs": list(allowlist)},
        )
