"""Revenue Ops router — Governed Revenue Ops Diagnostic delivery surface.

Endpoints (prefix /api/v1/revenue-ops):
  POST /diagnostics                 — create a diagnostic (records CEL2)
  POST /upload                      — intake a CRM/data CSV (preview only)
  POST /score                       — deterministic revenue-readiness score
  GET  /{diagnostic_id}/decision-passport
  POST /{diagnostic_id}/follow-up-drafts

Tenant-scoped via `customer_id` in the body / query. Drafts are returned as
approval-required items; nothing auto-sends.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.commercial_os.engine import CommercialEngine
from auto_client_acquisition.revenue_ops.decision_passport import (
    build_decision_passport,
)
from auto_client_acquisition.revenue_ops.diagnostic import create_diagnostic
from auto_client_acquisition.revenue_ops.follow_up_drafts import (
    generate_follow_up_drafts,
)
from auto_client_acquisition.revenue_ops.scoring import score_readiness
from auto_client_acquisition.revenue_ops.upload import intake_csv
from auto_client_acquisition.revenue_memory.event_store import get_default_store

router = APIRouter(prefix="/api/v1/revenue-ops", tags=["revenue-ops"])

# In-memory registry of created diagnostics — keyed by diagnostic_id. The
# commercial event stream is the source of truth for CEL state; this map only
# resolves a diagnostic_id back to its account for later lookups.
_DIAGNOSTICS: dict[str, dict[str, Any]] = {}

_GOVERNANCE_DECISION = "approval_required"


def _engine() -> CommercialEngine:
    """Engine bound to the shared default event store."""
    return CommercialEngine(store=get_default_store())


class CreateDiagnosticBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)
    notes: str = ""
    inputs: dict[str, Any] = Field(default_factory=dict)
    actor: str = "system"


class UploadBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1)
    csv_text: str = Field(..., min_length=1)


class ScoreBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1)
    signals: dict[str, bool] = Field(default_factory=dict)


class FollowUpDraftsBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1)
    extra_context: str = ""


@router.post("/diagnostics")
async def create_diagnostic_endpoint(body: CreateDiagnosticBody) -> dict[str, Any]:
    """Create a Governed Revenue Ops Diagnostic — records `commercial.prepared`."""
    try:
        diagnostic = create_diagnostic(
            customer_id=body.customer_id,
            account_id=body.account_id,
            engine=_engine(),
            notes=body.notes,
            inputs=body.inputs,
            actor=body.actor,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    _DIAGNOSTICS[diagnostic.diagnostic_id] = {
        "customer_id": diagnostic.customer_id,
        "account_id": diagnostic.account_id,
    }
    return {
        "diagnostic": diagnostic.to_dict(),
        "governance_decision": _GOVERNANCE_DECISION,
    }


@router.post("/upload")
async def upload_endpoint(body: UploadBody) -> dict[str, Any]:
    """Intake a CRM/data CSV for the diagnostic. Preview only; never persisted."""
    result = intake_csv(body.csv_text)
    return {
        "customer_id": body.customer_id,
        "upload": result.to_dict(),
        "governance_decision": _GOVERNANCE_DECISION,
    }


@router.post("/score")
async def score_endpoint(body: ScoreBody) -> dict[str, Any]:
    """Deterministic revenue-readiness score from readiness signals."""
    score = score_readiness(body.signals)
    return {
        "customer_id": body.customer_id,
        "readiness": score.to_dict(),
        "governance_decision": _GOVERNANCE_DECISION,
    }


@router.get("/{diagnostic_id}/decision-passport")
async def decision_passport_endpoint(
    diagnostic_id: str,
    customer_id: str = Query(..., min_length=1),
    signals: str = Query(
        default="",
        description="Comma-separated readiness signals that are present.",
    ),
) -> dict[str, Any]:
    """Assemble the diagnostic's decision passport."""
    record = _DIAGNOSTICS.get(diagnostic_id)
    if record is None:
        raise HTTPException(status_code=404, detail="unknown_diagnostic_id")
    if record["customer_id"] != customer_id:
        raise HTTPException(status_code=404, detail="unknown_diagnostic_id")

    present = {s.strip(): True for s in signals.split(",") if s.strip()}
    score = score_readiness(present)

    account_id = record["account_id"]
    engine = _engine()
    state = engine.current_state(
        customer_id=customer_id, subject_type="account", subject_id=account_id
    )
    passport = build_decision_passport(
        diagnostic_id=diagnostic_id,
        customer_id=customer_id,
        account_id=account_id,
        readiness=score,
        commercial_state=state["state"] if state else None,
        cel=state["cel"] if state else None,
    )
    return {
        "decision_passport": passport.to_dict(),
        "governance_decision": _GOVERNANCE_DECISION,
    }


@router.post("/{diagnostic_id}/follow-up-drafts")
async def follow_up_drafts_endpoint(
    diagnostic_id: str,
    body: FollowUpDraftsBody = Body(...),
) -> dict[str, Any]:
    """Generate governed follow-up drafts as approval-required items."""
    record = _DIAGNOSTICS.get(diagnostic_id)
    if record is None or record["customer_id"] != body.customer_id:
        raise HTTPException(status_code=404, detail="unknown_diagnostic_id")
    drafts = generate_follow_up_drafts(
        diagnostic_id=diagnostic_id,
        customer_id=body.customer_id,
        extra_context=body.extra_context,
    )
    return {
        "diagnostic_id": diagnostic_id,
        "drafts": [d.to_dict() for d in drafts],
        "count": len(drafts),
        "requires_approval": True,
        "auto_sent": False,
        "governance_decision": _GOVERNANCE_DECISION,
    }
