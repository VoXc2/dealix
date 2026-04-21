"""
Unifonic WhatsApp Integration — BSP (Business Service Provider) for KSA.
تكامل WhatsApp عبر يونيفونيك — مزود خدمة معتمد للسوق السعودي.

Unifonic is a Saudi-licensed WhatsApp BSP — the recommended Twilio alternative
for KSA sovereignty and local data residency compliance.

Docs: https://developer.unifonic.com/reference/whatsapp-messaging

Authentication: App SID via POST body parameter
Base URL: https://el.cloud.unifonic.com  (Authenticate API)

Environment variables:
- UNIFONIC_APP_SID     — Unifonic Application SID
- UNIFONIC_SENDER_ID   — Approved WhatsApp Business Phone Number / Sender ID
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# TODO: Confirm exact base URL from https://developer.unifonic.com/reference/overview
UNIFONIC_API_BASE = "https://el.cloud.unifonic.com"
UNIFONIC_WA_ENDPOINT = f"{UNIFONIC_API_BASE}/rest/WhatsApp/Messages"
UNIFONIC_WA_TEMPLATE_ENDPOINT = f"{UNIFONIC_API_BASE}/rest/WhatsApp/Messages/Template"


class UnifonicWhatsApp:
    """
    Unifonic WhatsApp messaging client.
    عميل رسائل WhatsApp عبر يونيفونيك.

    Usage:
        wa = UnifonicWhatsApp()
        await wa.send_text("+966501234567", "مرحباً! طلبك في الطريق 🚀")
        await wa.send_template("+966501234567", "order_confirmation", [("ORDER_ID", "12345")])
    """

    def __init__(
        self,
        app_sid: Optional[str] = None,
        sender_id: Optional[str] = None,
    ) -> None:
        self.app_sid = app_sid or os.getenv("UNIFONIC_APP_SID", "")
        self.sender_id = sender_id or os.getenv("UNIFONIC_SENDER_ID", "")

        if not self.app_sid:
            logger.warning("UNIFONIC_APP_SID not set — WhatsApp messages will fail")
        if not self.sender_id:
            logger.warning("UNIFONIC_SENDER_ID not set — WhatsApp messages will fail")

    def _base_params(self) -> dict[str, str]:
        """Base parameters for all Unifonic API calls."""
        return {
            "AppSid": self.app_sid,
            "SenderID": self.sender_id,
        }

    # ── Core send methods ─────────────────────────────────

    async def send_text(
        self,
        to: str,
        message: str,
        reference_id: Optional[str] = None,
    ) -> dict:
        """
        Send a plain text WhatsApp message.
        إرسال رسالة WhatsApp نصية عادية.

        Args:
            to: Recipient phone number in E.164 format (e.g. +966501234567)
            message: Text content (max ~4096 chars)
            reference_id: Optional unique reference for dedup/tracking

        Returns:
            Unifonic API response dict

        Docs: https://developer.unifonic.com/reference/whatsapp-send-message
        """
        phone = _normalize_phone(to)
        params = self._base_params()
        params.update({
            "Recipient": phone,
            "Body": message,
            "ContentType": "text",
        })
        if reference_id:
            params["MessageID"] = reference_id

        return await self._post(UNIFONIC_WA_ENDPOINT, params)

    async def send_template(
        self,
        to: str,
        template_name: str,
        variables: Optional[list[tuple[str, str]]] = None,
        language_code: str = "ar",
    ) -> dict:
        """
        Send a pre-approved WhatsApp template message.
        إرسال رسالة WhatsApp من قالب معتمد مسبقاً.

        Template messages are required for initiating conversations (24h window rule).
        رسائل القوالب مطلوبة لبدء المحادثات (قاعدة نافذة 24 ساعة).

        Args:
            to: Recipient E.164 phone number
            template_name: Approved template name (e.g. "order_confirmation")
            variables: List of (variable_name, value) tuples to substitute
            language_code: Template language — "ar" for Arabic, "en" for English

        Returns:
            Unifonic API response dict

        TODO: Verify template parameter format from
              https://developer.unifonic.com/reference/whatsapp-templates
        """
        phone = _normalize_phone(to)
        params = self._base_params()
        params.update({
            "Recipient": phone,
            "TemplateName": template_name,
            "LanguageCode": language_code,
        })

        # Build template variables as {{1}}, {{2}}, etc. or named params
        if variables:
            for i, (_, val) in enumerate(variables, start=1):
                params[f"Var{i}"] = val

        return await self._post(UNIFONIC_WA_TEMPLATE_ENDPOINT, params)

    async def send_media(
        self,
        to: str,
        media_url: str,
        caption: Optional[str] = None,
        media_type: str = "image",
    ) -> dict:
        """
        Send a media message (image, document, video).
        إرسال رسالة وسائط (صورة، مستند، فيديو).

        Args:
            to: Recipient E.164 phone number
            media_url: Publicly accessible URL of the media
            caption: Optional caption text
            media_type: "image" | "document" | "video" | "audio"

        TODO: Verify media endpoint and params from
              https://developer.unifonic.com/reference/whatsapp-media
        """
        phone = _normalize_phone(to)
        params = self._base_params()
        params.update({
            "Recipient": phone,
            "ContentType": media_type,
            "MediaURL": media_url,
        })
        if caption:
            params["Caption"] = caption

        return await self._post(UNIFONIC_WA_ENDPOINT, params)

    # ── Dealix-specific message helpers ──────────────────

    async def send_order_confirmation(
        self,
        phone: str,
        order_id: str,
        store_name: str,
        total_sar: float,
    ) -> dict:
        """
        Send order confirmation WhatsApp (Arabic).
        إرسال تأكيد الطلب عبر WhatsApp (عربي).

        Uses template "order_confirmation" — must be pre-approved in Unifonic.
        Uses approved WhatsApp template to comply with 24h initiation window.
        """
        message = (
            f"✅ تم استلام طلبك بنجاح!\n\n"
            f"رقم الطلب: {order_id}\n"
            f"المتجر: {store_name}\n"
            f"المجموع: {total_sar:,.0f} ريال\n\n"
            f"سيتم التواصل معك قريباً بخصوص الشحن. شكراً لثقتك!"
        )
        return await self.send_text(phone, message)

    async def send_cart_recovery(
        self,
        phone: str,
        cart_id: str,
        store_name: str,
        total_sar: float,
        recovery_url: Optional[str] = None,
    ) -> dict:
        """
        Send abandoned cart recovery WhatsApp (Arabic).
        إرسال رسالة استرداد السلة المهجورة عبر WhatsApp (عربي).
        """
        link_line = f"أكمل طلبك: {recovery_url}" if recovery_url else ""
        message = (
            f"👋 مرحباً! لاحظنا أنك تركت سلة مليانة في {store_name}.\n\n"
            f"💰 المجموع: {total_sar:,.0f} ريال\n"
            f"🔖 رقم السلة: {cart_id}\n\n"
            f"{link_line}\n\n"
            f"هل تحتاج مساعدة في إتمام الطلب؟ 😊"
        )
        return await self.send_text(phone, message)

    async def send_subscription_receipt(
        self,
        phone: str,
        plan: str,
        amount_sar: float,
        next_billing_date: str,
    ) -> dict:
        """
        Send subscription payment receipt.
        إرسال إيصال دفع الاشتراك.
        """
        plan_display = {"starter": "Starter", "pro": "Pro"}.get(plan, plan)
        message = (
            f"🧾 إيصال اشتراك Dealix\n\n"
            f"الخطة: {plan_display}\n"
            f"المبلغ: {amount_sar:,.0f} ريال/شهر\n"
            f"الدفعة القادمة: {next_billing_date}\n\n"
            f"شكراً لاشتراكك في Dealix! 🚀"
        )
        return await self.send_text(phone, message)

    # ── Internal HTTP ─────────────────────────────────────

    async def _post(self, url: str, params: dict) -> dict:
        """
        Execute authenticated POST to Unifonic API.
        تنفيذ طلب POST مصادق عليه لـ Unifonic API.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    url,
                    data=params,  # Unifonic uses form-encoded POST
                    headers={"Accept": "application/json"},
                )
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Unifonic WhatsApp HTTP error {exc.response.status_code}: {exc.response.text}")
            raise
        except Exception as exc:
            logger.error(f"Unifonic WhatsApp error: {exc}")
            raise


# ── Utilities ─────────────────────────────────────────────────────────────────

def _normalize_phone(phone: str) -> str:
    """
    Normalize phone to E.164 format for Saudi numbers.
    تحويل رقم الهاتف إلى صيغة E.164 للأرقام السعودية.

    Examples:
        "0501234567"  → "+966501234567"
        "966501234567" → "+966501234567"
        "+966501234567" → "+966501234567"
    """
    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    elif phone.startswith("0") and not phone.startswith("00"):
        # Saudi local number starting with 0 → +966
        phone = "+966" + phone[1:]
    elif phone.startswith("966") and not phone.startswith("+"):
        phone = "+" + phone
    return phone
