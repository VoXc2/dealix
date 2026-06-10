"""CRM v10 router — typed object model + scoring + timeline (no DB)."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from auto_client_acquisition.crm_v10 import (
    Account,
    Deal,
    InvalidStageTransition,
    Lead,
    ProofEventRef,
    ServiceSession,
    SupportTicket,
    advance_deal,
    advance_lead,
    all_object_schemas,
    build_timeline,
    compute_health,
    crm_v10_guardrails,
    list_object_types,
    score_deal,
    score_lead,
)

router = APIRouter(prefix="/api/v1/crm-v10", tags=["crm-v10"])


# ---- Request bodies (extra="forbid" so callers can't smuggle fields) ----


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ScoreLeadRequest(_Strict):
    lead: Lead
    account: Account


class ScoreDealRequest(_Strict):
    deal: Deal
    account: Account
    proof_events_count: int = 0


class TimelineRequest(_Strict):
    account_id: str
    leads: list[Lead] = []
    deals: list[Deal] = []
    service_sessions: list[ServiceSession] = []
    proof_events: list[ProofEventRef] = []


class CustomerHealthRequest(_Strict):
    account: Account
    deals: list[Deal] = []
    service_sessions: list[ServiceSession] = []
    proof_events: list[ProofEventRef] = []
    support_tickets: list[SupportTicket] = []


class AdvanceLeadRequest(_Strict):
    lead: Lead
    target_stage: str


class AdvanceDealRequest(_Strict):
    deal: Deal
    target_stage: str


# ---- Endpoints ----


@router.get("/status")
async def status() -> dict[str, Any]:
    return {"module": "crm_v10", **crm_v10_guardrails()}


@router.get("/schema")
async def schema() -> dict[str, Any]:
    schemas = all_object_schemas()
    return {
        "count": len(schemas),
        "object_types": list(schemas.keys()),
        "schemas": schemas,
    }


@router.get("/object-types")
async def object_types() -> dict[str, Any]:
    names = list_object_types()
    return {"count": len(names), "names": names}


@router.post("/score-lead")
async def score_lead_endpoint(payload: ScoreLeadRequest) -> dict[str, Any]:
    return score_lead(payload.lead, payload.account)


@router.post("/score-deal")
async def score_deal_endpoint(payload: ScoreDealRequest) -> dict[str, Any]:
    return score_deal(payload.deal, payload.account, payload.proof_events_count)


@router.post("/timeline")
async def timeline_endpoint(payload: TimelineRequest) -> dict[str, Any]:
    events = build_timeline(
        payload.account_id,
        payload.leads,
        payload.deals,
        payload.service_sessions,
        payload.proof_events,
    )
    return {"account_id": payload.account_id, "count": len(events), "events": events}


@router.post("/customer-health")
async def customer_health_endpoint(
    payload: CustomerHealthRequest,
) -> dict[str, Any]:
    health = compute_health(
        payload.account,
        payload.deals,
        payload.service_sessions,
        payload.proof_events,
        payload.support_tickets,
    )
    return health.model_dump(mode="json")


@router.post("/lead/advance")
async def lead_advance(payload: AdvanceLeadRequest) -> dict[str, Any]:
    try:
        advanced = advance_lead(payload.lead, payload.target_stage)
    except InvalidStageTransition as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return advanced.model_dump(mode="json")


@router.post("/deal/advance")
async def deal_advance(payload: AdvanceDealRequest) -> dict[str, Any]:
    try:
        advanced = advance_deal(payload.deal, payload.target_stage)
    except InvalidStageTransition as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return advanced.model_dump(mode="json")
