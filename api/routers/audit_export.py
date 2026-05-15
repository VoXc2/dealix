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


# ── Wave 14D.4 + 14E: PDF + control-graph endpoints ──────────────────


@router.get("/{customer_id}/pdf")
async def evidence_chain_pdf(
    customer_id: str,
    engagement_id: str = Query(""),
):
    from fastapi.responses import PlainTextResponse, Response
    from auto_client_acquisition.auditability_os.evidence_chain import build_chain
    from auto_client_acquisition.proof_to_market.pdf_renderer import render_markdown_to_pdf
    chain = build_chain(customer_id=customer_id, engagement_id=engagement_id)
    md = chain.to_markdown()
    pdf = render_markdown_to_pdf(md, title=f"Dealix Evidence Chain — {customer_id}")
    if pdf is None:
        return PlainTextResponse(
            content=md,
            headers={"X-PDF-Renderer": "unavailable; markdown returned as fallback"},
        )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=\"evidence_chain_{customer_id}.pdf\""},
    )


@router.get("/{customer_id}/control-graph")
async def evidence_control_graph_json(
    customer_id: str,
    project_id: str = Query(""),
) -> dict[str, Any]:
    """Wave 14E — Evidence Control Plane graph: nodes + edges + gaps +
    compliance summary in one payload."""
    from auto_client_acquisition.evidence_control_plane_os.evidence_graph import (
        build_control_graph,
    )
    graph = build_control_graph(customer_id=customer_id, project_id=project_id)
    return graph.to_dict()


@router.get("/{customer_id}/control-graph/markdown", response_class=PlainTextResponse)
async def evidence_control_graph_markdown(
    customer_id: str,
    project_id: str = Query(""),
) -> str:
    from auto_client_acquisition.evidence_control_plane_os.evidence_graph import (
        build_control_graph,
    )
    return build_control_graph(customer_id=customer_id, project_id=project_id).to_markdown()
