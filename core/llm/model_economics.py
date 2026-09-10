"""Model registry economics and request/effective-model telemetry.

This module is deliberately side-effect free: it does not change routing,
provider credentials, billing, or production configuration.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

REGISTRY_PATH = Path(__file__).resolve().parents[2] / "data" / "ai_ops" / "model_registry.yaml"
CacheStatus = Literal["hit", "miss", "unknown"]


def load_registry(path: Path = REGISTRY_PATH) -> list[dict[str, Any]]:
    """Load the JSON-compatible YAML registry without adding a YAML runtime dependency."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("model registry must be a list")
    return payload


def find_model(model_name: str, registry: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    """Resolve a canonical model name or documented legacy alias."""
    for entry in registry or load_registry():
        if entry.get("model_name") == model_name:
            return entry
        for alias in entry.get("legacy_aliases", []):
            if alias.get("model_name") == model_name:
                return entry
    return None


def production_allowed(model_name: str, *, on_date: str | None = None) -> bool:
    """Fail closed for non-production or expired model IDs."""
    entry = find_model(model_name)
    if not entry or not entry.get("production_eligible", False):
        return False
    day = on_date or datetime.now(UTC).date().isoformat()
    expires_on = entry.get("expires_on")
    return not expires_on or day < str(expires_on)


def _rate(pricing: dict[str, Any], cache_status: CacheStatus, output: bool) -> float:
    basis = pricing.get("budget_basis", "peak")
    rate_card = pricing.get(basis) or pricing.get("peak") or pricing.get("off_peak") or {}
    if output:
        return float(rate_card.get("output", 0.0))
    if cache_status == "hit":
        return float(rate_card.get("cache_hit", rate_card.get("cache_miss", 0.0)))
    return float(rate_card.get("cache_miss", 0.0))


def estimate_budget_cost_usd(model_name: str, *, input_tokens: int, output_tokens: int, cache_status: CacheStatus = "unknown") -> float | None:
    """Estimate cost using the registry's conservative budget basis (peak for DeepSeek)."""
    entry = find_model(model_name)
    if not entry or "pricing" not in entry:
        return None
    pricing = entry["pricing"]
    if pricing.get("rate_card_verified") is False:
        return None
    unit = float(pricing.get("unit_tokens", 1_000_000))
    input_cost = input_tokens / unit * _rate(pricing, cache_status, False)
    output_cost = output_tokens / unit * _rate(pricing, cache_status, True)
    return round(input_cost + output_cost, 9)


@dataclass(frozen=True, slots=True)
class ModelUsageEvent:
    logical_route: str
    requested_model: str
    effective_model: str
    cache_status: CacheStatus
    input_tokens: int
    output_tokens: int
    retries: int
    accepted: bool
    occurred_at: str
    budget_cost_usd: float | None

    @property
    def cost_per_accepted_result_usd(self) -> float | None:
        return self.budget_cost_usd if self.accepted else None


def build_usage_event(*, logical_route: str, requested_model: str, effective_model: str, input_tokens: int, output_tokens: int, cache_status: CacheStatus = "unknown", retries: int = 0, accepted: bool = True) -> ModelUsageEvent:
    """Create an audit-safe event separating requested and provider-effective model IDs."""
    return ModelUsageEvent(
        logical_route=logical_route,
        requested_model=requested_model,
        effective_model=effective_model,
        cache_status=cache_status,
        input_tokens=max(0, input_tokens),
        output_tokens=max(0, output_tokens),
        retries=max(0, retries),
        accepted=accepted,
        occurred_at=datetime.now(UTC).isoformat(),
        budget_cost_usd=estimate_budget_cost_usd(
            effective_model,
            input_tokens=max(0, input_tokens),
            output_tokens=max(0, output_tokens),
            cache_status=cache_status,
        ),
    )
