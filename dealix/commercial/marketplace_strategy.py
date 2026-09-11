"""Marketplace Strategy — cloud, app, integration, AI directories."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class MarketplaceType(StrEnum):
    CLOUD = "cloud"
    INTEGRATION = "integration"
    APP = "app"
    AI_DIRECTORY = "ai_directory"
    ERP_ECOSYSTEM = "erp_ecosystem"

class MarketplaceCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    marketplace_id: str
    name: str
    type: MarketplaceType
    buyer_access_score: int = Field(default=3, ge=1, le=5)
    distribution_score: int = Field(default=3, ge=1, le=5)
    support_burden: int = Field(default=3, ge=1, le=5)
    listing_cost_sar: float = 0.0
    commission_pct: float = 0.15

    def score(self) -> float:
        return round((self.buyer_access_score * self.distribution_score) / max(1, self.support_burden + self.commission_pct*10), 3)

class MarketplaceStrategy:
    def __init__(self) -> None:
        self.candidates: list[MarketplaceCandidate] = []

    def add(self, c: MarketplaceCandidate) -> None:
        self.candidates.append(c)

    def rank(self) -> list[MarketplaceCandidate]:
        return sorted(self.candidates, key=lambda x: x.score(), reverse=True)

    def seed_defaults(self) -> None:
        self.add(MarketplaceCandidate(marketplace_id="m1", name="Azure Marketplace", type=MarketplaceType.CLOUD, buyer_access_score=4, distribution_score=4, support_burden=3, commission_pct=0.15))
        self.add(MarketplaceCandidate(marketplace_id="m2", name="AWS Marketplace", type=MarketplaceType.CLOUD, buyer_access_score=4, distribution_score=4, support_burden=3, commission_pct=0.15))
        self.add(MarketplaceCandidate(marketplace_id="m3", name="Odoo Apps", type=MarketplaceType.ERP_ECOSYSTEM, buyer_access_score=3, distribution_score=3, support_burden=2, commission_pct=0.2))

__all__ = ["MarketplaceStrategy", "MarketplaceCandidate", "MarketplaceType"]
