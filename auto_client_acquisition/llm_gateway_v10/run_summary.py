"""Aggregate routing decisions for founder-facing run summaries."""
from __future__ import annotations

from auto_client_acquisition.llm_gateway_v10.schemas import (
    ModelTier,
    RoutingDecision,
)


def summarize_run(decisions: list[RoutingDecision]) -> dict:
    """Return totals + per-tier breakdown for ``decisions``.

    Defensive — empty list returns zeros; per-tier counts always
    include all four tiers (zero where absent).
    """
    try:
        total_usd = 0.0
        total_input = 0
        total_output = 0
        per_tier: dict[str, dict] = {
            t.value: {"count": 0, "usd": 0.0, "input_tokens": 0, "output_tokens": 0}
            for t in ModelTier
        }
        actions: dict[str, int] = {}
        for d in decisions or []:
            est = d.cost_estimate
            total_usd += float(est.estimated_usd or 0.0)
            total_input += int(est.estimated_input_tokens or 0)
            total_output += int(est.estimated_output_tokens or 0)
            slot = per_tier[d.tier.value]
            slot["count"] += 1
            slot["usd"] = round(slot["usd"] + float(est.estimated_usd or 0.0), 6)
            slot["input_tokens"] += int(est.estimated_input_tokens or 0)
            slot["output_tokens"] += int(est.estimated_output_tokens or 0)
            actions[d.action] = actions.get(d.action, 0) + 1
        return {
            "decision_count": len(decisions or []),
            "total_usd": round(total_usd, 6),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "per_tier": per_tier,
            "actions": actions,
        }
    except Exception:  # noqa: BLE001 - defensive default
        return {
            "decision_count": 0,
            "total_usd": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "per_tier": {t.value: {"count": 0, "usd": 0.0, "input_tokens": 0, "output_tokens": 0} for t in ModelTier},
            "actions": {},
        }
