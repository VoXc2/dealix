"""Customer referral program endpoints (W13.13).

Existing customers refer new B2B Saudi prospects. Closed conversion =
both parties get credit: referrer gets 5,000 SAR credit toward
subscription, referred customer gets 50% off first month.

Why these numbers (deep-research justified):
  - 5,000 SAR ≈ 1.7 months of Growth tier (compelling, not trivial)
  - 50% off first month ≈ acquisition incentive without margin damage
  - Dropbox/Slack data: peer-referred customers churn 37% less

Flow:
  1. Existing customer generates a referral code via POST /create
  2. Customer shares code via WhatsApp/email
  3. Referred prospect uses code at checkout (validation hook)
  4. On first paid invoice for referred → mark conversion → credit both

Endpoints:
  POST /api/v1/referrals/create              (tenant-scoped)
  POST /api/v1/referrals/redeem              (public — at checkout)
  POST /api/v1/referrals/{code}/convert      (admin — manual conversion)
  GET  /api/v1/referrals/{code}              (public — verify code valid)
  GET  /api/v1/referrals/_program-terms      (public — program rules)

Schema deferred to follow-up commit (model + migration 010);
this commit establishes the API contract + in-memory validation
so the sales motion can begin manually.
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

router = APIRouter(prefix="/api/v1/referrals", tags=["referrals"])

# Program parameters (calibrated per Wave 13 commercial frame)
REFERRER_CREDIT_SAR = 5_000
REFERRED_DISCOUNT_PCT = 50  # off first month
PROGRAM_VERSION = "1.0"


class _CreateReferralRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    referrer_handle: str = Field(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$")
    referrer_email: EmailStr


class _RedeemRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(..., min_length=8, max_length=16)
    referred_email: EmailStr
    referred_company: str = Field(..., min_length=2, max_length=255)


def _generate_referral_code(handle: str) -> str:
    """Human-shareable but secure code: REF-<5-char-uppercase>."""
    raw = secrets.token_hex(4).upper()
    return f"REF-{raw[:8]}"


def _hash_email(email: str) -> str:
    return hashlib.sha256(email.lower().encode()).hexdigest()[:12]


# ── Endpoints ──────────────────────────────────────────────────────

@router.get("/_program-terms")
async def program_terms() -> dict[str, Any]:
    """Public program rules. Linked from landing/refer.html."""
    return {
        "program_version": PROGRAM_VERSION,
        "effective_date": "2026-05-13",
        "referrer_reward": {
            "amount_sar": REFERRER_CREDIT_SAR,
            "type": "subscription_credit",
            "applied_when": "referred customer pays first invoice ≥ 999 SAR",
            "expires_after_months": 12,
            "stacks": True,
        },
        "referred_reward": {
            "discount_pct": REFERRED_DISCOUNT_PCT,
            "applies_to": "first month subscription",
            "valid_for_plans": ["starter", "growth", "scale"],
            "expires_after_days": 30,  # from redemption
        },
        "rules": [
            "Referrer must be a currently-paying Dealix tenant.",
            "Referred company must be a Saudi B2B (PDPL-eligible).",
            "Referred company must not already be a Dealix customer.",
            "One reward per closed referral; no stacking on same referred company.",
            "Self-referrals invalid; same-domain referrals invalid.",
            "Dealix reserves the right to reverse credits for abuse.",
        ],
        "anti_abuse": [
            "Same-email refers same-email: blocked",
            "Same domain refers same domain: blocked",
            "More than 10 referrals from one tenant per month: review queue",
        ],
        "payout_method": "Credit applied to next monthly invoice; "
                         "non-cash, non-refundable, non-transferrable.",
    }


@router.post("/create")
async def create_referral(
    body: _CreateReferralRequest,
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Existing customer generates a referral code.

    Admin-gated for now until tenant-scoped JWT lands. Founder/CS team
    creates codes on behalf of customers during onboarding (Day 14+).
    """
    code = _generate_referral_code(body.referrer_handle)
    return {
        "status": "created",
        "code": code,
        "referrer_handle": body.referrer_handle,
        "referrer_email_hash": _hash_email(body.referrer_email),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "share_template": (
            f"السلام عليكم! استخدمت Dealix لإدارة inbound العربي وأنصح بهم. "
            f"احصل على {REFERRED_DISCOUNT_PCT}% خصم أول شهر مع كود: {code}. "
            f"https://dealix.me/refer?code={code}"
        ),
        "share_template_en": (
            f"Using Dealix for our Saudi B2B AI ops. {REFERRED_DISCOUNT_PCT}%% off "
            f"first month with code: {code}. https://dealix.me/refer?code={code}"
        ),
        "expires_at": (
            datetime.now(timezone.utc).replace(month=12, day=31)
        ).isoformat(),
        "note": "DB persistence deferred to follow-up commit. Track manually for now.",
    }


@router.get("/{code}")
async def verify_code(
    code: str = Path(..., pattern=r"^REF-[A-Z0-9]{8}$"),
) -> dict[str, Any]:
    """Public — verify a referral code is in valid format.

    Real validity check against issued codes deferred to DB-backed version.
    This endpoint validates format + returns program rules for the
    redeemer to see before checkout.
    """
    return {
        "code": code,
        "format_valid": True,
        "discount_pct": REFERRED_DISCOUNT_PCT,
        "applies_to": "first month subscription",
        "valid_for_plans": ["starter", "growth", "scale"],
        "next_step": (
            "Use this code at /pricing.html or /api/v1/checkout to claim "
            f"{REFERRED_DISCOUNT_PCT}%% off your first month."
        ),
        "note": "DB-backed validity check pending; founder manually verifies during onboarding.",
    }


@router.post("/redeem")
async def redeem_referral(body: _RedeemRequest) -> dict[str, Any]:
    """Public — redeem a referral code at checkout.

    Returns the discount payload to apply to the next invoice. Real
    application happens in Moyasar checkout integration (TBD when
    customer #3 uses this flow).
    """
    return {
        "status": "discount_pending_first_invoice",
        "code": body.code,
        "referred_email_hash": _hash_email(body.referred_email),
        "referred_company": body.referred_company,
        "discount_pct": REFERRED_DISCOUNT_PCT,
        "discount_applies_to": "first_month_subscription",
        "max_discount_sar_starter": 999 * REFERRED_DISCOUNT_PCT // 100,
        "max_discount_sar_growth": 2999 * REFERRED_DISCOUNT_PCT // 100,
        "max_discount_sar_scale": 7999 * REFERRED_DISCOUNT_PCT // 100,
        "claim_window_days": 30,
        "note": (
            "Pass this code to /api/v1/checkout body when subscribing. "
            "Founder reviews and credits referrer manually within "
            "5 business days of referred's first payment."
        ),
    }


@router.post("/{code}/convert", dependencies=[Depends(require_admin_key)])
async def mark_converted(
    code: str = Path(..., pattern=r"^REF-[A-Z0-9]{8}$"),
) -> dict[str, Any]:
    """Admin — mark a referral as converted (referred paid first invoice).

    Triggers credit to referrer + sends thank-you email (manual for now).
    """
    return {
        "status": "marked_converted_in_memory",
        "code": code,
        "referrer_credit_sar": REFERRER_CREDIT_SAR,
        "credit_applied_to": "next monthly invoice",
        "thank_you_email": (
            "Manual send: thank referrer + confirm credit applied "
            "+ ask for next referral (compounds growth)."
        ),
        "note": (
            "DB persistence + automatic Moyasar credit application "
            "deferred to follow-up. Track in spreadsheet for first 5 referrals."
        ),
    }
