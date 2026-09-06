"""Bespoke service intake — capability discovery, never automatic price authority.

Public intake can describe a non-standard use case and receive a request ID.
It never receives an automatic price estimate. Commercial progression is:

intake -> Mini Diagnostic -> qualified discovery -> documented customer-specific
quote -> founder-reviewed proposal.
"""
from __future__ import annotations

import hashlib
import logging
import re
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(tags=["service-setup"])

_PRICE_AUTHORITY = "customer_specific_quote_after_qualified_discovery"

_ALLOWED_CATEGORIES = {
    "sales": True,
    "support": True,
    "ops": True,
    "compliance": True,
    "analytics": True,
}
_ALLOWED_COMPLEXITY = {"simple": True, "moderate": True, "complex": True}
_ALLOWED_DATA_BANDS = {"low": True, "medium": True, "high": True}


class _ServiceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=2, max_length=255)
    contact_name: str = Field(..., min_length=2, max_length=128)
    contact_email: EmailStr
    use_case_summary: str = Field(..., min_length=20, max_length=2000)
    use_case_category: str = Field(..., description="sales / support / ops / compliance / analytics")
    complexity: str = Field(..., description="simple / moderate / complex")
    integrations_count: int = Field(..., ge=1, le=10)
    data_volume_band: str = Field(..., description="low / medium / high")
    timeline_weeks: int = Field(..., ge=1, le=24)
    regulated_industry: bool = Field(default=False)
    existing_customer_handle: str | None = Field(default=None, max_length=64)


class _DecisionRequest(BaseModel):
    """Founder review; approval is valid only with discovery + quote references."""

    model_config = ConfigDict(extra="forbid")

    decision: str = Field(..., description="approved | rejected | needs_info")
    discovery_ref: str | None = Field(default=None, max_length=256)
    quote_id: str | None = Field(default=None, max_length=128)
    customer_specific_quote_sar: float | None = Field(default=None, gt=0)
    notes: str | None = Field(default=None, max_length=2000)


def _validate_enum(value: str, allowed: dict[str, bool], field: str) -> None:
    if value not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"{field} must be one of {sorted(allowed)}; got {value!r}",
        )


def _request_id(company: str, submitted_at: datetime) -> str:
    key = f"{company.lower()}:{submitted_at.isoformat(timespec='hours')}"
    return f"ssr_{hashlib.sha256(key.encode()).hexdigest()[:20]}"


