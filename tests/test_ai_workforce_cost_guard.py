"""Tests for auto_client_acquisition.ai_workforce.cost_guard (v7 Phase 4)."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_client_acquisition.ai_workforce.cost_guard import (
    CostBudget,
    CostEstimate,
    ModelTier,
    enforce_run_budget,
    estimate_for_task,
    pick_model_tier,
)


def test_estimate_for_classification_returns_cheap_tier():
    est = estimate_for_task("classification")
    assert est.model_tier == ModelTier.cheap_for_classification
    assert est.estimated_usd > 0
    assert est.estimated_usd < 0.40
    assert est.max_iterations == 3
    assert est.stop_when_good_enough is True


def test_estimate_for_strategy_returns_strong_tier():
    est = estimate_for_task("strategy", expected_size="large")
    assert est.model_tier == ModelTier.strong_for_strategy
    assert est.estimated_usd > 0
    # Hard ceiling protects against runaway estimates.
    assert est.estimated_usd <= 0.40


def test_enforce_run_budget_zero_spend_is_proceed():
    budget = CostBudget()
    result = enforce_run_budget([], budget)
    assert result["action"] == "proceed"
    assert result["within_budget"] is True
    assert result["total_usd"] == 0.0
    assert result["threshold_breached"] is None


def test_enforce_run_budget_over_cap_is_hard_stop():
    budget = CostBudget(per_run_budget_usd=0.10)
    expensive = CostEstimate(
        estimated_input_tokens=10_000,
        estimated_output_tokens=3_000,
        estimated_usd=0.30,  # 300% of cap
        model_tier=ModelTier.strong_for_strategy,
    )
    result = enforce_run_budget([expensive], budget)
    assert result["action"] == "hard_stop"
    assert result["within_budget"] is False
    assert result["threshold_breached"] == "hard_stop"


def test_cost_budget_rejects_extra_fields():
    with pytest.raises(ValidationError):
        CostBudget(per_run_budget_usd=0.5, surprise="boom")  # type: ignore[call-arg]


def test_pick_model_tier_for_arabic_draft_is_balanced():
    assert pick_model_tier("draft_arabic_message") == ModelTier.balanced_for_drafts


def test_unknown_purpose_defaults_to_cheap_tier():
    # Defensive: unknown intents must NOT auto-escalate to expensive tiers.
    assert pick_model_tier("totally_unknown_intent") == ModelTier.cheap_for_classification


def test_warning_threshold_warns_or_pauses():
    budget = CostBudget(per_run_budget_usd=0.10)  # 70% = 0.07, 90% = 0.09
    mid = CostEstimate(
        estimated_input_tokens=1_000,
        estimated_output_tokens=200,
        estimated_usd=0.075,
        model_tier=ModelTier.balanced_for_drafts,
    )
    result = enforce_run_budget([mid], budget)
    assert result["within_budget"] is True
    assert result["threshold_breached"] == "warning"
    assert result["action"] in {"warn_founder", "pause_for_approval"}
