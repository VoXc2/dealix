"""
Portkey LLM gateway — routes Anthropic / OpenAI / Google calls through a
single proxy that adds: automatic provider fallback, prompt caching,
per-tenant cost attribution, latency p95 dashboards.

We do NOT make Portkey a hard dependency. The module is import-safe
without `portkey-ai` installed; callers check `is_enabled()` and only
swap providers when the gateway is fully wired.

Public surface:
    PortkeyConfig.is_enabled()
    PortkeyConfig.anthropic_kwargs(tenant_id=...) -> dict
    PortkeyConfig.openai_kwargs(tenant_id=...) -> dict

These kwargs are merged into the Anthropic / OpenAI client constructors:
    Anthropic(**PortkeyConfig.anthropic_kwargs(tenant_id=t))
which causes the SDK to point at Portkey's gateway with the per-tenant
metadata header set.

Reference: https://docs.portkey.ai/docs/integrations/llms/anthropic
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)

_GATEWAY_BASE = "https://api.portkey.ai/v1"


@dataclass
class PortkeyConfig:
    api_key: str
    virtual_anthropic_key: str
    virtual_openai_key: str
    virtual_google_key: str

    @classmethod
    def from_env(cls) -> "PortkeyConfig | None":
        api_key = os.getenv("PORTKEY_API_KEY", "").strip()
        if not api_key:
            return None
        return cls(
            api_key=api_key,
            virtual_anthropic_key=os.getenv("PORTKEY_VIRTUAL_KEY_ANTHROPIC", "").strip(),
            virtual_openai_key=os.getenv("PORTKEY_VIRTUAL_KEY_OPENAI", "").strip(),
            virtual_google_key=os.getenv("PORTKEY_VIRTUAL_KEY_GOOGLE", "").strip(),
        )

    @staticmethod
    def is_enabled() -> bool:
        return bool(os.getenv("PORTKEY_API_KEY", "").strip())

    # -- helpers ----------------------------------------------------

    def _common_headers(self, tenant_id: str | None) -> dict[str, str]:
        headers = {
            "x-portkey-api-key": self.api_key,
        }
        if tenant_id:
            # Portkey ingests this into the metadata column of the
            # request log; the cost dashboard groups by it.
            headers["x-portkey-metadata"] = (
                '{"_user":"' + tenant_id + '","tenant_id":"' + tenant_id + '"}'
            )
        return headers

    def anthropic_kwargs(self, tenant_id: str | None = None) -> dict[str, Any]:
        """Anthropic SDK kwargs that route through Portkey."""
        headers = self._common_headers(tenant_id)
        if self.virtual_anthropic_key:
            headers["x-portkey-virtual-key"] = self.virtual_anthropic_key
        else:
            headers["x-portkey-provider"] = "anthropic"
        return {
            "base_url": _GATEWAY_BASE,
            "default_headers": headers,
        }

    def openai_kwargs(self, tenant_id: str | None = None) -> dict[str, Any]:
        headers = self._common_headers(tenant_id)
        if self.virtual_openai_key:
            headers["x-portkey-virtual-key"] = self.virtual_openai_key
        else:
            headers["x-portkey-provider"] = "openai"
        return {
            "base_url": _GATEWAY_BASE,
            "default_headers": headers,
        }

    def google_kwargs(self, tenant_id: str | None = None) -> dict[str, Any]:
        """Google Generative AI doesn't take base_url at SDK level the same
        way — return the headers + base URL for the caller to use with
        an httpx-based wrapper."""
        headers = self._common_headers(tenant_id)
        if self.virtual_google_key:
            headers["x-portkey-virtual-key"] = self.virtual_google_key
        else:
            headers["x-portkey-provider"] = "google"
        return {"base_url": _GATEWAY_BASE, "headers": headers}


def get_portkey_config() -> PortkeyConfig | None:
    """Singleton config, refreshed if env mutates (mainly for tests)."""
    return PortkeyConfig.from_env()


def with_portkey_metadata(client_kwargs: dict[str, Any], tenant_id: str) -> dict[str, Any]:
    """Convenience helper for one-off LLM client constructors.

    Usage:
        kwargs = with_portkey_metadata({}, tenant_id="ten_abc")
        client = Anthropic(**kwargs)

    Returns the *original* kwargs unchanged when Portkey is not configured,
    so call sites can adopt this everywhere safely.
    """
    cfg = get_portkey_config()
    if cfg is None:
        return client_kwargs
    return {**client_kwargs, **cfg.anthropic_kwargs(tenant_id=tenant_id)}
