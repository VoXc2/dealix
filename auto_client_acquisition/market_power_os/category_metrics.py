"""Category language metrics (inbound signals)."""

from __future__ import annotations

CATEGORY_PHRASES: frozenset[str] = frozenset({"proof pack", "governed ai operations", "source passport"})


def category_hit_count(text: str) -> int:
    low = text.lower()
    return sum(1 for p in CATEGORY_PHRASES if p in low)


__all__ = ["CATEGORY_PHRASES", "category_hit_count"]
