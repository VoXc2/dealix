"""Canonical value metric keys per commercial offer — for Proof Pack value sections."""

from __future__ import annotations

OFFER_REVENUE_INTELLIGENCE_SPRINT = "revenue_intelligence_sprint"
OFFER_COMPANY_BRAIN_SPRINT = "company_brain_sprint"
OFFER_AI_GOVERNANCE_REVIEW = "ai_governance_review"
OFFER_AI_QUICK_WIN_SPRINT = "ai_quick_win_sprint"
OFFER_EXECUTIVE_REPORTING_AUTOMATION = "executive_reporting_automation"

VALUE_METRICS_BY_OFFER: dict[str, tuple[str, ...]] = {
    OFFER_REVENUE_INTELLIGENCE_SPRINT: (
        "records_imported",
        "duplicates_removed",
        "data_quality_score",
        "accounts_scored",
        "top_opportunities_identified",
        "drafts_generated",
        "unsafe_outreach_blocked",
        "pipeline_value_estimated",
    ),
    OFFER_COMPANY_BRAIN_SPRINT: (
        "sources_registered",
        "documents_indexed",
        "questions_tested",
        "citation_coverage",
        "insufficient_evidence_rate",
        "knowledge_gaps_found",
        "answer_qa_score",
    ),
    OFFER_AI_GOVERNANCE_REVIEW: (
        "ai_use_cases_inventoried",
        "risk_rules_created",
        "approval_paths_defined",
        "unsafe_actions_blocked",
        "policy_gaps_found",
        "audit_coverage_designed",
    ),
    OFFER_AI_QUICK_WIN_SPRINT: (
        "manual_steps_mapped",
        "workflow_created",
        "approval_path_defined",
        "hours_saved_estimate",
        "qa_pass_rate",
        "handoff_completion",
    ),
    OFFER_EXECUTIVE_REPORTING_AUTOMATION: (
        "manual_reports_reduced",
        "data_sources_connected",
        "report_freshness",
        "decision_recommendations_generated",
        "qa_score",
        "time_to_report_reduction",
    ),
}


def value_metrics_for_offer(offer_id: str) -> tuple[str, ...]:
    """Return ordered metric keys for a known offer, or empty if unknown."""
    return VALUE_METRICS_BY_OFFER.get(offer_id, ())
