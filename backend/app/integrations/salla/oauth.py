"""
Salla OAuth2 Flow — Easy Mode (Webhook-based).
Docs: https://docs.salla.dev/docs/installation/oauth

Flow:
1. Merchant clicks "Install" in Salla App Store
2. Salla redirects to our /auth/salla/callback with ?code=XXX
3. We exchange code for access_token + refresh_token
4. We store tokens in DB keyed by merchant_id
5. Salla sends app.store.authorize webhook with same data
"""
import os
import httpx
from typing import Optional
from urllib.parse import urlencode


SALLA_AUTH_URL = "https://accounts.salla.sa/oauth2/auth"
SALLA_TOKEN_URL = "https://accounts.salla.sa/oauth2/token"
SALLA_API_BASE = "https://api.salla.dev/admin/v2"


class SallaOAuth:
    """Handles Salla OAuth2 authorization and token refresh."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ):
        self.client_id = client_id or os.getenv("SALLA_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("SALLA_CLIENT_SECRET", "")
        self.redirect_uri = redirect_uri or os.getenv(
            "SALLA_REDIRECT_URI", "https://api.dealix.sa/auth/salla/callback"
        )

    def authorize_url(self, state: str, scope: str = "offline_access") -> str:
        """Build the authorization URL to redirect merchants to."""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": state,
        }
        return f"{SALLA_AUTH_URL}?{urlencode(params)}"

    async def exchange_code(self, code: str) -> dict:
        """Exchange authorization code for access token."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                SALLA_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "scope": "offline_access",
                },
            )
            resp.raise_for_status()
            return resp.json()
            # Returns: {access_token, refresh_token, expires_in, scope, token_type}

    async def refresh_token(self, refresh_token: str) -> dict:
        """Refresh an expired access token."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                SALLA_TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            resp.raise_for_status()
            return resp.json()
