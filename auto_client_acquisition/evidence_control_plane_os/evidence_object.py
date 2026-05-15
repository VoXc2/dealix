"""Evidence object — canonical fields for auditable artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EvidenceType(StrEnum):
    SOURCE = "source"
    AI_RUN = "ai_run"
    POLICY_CHECK = "policy_check"
    GOVERNANCE_DECISION = "governance_decision"
    HUMAN_REVIEW = "human_review"
    APPROVAL = "approval"
    OUTPUT = "output"
    PROOF = "proof"
    VALUE = "value"
    RISK = "risk"
    DECISION = "decision"


@dataclass(frozen=True, slots=True)
class EvidenceObject:
    evidence_id: str
    evidence_type: str
    client_id: str
    project_id: str
    actor_type: str
    actor_id: str
    human_owner: str
    source_ids: tuple[str, ...]
    linked_artifacts: tuple[str, ...]
    summary: str
    confidence: str
    timestamp_iso: str
    tenant_id: str = "default"
    """Tenant scope for isolation. ``"default"`` in dev/test; production
    callers pass a real tenant id."""
    run_id: str = ""
    """Optional workflow-run correlation — ties this evidence into a
    single run trace in the Control Plane."""


def evidence_object_valid(obj: EvidenceObject) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not obj.evidence_id.strip():
        errors.append("evidence_id_required")
    if not obj.evidence_type.strip():
        errors.append("evidence_type_required")
    if not obj.client_id.strip():
        errors.append("client_id_required")
    if not obj.tenant_id.strip():
        errors.append("tenant_id_required")
    if not obj.summary.strip():
        errors.append("summary_required")
    if not obj.timestamp_iso.strip():
        errors.append("timestamp_required")
    return not errors, tuple(errors)


def is_critical_evidence_type(evidence_type: str) -> bool:
    return evidence_type in (
        EvidenceType.GOVERNANCE_DECISION,
        EvidenceType.APPROVAL,
        EvidenceType.AI_RUN,
        EvidenceType.OUTPUT,
    )
