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

    async def approve(self, partner_id: str) -> Partner:
        partner = self._partners.get(partner_id)
        if not partner:
            raise ValueError(f"Partner {partner_id} not found")
        partner.status = "active"
        self.log.info("partner_approved", id=partner_id)
        return partner

    async def get_tier(self, partner_id: str) -> str:
        partner = self._partners.get(partner_id)
        if not partner:
            raise ValueError(f"Partner {partner_id} not found")
        return partner.tier

    async def upgrade_tier(self, partner_id: str) -> Partner:
        partner = self._partners.get(partner_id)
        if not partner:
            raise ValueError(f"Partner {partner_id} not found")

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

        tier_order = ["bronze", "silver", "gold", "platinum"]
        current_idx = tier_order.index(partner.tier)
        min_referrals_map = {"bronze": 0, "silver": 5, "gold": 15, "platinum": 30}

        if current_idx < len(tier_order) - 1:
            next_tier = tier_order[current_idx + 1]
            if partner.total_referrals >= min_referrals_map[next_tier]:
                await self.upgrade_tier(partner_id)

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
