"""Revenue Pipeline — stage policy + advance rules.

Stages (canonical order):

    warm_intro_selected
    message_drafted
    founder_sent_manually
    replied
    diagnostic_requested
    diagnostic_delivered
    pilot_offered
    commitment_received       ← partial revenue truth (commitment, not cash)
    payment_received          ← REVENUE TRUTH (cash landed)
    delivery_started
    delivered
    proof_pack_delivered
    upsell_offered
    closed_won
    closed_lost
"""
from __future__ import annotations

from typing import Literal

PipelineStage = Literal[
    "warm_intro_selected",
    "message_drafted",
    "founder_sent_manually",
    "replied",
    "diagnostic_requested",
    "diagnostic_delivered",
    "pilot_offered",
    "commitment_received",
    "payment_received",
    "delivery_started",
    "delivered",
    "proof_pack_delivered",
    "upsell_offered",
    "closed_won",
    "closed_lost",
]


# Allowed forward transitions. A stage may also transition to
# ``closed_lost`` from any non-terminal stage (handled by helper below).
_FORWARD: dict[PipelineStage, set[PipelineStage]] = {
    "warm_intro_selected": {"message_drafted", "closed_lost"},
    "message_drafted": {"founder_sent_manually", "closed_lost"},
    "founder_sent_manually": {"replied", "closed_lost"},
    "replied": {"diagnostic_requested", "closed_lost"},
    "diagnostic_requested": {"diagnostic_delivered", "closed_lost"},
    "diagnostic_delivered": {"pilot_offered", "closed_lost"},
    "pilot_offered": {"commitment_received", "payment_received", "closed_lost"},
    "commitment_received": {"payment_received", "delivery_started", "closed_lost"},
    "payment_received": {"delivery_started", "closed_lost"},
    "delivery_started": {"delivered", "closed_lost"},
    "delivered": {"proof_pack_delivered", "closed_lost"},
    "proof_pack_delivered": {"upsell_offered", "closed_won", "closed_lost"},
    "upsell_offered": {"closed_won", "closed_lost"},
    "closed_won": set(),
    "closed_lost": set(),
}


def valid_transitions(stage: PipelineStage) -> set[PipelineStage]:
    return set(_FORWARD.get(stage, set()))


def advance_stage(
    *, current: PipelineStage, target: PipelineStage
) -> PipelineStage:
    """Advance from ``current`` to ``target``.

    Raises ``ValueError`` if the transition isn't allowed. The pipeline
    is forward-only by design; if a stage was wrongly advanced, the
    correction is to mark ``closed_lost`` and start a new pipeline.
    """
    allowed = valid_transitions(current)
    if target not in allowed:
        raise ValueError(
            f"invalid transition: {current!r} → {target!r}; "
            f"allowed: {sorted(allowed)}"
        )
    return target


def counts_as_commitment(stage: PipelineStage) -> bool:
    """Has this stage produced at least a written commitment?"""
    return stage in {
        "commitment_received",
        "payment_received",
        "delivery_started",
        "delivered",
        "proof_pack_delivered",
        "upsell_offered",
        "closed_won",
    }


def counts_as_revenue(stage: PipelineStage) -> bool:
    """Has REAL money landed for this customer?"""
    return stage in {
        "payment_received",
        "delivery_started",
        "delivered",
        "proof_pack_delivered",
        "upsell_offered",
        "closed_won",
    }
