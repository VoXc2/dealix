"""Evidence Object — canonical evidence record across the system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class EvidenceType(str, Enum):
    SOURCE = "source_evidence"
    INPUT = "input_evidence"
    POLICY = "policy_evidence"
    AI_RUN = "ai_run_evidence"
    HUMAN_REVIEW = "human_review_evidence"
    APPROVAL = "approval_evidence"
    OUTPUT = "output_evidence"
    PROOF = "proof_evidence"
    VALUE = "value_evidence"
    RISK = "risk_evidence"
    DECISION = "decision_evidence"


@dataclass(frozen=True)
class EvidenceObject:
    evidence_id: str
    evidence_type: EvidenceType
    client_id: str
    project_id: str
    actor_type: str
    actor_id: str
    human_owner: str
    source_ids: tuple[str, ...]
    linked_artifacts: tuple[str, ...]
    summary: str
    confidence: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.evidence_id:
            raise ValueError("evidence_id_required")
        if not self.human_owner:
            raise ValueError("human_owner_required")
        if not self.summary:
            raise ValueError("summary_required")
        if self.confidence not in {"low", "medium", "high"}:
            raise ValueError("confidence_must_be_low_medium_or_high")
