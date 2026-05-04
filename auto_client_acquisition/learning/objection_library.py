"""
Objection Library — mines ObjectionEventRecord rows to score response variants.

Phase 3 lightweight version. Full version (with statistical confidence
intervals) lands when ≥30 objection events accumulate.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any


def mine_objections(events: list, *, min_count: int = 1) -> dict[str, Any]:
    """Group objections by class + outcome; rank response variants by win rate.

    Args:
        events: iterable of ObjectionEventRecord-like
            (.objection_class, .response_variant, .outcome)
        min_count: minimum sample size before reporting a variant
    """
    rows = list(events or [])
    by_class: dict[str, list] = defaultdict(list)
    for e in rows:
        by_class[(e.objection_class or "unknown")].append(e)

    library: list[dict[str, Any]] = []
    for objection_class, items in by_class.items():
        variant_stats: dict[str, dict[str, int]] = defaultdict(
            lambda: {"won": 0, "lost": 0, "open": 0}
        )
        for ev in items:
            variant = ev.response_variant or "no_variant"
            outcome = (ev.outcome or "open").lower()
            if outcome == "won":
                variant_stats[variant]["won"] += 1
            elif outcome == "lost":
                variant_stats[variant]["lost"] += 1
            else:
                variant_stats[variant]["open"] += 1

        ranked = []
        for variant, stats in variant_stats.items():
            total = stats["won"] + stats["lost"]
            if total < min_count:
                continue
            win_rate = (stats["won"] / total) if total else 0.0
            ranked.append({
                "variant": variant,
                "samples": stats["won"] + stats["lost"] + stats["open"],
                "won": stats["won"],
                "lost": stats["lost"],
                "win_rate": round(win_rate, 3),
            })
        ranked.sort(key=lambda x: x["win_rate"], reverse=True)
        library.append({
            "objection_class": objection_class,
            "total_samples": len(items),
            "best_variant": ranked[0]["variant"] if ranked else None,
            "ranked_variants": ranked[:5],
        })

    return {
        "objection_classes_analyzed": len(by_class),
        "total_events": len(rows),
        "library": library,
        "note_ar": (
            "نتائج موثوقة بعد ≥٣٠ حدث objection. "
            "الحالي عيّنة صغيرة — استخدم كإرشاد لا كدليل قاطع."
            if len(rows) < 30 else None
        ),
    }
