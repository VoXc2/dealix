"""Core operating chain — Signal → … → Holding Company.

Encodes the sacred sequence from the Endgame doctrine and provides a
``validate_transition`` helper that the Intelligence OS uses to reject
forbidden jumps.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class ChainStage(IntEnum):
    SIGNAL = 0
    CAPABILITY_DIAGNOSTIC = 1
    PRODUCTIZED_SPRINT = 2
    GOVERNED_DELIVERY = 3
    QA = 4
    PROOF_PACK = 5
    RETAINER = 6
    CAPITAL_ASSET = 7
    PRODUCT_MODULE = 8
    BUSINESS_UNIT = 9
    STANDARD = 10
    ACADEMY_OR_PARTNER = 11
    VENTURE = 12
    HOLDING_COMPANY = 13


OPERATING_CHAIN: tuple[ChainStage, ...] = tuple(ChainStage)


# Stages whose owners are explicitly named in the doctrine.
STAGE_OWNERS: dict[ChainStage, str] = {
    ChainStage.SIGNAL: "Revenue",
    ChainStage.CAPABILITY_DIAGNOSTIC: "Revenue + Senior Operator",
    ChainStage.PRODUCTIZED_SPRINT: "BU Delivery Lead",
    ChainStage.GOVERNED_DELIVERY: "Delivery + Governance Runtime",
    ChainStage.QA: "Independent QA",
    ChainStage.PROOF_PACK: "Reporting OS",
    ChainStage.RETAINER: "Revenue",
    ChainStage.CAPITAL_ASSET: "Capital OS",
    ChainStage.PRODUCT_MODULE: "Product",
    ChainStage.BUSINESS_UNIT: "BU Lead",
    ChainStage.STANDARD: "Office of the Standard",
    ChainStage.ACADEMY_OR_PARTNER: "Academy / Partner Office",
    ChainStage.VENTURE: "Venture Council",
    ChainStage.HOLDING_COMPANY: "Dealix Group",
}


# Forbidden jumps from the doctrine — each entry maps a destination stage
# to the prerequisite stage that must have closed first.
FORBIDDEN_JUMPS: dict[ChainStage, ChainStage] = {
    ChainStage.ACADEMY_OR_PARTNER: ChainStage.STANDARD,
    ChainStage.VENTURE: ChainStage.RETAINER,
    ChainStage.PRODUCT_MODULE: ChainStage.CAPITAL_ASSET,
    ChainStage.BUSINESS_UNIT: ChainStage.PRODUCT_MODULE,
}


@dataclass(frozen=True)
class ChainViolation:
    from_stage: ChainStage
    to_stage: ChainStage
    reason: str


def validate_transition(
    from_stage: ChainStage,
    to_stage: ChainStage,
    *,
    completed_stages: frozenset[ChainStage] | None = None,
) -> ChainViolation | None:
    """Return a ``ChainViolation`` if the transition violates doctrine.

    A transition is valid when:
      * the destination stage is strictly later in the chain, and
      * any forbidden-jump prerequisite is already in ``completed_stages``.

    ``completed_stages`` defaults to the empty set for callers that only
    want the ordering check.
    """

    completed = completed_stages or frozenset()

    if to_stage <= from_stage:
        return ChainViolation(
            from_stage=from_stage,
            to_stage=to_stage,
            reason="non_forward_transition",
        )

    prerequisite = FORBIDDEN_JUMPS.get(to_stage)
    if prerequisite is not None and prerequisite not in completed:
        return ChainViolation(
            from_stage=from_stage,
            to_stage=to_stage,
            reason=f"missing_prerequisite:{prerequisite.name}",
        )

    return None
