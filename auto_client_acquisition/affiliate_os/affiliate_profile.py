"""Affiliate OS — affiliate application + profile schemas.

Placeholder names only. NO real PII is stored in the repo.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AffiliateType = Literal[
    "content_creator",
    "agency",
    "consultant",
    "newsletter",
    "community_operator",
    "saas_reseller",
]
AffiliateStatus = Literal["pending", "approved", "rejected"]
PromoChannel = Literal["newsletter", "blog", "community", "manual_share"]


class AffiliateApplication(BaseModel):
    """An inbound affiliate application. Public-facing intake payload."""

    model_config = ConfigDict(extra="forbid")

    affiliate_id: str = Field(min_length=1, max_length=64)
    placeholder_name: str = Field(min_length=1, max_length=80)
    affiliate_type: AffiliateType
    audience_segment: str = "tbd"
    region: str = "tbd"
    serves_b2b: bool = True
    has_existing_audience: bool = True
    saudi_market_focus: bool = True
    promo_channel: PromoChannel = "manual_share"
    notes_ar: str = ""
    notes_en: str = ""


class Affiliate(BaseModel):
    """A persisted affiliate profile after intake."""

    model_config = ConfigDict(extra="forbid")

    affiliate_id: str = Field(min_length=1, max_length=64)
    placeholder_name: str = Field(min_length=1, max_length=80)
    affiliate_type: AffiliateType
    audience_segment: str = "tbd"
    region: str = "tbd"
    promo_channel: PromoChannel = "manual_share"
    status: AffiliateStatus = "pending"
    fit_score: int = 0
    tier: str = "standard"
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    decided_at: str = ""
    rejected_reason: str = ""


__all__ = [
    "Affiliate",
    "AffiliateApplication",
    "AffiliateStatus",
    "AffiliateType",
    "PromoChannel",
]
