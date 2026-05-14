"""Audit Export router — Wave 3 preview.

GET /api/v1/audit/{customer_id}            → JSON chain
GET /api/v1/audit/{customer_id}/markdown   → markdown chain (procurement)
POST /api/v1/audit/event                   → record an audit event

Admin-key gated for write; read is tenant-scoped via path.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


class _AuditEventBody(BaseModel):
    customer_id: str = Field(..., min_length=1)
    engagement_id: str = ""
    kind: str = "ai_run"
    actor: str = "system"
    source_refs: list[str] = Field(default_factory=list)
    output_refs: list[str] = Field(default_factory=list)
    decision: str = ""
    policy_checked: str = ""
    summary: str = ""


@router.post("/event", dependencies=[Depends(require_admin_key)])
async def record_audit(body: _AuditEventBody) -> dict[str, Any]:
    from auto_client_acquisition.auditability_os.audit_event import (
        AuditEventKind,
        record_event,
    )
    valid_kinds = {k.value for k in AuditEventKind}
    if body.kind not in valid_kinds:
        raise HTTPException(status_code=422, detail=f"invalid kind {body.kind!r}")
    event = record_event(
        customer_id=body.customer_id,
        engagement_id=body.engagement_id,
        kind=body.kind,
        actor=body.actor,
        source_refs=body.source_refs,
        output_refs=body.output_refs,
        decision=body.decision,
        policy_checked=body.policy_checked,
        summary=body.summary,
    )
    return {"event": event.to_dict(), "governance_decision": "allow"}


@router.get("/{customer_id}")
async def evidence_chain_json(
    customer_id: str,
    engagement_id: str = Query(""),
) -> dict[str, Any]:
    from auto_client_acquisition.auditability_os.evidence_chain import build_chain
    chain = build_chain(customer_id=customer_id, engagement_id=engagement_id)
    return chain.to_dict()


@router.get("/{customer_id}/markdown", response_class=PlainTextResponse)
async def evidence_chain_markdown(
    customer_id: str,
    engagement_id: str = Query(""),
) -> str:
    from auto_client_acquisition.auditability_os.evidence_chain import build_chain
    chain = build_chain(customer_id=customer_id, engagement_id=engagement_id)
    return chain.to_markdown()
