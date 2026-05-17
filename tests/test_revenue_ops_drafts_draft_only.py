"""Revenue Ops Machine — drafts are always queued for approval, never sent."""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.revenue_ops_machine.drafts import (
    DraftSpec,
    blocked_proof_events,
    gate_specs,
    to_outreach_records,
)
from auto_client_acquisition.proof_ledger.schemas import ProofEventType

SAFE_SPECS = [
    DraftSpec(kind="follow_up", channel="email", message="Reply to book a review."),
    DraftSpec(kind="meeting_brief", channel="internal", message="Cover the workflow."),
]


def test_every_safe_draft_becomes_a_queued_record() -> None:
    gated = gate_specs(SAFE_SPECS)
    records = to_outreach_records(gated, lead_id="lead_1")
    assert len(records) == len(SAFE_SPECS)
    for rec in records:
        assert rec.status == "queued"
        assert rec.approval_required is True
        assert rec.sent_at is None
        assert rec.lead_id == "lead_1"


def test_no_record_is_ever_marked_sent() -> None:
    records = to_outreach_records(gate_specs(SAFE_SPECS), lead_id="lead_2")
    assert all(rec.status != "sent" for rec in records)


def test_external_draft_requires_approval() -> None:
    gated = gate_specs([DraftSpec(kind="follow_up", channel="email", message="Hello there.")])
    assert gated[0].blocked is False
    assert gated[0].decision == GovernanceDecision.REQUIRE_APPROVAL


def test_guaranteed_results_claim_is_blocked_and_dropped() -> None:
    specs = [
        DraftSpec(
            kind="follow_up",
            channel="email",
            message="We offer guaranteed results and guaranteed ROI.",
        )
    ]
    gated = gate_specs(specs)
    assert gated[0].blocked is True
    assert gated[0].decision == GovernanceDecision.BLOCK
    # A blocked draft never reaches the outreach queue.
    assert to_outreach_records(gated, lead_id="lead_3") == []


def test_blocked_draft_produces_risk_blocked_proof_event() -> None:
    specs = [DraftSpec(kind="follow_up", channel="email", message="guaranteed sales!")]
    gated = gate_specs(specs)
    events = blocked_proof_events(gated)
    assert len(events) == 1
    assert events[0].event_type == ProofEventType.RISK_BLOCKED
    assert events[0].risk_level == "high"


def test_auto_send_language_is_dropped_from_the_queue() -> None:
    specs = [
        DraftSpec(
            kind="follow_up",
            channel="whatsapp",
            message="We will auto-send this without approval.",
        )
    ]
    gated = gate_specs(specs)
    # "auto-send" is a forbidden operational term -> not auto-approved.
    assert gated[0].decision != GovernanceDecision.ALLOW
