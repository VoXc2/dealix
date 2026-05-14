"""Governance pressure → moat artifacts (rules, trust, product guardrails)."""

from __future__ import annotations

GOVERNANCE_TO_MOAT_STAGES: tuple[str, ...] = (
    "risk_recorded",
    "rule_versioned",
    "automated_test",
    "checklist",
    "sales_objection_response",
    "trust_page",
    "product_guardrail",
)


def governance_to_moat_progress(completed_stages: frozenset[str]) -> tuple[int, tuple[str, ...]]:
    done = sum(1 for s in GOVERNANCE_TO_MOAT_STAGES if s in completed_stages)
    missing = tuple(s for s in GOVERNANCE_TO_MOAT_STAGES if s not in completed_stages)
    return done, missing


def governance_moat_loop_complete(completed_stages: frozenset[str]) -> bool:
    return all(s in completed_stages for s in GOVERNANCE_TO_MOAT_STAGES)


def risk_to_seed_artifacts(risk_type: str) -> tuple[str, ...]:
    """Map a coarse risk label to first artifacts to create."""
    key = risk_type.strip().lower().replace(" ", "_")
    if "cold_whatsapp" in key or "cold_whats" in key:
        return ("no_cold_whatsapp_rule", "proposal_exclusion", "trust_page_section")
    if "pii" in key or "privacy" in key:
        return ("pii_handling_rule", "redaction_checklist", "audit_event_template")
    if "scrape" in key:
        return ("no_scraping_rule", "source_passport_enforcement", "sales_objection_response")
    return ("governance_rule_draft", "risk_register_entry", "approval_matrix_update")
