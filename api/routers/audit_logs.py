"""
Customer-facing audit log — required for SOC2/ISO27001-curious buyers
and for the customer's own internal compliance reviews.

Endpoints:
    GET  /api/v1/audit-logs                    — list (paginated, filtered)
    GET  /api/v1/audit-logs/export.csv         — CSV stream of the same query

Scope: enforces `request.state.tenant_id` — a tenant never sees another
tenant's rows. Super-admin callers may pass `?tenant_id=...` to inspect a
specific tenant (used for support).

Reads from `db.models.AuditLogRecord` (already populated by
`api/middleware/http_stack.AuditLogMiddleware`).
"""

from __future__ import annotations

import csv
import io
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import AuditLogRecord
from db.session import get_db

router = APIRouter(prefix="/api/v1/audit-logs", tags=["audit-logs"])
log = get_logger(__name__)

_MAX_LIMIT = 500
_MAX_LOOKBACK = timedelta(days=365)


def _resolve_tenant(request: Request, override: str | None) -> str:
    is_super = bool(getattr(request.state, "is_super_admin", False))
    caller = getattr(request.state, "tenant_id", None)
    if is_super and override:
        return override
    if override and caller and override != caller:
        raise HTTPException(403, "cross_tenant_access_denied")
    if not caller and not override:
        raise HTTPException(401, "tenant_unresolved")
    return caller or override or ""


def _row_to_dict(r: AuditLogRecord) -> dict[str, Any]:
    return {
        "id": r.id,
        "tenant_id": r.tenant_id,
        "user_id": r.user_id,
        "action": r.action,
        "entity_type": r.entity_type,
        "entity_id": r.entity_id,
        "status": r.status,
        "ip_address": r.ip_address,
        "request_id": r.request_id,
        "diff": r.diff,
        "created_at": r.created_at.isoformat(),
    }


async def _query_rows(
    db: AsyncSession,
    tenant_id: str,
    since: datetime,
    until: datetime,
    action: str | None,
    entity_type: str | None,
    limit: int,
) -> list[AuditLogRecord]:
    clauses = [
        AuditLogRecord.tenant_id == tenant_id,
        AuditLogRecord.created_at >= since,
        AuditLogRecord.created_at <= until,
    ]
    if action:
        clauses.append(AuditLogRecord.action == action)
    if entity_type:
        clauses.append(AuditLogRecord.entity_type == entity_type)

    try:
        return (
            (
                await db.execute(
                    select(AuditLogRecord)
                    .where(and_(*clauses))
                    .order_by(AuditLogRecord.created_at.desc())
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )
    except SQLAlchemyError:
        log.exception("audit_log_query_failed", tenant_id=tenant_id)
        return []


@router.get("")
async def list_audit_logs(
    request: Request,
    tenant_id: str | None = Query(default=None, max_length=64),
    since: datetime | None = Query(default=None),
    until: datetime | None = Query(default=None),
    action: str | None = Query(default=None, max_length=64),
    entity_type: str | None = Query(default=None, max_length=64),
    limit: int = Query(default=200, ge=1, le=_MAX_LIMIT),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Paginated audit-log list scoped to caller's tenant."""
    tid = _resolve_tenant(request, tenant_id)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    until_ts = until.replace(tzinfo=None) if until else now
    since_ts = (
        since.replace(tzinfo=None) if since else (until_ts - timedelta(days=30))
    )
    if (until_ts - since_ts) > _MAX_LOOKBACK:
        raise HTTPException(422, "lookback_window_too_large")

    rows = await _query_rows(db, tid, since_ts, until_ts, action, entity_type, limit)
    return {
        "tenant_id": tid,
        "count": len(rows),
        "since": since_ts.isoformat(),
        "until": until_ts.isoformat(),
        "items": [_row_to_dict(r) for r in rows],
    }


def _csv_stream(rows: list[AuditLogRecord]):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        [
            "id",
            "tenant_id",
            "user_id",
            "action",
            "entity_type",
            "entity_id",
            "status",
            "ip_address",
            "request_id",
            "created_at",
        ]
    )
    yield buf.getvalue()
    buf.seek(0)
    buf.truncate()
    for r in rows:
        writer.writerow(
            [
                r.id,
                r.tenant_id,
                r.user_id or "",
                r.action,
                r.entity_type,
                r.entity_id or "",
                r.status,
                r.ip_address or "",
                r.request_id or "",
                r.created_at.isoformat(),
            ]
        )
        yield buf.getvalue()
        buf.seek(0)
        buf.truncate()


@router.get("/export.csv")
async def export_audit_logs_csv(
    request: Request,
    tenant_id: str | None = Query(default=None, max_length=64),
    since: datetime | None = Query(default=None),
    until: datetime | None = Query(default=None),
    action: str | None = Query(default=None, max_length=64),
    entity_type: str | None = Query(default=None, max_length=64),
    limit: int = Query(default=_MAX_LIMIT, ge=1, le=_MAX_LIMIT),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """CSV stream — same query shape as the JSON list endpoint."""
    tid = _resolve_tenant(request, tenant_id)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    until_ts = until.replace(tzinfo=None) if until else now
    since_ts = (
        since.replace(tzinfo=None) if since else (until_ts - timedelta(days=30))
    )
    rows = await _query_rows(db, tid, since_ts, until_ts, action, entity_type, limit)

    log.info(
        "audit_log_export",
        tenant_id=tid,
        rows=len(rows),
        since=since_ts.isoformat(),
        until=until_ts.isoformat(),
    )
    filename = f"dealix-audit-{tid}-{since_ts.date().isoformat()}_{until_ts.date().isoformat()}.csv"
    return StreamingResponse(
        _csv_stream(rows),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
