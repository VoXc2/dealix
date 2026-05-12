"""
Audit writer helper — every mutation in T0+ routers writes an
`AuditLogRecord` row through this single funnel. Centralising the call
means the schema (`entity_type`, `entity_id`, `action`, `diff`, `status`)
is consistent everywhere and the founder / DPO / auditor has one shape
to query.

Public surface:
    await audit(
        db, action="invite_user", entity_type="user", entity_id=user.id,
        tenant_id=tenant_id, user_id=actor_id, diff={"email": "..."}
    )

Failures during audit-write are logged but never raised — auditing is
a side-effect that must not 5xx a customer mutation.
"""

from __future__ import annotations

import secrets
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from db.models import AuditLogRecord

log = get_logger(__name__)


async def audit(
    db: AsyncSession,
    *,
    action: str,
    entity_type: str,
    entity_id: str | None,
    tenant_id: str,
    user_id: str | None = None,
    status: str = "ok",
    diff: dict[str, Any] | None = None,
    request_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> str | None:
    """Persist an AuditLogRecord row; return its id or None on failure."""
    row_id = "aud_" + secrets.token_hex(12)
    row = AuditLogRecord(
        id=row_id,
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip_address=ip_address,
        user_agent=user_agent,
        request_id=request_id,
        diff=diff,
        status=status,
    )
    db.add(row)
    try:
        await db.commit()
        return row_id
    except SQLAlchemyError:
        await db.rollback()
        log.exception(
            "audit_write_failed",
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            tenant_id=tenant_id,
        )
        return None
