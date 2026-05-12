"""
WorkOS SSO — SAML / OIDC / Magic Link + SCIM Directory Sync.

We do NOT pull the `workos` Python SDK at import time so the app keeps
booting without the optional dep installed; instead we wrap the REST API
with httpx. The SDK can be swapped in later by replacing this file —
the public method names are deliberately a subset of `workos.client`.

Public surface:
    WorkOSClient().is_configured
    WorkOSClient().build_authorization_url(redirect_uri, state, connection_id?)
    WorkOSClient().exchange_code(code) -> profile dict
    WorkOSClient().admin_portal_link(tenant_id, intent="sso")

Tenant mapping: a tenant_id maps to one WorkOS `organization_id` stored
in `TenantRecord.meta_json["workos_org_id"]`. The frontend redirects the
admin to the WorkOS Admin Portal where they configure their IdP.

Reference: https://workos.com/docs/reference
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class WorkOSProfile:
    id: str
    email: str
    first_name: str | None
    last_name: str | None
    organization_id: str | None
    raw: dict[str, Any]


class WorkOSNotConfigured(RuntimeError):
    pass


class WorkOSClient:
    BASE = "https://api.workos.com"

    def __init__(self, api_key: str | None = None, client_id: str | None = None) -> None:
        self.api_key = (api_key or os.getenv("WORKOS_API_KEY", "")).strip()
        self.client_id = (client_id or os.getenv("WORKOS_CLIENT_ID", "")).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.client_id)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def build_authorization_url(
        self,
        *,
        redirect_uri: str,
        state: str | None = None,
        connection_id: str | None = None,
        organization_id: str | None = None,
        provider: str | None = None,
    ) -> str:
        """Build the WorkOS SSO URL that the user is redirected to."""
        if not self.is_configured:
            raise WorkOSNotConfigured("WORKOS_API_KEY / WORKOS_CLIENT_ID missing")
        params: dict[str, str] = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state or secrets.token_urlsafe(16),
        }
        if connection_id:
            params["connection_id"] = connection_id
        elif organization_id:
            params["organization_id"] = organization_id
        elif provider:
            params["provider"] = provider
        return f"{self.BASE}/sso/authorize?{urlencode(params)}"

    async def exchange_code(self, code: str) -> WorkOSProfile:
        """Exchange the authorization code for a profile."""
        if not self.is_configured:
            raise WorkOSNotConfigured("WORKOS_API_KEY / WORKOS_CLIENT_ID missing")
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{self.BASE}/sso/token",
                headers=self._headers(),
                json={
                    "client_id": self.client_id,
                    "client_secret": self.api_key,
                    "grant_type": "authorization_code",
                    "code": code,
                },
            )
            r.raise_for_status()
            data = r.json()
        profile = data.get("profile") or {}
        return WorkOSProfile(
            id=profile.get("id", ""),
            email=profile.get("email", ""),
            first_name=profile.get("first_name"),
            last_name=profile.get("last_name"),
            organization_id=profile.get("organization_id"),
            raw=profile,
        )

    async def admin_portal_link(
        self, organization_id: str, intent: str = "sso"
    ) -> str:
        """Return a one-time link to the WorkOS Admin Portal for the org."""
        if not self.is_configured:
            raise WorkOSNotConfigured("WORKOS_API_KEY / WORKOS_CLIENT_ID missing")
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{self.BASE}/portal/generate_link",
                headers=self._headers(),
                json={"organization": organization_id, "intent": intent},
            )
            r.raise_for_status()
            return r.json().get("link", "")


_singleton: WorkOSClient | None = None


def get_workos_client() -> WorkOSClient:
    global _singleton
    if _singleton is None:
        _singleton = WorkOSClient()
    return _singleton
