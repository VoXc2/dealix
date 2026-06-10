"""Customer expansion paths from primary wedge offers."""

from __future__ import annotations

from enum import StrEnum


class ExpansionEntry(StrEnum):
    REVENUE_INTELLIGENCE = "revenue_intelligence"
    COMPANY_BRAIN = "company_brain"
    AI_QUICK_WIN = "ai_quick_win"


_EXPANSION_MAP: dict[ExpansionEntry, tuple[str, ...]] = {
    ExpansionEntry.REVENUE_INTELLIGENCE: (
        "revenue_intelligence_sprint",
        "monthly_revops_os",
        "executive_reporting",
        "sales_company_brain",
        "ai_governance_review",
        "client_workspace",
    ),
    ExpansionEntry.COMPANY_BRAIN: (
        "company_brain_sprint",
        "monthly_company_brain",
        "support_suggested_replies",
        "policy_assistant",
        "ai_governance_program",
    ),
    ExpansionEntry.AI_QUICK_WIN: (
        "ai_quick_win_sprint",
        "monthly_ai_ops",
        "workflow_dashboard",
        "reporting_automation",
        "governance_runtime",
    ),
}


def expansion_path(entry: ExpansionEntry) -> tuple[str, ...]:
    return _EXPANSION_MAP[entry]
