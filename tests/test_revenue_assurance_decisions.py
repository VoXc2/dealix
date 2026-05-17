"""Definition of Done, Root Cause Matrix, and Control Rules."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_assurance_os.control_rules import channel_verdict
from auto_client_acquisition.revenue_assurance_os.definition_of_done import dod_status
from auto_client_acquisition.revenue_assurance_os.root_cause import diagnose


def test_dod_reports_missing_criteria() -> None:
    status = dod_status("sales_autopilot", {"every_lead_enters_system"})
    assert status.done is False
    assert "every_lead_scored" in status.missing
    assert status.satisfied_count == 1


def test_dod_unknown_machine_raises() -> None:
    with pytest.raises(ValueError):
        dod_status("imaginary_machine", set())


def test_root_cause_for_weak_conversations_says_do_not_build() -> None:
    counts = {
        "target_accounts": 100,
        "conversations": 3,
        "proof_pack_requests": 2,
        "meetings": 2,
        "scopes": 1,
        "invoices": 1,
        "paid": 1,
        "proof_packs_delivered": 1,
        "upsells": 1,
        "referrals": 1,
    }
    diagnosis = diagnose(counts)
    assert diagnosis.bottleneck_stage == "conversations"
    assert diagnosis.build_recommended is False


def test_root_cause_for_delivery_allows_build() -> None:
    counts = {
        "target_accounts": 100,
        "conversations": 90,
        "proof_pack_requests": 80,
        "meetings": 70,
        "scopes": 60,
        "invoices": 50,
        "paid": 40,
        "proof_packs_delivered": 1,
        "upsells": 1,
        "referrals": 1,
    }
    diagnosis = diagnose(counts)
    assert diagnosis.bottleneck_stage == "proof_packs_delivered"
    assert diagnosis.build_recommended is True


def test_channel_verdict_kill_on_compliance_issue() -> None:
    decision = channel_verdict(
        channel="cold_email",
        qualified_leads=5,
        reply_rate=0.2,
        meeting_rate=0.2,
        compliance_issues=1,
    )
    assert decision.verdict == "kill"


def test_channel_verdict_scale_on_clean_signal() -> None:
    decision = channel_verdict(
        channel="warm_intro",
        qualified_leads=4,
        reply_rate=0.3,
        meeting_rate=0.25,
    )
    assert decision.verdict == "scale"


def test_channel_verdict_keep_on_weak_signal() -> None:
    decision = channel_verdict(
        channel="newsletter",
        qualified_leads=1,
        reply_rate=0.05,
        meeting_rate=0.03,
    )
    assert decision.verdict == "keep"
