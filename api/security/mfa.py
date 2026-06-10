"""
Multi-Factor Authentication (MFA) manager.
مدير المصادقة متعددة العوامل.

Supports TOTP (authenticator apps) and SMS-based OTP.
Uses pyotp for TOTP and a pluggable SMS provider.
"""

from __future__ import annotations

import hashlib
import os
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class TOTPSetup:
    secret: str
    qr_code_data: str
    backup_codes: list[str]
    uri: str


@dataclass
class MFARecoveryCode:
    code_hash: str
    used: bool = False
    used_at: str | None = None


class MFAManager:
    """MFA manager handling TOTP and SMS verification.

    Integrates with pyotp for TOTP (RFC 6238) and
    external SMS gateways for SMS OTP delivery.
    """

    # In-memory store for OTP codes (in production, use Redis with TTL)
    _sms_codes: dict[str, dict[str, Any]] = {}
    _recovery_codes: dict[str, list[MFARecoveryCode]] = {}

    TOTP_ISSUER = "Dealix"
    SMS_CODE_TTL = timedelta(minutes=5)
    BACKUP_CODE_COUNT = 8

    async def setup_totp(self, user_id: str, email: str = "") -> TOTPSetup:
        """Generate TOTP secret and provisioning URI for authenticator app setup."""
        import pyotp

        secret = pyotp.random_base32()
        uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=email or user_id,
            issuer_name=self.TOTP_ISSUER,
        )

        backup_codes = [secrets.token_hex(4).upper() for _ in range(self.BACKUP_CODE_COUNT)]
        self._recovery_codes[user_id] = [
            MFARecoveryCode(code_hash=hashlib.sha256(c.encode()).hexdigest())
            for c in backup_codes
        ]

        log.info("mfa_totp_setup", user_id=user_id)

        return TOTPSetup(
            secret=secret,
            qr_code_data=uri,
            backup_codes=backup_codes,
            uri=uri,
        )

    async def verify_totp(self, user_id: str, code: str, secret: str) -> bool:
        """Verify a TOTP code against the user's stored secret."""
        import pyotp

        if not secret or not code:
            return False

        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(code, valid_window=1)

        if is_valid:
            log.info("mfa_totp_verified", user_id=user_id)
        else:
            log.warning("mfa_totp_failed", user_id=user_id)

        return is_valid

    async def send_sms_code(self, user_id: str, phone: str) -> bool:
        """Generate and send an SMS OTP code to the user's phone.

        Uses the configured SMS provider (Twilio, Unifonic, or custom).
        Falls back to logging the code in development.
        """
        code = f"{secrets.randbelow(1000000):06d}"
        expires_at = datetime.now(UTC) + self.SMS_CODE_TTL

        self._sms_codes[f"{user_id}:sms"] = {
            "code": code,
            "expires_at": expires_at.isoformat(),
            "attempts": 0,
            "phone": phone,
        }

        provider = os.getenv("SMS_PROVIDER", "log")
        sent = False

        if provider == "twilio":
            sent = await self._send_via_twilio(phone, code)
        elif provider == "unifonic":
            sent = await self._send_via_unifonic(phone, code)
        elif provider == "log":
            log.info("mfa_sms_code_dev", user_id=user_id, phone=phone, code=code)
            sent = True
        else:
            log.warning("mfa_sms_unknown_provider", provider=provider)
            sent = await self._send_via_unifonic(phone, code)

        if sent:
            log.info("mfa_sms_sent", user_id=user_id, phone=phone[-4:])

        return sent

    async def verify_sms(self, user_id: str, code: str) -> bool:
        """Verify an SMS OTP code."""
        key = f"{user_id}:sms"
        stored = self._sms_codes.get(key)
        if not stored:
            log.warning("mfa_sms_no_code", user_id=user_id)
            return False

        stored["attempts"] = stored.get("attempts", 0) + 1
        if stored["attempts"] > 5:
            self._sms_codes.pop(key, None)
            log.warning("mfa_sms_too_many_attempts", user_id=user_id)
            return False

        expires_at = datetime.fromisoformat(stored["expires_at"])
        if datetime.now(UTC) > expires_at:
            self._sms_codes.pop(key, None)
            log.warning("mfa_sms_expired", user_id=user_id)
            return False

        if stored["code"] != code:
            log.warning("mfa_sms_wrong_code", user_id=user_id)
            return False

        self._sms_codes.pop(key, None)
        log.info("mfa_sms_verified", user_id=user_id)
        return True

    async def verify_recovery_code(self, user_id: str, code: str) -> bool:
        """Verify a backup/recovery code."""
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        codes = self._recovery_codes.get(user_id, [])

        for rc in codes:
            if rc.code_hash == code_hash and not rc.used:
                rc.used = True
                rc.used_at = datetime.now(UTC).isoformat()
                log.info("mfa_recovery_code_used", user_id=user_id)
                return True

        log.warning("mfa_recovery_code_failed", user_id=user_id)
        return False

    def get_remaining_recovery_codes(self, user_id: str) -> int:
        """Get count of unused recovery codes."""
        codes = self._recovery_codes.get(user_id, [])
        return sum(1 for c in codes if not c.used)

    async def _send_via_twilio(self, phone: str, code: str) -> bool:
        """Send SMS via Twilio."""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        from_number = os.getenv("TWILIO_FROM_NUMBER", "")

        if not all([account_sid, auth_token, from_number]):
            log.warning("mfa_twilio_not_configured")
            return False

        basic = base64_encode(f"{account_sid}:{auth_token}")
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
                headers={
                    "Authorization": f"Basic {basic}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "To": phone,
                    "From": from_number,
                    "Body": f"Your Dealix verification code is: {code}. Valid for 5 minutes.",
                },
            )
            return resp.is_success

    async def _send_via_unifonic(self, phone: str, code: str) -> bool:
        """Send SMS via Unifonic (Saudi preferred provider)."""
        app_sid = os.getenv("UNIFONIC_APP_SID", "")
        sender_id = os.getenv("UNIFONIC_SENDER_ID", "Dealix")

        if not app_sid:
            log.warning("mfa_unifonic_not_configured")
            return False

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                "https://api.unifonic.com/rest/Messages/Send",
                json={
                    "AppSid": app_sid,
                    "SenderID": sender_id,
                    "Recipient": phone,
                    "Body": f"Your Dealix verification code: {code}. Valid for 5 minutes.",
                },
            )
            return resp.is_success

    def clear_user_data(self, user_id: str) -> None:
        """Clear all MFA data for a user (on disable)."""
        self._sms_codes.pop(f"{user_id}:sms", None)
        self._recovery_codes.pop(user_id, None)


def base64_encode(s: str) -> str:
    import base64
    return base64.b64encode(s.encode()).decode()
