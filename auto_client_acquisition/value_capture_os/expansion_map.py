"""Commercial expansion chains — next monetization step per track."""

from __future__ import annotations

TRACK_REVENUE_INTELLIGENCE = "revenue_intelligence"
TRACK_COMPANY_BRAIN = "company_brain"
TRACK_GOVERNANCE = "governance"
TRACK_AI_QUICK_WIN = "ai_quick_win"

_EXPANSION_CHAINS: dict[str, tuple[str, ...]] = {
    TRACK_REVENUE_INTELLIGENCE: (
        "capability_diagnostic",
        "revenue_intelligence_sprint",
        "monthly_revops_os",
        "executive_reporting",
        "sales_company_brain",
        "client_workspace",
        "dealix_revenue_os",
    ),
    TRACK_COMPANY_BRAIN: (
        "capability_diagnostic",
        "company_brain_sprint",
        "monthly_company_brain",
        "support_assistant",
        "governance_review",
        "enterprise_knowledge_os",
    ),
    TRACK_GOVERNANCE: (
        "ai_governance_review",
        "monthly_governance",
        "governance_runtime",
        "ai_control_plane",
        "enterprise_ai_os",
    ),
    TRACK_AI_QUICK_WIN: (
        "ai_quick_win_sprint",
        "monthly_ai_ops",
        "workflow_dashboard",
        "reporting_automation",
        "governance_runtime",
    ),
}


def recommended_expansion_offer(*, track: str, current_stage: str) -> str | None:
    """Return the next stage slug in the commercial map, or None if terminal / unknown."""
    chain = _EXPANSION_CHAINS.get(track)
    if not chain:
        return None
    try:
        idx = chain.index(current_stage)
    except ValueError:
        return None
    if idx + 1 >= len(chain):
        return None
    return chain[idx + 1]
