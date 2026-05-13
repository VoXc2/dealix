"""Evidence Gap Rules — gap → decision."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceGap(str, Enum):
    SOURCE_GAP = "source_gap"
    POLICY_GAP = "policy_gap"
    APPROVAL_GAP = "approval_gap"
    PROOF_GAP = "proof_gap"
    VALUE_GAP = "value_gap"
    AGENT_GAP = "agent_gap"


@dataclass(frozen=True)
class EvidenceGapDecision:
    gap: EvidenceGap
    decision: str
    severity: str  # low | medium | high | critical


_GAP_DECISIONS: dict[EvidenceGap, EvidenceGapDecision] = {
    EvidenceGap.SOURCE_GAP: EvidenceGapDecision(
        EvidenceGap.SOURCE_GAP, "block_ai_use", "high"
    ),
    EvidenceGap.POLICY_GAP: EvidenceGapDecision(
        EvidenceGap.POLICY_GAP, "block_client_delivery", "high"
    ),
    EvidenceGap.APPROVAL_GAP: EvidenceGapDecision(
        EvidenceGap.APPROVAL_GAP, "incident_review", "critical"
    ),
    EvidenceGap.PROOF_GAP: EvidenceGapDecision(
        EvidenceGap.PROOF_GAP, "remove_claim", "medium"
    ),
    EvidenceGap.VALUE_GAP: EvidenceGapDecision(
        EvidenceGap.VALUE_GAP, "no_retainer_push", "medium"
    ),
    EvidenceGap.AGENT_GAP: EvidenceGapDecision(
        EvidenceGap.AGENT_GAP, "no_production_use", "high"
    ),
}


def evaluate_evidence_gap(gap: EvidenceGap) -> EvidenceGapDecision:
    return _GAP_DECISIONS[gap]
