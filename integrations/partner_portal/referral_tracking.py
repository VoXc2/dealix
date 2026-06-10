"""
Referral Tracking — tracks partner referrals through the pipeline.
تتبع الإحالات — يتتبع إحالات الشركاء عبر مسار المبيعات.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


class ReferralStage(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


@dataclass
class ReferralData:
    company_name: str
    contact_name: str
    contact_email: str
    contact_phone: str = ""
    sector: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "sector": self.sector,
            "notes": self.notes,
        }


@dataclass
class ConversionResult:
    success: bool
    referral_id: str
    deal_value_sar: float = 0.0
    commission_amount_sar: float = 0.0
    commission_rate: float = 0.0
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "referral_id": self.referral_id,
            "deal_value_sar": self.deal_value_sar,
            "commission_amount_sar": self.commission_amount_sar,
            "commission_rate": self.commission_rate,
            "notes": self.notes,
        }


@dataclass
class Referral:
    id: str
    partner_id: str
    company_name: str
    contact_name: str
    contact_email: str
    contact_phone: str = ""
    sector: str = ""
    notes: str = ""
    stage: ReferralStage = ReferralStage.NEW
    deal_value_sar: float = 0.0
    commission_rate: float = 0.10
    commission_amount_sar: float = 0.0
    created_at: datetime = field(default_factory=utcnow)
    converted_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "partner_id": self.partner_id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "sector": self.sector,
            "notes": self.notes,
            "stage": self.stage.value,
            "deal_value_sar": self.deal_value_sar,
            "commission_rate": self.commission_rate,
            "commission_amount_sar": self.commission_amount_sar,
            "created_at": self.created_at.isoformat(),
            "converted_at": self.converted_at.isoformat() if self.converted_at else None,
        }


class ReferralTracker:
    def __init__(self):
        self._referrals: dict[str, Referral] = {}
        self.log = logger.bind(component="referral_tracker")

    async def create_referral(self, partner_id: str, data: ReferralData) -> Referral:
        referral = Referral(
            id=generate_id("ref"),
            partner_id=partner_id,
            company_name=data.company_name,
            contact_name=data.contact_name,
            contact_email=data.contact_email,
            contact_phone=data.contact_phone,
            sector=data.sector,
            notes=data.notes,
            stage=ReferralStage.NEW,
        )
        self._referrals[referral.id] = referral
        self.log.info("referral_created", id=referral.id, partner_id=partner_id, company=data.company_name)
        return referral

    async def convert(self, referral_id: str, deal_value: float) -> ConversionResult:
        referral = self._referrals.get(referral_id)
        if not referral:
            return ConversionResult(success=False, referral_id=referral_id, notes="Referral not found")

        if referral.stage == ReferralStage.WON:
            return ConversionResult(success=False, referral_id=referral_id, notes="Already converted")

        commission_amount = deal_value * referral.commission_rate

        referral.stage = ReferralStage.WON
        referral.deal_value_sar = deal_value
        referral.commission_amount_sar = commission_amount
        referral.converted_at = utcnow()

        result = ConversionResult(
            success=True,
            referral_id=referral_id,
            deal_value_sar=deal_value,
            commission_amount_sar=commission_amount,
            commission_rate=referral.commission_rate,
            notes="Referral converted successfully",
        )

        self.log.info(
            "referral_converted",
            id=referral_id,
            deal_value=deal_value,
            commission=commission_amount,
        )
        return result

    async def update_stage(self, referral_id: str, stage: ReferralStage) -> Referral | None:
        referral = self._referrals.get(referral_id)
        if not referral:
            return None
        referral.stage = stage
        return referral

    async def get_pipeline(self, partner_id: str) -> list[Referral]:
        return [r for r in self._referrals.values() if r.partner_id == partner_id]

    def get_referral(self, referral_id: str) -> Referral | None:
        return self._referrals.get(referral_id)

    def list_referrals(self, stage: ReferralStage | None = None) -> list[Referral]:
        if stage:
            return [r for r in self._referrals.values() if r.stage == stage]
        return list(self._referrals.values())

    def get_stats(self) -> dict[str, Any]:
        referrals = self._referrals.values()
        return {
            "total": len(referrals),
            "by_stage": {
                s.value: sum(1 for r in referrals if r.stage == s)
                for s in ReferralStage
            },
            "total_deal_value": sum(r.deal_value_sar for r in referrals if r.stage == ReferralStage.WON),
            "total_commission": sum(r.commission_amount_sar for r in referrals if r.stage == ReferralStage.WON),
            "conversion_rate": (
                sum(1 for r in referrals if r.stage == ReferralStage.WON) / len(referrals) * 100
                if referrals else 0.0
            ),
        }
