"""
OpenID Connect (OIDC) authentication provider.
مزوّد المصادقة عبر OpenID Connect.

Supports Azure AD, Google Workspace, and custom OIDC providers.
Each provider is mapped per-tenant through tenant settings.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlencode

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class OIDCTokens:
    access_token: str
    id_token: str
    refresh_token: str | None = None
    expires_in: int = 3600
    token_type: str = "Bearer"
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class OIDCUserInfo:
    sub: str
    email: str
    name: str
    preferred_username: str | None = None
    picture: str | None = None
    tenant_id: str | None = None
    raw_attributes: dict[str, Any] = field(default_factory=dict)


class OIDCAuth:
    """OpenID Connect authentication provider.

    Supports multiple providers via a registry pattern.
    Each tenant can configure their own OIDC provider through settings.
    """

    PROVIDERS: dict[str, dict[str, Any]] = {
        "azure_ad": {
            "issuer": "https://login.microsoftonline.com/{tenant}/v2.0",
            "scopes": ["openid", "profile", "email"],
            "authorization_endpoint": "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize",
            "token_endpoint": "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
            "jwks_uri": "https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys",
        },
        "google": {
            "issuer": "https://accounts.google.com",
            "scopes": ["openid", "profile", "email"],
            "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
        },
    }

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=15)

    def _get_client_config(self, provider: str) -> dict[str, Any]:
        """Get provider config, supporting custom providers via env vars."""
        if provider in self.PROVIDERS:
            config = dict(self.PROVIDERS[provider])
            azure_tenant = os.getenv("AZURE_AD_TENANT_ID", "common")
            return {
                k: v.format(tenant=azure_tenant) if isinstance(v, str) else v
                for k, v in config.items()
            }
        # Custom OIDC provider via environment variables
        config = {
            "issuer": os.getenv(f"OIDC_{provider.upper()}_ISSUER", ""),
            "scopes": os.getenv(f"OIDC_{provider.upper()}_SCOPES", "openid,profile,email").split(","),
            "authorization_endpoint": os.getenv(f"OIDC_{provider.upper()}_AUTH_URL", ""),
            "token_endpoint": os.getenv(f"OIDC_{provider.upper()}_TOKEN_URL", ""),
            "jwks_uri": os.getenv(f"OIDC_{provider.upper()}_JWKS_URL", ""),
        }
        if not config["issuer"]:
            raise ValueError(f"Unknown OIDC provider: {provider}")
        return config

    def _get_client_credentials(self, provider: str) -> tuple[str, str]:
        """Get client ID and secret for the given provider."""
        client_id = os.getenv(
            f"OIDC_{provider.upper()}_CLIENT_ID",
            os.getenv("OIDC_CLIENT_ID", ""),
        )
        client_secret = os.getenv(
            f"OIDC_{provider.upper()}_CLIENT_SECRET",
            os.getenv("OIDC_CLIENT_SECRET", ""),
        )
        return client_id, client_secret

    async def get_auth_url(self, provider: str, redirect_uri: str) -> str:
        """Generate the OIDC authorization URL for the given provider."""
        config = self._get_client_config(provider)
        client_id, _ = self._get_client_credentials(provider)
        state = str(uuid.uuid4())
        nonce = str(uuid.uuid4())

        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(config["scopes"]),
            "state": state,
            "nonce": nonce,
        }
        auth_url = f"{config['authorization_endpoint']}?{urlencode(params)}"
        return auth_url

    async def handle_callback(self, provider: str, code: str, redirect_uri: str) -> OIDCTokens:
        """Exchange the authorization code for tokens."""
        config = self._get_client_config(provider)
        client_id, client_secret = self._get_client_credentials(provider)

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        resp = await self._client.post(config["token_endpoint"], data=payload)
        resp.raise_for_status()
        data = resp.json()

        return OIDCTokens(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in", 3600),
            token_type=data.get("token_type", "Bearer"),
            raw_response=data,
        )

    async def get_user_info(self, provider: str, access_token: str) -> OIDCUserInfo:
        """Retrieve user info from the OIDC provider's UserInfo endpoint."""
        config = self._get_client_config(provider)
        userinfo_endpoint = config.get(
            "userinfo_endpoint",
            config["issuer"].rstrip("/") + "/userinfo"
            if not config["issuer"].startswith("https://accounts.google")
            else "https://www.googleapis.com/oauth2/v3/userinfo",
        )

        resp = await self._client.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        resp.raise_for_status()
        data = resp.json()

        return OIDCUserInfo(
            sub=data.get("sub", ""),
            email=data.get("email", ""),
            name=data.get("name", ""),
            preferred_username=data.get("preferred_username"),
            picture=data.get("picture"),
            tenant_id=data.get("tid"),
            raw_attributes=data,
        )

    async def refresh_tokens(self, provider: str, refresh_token: str) -> OIDCTokens:
        """Refresh access tokens using a refresh token."""
        config = self._get_client_config(provider)
        client_id, client_secret = self._get_client_credentials(provider)

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        resp = await self._client.post(config["token_endpoint"], data=payload)
        resp.raise_for_status()
        data = resp.json()

        return OIDCTokens(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            refresh_token=data.get("refresh_token", refresh_token),
            expires_in=data.get("expires_in", 3600),
            token_type=data.get("token_type", "Bearer"),
            raw_response=data,
        )

    async def close(self) -> None:
        await self._client.aclose()
