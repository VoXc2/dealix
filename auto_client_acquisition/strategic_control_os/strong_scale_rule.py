"""Strong Scale Rule — six conditions must hold simultaneously.

See ``docs/strategic_control/STRONG_SCALE_RULE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StrongScaleCondition(str, Enum):
    PROOF = "proof"
    REPEATABILITY = "repeatability"
    MARGIN = "margin"
    GOVERNANCE = "governance"
    DEMAND = "demand"
    OWNER = "owner"


STRONG_SCALE_CONDITIONS: tuple[StrongScaleCondition, ...] = tuple(StrongScaleCondition)


@dataclass(frozen=True)
class StrongScaleEvidence:
    candidate: str
    proof_strong: bool
    delivery_is_checklist: bool
    healthy_margin: bool
    governance_active: bool
    repeat_demand: bool
    named_owner: bool


@dataclass(frozen=True)
class StrongScaleAssessment:
    allow_scale: bool
    missing_conditions: tuple[StrongScaleCondition, ...]
    recommended_moves: tuple[str, ...]


_RECOMMENDED_MOVES: tuple[str, ...] = (
    "raise_price",
    "build_product_module",
    "author_playbook",
    "offer_recurring_retainer",
    "recruit_partner",
)


def evaluate_strong_scale(evidence: StrongScaleEvidence) -> StrongScaleAssessment:
    missing: list[StrongScaleCondition] = []
    if not evidence.proof_strong:
        missing.append(StrongScaleCondition.PROOF)
    if not evidence.delivery_is_checklist:
        missing.append(StrongScaleCondition.REPEATABILITY)
    if not evidence.healthy_margin:
        missing.append(StrongScaleCondition.MARGIN)
    if not evidence.governance_active:
        missing.append(StrongScaleCondition.GOVERNANCE)
    if not evidence.repeat_demand:
        missing.append(StrongScaleCondition.DEMAND)
    if not evidence.named_owner:
        missing.append(StrongScaleCondition.OWNER)

    return StrongScaleAssessment(
        allow_scale=not missing,
        missing_conditions=tuple(missing),
        recommended_moves=_RECOMMENDED_MOVES if not missing else (),
    )
