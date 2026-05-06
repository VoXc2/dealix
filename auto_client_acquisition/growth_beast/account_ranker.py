"""Rank synthetic accounts from target segments (deterministic)."""
from __future__ import annotations

from typing import Any


def rank_accounts(segments: list[dict[str, Any]], *, limit: int = 10) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    for i, seg in enumerate(sorted(segments, key=lambda s: -int(s.get("fit_score") or 0))):
        ranked.append(
            {
                "rank": i + 1,
                "label_ar": seg.get("segment_name_ar") or seg.get("segment_name_en") or "unknown",
                "fit_score": int(seg.get("fit_score") or 0),
                "safe_route": seg.get("recommended_route") or "warm_intro_or_partner",
            }
        )
    return ranked[:limit]
