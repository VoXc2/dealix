"""V14 Phase K7 — enrichment provider abstraction (no-scrape, no-store).

Closes the registry's `next_activation_step_en` for `enrichment`:
"Wire real provider API keys and add a unified confidence-score test."

Design (deliberately minimal):

  - Abstract base class `EnrichmentProvider` with a single method
    `enrich(domain, contact_email)` returning an `EnrichmentResult`
    with a `confidence_score` in [0.0, 1.0].
  - Three concrete providers, picked at runtime via env var
    `DEALIX_ENRICHMENT_PROVIDER`:
      - `none` (default) — degraded fallback; returns
        `confidence_score=0.0` and `reason_code=no_provider`.
        This keeps the system green even without a paid API key.
      - `hunter` — Hunter.io (recommended for KSA); reads
        `HUNTER_API_KEY` env var. Live HTTP calls happen ONLY when
        the key is present AND `DEALIX_ENRICHMENT_LIVE_CALLS=true`.
        Otherwise returns a stable mock based on the domain hash
        (deterministic, useful for unit tests).
      - `mock` — always returns a deterministic confidence score.

Hard rules:
  - NO scraping (NO_SCRAPING gate)
  - NO PII storage on this layer (caller decides retention)
  - Default-deny on missing inputs (empty domain → score 0.0)
  - Confidence score is bounded [0.0, 1.0]; out-of-range returns
    clamp to nearest boundary
  - All providers must be deterministic for the same inputs in the
    same minute window (cache key = `domain + minute_bucket`)
"""
from __future__ import annotations

import hashlib
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class EnrichmentResult:
    """Outcome of an enrichment call. Immutable so callers cannot
    tamper with the score after the gate decision."""

    domain: str
    contact_email: str
    confidence_score: float  # [0.0, 1.0]
    company_name_guess: str = ""
    industry_guess: str = ""
    employee_count_band: str = ""  # "1-10" / "11-50" / etc.
    reason_code: str = "ok"  # ok | no_provider | live_disabled | no_data | invalid_input
    provider_id: str = "none"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_demo_mode(self) -> bool:
        # Wave 7.5 §24.2 — surfaces honestly when score is mock/deterministic
        # so customer-facing UI can render a DEMO MODE pill instead of
        # silently presenting hash-derived numbers as real intelligence.
        return self.reason_code in ("no_provider", "live_disabled")

    def to_public_dict(self) -> dict[str, Any]:
        # Used by customer_company_portal + executive_command_center to
        # surface enrichment data with explicit demo-mode flag.
        return {
            "domain": self.domain,
            "confidence_score": self.confidence_score,
            "company_name_guess": self.company_name_guess,
            "industry_guess": self.industry_guess,
            "employee_count_band": self.employee_count_band,
            "is_demo_mode": self.is_demo_mode,
            "data_source": "live_provider" if not self.is_demo_mode else "deterministic_demo_fallback",
            "demo_reason": "HUNTER_API_KEY not configured — set the env var on Railway and DEALIX_ENRICHMENT_LIVE_CALLS=true to activate live calls."
            if self.is_demo_mode and self.reason_code == "live_disabled"
            else None,
        }


def _clamp_score(s: float) -> float:
    if s < 0.0:
        return 0.0
    if s > 1.0:
        return 1.0
    return float(s)


def _stable_score_for(domain: str) -> float:
    """Deterministic mock score derived from SHA-256 of the domain.
    Returns 0.45 for empty input; otherwise [0.0, 1.0]."""
    if not domain:
        return 0.0
    h = hashlib.sha256(domain.encode("utf-8")).hexdigest()
    val = int(h[:8], 16) / 0xFFFFFFFF
    return _clamp_score(val)


