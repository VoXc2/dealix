"""
Customers domain — success, CRM, portal, inbox, support.
مجال العملاء — النجاح، إدارة علاقات العملاء، البوابة، البريد الوارد، الدعم.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    billing,
    crm_v10,
    customer_company_portal,
    customer_data_plane,
    customer_inbox_v10,
    customer_loop,
    customer_success,
    customer_success_os,
    executive_pack_per_customer,
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

_LEGACY_BILLING_MUTATION_PATHS = {
    "/api/v1/billing/plans",
    "/api/v1/billing/subscribe",
    "/api/v1/billing/upgrade",
    "/api/v1/billing/cancel",
    "/api/v1/billing/invoices/{invoice_id}/pay",
}

# Launch authority is quote-only and live charge is disabled. Keep read-only
# subscription/invoice/features views for existing tenants, but do not expose
# the legacy SaaS plan catalogue or any endpoint that mutates a subscription or
# creates a Moyasar payment link. Source code remains available for rollback and
# historical reference; mounting is the authority boundary.
billing.router.routes[:] = [
    route
    for route in billing.router.routes
    if getattr(route, "path", None) not in _LEGACY_BILLING_MUTATION_PATHS
]


_ROUTERS = [
    billing.router,
    company_brain_mvp_router.router,
    customer_success.router,
    customer_success_os.router,
    customer_loop.router,
    customer_data_plane.router,
    customer_brain_router.router,
    customer_company_portal.router,
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
