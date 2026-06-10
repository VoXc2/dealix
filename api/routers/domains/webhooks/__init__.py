"""
Webhooks domain — inbound/outbound webhook handlers.
مجال الـ Webhooks — معالجات الـ webhook الواردة والصادرة.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    channel_policy_gateway as channel_policy_gateway_router,
)
from api.routers import (
    support_webhook,
    webhooks,
)
from api.routers import (
    whatsapp_decision_bot as whatsapp_decision_bot_router,
)

_ROUTERS = [
    webhooks.router,
    support_webhook.router,
    whatsapp_decision_bot_router.router,
    channel_policy_gateway_router.router,
]


def get_routers() -> list[APIRouter]:
    """Return all webhooks-domain routers."""
    return _ROUTERS
