"""Strategic Product Sequence — order matters; forbidden inversions exist.

See ``docs/strategic_control/STRATEGIC_PRODUCT_SEQUENCE.md``.
"""

from __future__ import annotations

from enum import IntEnum


class ProductSequenceStep(IntEnum):
    REVENUE_INTELLIGENCE_SPRINT = 1
    DATA_READINESS_ENGINE = 2
    GOVERNANCE_RUNTIME = 3
    PROOF_PACK_GENERATOR = 4
    FOUNDER_COMMAND_CENTER = 5
    CLIENT_WORKSPACE = 6
    COMPANY_BRAIN = 7
    MONTHLY_RETAINER_ENGINE = 8
    AI_CONTROL_PLANE = 9
    PARTNER_ACADEMY_PORTAL = 10


PRODUCT_SEQUENCE: tuple[ProductSequenceStep, ...] = tuple(ProductSequenceStep)


# Steps that may not start until a named prerequisite step is in
# operation. Encodes the doctrine's forbidden inversions.
FORBIDDEN_INVERSIONS: dict[ProductSequenceStep, ProductSequenceStep] = {
    ProductSequenceStep.CLIENT_WORKSPACE: ProductSequenceStep.COMPANY_BRAIN,  # need pull
    ProductSequenceStep.PARTNER_ACADEMY_PORTAL: ProductSequenceStep.AI_CONTROL_PLANE,
    ProductSequenceStep.AI_CONTROL_PLANE: ProductSequenceStep.MONTHLY_RETAINER_ENGINE,
    ProductSequenceStep.COMPANY_BRAIN: ProductSequenceStep.PROOF_PACK_GENERATOR,
    ProductSequenceStep.MONTHLY_RETAINER_ENGINE: ProductSequenceStep.PROOF_PACK_GENERATOR,
}


def is_valid_order(
    step: ProductSequenceStep,
    *,
    completed: frozenset[ProductSequenceStep],
) -> tuple[bool, str | None]:
    """Return ``(valid, missing_step_or_None)``.

    A step is valid if every predecessor in the canonical sequence is
    completed and any forbidden-inversion prerequisite is also
    completed.
    """

    for prior in PRODUCT_SEQUENCE:
        if prior >= step:
            break
        if prior not in completed:
            return (False, prior.name)

    inversion = FORBIDDEN_INVERSIONS.get(step)
    if inversion is not None and inversion not in completed:
        return (False, inversion.name)

    return (True, None)
