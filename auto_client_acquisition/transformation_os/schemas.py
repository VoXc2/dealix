"""Schemas for the 5-stage Transformation System.

Dealix sells transformation, not tools. A transformation engagement
moves a client through 5 governed stages, each tied to a rung of the
offer ladder, and each transition gated by verified evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class TransformationStage(StrEnum):
    """The 5 stages of an AI transformation engagement."""

    ASSESSMENT = "assessment"
    PILOT = "pilot"
    WORKFLOW_REDESIGN = "workflow_redesign"
    OPERATIONAL_DEPLOYMENT = "operational_deployment"
    GOVERNANCE_SCALE = "governance_scale"


# Each stage maps to a rung of the service_catalog offer ladder.
STAGE_TO_OFFER: dict[TransformationStage, str] = {
    TransformationStage.ASSESSMENT: "free_mini_diagnostic",
    TransformationStage.PILOT: "revenue_proof_sprint_499",
    TransformationStage.WORKFLOW_REDESIGN: "data_to_revenue_pack_1500",
    TransformationStage.OPERATIONAL_DEPLOYMENT: "growth_ops_monthly_2999",
    TransformationStage.GOVERNANCE_SCALE: "executive_command_center_7500",
}


@dataclass(frozen=True, slots=True)
class StageEvidence:
    """Evidence that the work of one stage actually happened."""

    evidence_id: str
    stage: str
    kind: str
    ref: str
    verified: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "evidence_id": self.evidence_id,
            "stage": self.stage,
            "kind": self.kind,
            "ref": self.ref,
            "verified": self.verified,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> StageEvidence:
        return cls(
            evidence_id=str(data["evidence_id"]),
            stage=str(data["stage"]),
            kind=str(data["kind"]),
            ref=str(data.get("ref", "")),
            verified=bool(data["verified"]),
        )


@dataclass(frozen=True, slots=True)
class TransformationRecord:
    """The state of one client's transformation engagement."""

    engagement_id: str
    client_id: str
    current_stage: str = TransformationStage.ASSESSMENT.value
    completed_stages: tuple[str, ...] = field(default_factory=tuple)
    evidence: tuple[StageEvidence, ...] = field(default_factory=tuple)

    def offer_for_current_stage(self) -> str:
        """The offer-ladder rung that matches the current stage."""
        return STAGE_TO_OFFER[TransformationStage(self.current_stage)]

    def to_dict(self) -> dict[str, object]:
        return {
            "engagement_id": self.engagement_id,
            "client_id": self.client_id,
            "current_stage": self.current_stage,
            "current_offer": self.offer_for_current_stage(),
            "completed_stages": list(self.completed_stages),
            "evidence": [e.to_dict() for e in self.evidence],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> TransformationRecord:
        raw_evidence = data.get("evidence", []) or []
        return cls(
            engagement_id=str(data["engagement_id"]),
            client_id=str(data["client_id"]),
            current_stage=str(data.get("current_stage", TransformationStage.ASSESSMENT.value)),
            completed_stages=tuple(str(s) for s in data.get("completed_stages", []) or []),
            evidence=tuple(StageEvidence.from_dict(e) for e in raw_evidence),
        )
