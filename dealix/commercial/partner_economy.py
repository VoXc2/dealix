"""Partner Economy — referral, co-sell, white-label, SI, consultancies, cloud."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class PartnerType(StrEnum):
    SYSTEM_INTEGRATOR = "system_integrator"
    CONSULTANCY = "consultancy"
    AGENCY = "agency"
    CLOUD_PROVIDER = "cloud_provider"
    ERP_VENDOR = "erp_vendor"
    CYBER_FIRM = "cyber_firm"
    ACCOUNTING = "accounting"
    INDUSTRY_SPECIALIST = "industry_specialist"
    DISTRIBUTOR = "distributor"

class PartnerMotion(StrEnum):
    REFERRAL = "referral"
    CO_SELL = "co_sell"
    WHITE_LABEL = "white_label"
    IMPLEMENTATION = "implementation"
    SUBCONTRACTOR = "subcontractor"
    INTEGRATION = "integration"

class PartnerCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    partner_id: str
    name: str
    type: PartnerType
    motion: PartnerMotion = PartnerMotion.REFERRAL
    sector_fit: list[str] = Field(default_factory=list)
    access_score: int = Field(default=3, ge=1, le=5)
    capability_score: int = Field(default=3, ge=1, le=5)
    trust_score: int = Field(default=3, ge=1, le=5)
    margin_share_pct: float = 0.15
    win_rate: float = Field(default=0.3, ge=0.0, le=1.0)
    sales_cycle_days: int = 45
    proof_reuse: int = Field(default=2, ge=0, le=5)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def economic_score(self) -> float:
        # access*capability*trust*win_rate*proof / (margin_share + cycle)
        numerator = self.access_score * self.capability_score * self.trust_score * self.win_rate * (self.proof_reuse+1)
        denominator = self.margin_share_pct*10 + self.sales_cycle_days/30
        return round(numerator / max(1, denominator), 3)

class PartnerEconomy:
    def __init__(self) -> None:
        self.partners: list[PartnerCandidate] = []

    def add(self, p: PartnerCandidate) -> None:
        self.partners.append(p)

    def rank(self) -> list[PartnerCandidate]:
        return sorted(self.partners, key=lambda x: x.economic_score(), reverse=True)

    def seed_defaults(self) -> None:
        self.add(PartnerCandidate(partner_id="p1", name="Cloud Provider (Riyadh)", type=PartnerType.CLOUD_PROVIDER, motion=PartnerMotion.CO_SELL, sector_fit=["technology_saas_si","finance"], access_score=5, capability_score=4, trust_score=4, margin_share_pct=0.15, win_rate=0.4, proof_reuse=3))
        self.add(PartnerCandidate(partner_id="p2", name="Big4 Consultancy", type=PartnerType.CONSULTANCY, motion=PartnerMotion.REFERRAL, sector_fit=["government_b2g","finance"], access_score=4, capability_score=5, trust_score=5, margin_share_pct=0.2, win_rate=0.35, proof_reuse=4))
        self.add(PartnerCandidate(partner_id="p3", name="ERP Implementer", type=PartnerType.ERP_VENDOR, motion=PartnerMotion.IMPLEMENTATION, sector_fit=["industrial","construction"], access_score=4, capability_score=4, trust_score=3, margin_share_pct=0.18, win_rate=0.3, proof_reuse=2))

    def to_dict(self) -> dict[str, Any]:
        return {"ranked": [(p.partner_id, p.economic_score()) for p in self.rank()], "total": len(self.partners)}

__all__ = ["PartnerEconomy", "PartnerCandidate", "PartnerType", "PartnerMotion", "UNKNOWN"]
