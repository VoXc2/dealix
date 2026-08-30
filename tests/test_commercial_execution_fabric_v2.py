from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx

from dealix.commercial.conversation_autonomy import plan_conversation_turn
from dealix.commercial.external_execution_gate import (
    ApprovalEnvelope,
    RuntimeAuthority,
    build_external_action_packet,
    canonical_content_sha256,
    evaluate_external_action,
)
from dealix.commercial.gmail_guarded_provider import GmailArtifact, send_approved_gmail_message
from dealix.commercial.web_research_adapter import AUTHORITY, TavilyReadOnlyAdapter


def _ts(delta_minutes: int) -> str:
    return (datetime.now(UTC) + timedelta(minutes=delta_minutes)).isoformat()


def _packet(*, destination: str = "buyer@example.com", body: str = "Requested diagnostic follow-up"):
    content_hash = canonical_content_sha256(destination=destination, subject="Dealix follow-up", body=body)
    return build_external_action_packet(
        action_id="a-1",
        action_class="EMAIL_SEND",
        purpose_class="REQUESTED_FOLLOWUP",
        destination=destination,
        channel="email",
        artifact_ref="runtime://draft/a-1",
        content_sha256=content_hash,
        identity_or_relationship_ref="evidence://interaction/1",
        consent_or_channel_eligibility_ref="evidence://requested-followup/1",
        suppression_check_ref="evidence://suppression/1",
        suppression_clear=True,
        claim_evidence_refs=["evidence://claims/1"],
        sender_identity_ref="policy://dealix-sender-identity",
        exact_scope="one_message_to_buyer@example.com",
        expires_at=_ts(30),
        provider="gmail_api",
        idempotency_key="send-a-1-v1",
    )


def _approval(packet, *, state="APPROVED"):
    return ApprovalEnvelope(
        approval_id="approval-1",
        action_fingerprint=packet.action_fingerprint,
        exact_scope=packet.exact_scope,
        authority_class=packet.action_class,
        approval_state=state,
        approval_state_ref="approval://1/state",
        state_checked_at=_ts(-1),
        expires_at=_ts(20),
        evidence_refs=["approval://1/evidence"],
    )


def test_exact_approval_still_cannot_send_while_runtime_authority_is_false() -> None:
    packet = _packet()
    decision = evaluate_external_action(packet, approval=_approval(packet), runtime=RuntimeAuthority())
    assert decision.verdict == "READY_BUT_RUNTIME_AUTHORITY_DISABLED"
    assert decision.provider_execution_allowed is False
    assert decision.approval_valid is True


def test_exact_approved_packet_can_become_provider_ready_only_with_all_runtime_switches() -> None:
    packet = _packet()
    runtime = RuntimeAuthority(external_send=True, connector_write=True)
    decision = evaluate_external_action(packet, approval=_approval(packet), runtime=runtime)
    assert decision.verdict == "READY_FOR_PROVIDER_EXECUTION"
    assert decision.provider_execution_allowed is True


def test_content_or_destination_change_invalidates_previous_approval() -> None:
    original = _packet()
    approval = _approval(original)
    changed = _packet(destination="other@example.com")
    decision = evaluate_external_action(
        changed,
        approval=approval,
        runtime=RuntimeAuthority(external_send=True, connector_write=True),
    )
    assert decision.provider_execution_allowed is False
    assert "APPROVAL_FINGERPRINT_MISMATCH" in decision.reasons


def test_direct_marketing_requires_consent_and_opt_out() -> None:
    content_hash = canonical_content_sha256(destination="x@example.com", subject="x", body="x")
    packet = build_external_action_packet(
        action_id="m-1",
        action_class="EMAIL_SEND",
        purpose_class="DIRECT_MARKETING",
        destination="x@example.com",
        channel="email",
        artifact_ref="runtime://m1",
        content_sha256=content_hash,
        identity_or_relationship_ref="evidence://identity/x",
        consent_or_channel_eligibility_ref="",
        suppression_check_ref="evidence://suppression/x",
        suppression_clear=True,
        claim_evidence_refs=["evidence://claims/x"],
        sender_identity_ref="policy://sender",
        opt_out_mechanism_ref="",
        exact_scope="one-email",
        expires_at=_ts(30),
        provider="gmail_api",
        idempotency_key="m1",
    )
    decision = evaluate_external_action(packet, approval=None)
    assert "DIRECT_MARKETING_CONSENT_NOT_PROVEN" in decision.reasons
    assert "DIRECT_MARKETING_OPT_OUT_NOT_PROVEN" in decision.reasons
    assert decision.provider_execution_allowed is False


def test_suppression_overrides_approval() -> None:
    packet = _packet().model_copy(update={"suppression_clear": False})
    decision = evaluate_external_action(
        packet,
        approval=_approval(packet),
        runtime=RuntimeAuthority(external_send=True, connector_write=True),
    )
    assert decision.provider_execution_allowed is False
    assert "SUPPRESSED_OR_SUPPRESSION_NOT_PROVEN_CLEAR" in decision.reasons


