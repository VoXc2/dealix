"""Diagnostic Workflow Router — v6 Phase 4 founder happy-path.

Endpoints under /api/v1/diagnostic-workflow/:
    GET  /status            — module health + active guardrails
    POST /intake            — IntakeRequest -> IntakeRecord
    POST /build             — IntakeRequest -> DiagnosticBundle
    POST /recommend-service — IntakeRequest -> {recommended_bundle}
    POST /pilot-offer       — IntakeRequest -> PilotOffer
    POST /proof-plan        — IntakeRequest -> ProofPlan

Pure local composition. No LLM, no live send, no charge. Pilot price
is fixed at 499 SAR via the schema.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.diagnostic_workflow import (
    IntakeRequest,
    build_diagnostic,
    build_pilot_offer,
    build_proof_plan,
    parse_intake,
    recommend_service,
)

router = APIRouter(
    prefix="/api/v1/diagnostic-workflow",
    tags=["diagnostic-workflow"],
)


@router.get("/status")
async def workflow_status() -> dict[str, Any]:
    return {
        "module": "diagnostic_workflow",
        "status": "operational",
        "guardrails": {
            "no_llm_calls": True,
            "no_live_sends": True,
            "no_external_http": True,
            "no_raw_email_or_phone": True,
            "pilot_price_locked_499_sar": True,
            "approval_required_on_every_step": True,
            "pdpl_aware": True,
        },
    }


@router.post("/intake")
async def workflow_intake(payload: IntakeRequest) -> dict[str, Any]:
    record = parse_intake(payload)
    return record.model_dump(mode="json")


@router.post("/build")
async def workflow_build(payload: IntakeRequest) -> dict[str, Any]:
    record = parse_intake(payload)
    bundle = build_diagnostic(record)
    return bundle.model_dump(mode="json")


@router.post("/recommend-service")
async def workflow_recommend_service(payload: IntakeRequest) -> dict[str, Any]:
    record = parse_intake(payload)
    bundle = build_diagnostic(record)
    return {"recommended_bundle": recommend_service(bundle)}


@router.post("/pilot-offer")
async def workflow_pilot_offer(payload: IntakeRequest) -> dict[str, Any]:
    record = parse_intake(payload)
    bundle = build_diagnostic(record)
    offer = build_pilot_offer(bundle)
    return offer.model_dump(mode="json")


@router.post("/proof-plan")
async def workflow_proof_plan(payload: IntakeRequest) -> dict[str, Any]:
    record = parse_intake(payload)
    bundle = build_diagnostic(record)
    plan = build_proof_plan(record, bundle.recommended_bundle)
    return plan.model_dump(mode="json")
