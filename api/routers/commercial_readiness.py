"""Commercial readiness — service score + gates (read-only)."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.delivery_os.readiness_gates import check_readiness_gate
from auto_client_acquisition.delivery_os.service_readiness import compute_service_readiness_score

router = APIRouter(prefix="/api/v1/commercial", tags=["Sales"])


class ReadinessGateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gate: Literal["delivery", "ai", "production"]
    context: dict[str, Any] = Field(default_factory=dict)


@router.get("/service-readiness/{service_id}")
def get_service_readiness(service_id: str) -> dict[str, Any]:
    """Baseline score from repo YAML; optional overrides via query later."""
    sid = service_id.strip()
    if not sid:
        raise HTTPException(status_code=422, detail="service_id required")
    return compute_service_readiness_score(sid)


@router.post("/service-readiness/{service_id}")
def post_service_readiness(
    service_id: str,
    body: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Merge boolean overrides into baseline YAML evidence."""
    sid = service_id.strip()
    overrides = {k: bool(v) for k, v in body.items() if isinstance(v, bool)}
    return compute_service_readiness_score(sid, evidence_overrides=overrides or None)


@router.post("/readiness-gates/check")
def post_readiness_gates_check(body: ReadinessGateBody) -> dict[str, Any]:
    """Run one of: delivery | ai | production readiness gate."""
    return check_readiness_gate(body.gate, body.context)
