"""Revenue Autopilot automations — drafts only, approvals routed, no live send."""
from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.revenue_autopilot import orchestrator
from auto_client_acquisition.revenue_autopilot.orchestrator import (
    advance_funnel,
    capture_lead,
    run_automation,
)

_FORBIDDEN_MODES = {"live_send", "live_charge", "auto_send", "auto_charge"}

_QUALIFIED_A = {
    "is_decision_maker": True, "is_b2b_company": True,
    "has_revenue_workflow": True, "uses_or_plans_ai": True,
}


@pytest.fixture(autouse=True)
def _reset():
    orchestrator.reset()
    yield
    orchestrator.reset()


def test_lead_capture_scores_and_drafts_first_response():
    engagement, result = capture_lead(
        contact={"name": "Test", "company": "Acme"},
        signals=_QUALIFIED_A,
    )
    assert engagement.current_stage == "qualified_A"
    assert engagement.lead_score is not None
    assert engagement.lead_score.points == 12
    assert len(engagement.drafts) == 1
    # First-response email is queued for founder approval, never auto-sent.
    assert engagement.drafts[0].action_mode == "approval_required"
    assert engagement.drafts[0].approval_id is not None
    assert result.stage_before == "new_lead"
    assert result.stage_after == "qualified_A"


def test_no_automation_ever_produces_a_live_send_action_mode():
    engagement, _ = capture_lead(contact={}, signals=_QUALIFIED_A)
    eid = engagement.engagement_id
    run_automation("qualified_lead", eid)
    run_automation("meeting_booked", eid)
    run_automation("meeting_done", eid, {"scope_requested": True})
    run_automation("scope_requested", eid)
    advance_funnel(eid, "invoice_sent")
    run_automation("invoice_paid", eid)
    run_automation("delivery", eid)
    run_automation("proof_pack_sent", eid)
    final, _ = run_automation("retainer_sprint_upsell", eid, {"target": "sprint_candidate"})

    assert final.current_stage == "sprint_candidate"
    for draft in final.drafts:
        assert draft.action_mode not in _FORBIDDEN_MODES
        assert draft.action_mode in ("draft_only", "approval_required", "approved_manual")


def test_external_actions_are_routed_to_the_approval_center():
    store = get_default_approval_store()
    engagement, _ = capture_lead(contact={}, signals=_QUALIFIED_A)
    eid = engagement.engagement_id
    before = len([a for a in store.list_pending() if a.object_id == eid])
    run_automation("qualified_lead", eid)
    after = len([a for a in store.list_pending() if a.object_id == eid])
    # qualified_lead queues a booking email for approval.
    assert after > before
    # Every approval_id on the engagement exists in the approval center.
    pending_ids = {a.approval_id for a in store.list_pending()}
    history_ids = {a.approval_id for a in store.list_history(limit=1000)}
    for approval_id in engagement.approval_ids:
        assert approval_id in pending_ids | history_ids


def test_hard_rule_invoice_paid_rejected_before_invoice_sent():
    engagement, _ = capture_lead(contact={}, signals=_QUALIFIED_A)
    eid = engagement.engagement_id
    run_automation("meeting_booked", eid)
    run_automation("meeting_done", eid, {"scope_requested": True})
    run_automation("scope_requested", eid)
    # Skipping the founder's invoice_sent advance — automation must refuse.
    with pytest.raises(ValueError):
        run_automation("invoice_paid", eid)


def test_meeting_done_without_scope_routes_to_nurture():
    engagement, _ = capture_lead(contact={}, signals=_QUALIFIED_A)
    eid = engagement.engagement_id
    run_automation("meeting_booked", eid)
    final, _ = run_automation("meeting_done", eid, {"scope_requested": False})
    assert final.current_stage == "nurture"


def test_every_automation_logs_an_evidence_event():
    engagement, _ = capture_lead(contact={}, signals=_QUALIFIED_A)
    eid = engagement.engagement_id
    assert len(engagement.evidence_events) == 1  # form_submitted
    run_automation("qualified_lead", eid)
    assert len(engagement.evidence_events) == 2
    assert engagement.evidence_events[-1].kind == "qualified_lead_actioned"


def test_unknown_automation_name_raises():
    engagement, _ = capture_lead(contact={}, signals=_QUALIFIED_A)
    with pytest.raises(ValueError):
        run_automation("not_a_real_automation", engagement.engagement_id)
