"""Dealix Intelligence — cloud cost estimation.

USD-per-1K-token rates per ModelTier, used by ``dealix_model_router`` to
enforce ``TaskRequirements.max_cost_usd_per_call`` BEFORE a cloud call is
made and to report the actual cost AFTER.

The pre-call estimate uses a realistic *expected* output length (not the
hard generation ceiling) so legitimate calls fit their caps, while a
genuinely oversized prompt still trips the gate. These are estimates, not
a billing contract — the real charge comes from the provider.
"""

from __future__ import annotations

from auto_client_acquisition.llm_gateway_v10.schemas import ModelTier

# (input_usd_per_1k_tokens, output_usd_per_1k_tokens).
_RATES: dict[ModelTier, tuple[float, float]] = {
    ModelTier.cheap_for_classification: (0.0003, 0.0010),
    ModelTier.balanced_for_drafts: (0.0025, 0.0080),
    ModelTier.strong_for_strategy: (0.0030, 0.0120),
    ModelTier.local_no_model: (0.0, 0.0),
}

# Hard generation ceiling requested from the provider (the `max_tokens` arg).
_MAX_OUTPUT_TOKENS: dict[ModelTier, int] = {
    ModelTier.cheap_for_classification: 384,
    ModelTier.balanced_for_drafts: 900,
    ModelTier.strong_for_strategy: 1200,
    ModelTier.local_no_model: 0,
}

# Realistic expected output length for the pre-call cost estimate.
_EXPECTED_OUTPUT_TOKENS: dict[ModelTier, int] = {
    ModelTier.cheap_for_classification: 120,
    ModelTier.balanced_for_drafts: 350,
    ModelTier.strong_for_strategy: 500,
    ModelTier.local_no_model: 0,
}


def estimate_tokens(text: str) -> int:
    """Rough token count — ~4 chars per token (ASCII + Arabic average)."""
    return max(1, len(text) // 4)


def max_output_tokens(tier: ModelTier) -> int:
    """Per-tier hard generation ceiling to request from the cloud router."""
    return _MAX_OUTPUT_TOKENS.get(tier, 900)


def estimate_cost_usd(tier: ModelTier, input_tokens: int, output_tokens: int) -> float:
    """USD cost for a call given token counts. Used for the post-call report."""
    in_rate, out_rate = _RATES.get(tier, _RATES[ModelTier.strong_for_strategy])
    return round((input_tokens / 1000.0) * in_rate + (output_tokens / 1000.0) * out_rate, 6)


def estimate_call_cost_usd(tier: ModelTier, prompt: str) -> float:
    """Pre-call cost estimate from a prompt, using a realistic expected output.

    A normal-sized prompt fits comfortably under its task cap; an oversized
    prompt drives the input term up and trips the cost gate.
    """
    expected_output = _EXPECTED_OUTPUT_TOKENS.get(tier, 350)
    return estimate_cost_usd(
        tier,
        input_tokens=estimate_tokens(prompt),
        output_tokens=expected_output,
    )


__all__ = [
    "estimate_call_cost_usd",
    "estimate_cost_usd",
    "estimate_tokens",
    "max_output_tokens",
]
