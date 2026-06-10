"""
Privileged access audit trail middleware.
وسيط سجل تدقيق الوصول المميز.

Records all privileged actions (super admin, tenant admin, system operations)
to an immutable audit log for compliance with PDPL Article 18,
NCA ECC-11 (Operations), and SOC 2 Type II requirements.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class AuditEntry:
    id: str
    admin_id: str
    admin_email: str
    admin_role: str
    tenant_id: str | None
    action: str
    resource: str
    resource_id: str | None
    detail: dict[str, Any]
    ip_address: str | None
    user_agent: str | None
    request_id: str | None
    status: str  # success / denied / error
    created_at: str


class PrivilegedAuditMiddleware(BaseHTTPMiddleware):
    """Middleware that audit-logs all privileged access.

    Captures every request to /admin/, /api/v1/admin/,
    and any request by a super_admin or tenant_admin.
    """

    def __init__(self, app: Any) -> None:
        super().__init__(app)
        # In-memory audit store (in production, use PostgreSQL + read replicas)
        self._audit_log: list[AuditEntry] = []
        self._max_entries = 100_000
        self._exempt_paths = {
            "/health",
            "/ready",
            "/metrics",
        }

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Inspect and audit privileged requests."""
        if request.url.path in self._exempt_paths:
            return await call_next(request)

        # Determine if this is a privileged request
        is_admin_path = request.url.path.startswith("/admin") or request.url.path.startswith("/api/v1/admin")
        user = getattr(request.state, "user", None)
        is_privileged = is_admin_path

        if user and hasattr(user, "system_role"):
            is_privileged = is_privileged or user.system_role == "super_admin"
        if user and hasattr(user, "role"):
            is_privileged = is_privileged or getattr(user, "role", "") == "tenant_admin"

        if not is_privileged:
            return await call_next(request)

        # Extract audit context before processing
        admin_id = getattr(user, "id", "unknown") if user else "unknown"
        admin_email = getattr(user, "email", "unknown") if user else "unknown"
        admin_role = getattr(user, "system_role", getattr(user, "role", "unknown")) if user else "unknown"
        tenant_id = getattr(request.state, "tenant_context", None)
        tenant_id = getattr(tenant_id, "tenant_id", None) if tenant_id else None
        ip = self._get_client_ip(request)
        ua = request.headers.get("User-Agent", "")
        request_id = getattr(request.state, "request_id", str(uuid.uuid4().hex[:12]))

        # Process the request
        start_time = datetime.now(UTC)
        try:
            response = await call_next(request)
            status = "success" if response.status_code < 400 else "denied" if response.status_code == 403 else "error"
        except Exception as exc:
            status = "error"
            detail = {"error": str(exc)[:500]}
            self._record_entry(
                admin_id=admin_id,
                admin_email=admin_email,
                admin_role=admin_role,
                tenant_id=tenant_id,
                action=f"{request.method}_{status}",
                resource=request.url.path,
                resource_id=request.path_params.get("id") if hasattr(request, "path_params") else None,
                detail=detail,
                ip_address=ip,
                user_agent=ua,
                request_id=request_id,
                status=status,
            )
            raise

        duration_ms = int((datetime.now(UTC) - start_time).total_seconds() * 1000)

        detail: dict[str, Any] = {
            "method": request.method,
            "path": request.url.path,
            "query": str(request.url.query),
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }

        # Include request body for mutations (sanitized)
        if request.method in ("POST", "PUT", "PATCH"):
            detail["has_body"] = True

        self._record_entry(
            admin_id=admin_id,
            admin_email=admin_email,
            admin_role=admin_role,
            tenant_id=tenant_id,
            action=f"{request.method}_{request.url.path.split('/')[-1]}",
            resource=request.url.path,
            resource_id=request.path_params.get("id") if hasattr(request, "path_params") else None,
            detail=detail,
            ip_address=ip,
            user_agent=ua,
            request_id=request_id,
            status=status,
        )

        return response

    async def log_access(
        self,
        admin_id: str,
        action: str,
        resource: str,
        detail: dict[str, Any],
        admin_email: str = "",
        admin_role: str = "",
        tenant_id: str | None = None,
        ip_address: str | None = None,
    ) -> None:
        """Programmatic audit log entry for background privileged operations."""
        self._record_entry(
            admin_id=admin_id,
            admin_email=admin_email,
            admin_role=admin_role,
            tenant_id=tenant_id,
            action=action,
            resource=resource,
            resource_id=detail.get("resource_id") if isinstance(detail, dict) else None,
            detail=detail,
            ip_address=ip_address,
            user_agent="background_job",
            request_id=str(uuid.uuid4().hex[:12]),
            status="success",
        )

    async def get_audit_log(
        self,
        days: int = 90,
        admin_id: str | None = None,
        action: str | None = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> list[AuditEntry]:
        """Retrieve audit log entries with optional filters.

        In production, this queries the audit_logs table.
        """
        cutoff = datetime.now(UTC) - timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        filtered = [e for e in self._audit_log if e.created_at >= cutoff_str]

        if admin_id:
            filtered = [e for e in filtered if e.admin_id == admin_id]
        if action:
            filtered = [e for e in filtered if e.action == action]

        filtered.sort(key=lambda e: e.created_at, reverse=True)
        return filtered[offset : offset + limit]

    def _record_entry(self, **kwargs: Any) -> None:
        """Create and store an audit entry."""
        entry = AuditEntry(
            id=str(uuid.uuid4()),
            admin_id=kwargs["admin_id"],
            admin_email=kwargs.get("admin_email", ""),
            admin_role=kwargs.get("admin_role", ""),
            tenant_id=kwargs.get("tenant_id"),
            action=kwargs["action"],
            resource=kwargs["resource"],
            resource_id=kwargs.get("resource_id"),
            detail=kwargs.get("detail", {}),
            ip_address=kwargs.get("ip_address"),
            user_agent=kwargs.get("user_agent"),
            request_id=kwargs.get("request_id"),
            status=kwargs.get("status", "success"),
            created_at=datetime.now(UTC).isoformat(),
        )
        self._audit_log.append(entry)

        log.info(
            "privileged_audit",
            admin_id=entry.admin_id,
            action=entry.action,
            resource=entry.resource,
            status=entry.status,
        )

        if len(self._audit_log) > self._max_entries:
            self._audit_log = self._audit_log[-self._max_entries:]

    @staticmethod
    def _get_client_ip(request: Request) -> str | None:
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        client = request.client
        return client.host if client else None

    async def export_audit_log(self, days: int = 90) -> str:
        """Export audit log as JSON for compliance reporting."""
        entries = await self.get_audit_log(days=days, limit=self._max_entries)
        return json.dumps([e.__dict__ for e in entries], indent=2, ensure_ascii=False)
