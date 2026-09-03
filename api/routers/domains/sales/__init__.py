"""
Sales domain — leads, revenue, outreach, pricing, payments.
مجال المبيعات — العملاء المحتملون، الإيرادات، التوعية، التسعير، المدفوعات.
"""

from __future__ import annotations

from copy import copy

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


def _filtered_router(source: APIRouter, blocked_paths: set[str]) -> APIRouter:
    """Return a launch-safe router view without mutating the shared source router.

    FastAPI routers are module-level singletons across app-factory calls. Mutating
    ``source.routes`` during import makes route registration depend on import order
    and can remove unrelated compatibility routes from later ``create_app()`` runs.
    A shallow router copy preserves router metadata while giving this launch view
    its own route list.
    """

    filtered = copy(source)
    filtered.routes = [
        route
        for route in source.routes
        if getattr(route, "path", None) not in blocked_paths
    ]
    return filtered


_LEGACY_DOMINANCE_PATHS = {
    "/api/v1/customers/{customer_id}/proof-pack",
}

# Keep useful dominance intelligence routes while excluding the retired proof
# generator from the launch router view. The shared source router is untouched.
_dominance_router = _filtered_router(dominance.router, _LEGACY_DOMINANCE_PATHS)

_LEGACY_COMMERCIAL_RUNTIME_PATHS = {
    "/api/v1/public/services",
    "/api/v1/ops-autopilot/leads/{lead_id}/meeting-brief",
    "/api/v1/invoices/draft",
}

# api.main later mounts AUTOPILOT_ROUTERS directly, so publish an explicit
# launch-safe list instead of deleting routes from the shared module-level
# APIRouter instances. The canonical replacement router below owns these URLs.
revenue_ops_autopilot.AUTOPILOT_ROUTERS = [
    _filtered_router(router, _LEGACY_COMMERCIAL_RUNTIME_PATHS)
    for router in revenue_ops_autopilot.AUTOPILOT_ROUTERS
]

_LEGACY_PRICING_RUNTIME_PATHS = {
    "/api/v1/pricing/plans",
    "/api/v1/pricing/usage",
    "/api/v1/pricing/menu",
    "/api/v1/checkout",
    "/api/v1/pricing/outcome-simulate",
}

# Current commercial authority is quote-only after qualified discovery and
# live charge is false. Use a launch-safe router view so safe reconciliation
# endpoints (including the Moyasar webhook) remain available without mutating
# the original pricing router.
_pricing_router = _filtered_router(pricing.router, _LEGACY_PRICING_RUNTIME_PATHS)

_LEGACY_COMMERCIAL_MAP_PATHS = {
    "/api/v1/commercial-map",
    "/api/v1/commercial-map/markdown",
}

# api.main later imports commercial_map.router explicitly. Rebind only the
# exported router reference to a launch-safe copy; the original router object is
# not modified. The canonical commercial_runtime_truth router owns these URLs.
commercial_map.router = _filtered_router(commercial_map.router, _LEGACY_COMMERCIAL_MAP_PATHS)


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
    _pricing_router,
    payment_ops_router.router,
    leadops_spine.router,
    leadops_reliability.router,
    _dominance_router,
    email_send.router,
    case_study_engine.router,
]


def get_routers() -> list[APIRouter]:
    """Return all sales-domain routers."""
    return _ROUTERS