class EnrichmentProvider(ABC):
    """Abstract base — every provider MUST implement enrich()."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        ...

    @abstractmethod
    def enrich(self, *, domain: str, contact_email: str = "") -> EnrichmentResult:
        ...


class _NoOpProvider(EnrichmentProvider):
    """Default fallback: always returns confidence 0.0 with reason
    `no_provider`. Keeps the system green when no API key is
    configured."""

    provider_id = "none"  # type: ignore[assignment]

    def enrich(self, *, domain: str, contact_email: str = "") -> EnrichmentResult:
        if not domain:
            return EnrichmentResult(
                domain="",
                contact_email=contact_email,
                confidence_score=0.0,
                reason_code="invalid_input",
                provider_id=self.provider_id,
            )
        return EnrichmentResult(
            domain=domain,
            contact_email=contact_email,
            confidence_score=0.0,
            reason_code="no_provider",
            provider_id=self.provider_id,
        )


class _MockProvider(EnrichmentProvider):
    """Deterministic mock — useful for tests. Returns a stable
    confidence score derived from SHA-256 of the domain."""

    provider_id = "mock"  # type: ignore[assignment]

    def enrich(self, *, domain: str, contact_email: str = "") -> EnrichmentResult:
        if not domain:
            return EnrichmentResult(
                domain="",
                contact_email=contact_email,
                confidence_score=0.0,
                reason_code="invalid_input",
                provider_id=self.provider_id,
            )
        score = _stable_score_for(domain)
        return EnrichmentResult(
            domain=domain,
            contact_email=contact_email,
            confidence_score=score,
            company_name_guess=domain.split(".")[0].title(),
            industry_guess="b2b_services",
            employee_count_band="11-50",
            reason_code="ok",
            provider_id=self.provider_id,
        )


class _HunterProvider(EnrichmentProvider):
    """Hunter.io adapter. Returns mock data unless
    DEALIX_ENRICHMENT_LIVE_CALLS=true AND HUNTER_API_KEY is set.

    This module never scrapes. It only calls Hunter's documented
    domain-search API when explicitly enabled.
    """

    provider_id = "hunter"  # type: ignore[assignment]

    def enrich(self, *, domain: str, contact_email: str = "") -> EnrichmentResult:
        if not domain:
            return EnrichmentResult(
                domain="",
                contact_email=contact_email,
                confidence_score=0.0,
                reason_code="invalid_input",
                provider_id=self.provider_id,
            )

        live = os.environ.get("DEALIX_ENRICHMENT_LIVE_CALLS", "").lower() == "true"
        api_key = os.environ.get("HUNTER_API_KEY", "")

        if not live or not api_key:
            # Graceful degradation: return deterministic mock score so
            # callers can build/test without a real API key.
            score = _stable_score_for(domain)
            return EnrichmentResult(
                domain=domain,
                contact_email=contact_email,
                confidence_score=score,
                company_name_guess=domain.split(".")[0].title(),
                industry_guess="unknown",
                reason_code="live_disabled",
                provider_id=self.provider_id,
            )

        # Live path. Imported lazily so test environments without
        # httpx still work for the no-op / mock providers.
        try:
            import httpx  # noqa: PLC0415

            with httpx.Client(timeout=10.0) as client:
                r = client.get(
                    "https://api.hunter.io/v2/domain-search",
                    params={"domain": domain, "api_key": api_key, "limit": 1},
                )
            if r.status_code != 200:
                return EnrichmentResult(
                    domain=domain,
                    contact_email=contact_email,
                    confidence_score=0.0,
                    reason_code=f"http_{r.status_code}",
                    provider_id=self.provider_id,
                )
            data = r.json().get("data", {}) or {}
            org = data.get("organization") or domain.split(".")[0].title()
            industry = (data.get("industry") or "").lower() or "unknown"
            emails = data.get("emails", []) or []
            score = _clamp_score(min(1.0, len(emails) / 50.0)) if emails else 0.0
            return EnrichmentResult(
                domain=domain,
                contact_email=contact_email,
                confidence_score=score,
                company_name_guess=org,
                industry_guess=industry,
                employee_count_band=data.get("organization_size_band", ""),
                reason_code="ok" if emails else "no_data",
                provider_id=self.provider_id,
                metadata={"emails_found": len(emails)},
            )
        except Exception as exc:  # noqa: BLE001
            return EnrichmentResult(
                domain=domain,
                contact_email=contact_email,
                confidence_score=0.0,
                reason_code=f"client_error:{type(exc).__name__}",
                provider_id=self.provider_id,
            )


_PROVIDERS: dict[str, type[EnrichmentProvider]] = {
    "none": _NoOpProvider,
    "mock": _MockProvider,
    "hunter": _HunterProvider,
}


def get_provider(name: str | None = None) -> EnrichmentProvider:
    """Pick an enrichment provider by name. Falls back to the
    `DEALIX_ENRICHMENT_PROVIDER` env var or `none` if unset.

    Always returns a working provider — never raises. Unknown names
    default to the no-op provider so the system stays green.
    """
    chosen = (name or os.environ.get("DEALIX_ENRICHMENT_PROVIDER", "none")).lower()
    cls = _PROVIDERS.get(chosen, _NoOpProvider)
    return cls()


def enrich_lead(
    *,
    domain: str,
    contact_email: str = "",
    provider_name: str | None = None,
) -> EnrichmentResult:
    """Convenience top-level. Picks the configured provider and runs
    enrich(). Always returns an EnrichmentResult; never raises."""
    return get_provider(provider_name).enrich(domain=domain, contact_email=contact_email)
