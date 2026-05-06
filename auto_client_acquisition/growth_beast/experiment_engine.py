"""One weekly experiment suggestion from top segment."""
from __future__ import annotations

from typing import Any


def suggest_experiment(segment_label_ar: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "hypothesis_ar": f"إذا ركزنا رسائل المتابعة على {segment_label_ar} سنرفع الردود-qualified",
        "metric": "qualified_replies",
        "action_mode": "approval_required",
    }
