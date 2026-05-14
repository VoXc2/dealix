"""Market authority — category ownership signals (0–100), equal-weight composite."""

from __future__ import annotations

from typing import NamedTuple


class MarketAuthorityInputs(NamedTuple):
    """Each signal 0–100 (inbound, language pull, benchmarks, academy, etc.)."""

    inbound_diagnostics: float
    partner_referrals: float
    repeated_language: float
    content_conversations: float
    benchmark_requests: float
    academy_interest: float


def compute_market_authority_score(inputs: MarketAuthorityInputs) -> float:
    vals = tuple(inputs)
    return max(0.0, min(100.0, float(sum(vals) / len(vals))))
