"""
Unifonic Integration — WhatsApp & SMS via Unifonic Authenticate API.
تكامل يونيفونيك — WhatsApp والرسائل النصية عبر Unifonic.

Unifonic is a Saudi-licensed BSP (Business Service Provider) for WhatsApp
and SMS messaging — the preferred Twilio alternative for KSA compliance.

Docs: https://developer.unifonic.com/

Environment variables:
- UNIFONIC_APP_SID      — Unifonic Application SID
- UNIFONIC_SENDER_ID    — Approved WhatsApp sender / SMS Sender ID
"""
from .whatsapp import UnifonicWhatsApp
from .sms import UnifonicSMS

__all__ = ["UnifonicWhatsApp", "UnifonicSMS"]
