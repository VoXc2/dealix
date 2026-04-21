"""
Unifonic SMS Integration — Saudi-licensed SMS via Unifonic.
تكامل الرسائل النصية عبر يونيفونيك — مرخص في المملكة العربية السعودية.

Docs: https://developer.unifonic.com/reference/send-sms

Authentication: App SID via POST body
Base URL: https://el.cloud.unifonic.com

Environment variables:
- UNIFONIC_APP_SID    — Unifonic Application SID
- UNIFONIC_SENDER_ID  — Approved SMS Sender ID (e.g. "Dealix" or numeric)
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# TODO: Confirm exact SMS endpoint from https://developer.unifonic.com/reference/send-sms
UNIFONIC_API_BASE = "https://el.cloud.unifonic.com"
UNIFONIC_SMS_ENDPOINT = f"{UNIFONIC_API_BASE}/rest/SMS/messages"
UNIFONIC_SMS_BULK_ENDPOINT = f"{UNIFONIC_API_BASE}/rest/SMS/messages/bulk"


class UnifonicSMS:
    """
    Unifonic SMS client for transactional and marketing SMS.
    عميل SMS يونيفونيك للرسائل التشغيلية والتسويقية.

    Usage:
        sms = UnifonicSMS()
        await sms.send("+966501234567", "رمز التحقق الخاص بك: 4829")
        await sms.send_otp("+966501234567", "4829")
    """

    def __init__(
        self,
        app_sid: Optional[str] = None,
        sender_id: Optional[str] = None,
    ) -> None:
        self.app_sid = app_sid or os.getenv("UNIFONIC_APP_SID", "")
        self.sender_id = sender_id or os.getenv("UNIFONIC_SENDER_ID", "Dealix")

        if not self.app_sid:
            logger.warning("UNIFONIC_APP_SID not set — SMS messages will fail")

    def _base_params(self) -> dict[str, str]:
        return {
            "AppSid": self.app_sid,
            "SenderID": self.sender_id,
        }

    # ── Core send ─────────────────────────────────────────

    async def send(
        self,
        to: str,
        message: str,
        reference_id: Optional[str] = None,
        priority: str = "Normal",
    ) -> dict:
        """
        Send a single SMS.
        إرسال رسالة SMS واحدة.

        Args:
            to: Recipient phone in E.164 format (+966XXXXXXXXX)
            message: Text content (max 160 chars for single SMS, 153 per segment for multi)
            reference_id: Optional unique message ID for tracking
            priority: "Normal" | "High" — High priority for OTPs

        Returns:
            Unifonic API response dict

        Docs: https://developer.unifonic.com/reference/send-sms
        """
        phone = _normalize_phone(to)
        params = self._base_params()
        params.update({
            "Recipient": phone,
            "Body": message,
            "Priority": priority,
        })
        if reference_id:
            params["MessageID"] = reference_id

        return await self._post(UNIFONIC_SMS_ENDPOINT, params)

    async def send_bulk(
        self,
        recipients: list[str],
        message: str,
    ) -> dict:
        """
        Send the same SMS to multiple recipients.
        إرسال رسالة SMS لعدة مستلمين.

        Args:
            recipients: List of E.164 phone numbers
            message: Text content

        Returns:
            Unifonic bulk send response dict

        TODO: Confirm bulk endpoint and param format from
              https://developer.unifonic.com/reference/bulk-sms
        """
        phones = ",".join(_normalize_phone(p) for p in recipients)
        params = self._base_params()
        params.update({
            "Recipient": phones,
            "Body": message,
        })
        return await self._post(UNIFONIC_SMS_BULK_ENDPOINT, params)

    # ── Dealix-specific helpers ───────────────────────────

    async def send_otp(
        self,
        phone: str,
        code: str,
        expiry_minutes: int = 5,
    ) -> dict:
        """
        Send OTP verification code via SMS.
        إرسال رمز التحقق OTP عبر SMS.

        Args:
            phone: Recipient phone (E.164 or Saudi local format)
            code: OTP code string (4-6 digits)
            expiry_minutes: Code validity window (for message text)
        """
        message = (
            f"رمز التحقق الخاص بك في Dealix: {code}\n"
            f"صالح لمدة {expiry_minutes} دقائق. لا تشاركه مع أحد.\n"
            f"Your Dealix OTP: {code} (valid {expiry_minutes}min)"
        )
        return await self.send(phone, message, priority="High")

    async def send_payment_reminder(
        self,
        phone: str,
        amount_sar: float,
        due_date: str,
        plan: str,
    ) -> dict:
        """
        Send subscription payment reminder via SMS.
        إرسال تذكير بدفع الاشتراك عبر SMS.
        """
        plan_display = {"starter": "Starter", "pro": "Pro"}.get(plan, plan)
        message = (
            f"تذكير: اشتراك Dealix {plan_display} - "
            f"{amount_sar:,.0f} ريال مستحق بتاريخ {due_date}. "
            f"للدفع: pay.dealix.sa"
        )
        return await self.send(phone, message)

    async def send_alert(
        self,
        phone: str,
        title: str,
        body: str,
    ) -> dict:
        """
        Send a general alert SMS.
        إرسال رسالة تنبيه عامة عبر SMS.
        """
        message = f"⚠️ {title}\n{body}"
        return await self.send(phone, message)

    # ── Message status ────────────────────────────────────

    async def get_message_status(self, message_id: str) -> dict:
        """
        Get delivery status of a sent message.
        الحصول على حالة تسليم رسالة مُرسلة.

        TODO: Confirm status endpoint from
              https://developer.unifonic.com/reference/get-message-status
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                f"{UNIFONIC_API_BASE}/rest/SMS/messages/{message_id}",
                params={"AppSid": self.app_sid},
            )
            resp.raise_for_status()
            return resp.json()

    # ── Internal HTTP ─────────────────────────────────────

    async def _post(self, url: str, params: dict) -> dict:
        """
        POST form-encoded data to Unifonic API.
        إرسال بيانات مشفرة form-encoded إلى Unifonic API.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    url,
                    data=params,
                    headers={"Accept": "application/json"},
                )
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Unifonic SMS HTTP error {exc.response.status_code}: {exc.response.text}")
            raise
        except Exception as exc:
            logger.error(f"Unifonic SMS error: {exc}")
            raise


# ── Utilities ─────────────────────────────────────────────────────────────────

def _normalize_phone(phone: str) -> str:
    """
    Normalize phone number to E.164 format.
    تحويل رقم الهاتف إلى صيغة E.164.

    Examples:
        "0501234567"   → "+966501234567"
        "966501234567" → "+966501234567"
        "+966501234567" → "+966501234567"
    """
    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    elif phone.startswith("0") and not phone.startswith("00"):
        phone = "+966" + phone[1:]
    elif phone.startswith("966") and not phone.startswith("+"):
        phone = "+" + phone
    return phone
