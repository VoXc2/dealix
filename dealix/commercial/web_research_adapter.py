"""Bounded read-only web-research adapter for the existing Market Radar.

Tavily is the first admitted web-coverage candidate because one API currently
provides search, extract, crawl, map and research endpoints.  This adapter does
not create commercial truth or external execution authority and does not run
unless explicitly enabled with an API key at runtime.
"""
from __future__ import annotations

import hashlib
import os
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field

Endpoint = Literal["search", "extract", "crawl", "map", "research"]
SCHEMA = "dealix.web-research-receipt.v1"
AUTHORITY = {
    "relationship": False,
    "consent": False,
    "opportunity": False,
    "offer": False,
    "quote": False,
    "contract": False,
    "external_send": False,
    "payment": False,
    "customer_proof": False,
    "execution": False,
    "production": False,
}


class WebResearchReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = SCHEMA
    request_id: str
    adapter: str = "TAVILY_READ_ONLY"
    endpoint: Endpoint
    observed_at: str
    fresh_until: str
    source_refs: list[str]
    source_count: int
    result_digest: str
    status: str
    authority: dict[str, bool] = Field(default_factory=lambda: dict(AUTHORITY))
    next_evidence: list[str] = Field(default_factory=list)


class WebResearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    receipt: WebResearchReceipt
    payload: Any = None


def _urls(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in {"url", "source", "source_url"} and isinstance(child, str) and child.startswith(("http://", "https://")):
                found.append(child)
            else:
                found.extend(_urls(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_urls(child))
    return sorted(set(found))


def _digest(value: Any) -> str:
    import json

    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class TavilyReadOnlyAdapter:
    """Direct HTTP adapter using Dealix's existing ``httpx`` dependency."""

    BASE_URL = "https://api.tavily.com"
    ALLOWED_ENDPOINTS = {"search", "extract", "crawl", "map", "research"}

    def __init__(
        self,
        *,
        api_key: str | None = None,
        enabled: bool = False,
        timeout_seconds: float = 45.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._api_key = (api_key or os.environ.get("TAVILY_API_KEY", "")).strip()
        self._enabled = bool(enabled)
        self._timeout = timeout_seconds
        self._transport = transport

    @property
    def access_state(self) -> str:
        if not self._enabled:
            return "BLOCKED_NOT_EXPLICITLY_ENABLED"
        if not self._api_key:
            return "BLOCKED_MISSING_API_KEY"
        return "READ_ONLY_READY"

    def execute(
        self,
        *,
        endpoint: Endpoint,
        payload: dict[str, Any],
        request_id: str,
        freshness_hours: int = 24,
    ) -> WebResearchResult:
        if endpoint not in self.ALLOWED_ENDPOINTS:
            raise ValueError(f"endpoint not admitted: {endpoint}")
        if self.access_state != "READ_ONLY_READY":
            now = datetime.now(UTC)
            receipt = WebResearchReceipt(
                request_id=request_id,
                endpoint=endpoint,
                observed_at=now.isoformat(),
                fresh_until=now.isoformat(),
                source_refs=[],
                source_count=0,
                result_digest=_digest({"blocked": self.access_state}),
                status=self.access_state,
                next_evidence=["ENABLE_BOUNDED_READ_ONLY_ADAPTER_AND_PROVIDE_SECRET_OUTSIDE_GIT"],
            )
            return WebResearchResult(receipt=receipt, payload=None)

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "X-Project-ID": "dealix-market-radar",
        }
        with httpx.Client(timeout=self._timeout, transport=self._transport) as client:
            response = client.post(f"{self.BASE_URL}/{endpoint}", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        now = datetime.now(UTC)
        refs = _urls(data)
        receipt = WebResearchReceipt(
            request_id=request_id,
            endpoint=endpoint,
            observed_at=now.isoformat(),
            fresh_until=(now + timedelta(hours=max(1, freshness_hours))).isoformat(),
            source_refs=refs,
            source_count=len(refs),
            result_digest=_digest(data),
            status="READ_ONLY_RESULT_RECEIVED",
            next_evidence=["NORMALIZE_SOURCE_BOUND_FACTS_BEFORE_MARKET_RADAR_ADMISSION"],
        )
        return WebResearchResult(receipt=receipt, payload=data)


__all__ = ["AUTHORITY", "TavilyReadOnlyAdapter", "WebResearchReceipt", "WebResearchResult"]
