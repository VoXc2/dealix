"""Service Quality v5 — QA gate + SLA reader. Read-only / pure-function."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.service_quality import (
    check_delivery_payload,
    get_sla,
    list_slas,
)

router = APIRouter(prefix="/api/v1/service-quality", tags=["service-quality"])


@router.get("/status")
async def service_quality_status() -> dict:
    return {
        "module": "service_quality",
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
            "qa_gate_blocks_forbidden_actions": True,
            "qa_gate_blocks_forbidden_vocabulary": True,
        },
    }


@router.post("/check")
async def qa_check(payload: dict = Body(...)) -> dict:
    """Run the QA gate over a delivery payload.

    Body:
      - service_id: str (required)
      - provided_inputs: list[str] (optional)
      - intended_actions: list[str] (optional)
      - deliverable: any (truthy = present)
      - draft_text: str (optional — runs through safe_publishing_gate)

    Returns: ``QAGateResult`` with verdict (pass / needs_review / blocked).
    """
    service_id = payload.get("service_id")
    if not isinstance(service_id, str) or not service_id:
        raise HTTPException(
            status_code=400, detail="payload.service_id is required",
        )
    try:
        result = check_delivery_payload(service_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result.to_dict()


@router.get("/sla")
async def list_all_slas() -> dict:
    """All per-service SLAs from the YAML matrix."""
    rows = list_slas()
    return {"count": len(rows), "slas": rows}


@router.get("/sla/{service_id}")
async def get_one_sla(service_id: str) -> dict:
    """Get SLA for one service."""
    try:
        sla = get_sla(service_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return sla.to_dict()
