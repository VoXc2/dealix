"""Proof Economy — Proof Pack shape and proof-to-retainer protocol.

See ``docs/endgame/PROOF_ECONOMY.md``. Pairs with
``auto_client_acquisition.proof_engine.evidence`` for evidence levels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from auto_client_acquisition.proof_engine.evidence import EvidenceLevel


class ProofType(str, Enum):
    REVENUE = "revenue"
    TIME = "time"
    QUALITY = "quality"
    RISK = "risk"
    KNOWLEDGE = "knowledge"


class ProofToRetainerMotion(str, Enum):
    CONTINUE = "continue"
    EXPAND = "expand"
    PAUSE = "pause"


@dataclass(frozen=True)
class ProofPack:
    engagement_id: str
    problem: str
    inputs: tuple[str, ...]
    work_completed: tuple[str, ...]
    metrics: dict[str, float]
    before_after: dict[str, tuple[float, float]]
    ai_outputs: tuple[str, ...]
    governance_events: tuple[str, ...]
    business_value: str
    risks: tuple[str, ...]
    recommended_next_step: ProofToRetainerMotion
    proof_types: tuple[ProofType, ...]
    evidence_level: EvidenceLevel = EvidenceLevel.L3_CUSTOMER_APPROVED
    consent_public: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.proof_types:
            raise ValueError("proof_types_required")
        if self.evidence_level >= EvidenceLevel.L4_PUBLIC_APPROVED and not self.consent_public:
            raise ValueError("public_evidence_requires_consent")


# Proof type → recommended Monthly retainer. Encodes the doctrine map
# from `PROOF_ECONOMY.md` § 3.
RETAINER_BY_PROOF_TYPE: dict[ProofType, str] = {
    ProofType.REVENUE: "Monthly RevOps OS",
    ProofType.KNOWLEDGE: "Monthly Company Brain",
    ProofType.RISK: "Monthly Governance",
    ProofType.TIME: "Monthly AI Ops",
    ProofType.QUALITY: "Monthly AI Ops",
}


def recommended_retainer(pack: ProofPack) -> str | None:
    """Return the retainer that best fits the pack's strongest proof type.

    The "strongest" type is the first listed in ``proof_types``; producers
    are expected to order them by strength. Returns ``None`` if the
    motion is ``PAUSE``.
    """

    if pack.recommended_next_step is ProofToRetainerMotion.PAUSE:
        return None
    if not pack.proof_types:
        return None
    return RETAINER_BY_PROOF_TYPE[pack.proof_types[0]]
