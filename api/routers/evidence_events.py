"""Evidence event aliases for governed revenue ops."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.proof_ledger import ProofEvent, ProofEventType, get_default_ledger
from auto_client_acquisition.revenue_ops import EvidenceEventRequest, record_evidence_event

router = APIRouter(prefix="/api/v1/evidence", tags=["evidence"])

_HARD_GATES = {
    "no_fake_proof": True,
    "evidence_ref_required": True,
    "source_ref_required": True,
}

_EVENT_MAP: dict[str, ProofEventType] = {
    "diagnostic_created": ProofEventType.DIAGNOSTIC_DELIVERED,
    "follow_up_drafted": ProofEventType.DELIVERY_TASK_COMPLETED,
    "used_in_meeting": ProofEventType.DELIVERY_TASK_COMPLETED,
    "scope_requested": ProofEventType.UPSELL_RECOMMENDED,
    "invoice_sent": ProofEventType.INVOICE_PREPARED,
    "invoice_paid": ProofEventType.PAYMENT_CONFIRMED,
}


@router.get("/status")
async def evidence_status() -> dict[str, Any]:
    return {
        "service": "evidence_events_alias",
        "status": "operational",
        "backing_store": "proof_ledger",
        "hard_gates": _HARD_GATES,
    }


@router.post("/events")
async def create_evidence_event(req: EvidenceEventRequest) -> dict[str, Any]:
    try:
        revenue_event = record_evidence_event(req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    proof_type = _EVENT_MAP.get(req.event_type, ProofEventType.DELIVERY_TASK_COMPLETED)
    proof_event = ProofEvent(
        event_type=proof_type,
        customer_handle=req.diagnostic_id,
        service_id="governed_revenue_ops_diagnostic",
        summary_ar=req.summary_ar,
        summary_en=req.summary_en,
        evidence_source=req.source_ref,
        payload={"evidence_ref": req.evidence_ref, "event_type": req.event_type},
    )
    stored = get_default_ledger().record(proof_event)
    return {
        "event": revenue_event,
        "proof_ledger_event": stored.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }
