"""Track category language health in outbound copy (Market Power layer)."""

from __future__ import annotations

from auto_client_acquisition.category_os.language_adoption import (
    avoided_term_hits,
    preferred_term_hits,
)


def market_language_health_score(text: str) -> int:
    """Heuristic 0-100: preferred phrases raise score, avoided phrases lower it."""
    p = preferred_term_hits(text)
    a = avoided_term_hits(text)
    raw = 55 + p * 8 - a * 12
    return max(0, min(100, raw))
