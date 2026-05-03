"""
Decision Cards router — Command Center feed.

Endpoints:
    GET  /api/v1/cards/feed?role={ceo|sales|growth|service|support|agency}
        → list of decision cards for the role (demo data when DB empty)
    GET  /api/v1/cards/roles
        → list of supported roles + Arabic labels
    POST /api/v1/cards/{card_id}/decision  body: {"action":"approve|skip|edit"}
        → records a decision (no-op stub for PR-FE-4; full audit in next PR)

Cards are intentionally short-lived. The feed is rebuilt on every request
from the latest signals + funnel events.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query

from auto_client_acquisition.revenue_company_os.card_factory import (
    build_feed,
    list_roles,
)
from auto_client_acquisition.revenue_company_os.cards import Role

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/cards", tags=["cards"])


# Allow callers to pass either canonical or convenience role names
_ROLE_ALIASES = {
    "ceo": Role.CEO,
    "sales": Role.SALES,
    "sales_manager": Role.SALES,
    "growth": Role.GROWTH,
    "growth_manager": Role.GROWTH,
    "service": Role.SERVICE,
    "service_delivery": Role.SERVICE,
    "support": Role.SUPPORT,
    "agency": Role.AGENCY,
    "agency_partner": Role.AGENCY,
}


@router.get("/roles")
async def get_roles() -> dict[str, Any]:
    return {"roles": list_roles()}


@router.get("/feed")
async def get_feed(
    role: str = Query(..., description="ceo|sales|growth|service|support|agency"),
) -> dict[str, Any]:
    role_enum = _ROLE_ALIASES.get(role.lower())
    if role_enum is None:
        raise HTTPException(status_code=400, detail=f"unknown_role: {role}")
    cards = build_feed(role_enum)
    is_demo = bool(cards) and all(c.meta.get("is_demo") for c in cards)
    return {
        "role": role_enum.value,
        "is_demo": is_demo,
        "demo_label_ar": "بيانات تجريبية" if is_demo else None,
        "count": len(cards),
        "cards": [c.to_dict() for c in cards],
    }


@router.post("/{card_id}/decision")
async def submit_decision(
    card_id: str,
    body: dict[str, Any] = Body(...),
) -> dict[str, Any]:
    """Records the operator's decision on a card.

    Stub for PR-FE-4 — accepts the input and returns ack. Full audit log
    + downstream effects (e.g., enqueue outreach) land in a follow-up PR.
    """
    action = str(body.get("action") or "").lower()
    allowed = {"approve", "edit", "skip", "dismiss", "details"}
    if action not in allowed:
        raise HTTPException(status_code=400, detail=f"unknown_action: {action}")
    log.info("card_decision card_id=%s action=%s", card_id, action)
    return {
        "card_id": card_id,
        "action": action,
        "recorded": True,
        "note": "PR-FE-4 stub — full audit in next iteration",
    }
