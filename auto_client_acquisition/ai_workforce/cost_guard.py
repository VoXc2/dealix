"""Cost Guard — bounds API spend for the AI workforce (v7 Phase 4).

Pure deterministic budgeting. No LLM calls, no external HTTP, no cost API.
Estimates are derived from a static lookup table and used to gate workforce
runs against per-run / per-agent / monthly founder budgets.

Tiers map intent → model class without binding to a vendor model name:
    cheap_for_classification — short, structured tasks (intake, scoring)
    balanced_for_drafts      — Arabic/English drafts, summaries
    strong_for_strategy      — multi-step reasoning, weekly plans, audits
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CostBudget(BaseModel):
    """Rolling budget envelope enforced on every WorkforceRun."""

    model_config = ConfigDict(extra="forbid")

    per_run_budget_usd: float = 0.50
    per_agent_budget_usd: float = 0.10
    monthly_founder_budget_usd: float = 50.0
    warning_threshold_pct: float = 70.0
    hard_stop_threshold_pct: float = 100.0


class ModelTier(StrEnum):
    cheap_for_classification = "cheap_for_classification"
    balanced_for_drafts = "balanced_for_drafts"
    strong_for_strategy = "strong_for_strategy"


class CostEstimate(BaseModel):
    """Pre-run estimate of token + USD cost for a single workforce step."""

    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_usd: float
    model_tier: ModelTier
    cache_key: str = ""
    max_iterations: int = 3
    stop_when_good_enough: bool = True
    human_review_when_budget_exceeded: bool = True


# ── Deterministic intent → tier map ──────────────────────────────────────
# Anything containing one of these substrings (lower-case, underscore-friendly)
# is routed to the matching tier. Order matters: first hit wins. Keeping this
# intentionally short — purpose-bound, not exhaustive.
_TIER_KEYWORDS: tuple[tuple[ModelTier, tuple[str, ...]], ...] = (
    (
        ModelTier.cheap_for_classification,
        ("classification", "classify", "intake", "score", "tag", "label", "filter"),
    ),
    (
        ModelTier.balanced_for_drafts,
        ("draft", "summary", "summarize", "rewrite", "translate", "follow_up", "arabic_message"),
    ),
    (
        ModelTier.strong_for_strategy,
        ("strategy", "plan", "audit", "diagnostic_reasoning", "weekly_brief", "decision"),
    ),
)


def pick_model_tier(task_purpose: str) -> ModelTier:
    """Map a free-form task purpose string to a model tier."""
    needle = (task_purpose or "").strip().lower()
    for tier, keywords in _TIER_KEYWORDS:
        for kw in keywords:
            if kw in needle:
                return tier
    # Default to the cheapest tier — unknown intents must not silently
    # escalate to strong/expensive models.
    return ModelTier.cheap_for_classification


# ── Token-count + USD estimate per (tier, size) ──────────────────────────
# Numbers are bounded and conservative. They are NOT live billing rates,
# only an in-process planning heuristic used to gate runs.
SizeKey = Literal["small", "medium", "large"]

_TOKEN_TABLE: dict[ModelTier, dict[str, tuple[int, int]]] = {
    ModelTier.cheap_for_classification: {
        "small": (400, 80),
        "medium": (1_200, 200),
        "large": (3_000, 400),
    },
    ModelTier.balanced_for_drafts: {
        "small": (800, 300),
        "medium": (2_500, 700),
        "large": (6_000, 1_500),
    },
    ModelTier.strong_for_strategy: {
        "small": (2_000, 700),
        "medium": (5_000, 1_500),
        "large": (10_000, 3_000),
    },
}

# USD per 1K tokens — bounded planning rates, not live prices.
_RATE_PER_1K_INPUT_USD: dict[ModelTier, float] = {
    ModelTier.cheap_for_classification: 0.0005,
    ModelTier.balanced_for_drafts: 0.003,
    ModelTier.strong_for_strategy: 0.015,
}
_RATE_PER_1K_OUTPUT_USD: dict[ModelTier, float] = {
    ModelTier.cheap_for_classification: 0.0015,
    ModelTier.balanced_for_drafts: 0.012,
    ModelTier.strong_for_strategy: 0.060,
}

# Hard ceiling per estimate — we never plan a single step that exceeds this.
_PER_ESTIMATE_USD_CEILING: float = 0.40


def estimate_for_task(task_purpose: str, expected_size: str = "medium") -> CostEstimate:
    """Deterministic cost estimate for a single workforce step.

    Pure: no I/O, no LLM, no clock. ``expected_size`` falls back to
    ``medium`` when not in {"small","medium","large"}.
    """
    tier = pick_model_tier(task_purpose)
    size = expected_size if expected_size in {"small", "medium", "large"} else "medium"
    in_tok, out_tok = _TOKEN_TABLE[tier][size]
    rate_in = _RATE_PER_1K_INPUT_USD[tier]
    rate_out = _RATE_PER_1K_OUTPUT_USD[tier]
    usd = (in_tok / 1000.0) * rate_in + (out_tok / 1000.0) * rate_out
    usd = round(min(usd, _PER_ESTIMATE_USD_CEILING), 6)
    cache_key = f"{tier.value}:{size}:{(task_purpose or '').strip().lower()[:40]}"
    return CostEstimate(
        estimated_input_tokens=in_tok,
        estimated_output_tokens=out_tok,
        estimated_usd=usd,
        model_tier=tier,
        cache_key=cache_key,
        max_iterations=3,
        stop_when_good_enough=True,
        human_review_when_budget_exceeded=True,
    )


def enforce_run_budget(
    estimates: list[CostEstimate],
    budget: CostBudget,
) -> dict:
    """Sum estimates and decide whether a workforce run may proceed.

    Returns a plain dict (cheap to log) with:
        within_budget: bool
        total_usd: float
        threshold_breached: "warning" | "hard_stop" | None
        action: "proceed" | "warn_founder" | "pause_for_approval" | "hard_stop"
    """
    total = round(sum(float(e.estimated_usd) for e in estimates), 6)
    cap = float(budget.per_run_budget_usd)
    if cap <= 0:
        # Zero or negative budget — block by default to avoid runaway runs.
        return {
            "within_budget": total == 0.0,
            "total_usd": total,
            "threshold_breached": "hard_stop",
            "action": "hard_stop" if total > 0 else "pause_for_approval",
        }

    pct = (total / cap) * 100.0
    hard_pct = float(budget.hard_stop_threshold_pct)
    warn_pct = float(budget.warning_threshold_pct)

    if pct >= hard_pct:
        return {
            "within_budget": False,
            "total_usd": total,
            "threshold_breached": "hard_stop",
            "action": "hard_stop",
        }
    if pct >= warn_pct:
        # Over the warning line but under the hard stop — pause for the
        # founder to approve continuation rather than warn-only.
        return {
            "within_budget": True,
            "total_usd": total,
            "threshold_breached": "warning",
            "action": "pause_for_approval" if pct >= 90.0 else "warn_founder",
        }
    return {
        "within_budget": True,
        "total_usd": total,
        "threshold_breached": None,
        "action": "proceed",
    }


__all__ = [
    "CostBudget",
    "CostEstimate",
    "ModelTier",
    "estimate_for_task",
    "enforce_run_budget",
    "pick_model_tier",
]
