"""Pick best offer hint from ranked segments + pilot tier."""
from __future__ import annotations

from typing import Any


def best_offer_hint(top_segment: dict[str, Any] | None) -> dict[str, Any]:
    label = (
        (top_segment or {}).get("label_ar")
        or (top_segment or {}).get("segment_name_ar")
        or "pilot_499"
    )
    return {
        "schema_version": 1,
        "offer_key": "pilot_499_sar",
        "segment_hint_ar": str(label),
        "action_mode": "draft_only",
        "no_guarantee": True,
    }
