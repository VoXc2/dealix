"""Tier-1 Lead Machine — Source Registry (allowed_use, risk, consent)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Tier1LeadSource(StrEnum):
    """Known ingestion sources — every lead MUST map to one."""

    WARM_INTRO = "warm_intro"
    PARTNER_REFERRAL = "partner_referral"
    INBOUND_FORM = "inbound_form"
    INBOUND_WHATSAPP = "inbound_whatsapp"
    CUSTOMER_CSV = "customer_uploaded_csv"
    CRM_IMPORT = "crm_import"
    GOOGLE_SHEET = "google_sheet"
    MANUAL_LINKEDIN_RESEARCH = "manual_linkedin_research"
    WEBSITE_INQUIRY = "website_inquiry"
    EVENT_LIST_PERMISSION = "event_list_with_permission"
    PUBLIC_BUSINESS_INFO_ALLOWED = "public_business_info_allowed"
    FOUNDER_OBSERVATION = "founder_observation"
    INBOUND = "inbound"
    # Forbidden aliases — registry lists them with blocked flags
    PURCHASED_LIST = "purchased_list"
    SCRAPING = "scraping"
    COLD_WHATSAPP = "cold_whatsapp"
    LINKEDIN_AUTOMATION = "linkedin_automation"


@dataclass(frozen=True)
class SourcePolicy:
    allowed_use: str  # marketing_ops | sales_qualification | internal_only | blocked
    risk_level: str  # low | medium | high | blocked
    consent_required: bool
    can_store: bool
    can_enrich: bool
    can_contact: bool
    retention_policy: str  # human-readable policy key


_POLICIES: dict[Tier1LeadSource, SourcePolicy] = {
    Tier1LeadSource.WARM_INTRO: SourcePolicy(
        "sales_qualification", "low", False, True, True, True, "standard_b2b_24m"
    ),
    Tier1LeadSource.PARTNER_REFERRAL: SourcePolicy(
        "sales_qualification", "low", False, True, True, True, "standard_b2b_24m"
    ),
    Tier1LeadSource.INBOUND_FORM: SourcePolicy(
        "sales_qualification", "low", True, True, True, True, "consent_scope_form"
    ),
    Tier1LeadSource.INBOUND_WHATSAPP: SourcePolicy(
        "sales_qualification", "medium", True, True, True, True, "consent_inbound_thread"
    ),
    Tier1LeadSource.CUSTOMER_CSV: SourcePolicy(
        "sales_qualification", "medium", True, True, True, True, "customer_dpa_scope"
    ),
    Tier1LeadSource.CRM_IMPORT: SourcePolicy(
        "sales_qualification", "medium", True, True, True, True, "crm_license_scope"
    ),
    Tier1LeadSource.GOOGLE_SHEET: SourcePolicy(
        "sales_qualification", "medium", True, True, True, True, "sheet_owner_consent"
    ),
    Tier1LeadSource.MANUAL_LINKEDIN_RESEARCH: SourcePolicy(
        "sales_qualification", "medium", False, True, True, True, "manual_public_profile_only"
    ),
    Tier1LeadSource.WEBSITE_INQUIRY: SourcePolicy(
        "sales_qualification", "low", True, True, True, True, "consent_scope_form"
    ),
    Tier1LeadSource.EVENT_LIST_PERMISSION: SourcePolicy(
        "sales_qualification", "medium", True, True, True, True, "event_opt_in"
    ),
    Tier1LeadSource.PUBLIC_BUSINESS_INFO_ALLOWED: SourcePolicy(
        "sales_qualification", "low", False, True, True, True, "public_registry_only"
    ),
    Tier1LeadSource.FOUNDER_OBSERVATION: SourcePolicy(
        "internal_only", "low", False, True, False, False, "founder_notes_12m"
    ),
    Tier1LeadSource.INBOUND: SourcePolicy(
        "sales_qualification", "low", True, True, True, True, "consent_scope_general"
    ),
    Tier1LeadSource.PURCHASED_LIST: SourcePolicy(
        "blocked", "blocked", True, False, False, False, "do_not_process"
    ),
    Tier1LeadSource.SCRAPING: SourcePolicy(
        "blocked", "blocked", True, False, False, False, "do_not_process"
    ),
    Tier1LeadSource.COLD_WHATSAPP: SourcePolicy(
        "blocked", "blocked", True, False, False, False, "do_not_process"
    ),
    Tier1LeadSource.LINKEDIN_AUTOMATION: SourcePolicy(
        "blocked", "blocked", True, False, False, False, "do_not_process"
    ),
}


def source_policies() -> dict[str, dict[str, object]]:
    """Serializable registry for APIs."""
    out: dict[str, dict[str, object]] = {}
    for src, pol in _POLICIES.items():
        out[src.value] = {
            "allowed_use": pol.allowed_use,
            "risk_level": pol.risk_level,
            "consent_required": pol.consent_required,
            "can_store": pol.can_store,
            "can_enrich": pol.can_enrich,
            "can_contact": pol.can_contact,
            "retention_policy": pol.retention_policy,
        }
    return out


def forbidden_sources() -> list[str]:
    return [s.value for s in Tier1LeadSource if _POLICIES[s].allowed_use == "blocked"]


def get_source_policy(source: Tier1LeadSource) -> SourcePolicy:
    """Return the frozen policy row for a Tier-1 source."""
    return _POLICIES[source]