def test_founder_linkedin_is_manual_native() -> None:
    content_hash = canonical_content_sha256(destination="linkedin-profile", subject="manual", body="manual")
    packet = build_external_action_packet(
        action_id="li-1",
        action_class="FOUNDER_LINKEDIN_MANUAL",
        purpose_class="REQUESTED_FOLLOWUP",
        destination="linkedin-profile",
        channel="founder_linkedin",
        artifact_ref="runtime://li1",
        content_sha256=content_hash,
        suppression_check_ref="evidence://suppression/li",
        suppression_clear=True,
        claim_evidence_refs=["evidence://claims/li"],
        sender_identity_ref="policy://founder",
        exact_scope="manual-native",
        expires_at=_ts(30),
        provider="manual_native",
        idempotency_key="li1",
    )
    decision = evaluate_external_action(packet, approval=None)
    assert decision.verdict == "MANUAL_NATIVE_ONLY"


def test_tavily_is_fail_closed_without_explicit_enablement() -> None:
    adapter = TavilyReadOnlyAdapter(api_key="secret", enabled=False)
    result = adapter.execute(endpoint="search", payload={"query": "Saudi B2B AI"}, request_id="r1")
    assert result.receipt.status == "BLOCKED_NOT_EXPLICITLY_ENABLED"
    assert result.receipt.authority == AUTHORITY
    assert result.payload is None


def test_tavily_mock_result_preserves_all_false_authority_and_sources() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer secret"
        return httpx.Response(200, json={"results": [{"url": "https://example.com/a", "content": "x"}]})

    adapter = TavilyReadOnlyAdapter(api_key="secret", enabled=True, transport=httpx.MockTransport(handler))
    result = adapter.execute(endpoint="search", payload={"query": "q"}, request_id="r2")
    assert result.receipt.status == "READ_ONLY_RESULT_RECEIVED"
    assert result.receipt.source_refs == ["https://example.com/a"]
    assert result.receipt.authority["relationship"] is False
    assert result.receipt.authority["external_send"] is False


def test_conversation_router_maps_objection_to_negotiation_without_send() -> None:
    class FakeEngine:
        def handle_objection(self, category, context=None, lang="both"):
            return {"category": category, "authority": {"execution_allowed": False}, "context": context}

    plan = plan_conversation_turn(
        "too expensive",
        evidence_refs=["email://thread/1#msg2"],
        route_result={"category": "OBJECTION", "route": "objection_handling", "suppress": False},
        objection_category="price",
        negotiation_engine=FakeEngine(),
    )
    assert plan.proposed_action == "prepare_negotiation"
    assert plan.external_effect_allowed is False
    assert plan.negotiation_support["category"] == "price"


def test_unsubscribe_is_suppression_not_sales_opportunity() -> None:
    plan = plan_conversation_turn(
        "unsubscribe",
        evidence_refs=["email://thread/1#msg3"],
        route_result={"category": "UNSUBSCRIBE", "route": "suppress_immediately", "suppress": True},
    )
    assert plan.suppress is True
    assert plan.stage == "SUPPRESSED"
    assert plan.approval_class == "SUPPRESSION_ENFORCEMENT"


class _FakeSendCall:
    def execute(self):
        return {"id": "msg-1", "threadId": "thread-1"}


class _FakeMessages:
    def __init__(self):
        self.calls = []

    def send(self, *, userId, body):
        self.calls.append((userId, body))
        return _FakeSendCall()


class _FakeUsers:
    def __init__(self, messages):
        self._messages = messages

    def messages(self):
        return self._messages


class _FakeGmail:
    def __init__(self):
        self.messages_api = _FakeMessages()

    def users(self):
        return _FakeUsers(self.messages_api)


def test_gmail_provider_executes_once_only_after_exact_gate_pass() -> None:
    artifact = GmailArtifact(to="buyer@example.com", subject="Dealix follow-up", body_text="Requested diagnostic follow-up")
    packet = _packet(body=artifact.body_text)
    assert packet.content_sha256 == artifact.content_sha256
    fake = _FakeGmail()
    receipt = send_approved_gmail_message(
        artifact,
        packet=packet,
        approval=_approval(packet),
        runtime=RuntimeAuthority(external_send=True, connector_write=True),
        service=fake,
    )
    assert receipt.status == "PROVIDER_ACCEPTED_SEND_REQUEST"
    assert receipt.provider_message_id == "msg-1"
    assert receipt.body_or_subject_logged is False
    assert len(fake.messages_api.calls) == 1


def test_gmail_provider_refuses_content_drift() -> None:
    artifact = GmailArtifact(to="buyer@example.com", subject="Dealix follow-up", body_text="CHANGED")
    packet = _packet(body="original")
    try:
        send_approved_gmail_message(
            artifact,
            packet=packet,
            approval=_approval(packet),
            runtime=RuntimeAuthority(external_send=True, connector_write=True),
            service=_FakeGmail(),
        )
    except PermissionError as exc:
        assert "message content changed" in str(exc)
    else:
        raise AssertionError("content drift must fail closed")
