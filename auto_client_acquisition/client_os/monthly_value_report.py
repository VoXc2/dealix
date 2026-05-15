"""Monthly value report — eight canonical sections for client cadence."""

from __future__ import annotations

from collections.abc import Mapping

MONTHLY_VALUE_REPORT_SECTIONS: tuple[str, ...] = (
    "what_was_done",
    "what_changed",
    "value_observed",
    "value_estimated",
    "risks_blocked",
    "needs_approval",
    "capability_improved",
    "next_step_recommendation",
)


def monthly_value_report_sections_complete(
    content_by_section: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [
        k
        for k in MONTHLY_VALUE_REPORT_SECTIONS
        if not (content_by_section.get(k) or "").strip()
    ]
    return not missing, tuple(missing)


def build_empty_monthly_value_report() -> dict[str, str]:
    return {k: "" for k in MONTHLY_VALUE_REPORT_SECTIONS}


def monthly_value_report_from_sprint_kpis(
    *,
    accounts_imported: int,
    duplicates_found: int,
    top_ranked: int,
    drafts_generated: int,
    governance_blocks: int,
) -> dict[str, str]:
    """Deterministic starter text — human must still finalize before client send."""
    r = build_empty_monthly_value_report()
    r["what_was_done"] = (
        f"Import + quality pass: {accounts_imported} accounts; "
        f"{duplicates_found} duplicate hints; {top_ranked} priority rows surfaced."
    )
    r["what_changed"] = "Ranked opportunities and draft-only outreach assets prepared."
    r["value_observed"] = (
        f"Observed: {drafts_generated} governed drafts generated; "
        f"{governance_blocks} unsafe outbound patterns blocked at doctrine/runtime."
    )
    r["value_estimated"] = "Estimated upside requires client confirmation — not used as public claim."
    r["risks_blocked"] = "Cold WhatsApp automation, LinkedIn automation, scraping, and bulk auto-send remain blocked."
    r["needs_approval"] = "All external sends require explicit human approval in Dealix posture."
    r["capability_improved"] = "Data readiness + governance checkpoints exercised on live client data."
    r["next_step_recommendation"] = "Review drafts, approve sends manually, then refresh Proof Pack for retainer gate."
    return r


__all__ = [
    "MONTHLY_VALUE_REPORT_SECTIONS",
    "build_empty_monthly_value_report",
    "monthly_value_report_from_sprint_kpis",
    "monthly_value_report_sections_complete",
]
