"""Proof-to-Retainer Gate — Continue / Expand / Pause decisions.

See ``docs/operating_manual/PROOF_TO_RETAINER_SYSTEM.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RetainerMotion(str, Enum):
    CONTINUE = "continue"
    EXPAND = "expand"
    PAUSE = "pause"


# Doctrine thresholds for the retainer gate.
RETAINER_GATE_THRESHOLDS: dict[str, float] = {
    "proof_score_min": 80.0,
    "client_health_min": 70.0,
}


@dataclass(frozen=True)
class RetainerGateInputs:
    engagement_id: str
    proof_score: float                 # 0..100
    client_health: float               # 0..100
    workflow_is_recurring: bool
    monthly_value_clear: bool
    stakeholder_engaged: bool
    strongest_proof_type: str          # one of: revenue, knowledge, risk, time, quality
    adjacent_capability_signal: bool = False  # True triggers Expand instead of Continue


_PROOF_TYPE_TO_RETAINER: dict[str, str] = {
    "revenue": "Monthly RevOps OS",
    "knowledge": "Monthly Company Brain",
    "risk": "Monthly Governance",
    "time": "Monthly AI Ops",
    "quality": "Monthly AI Ops",
}


@dataclass(frozen=True)
class RetainerGateResult:
    motion: RetainerMotion
    retainer_offer: str | None
    reasons: tuple[str, ...]


def evaluate_retainer_gate(inputs: RetainerGateInputs) -> RetainerGateResult:
    reasons: list[str] = []

    gate_open = True
    if inputs.proof_score < RETAINER_GATE_THRESHOLDS["proof_score_min"]:
        gate_open = False
        reasons.append("proof_score_below_threshold")
    if inputs.client_health < RETAINER_GATE_THRESHOLDS["client_health_min"]:
        gate_open = False
        reasons.append("client_health_below_threshold")
    if not inputs.workflow_is_recurring:
        gate_open = False
        reasons.append("workflow_not_recurring")
    if not inputs.monthly_value_clear:
        gate_open = False
        reasons.append("monthly_value_unclear")
    if not inputs.stakeholder_engaged:
        gate_open = False
        reasons.append("stakeholder_not_engaged")

    if not gate_open:
        return RetainerGateResult(
            motion=RetainerMotion.PAUSE,
            retainer_offer=None,
            reasons=tuple(reasons),
        )

    retainer = _PROOF_TYPE_TO_RETAINER.get(inputs.strongest_proof_type)
    if retainer is None:
        return RetainerGateResult(
            motion=RetainerMotion.PAUSE,
            retainer_offer=None,
            reasons=("unknown_proof_type",),
        )

    motion = (
        RetainerMotion.EXPAND
        if inputs.adjacent_capability_signal
        else RetainerMotion.CONTINUE
    )
    return RetainerGateResult(
        motion=motion,
        retainer_offer=retainer,
        reasons=("retainer_gate_passed",),
    )
