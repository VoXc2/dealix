"""No-commodity escape framings."""

from __future__ import annotations

COMMODITY_ESCAPE_FRAME: dict[str, str] = {
    "chatbot": "company_brain_governed",
    "automation": "governed_workflow_with_approval_audit_sop_proof",
    "lead_list": "revenue_intelligence_data_quality_scoring_draft_only_proof_pack",
    "dashboard": "executive_operating_report_sources_governance_recommendations",
}


def escape_commodity_framing(commodity_label: str) -> str:
    """Return Dealix non-commodity framing key for a commodity label."""
    key = commodity_label.strip().lower()
    return COMMODITY_ESCAPE_FRAME.get(key, "governed_ai_operating_capability")
