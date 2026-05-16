"""Freshness scoring for retrieval governance."""

from __future__ import annotations


def compute_freshness_score(*, now_epoch: int, created_at_epoch: int, ttl_seconds: int) -> float:
    if ttl_seconds <= 0:
        return 0.0
    age = max(0, now_epoch - created_at_epoch)
    score = 1.0 - (age / ttl_seconds)
    return round(max(0.0, min(1.0, score)), 4)


def is_stale(*, freshness_score: float, min_threshold: float = 0.35) -> bool:
    return freshness_score < min_threshold


__all__ = ['compute_freshness_score', 'is_stale']
