"""Cost estimation helpers for agent traces."""
from __future__ import annotations


def estimate_cost(*, input_tokens: int = 0, output_tokens: int = 0,
                   model: str = "default") -> float:
    """Crude cost estimate (USD). Future: per-model rate cards."""
    # Rough Claude / GPT-4 averages — directional only
    rates = {
        "claude-sonnet": (3.0, 15.0),    # per 1M tokens
        "claude-opus": (15.0, 75.0),
        "gpt-4o": (2.5, 10.0),
        "gpt-4o-mini": (0.15, 0.60),
        "default": (1.0, 3.0),
    }
    in_rate, out_rate = rates.get(model, rates["default"])
    return round(
        (input_tokens * in_rate + output_tokens * out_rate) / 1_000_000, 6
    )
