"""Case-safe anonymized proof summaries for external use."""

from __future__ import annotations


def case_safe_public_summary_ok(
    *,
    mentions_client_name: bool,
    includes_confidential_metrics: bool,
    includes_sector_pattern: bool,
    includes_work_performed_summary: bool,
) -> tuple[bool, tuple[str, ...]]:
    errs: list[str] = []
    if mentions_client_name:
        errs.append("remove_client_name_without_consent")
    if includes_confidential_metrics:
        errs.append("anonymize_or_aggregate_metrics")
    if not includes_sector_pattern:
        errs.append("sector_or_problem_pattern_required")
    if not includes_work_performed_summary:
        errs.append("work_performed_summary_required")
    return not errs, tuple(errs)
