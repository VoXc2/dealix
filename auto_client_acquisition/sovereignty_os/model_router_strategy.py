"""Model router strategy — governed routing, not raw vendor lock-in."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RouterTier = Literal["cheap", "balanced", "premium", "rules_only"]


@dataclass(frozen=True, slots=True)
class ModelRouterContext:
    task_type: str
    risk_level: str  # low/medium/high
    contains_pii: bool
    language: str
    required_quality: str  # low/medium/high
    latency_need: str = "normal"  # low/normal/high
    cost_budget_tight: bool = False


def route_model_decision(ctx: ModelRouterContext) -> tuple[RouterTier, tuple[str, ...]]:
    """Return tier + recommended enforcement tags (deterministic)."""
    tags: list[str] = []
    if ctx.contains_pii:
        tags.append("redaction_or_block_before_model")
        tags.append("human_review_queue")
    if ctx.risk_level == "high" or ctx.required_quality == "high":
        tier: RouterTier = "premium"
    elif ctx.cost_budget_tight and ctx.required_quality == "low" and not ctx.contains_pii:
        tier = "cheap"
    elif ctx.task_type.strip().lower() in {"classify", "tag", "route"} and not ctx.contains_pii:
        tier = "balanced"
    else:
        tier = "balanced"
    if ctx.language.strip().lower().startswith("ar") and ctx.required_quality == "high":
        tier = "premium"
        tags.append("arabic_quality_gate")
    if ctx.risk_level == "high" and ctx.contains_pii:
        tags = ["no_model_rules_only", "block_until_passport_clear"]
        return "rules_only", tuple(dict.fromkeys(tags))
    return tier, tuple(dict.fromkeys(tags))
