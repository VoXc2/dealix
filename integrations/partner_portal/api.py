"""
Partner Portal API — all partner distribution endpoints.
واجهة برمجة تطبيقات بوابة الشركاء — جميع نقاط نهاية توزيع الشركاء.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from integrations.partner_portal.commission_engine import CommissionEngine
from integrations.partner_portal.partner_registry import PartnerRegistration, PartnerRegistry
from integrations.partner_portal.referral_tracking import ReferralData, ReferralStage, ReferralTracker
from integrations.partner_portal.white_label_config import Theme, WLConfig, WhiteLabelConfig

router = APIRouter(prefix="/api/v1/partners", tags=["partner-portal"])

_registry = PartnerRegistry()
_tracker = ReferralTracker()
_commission = CommissionEngine()
_white_label = WhiteLabelConfig()

_HARD_GATES = {
    "no_auto_approve": True,
    "no_auto_pay": True,
    "approval_required_for_payment": True,
}


class PartnerRegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company_name_ar: str = Field(..., min_length=2, max_length=100)
    company_name_en: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    phone: str = Field(..., min_length=8, max_length=20)
    commercial_registration: str = Field(..., min_length=5, max_length=50)
    sector_focus: list[str] = Field(default_factory=list)
    region: str = "all"
    website: str = ""
    locale: str = "ar"


class ReferralCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_id: str
    company_name: str
    contact_name: str
    contact_email: str
    contact_phone: str = ""
    sector: str = ""
    notes: str = ""


class ReferralConvertRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    deal_value_sar: float = Field(..., gt=0)


class CommissionPayRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    commission_id: str


class WLConfigRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_id: str
    subdomain: str = Field(..., pattern=r"^[a-z0-9-]+$")
    company_name_ar: str
    company_name_en: str
    custom_domain: str = ""
    locale: str = "ar"


class ThemeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_id: str
    primary_color: str = "#1a1a2e"
    secondary_color: str = "#e94560"
    accent_color: str = "#0f3460"
    logo_url: str = ""
    favicon_url: str = ""


@router.post("/register")
async def register_partner(body: PartnerRegisterRequest) -> dict[str, Any]:
    data = PartnerRegistration(
        company_name_ar=body.company_name_ar,
        company_name_en=body.company_name_en,
        email=body.email,
        phone=body.phone,
        commercial_registration=body.commercial_registration,
        sector_focus=body.sector_focus,
        region=body.region,
        website=body.website,
        locale=body.locale,
    )
    partner = await _registry.register(data)
    return {"status": "registered", "partner": partner.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/partners")
async def list_partners(status: str | None = None) -> dict[str, Any]:
    partners = _registry.list_partners(status)
    return {
        "count": len(partners),
        "partners": [p.to_dict() for p in partners],
        "stats": _registry.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/partners/{partner_id}")
async def get_partner(partner_id: str) -> dict[str, Any]:
    partner = _registry.get_partner(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"partner": partner.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/partners/{partner_id}/approve")
async def approve_partner(partner_id: str) -> dict[str, Any]:
    try:
        partner = await _registry.approve(partner_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "approved", "partner": partner.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/partners/{partner_id}/upgrade")
async def upgrade_partner(partner_id: str) -> dict[str, Any]:
    try:
        partner = await _registry.upgrade_tier(partner_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "upgraded", "partner": partner.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/referrals/create")
async def create_referral(body: ReferralCreateRequest) -> dict[str, Any]:
    partner = _registry.get_partner(body.partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    data = ReferralData(
        company_name=body.company_name,
        contact_name=body.contact_name,
        contact_email=body.contact_email,
        contact_phone=body.contact_phone,
        sector=body.sector,
        notes=body.notes,
    )
    referral = await _tracker.create_referral(body.partner_id, data)
    await _registry.update_referral_count(body.partner_id)
    return {"status": "created", "referral": referral.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/referrals")
async def list_referrals(stage: str | None = None) -> dict[str, Any]:
    stage_enum = ReferralStage(stage) if stage else None
    referrals = _tracker.list_referrals(stage_enum)
    return {
        "count": len(referrals),
        "referrals": [r.to_dict() for r in referrals],
        "stats": _tracker.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/referrals/partner/{partner_id}")
async def partner_pipeline(partner_id: str) -> dict[str, Any]:
    referrals = await _tracker.get_pipeline(partner_id)
    return {
        "partner_id": partner_id,
        "count": len(referrals),
        "referrals": [r.to_dict() for r in referrals],
        "hard_gates": _HARD_GATES,
    }


@router.post("/referrals/{referral_id}/convert")
async def convert_referral(referral_id: str, body: ReferralConvertRequest) -> dict[str, Any]:
    result = await _tracker.convert(referral_id, body.deal_value_sar)
    if result.success:
        commission = await _commission.calculate(referral_id)
        await _registry.add_commission(commission.partner_id, commission.amount_sar)
    return {"conversion": result.to_dict(), "commission": commission.to_dict() if result.success else None, "hard_gates": _HARD_GATES}


@router.get("/commissions")
async def list_commissions(partner_id: str | None = None) -> dict[str, Any]:
    if partner_id:
        commissions = await _commission.get_history(partner_id)
    else:
        commissions = []
    return {
        "count": len(commissions),
        "commissions": [c.to_dict() for c in commissions],
        "stats": _commission.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/commissions/{commission_id}/pay")
async def pay_commission(commission_id: str) -> dict[str, Any]:
    result = await _commission.pay(commission_id)
    return {"payment": result.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/tiers")
async def list_tiers(locale: str = "en") -> dict[str, Any]:
    from integrations.partner_portal.partner_tiers import PARTNER_TIERS
    tiers = {}
    for name, info in PARTNER_TIERS.items():
        tiers[name] = {
            "commission_rate": info["commission_rate"],
            "min_referrals": info["min_referrals"],
            "features": info.get(f"benefits_ar" if locale == "ar" else "features", info["features"]),
            "commission_payout": info["commission_payout"],
            "support_level": info["support_level"],
            "white_label": info["white_label"],
        }
    return {"tiers": tiers, "hard_gates": _HARD_GATES}


@router.post("/white-label/create")
async def create_white_label(body: WLConfigRequest) -> dict[str, Any]:
    partner = _registry.get_partner(body.partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    config = WLConfig(
        partner_id=body.partner_id,
        subdomain=body.subdomain,
        company_name_ar=body.company_name_ar,
        company_name_en=body.company_name_en,
        custom_domain=body.custom_domain,
        locale=body.locale,
    )
    instance = await _white_label.create(body.partner_id, config)
    return {"status": "created", "instance": instance.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/white-label/domain/{partner_id}")
async def get_white_label_domain(partner_id: str) -> dict[str, Any]:
    try:
        domain = await _white_label.get_domain(partner_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"partner_id": partner_id, "domain": domain, "hard_gates": _HARD_GATES}


@router.post("/white-label/theme")
async def apply_theme(body: ThemeRequest) -> dict[str, Any]:
    theme = Theme(
        primary_color=body.primary_color,
        secondary_color=body.secondary_color,
        accent_color=body.accent_color,
        logo_url=body.logo_url,
        favicon_url=body.favicon_url,
    )
    try:
        await _white_label.apply_theme(body.partner_id, theme)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "theme_applied", "partner_id": body.partner_id, "hard_gates": _HARD_GATES}
