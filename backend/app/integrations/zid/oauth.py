"""
Zid OAuth2 Flow.
تدفق OAuth2 لمنصة زد.

Docs: https://docs.zid.sa/reference/authentication

Flow:
1. Merchant opens Dealix from Zid App Market
2. Zid passes X-Manager-Token + X-Manager-Store-Id in headers (Easy Flow)
   OR redirects to our callback with ?code=XXX (Standard OAuth2)
3. We exchange code for access_token using client_credentials or auth_code grant
4. Store tokens keyed by manager_id / store_id

Environment variables:
- ZID_CLIENT_ID
- ZID_CLIENT_SECRET
- ZID_REDIRECT_URI
"""

from __future__ import annotations

import os
import logging
from typing import Optional
from urllib.parse import urlencode

import httpx

logger = logging.getLogger(__name__)

# TODO: Confirm exact auth base URL from Zid developer portal
# https://docs.zid.sa/reference/authentication
ZID_AUTH_BASE = "https://api.zid.sa"
ZID_AUTHORIZE_URL = f"{ZID_AUTH_BASE}/v1/oauth/authorize"
ZID_TOKEN_URL = f"{ZID_AUTH_BASE}/v1/oauth/token"
ZID_API_BASE = "https://api.zid.sa/v1"


class ZidOAuth:
    """
    Handles Zid OAuth2 authorization and token lifecycle.
    يدير دورة حياة OAuth2 مع منصة زد.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ) -> None:
        self.client_id = client_id or os.getenv("ZID_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("ZID_CLIENT_SECRET", "")
        self.redirect_uri = redirect_uri or os.getenv(
            "ZID_REDIRECT_URI", "https://api.dealix.sa/auth/zid/callback"
        )

    def authorize_url(self, state: str, scope: str = "offline_access store.r orders.r") -> str:
        """
        Build the Zid authorization URL to redirect merchants to.
        بناء رابط تفويض زد لإعادة توجيه التجار.
        """
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": state,
        }
        return f"{ZID_AUTHORIZE_URL}?{urlencode(params)}"

    async def exchange_code(self, code: str) -> dict:
        """
        Exchange authorization code for access_token + refresh_token.
        استبدال رمز التفويض بـ access_token + refresh_token.

        Returns:
            dict with access_token, refresh_token, expires_in, scope
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                ZID_TOKEN_URL,
                json={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                },
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            resp.raise_for_status()
            return resp.json()

    async def refresh_token(self, refresh_token: str) -> dict:
        """
        Refresh an expired access token.
        تجديد رمز الوصول المنتهي.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                ZID_TOKEN_URL,
                json={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            resp.raise_for_status()
            return resp.json()

    async def revoke_token(self, token: str) -> bool:
        """
        Revoke an access or refresh token (on uninstall).
        إلغاء رمز الوصول (عند إلغاء التثبيت).

        TODO: Confirm revoke endpoint from Zid docs.
        """
        # TODO: Verify endpoint path from https://docs.zid.sa/reference/authentication
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(
                    f"{ZID_AUTH_BASE}/v1/oauth/revoke",
                    json={"token": token, "client_id": self.client_id},
                    headers={"Accept": "application/json"},
                )
                return resp.status_code in (200, 204)
            except Exception as exc:
                logger.warning(f"Zid token revoke failed: {exc}")
                return False
