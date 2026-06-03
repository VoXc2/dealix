"""Static model catalog for bookkeeping.

NO live API call ever fires from this module. The catalog records the
names and per-1K rates we *would* meter against, so estimates can be
audited offline. Rates are bounded planning numbers, not live billing.
"""
from __future__ import annotations

from auto_client_acquisition.llm_gateway_v10.schemas import ModelTier

# (tier, language) → metering descriptor.
# language "x" entries act as a generic fallback if a specific lookup misses.
_CATALOG: dict[tuple[ModelTier, str], dict[str, float | str]] = {
    (ModelTier.cheap_for_classification, "ar"): {
        "model_name": "cheap-classifier-ar",
        "input_cost_per_1k_usd": 0.0005,
        "output_cost_per_1k_usd": 0.0015,
    },
    (ModelTier.cheap_for_classification, "en"): {
        "model_name": "cheap-classifier-en",
        "input_cost_per_1k_usd": 0.0005,
        "output_cost_per_1k_usd": 0.0015,
    },
    (ModelTier.cheap_for_classification, "bilingual"): {
        "model_name": "cheap-classifier-bi",
        "input_cost_per_1k_usd": 0.0006,
        "output_cost_per_1k_usd": 0.0018,
    },
    (ModelTier.balanced_for_drafts, "ar"): {
        "model_name": "balanced-drafter-ar",
        "input_cost_per_1k_usd": 0.003,
        "output_cost_per_1k_usd": 0.012,
    },
    (ModelTier.balanced_for_drafts, "en"): {
        "model_name": "balanced-drafter-en",
        "input_cost_per_1k_usd": 0.003,
        "output_cost_per_1k_usd": 0.012,
    },
    (ModelTier.balanced_for_drafts, "bilingual"): {
        "model_name": "balanced-drafter-bi",
        "input_cost_per_1k_usd": 0.0035,
        "output_cost_per_1k_usd": 0.014,
    },
    (ModelTier.strong_for_strategy, "ar"): {
        "model_name": "strong-strategist-ar",
        "input_cost_per_1k_usd": 0.015,
        "output_cost_per_1k_usd": 0.060,
    },
    (ModelTier.strong_for_strategy, "en"): {
        "model_name": "strong-strategist-en",
        "input_cost_per_1k_usd": 0.015,
        "output_cost_per_1k_usd": 0.060,
    },
    (ModelTier.strong_for_strategy, "bilingual"): {
        "model_name": "strong-strategist-bi",
        "input_cost_per_1k_usd": 0.018,
        "output_cost_per_1k_usd": 0.072,
    },
    (ModelTier.local_no_model, "ar"): {
        "model_name": "local-deterministic",
        "input_cost_per_1k_usd": 0.0,
        "output_cost_per_1k_usd": 0.0,
    },
    (ModelTier.local_no_model, "en"): {
        "model_name": "local-deterministic",
        "input_cost_per_1k_usd": 0.0,
        "output_cost_per_1k_usd": 0.0,
    },
    (ModelTier.local_no_model, "bilingual"): {
        "model_name": "local-deterministic",
        "input_cost_per_1k_usd": 0.0,
        "output_cost_per_1k_usd": 0.0,
    },
}


def lookup_model(tier: ModelTier, language: str) -> dict[str, float | str]:
    """Return the catalog entry for ``(tier, language)``.

    Defensive: missing combinations fall back to the English entry,
    then to a zero-cost local entry, never raising.
    """
    try:
        if (tier, language) in _CATALOG:
            return dict(_CATALOG[(tier, language)])
        if (tier, "en") in _CATALOG:
            return dict(_CATALOG[(tier, "en")])
        return {
            "model_name": "local-deterministic",
            "input_cost_per_1k_usd": 0.0,
            "output_cost_per_1k_usd": 0.0,
        }
    except Exception:
        return {
            "model_name": "local-deterministic",
            "input_cost_per_1k_usd": 0.0,
            "output_cost_per_1k_usd": 0.0,
        }
