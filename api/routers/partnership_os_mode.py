"""Partnership OS — practical mode (draft-only, no white-label promise in API)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body

router = APIRouter(prefix="/api/v1/partnership-os", tags=["partnership-os"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "partnership_os",
        "delegate": "gtm_os + self-growth partner radar",
        "endpoints": [
            "GET /api/v1/gtm/status",
            "GET /api/v1/self-growth/partner-radar",
        ],
        "rules": {
            "no_white_label_before_3_paid_pilots": True,
            "no_revenue_share_without_founder_approval": True,
        },
    }


@router.post("/fit-score")
async def fit_score(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """Deterministic stub — partner name is optional label only."""
    ptype = str(payload.get("partner_type") or "agency")
    score = 70 if ptype in {"agency", "marketing_agency"} else 55
    return {
        "partner_type": ptype,
        "fit_score": score,
        "action_mode": "suggest_only",
        "note": "No fake partner logos or pipeline numbers.",
    }
