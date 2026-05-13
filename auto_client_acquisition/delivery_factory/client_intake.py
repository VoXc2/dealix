"""Client Intake — formal entry point into Dealix's 8-stage Delivery Standard.

نظام استقبال العميل — البوابة الرسمية لمعيار التسليم بثماني مراحل.

Captures the minimum scoped information required to (a) match a prospect to
one of the three starting offers (Revenue Intelligence / AI Quick Win / Company
Brain), (b) seed Stage 1 (Discover) of the Delivery Standard, and (c) write a
StageEntered event to the event store so the project is auditable from minute
zero.

Pure module (no DB writes). The router layer persists results.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from core.logging import get_logger

log = get_logger(__name__)


class StartingOffer(StrEnum):
    """The three canonical entry points (per docs/strategy/three_starting_offers.md)."""

    REVENUE_INTELLIGENCE = "revenue_intelligence_sprint"
    AI_QUICK_WIN = "ai_quick_win_sprint"
    COMPANY_BRAIN = "company_brain_sprint"


class CustomerTier(StrEnum):
    SME = "sme"
    MID_MARKET = "mid_market"
    ENTERPRISE = "enterprise"
    SOVEREIGN = "sovereign"


class Vertical(StrEnum):
    BFSI = "bfsi"
    RETAIL_ECOMM = "retail_ecomm"
    HEALTHCARE = "healthcare"
    LOGISTICS = "logistics"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"
    HOSPITALITY = "hospitality"
    PROFESSIONAL_SERVICES = "professional_services"
    OTHER = "other"


class IntakeRequest(BaseModel):
    """Information captured at first prospect contact."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    company_name_ar: str = Field(min_length=1, max_length=200)
    company_name_en: str | None = None
    commercial_registration: str | None = Field(default=None, description="السجل التجاري")
    vat_number: str | None = None
    vertical: Vertical
    tier: CustomerTier
    region: str = Field(default="riyadh", description="City code, e.g. riyadh|jeddah|khobar")
    headcount: int | None = Field(default=None, ge=0)
    annual_revenue_sar: float | None = Field(default=None, ge=0)
    primary_pain_ar: str = Field(min_length=1, max_length=500)
    primary_pain_en: str | None = None
    requested_offer: StartingOffer
    contact_name: str
    contact_role: str
    contact_email: str
    contact_phone: str | None = None
    pdpl_acknowledged: bool = Field(
        default=False,
        description="Customer acknowledges PDPL Art. 13 notice — required to proceed",
    )


class IntakeResult(BaseModel):
    """What we return to the requester (and persist as the project seed)."""

    model_config = ConfigDict(use_enum_values=True)

    project_id: str = Field(default_factory=lambda: f"prj_{uuid4().hex[:12]}")
    intake_id: str = Field(default_factory=lambda: f"intk_{uuid4().hex[:12]}")
    accepted: bool
    rejection_reason_ar: str | None = None
    rejection_reason_en: str | None = None
    matched_offer: StartingOffer | None = None
    estimated_price_sar: int | None = None
    estimated_duration_days: int | None = None
    next_stage: str = "discover"
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


_OFFER_PRICING_SAR: dict[StartingOffer, tuple[int, int]] = {
    StartingOffer.REVENUE_INTELLIGENCE: (9_500, 10),
    StartingOffer.AI_QUICK_WIN: (12_000, 7),
    StartingOffer.COMPANY_BRAIN: (20_000, 21),
}


def _disqualification_reason(intake: IntakeRequest) -> tuple[str, str] | None:
    """Apply the deal-breaker rules from docs/go-to-market/icp_saudi.md §3.2.

    Returns (reason_ar, reason_en) if disqualified, else None.
    """
    if not intake.pdpl_acknowledged:
        return (
            "إقرار PDPL مطلوب قبل تشغيل أي إجراء خارجي.",
            "PDPL acknowledgement is required before any outbound action can run.",
        )
    if not intake.commercial_registration and intake.tier in (
        CustomerTier.ENTERPRISE,
        CustomerTier.SOVEREIGN,
    ):
        return (
            "السجل التجاري مطلوب للمؤسسات.",
            "Commercial Registration required for Enterprise / Sovereign tiers.",
        )
    if (
        intake.tier == CustomerTier.ENTERPRISE
        and not intake.vat_number
    ):
        return (
            "الرقم الضريبي (VAT) مطلوب للمؤسسات.",
            "VAT registration required for Enterprise tier.",
        )
    if intake.annual_revenue_sar is not None and intake.annual_revenue_sar < 5_000_000 and intake.tier != CustomerTier.SME:
        return (
            "إيراد سنوي < 5 مليون ريال — يُفضّل التواصل عبر باقة SME.",
            "Annual revenue < SAR 5M — route to SME tier instead.",
        )
    return None


def process_intake(intake: IntakeRequest) -> IntakeResult:
    """Validate intake against the ICP and produce a project seed.

    This function is pure: it does not persist to DB and does not call out to
    the event store. The router layer is responsible for both. We keep it pure
    so it is trivially testable.
    """
    log.info(
        "intake_received",
        company=intake.company_name_ar,
        vertical=intake.vertical,
        tier=intake.tier,
        requested_offer=intake.requested_offer,
    )

    disq = _disqualification_reason(intake)
    if disq:
        reason_ar, reason_en = disq
        log.info("intake_rejected", reason=reason_en)
        return IntakeResult(
            accepted=False,
            rejection_reason_ar=reason_ar,
            rejection_reason_en=reason_en,
            matched_offer=None,
        )

    price, duration = _OFFER_PRICING_SAR[intake.requested_offer]
    return IntakeResult(
        accepted=True,
        matched_offer=intake.requested_offer,
        estimated_price_sar=price,
        estimated_duration_days=duration,
    )


def intake_summary(intake: IntakeRequest, result: IntakeResult) -> dict[str, Any]:
    """Bilingual summary written into the Discover-stage artifact."""
    return {
        "schema_version": 1,
        "project_id": result.project_id,
        "intake_id": result.intake_id,
        "company": {
            "name_ar": intake.company_name_ar,
            "name_en": intake.company_name_en,
            "cr": intake.commercial_registration,
            "vat": intake.vat_number,
            "vertical": intake.vertical,
            "tier": intake.tier,
            "region": intake.region,
        },
        "scope": {
            "pain_ar": intake.primary_pain_ar,
            "pain_en": intake.primary_pain_en,
            "offer": result.matched_offer,
            "price_sar": result.estimated_price_sar,
            "duration_days": result.estimated_duration_days,
        },
        "compliance": {
            "pdpl_acknowledged": intake.pdpl_acknowledged,
            "lawful_basis": "PDPL Art. 5 — contract (services engagement)",
        },
        "accepted": result.accepted,
        "rejection_reason_ar": result.rejection_reason_ar,
        "rejection_reason_en": result.rejection_reason_en,
        "created_at": result.created_at,
    }
