"""
Zid Platform Integration — OAuth2 + Webhooks + Orders Sync.
تكامل منصة زد — OAuth2 + Webhooks + مزامنة الطلبات.

Docs: https://docs.zid.sa/
"""
from .oauth import ZidOAuth
from .client import ZidClient
from .webhooks import handle_zid_webhook

__all__ = ["ZidOAuth", "ZidClient", "handle_zid_webhook"]
