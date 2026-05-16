"""Deal Desk API — draft-only requests; approval-first."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.commercial_engagements.deal_desk_os import (
    create_deal_desk_request,
    get_request,
    list_requests,
    objection_intelligence_hints,
    record_approval,
    submit_for_approval,
)

router = APIRouter(prefix="/api/v1/commercial/deal-desk", tags=["Sales"])


class DealDeskCreateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str
    offer_tier: str
    amount_sar: float = Field(ge=0)
    objection_tags: list[str] = Field(default_factory=list)
    notes: str = ""


class DealDeskApprovalBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approved: bool
    approver_note: str = ""


@router.post("/requests")
def post_create_request(body: DealDeskCreateBody) -> dict[str, Any]:
    req = create_deal_desk_request(
        company=body.company,
        offer_tier=body.offer_tier,
        amount_sar=body.amount_sar,
        objection_tags=body.objection_tags,
        notes=body.notes,
    )
    return {
        "request": req.to_dict(),
        "objection_hints": objection_intelligence_hints(body.objection_tags),
        "external_send": False,
    }


@router.get("/requests")
def get_requests(status: str | None = None) -> dict[str, Any]:
    st = status.strip() if status else None
    if st and st not in ("draft", "pending_approval", "approved", "rejected"):
        raise HTTPException(status_code=422, detail="invalid status")
    rows = list_requests(status=st)  # type: ignore[arg-type]
    return {"requests": [r.to_dict() for r in rows], "count": len(rows)}


@router.get("/requests/{request_id}")
def get_one_request(request_id: str) -> dict[str, Any]:
    req = get_request(request_id)
    if req is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"request": req.to_dict()}


@router.post("/requests/{request_id}/submit")
def post_submit(request_id: str) -> dict[str, Any]:
    try:
        req = submit_for_approval(request_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="not found") from None
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"request": req.to_dict()}


@router.post("/requests/{request_id}/approval")
def post_approval(request_id: str, body: DealDeskApprovalBody) -> dict[str, Any]:
    try:
        req = record_approval(request_id, approved=body.approved, approver_note=body.approver_note)
    except KeyError:
        raise HTTPException(status_code=404, detail="not found") from None
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"request": req.to_dict(), "external_send": False}
