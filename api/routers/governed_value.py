"""Governed Value OS — HTTP surface for the North Star metric, proof state
machine, and 7-gate map (doctrine: "Governed Revenue & AI Operations").

Endpoints (read-only + draft-only — never sends, never charges):
- GET  /api/v1/governed-value/north-star    — Governed Value Decisions count
- POST /api/v1/governed-value/decisions     — record one governed value decision
- GET  /api/v1/governed-value/state-machine — proof states, transitions, L-labels
- POST /api/v1/governed-value/transition    — validate a proposed state transition
- GET  /api/v1/governed-value/gates         — 7-gate map status
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.governed_value_os import (
    ALLOWED_TRANSITIONS,
    GATES,
    PROOF_LEVEL_LABEL,
    ProofState,
    ProofTransitionError,
    count_decisions,
    evaluate_gates,
    list_decisions,
    record_decision,
    validate_transition,
)

router = APIRouter(prefix="/api/v1/governed-value", tags=["Governed Value OS"])


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str = Field(..., min_length=1, max_length=500)
    decision_kind: str = Field(..., min_length=1, max_length=80)
    source_ref: str = Field(..., min_length=1, max_length=200)
    approval_ref: str = Field(..., min_length=1, max_length=200)
    evidence_refs: list[str] = Field(..., min_length=1)
    value_estimate_sar: float = Field(default=0.0, ge=0)


class TransitionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    current: ProofState
    target: ProofState
    founder_confirmed: bool = False
    scope_requested: bool = False
    payment_ref: str = ""


@router.get("/north-star")
async def north_star() -> dict[str, Any]:
    """Governed Value Decisions Created — Dealix's North Star metric."""
    recent = list_decisions(limit=20)
    return {
        "metric": "governed_value_decisions_created",
        "count": count_decisions(),
        "recent": [d.to_dict() for d in recent],
        "is_estimate": True,
    }


@router.post("/decisions")
async def create_decision(req: DecisionRequest) -> dict[str, Any]:
    """Record a governed value decision.

    Refused with HTTP 403 if source, approval, or evidence trail is missing —
    a decision without those three is not governed.
    """
    try:
        decision = record_decision(
            summary=req.summary,
            decision_kind=req.decision_kind,
            source_ref=req.source_ref,
            approval_ref=req.approval_ref,
            evidence_refs=tuple(req.evidence_refs),
            value_estimate_sar=req.value_estimate_sar,
        )
    except ValueError as exc:
        raise HTTPException(status_code=403, detail={"governed_value_violation": str(exc)})
    return {"decision": decision.to_dict()}


@router.get("/state-machine")
async def state_machine_reference() -> dict[str, Any]:
    """Proof states, allowed transitions, and governed-value L-labels."""
    return {
        "states": [s.value for s in ProofState],
        "level_labels": {s.value: PROOF_LEVEL_LABEL[s] for s in ProofState},
        "transitions": {
            s.value: sorted(t.value for t in targets)
            for s, targets in ALLOWED_TRANSITIONS.items()
        },
    }


@router.post("/transition")
async def validate_proof_transition(req: TransitionRequest) -> dict[str, Any]:
    """Validate a proposed proof-state transition against doctrine guards."""
    try:
        validate_transition(
            req.current,
            req.target,
            founder_confirmed=req.founder_confirmed,
            scope_requested=req.scope_requested,
            payment_ref=req.payment_ref,
        )
    except ProofTransitionError as exc:
        raise HTTPException(
            status_code=403,
            detail={
                "code": exc.code,
                "reason_ar": exc.reason_ar,
                "reason_en": exc.reason_en,
            },
        )
    return {
        "allowed": True,
        "current": req.current.value,
        "target": req.target.value,
        "target_level": PROOF_LEVEL_LABEL[req.target],
    }


@router.get("/gates")
async def gate_map(
    messages_sent: int = 0,
    classified_replies: int = 0,
    used_in_meeting: int = 0,
    scope_requested: int = 0,
    invoice_paid: int = 0,
    offer_sold_twice: bool = False,
    repeated_workflows: int = 0,
) -> dict[str, Any]:
    """The 7-gate proof-before-scale map, evaluated against current signals."""
    gates = evaluate_gates(
        messages_sent=messages_sent,
        classified_replies=classified_replies,
        used_in_meeting=used_in_meeting,
        scope_requested=scope_requested,
        invoice_paid=invoice_paid,
        offer_sold_twice=offer_sold_twice,
        repeated_workflows=repeated_workflows,
    )
    return {
        "gates": gates,
        "total": len(GATES),
        "passed": sum(1 for g in gates if g["passed"]),
    }
