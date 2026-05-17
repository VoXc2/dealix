"""Founder pipeline view — a projection over the canonical journey.

The founder-led revenue machine talks in 16 pipeline labels. Rather than
run a second state machine (which would duplicate the doctrine guards in
``business_ops.stage_definitions`` and ``crm_v10.stage_machine``), this
module *projects* the canonical 22-stage ``JourneyStage`` plus a
lead-level ``LeadClassification`` onto those 16 labels.

There is no transition logic here — advancing a lead/deal stays the job
of the existing state machines. This is a pure read-model.
"""

from __future__ import annotations

from enum import StrEnum

from auto_client_acquisition.business_ops.stage_definitions import JourneyStage


class PipelineState(StrEnum):
    """The 16 founder-facing pipeline labels."""

    NEW_LEAD = "new_lead"
    QUALIFIED_A = "qualified_A"
    QUALIFIED_B = "qualified_B"
    NURTURE = "nurture"
    PARTNER_CANDIDATE = "partner_candidate"
    MEETING_BOOKED = "meeting_booked"
    MEETING_DONE = "meeting_done"
    SCOPE_REQUESTED = "scope_requested"
    SCOPE_SENT = "scope_sent"
    INVOICE_SENT = "invoice_sent"
    INVOICE_PAID = "invoice_paid"
    DELIVERY_STARTED = "delivery_started"
    PROOF_PACK_SENT = "proof_pack_sent"
    SPRINT_CANDIDATE = "sprint_candidate"
    RETAINER_CANDIDATE = "retainer_candidate"
    CLOSED_LOST = "closed_lost"


class LeadClassification(StrEnum):
    """Lead-level classifications — not transition states.

    Set by the founder lead scorer (``founder_lead_scoring``) or by the
    delivery/upsell flow. They refine the pre-meeting and post-delivery
    ends of the funnel, where ``JourneyStage`` alone is not specific
    enough for the founder view.
    """

    UNCLASSIFIED = "unclassified"
    QUALIFIED_A = "qualified_A"
    QUALIFIED_B = "qualified_B"
    NURTURE = "nurture"
    PARTNER_CANDIDATE = "partner_candidate"
    SPRINT_CANDIDATE = "sprint_candidate"
    RETAINER_CANDIDATE = "retainer_candidate"
    DROP = "drop"


# Each JourneyStage projects onto a PipelineState. ``None`` means the
# stage is pre-meeting — too early for a journey-driven label, so the
# lead classification drives the view instead.
_STAGE_VIEW: dict[JourneyStage, PipelineState | None] = {
    JourneyStage.TARGET_IDENTIFIED: None,
    JourneyStage.ICP_QUALIFIED: None,
    JourneyStage.WARM_INTRO_DRAFTED: None,
    JourneyStage.OUTREACH_APPROVED: None,
    JourneyStage.OUTREACH_SENT: None,
    JourneyStage.RESPONSE_RECEIVED: None,
    JourneyStage.DISCOVERY_SCHEDULED: PipelineState.MEETING_BOOKED,
    JourneyStage.DISCOVERY_COMPLETED: PipelineState.MEETING_DONE,
    JourneyStage.FIT_SCORED: PipelineState.SCOPE_REQUESTED,
    JourneyStage.OFFER_PRESENTED: PipelineState.SCOPE_REQUESTED,
    JourneyStage.PROPOSAL_SENT: PipelineState.SCOPE_SENT,
    JourneyStage.NEGOTIATION: PipelineState.SCOPE_SENT,
    JourneyStage.VERBAL_AGREEMENT: PipelineState.SCOPE_SENT,
    JourneyStage.CONTRACT_SENT: PipelineState.SCOPE_SENT,
    JourneyStage.CONTRACT_SIGNED: PipelineState.SCOPE_SENT,
    JourneyStage.INVOICE_ISSUED: PipelineState.INVOICE_SENT,
    JourneyStage.PAYMENT_CONFIRMED: PipelineState.INVOICE_PAID,
    JourneyStage.ONBOARDING_STARTED: PipelineState.DELIVERY_STARTED,
    JourneyStage.DELIVERY_IN_PROGRESS: PipelineState.DELIVERY_STARTED,
    JourneyStage.DELIVERY_COMPLETED: PipelineState.PROOF_PACK_SENT,
    JourneyStage.RESULT_DOCUMENTED: PipelineState.PROOF_PACK_SENT,
    JourneyStage.CASE_STUDY_CANDIDATE: PipelineState.PROOF_PACK_SENT,
}

# Pre-meeting view: the classification is the label.
_CLASSIFICATION_VIEW: dict[LeadClassification, PipelineState] = {
    LeadClassification.QUALIFIED_A: PipelineState.QUALIFIED_A,
    LeadClassification.QUALIFIED_B: PipelineState.QUALIFIED_B,
    LeadClassification.NURTURE: PipelineState.NURTURE,
    LeadClassification.PARTNER_CANDIDATE: PipelineState.PARTNER_CANDIDATE,
    LeadClassification.DROP: PipelineState.CLOSED_LOST,
}

# Stages where a post-delivery upsell classification can refine the view.
_POST_DELIVERY = frozenset({
    JourneyStage.DELIVERY_COMPLETED,
    JourneyStage.RESULT_DOCUMENTED,
    JourneyStage.CASE_STUDY_CANDIDATE,
})

_UPSELL_VIEW: dict[LeadClassification, PipelineState] = {
    LeadClassification.SPRINT_CANDIDATE: PipelineState.SPRINT_CANDIDATE,
    LeadClassification.RETAINER_CANDIDATE: PipelineState.RETAINER_CANDIDATE,
}


def to_pipeline_view(
    journey_stage: JourneyStage,
    *,
    lead_classification: LeadClassification = LeadClassification.UNCLASSIFIED,
    closed_lost: bool = False,
) -> PipelineState:
    """Project a canonical journey stage onto a founder pipeline label.

    ``closed_lost`` (a lost deal or disqualified lead) overrides everything.
    Pre-meeting stages defer to ``lead_classification``; post-delivery
    stages let a sprint/retainer classification refine the view.
    """
    if closed_lost:
        return PipelineState.CLOSED_LOST

    view = _STAGE_VIEW[journey_stage]

    if view is None:
        return _CLASSIFICATION_VIEW.get(lead_classification, PipelineState.NEW_LEAD)

    if journey_stage in _POST_DELIVERY and lead_classification in _UPSELL_VIEW:
        return _UPSELL_VIEW[lead_classification]

    return view


def all_pipeline_states() -> tuple[PipelineState, ...]:
    """The 16 founder pipeline labels in funnel order."""
    return tuple(PipelineState)


__all__ = [
    "LeadClassification",
    "PipelineState",
    "all_pipeline_states",
    "to_pipeline_view",
]
