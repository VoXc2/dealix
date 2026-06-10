"""Language tracking — simple novelty signal."""

from __future__ import annotations


def language_drift_score(*, competitor_mentions: int, own_mentions: int) -> int:
    if own_mentions <= 0:
        return 0
    return min(100, round(100 * competitor_mentions / (own_mentions + 1)))


__all__ = ["language_drift_score"]
