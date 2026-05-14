"""
Customers domain — success, CRM, portal, inbox, support.
مجال العملاء — النجاح، إدارة علاقات العملاء، البوابة، البريد الوارد، الدعم.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    company_brain_mvp as company_brain_mvp_router,
    crm_v10,
    customer_brain as customer_brain_router,
    customer_company_portal,
    customer_data_plane,
    customer_inbox_v10,
    customer_loop,
    customer_success,
    customer_success_os,
    executive_pack_per_customer,
    service_sessions as service_sessions_router,
    support_journey as support_journey_router,
    support_os,
)

_ROUTERS = [
    company_brain_mvp_router.router,
    customer_success.router,
    customer_success_os.router,
    customer_loop.router,
    customer_data_plane.router,
    customer_brain_router.router,
    customer_company_portal.router,
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
