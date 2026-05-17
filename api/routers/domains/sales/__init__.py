"""
Sales domain — leads, revenue, outreach, pricing, payments.
مجال المبيعات — العملاء المحتملون، الإيرادات، التوعية، التسعير، المدفوعات.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    case_study_engine,
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
    revenue_machine,
    revenue_os,
    revenue_pipeline,
    revenue_profitability as revenue_profitability_router,
    revops,
    sales,
    sales_os,
)

_ROUTERS = [
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
    revenue_machine.router,
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
