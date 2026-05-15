"""Service-ladder wiring — maps the Enterprise Maturity Index to the offer ladder.

ربط سلّم الخدمات — يحوّل مؤشر نضج المؤسسة إلى مستوى ودرجة العرض المناسبة.

Reuses ``client_maturity_os.offer_matrix`` so a maturity index recommends the
right rung of the commercial service ladder.
"""

from __future__ import annotations

from auto_client_acquisition.client_maturity_os.offer_matrix import (
    blocked_offers_for_level,
    primary_offer_for_level,
)

# Thresholds mirror ``maturity_engine._infer_maturity_level`` score bands.
# This mapping deliberately omits the gate logic (retainer eligibility, level-7
# entry gates) — those depend on inputs the maturity index alone cannot carry,
# so the API note instructs callers to verify eligibility gates before offering.
_LADDER_THRESHOLDS: tuple[tuple[float, int], ...] = (
    (35.0, 0),
    (48.0, 1),
    (58.0, 2),
    (68.0, 3),
    (78.0, 4),
    (86.0, 5),
    (93.0, 6),
)


def emi_to_ladder_level(emi: float) -> int:
    """Map an Enterprise Maturity Index (0–100) to a ladder level (0–7)."""
    for threshold, level in _LADDER_THRESHOLDS:
        if emi < threshold:
            return level
    return 7


def enterprise_offer_recommendation(emi: float) -> dict:
    """Recommend the next offer (and blocked offers) for a maturity index."""
    level = emi_to_ladder_level(emi)
    return {
        "ladder_level": level,
        "recommended_offer": primary_offer_for_level(level),
        "blocked_offers": sorted(blocked_offers_for_level(level)),
        "note_ar": "التوصية مبنية على مؤشر النضج فقط؛ تحقَّق من بوابات الأهلية قبل العرض.",
        "note_en": (
            "Recommendation reflects the maturity index only; "
            "verify eligibility gates before offering."
        ),
    }


__all__ = ["emi_to_ladder_level", "enterprise_offer_recommendation"]
