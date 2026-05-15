"""Static model route cost table (update from finance; deterministic reads)."""

from __future__ import annotations

_DEFAULT_USD_PER_1K: dict[str, float] = {
    "economy_route": 0.002,
    "standard_route": 0.02,
    "premium_ar_exec_route": 0.08,
}


def usd_per_1k_tokens(model_route: str) -> float:
    return _DEFAULT_USD_PER_1K.get(model_route, _DEFAULT_USD_PER_1K["standard_route"])


def estimate_run_cost_usd(model_route: str, prompt_tokens: int, completion_tokens: int) -> float:
    unit = usd_per_1k_tokens(model_route)
    k = (max(0, prompt_tokens) + max(0, completion_tokens)) / 1000.0
    return round(unit * k, 6)


__all__ = ["estimate_run_cost_usd", "usd_per_1k_tokens"]
