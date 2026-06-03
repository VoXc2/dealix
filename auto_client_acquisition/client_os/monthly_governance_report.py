"""Monthly governance report — cadence sections for enterprise clients."""

from __future__ import annotations

from collections.abc import Mapping

MONTHLY_GOVERNANCE_REPORT_SECTIONS: tuple[str, ...] = (
    "policy_changes",
    "approval_stats",
    "blocked_actions",
    "pii_and_external_paths",
    "incidents_or_near_misses",
    "training_and_enablement",
    "next_month_controls",
)


def monthly_governance_report_sections_complete(
    content_by_section: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in MONTHLY_GOVERNANCE_REPORT_SECTIONS if not (content_by_section.get(k) or "").strip()]
    return not missing, tuple(missing)


def build_empty_monthly_governance_report() -> dict[str, str]:
    return dict.fromkeys(MONTHLY_GOVERNANCE_REPORT_SECTIONS, "")


__all__ = [
    "MONTHLY_GOVERNANCE_REPORT_SECTIONS",
    "build_empty_monthly_governance_report",
    "monthly_governance_report_sections_complete",
]
