"""
Dealix — Unified Entry Point
=============================
Mounts both:
  - Dashboard API (dashboard_api.py) with all production endpoints
  - WhatsApp Webhook (whatsapp_webhook_v2.py) with /webhook/whatsapp

Run:
    uvicorn main:app --host 0.0.0.0 --port 8002 --reload

Environment variables:
    DEALIX_DB           Path to SQLite DB (default: ../dealix_leads.db)
    JWT_SECRET          JWT signing secret
    GROQ_API_KEY        Groq API key
    TWILIO_ACCOUNT_SID  Twilio SID
    TWILIO_AUTH_TOKEN   Twilio auth token
    TWILIO_WHATSAPP_FROM Twilio WhatsApp sender (default: whatsapp:+14155238886)
    CORS_ORIGINS        Comma-separated list of allowed origins
"""

from __future__ import annotations

from dashboard_api import app
from whatsapp_webhook_v2 import router as webhook_router

# Mount the WhatsApp webhook routes into the main dashboard app
app.include_router(webhook_router)
