"""
Customers domain — success, CRM, portal, inbox, support.
مجال العملاء — النجاح، إدارة علاقات العملاء، البوابة، البريد الوارد، الدعم.
"""

from __future__ import annotations

from copy import copy

from fastapi import APIRouter

from api.routers import (
    billing,
    crm_v10,
    customer_company_portal,
    customer_data_plane,
    customer_inbox_v10,
    customer_loop,
    customer_ops,
    customer_success,
    customer_success_os,
    executive_pack_per_customer,
    onboarding,
    support_os,
)
from api.routers import (
    company_brain_mvp as company_brain_mvp_router,
)
from api.routers import (
    customer_brain as customer_brain_router,
)
from api.routers import (
    service_sessions as service_sessions_router,
)
from api.routers import (
    support_journey as support_journey_router,
)
from api.routers.customer import dashboard as customer_dashboard_router


def _filtered_router(source: APIRouter, blocked_paths: set[str]) -> APIRouter:
    """Return a router copy with launch-retired paths excluded.

    Never mutate module-level ``APIRouter.routes`` during import: those routers are
    reused by the FastAPI app factory and by compatibility imports/tests.
    """

    filtered = copy(source)
    filtered.routes = [
        route
        for route in source.routes
        if getattr(route, "path", None) not in blocked_paths
    ]
    return filtered


_LEGACY_BILLING_MUTATION_PATHS = {
    "/api/v1/billing/plans",
    "/api/v1/billing/subscribe",
    "/api/v1/billing/upgrade",
    "/api/v1/billing/cancel",
    "/api/v1/billing/invoices/{invoice_id}/pay",
}

# Keep read-only existing-tenant subscription/invoice/features views while
# excluding the retired SaaS plan catalogue and subscription/payment mutations.
_billing_router = _filtered_router(billing.router, _LEGACY_BILLING_MUTATION_PATHS)

_LEGACY_SELF_SERVE_ONBOARDING_PATHS = {
    "/api/v1/onboarding/plans",
    "/api/v1/onboarding/signup",
}

# api.main later includes onboarding.router explicitly. Rebind the exported
# reference to a filtered copy rather than deleting routes from the shared
# APIRouter object. Existing-tenant wizard/invite flows remain mounted.
onboarding.router = _filtered_router(onboarding.router, _LEGACY_SELF_SERVE_ONBOARDING_PATHS)


_ROUTERS = [
    _billing_router,
    company_brain_mvp_router.router,
    customer_success.router,
    customer_success_os.router,
    customer_loop.router,
    customer_data_plane.router,
    customer_brain_router.router,
    customer_company_portal.router,
    customer_ops.router,
    customer_dashboard_router.router,
    customer_inbox_v10.router,
    crm_v10.router,
    executive_pack_per_customer.router,
    service_sessions_router.router,
    support_journey_router.router,
    support_os.router,
]


def get_routers() -> list[APIRouter]:
    """Return all customers-domain routers."""
    return _ROUTERS
