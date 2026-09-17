"""
Partner Registry — manages partner registration, approval, and tier progression.
سجل الشركاء — يدير تسجيل الشركاء والموافقة والتدرج في المستويات.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class PartnerRegistration:
    company_name_ar: str
    company_name_en: str
    email: str
    phone: str
    commercial_registration: str
    sector_focus: list[str] = field(default_factory=list)
    region: str = "all"
    website: str = ""
    locale: str = "ar"

    def to_dict(self) -> dict[str, Any]:
        return {
            "company_name_ar": self.company_name_ar,
            "company_name_en": self.company_name_en,
            "email": self.email,
            "phone": self.phone,
            "commercial_registration": self.commercial_registration,
            "sector_focus": self.sector_focus,
            "region": self.region,
            "website": self.website,
            "locale": self.locale,
        }


@dataclass
class Partner:
    id: str
    company_name_ar: str
    company_name_en: str
    email: str
    phone: str
    commercial_registration: str
    tier: str = "bronze"
    status: str = "pending"
    total_referrals: int = 0
    total_commission_sar: float = 0.0
    sector_focus: list[str] = field(default_factory=list)
    region: str = "all"
    locale: str = "ar"
    legal_classification_status: str = "unreviewed"
    terms_accepted: bool = False
    certification_passed: bool = False
    tax_profile_recorded: bool = False
    policy_version: str = ""
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "company_name_ar": self.company_name_ar,
            "company_name_en": self.company_name_en,
            "email": self.email,
            "phone": self.phone,
            "commercial_registration": self.commercial_registration,
            "tier": self.tier,
            "status": self.status,
            "total_referrals": self.total_referrals,
            "total_commission_sar": self.total_commission_sar,
            "sector_focus": self.sector_focus,
            "region": self.region,
            "locale": self.locale,
            "legal_classification_status": self.legal_classification_status,
            "terms_accepted": self.terms_accepted,
            "certification_passed": self.certification_passed,
            "tax_profile_recorded": self.tax_profile_recorded,
            "policy_version": self.policy_version,
            "created_at": self.created_at.isoformat(),
        }


class PartnerRegistry:
    TIERS = {"bronze": 0.10, "silver": 0.15, "gold": 0.20, "platinum": 0.25}

    def __init__(self):
        self._partners: dict[str, Partner] = {}
        self.log = logger.bind(component="partner_registry")

    async def register(self, data: PartnerRegistration) -> Partner:
        partner = Partner(
            id=generate_id("prt"),
            company_name_ar=data.company_name_ar,
            company_name_en=data.company_name_en,
            email=data.email,
            phone=data.phone,
            commercial_registration=data.commercial_registration,
            sector_focus=data.sector_focus,
            region=data.region,
            locale=data.locale,
            status="pending",
            tier="bronze",
        )
        self._partners[partner.id] = partner
        self.log.info("partner_registered", id=partner.id, company=data.company_name_en)
        return partner

    async def approve(
        self,
        partner_id: str,
        *,
        legal_classification_status: str,
        terms_accepted: bool,
        certification_passed: bool,
        tax_profile_recorded: bool,
        policy_version: str,
    ) -> Partner:
        """Activate only after the V3 eligibility gates are explicitly satisfied."""
        from dealix.commercial.partner_program_v2 import PARTNER_POLICY_VERSION

        partner = self._partners.get(partner_id)
        if not partner:
            raise ValueError(f"Partner {partner_id} not found")
        reasons = []
        if legal_classification_status != "clear":
            reasons.append("legal_classification_not_clear")
        if not terms_accepted:
            reasons.append("terms_not_accepted")
        if not certification_passed:
            reasons.append("certification_not_passed")
        if not tax_profile_recorded:
            reasons.append("tax_profile_not_recorded")
        if policy_version != PARTNER_POLICY_VERSION:
            reasons.append("policy_version_mismatch")
        if reasons:
            partner.status = "hold"
            raise ValueError("partner_activation_hold:" + ",".join(reasons))

        partner.legal_classification_status = legal_classification_status
        partner.terms_accepted = terms_accepted
        partner.certification_passed = certification_passed
        partner.tax_profile_recorded = tax_profile_recorded
        partner.policy_version = policy_version
        partner.status = "active"
        self.log.info("partner_approved", id=partner_id, policy_version=policy_version)
        return partner

    async def get_tier(self, partner_id: str) -> str:
        partner = self._partners.get(partner_id)
        if not partner:
            raise ValueError(f"Partner {partner_id} not found")
        return partner.tier

    async def upgrade_tier(
        self,
        partner_id: str,
        *,
        verified_economic_quality: bool = False,
        compliance_clear: bool = False,
    ) -> Partner:
        partner = self._partners.get(partner_id)
        if not partner:
            raise ValueError(f"Partner {partner_id} not found")
        if partner.status != "active":
            raise ValueError("partner_not_active")
        if not verified_economic_quality or not compliance_clear:
            raise ValueError("tier_upgrade_requires_verified_economic_quality_and_compliance")

        tier_order = ["bronze", "silver", "gold", "platinum"]
        current_idx = tier_order.index(partner.tier)
        if current_idx >= len(tier_order) - 1:
            self.log.info("partner_already_max_tier", id=partner_id, tier=partner.tier)
            return partner
        partner.tier = tier_order[current_idx + 1]
        self.log.info("partner_upgraded", id=partner_id, new_tier=partner.tier)
        return partner

    async def update_referral_count(self, partner_id: str) -> None:
        partner = self._partners.get(partner_id)
        if not partner:
            return
        partner.total_referrals += 1

        # Referral count is informational only. V3 tier progression requires
        # verified economic quality and a clear compliance record.

    async def add_commission(self, partner_id: str, amount_sar: float) -> None:
        partner = self._partners.get(partner_id)
        if partner:
            partner.total_commission_sar += amount_sar

    def get_partner(self, partner_id: str) -> Partner | None:
        return self._partners.get(partner_id)

    def list_partners(self, status: str | None = None) -> list[Partner]:
        if status:
            return [p for p in self._partners.values() if p.status == status]
        return list(self._partners.values())

    def get_stats(self) -> dict[str, Any]:
        active = sum(1 for p in self._partners.values() if p.status == "active")
        pending = sum(1 for p in self._partners.values() if p.status == "pending")
        return {
            "total": len(self._partners),
            "active": active,
            "pending": pending,
            "by_tier": {
                t: sum(1 for p in self._partners.values() if p.tier == t)
                for t in self.TIERS
            },
            "total_commission_paid": sum(p.total_commission_sar for p in self._partners.values()),
        }