@router.post("/api/v1/service-setup/requests", status_code=201)
async def submit_request(body: _ServiceRequest) -> dict[str, Any]:
    """Record a bespoke-capability request without computing or publishing a price."""
    _validate_enum(body.use_case_category, _ALLOWED_CATEGORIES, "use_case_category")
    _validate_enum(body.complexity, _ALLOWED_COMPLEXITY, "complexity")
    _validate_enum(body.data_volume_band, _ALLOWED_DATA_BANDS, "data_volume_band")
    if body.existing_customer_handle is not None:
        if not re.match(r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$", body.existing_customer_handle):
            raise HTTPException(
                status_code=400, detail="invalid existing_customer_handle format",
            )

    submitted_at = datetime.now(UTC)
    request_id = _request_id(body.company_name, submitted_at)

    log.info(
        "service_setup_request id=%s company=%s category=%s complexity=%s",
        request_id,
        body.company_name,
        body.use_case_category,
        body.complexity,
    )

    return {
        "status": "intake_received",
        "request_id": request_id,
        "submitted_at": submitted_at.isoformat(),
        "public_fixed_price": False,
        "automatic_price_estimate": False,
        "price_authority": _PRICE_AUTHORITY,
        "next_step": "free_mini_diagnostic_then_qualified_discovery",
        "note": (
            "No price is generated from public intake fields. If the problem is qualified, "
            "a customer-specific quote is produced after discovery and founder review."
        ),
    }


@router.get("/api/v1/service-setup/requests/{request_id}")
async def get_request_status(
    request_id: str = Path(..., pattern=r"^ssr_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    raise HTTPException(
        status_code=404,
        detail={
            "error": "request_not_persisted",
            "note": (
                "Service-setup request persistence is not enabled in this compatibility path. "
                "Use the canonical opportunity/evidence flow for active customer work."
            ),
            "request_id": request_id,
        },
    )


@router.post(
    "/api/v1/admin/service-setup/requests/{request_id}/decision",
    dependencies=[Depends(require_admin_key)],
)
async def decide_request(
    body: _DecisionRequest,
    request_id: str = Path(..., pattern=r"^ssr_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    if body.decision not in {"approved", "rejected", "needs_info"}:
        raise HTTPException(
            status_code=400,
            detail="decision must be one of {approved, rejected, needs_info}",
        )

    if body.decision == "approved":
        if not body.discovery_ref or not body.quote_id or body.customer_specific_quote_sar is None:
            raise HTTPException(
                status_code=409,
                detail="approved_requires_discovery_ref_and_customer_specific_quote",
            )

    log.info(
        "service_setup_decision request_id=%s decision=%s quote_id=%s",
        request_id,
        body.decision,
        body.quote_id,
    )

    return {
        "status": "reviewed_not_customer_sent",
        "request_id": request_id,
        "decision": body.decision,
        "discovery_ref": body.discovery_ref,
        "quote_id": body.quote_id,
        "customer_specific_quote_sar": body.customer_specific_quote_sar,
        "public_fixed_price": False,
        "external_send_allowed": False,
        "next_step": (
            "render_founder_reviewed_proposal" if body.decision == "approved" else "internal_follow_up"
        ),
    }


class _ProposalBody(BaseModel):
    customer_name: str
    customer_handle: str
    sector: str = "b2b_services"
    city: str = "Riyadh"
    engagement_id: str
    discovery_ref: str
    quote_id: str
    price_sar: float = Field(..., gt=0)
    delivery_days: int = 30


@router.post("/api/v1/service-setup/proposal/{customer_id}")
async def render_proposal_endpoint(
    customer_id: str, body: _ProposalBody
) -> dict[str, Any]:
    """Render a draft proposal only from documented discovery + customer-specific quote."""
    if customer_id != body.customer_handle:
        raise HTTPException(
            status_code=400,
            detail="customer_id in path must match body.customer_handle",
        )
    from auto_client_acquisition.sales_os.proposal_renderer import (
        ProposalContext,
        render_proposal,
    )
    ctx = ProposalContext(
        customer_name=body.customer_name,
        customer_handle=body.customer_handle,
        sector=body.sector,
        city=body.city,
        engagement_id=body.engagement_id,
        price_sar=body.price_sar,
        delivery_days=body.delivery_days,
    )
    md = render_proposal(ctx)
    return {
        "customer_id": customer_id,
        "engagement_id": body.engagement_id,
        "discovery_ref": body.discovery_ref,
        "quote_id": body.quote_id,
        "price_sar": body.price_sar,
        "price_authority": _PRICE_AUTHORITY,
        "proposal_markdown": md,
        "governance_decision": "allow_with_review",
        "external_send_allowed": False,
        "next_step": "founder_review_then_action_specific_send_authority",
    }


class _QualifyBody(BaseModel):
    pain_clear: bool
    owner_present: bool
    data_available: bool
    accepts_governance: bool
    has_budget: bool
    wants_safe_methods: bool = True
    proof_path_visible: bool = True
    retainer_path_visible: bool = True
    raw_request_text: str = ""
    sector: str = ""
    city: str = ""


@router.post("/api/v1/service-setup/qualify")
async def qualify_lead(body: _QualifyBody) -> dict[str, Any]:
    """Sales qualification scorer. Deterministic decision tree; not quote authority."""
    from auto_client_acquisition.sales_os.qualification import qualify
    result = qualify(**body.model_dump())
    return {
        **result.to_dict(),
        "is_estimate": True,
        "governance_decision": "allow",
        "price_authority": _PRICE_AUTHORITY,
        "public_fixed_price": False,
    }
