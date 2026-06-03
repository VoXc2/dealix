"""Market language coverage score for empire layer copy checks."""

from __future__ import annotations

from auto_client_acquisition.category_os.language_adoption import preferred_term_hits


def market_language_coverage_score(text: str) -> int:
    """Map preferred-term hits to a 0-100 score (rough heuristic)."""
    hits = preferred_term_hits(text)
    return min(100, hits * 12)
