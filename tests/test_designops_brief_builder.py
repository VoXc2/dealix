"""Brief builder tests — deterministic, no LLM, no I/O."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_client_acquisition.designops.brief_builder import (
    BriefRequest,
    LockedBrief,
    build_brief,
)


def _full_request(**overrides) -> BriefRequest:
    base = dict(
        skill_name="dealix-sales-email-draft",
        customer_handle="Acme-Saudi-Pilot-EXAMPLE",
        sector="fintech",
        pipeline_state="diagnostic_delivered",
        service_id="svc_diagnostic_v1",
        proof_event_ids=["evt_diag_001"],
    )
    base.update(overrides)
    return BriefRequest(**base)


def test_empty_context_returns_missing_questions() -> None:
    req = BriefRequest(
        skill_name="dealix-sales-email-draft",
        customer_handle="Acme-Saudi-Pilot-EXAMPLE",
    )
    brief = build_brief(req)
    assert isinstance(brief, LockedBrief)
    assert brief.missing_context_questions, "must ask before generating"
    assert brief.content_sections == []
    assert "insufficient_context" in brief.blocked_items
    assert brief.next_step == "ask_founder_for_missing_context"
    assert brief.approval_status == "approval_required"


def test_full_context_returns_content_sections() -> None:
    brief = build_brief(_full_request())
    assert brief.content_sections, "should have sections"
    assert brief.missing_context_questions == []
    assert any(s["id"] == "intro" for s in brief.content_sections)
    assert any(s["id"] == "proof" for s in brief.content_sections)
    # required_evidence picks up service_id + proof_event_ids
    assert "service_id:svc_diagnostic_v1" in brief.required_evidence
    assert "evt_diag_001" in brief.required_evidence


def test_no_proof_events_marks_proof_section_planned() -> None:
    req = _full_request(proof_event_ids=[])
    brief = build_brief(req)
    proof_section = next(
        (s for s in brief.content_sections if s["id"] == "proof"), None
    )
    assert proof_section is not None
    assert proof_section.get("status") == "planned / not yet proven"
    assert "no_proof_events_attached" in brief.blocked_items


def test_approval_status_is_always_approval_required() -> None:
    # Insufficient context branch
    req_thin = BriefRequest(
        skill_name="dealix-sales-email-draft",
        customer_handle="Acme-Saudi-Pilot-EXAMPLE",
    )
    assert build_brief(req_thin).approval_status == "approval_required"

    # Full-context branch
    assert build_brief(_full_request()).approval_status == "approval_required"


def test_visual_direction_defaults_to_saudi_executive_trust() -> None:
    brief = build_brief(_full_request())
    assert brief.visual_direction == "saudi_executive_trust"


def test_visual_direction_passthrough_when_provided() -> None:
    brief = build_brief(_full_request(visual_direction="warm_founder_led_beta"))
    assert brief.visual_direction == "warm_founder_led_beta"


def test_brief_request_empty_customer_handle_raises() -> None:
    with pytest.raises(ValidationError):
        BriefRequest(
            skill_name="dealix-sales-email-draft",
            customer_handle="",  # min_length=1 violation
        )


def test_brief_request_extra_field_raises() -> None:
    """extra='forbid' must catch typos in caller payload."""
    with pytest.raises(ValidationError):
        BriefRequest(
            skill_name="dealix-sales-email-draft",
            customer_handle="Acme-Saudi-Pilot-EXAMPLE",
            unknown_field="oops",  # type: ignore[call-arg]
        )


def test_arabic_primary_english_secondary_default() -> None:
    brief = build_brief(_full_request())
    assert brief.language_primary == "ar"
    assert brief.language_secondary == "en"
