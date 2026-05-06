"""Roll sector-level learning from proof themes."""
from __future__ import annotations

from collections import Counter
from typing import Any


def sector_learning(themes: list[str]) -> dict[str, Any]:
    counts = Counter(themes)
    top = counts.most_common(3)
    return {
        "schema_version": 1,
        "top_themes": [{"theme": t, "count": c} for t, c in top],
        "next_targeting_hint_ar": "ركّز الرسائل على الشريحة التي تكرر فيها نفس الألم التشغيلي.",
    }
