"""LeadOps Spine HTTP surface.

5 endpoints:
  GET  /api/v1/leadops/status
  POST /api/v1/leadops/run        — full pipeline on one raw payload
  POST /api/v1/leadops/brief      — brief-only run (no draft)
  POST /api/v1/leadops/draft      — generate draft for an existing lead
  GET  /api/v1/leadops/debug      — pipeline trace for one lead

Hard gates: NO_LIVE_SEND, NO_COLD_WHATSAPP, approval-required.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.leadops_spine import (
    debug_lead,
    list_records,
    run_pipeline,
)

router = APIRouter(prefix="/api/v1/leadops", tags=["leadops-spine"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_cold_whatsapp": True,
    "no_scraping": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "leadops_spine",
        "version": "1.0.0",
        "records_in_memory": len(list_records()),
        "hard_gates": _HARD_GATES,
        "data_status": "live" if list_records() else "ready_no_records_yet",
    }


@router.post("/run")
async def run(body: dict[str, Any]) -> dict[str, Any]:
    """Run full pipeline on one raw payload.

    Body shape: {
      'raw_payload': { company, name, email, phone, sector, region, message },
      'source': 'whatsapp' | 'form' | 'csv' | 'warm_intro' | 'manual' | ...,
      'customer_handle': optional
    }
    """
    raw = body.get("raw_payload")
    if not isinstance(raw, dict):
        raise HTTPException(status_code=422, detail="raw_payload must be a dict")
    source = body.get("source") or "manual"
    customer_handle = body.get("customer_handle")
    record = run_pipeline(
        raw_payload=raw,
        source=source,
        customer_handle=customer_handle,
    )
    return {
        "leadops_id": record.leadops_id,
        "compliance_status": record.compliance_status,
        "score": record.score,
        "offer_route": record.offer_route,
        "next_action": record.next_action,
        "draft_id": record.draft_id,
        "approval_id": record.approval_id,
        "safety_summary": record.safety_summary,
        "hard_gates": _HARD_GATES,
    }


@router.post("/brief")
async def brief(body: dict[str, Any]) -> dict[str, Any]:
    """Run pipeline but skip draft generation (just brief + score)."""
    raw = body.get("raw_payload")
    if not isinstance(raw, dict):
        raise HTTPException(status_code=422, detail="raw_payload must be a dict")
    source = body.get("source") or "manual"
    record = run_pipeline(raw_payload=raw, source=source)
    return {
        "leadops_id": record.leadops_id,
        "brief": record.brief,
        "score": record.score,
        "compliance_status": record.compliance_status,
        "hard_gates": _HARD_GATES,
    }


@router.post("/draft")
async def draft(body: dict[str, Any]) -> dict[str, Any]:
    """Re-emit a draft for an existing leadops_id (no new persistence)."""
    leadops_id = body.get("leadops_id")
    if not leadops_id:
        raise HTTPException(status_code=422, detail="leadops_id required")
    trace = debug_lead(leadops_id)
    if "error" in trace:
        raise HTTPException(status_code=404, detail=trace["error"])
    return {
        "leadops_id": leadops_id,
        "draft_id": trace["trace"].get("10_draft_id"),
        "approval_id": trace["trace"].get("11_approval_id"),
        "offer_route": trace["trace"].get("8_offer_route"),
        "hard_gates": _HARD_GATES,
    }


@router.get("/debug")
async def debug(leadops_id: str) -> dict[str, Any]:
    """Full pipeline trace for one lead."""
    trace = debug_lead(leadops_id)
    if "error" in trace:
        raise HTTPException(status_code=404, detail=trace["error"])
    return {**trace, "hard_gates": _HARD_GATES}
