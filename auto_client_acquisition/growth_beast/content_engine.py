"""Safe content angle — draft only."""
from __future__ import annotations

from typing import Any


def suggest_content_angle(segment_label_ar: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "linkedin_post_hook_ar": (
            f"لماذا {segment_label_ar} تحتاج تشخيصاً قبل أي عرض — بدون وعود زائفة"
        ),
        "action_mode": "approval_required",
        "blocked_channels": ["cold_whatsapp", "linkedin_automation", "mass_dm"],
    }
