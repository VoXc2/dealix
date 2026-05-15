"""ROI cost + value model.

Two kinds of figure, kept strictly separate:
  - VERIFIED cost — LLM spend computed from the model router's actual
    recorded token usage. Evidence: ``core.llm.router.usage_summary``.
  - ESTIMATED value — operational value projected from activity counts
    using documented, conservative assumptions. Never presented as
    verified.
"""
from __future__ import annotations

__all__ = [
    "USD_TO_SAR",
    "ANALYST_HOURLY_SAR",
    "MINUTES_SAVED_PER_GROUNDED_ANSWER",
    "MINUTES_SAVED_PER_AGENT_RUN",
    "llm_cost_sar_from_usage",
    "estimated_value_from_activity",
]

# ── Documented assumptions (conservative; tune per engagement) ────────
USD_TO_SAR: float = 3.75
ANALYST_HOURLY_SAR: float = 75.0
MINUTES_SAVED_PER_GROUNDED_ANSWER: float = 8.0
MINUTES_SAVED_PER_AGENT_RUN: float = 15.0

# USD per 1M tokens (input, output) — mirrors core.config.models.COST_HINTS.
_FALLBACK_COST_PER_MTOK: tuple[float, float] = (3.00, 15.00)


def llm_cost_sar_from_usage() -> float:
    """VERIFIED LLM cost in SAR, from the router's recorded token usage.

    Returns 0.0 when no LLM calls have been made (e.g. fully deterministic
    runs) — an honest zero, not an estimate.
    """
    try:
        from core.config.models import COST_HINTS, Provider
        from core.llm.router import get_router

        usage = get_router().usage_summary()
    except Exception:  # noqa: BLE001
        return 0.0

    total_usd = 0.0
    for provider_name, record in usage.items():
        try:
            in_rate, out_rate = COST_HINTS.get(Provider(provider_name), _FALLBACK_COST_PER_MTOK)
        except Exception:  # noqa: BLE001
            in_rate, out_rate = _FALLBACK_COST_PER_MTOK
        total_usd += (record.get("input_tokens", 0) / 1_000_000) * in_rate
        total_usd += (record.get("output_tokens", 0) / 1_000_000) * out_rate
    return round(total_usd * USD_TO_SAR, 4)


def estimated_value_from_activity(
    grounded_answers: int,
    successful_agent_runs: int,
) -> tuple[float, float]:
    """ESTIMATED operational value of AI activity.

    Returns ``(hours_saved, value_sar)``. This is a projection from
    documented assumptions — it is an estimate, never a verified outcome.
    """
    minutes = (
        grounded_answers * MINUTES_SAVED_PER_GROUNDED_ANSWER
        + successful_agent_runs * MINUTES_SAVED_PER_AGENT_RUN
    )
    hours = round(minutes / 60.0, 4)
    value_sar = round(hours * ANALYST_HOURLY_SAR, 2)
    return hours, value_sar
