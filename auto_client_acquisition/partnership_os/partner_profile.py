"""V12 Partnership OS — Partner profile schema."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PartnerType = Literal[
    "marketing_agency",
    "sales_consultant",
    "crm_implementer",
    "hubspot_freelancer",
    "zoho_freelancer",
    "tech_partner_for_smes",
    "consulting_firm",
]


class Partner(BaseModel):
    """A partner profile. Names MUST stay placeholders in the repo."""

    model_config = ConfigDict(extra="forbid")

    partner_id: str = Field(min_length=1, max_length=64)
    placeholder_name: str = Field(min_length=1, max_length=80)
    partner_type: PartnerType
    sector: str = "tbd"
    region: str = "tbd"
    status: Literal["pending", "active", "paused", "rejected"] = "pending"
    notes_ar: str = ""
    notes_en: str = ""
