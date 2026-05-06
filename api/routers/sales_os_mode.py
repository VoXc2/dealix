"""Sales OS — closing helpers (draft script + qualification hints)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body

from api.schemas import SalesScriptRequest
from core.prompts.sales_scripts import get_sales_script

router = APIRouter(prefix="/api/v1/sales-os", tags=["sales-os"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "sales_os",
        "delegate": "sales + crm_v10",
        "endpoints": [
            "POST /api/v1/sales/script",
            "POST /api/v1/crm-v10/score-lead",
            "POST /api/v1/crm-v10/score-deal",
        ],
        "guardrails": {
            "no_guarantee_claims": True,
            "approval_required_for_external_messages": True,
        },
    }


@router.post("/pilot-offer-draft")
async def pilot_offer_draft(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """Return a short Arabic opener mentioning 499 pilot — still requires human edit."""
    sector = str(payload.get("sector") or "b2b_services")
    company = str(payload.get("company") or "الفريق")
    try:
        script = get_sales_script("opener", locale="ar", name="", sector=sector, company=company, date="", time="", link="")
    except KeyError:
        script = ""
    return {
        "action_mode": "draft_only",
        "pilot_price_sar": 499,
        "script_ar": script,
        "note": "Edit before send; no cold WhatsApp; no guarantees.",
    }


@router.post("/qualify")
async def qualify_stub(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """Non-persistent stub — use crm_v10 for real scoring."""
    fit = str(payload.get("fit") or "unknown")
    return {
        "fit": fit,
        "recommended_next": "Run POST /api/v1/crm-v10/score-lead with typed Lead+Account",
        "action_mode": "suggest_only",
    }
