"""next_fix — pick the single most-impactful fix from diagnose()."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.leadops_reliability.debug import diagnose


_SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def suggest_next_fix() -> dict[str, Any]:
    """Returns the single highest-priority fix to apply, or healthy state."""
    result = diagnose()
    issues = result.get("issues", [])
    if not issues:
        return {
            "next_fix_ar": "لا إصلاحات مطلوبة — LeadOps في وضع سليم.",
            "next_fix_en": "No fixes required — LeadOps is healthy.",
            "severity": "info",
            "issue_id": None,
        }
    issues_sorted = sorted(
        issues,
        key=lambda i: _SEVERITY_ORDER.get(i.get("severity", "low"), 4),
    )
    top = issues_sorted[0]
    return {
        "next_fix_ar": top.get("fix_ar", "—"),
        "next_fix_en": top.get("fix_en", "—"),
        "severity": top.get("severity", "low"),
        "issue_id": top.get("id"),
        "reason_ar": top.get("reason_ar", "—"),
        "reason_en": top.get("reason_en", "—"),
    }
