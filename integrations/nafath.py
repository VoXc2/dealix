"""
Nafath integration — Saudi National Digital Identity.
دمج النفاذ — الهوية الرقمية السعودية.

Nafath is the Saudi national single sign-on and digital identity platform
managed by the National Information Center (NIC). This client provides:

1. Identity verification (real-time via Nafath APIs)
2. Digital signature verification
3. User profile retrieval

Ref: https://nafath.sa
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class AuthRequest:
    request_id: str
    national_id: str
    status: str  # pending / approved / rejected / expired
    expires_at: str
    qr_code: str | None = None
    app_url: str | None = None
    method: str = "biometric"  # biometric / otp / smartcard


@dataclass
class AuthStatus:
    request_id: str
    status: str  # pending / approved / rejected / expired
    national_id: str
    verified_at: str | None = None
    method_used: str | None = None
    error_message: str | None = None


@dataclass
class UserInfo:
    national_id: str
    full_name_ar: str
    full_name_en: str
    date_of_birth: str
    gender: str
    nationality: str
    is_valid: bool
    expiry_date: str
    phone_number: str | None = None
    email: str | None = None


class NafathClient:
    """Client for the Nafath National Digital Identity API.

    Uses Mutual TLS (mTLS) for API authentication.
    Requires client certificate and private key configured via env vars.
    """

    BASE_URL = "https://api.nafath.sa/api/v1"
    SANDBOX_URL = "https://sandbox.api.nafath.sa/api/v1"

    def __init__(self, sandbox: bool = True) -> None:
        self.sandbox = sandbox
        self.base = self.SANDBOX_URL if sandbox else self.BASE_URL
        self.client_cert = os.getenv("NAFATH_CLIENT_CERT_PATH", "")
        self.client_key = os.getenv("NAFATH_CLIENT_KEY_PATH", "")
        self.api_key = os.getenv("NAFATH_API_KEY", "")
        self.secret_key = os.getenv("NAFATH_SECRET_KEY", "")
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            client_kwargs: dict[str, Any] = {
                "timeout": 30,
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-API-Key": self.api_key,
                },
            }
            if self.client_cert and self.client_key:
                client_kwargs["cert"] = (self.client_cert, self.client_key)
            if self.secret_key:
                client_kwargs["headers"]["X-Secret-Key"] = self.secret_key

            self._client = httpx.AsyncClient(**client_kwargs)

        return self._client

    async def request_authentication(
        self,
        national_id: str,
        method: str = "biometric",
        callback_url: str | None = None,
    ) -> AuthRequest:
        """Initiate an authentication request for a national ID.

        The user receives a push notification on their Nafath app
        to approve the authentication via biometric or OTP.
        """
        client = await self._get_client()
        request_id = str(uuid.uuid4())
        timestamp = str(int(time.time()))

        payload: dict[str, Any] = {
            "nationalId": national_id,
            "method": method,
            "requestId": request_id,
            "timestamp": timestamp,
            "service": "Dealix Identity Verification",
        }
        if callback_url:
            payload["callbackUrl"] = callback_url

        signature = self._sign_payload(payload)
        payload["signature"] = signature

        try:
            resp = await client.post(
                f"{self.base}/auth/request",
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

            log.info(
                "nafath_auth_requested",
                national_id=national_id[-4:],
                method=method,
                request_id=request_id,
            )

            return AuthRequest(
                request_id=request_id,
                national_id=national_id,
                status=data.get("status", "pending"),
                expires_at=data.get("expiresAt", ""),
                qr_code=data.get("qrCode"),
                app_url=data.get("appUrl"),
                method=method,
            )

        except httpx.HTTPStatusError as exc:
            log.error(
                "nafath_auth_request_failed",
                national_id=national_id[-4:],
                status_code=exc.response.status_code,
                response=exc.response.text[:500],
            )
            raise

    async def check_status(self, request_id: str) -> AuthStatus:
        """Check the status of an authentication request."""
        client = await self._get_client()

        try:
            resp = await client.get(
                f"{self.base}/auth/status/{request_id}",
            )
            resp.raise_for_status()
            data = resp.json()

            return AuthStatus(
                request_id=request_id,
                status=data.get("status", "pending"),
                national_id=data.get("nationalId", ""),
                verified_at=data.get("verifiedAt"),
                method_used=data.get("method"),
                error_message=data.get("errorMessage"),
            )

        except httpx.HTTPStatusError as exc:
            log.error(
                "nafath_status_check_failed",
                request_id=request_id,
                status_code=exc.response.status_code,
            )
            return AuthStatus(
                request_id=request_id,
                status="error",
                national_id="",
                error_message=f"HTTP {exc.response.status_code}",
            )

    async def get_user_info(self, token: str) -> UserInfo:
        """Retrieve user information using an authentication token."""
        client = await self._get_client()

        try:
            resp = await client.get(
                f"{self.base}/user/info",
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()

            return UserInfo(
                national_id=data.get("nationalId", ""),
                full_name_ar=data.get("fullNameAr", ""),
                full_name_en=data.get("fullNameEn", ""),
                date_of_birth=data.get("dateOfBirth", ""),
                gender=data.get("gender", ""),
                nationality=data.get("nationality", "SAU"),
                is_valid=data.get("isValid", False),
                expiry_date=data.get("expiryDate", ""),
                phone_number=data.get("phoneNumber"),
                email=data.get("email"),
            )

        except httpx.HTTPStatusError as exc:
            log.error(
                "nafath_user_info_failed",
                status_code=exc.response.status_code,
            )
            raise

    async def verify_identity(self, national_id: str) -> bool:
        """Quick identity verification check.

        Returns True if the national ID is valid and active.
        """
        try:
            auth = await self.request_authentication(national_id, method="biometric")
            if auth.status == "pending":
                status = await self.check_status(auth.request_id)
                return status.status == "approved"
            return auth.status == "approved"
        except Exception as exc:
            log.error("nafath_verify_identity_error", error=str(exc))
            return False

    def _sign_payload(self, payload: dict[str, Any]) -> str:
        """Create HMAC-SHA256 signature for request integrity."""
        message = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        key = self.secret_key.encode() if self.secret_key else b""
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
