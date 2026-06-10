"""
IP allowlisting middleware for enterprise network-level access control.
وسيط قائمة السماح لعناوين IP للتحكم في الوصول على مستوى الشبكة للمؤسسات.

Enforces tenant-scoped IP allowlists. Requests from non-allowlisted IPs
are rejected with 403 before reaching any route handler.
"""

from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass, field
from typing import Any

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class AllowlistEntry:
    cidr: str
    network: ipaddress.IPv4Network | ipaddress.IPv6Network
    description: str = ""
    created_at: str = ""


class IPAllowlistMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware that enforces IP allowlisting per tenant.

    Each tenant can have a set of allowed CIDR ranges.
    Requests from IPs outside the allowlist receive 403 Forbidden.

    Bypass: trusted networks (internal), health checks, and super admin
    can be exempted via configuration.
    """

    def __init__(
        self,
        app: Any,
        global_allowlist: list[str] | None = None,
        trusted_proxies: list[str] | None = None,
    ) -> None:
        super().__init__(app)
        self._tenant_allowlists: dict[str, list[AllowlistEntry]] = {}
        # Global allowlist bypasses all tenant checks (monitoring, health checks)
        self._global_allowlist = [
            AllowlistEntry(
                cidr=cidr,
                network=ipaddress.ip_network(cidr, strict=False),
                description="global_allowlist",
            )
            for cidr in (global_allowlist or os.getenv("GLOBAL_IP_ALLOWLIST", "").split(",") if os.getenv("GLOBAL_IP_ALLOWLIST") else [])
            if cidr.strip()
        ]
        # Trusted proxies — extract real client IP from X-Forwarded-For
        self._trusted_proxies = set(
            trusted_proxies or os.getenv("TRUSTED_PROXIES", "127.0.0.1,::1").split(",")
        )
        self._exempt_paths = {
            "/health",
            "/ready",
            "/metrics",
            "/api/v1/health",
            "/docs",
            "/openapi.json",
        }
        self._enabled = os.getenv("IP_ALLOWLIST_ENABLED", "false").lower() == "true"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Check IP allowlisting before processing the request."""
        if not self._enabled:
            return await call_next(request)

        # Skip exempt paths
        if request.url.path in self._exempt_paths:
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        if not client_ip:
            return await call_next(request)

        # Check global allowlist first
        if self._is_in_global_allowlist(client_ip):
            return await call_next(request)

        # Check tenant allowlist
        tenant_id = request.state.tenant_context.tenant_id if hasattr(request.state, "tenant_context") else ""
        if tenant_id:
            if self._is_ip_allowed(client_ip, tenant_id):
                return await call_next(request)
        else:
            # No tenant context — only allow if global allowlist matches
            log.warning("ip_allowlist_no_tenant", ip=client_ip, path=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: no tenant context and IP not in global allowlist",
            )

        log.warning("ip_allowlist_blocked", ip=client_ip, tenant_id=tenant_id, path=request.url.path)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: IP not in tenant allowlist",
        )

    async def check_ip(self, ip: str, tenant_id: str) -> bool:
        """Check if an IP is allowed for a tenant."""
        return self._is_ip_allowed(ip, tenant_id)

    async def add_to_allowlist(self, tenant_id: str, cidr: str, description: str = "") -> None:
        """Add a CIDR range to a tenant's allowlist."""
        if tenant_id not in self._tenant_allowlists:
            self._tenant_allowlists[tenant_id] = []

        entry = AllowlistEntry(
            cidr=cidr,
            network=ipaddress.ip_network(cidr, strict=False),
            description=description,
        )
        self._tenant_allowlists[tenant_id].append(entry)
        log.info("ip_allowlist_added", tenant_id=tenant_id, cidr=cidr)

    async def remove_from_allowlist(self, tenant_id: str, cidr: str) -> None:
        """Remove a CIDR range from a tenant's allowlist."""
        if tenant_id not in self._tenant_allowlists:
            return

        original_count = len(self._tenant_allowlists[tenant_id])
        self._tenant_allowlists[tenant_id] = [
            e for e in self._tenant_allowlists[tenant_id] if e.cidr != cidr
        ]

        if len(self._tenant_allowlists[tenant_id]) < original_count:
            log.info("ip_allowlist_removed", tenant_id=tenant_id, cidr=cidr)

    async def get_allowlist(self, tenant_id: str) -> list[str]:
        """Get all allowlisted CIDRs for a tenant."""
        entries = self._tenant_allowlists.get(tenant_id, [])
        return [e.cidr for e in entries]

    def _get_client_ip(self, request: Request) -> str | None:
        """Extract the real client IP from request headers or direct connection."""
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            ips = [ip.strip() for ip in forwarded.split(",")]
            real_ips = [ip for ip in ips if ip not in self._trusted_proxies]
            if real_ips:
                return real_ips[0]

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        client = request.client
        if client:
            return client.host

        return None

    def _is_in_global_allowlist(self, ip: str) -> bool:
        """Check if IP is in the global allowlist."""
        try:
            addr = ipaddress.ip_address(ip)
            return any(addr in entry.network for entry in self._global_allowlist)
        except ValueError:
            return False

    def _is_ip_allowed(self, ip: str, tenant_id: str) -> bool:
        """Check if IP is allowed for a specific tenant."""
        entries = self._tenant_allowlists.get(tenant_id, [])
        if not entries:
            return True

        try:
            addr = ipaddress.ip_address(ip)
            return any(addr in entry.network for entry in entries)
        except ValueError:
            return False
