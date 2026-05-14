"""Capital review — mandatory outputs after each engagement."""

from __future__ import annotations

from collections.abc import Mapping

CAPITAL_REVIEW_OUTPUT_KEYS: tuple[str, ...] = (
    "capital_asset",
    "productization_candidate",
    "expansion_recommendation",
    "pricing_note",
    "risk_note",
)


def capital_review_outputs_complete(
    outputs_by_key: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [
        k for k in CAPITAL_REVIEW_OUTPUT_KEYS if not (outputs_by_key.get(k) or "").strip()
    ]
    return not missing, tuple(missing)
