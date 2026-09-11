from __future__ import annotations

import importlib.util
import sys
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from dealix.commercial.external_execution_gate import (
    build_external_action_packet,
    canonical_content_sha256,
)
from dealix.company_os.founder_delegation import (
    DelegationUsage,
    FounderDelegationSession,
    evaluate_founder_delegation,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "company" / "dealix_command_room_v1.json"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_command_room_v1.py"
RUNNER = ROOT / "scripts" / "commercial" / "run_dealix_command_room_v1.py"
INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_command_room_v1.sh"

CANONICAL_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _packet(*, destination: str = "known@example.com", body: str = "Requested follow-up", expires: datetime | None = None):
    expiry = expires or (datetime.now(UTC) + timedelta(minutes=15))
    content_hash = canonical_content_sha256(
        destination=destination,
        subject="Dealix follow-up",
        body=body,
    )
    return build_external_action_packet(
        action_id="ACT-TEST-001",
        action_class="EMAIL_SEND",
        purpose_class="REQUESTED_FOLLOWUP",
        destination=destination,
        channel="gmail",
        environment="production",
        artifact_ref="artifact:test-followup",
        content_sha256=content_hash,
        identity_or_relationship_ref="interaction:test-001",
        consent_or_channel_eligibility_ref="eligibility:test-001",
        suppression_check_ref="suppression:test-clear-001",
        suppression_clear=True,
        claim_evidence_refs=["evidence:test-001"],
        sender_identity_ref="sender:dealix-founder-office",
        opt_out_mechanism_ref="",
        risk_class="MEDIUM",
        exact_scope="reply to known@example.com in existing requested-followup thread",
        expires_at=_iso(expiry),
        provider="gmail_api",
        idempotency_key="idem:test-followup-001",
    )


def _session(*, now: datetime | None = None, **overrides):
    current = now or datetime.now(UTC)
    values = {
        "session_id": "FDS-TEST-001",
        "founder_identity_ref": "founder:verified:test",
        "canonical_approval_ref": "approval-policy:test",
        "channel": "gmail",
        "provider": "gmail_api",
        "conversation_ids": ["thread-001"],
        "recipients": ["known@example.com"],
        "allowed_purpose_classes": ["REQUESTED_FOLLOWUP"],
        "allowed_action_classes": ["EMAIL_SEND"],
        "starts_at": _iso(current - timedelta(minutes=1)),
        "expires_at": _iso(current + timedelta(minutes=30)),
        "max_messages": 10,
        "max_calls": 0,
        "consent_or_channel_eligibility_ref": "eligibility:test-001",
        "suppression_check_ref": "suppression:test-clear-001",
    }
    values.update(overrides)
    return FounderDelegationSession(**values)


def test_command_room_keeps_exactly_five_permanent_agents_and_explicit_channel_readiness() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert set(config["canonical_agents"]) == CANONICAL_AGENTS
    assert config["deep_wip_max"] == 3
    assert config["founder_delegation"]["enabled_by_default"] is False
    assert all("readiness" in channel for channel in config["channels"])
    assert all("live_execution_ready" in channel for channel in config["channels"])
    assert not any(channel["live_execution_ready"] for channel in config["channels"])


def test_gmail_and_whatsapp_do_not_claim_unproven_live_execution() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    channels = {channel["id"]: channel for channel in config["channels"]}
    assert channels["gmail"]["readiness"] == "PROVIDER_QUARANTINED"
    assert channels["gmail"]["live_execution_ready"] is False
    assert channels["whatsapp-business"]["readiness"] == "ADAPTER_PRESENT_AUTHORITY_NOT_PROVEN"
    assert channels["whatsapp-business"]["live_execution_ready"] is False
    assert channels["voice"]["automated_identity_disclosure_required"] is True
    assert channels["voice"]["live_execution_ready"] is False


def test_requested_followup_can_only_become_eligible_for_exact_action_approval() -> None:
    now = datetime.now(UTC)
    decision = evaluate_founder_delegation(
        session=_session(now=now),
        packet=_packet(expires=now + timedelta(minutes=15)),
        usage=DelegationUsage(messages_committed=0, calls_committed=0),
        now=now,
        conversation_id="thread-001",
    )
    assert decision.verdict == "ELIGIBLE_FOR_ACTION_BOUND_APPROVAL"
    assert decision.approval_minting_allowed is True
    assert decision.provider_execution_allowed is False
    assert decision.reasons == []


def test_delegation_requires_recipient_or_conversation_scope() -> None:
    with pytest.raises(ValueError, match="at least one recipient or conversation scope"):
        _session(recipients=[], conversation_ids=[])


def test_new_recipient_outside_delegation_scope_is_blocked() -> None:
    now = datetime.now(UTC)
    decision = evaluate_founder_delegation(
        session=_session(now=now),
        packet=_packet(destination="new-person@example.com", expires=now + timedelta(minutes=15)),
        usage=DelegationUsage(),
        now=now,
        conversation_id="thread-001",
    )
    assert decision.verdict == "BLOCKED"
    assert decision.approval_minting_allowed is False
    assert "recipient is outside delegated scope" in decision.reasons


def test_expired_or_revoked_delegation_is_blocked() -> None:
    now = datetime.now(UTC)
    expired = _session(
        now=now,
        starts_at=_iso(now - timedelta(hours=2)),
        expires_at=_iso(now - timedelta(minutes=1)),
    )
    revoked = _session(now=now, revoked=True)

    expired_decision = evaluate_founder_delegation(
        session=expired,
        packet=_packet(expires=now + timedelta(minutes=15)),
        usage=DelegationUsage(),
        now=now,
        conversation_id="thread-001",
    )
    revoked_decision = evaluate_founder_delegation(
        session=revoked,
        packet=_packet(expires=now + timedelta(minutes=15)),
        usage=DelegationUsage(),
        now=now,
        conversation_id="thread-001",
    )

    assert "delegation session is expired" in expired_decision.reasons
    assert "delegation session is revoked" in revoked_decision.reasons
    assert expired_decision.provider_execution_allowed is False
    assert revoked_decision.provider_execution_allowed is False


def test_message_budget_exhaustion_blocks_delegation() -> None:
    now = datetime.now(UTC)
    decision = evaluate_founder_delegation(
        session=_session(now=now, max_messages=2),
        packet=_packet(expires=now + timedelta(minutes=15)),
        usage=DelegationUsage(),
        now=now,
        conversation_id="thread-001",
    )
    assert decision.verdict == "BLOCKED"
    assert "delegated message budget exhausted" in decision.reasons


def test_delegation_cannot_expand_into_quote_contract_payment_publish_or_spend() -> None:
    now = datetime.now(UTC)
    dangerous = _session(
        now=now,
        binding_quote_allowed=True,
        contract_commitment_allowed=True,
        payment_or_refund_allowed=True,
        public_publish_allowed=True,
        paid_spend_allowed=True,
    )
    decision = evaluate_founder_delegation(
        session=dangerous,
        packet=_packet(expires=now + timedelta(minutes=15)),
        usage=DelegationUsage(),
        now=now,
        conversation_id="thread-001",
    )
    assert decision.verdict == "BLOCKED"
    assert len(decision.reasons) >= 5
    assert decision.provider_execution_allowed is False


def test_material_message_change_changes_action_hash() -> None:
    a = _packet(body="Version A")
    b = _packet(body="Version B")
    assert a.content_sha256 != b.content_sha256
    assert a.action_hash != b.action_hash


def test_command_room_runner_and_installer_do_not_create_live_effect_authority() -> None:
    runner = RUNNER.read_text(encoding="utf-8")
    installer = INSTALLER.read_text(encoding="utf-8")
    verifier = VERIFY.read_text(encoding="utf-8")

    assert "EXTERNAL_EFFECTS=NONE_BY_THIS_RUNNER" in runner
    assert '"DEALIX_EXTERNAL_SEND": {"1", "true", "yes"}' in runner
    assert "export DEALIX_EXTERNAL_SEND=0" in installer
    assert "SCHEDULER_CREATED=false" in installer
    assert "LIVE_EXTERNAL_CHANNELS_CLAIMED_READY=0" in verifier
    assert "systemctl enable" not in installer
    assert "systemctl start" not in installer


def test_default_command_room_executes_exactly_all_five_canonical_agents() -> None:
    spec = importlib.util.spec_from_file_location("dealix_command_room_runner_test", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    owners = [owner for _, owner, _, _ in module.RUNNERS]
    assert set(owners) == CANONICAL_AGENTS
    assert len(owners) == len(CANONICAL_AGENTS)
    labels = {label for label, _, _, _ in module.RUNNERS}
    assert "weekly_proof_pack" in labels
    assert "content_factory" in labels
