"""AI use case risk classification — Dealix Responsible AI."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    FORBIDDEN = "forbidden"


@dataclass(frozen=True, slots=True)
class UseCaseCard:
    use_case_id: str
    name: str
    department: str
    data_sources: tuple[str, ...]
    contains_pii: bool
    risk_level: RiskLevel
    human_oversight: str
    external_action_allowed: bool
    governance_decision: str
    proof_metric: str


def forbidden_use_case_reasons(
    *,
    requests_scraping_system: bool,
    requests_cold_whatsapp_automation: bool,
    requests_linkedin_automation: bool,
    requests_guaranteed_sales_claims: bool,
    sourceless_decisioning: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if requests_scraping_system:
        reasons.append("forbidden_scraping_system")
    if requests_cold_whatsapp_automation:
        reasons.append("forbidden_cold_whatsapp_automation")
    if requests_linkedin_automation:
        reasons.append("forbidden_linkedin_automation")
    if requests_guaranteed_sales_claims:
        reasons.append("forbidden_guaranteed_sales_claims")
    if sourceless_decisioning:
        reasons.append("forbidden_sourceless_decisioning")
    return tuple(reasons)


def classify_operational_risk(
    *,
    external_outreach: bool,
    financial_or_compliance_decision: bool,
    sensitive_personal_data: bool,
    automated_workflow_high_impact: bool,
    customer_facing_draft: bool,
    pii_in_analysis: bool,
    internal_summarization_non_sensitive: bool,
) -> RiskLevel:
    """Heuristic risk tier for supported use cases (non-forbidden)."""
    if internal_summarization_non_sensitive and not (
        external_outreach
        or financial_or_compliance_decision
        or sensitive_personal_data
        or automated_workflow_high_impact
        or customer_facing_draft
        or pii_in_analysis
    ):
        return RiskLevel.LOW
    if external_outreach or financial_or_compliance_decision or (
        sensitive_personal_data and automated_workflow_high_impact
    ):
        return RiskLevel.HIGH
    if customer_facing_draft or pii_in_analysis or automated_workflow_high_impact:
        return RiskLevel.MEDIUM
    return RiskLevel.MEDIUM


def high_risk_requires_governance_review(level: RiskLevel) -> bool:
    return level == RiskLevel.HIGH


def use_case_card_consistent(card: UseCaseCard) -> tuple[bool, tuple[str, ...]]:
    """Light consistency: declared risk vs flags + sources present."""
    errors: list[str] = []
    if not card.data_sources:
        errors.append("data_sources_required")
    if not card.proof_metric.strip():
        errors.append("proof_metric_required")
    if card.external_action_allowed and card.risk_level == RiskLevel.LOW:
        errors.append("external_action_not_low_risk")
    if card.contains_pii and card.risk_level == RiskLevel.LOW:
        errors.append("pii_use_case_not_low_risk")
    return not errors, tuple(errors)
