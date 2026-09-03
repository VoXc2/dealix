"""
Sales domain — leads, revenue, outreach, pricing, payments.
مجال المبيعات — العملاء المحتملون، الإيرادات، التوعية، التسعير، المدفوعات.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    case_study_engine,
    commercial_intelligence,
    commercial_map,
    commercial_runtime_truth,
    company_targeting,
    dominance,
    email_send,
    leadops_reliability,
    leadops_spine,
    leads,
    outreach,
    pricing,
    prospect,
    revenue,
    revenue_ops_autopilot,
    revenue_os,
    revenue_pipeline,
    revops,
    sales,
    sales_os,
)
from api.routers import (
    commercial_engagements as commercial_engagements_router,
)
from api.routers import (
    commercial_readiness as commercial_readiness_router,
)
from api.routers import (
    decision_passport as decision_passport_router,
)
from api.routers import (
    payment_ops as payment_ops_router,
)
from api.routers import (
    proof_pack_governed as proof_pack_governed_router,
)
from api.routers import (
    revenue_data_intake as revenue_data_intake_router,
)
from api.routers import (
    revenue_intelligence as revenue_intelligence_router,
)
from api.routers import (
    revenue_os_catalog as revenue_os_catalog_router,
)
from api.routers import (
    revenue_profitability as revenue_profitability_router,
)

_LEGACY_DOMINANCE_PATHS = {
    "/api/v1/customers/{customer_id}/proof-pack",
}

# The legacy dominance proof-pack endpoint emits unsupported fixed prices,
# seven-day claims, fabricated outcome placeholders and referral economics.
# Keep the useful dominance intelligence routes, but do not expose that endpoint.
dominance.router.routes[:] = [
    route
    for route in dominance.router.routes
    if getattr(route, "path", None) not in _LEGACY_DOMINANCE_PATHS
]

_LEGACY_COMMERCIAL_RUNTIME_PATHS = {
    "/api/v1/public/services",
    "/api/v1/ops-autopilot/leads/{lead_id}/meeting-brief",
    "/api/v1/invoices/draft",
}

# Quarantine the three retired commercial-authority routes before api.main later
# includes AUTOPILOT_ROUTERS. Their source is retained for rollback/history, but
# they are not mounted and therefore cannot act as launch pricing authority.
for _autopilot_router in revenue_ops_autopilot.AUTOPILOT_ROUTERS:
    _autopilot_router.routes[:] = [
        route
        for route in _autopilot_router.routes
        if getattr(route, "path", None) not in _LEGACY_COMMERCIAL_RUNTIME_PATHS
    ]

_LEGACY_PRICING_RUNTIME_PATHS = {
    "/api/v1/pricing/plans",
    "/api/v1/pricing/usage",
    "/api/v1/pricing/menu",
    "/api/v1/checkout",
    "/api/v1/pricing/outcome-simulate",
}

# Current commercial authority is quote-only after qualified discovery and
# live charge is false. Keep the Moyasar webhook mounted for reconciliation of
# already-existing provider events, but remove every route that can publish a
# price, create usage-based billable state, simulate a legacy price ladder, or
# mint a new checkout invoice/payment link.
pricing.router.routes[:] = [
    route
    for route in pricing.router.routes
    if getattr(route, "path", None) not in _LEGACY_PRICING_RUNTIME_PATHS
]

_LEGACY_COMMERCIAL_MAP_PATHS = {
    "/api/v1/commercial-map",
    "/api/v1/commercial-map/markdown",
}

# The legacy public commercial map is still useful as internal source/history,
# but it contains retired SKU names, checkout links and price ladders. Remove
# its HTTP exposure while retaining module helpers for non-authoritative reads.
commercial_map.router.routes[:] = [
    route
    for route in commercial_map.router.routes
    if getattr(route, "path", None) not in _LEGACY_COMMERCIAL_MAP_PATHS
]


_ROUTERS = [
    commercial_runtime_truth.router,
    company_targeting.router,
    commercial_intelligence.router,
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
