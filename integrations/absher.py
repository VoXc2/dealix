"""
Absher integration — Saudi Government E-Services Portal.
دمج أبشر — بوابة الخدمات الإلكترونية الحكومية السعودية.

Absher provides identity verification, user profile data, and
government service access. This client implements:

1. Identity verification (national ID + birth date match)
2. User profile retrieval (name, address, contact info)
3. Document verification

Ref: https://www.absher.sa
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class VerificationResult:
    verified: bool
    national_id: str
    full_name_ar: str | None = None
    full_name_en: str | None = None
    match_score: float = 0.0
    error_message: str | None = None
    request_id: str | None = None


@dataclass
class UserProfile:
    absher_id: str
    national_id: str
    full_name_ar: str
    full_name_en: str
    date_of_birth: str
    gender: str
    nationality: str
    phone_number: str | None = None
    email: str | None = None
    address: str | None = None
    city: str | None = None
    country: str = "Saudi Arabia"
    is_active: bool = True


class AbsherClient:
    """Client for the Absher Government Services API.

    Requires API credentials from the Absher Business portal.
    Uses HMAC-SHA256 request signing for API authentication.
    """

    BASE_URL = "https://api.absher.sa/api/v1"
    SANDBOX_URL = "https://sandbox.api.absher.sa/api/v1"

    def __init__(self, sandbox: bool = True) -> None:
        self.sandbox = sandbox
        self.base = self.SANDBOX_URL if sandbox else self.BASE_URL
        self.client_id = os.getenv("ABSHE_CLIENT_ID", "")
        self.client_secret = os.getenv("ABSHE_CLIENT_SECRET", "")
        self.api_key = os.getenv("ABSHE_API_KEY", "")
        self._client: httpx.AsyncClient | None = None
        self._access_token: str | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-Client-ID": self.client_id,
                    "X-API-Key": self.api_key,
                },
            )
        return self._client

    async def _authenticate(self) -> str:
        """Authenticate with Absher API and get access token."""
        if self._access_token:
            return self._access_token

        client = await self._get_client()

        try:
            resp = await client.post(
                f"{self.base}/auth/token",
                json={
                    "clientId": self.client_id,
                    "clientSecret": self.client_secret,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            self._access_token = data.get("accessToken", "")
            return self._access_token

        except httpx.HTTPStatusError as exc:
            log.error(
                "absher_auth_failed",
                status_code=exc.response.status_code,
            )
            raise

    async def verify_identity(self, national_id: str, birth_date: str) -> VerificationResult:
        """Verify identity by matching national ID with date of birth.

        Used for KYC (Know Your Customer) compliance.
        Returns match score and basic profile data if verified.
        """
        client = await self._get_client()
        token = await self._authenticate()
        request_id = str(uuid.uuid4())

        payload: dict[str, Any] = {
            "nationalId": national_id,
            "dateOfBirth": birth_date,
            "requestId": request_id,
            "service": "Dealix KYC Verification",
        }

        signature = self._sign_payload(payload)
        payload["signature"] = signature

        try:
            resp = await client.post(
                f"{self.base}/identity/verify",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

            is_verified = data.get("verified", False) or data.get("match", False)
            log.info(
                "absher_identity_verification",
                national_id=national_id[-4:],
                verified=is_verified,
            )

            return VerificationResult(
                verified=is_verified,
                national_id=national_id,
                full_name_ar=data.get("fullNameAr"),
                full_name_en=data.get("fullNameEn"),
                match_score=data.get("matchScore", 1.0 if is_verified else 0.0),
                request_id=request_id,
            )

        except httpx.HTTPStatusError as exc:
            log.error(
                "absher_verify_failed",
                national_id=national_id[-4:],
                status_code=exc.response.status_code,
            )
            return VerificationResult(
                verified=False,
                national_id=national_id,
                error_message=f"Verification failed: HTTP {exc.response.status_code}",
                request_id=request_id,
            )

    async def get_user_profile(self, absher_id: str) -> UserProfile:
        """Retrieve full user profile from Absher."""
        client = await self._get_client()
        token = await self._authenticate()

        try:
            resp = await client.get(
                f"{self.base}/user/profile/{absher_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()

            return UserProfile(
                absher_id=absher_id,
                national_id=data.get("nationalId", ""),
                full_name_ar=data.get("fullNameAr", ""),
                full_name_en=data.get("fullNameEn", ""),
                date_of_birth=data.get("dateOfBirth", ""),
                gender=data.get("gender", ""),
                nationality=data.get("nationality", "SAU"),
                phone_number=data.get("phoneNumber"),
                email=data.get("email"),
                address=data.get("address"),
                city=data.get("city"),
                country=data.get("country", "Saudi Arabia"),
                is_active=data.get("isActive", True),
            )

        except httpx.HTTPStatusError as exc:
            log.error(
                "absher_profile_failed",
                absher_id=absher_id,
                status_code=exc.response.status_code,
            )
            raise

    async def verify_document(self, national_id: str, document_type: str, document_number: str) -> bool:
        """Verify a government-issued document (national ID, passport, iqama).

        Args:
            national_id: The person's national ID / iqama number
            document_type: 'national_id', 'passport', 'iqama'
            document_number: The document number to verify
        """
        client = await self._get_client()
        token = await self._authenticate()

        payload = {
            "nationalId": national_id,
            "documentType": document_type,
            "documentNumber": document_number,
            "timestamp": str(int(time.time())),
        }

        signature = self._sign_payload(payload)
        payload["signature"] = signature

        try:
            resp = await client.post(
                f"{self.base}/document/verify",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("verified", False)

        except httpx.HTTPStatusError as exc:
            log.error(
                "absher_document_verify_failed",
                document_type=document_type,
                status_code=exc.response.status_code,
            )
            return False

    def _sign_payload(self, payload: dict[str, Any]) -> str:
        """Create HMAC-SHA256 signature for request integrity."""
        message = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        key = self.client_secret.encode() if self.client_secret else b""
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
