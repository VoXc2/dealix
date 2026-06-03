"""Evidence gap detection — operational rules from docs/evidence_control_plane."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class GapSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class EvidencePresence:
    has_source_passport: bool
    has_governance_decision_on_output: bool
    has_approval_for_external: bool
    has_proof_for_claim: bool
    has_human_review: bool
    has_agent_auditability_card: bool
    has_value_event_for_retainer: bool


def detect_evidence_gaps(presence: EvidencePresence) -> tuple[str, ...]:
    gaps: list[str] = []
    if not presence.has_source_passport:
        gaps.append("source_passport_missing")
    if not presence.has_governance_decision_on_output:
        gaps.append("governance_decision_missing")
    if not presence.has_approval_for_external:
        gaps.append("approval_missing_external")
    if not presence.has_proof_for_claim:
        gaps.append("proof_missing_claim")
    if not presence.has_human_review:
        gaps.append("human_review_missing")
    if not presence.has_agent_auditability_card:
        gaps.append("agent_auditability_missing")
    if not presence.has_value_event_for_retainer:
        gaps.append("value_event_missing_retainer")
    return tuple(gaps)


def gap_severity(gap: str) -> GapSeverity:
    if gap in ("approval_missing_external",):
        return GapSeverity.CRITICAL
    if gap in ("source_passport_missing", "governance_decision_missing"):
        return GapSeverity.HIGH
    if gap in ("proof_missing_claim", "human_review_missing", "agent_auditability_missing"):
        return GapSeverity.MEDIUM
    if gap == "value_event_missing_retainer":
        return GapSeverity.LOW
    return GapSeverity.MEDIUM
