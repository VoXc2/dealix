"""
Saudi targeting profile — ICP-shaped input for local discovery + Tier1 bridge.

Maps ``Tier1LeadSource`` (Revenue OS registry) to ``LeadSource`` (intake pipeline)
and builds safe bodies for ``POST /api/v1/leads/discover/local``.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from auto_client_acquisition.agents.intake import LeadSource
from auto_client_acquisition.connectors.google_maps import INDUSTRY_QUERIES, SAUDI_CITIES
from auto_client_acquisition.revenue_os.anti_waste import AntiWasteViolation, validate_pipeline_step
from auto_client_acquisition.revenue_os.source_registry import Tier1LeadSource, get_source_policy


class SaudiTargetingProfile(BaseModel):
    """Structured ICP slice for Saudi local Places discovery (no scraping)."""

    industry_key: str = Field(
        ...,
        description="Key in INDUSTRY_QUERIES (e.g. dental_clinic, logistics).",
    )
    city_key: str = Field(
        ...,
        description="Key in SAUDI_CITIES (e.g. riyadh, jeddah).",
    )
    max_results: int = Field(default=20, ge=1, le=40)
    hydrate_details: bool = True
    query_lang: Literal["ar", "en", "mixed"] = "mixed"
    signal_keywords: list[str] = Field(
        default_factory=list,
        description="Optional extra tokens appended to custom_query (founder-provided, no web fetch).",
    )
    custom_query_override: str | None = Field(
        default=None,
        max_length=500,
        description="If set, used as custom_query for Places text search.",
    )

    @field_validator("industry_key")
    @classmethod
    def _industry_must_exist(cls, v: str) -> str:
        key = v.strip()
        if key not in INDUSTRY_QUERIES:
            allowed = ", ".join(sorted(INDUSTRY_QUERIES.keys())[:12]) + ", …"
            raise ValueError(f"unknown industry_key={key!r}; examples: {allowed}")
        return key

    @field_validator("city_key")
    @classmethod
    def _city_must_exist(cls, v: str) -> str:
        key = v.strip().lower()
        if key not in SAUDI_CITIES:
            raise ValueError(
                f"unknown city_key={key!r}; allowed: {', '.join(sorted(SAUDI_CITIES.keys()))}"
            )
        return key

    @field_validator("signal_keywords")
    @classmethod
    def _cap_keywords(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for x in v[:12]:
            s = str(x).strip()
            if s and s not in out:
                out.append(s)
        return out


def build_local_discover_body(profile: SaudiTargetingProfile) -> dict[str, Any]:
    """Build JSON body for ``POST /api/v1/leads/discover/local``."""
    body: dict[str, Any] = {
        "industry": profile.industry_key,
        "city": profile.city_key,
        "max_results": profile.max_results,
        "hydrate_details": profile.hydrate_details,
    }
    if profile.custom_query_override:
        body["custom_query"] = profile.custom_query_override.strip()
        return body

    if profile.signal_keywords:
        ar_city, _en_city = SAUDI_CITIES[profile.city_key]
        seed_q = INDUSTRY_QUERIES[profile.industry_key][0]
        extra = " ".join(profile.signal_keywords)
        body["custom_query"] = f"{seed_q} {ar_city} {extra}".strip()
    return body


def merge_targeting_into_discover_body(body: dict[str, Any]) -> dict[str, Any]:
    """
    If ``body`` contains ``targeting_profile`` (dict), merge derived discover fields.

    Explicit ``industry`` / ``city`` / ``custom_query`` on ``body`` win over profile defaults.
    """
    raw = body.get("targeting_profile")
    if raw is None:
        return body
    if not isinstance(raw, dict):
        raise ValueError("targeting_profile_must_be_object")

    profile = SaudiTargetingProfile.model_validate(raw)
    derived = build_local_discover_body(profile)
    out = {**body}
    out.pop("targeting_profile", None)
    for k, v in derived.items():
        if k not in out or out[k] in (None, "", []):
            out[k] = v
    return out


def parse_tier1_lead_source(value: str) -> Tier1LeadSource:
    try:
        return Tier1LeadSource(str(value).strip())
    except ValueError as e:
        raise ValueError(f"invalid_tier1_source:{value}") from e


def assert_tier1_storage_allowed(tier1: Tier1LeadSource) -> None:
    pol = get_source_policy(tier1)
    if pol.allowed_use == "blocked" or not pol.can_store:
        raise ValueError(f"source_not_storable:{tier1.value}")


def map_tier1_to_intake_lead_source(tier1: Tier1LeadSource) -> LeadSource:
    """Deterministic bridge: Tier1 registry → intake ``LeadSource``."""
    mapping: dict[Tier1LeadSource, LeadSource] = {
        Tier1LeadSource.WARM_INTRO: LeadSource.REFERRAL,
        Tier1LeadSource.PARTNER_REFERRAL: LeadSource.REFERRAL,
        Tier1LeadSource.INBOUND_FORM: LeadSource.WEBSITE,
        Tier1LeadSource.INBOUND_WHATSAPP: LeadSource.WHATSAPP,
        Tier1LeadSource.CUSTOMER_CSV: LeadSource.API,
        Tier1LeadSource.CRM_IMPORT: LeadSource.API,
        Tier1LeadSource.GOOGLE_SHEET: LeadSource.API,
        Tier1LeadSource.MANUAL_LINKEDIN_RESEARCH: LeadSource.LINKEDIN,
        Tier1LeadSource.WEBSITE_INQUIRY: LeadSource.WEBSITE,
        Tier1LeadSource.EVENT_LIST_PERMISSION: LeadSource.API,
        Tier1LeadSource.PUBLIC_BUSINESS_INFO_ALLOWED: LeadSource.MANUAL,
        Tier1LeadSource.FOUNDER_OBSERVATION: LeadSource.MANUAL,
        Tier1LeadSource.INBOUND: LeadSource.WEBSITE,
        Tier1LeadSource.PURCHASED_LIST: LeadSource.MANUAL,  # blocked before mapping in practice
        Tier1LeadSource.SCRAPING: LeadSource.MANUAL,
        Tier1LeadSource.COLD_WHATSAPP: LeadSource.WHATSAPP,
        Tier1LeadSource.LINKEDIN_AUTOMATION: LeadSource.LINKEDIN,
    }
    return mapping[tier1]


def anti_waste_violations_for_tier1_intake(tier1: Tier1LeadSource) -> list[AntiWasteViolation]:
    """Intake-only check: blocked sources and golden-chain hygiene defaults."""
    return validate_pipeline_step(
        has_decision_passport=False,
        lead_source=tier1.value,
        action_external=False,
        upsell_attempt=False,
        proof_event_count=0,
        evidence_level_for_public=0,
        public_marketing_attempt=False,
        feature_request_count=0,
    )
