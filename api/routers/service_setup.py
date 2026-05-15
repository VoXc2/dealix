"""Bespoke AI Service Setup intake endpoint (W8.1 — R5 productization).

Lets a prospect/customer submit a request for a custom AI service
(beyond the standard S1-S7 menu), get an automatic price estimate
based on scope, and queue the request for founder review.

R5 in v4 §3:
  - 5K-25K SAR setup + monthly fee
  - Activates after customer #5 with a clear non-standard use case
  - Examples: per-customer LLM fine-tune, custom workflow agent,
    industry-specific compliance checker

Endpoints:

  POST /api/v1/service-setup/requests
       Public — anyone can submit a request. Validates scope fields,
       computes an estimate, returns request_id.

  GET  /api/v1/service-setup/requests/{request_id}
       Public read-only — fetch status of a submitted request.

  POST /api/v1/admin/service-setup/requests/{request_id}/decision
       Admin-only — founder approves/rejects with quoted price.

Scope inputs that drive the price estimate:
  - use_case_category  (sales / support / ops / compliance / analytics)
  - complexity         (simple / moderate / complex)
  - integrations_count (1 / 2 / 3+)
  - data_volume_band   (low / medium / high)
  - timeline_weeks     (1-12)
  - regulated_industry (bool — adds compliance premium)

These map to a deterministic pricing formula so customers see the
same number twice. Founder can override on review.
"""
from __future__ import annotations

import hashlib
import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(tags=["service-setup"])

# ── Pricing parameters ──────────────────────────────────────────

BASE_PRICE_HALALAS = 500_000  # 5,000 SAR floor
CATEGORY_MULTIPLIER = {
    "sales":      1.0,
    "support":    0.9,
    "ops":        1.1,
    "compliance": 1.5,  # higher complexity by nature
    "analytics":  1.2,
}
COMPLEXITY_MULTIPLIER = {"simple": 1.0, "moderate": 1.5, "complex": 2.5}
INTEGRATION_PRICE_HALALAS = 150_000  # 1,500 SAR per integration beyond the first
DATA_VOLUME_MULTIPLIER = {"low": 1.0, "medium": 1.2, "high": 1.5}
REGULATED_PREMIUM_PCT = 0.30  # +30% for regulated industries
MONTHLY_SUPPORT_HALALAS = 100_000  # 1,000 SAR/month maintenance (configurable)
MAX_SETUP_HALALAS = 2_500_000  # 25,000 SAR cap per v4 §3 R5


class _ServiceRequest(BaseModel):
    """Customer submits this to request a bespoke AI service setup."""

    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=2, max_length=255)
    contact_name: str = Field(..., min_length=2, max_length=128)
    contact_email: EmailStr
    use_case_summary: str = Field(..., min_length=20, max_length=2000,
                                  description="What problem are we solving?")
    use_case_category: str = Field(..., description="sales / support / ops / compliance / analytics")
    complexity: str = Field(..., description="simple / moderate / complex")
    integrations_count: int = Field(..., ge=1, le=10)
    data_volume_band: str = Field(..., description="low / medium / high")
    timeline_weeks: int = Field(..., ge=1, le=24)
    regulated_industry: bool = Field(default=False)
    existing_customer_handle: str | None = Field(default=None, max_length=64)


class _DecisionRequest(BaseModel):
    """Admin response after reviewing a submitted request."""

    model_config = ConfigDict(extra="forbid")

    decision: str = Field(..., description="approved | rejected | needs_info")
    quoted_setup_halalas: int | None = Field(default=None, ge=0,
                                              le=MAX_SETUP_HALALAS * 2,
                                              description="founder override of computed estimate")
    quoted_monthly_halalas: int | None = Field(default=None, ge=0,
                                                le=10_000_000)
    notes: str | None = Field(default=None, max_length=2000)


def _validate_enum(value: str, allowed: dict, field: str) -> None:
    if value not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"{field} must be one of {sorted(allowed)}; got {value!r}",
        )


def _compute_estimate(body: _ServiceRequest) -> dict[str, int]:
    """Deterministic pricing formula. Same inputs = same estimate.

    Formula (all in halalas, 1 SAR = 100 halalas):
      base = BASE_PRICE_HALALAS
      base *= category_mult * complexity_mult * data_volume_mult
      base += (integrations_count - 1) * INTEGRATION_PRICE
      if regulated: base *= 1.30
      base = min(base, MAX_SETUP_HALALAS)

      monthly = MONTHLY_SUPPORT_HALALAS * (complexity_mult / 1.0)
    """
    setup = BASE_PRICE_HALALAS
    setup *= CATEGORY_MULTIPLIER.get(body.use_case_category, 1.0)
    setup *= COMPLEXITY_MULTIPLIER.get(body.complexity, 1.0)
    setup *= DATA_VOLUME_MULTIPLIER.get(body.data_volume_band, 1.0)
    setup += max(0, body.integrations_count - 1) * INTEGRATION_PRICE_HALALAS
    if body.regulated_industry:
        setup *= 1 + REGULATED_PREMIUM_PCT
    setup = int(min(setup, MAX_SETUP_HALALAS))

    monthly = int(
        MONTHLY_SUPPORT_HALALAS * COMPLEXITY_MULTIPLIER.get(body.complexity, 1.0)
    )

    return {
        "setup_halalas": setup,
        "setup_sar": setup // 100,
        "monthly_halalas": monthly,
        "monthly_sar": monthly // 100,
        "currency": "SAR",
    }


