"""
Sales domain — leads, revenue, outreach, pricing, payments.
مجال المبيعات — العملاء المحتملون، الإيرادات، التوعية، التسعير، المدفوعات.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    board_metrics as board_metrics_router,
    case_study_engine,
    deal_desk as deal_desk_router,
    grounding_score as grounding_score_router,
    unit_economics as unit_economics_router,
    commercial_engagements as commercial_engagements_router,
    commercial_readiness as commercial_readiness_router,
    decision_passport as decision_passport_router,
    proof_pack_governed as proof_pack_governed_router,
    revenue_data_intake as revenue_data_intake_router,
    revenue_intelligence as revenue_intelligence_router,
    revenue_os_catalog as revenue_os_catalog_router,
    dominance,
    email_send,
    leadops_reliability,
    leadops_spine,
    leads,
    outreach,
    payment_ops as payment_ops_router,
    pricing,
    prospect,
    revenue,
    revenue_os,
    revenue_pipeline,
    revenue_profitability as revenue_profitability_router,
    revops,
    sales,
    sales_os,
    trust_dashboard as trust_dashboard_router,
    unified_readiness as unified_readiness_router,
)

_ROUTERS = [
    unified_readiness_router.router,
    unit_economics_router.router,
    grounding_score_router.router,
    board_metrics_router.router,
    deal_desk_router.router,
    trust_dashboard_router.router,
    decision_passport_router.router,
    revenue_os_catalog_router.router,
    commercial_readiness_router.router,
    commercial_engagements_router.router,
    revenue_data_intake_router.router,
    revenue_intelligence_router.router,
    proof_pack_governed_router.router,
    leads.router,
    sales.router,
    sales_os.router,
    revenue.router,
    revenue_os.router,
    revenue_pipeline.router,
    revops.router,
    revenue_profitability_router.router,
    outreach.router,
    prospect.router,
    pricing.router,
    payment_ops_router.router,
    leadops_spine.router,
    leadops_reliability.router,
    dominance.router,
    email_send.router,
    case_study_engine.router,
]


def get_routers() -> list[APIRouter]:
    """Return all sales-domain routers."""
    return _ROUTERS
