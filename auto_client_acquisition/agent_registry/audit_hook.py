"""Audit hook for the Agent Registry.

Every registry mutation (register / disable) and every agent run check
writes one row to :class:`db.models.AuditLogRecord` — doctrine #9: no
agent action without an audit trail. No PII is written: the diff carries
only the agent name, owner and scope summary.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from db.models import AuditLogRecord

_LOG = logging.getLogger(__name__)


def emit_audit(
    *,
    engine: Engine,
    action: str,
    agent_name: str,
    tenant_id: str = "system",
    detail: dict[str, object] | None = None,
) -> str:
    """Write one audit-log row for an agent-registry action. Returns the row id.

    ``action`` example: ``agent_registry.register``, ``agent_registry.disable``,
    ``agent_registry.run_check``.
    """
    row_id = f"aud_{uuid4().hex[:20]}"
    row = AuditLogRecord(
        id=row_id,
        tenant_id=tenant_id,
        user_id=None,
        action=action,
        entity_type="agent_registry",
        entity_id=agent_name,
        diff=dict(detail or {}),
        status="ok",
        created_at=datetime.now(UTC),
    )
    maker = sessionmaker(engine, expire_on_commit=False, future=True)
    session: Session
    try:
        with maker() as session:
            session.add(row)
            session.commit()
    except Exception as exc:  # noqa: BLE001 — audit failure must not block governance
        _LOG.warning("agent_registry_audit_failed:%s", type(exc).__name__)
    return row_id


__all__ = ["emit_audit"]
