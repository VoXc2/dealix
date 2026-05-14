"""Privacy runtime board — operational privacy signals for leadership."""

from __future__ import annotations

from collections.abc import Mapping

PRIVACY_RUNTIME_BOARD_SIGNALS: tuple[str, ...] = (
    "pii_detected",
    "redactions_applied",
    "policy_decisions",
    "blocked_disclosures",
    "external_use_attempts",
    "source_passports_missing",
    "approval_required",
    "approval_completed",
)


def privacy_runtime_board_checklist_passes(
    signals_reported: Mapping[str, bool],
) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in PRIVACY_RUNTIME_BOARD_SIGNALS if not signals_reported.get(k)]
    return not missing, tuple(missing)
