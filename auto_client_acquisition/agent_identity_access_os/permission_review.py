"""Permission review cadence markers (documentation-first)."""

from __future__ import annotations

PERMISSION_REVIEW_SIGNALS: tuple[str, ...] = (
    "quarterly_tool_matrix_reviewed",
    "owner_attestation_signed",
    "deny_list_updated",
)


def permission_review_coverage_score(tracked: frozenset[str]) -> int:
    if not PERMISSION_REVIEW_SIGNALS:
        return 0
    n = sum(1 for s in PERMISSION_REVIEW_SIGNALS if s in tracked)
    return (n * 100) // len(PERMISSION_REVIEW_SIGNALS)


__all__ = ["PERMISSION_REVIEW_SIGNALS", "permission_review_coverage_score"]
