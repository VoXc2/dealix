"""
Webhooks Entry Point — Dealix inbound integrations.
Exports sub-routers for payment confirmations, WhatsApp, and future channels.
"""

from fastapi import APIRouter
from app.api.v1.webhooks import payments
from app.api.v1.webhooks import whatsapp

router = APIRouter()

# Payment webhooks (Moyasar etc.)
router.include_router(payments.router, prefix="/payments", tags=["Payment Webhooks"])

# WhatsApp inbound webhook (Twilio)
router.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp Webhook"])
