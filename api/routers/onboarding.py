"""Customer Onboarding API Router.

Manages the client onboarding journey from payment to first value delivery.
All actions require admin authentication.

Prefix: /api/v1/onboarding
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from dealix.commercial.onboarding import OnboardingOrchestrator

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/onboarding", tags=["Customers"])

_ADMIN_KEY = os.getenv("DEALIX_ADMIN_API_KEY", "")
_orchestrator = OnboardingOrchestrator()

# In-memory store (replace with DB in production)
_records: dict[str, Any] = {}


def _require_admin(x_api_key: str = Header(default="", alias="X-Admin-API-Key")) -> None:
    if not _ADMIN_KEY:
        return
    if x_api_key != _ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin API key")


class CreateOnboardingRequest(BaseModel):
    account_id: str
    company_name: str
    contact_name: str
    contact_phone: str
    service_tier: str


class AdvanceStageRequest(BaseModel):
    completed_stage: str
    notes: str = ""


@router.post("/create")
async def create_onboarding(
    req: CreateOnboardingRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Create a new onboarding record after payment confirmation.

    Creates welcome drafts (AR+EN) that require founder approval before sending.
    Returns 5-stage onboarding plan with SLA deadlines.
    """
    record = _orchestrator.create_onboarding(
        account_id=req.account_id,
        company_name=req.company_name,
        contact_name=req.contact_name,
        contact_phone=req.contact_phone,
        service_tier=req.service_tier,
    )
    _records[req.account_id] = record.to_dict()
    return {
        "onboarding_id": record.onboarding_id,
        "current_stage": record.current_stage,
        "steps": [s.model_dump() for s in record.steps],
        "welcome_draft_ar": record.welcome_draft_ar,
        "welcome_draft_en": record.welcome_draft_en,
        "governance_note": "Welcome drafts require founder approval before sending",
        "intake_form": _orchestrator.get_intake_form(),
    }


@router.get("/{account_id}")
async def get_onboarding(
    account_id: str,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Get onboarding status for a customer."""
    record = _records.get(account_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"No onboarding record for account: {account_id}")
    return record


@router.post("/{account_id}/advance")
async def advance_onboarding_stage(
    account_id: str,
    req: AdvanceStageRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Mark an onboarding stage as completed and advance to the next."""
    record_dict = _records.get(account_id)
    if not record_dict:
        raise HTTPException(status_code=404, detail=f"No onboarding record for account: {account_id}")

    from dealix.commercial.onboarding import OnboardingRecord
    record = OnboardingRecord(**record_dict)
    updated = _orchestrator.advance_stage(record, req.completed_stage)
    _records[account_id] = updated.to_dict()

    return {
        "account_id": account_id,
        "completed_stage": req.completed_stage,
        "new_stage": updated.current_stage,
        "is_on_track": updated.is_on_track(),
        "updated_at": datetime.now(UTC).isoformat(),
    }


@router.get("/{account_id}/overdue-check")
async def check_overdue(
    account_id: str,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    """Check for overdue onboarding steps and get action items."""
    record_dict = _records.get(account_id)
    if not record_dict:
        raise HTTPException(status_code=404, detail=f"No onboarding record for account: {account_id}")

    from dealix.commercial.onboarding import OnboardingRecord
    record = OnboardingRecord(**record_dict)
    overdue = _orchestrator.get_overdue_steps(record)

    return {
        "account_id": account_id,
        "is_on_track": len(overdue) == 0,
        "overdue_count": len(overdue),
        "overdue_steps": [s.model_dump() for s in overdue],
        "checked_at": datetime.now(UTC).isoformat(),
    }


@router.get("/intake-form/template")
async def get_intake_template() -> dict[str, Any]:
    """Returns the standard intake session question template."""
    return _orchestrator.get_intake_form()
