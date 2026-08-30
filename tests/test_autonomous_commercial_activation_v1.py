from __future__ import annotations

from dealix.commercial_ops.autonomous_activation import build_activation_command
from dealix.commercial_ops.outreach_drafts import build_outreach_draft_ar


def _war_room(status: str, **extra: str) -> dict:
    row = {
        "company": "Example Co",
        "channel": "email_manual",
        "status": status,
        "priority": "high",
        "pain_hypothesis": "Fragmented commercial handoffs",
        **extra,
    }
    return {"targets": {"items": [row]}}


def test_research_target_never_becomes_relationship_or_send_authority() -> None:
    command = build_activation_command(_war_room("not_contacted"))
    item = command["founder_top_5"][0]
    assert item["stage"] == "ATTENTION"
    assert item["proposed_action"] == "research"
    assert item["action_class"] == "INTERNAL_EXECUTABLE"
    assert item["external_effect_allowed"] is False
    assert command["activation_policy"]["external_send"] is False


def test_legacy_approved_to_send_label_is_not_execution_authority() -> None:
    command = build_activation_command(_war_room("approved_to_send"))
    item = command["founder_top_5"][0]
    assert item["proposed_action"] == "internal_review"
    assert "NOT_EXTERNAL_EXECUTION_AUTHORITY" in item["authority_reason"]
    assert command["execution_authorized_queue"] == []


def test_reply_without_evidence_cannot_promote_to_qualification() -> None:
    command = build_activation_command(_war_room("replied"))
    item = command["founder_top_5"][0]
    assert item["stage"] == "ATTENTION"
    assert item["proposed_action"] == "internal_review"
    assert "WITHOUT_INTERACTION_EVIDENCE" in item["authority_reason"]


def test_reply_with_interaction_evidence_can_prepare_internal_qualification() -> None:
    command = build_activation_command(
        _war_room("replied", interaction_evidence_ref="proof://interaction/123")
    )
    item = command["founder_top_5"][0]
    assert item["stage"] == "INTERACTION"
    assert item["proposed_action"] == "qualify"
    assert "proof://interaction/123" in item["evidence_refs"]
    assert item["external_effect_allowed"] is False


def test_outreach_draft_uses_current_commercial_path_not_legacy_ten_lead_pilot() -> None:
    draft = build_outreach_draft_ar(
        {"company": "Example Co", "channel": "email_manual", "pain_hypothesis": "Revenue leakage"},
        icp={},
        objection_snippet="",
    )
    assert "10 leads" not in draft
    assert "pilot صغير" not in draft
    assert "Mini Diagnostic" in draft
    assert "عرض مخصص" in draft
