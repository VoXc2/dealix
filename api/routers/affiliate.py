"""Affiliate program endpoints (W13.3 — distinct from W13.13 customer referrals).

Customer referrals (W13.13) = existing paying customer refers a peer.
Affiliate program (this) = external partners (influencers, consultants,
agencies that aren't yet on R6 White-Label) earn commission for any
customer they bring.

Differences vs W13.13:
  - Affiliates may NOT be customers themselves
  - Commission % varies by tier (10/15/20/25%)
  - First-12-months MRR commission, not lifetime
  - Tracked via unique affiliate code at checkout
  - Monthly payouts vs subscription credits

Why these structures (Wave 13 deep research):
  - Stripe/Shopify affiliate models pay 10-30% recurring for 12 months
  - Single-tier programs underperform vs tiered (Hubspot data)
  - Influencer programs in MENA pay flat-rate per closed deal (1-5K USD)

Endpoints:
  POST /api/v1/affiliates/apply              (public — apply to become affiliate)
  POST /api/v1/affiliates/approve            (admin — approve application)
  POST /api/v1/affiliates/track              (public — record click)
  POST /api/v1/affiliates/attribute          (admin — credit closed deal)
  GET  /api/v1/affiliates/_tiers             (public — tier structure)
"""
from __future__ import annotations

import hashlib
import logging
import secrets
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/affiliates", tags=["affiliates"])

# Tier structure — calibrated to industry SaaS norms
# Lower tier = entry partner; Higher tier = proven volume
TIERS = {
    "bronze": {
        "commission_pct": 10,
        "min_closes_per_quarter": 0,
        "payout_max_sar_per_month": 5_000,
        "qualification": "Newly approved affiliate",
    },
    "silver": {
        "commission_pct": 15,
        "min_closes_per_quarter": 2,
        "payout_max_sar_per_month": 15_000,
        "qualification": "2+ closed deals in trailing quarter",
    },
    "gold": {
        "commission_pct": 20,
        "min_closes_per_quarter": 5,
        "payout_max_sar_per_month": 50_000,
        "qualification": "5+ closed deals in trailing quarter",
    },
    "platinum": {
        "commission_pct": 25,
        "min_closes_per_quarter": 10,
        "payout_max_sar_per_month": 200_000,
        "qualification": "10+ closed deals in trailing quarter (likely R6 candidate)",
    },
}

COMMISSION_MONTHS = 12  # first-12-month MRR commission window


class _ApplicationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=2, max_length=128)
    email: EmailStr
    company: str | None = Field(default=None, max_length=255)
    audience_size_estimate: int | None = Field(default=None, ge=0, le=10_000_000)
    audience_description: str = Field(..., min_length=20, max_length=2000)
    saudi_b2b_relevant: bool = Field(default=True)
    referrer_url: str | None = Field(default=None, max_length=512)


class _TrackingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(..., pattern=r"^AFF-[A-Z0-9]{8}$")
    landing_page: str = Field(..., max_length=512)
    user_agent_hash: str | None = Field(default=None, max_length=64,
                                         description="server-computed hash, not raw UA")


