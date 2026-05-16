"""Governed Revenue & AI Operations API surface.

Read-only strategy contracts + strict state-machine transition checks.
No external send, no billing execution, no autonomous actions.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.governed_revenue_ops import (
    NORTH_STAR,
    OPERATING_CHAIN,
    POSITIONING_AR,
    POSITIONING_EN,
    SERVICE_LADDER,
    GovernedValueAdvanceRequest,
    advance_state,
    list_state_machine,
)

router = APIRouter(
    prefix="/api/v1/governed-revenue-ops",
    tags=["governed-revenue-ops"],
)


_HARD_GATES = {
    "no_autonomous_external_send": True,
    "approval_required_for_external_actions": True,
    "no_revenue_before_invoice_paid": True,
    "evidence_required_for_governed_value_decision": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    featured = [offer.service_id for offer in SERVICE_LADDER if offer.featured_in_first_meeting]
    return {
        "service": "governed_revenue_ops",
        "positioning_en": POSITIONING_EN,
        "positioning_ar": POSITIONING_AR,
        "north_star": NORTH_STAR,
        "featured_offers_first_meeting": featured,
        "hard_gates": _HARD_GATES,
    }


@router.get("/operating-chain")
async def operating_chain() -> dict[str, Any]:
    return {
        "chain": [step.model_dump() for step in OPERATING_CHAIN],
        "rule_en": "Anything outside this chain is noise.",
        "rule_ar": "أي شيء خارج هذه السلسلة يعتبر ضجيجاً.",
    }


@router.get("/services")
async def services() -> dict[str, Any]:
    offers = [offer.model_dump() for offer in SERVICE_LADDER]
    featured = [offer for offer in offers if offer["featured_in_first_meeting"]]
    return {
        "offers": offers,
        "featured_first_meeting": featured,
        "note_en": "Start with 3 offers in first meeting: Diagnostic -> Sprint -> Retainer.",
        "note_ar": "في أول مقابلة اعرض 3 خدمات فقط: Diagnostic ثم Sprint ثم Retainer.",
    }


@router.get("/state-machine")
async def state_machine() -> dict[str, Any]:
    machine = list_state_machine()
    machine["rules"] = {
        "no_sent_without_founder_confirmed": True,
        "no_l7_confirmed_without_payment": True,
        "no_revenue_before_invoice_paid": True,
        "l5_requires_used_in_meeting": True,
        "l6_requires_scope_or_pilot_intro_request": True,
    }
    return machine


@router.post("/state-machine/advance")
async def state_machine_advance(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        req = GovernedValueAdvanceRequest(**payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"invalid payload: {exc}") from exc
    result = advance_state(req)
    code = 200 if result.accepted else 409
    body = result.model_dump(mode="json")
    body["hard_gates"] = _HARD_GATES
    if result.accepted:
        return body
    raise HTTPException(status_code=code, detail=body)
