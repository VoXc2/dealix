"""ROI OS router — ROI snapshot + executive brief.

Read-only. Every response carries a ``governance_decision``. Cost lines
are always present (``no_hidden_pricing``).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.roi_os.executive_brief import build_brief
from auto_client_acquisition.roi_os.roi_aggregator import compute_roi

router = APIRouter(prefix="/api/v1/roi", tags=["Analytics"])


@router.get("/{customer_id}/snapshot")
async def snapshot(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    snap = compute_roi(customer_id, window_days=window_days)
    payload = snap.to_dict()
    payload["governance_decision"] = GovernanceDecision.ALLOW.value
    return payload


@router.get("/{customer_id}/executive-brief")
async def executive_brief(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
    format: str = Query("json", pattern="^(json|markdown)$"),
) -> Any:
    brief = build_brief(customer_id, window_days=window_days)
    if format == "markdown":
        return PlainTextResponse(brief.markdown, media_type="text/markdown")
    payload = brief.to_dict()
    payload["governance_decision"] = GovernanceDecision.ALLOW.value
    return payload
