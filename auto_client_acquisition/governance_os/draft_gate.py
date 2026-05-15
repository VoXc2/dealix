"""Draft and intake governance helpers (delegates to Revenue OS anti-waste where useful)."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step
from auto_client_acquisition.revenue_os.source_registry import Tier1LeadSource


def audit_draft_text(text: str) -> list[str]:
    """
    Flag risky phrases in **draft** marketing or outreach copy.

    This is a shallow guardrail — human review remains mandatory.
    """
    issues: list[str] = []
    blob = text.lower()
    forbidden_terms = (
        "scraping",
        "scrape ",
        "purchased list",
        "cold whatsapp",
        "linkedin automation",
        "auto-send",
        "auto send",
        "send automatically without approval",
    )
    for term in forbidden_terms:
        if term in blob:
            issues.append(f"forbidden_term:{term}")
    guarantee_or_misrep = (
        "guaranteed sales",
        "guaranteed results",
        "guaranteed roi",
        "guarantee roi",
        "we guarantee",
        "نضمن",
        "نضمن لك",
        "نضمن لكم",
        "نضمن النتائج",
        "نضمن لك مبيعات",
        "fake proof",
        "fake testimonial",
    )
    for term in guarantee_or_misrep:
        if term in blob:
            issues.append(f"forbidden_claim:{term}")
    return issues


def intake_violations_for_source(lead_source: str) -> list[str]:
    """Anti-waste intake check on a lead source string (e.g. Tier1 value)."""
    vio = validate_pipeline_step(
        has_decision_passport=False,
        lead_source=lead_source,
        action_external=False,
        upsell_attempt=False,
        proof_event_count=0,
        evidence_level_for_public=0,
        public_marketing_attempt=False,
        feature_request_count=0,
    )
    if vio:
        return [f"{v.code}:{v.detail_en}" for v in vio]
    try:
        Tier1LeadSource(lead_source)
    except ValueError:
        return [f"unknown_tier1_source:{lead_source}"]
    return []
