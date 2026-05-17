"""Affiliate OS router — public intake + admin-gated affiliate operations.

Governance verdicts are returned in-band with HTTP 200 (a BLOCKED asset is a
valid outcome, not a server error). Every handler degrades gracefully — a
missing backing module yields ``degraded: true``, never a 5xx.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/affiliate-os", tags=["affiliate_os"])


# ─── Request models ──────────────────────────────────────────────────


class ApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    affiliate_id: str = Field(min_length=1, max_length=64)
    placeholder_name: str = Field(min_length=1, max_length=80)
    affiliate_type: str
    audience_segment: str = "tbd"
    region: str = "tbd"
    serves_b2b: bool = True
    has_existing_audience: bool = True
    saudi_market_focus: bool = True
    promo_channel: str = "manual_share"
    notes_ar: str = ""
    notes_en: str = ""


class AssetSubmitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1, max_length=64)
    affiliate_id: str = Field(min_length=1, max_length=64)
    copy_text: str = Field(min_length=1, max_length=4000)
    locale: str = "en"


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: str  # "approved" | "rejected"
    reason: str = ""


class LinkRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    landing_path: str = "/pricing.html"


class CommissionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    affiliate_id: str = Field(min_length=1, max_length=64)
    referral_code: str = Field(min_length=1, max_length=64)
    invoice_id: str = Field(min_length=1, max_length=80)
    deal_amount_sar: int = Field(gt=0)


class PayoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    commission_id: str = Field(min_length=1, max_length=64)


class PayoutApproveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approver: str = "founder"


# ─── Public endpoints ────────────────────────────────────────────────


@router.get("/status")
async def affiliate_os_status() -> dict[str, Any]:
    """Service status + the hard gates this OS enforces."""
    return {
        "service": "affiliate_os",
        "status": "ok",
        "version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hard_gates": {
            "commission_requires_invoice_paid": True,
            "payout_requires_human_approval": True,
            "no_guaranteed_claims": True,
            "no_real_pii_stored": True,
        },
    }


@router.post("/apply")
async def affiliate_apply(body: ApplyRequest) -> dict[str, Any]:
    """Public affiliate application intake."""
    try:
        from auto_client_acquisition.affiliate_os.affiliate_profile import (
            AffiliateApplication,
        )
        from auto_client_acquisition.affiliate_os.affiliate_store import (
            submit_application,
        )

        application = AffiliateApplication(**body.model_dump())
        affiliate = submit_application(application)
        return {
            "received": True,
            "affiliate": affiliate.model_dump(),
            "governance_decision": "allow",
        }
    except Exception as exc:  # noqa: BLE001
        return {"received": False, "degraded": True, "note": str(exc)}


@router.post("/assets/submit")
async def affiliate_asset_submit(body: AssetSubmitRequest) -> dict[str, Any]:
    """Public: submit promotional copy. Runs the governance claim gates and
    returns the verdict in-band (HTTP 200 even when BLOCKED)."""
    try:
        from auto_client_acquisition.affiliate_os.asset_registry import (
            AssetSubmission,
            review_asset_copy,
        )

        result = review_asset_copy(AssetSubmission(**body.model_dump()))
        approved = result.approved_asset
        return {
            "approved": approved is not None,
            "governance_decision": result.decision.value,
            "issues": list(result.issues),
            "asset": approved.model_dump() if approved else None,
        }
    except Exception as exc:  # noqa: BLE001
        return {"approved": False, "degraded": True, "note": str(exc)}


# ─── Admin-gated ops endpoints ───────────────────────────────────────


@router.get("/affiliates", dependencies=[Depends(require_admin_key)])
async def list_affiliates_endpoint(status: str | None = None) -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os.affiliate_store import (
            list_affiliates,
        )

        items = list_affiliates(status=status)
        return {"count": len(items), "items": [a.model_dump() for a in items]}
    except Exception as exc:  # noqa: BLE001
        return {"count": 0, "items": [], "degraded": True, "note": str(exc)}


@router.post(
    "/affiliates/{affiliate_id}/decision",
    dependencies=[Depends(require_admin_key)],
)
async def decide_affiliate(
    affiliate_id: str, body: DecisionRequest
) -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os.affiliate_store import set_status

        affiliate = set_status(
            affiliate_id=affiliate_id,
            status=body.decision,
            reason=body.reason,
        )
        if affiliate is None:
            return {"updated": False, "note": "affiliate_not_found"}
        return {"updated": True, "affiliate": affiliate.model_dump()}
    except Exception as exc:  # noqa: BLE001
        return {"updated": False, "degraded": True, "note": str(exc)}


@router.post(
    "/affiliates/{affiliate_id}/link",
    dependencies=[Depends(require_admin_key)],
)
async def mint_affiliate_link(
    affiliate_id: str, body: LinkRequest
) -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os.referral_links import (
            build_tracking_url,
            create_affiliate_link,
        )

        link = create_affiliate_link(
            affiliate_id=affiliate_id, landing_path=body.landing_path
        )
        return {
            "created": True,
            "link": link.to_dict(),
            "tracking_url": build_tracking_url(link),
        }
    except ValueError as exc:
        return {"created": False, "note": str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"created": False, "degraded": True, "note": str(exc)}


@router.post("/commissions/calculate", dependencies=[Depends(require_admin_key)])
async def calculate_commission_endpoint(body: CommissionRequest) -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os.commission_engine import (
            calculate_commission,
        )

        commission = calculate_commission(
            affiliate_id=body.affiliate_id,
            referral_code=body.referral_code,
            invoice_id=body.invoice_id,
            deal_amount_sar=body.deal_amount_sar,
        )
        if commission is None:
            return {
                "created": False,
                "reason": "commission_gate_not_met",
                "note": (
                    "no commission — affiliate not approved, link invalid, "
                    "or invoice has no payment-confirmation evidence"
                ),
            }
        return {"created": True, "commission": commission.model_dump()}
    except Exception as exc:  # noqa: BLE001
        return {"created": False, "degraded": True, "note": str(exc)}


@router.post("/payouts/request", dependencies=[Depends(require_admin_key)])
async def request_payout_endpoint(body: PayoutRequest) -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os.payout_gate import request_payout

        payout = request_payout(commission_id=body.commission_id)
        return {"payout": payout.model_dump()}
    except Exception as exc:  # noqa: BLE001
        return {"payout": None, "degraded": True, "note": str(exc)}


@router.post(
    "/payouts/{payout_id}/approve",
    dependencies=[Depends(require_admin_key)],
)
async def approve_payout_endpoint(
    payout_id: str, body: PayoutApproveRequest
) -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os.payout_gate import approve_payout

        payout = approve_payout(payout_id=payout_id, approver=body.approver)
        if payout is None:
            return {"updated": False, "note": "payout_not_found"}
        return {"updated": True, "payout": payout.model_dump()}
    except Exception as exc:  # noqa: BLE001
        return {"updated": False, "degraded": True, "note": str(exc)}


@router.get("/payouts", dependencies=[Depends(require_admin_key)])
async def list_payouts_endpoint(affiliate_id: str | None = None) -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os.payout_gate import list_payouts

        items = list_payouts(affiliate_id=affiliate_id)
        return {"count": len(items), "items": [p.model_dump() for p in items]}
    except Exception as exc:  # noqa: BLE001
        return {"count": 0, "items": [], "degraded": True, "note": str(exc)}
