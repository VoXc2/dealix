"""Per-call cost budget."""
from __future__ import annotations

from typing import Any


# Default budget caps (per single tool call)
_DEFAULT_MAX_TOKENS = 50_000
_DEFAULT_MAX_USD = 1.0  # cap any single call at $1


def check_cost_budget(
    *,
    estimated_tokens: int,
    estimated_usd: float,
    max_tokens: int = _DEFAULT_MAX_TOKENS,
    max_usd: float = _DEFAULT_MAX_USD,
) -> dict[str, Any]:
    """Returns {passed, reasons, budget_remaining}."""
    reasons: list[str] = []
    if estimated_tokens > max_tokens:
        reasons.append(f"tokens_over_cap:{estimated_tokens}>{max_tokens}")
    if estimated_usd > max_usd:
        reasons.append(f"usd_over_cap:{estimated_usd}>{max_usd}")
    return {
        "passed": len(reasons) == 0,
        "reasons": reasons,
        "estimated_tokens": estimated_tokens,
        "estimated_usd": estimated_usd,
        "max_tokens": max_tokens,
        "max_usd": max_usd,
    }
