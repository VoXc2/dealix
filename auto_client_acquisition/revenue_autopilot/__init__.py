"""Revenue Autopilot — governed funnel from lead to paid diagnostic.

A thin wiring layer over existing Dealix modules (approval_center,
proof_os, sales_os, diagnostic_engine). It adds the founder doctrine's
named funnel, point-based lead score, and 10 automation hooks.

Doctrine: docs/REVENUE_AUTOPILOT.md
"""
from auto_client_acquisition.revenue_autopilot.funnel import (
    FunnelStage,
    advance_stage,
    is_revenue_countable,
)
from auto_client_acquisition.revenue_autopilot.lead_scorer import (
    LeadScore,
    LeadSignals,
    score_lead,
)
from auto_client_acquisition.revenue_autopilot.orchestrator import (
    advance_funnel,
    capture_lead,
    get_engagement,
    list_engagements,
    run_automation,
)

__all__ = [
    "FunnelStage",
    "LeadScore",
    "LeadSignals",
    "advance_funnel",
    "advance_stage",
    "capture_lead",
    "get_engagement",
    "is_revenue_countable",
    "list_engagements",
    "run_automation",
    "score_lead",
]
