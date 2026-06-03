"""Budget discipline by operating stage."""

from __future__ import annotations

from enum import IntEnum


class OperatingBudgetStage(IntEnum):
    FOUNDER_PROOF = 1
    REPEATABLE_SPRINT = 2
    RETAINER_ENGINE = 3
    ENTERPRISE_TRUST = 4
    ECOSYSTEM = 5
    VENTURE_FACTORY = 6


# Categories from docs — whether spend is encouraged at this stage
_STAGE_ALLOWED: dict[int, frozenset[str]] = {
    1: frozenset(
        {
            "revenue_capture",
            "delivery_efficiency_light",
            "governance_basic",
            "proof_basic",
        },
    ),
    2: frozenset(
        {
            "revenue_capture",
            "delivery_efficiency",
            "proof_value",
            "productization_early",
            "governance_basic",
        },
    ),
    3: frozenset(
        {
            "delivery_efficiency",
            "productization",
            "proof_value",
            "governance_trust",
            "talent_enablement",
        },
    ),
    4: frozenset(
        {
            "governance_trust",
            "proof_value",
            "productization",
            "venture_optionality_light",
        },
    ),
    5: frozenset(
        {
            "distribution",
            "talent_enablement",
            "proof_value",
            "governance_trust",
        },
    ),
    6: frozenset(
        {
            "venture_optionality",
            "productization",
            "distribution",
            "talent_enablement",
        },
    ),
}


def spend_allowed_for_stage(stage: OperatingBudgetStage, category: str) -> bool:
    return category in _STAGE_ALLOWED.get(int(stage), frozenset())