def _request_id(company: str, submitted_at: datetime) -> str:
    """Deterministic ID: same company + same hour = same ID (idempotency)."""
    key = f"{company.lower()}:{submitted_at.isoformat(timespec='hours')}"
    return f"ssr_{hashlib.sha256(key.encode()).hexdigest()[:20]}"


# ── Endpoints ──────────────────────────────────────────────────────

@router.post("/api/v1/service-setup/requests", status_code=201)
async def submit_request(body: _ServiceRequest) -> dict[str, Any]:
    """Submit a bespoke AI service setup request. Returns request_id + estimate."""
    _validate_enum(body.use_case_category, CATEGORY_MULTIPLIER, "use_case_category")
    _validate_enum(body.complexity, COMPLEXITY_MULTIPLIER, "complexity")
    _validate_enum(body.data_volume_band, DATA_VOLUME_MULTIPLIER, "data_volume_band")
    if body.existing_customer_handle is not None:
        if not re.match(r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$", body.existing_customer_handle):
            raise HTTPException(
                status_code=400, detail="invalid existing_customer_handle format",
            )

    submitted_at = datetime.now(timezone.utc)
    request_id = _request_id(body.company_name, submitted_at)
    estimate = _compute_estimate(body)

    log.info(
        "service_setup_request id=%s company=%s category=%s complexity=%s est_setup_sar=%d",
        request_id, body.company_name, body.use_case_category,
        body.complexity, estimate["setup_sar"],
    )

    return {
        "status": "received",
        "request_id": request_id,
        "submitted_at": submitted_at.isoformat(),
        "estimate": estimate,
        "next_step": (
            "Sami (founder) will review your request within 48 hours and either "
            "approve with a final quote, request more info, or politely decline. "
            "You'll receive an email at the contact_email you provided."
        ),
        "estimate_note": (
            "This is an automated estimate based on standard pricing inputs. "
            "Final quote may differ by ±20% based on review. Setup is capped "
            f"at {MAX_SETUP_HALALAS // 100} SAR per v4 §3 R5."
        ),
    }


@router.get("/api/v1/service-setup/requests/{request_id}")
async def get_request_status(
    request_id: str = Path(..., pattern=r"^ssr_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    """Fetch status of a submitted request.

    Stub: returns 404 with note that persistence requires a DB table.
    Activates after customer #5 actually submits a request (per v4 §7).
    """
    raise HTTPException(
        status_code=404,
        detail={
            "error": "request_not_persisted",
            "note": (
                "Service-setup requests require a service_setup_requests DB "
                "table. Currently /requests returns the estimate inline at "
                "submit time. Persistence activates after customer #5 (v4 §7)."
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
    """Founder decides on a submitted request (approve/reject/needs_info).

    Stub: requires DB persistence (see GET endpoint note). Until then,
    this endpoint validates the input shape so the admin workflow can
    be wired against a real frontend.
    """
    if body.decision not in {"approved", "rejected", "needs_info"}:
        raise HTTPException(
            status_code=400,
            detail="decision must be one of {approved, rejected, needs_info}",
        )
    if body.decision == "approved":
        if body.quoted_setup_halalas is None:
            raise HTTPException(
                status_code=400,
                detail="approved decision requires quoted_setup_halalas",
            )

    log.info(
        "service_setup_decision request_id=%s decision=%s setup_halalas=%s",
        request_id, body.decision, body.quoted_setup_halalas,
    )

    return {
        "status": "recorded_in_memory",
        "request_id": request_id,
        "decision": body.decision,
        "quoted_setup_sar": (body.quoted_setup_halalas or 0) // 100,
        "quoted_monthly_sar": (body.quoted_monthly_halalas or 0) // 100,
        "note": "DB persistence pending — see GET endpoint note. Email customer manually for now.",
    }


# ── Phase-2 90-day activation: Proposal renderer ─────────────────────


class _ProposalBody(BaseModel):
    customer_name: str
    customer_handle: str
    sector: str = "b2b_services"
    city: str = "Riyadh"
    engagement_id: str
    price_sar: int = 499
    delivery_days: int = 7


@router.post("/api/v1/service-setup/proposal/{customer_id}")
async def render_proposal_endpoint(
    customer_id: str, body: _ProposalBody
) -> dict[str, Any]:
    """Render a bilingual proposal for the Revenue Intelligence Sprint.

    Returns the markdown body inline so the founder can email it (manual)
    or pipe it into a future transactional_send call. Tenant-scoped via
    customer_id in path (must match body.customer_handle).
    """
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
        "price_sar": body.price_sar,
        "proposal_markdown": md,
        "governance_decision": "allow_with_review",
        "next_step": "founder_review_then_send_via_email",
    }


# ── Sales qualification endpoint ─────────────────────────────────────


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
    """Sales qualification scorer. Deterministic decision tree."""
    from auto_client_acquisition.sales_os.qualification import qualify
    result = qualify(**body.model_dump())
    return {
        **result.to_dict(),
        "is_estimate": True,
        "governance_decision": "allow",
    }