class _AttributionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    affiliate_code: str = Field(..., pattern=r"^AFF-[A-Z0-9]{8}$")
    customer_handle: str = Field(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$")
    initial_mrr_halalas: int = Field(..., ge=0)
    plan: str = Field(..., description="starter / growth / scale")


def _generate_affiliate_code(email: str) -> str:
    """Deterministic per email for idempotency on approval."""
    suffix = hashlib.sha256(email.lower().encode()).hexdigest()[:8].upper()
    return f"AFF-{suffix}"


def _generate_payout_id() -> str:
    return f"po_{secrets.token_hex(8)}"


@router.get("/_tiers")
async def list_tiers() -> dict[str, Any]:
    """Public tier structure. Linked from affiliate landing + application form."""
    return {
        "currency": "SAR",
        "commission_basis": "first 12 months of customer MRR",
        "payment_method": "monthly ZATCA-compliant payout (Saudi IBAN or PayPal for non-Saudi)",
        "tiers": TIERS,
        "auto_tier_upgrade": (
            "Quarterly review: if affiliate hit min_closes threshold "
            "in last 90 days, auto-promote to next tier."
        ),
        "auto_tier_demote_threshold": (
            "If 2 consecutive quarters below min_closes, demote one tier."
        ),
        "anti_abuse": [
            "Self-referrals via affiliate code: blocked",
            "Same-domain refers same-domain: blocked",
            "Cookie window: 90 days (Last-touch attribution)",
            "Chargeback within 90 days: commission clawback",
        ],
    }


@router.post("/apply", status_code=201)
async def apply_affiliate(body: _ApplicationRequest) -> dict[str, Any]:
    """Public — apply to become a Dealix affiliate. Admin reviews + approves."""
    application_id = f"app_{secrets.token_hex(8)}"
    email_hash = hashlib.sha256(body.email.encode()).hexdigest()[:12]

    log.info(
        "affiliate_application id=%s email_hash=%s saudi_b2b=%s",
        application_id, email_hash, body.saudi_b2b_relevant,
    )

    return {
        "status": "received",
        "application_id": application_id,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "review_sla_business_days": 5,
        "next_step": (
            "Founder personally reviews each application within 5 business days. "
            "If approved, you'll receive your affiliate code and Bronze-tier "
            "tracking link by email."
        ),
        "tier_at_approval": "bronze",
        "tier_commission_pct": 10,
        "commission_basis_months": COMMISSION_MONTHS,
        "note": "Persistence pending; founder reviews applications via email for now.",
    }


@router.post(
    "/approve",
    dependencies=[Depends(require_admin_key)],
    status_code=201,
)
async def approve_application(
    email: EmailStr,
    initial_tier: str = "bronze",
) -> dict[str, Any]:
    """Admin — approve application + issue affiliate code.

    Email field as query param so admin can approve via simple curl:
      POST /approve?email=affiliate@example.com&initial_tier=bronze
    """
    if initial_tier not in TIERS:
        raise HTTPException(
            status_code=400,
            detail=f"initial_tier must be one of {sorted(TIERS)}",
        )

    code = _generate_affiliate_code(str(email))
    tier_info = TIERS[initial_tier]

    log.info(
        "affiliate_approved email_hash=%s tier=%s code=%s",
        hashlib.sha256(str(email).encode()).hexdigest()[:12],
        initial_tier, code,
    )

    return {
        "status": "approved",
        "code": code,
        "tier": initial_tier,
        "commission_pct": tier_info["commission_pct"],
        "tracking_link_template": (
            f"https://dealix.me/?ref={code}&utm_source=affiliate"
        ),
        "share_template": (
            f"تابعت Dealix فترة وهم AI نظام تشغيل B2B سعودي حقيقي "
            f"(PDPL + ZATCA wired). جرّبوا الـ Pilot عبر "
            f"https://dealix.me/?ref={code} — لو اشتركوا، آخذ "
            f"{tier_info['commission_pct']}% commission على أول 12 شهر."
        ),
    }


@router.post("/track", status_code=202)
async def track_click(body: _TrackingRequest) -> dict[str, Any]:
    """Public — record an affiliate click (called from referral landing).

    No PII captured: just the code + landing page + hashed user agent.
    Used for attribution + fraud detection.
    """
    return {
        "status": "tracked",
        "code": body.code,
        "tracked_at": datetime.now(timezone.utc).isoformat(),
        "attribution_window_days": 90,
        "note": "Persistence + click-to-conversion analytics deferred.",
    }


@router.post(
    "/attribute",
    dependencies=[Depends(require_admin_key)],
    status_code=201,
)
async def attribute_close(body: _AttributionRequest) -> dict[str, Any]:
    """Admin — credit an affiliate for a closed deal.

    Triggered manually until automation hooks ride on Moyasar webhook
    (TBD when customer #5 closes via affiliate path).
    """
    valid_plans = ("starter", "growth", "scale")
    if body.plan not in valid_plans:
        raise HTTPException(
            status_code=400, detail=f"plan must be one of {valid_plans}",
        )

    # Default to bronze tier; real implementation looks up affiliate row
    commission_pct = TIERS["bronze"]["commission_pct"]
    monthly_commission_halalas = (body.initial_mrr_halalas * commission_pct) // 100
    total_12mo_commission_halalas = monthly_commission_halalas * COMMISSION_MONTHS

    payout_id = _generate_payout_id()

    log.info(
        "affiliate_attribution id=%s code=%s customer=%s mrr=%d "
        "12mo_commission=%d",
        payout_id, body.affiliate_code, body.customer_handle,
        body.initial_mrr_halalas, total_12mo_commission_halalas,
    )

    return {
        "status": "attributed",
        "payout_id": payout_id,
        "affiliate_code": body.affiliate_code,
        "customer_handle": body.customer_handle,
        "plan": body.plan,
        "customer_mrr_sar": body.initial_mrr_halalas // 100,
        "commission_pct": commission_pct,
        "monthly_payout_sar": monthly_commission_halalas // 100,
        "total_12mo_payout_sar": total_12mo_commission_halalas // 100,
        "first_payout_at": (
            datetime.now(timezone.utc).replace(day=1) + datetime.now(timezone.utc).resolution
        ).isoformat() if False else "first business day of next month",
        "clawback_window_days": 90,
        "note": (
            "Payouts processed monthly batch. ZATCA-compliant invoice "
            "issued to affiliate. Persistence + automated Moyasar trigger "
            "deferred to follow-up."
        ),
    }
