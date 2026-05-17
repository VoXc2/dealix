"""Founder pipeline view — projection over the canonical journey."""

from __future__ import annotations

from auto_client_acquisition.business_ops.stage_definitions import JourneyStage
from auto_client_acquisition.crm_v10.pipeline_view import (
    LeadClassification,
    PipelineState,
    _STAGE_VIEW,
    all_pipeline_states,
    to_pipeline_view,
)


def test_every_journey_stage_is_mapped():
    """No orphan JourneyStage — the projection must cover all 22 stages."""
    assert set(_STAGE_VIEW) == set(JourneyStage)


def test_sixteen_pipeline_states():
    assert len(all_pipeline_states()) == 16
    assert len(set(all_pipeline_states())) == 16


def test_all_pipeline_states_are_reachable():
    """Every one of the 16 labels must be producible by some projection."""
    produced: set[PipelineState] = set()
    for stage in JourneyStage:
        for classification in LeadClassification:
            produced.add(to_pipeline_view(stage, lead_classification=classification))
    produced.add(to_pipeline_view(JourneyStage.TARGET_IDENTIFIED, closed_lost=True))
    assert produced == set(PipelineState)


def test_journey_stage_projections():
    assert to_pipeline_view(JourneyStage.DISCOVERY_SCHEDULED) == PipelineState.MEETING_BOOKED
    assert to_pipeline_view(JourneyStage.DISCOVERY_COMPLETED) == PipelineState.MEETING_DONE
    assert to_pipeline_view(JourneyStage.FIT_SCORED) == PipelineState.SCOPE_REQUESTED
    assert to_pipeline_view(JourneyStage.PROPOSAL_SENT) == PipelineState.SCOPE_SENT
    assert to_pipeline_view(JourneyStage.INVOICE_ISSUED) == PipelineState.INVOICE_SENT
    assert to_pipeline_view(JourneyStage.PAYMENT_CONFIRMED) == PipelineState.INVOICE_PAID
    assert to_pipeline_view(JourneyStage.DELIVERY_IN_PROGRESS) == PipelineState.DELIVERY_STARTED
    assert to_pipeline_view(JourneyStage.RESULT_DOCUMENTED) == PipelineState.PROOF_PACK_SENT


def test_closed_lost_overrides_everything():
    assert (
        to_pipeline_view(JourneyStage.PAYMENT_CONFIRMED, closed_lost=True)
        == PipelineState.CLOSED_LOST
    )


def test_pre_meeting_defers_to_classification():
    assert (
        to_pipeline_view(JourneyStage.TARGET_IDENTIFIED) == PipelineState.NEW_LEAD
    )
    assert (
        to_pipeline_view(
            JourneyStage.ICP_QUALIFIED,
            lead_classification=LeadClassification.QUALIFIED_A,
        )
        == PipelineState.QUALIFIED_A
    )
    assert (
        to_pipeline_view(
            JourneyStage.OUTREACH_SENT,
            lead_classification=LeadClassification.PARTNER_CANDIDATE,
        )
        == PipelineState.PARTNER_CANDIDATE
    )
    assert (
        to_pipeline_view(
            JourneyStage.TARGET_IDENTIFIED,
            lead_classification=LeadClassification.DROP,
        )
        == PipelineState.CLOSED_LOST
    )


def test_post_delivery_upsell_classification_refines_view():
    assert (
        to_pipeline_view(
            JourneyStage.RESULT_DOCUMENTED,
            lead_classification=LeadClassification.SPRINT_CANDIDATE,
        )
        == PipelineState.SPRINT_CANDIDATE
    )
    assert (
        to_pipeline_view(
            JourneyStage.CASE_STUDY_CANDIDATE,
            lead_classification=LeadClassification.RETAINER_CANDIDATE,
        )
        == PipelineState.RETAINER_CANDIDATE
    )
    # An upsell classification before delivery does not leak backward.
    assert (
        to_pipeline_view(
            JourneyStage.PROPOSAL_SENT,
            lead_classification=LeadClassification.SPRINT_CANDIDATE,
        )
        == PipelineState.SCOPE_SENT
    )
