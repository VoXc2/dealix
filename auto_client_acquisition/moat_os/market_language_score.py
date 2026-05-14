"""Market language adoption slice for moat scoring — reuses empire heuristic."""

from __future__ import annotations

from auto_client_acquisition.operating_empire_os.market_language_score import (
    market_language_coverage_score,
)


def moat_market_language_adoption_score(text_sample: str) -> int:
    """0–100 adoption proxy from copy/signals text (preferred Dealix terms)."""
    return market_language_coverage_score(text_sample)
