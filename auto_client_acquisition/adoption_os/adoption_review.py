"""Adoption review — post-sprint outcomes and onboarding phases."""

from __future__ import annotations

from enum import StrEnum

ONBOARDING_PHASES: tuple[str, ...] = (
    "kickoff",
    "capability_diagnostic",
    "source_passport_setup",
    "data_readiness_review",
    "workflow_owner_assignment",
    "governance_boundary",
    "first_sprint",
    "proof_pack",
    "adoption_review",
    "retainer_decision",
)


class AdoptionOutcome(StrEnum):
    ADOPTED = "adopted"
    PARTIALLY_ADOPTED = "partially_adopted"
    BLOCKED = "blocked"
    NOT_ADOPTED = "not_adopted"


ADOPTION_REVIEW_SIGNALS: tuple[str, ...] = (
    "outputs_used",
    "who_used_outputs",
    "approvals_completed",
    "returned_to_system",
    "value_visible",
    "monthly_workflow_exists",
    "adoption_blockers",
    "training_needed",
)


def adoption_review_coverage_score(signals_captured: frozenset[str]) -> int:
    if not ADOPTION_REVIEW_SIGNALS:
        return 0
    n = sum(1 for s in ADOPTION_REVIEW_SIGNALS if s in signals_captured)
    return (n * 100) // len(ADOPTION_REVIEW_SIGNALS)


def onboarding_phase_index(phase: str) -> int | None:
    try:
        return ONBOARDING_PHASES.index(phase)
    except ValueError:
        return None
