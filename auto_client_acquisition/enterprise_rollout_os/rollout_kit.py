"""Enterprise rollout kit — artifacts for trust and cadence."""

from __future__ import annotations

ROLLOUT_KIT_ITEMS: tuple[str, ...] = (
    "executive_brief",
    "capability_diagnostic",
    "data_request_template",
    "source_passport_form",
    "governance_boundary_document",
    "workflow_owner_guide",
    "approval_matrix",
    "proof_pack_template",
    "monthly_value_report_template",
    "adoption_review_template",
    "incident_response_guide",
    "what_dealix_refuses_to_build",
)


def rollout_kit_coverage_score(items_delivered: frozenset[str]) -> int:
    if not ROLLOUT_KIT_ITEMS:
        return 0
    n = sum(1 for i in ROLLOUT_KIT_ITEMS if i in items_delivered)
    return (n * 100) // len(ROLLOUT_KIT_ITEMS)
