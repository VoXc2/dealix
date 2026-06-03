"""Friction Log router — POST events + GET aggregated / raw.

Tenant-scoped via customer_id in path / body. Notes are sanitized for
PII before persistence.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.friction_log.aggregator import aggregate as aggregate_friction
from auto_client_acquisition.friction_log.schemas import FrictionKind, FrictionSeverity
from auto_client_acquisition.friction_log.store import emit, list_events
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision

router = APIRouter(prefix="/api/v1/friction-log", tags=["friction-log"])


class FrictionEmitBody(BaseModel):
    customer_id: str = Field(..., min_length=1)
    kind: str = FrictionKind.MANUAL_OVERRIDE.value
    severity: str = FrictionSeverity.LOW.value
    workflow_id: str = ""
    evidence_ref: str = ""
    cost_minutes: int = 0
    notes: str = ""


@router.post("/event")
async def emit_event(body: FrictionEmitBody) -> dict[str, Any]:
    if body.kind not in {k.value for k in FrictionKind}:
        raise HTTPException(status_code=422, detail=f"invalid kind {body.kind!r}")
    if body.severity not in {s.value for s in FrictionSeverity}:
        raise HTTPException(status_code=422, detail=f"invalid severity {body.severity!r}")
    try:
        event = emit(
            customer_id=body.customer_id,
            kind=body.kind,
            severity=body.severity,
            workflow_id=body.workflow_id,
            evidence_ref=body.evidence_ref,
            cost_minutes=body.cost_minutes,
            notes=body.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return {
        "event": event.to_dict(),
        "governance_decision": GovernanceDecision.ALLOW.value,
    }


@router.get("/{customer_id}")
async def get_aggregate(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    agg = aggregate_friction(customer_id=customer_id, window_days=window_days)
    payload = agg.to_dict()
    payload["governance_decision"] = GovernanceDecision.ALLOW.value
    return payload


@router.get("/{customer_id}/events")
async def get_events(
    customer_id: str,
    limit: int = Query(200, ge=1, le=2000),
    since_days: int = Query(30, ge=1, le=365),
    kind: str | None = Query(None),
) -> dict[str, Any]:
    events = list_events(
        customer_id=customer_id, limit=limit, since_days=since_days, kind=kind
    )
    return {
        "customer_id": customer_id,
        "count": len(events),
        "events": [e.to_dict() for e in events],
        "governance_decision": GovernanceDecision.ALLOW.value,
    }
