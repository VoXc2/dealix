from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta

import httpx
import pytest

from dealix.commercial.conversation_autonomy import plan_conversation_turn
from dealix.commercial.external_execution_gate import (
    ApprovalEnvelope,
    ResolvedAuthoritySnapshot,
    RuntimeAuthority,
    build_external_action_packet,
    canonical_action_hash,
    canonical_content_sha256,
    evaluate_external_action,
    evaluate_resolved_external_action,
)
from dealix.commercial.gmail_guarded_provider import GmailArtifact, send_approved_gmail_message
from dealix.commercial.idempotency_ledger import SqliteIdempotencyLedger
from dealix.commercial.web_research_adapter import AUTHORITY, TavilyReadOnlyAdapter


def _ts(delta_minutes: int) -> str:
    return (datetime.now(UTC) + timedelta(minutes=delta_minutes)).isoformat()


def _packet(*, destination: str = "buyer@example.com", body: str = "Requested diagnostic follow-up", idempotency_key: str = "send-a-1-v1"):
    content_hash=canonical_content_sha256(destination=destination,subject="Dealix follow-up",body=body)
    return build_external_action_packet(action_id="a-1",action_class="EMAIL_SEND",purpose_class="REQUESTED_FOLLOWUP",
        destination=destination,channel="email",environment="production",artifact_ref="runtime://draft/a-1",content_sha256=content_hash,
        identity_or_relationship_ref="evidence://interaction/1",consent_or_channel_eligibility_ref="evidence://requested-followup/1",
        suppression_check_ref="evidence://suppression/1",suppression_clear=True,claim_evidence_refs=["evidence://claims/1"],
        sender_identity_ref="policy://dealix-sender-identity",exact_scope=f"one_message_to_{destination}",expires_at=_ts(30),provider="gmail_api",idempotency_key=idempotency_key)


def _approval(packet, *, state="APPROVED"):
    return ApprovalEnvelope(approval_id="approval-1",action_hash=packet.action_hash,exact_scope=packet.exact_scope,
        authority_class=packet.action_class,approval_state=state,approval_state_ref="approval://1/state",
        state_checked_at=datetime.now(UTC).isoformat(),expires_at=_ts(20),evidence_refs=["approval://1/evidence"])


class _Resolver:
    def __init__(self, *, state="APPROVED", runtime=None):
        self.state=state; self.runtime=runtime or RuntimeAuthority(external_send=True,connector_write=True)
    def resolve_current(self,packet):
        return ResolvedAuthoritySnapshot(source_ref="canonical://approval-center/current",resolved_at=datetime.now(UTC).isoformat(),approval=_approval(packet,state=self.state),runtime=self.runtime,
            identity_or_relationship_ref=packet.identity_or_relationship_ref,consent_or_channel_eligibility_ref=packet.consent_or_channel_eligibility_ref,
            suppression_check_ref=packet.suppression_check_ref,suppression_clear=packet.suppression_clear,claim_evidence_refs=list(packet.claim_evidence_refs),
            sender_identity_ref=packet.sender_identity_ref,opt_out_mechanism_ref=packet.opt_out_mechanism_ref)


def test_action_hash_matches_repository_l5_contract() -> None:
    expected=hashlib.sha256(b"EMAIL_SEND|buyer@example.com|production|payload").hexdigest()[:16]
    assert canonical_action_hash(action_type="EMAIL_SEND",target="buyer@example.com",environment="production",payload="payload")==expected


def test_caller_supplied_approval_and_runtime_never_grant_provider_authority() -> None:
    packet=_packet(); d=evaluate_external_action(packet,approval=_approval(packet),runtime=RuntimeAuthority(external_send=True,connector_write=True))
    assert d.verdict=="HOLD_CANONICAL_AUTHORITY_REQUIRED" and d.provider_execution_allowed is False


def test_packet_mutation_with_stale_hashes_is_rejected() -> None:
    mutated=_packet().model_copy(update={"destination":"other@example.com"})
    d=evaluate_resolved_external_action(mutated,authority=_Resolver().resolve_current(mutated))
    assert not d.provider_execution_allowed and "PACKET_INTEGRITY_MISMATCH" in d.reasons and "ACTION_HASH_MISMATCH" in d.reasons


def test_fresh_revocation_blocks_cached_approval() -> None:
    packet=_packet(); d=evaluate_resolved_external_action(packet,authority=_Resolver(state="REVOKED").resolve_current(packet))
    assert not d.provider_execution_allowed and "APPROVAL_STATE_REVOKED" in d.reasons


def test_stale_approval_state_check_is_rejected_even_with_fresh_snapshot() -> None:
    packet=_packet(); fresh=_Resolver().resolve_current(packet)
    stale=fresh.model_copy(update={"approval":fresh.approval.model_copy(update={"state_checked_at":_ts(-2)})})
    d=evaluate_resolved_external_action(packet,authority=stale)
    assert not d.provider_execution_allowed and "APPROVAL_STATE_STALE" in d.reasons


def test_fresh_resolved_packet_can_only_be_ready_with_all_runtime_switches() -> None:
    packet=_packet()
    assert evaluate_resolved_external_action(packet,authority=_Resolver(runtime=RuntimeAuthority()).resolve_current(packet)).verdict=="READY_BUT_RUNTIME_AUTHORITY_DISABLED"
    assert evaluate_resolved_external_action(packet,authority=_Resolver().resolve_current(packet)).verdict=="READY_FOR_PROVIDER_EXECUTION"


def test_direct_marketing_requires_fresh_consent_and_opt_out() -> None:
    h=canonical_content_sha256(destination="x@example.com",subject="x",body="x")
    packet=build_external_action_packet(action_id="m-1",action_class="EMAIL_SEND",purpose_class="DIRECT_MARKETING",destination="x@example.com",channel="email",environment="production",artifact_ref="runtime://m1",content_sha256=h,
        identity_or_relationship_ref="evidence://identity/x",consent_or_channel_eligibility_ref="",suppression_check_ref="evidence://suppression/x",suppression_clear=True,
        claim_evidence_refs=["evidence://claims/x"],sender_identity_ref="policy://sender",opt_out_mechanism_ref="",exact_scope="one-email",expires_at=_ts(30),provider="gmail_api",idempotency_key="m1")
    d=evaluate_resolved_external_action(packet,authority=_Resolver().resolve_current(packet))
    assert "DIRECT_MARKETING_CONSENT_NOT_PROVEN_FRESH" in d.reasons and "DIRECT_MARKETING_OPT_OUT_NOT_PROVEN_FRESH" in d.reasons


def test_founder_linkedin_is_manual_native() -> None:
    h=canonical_content_sha256(destination="linkedin-profile",subject="manual",body="manual")
    packet=build_external_action_packet(action_id="li-1",action_class="FOUNDER_LINKEDIN_MANUAL",purpose_class="REQUESTED_FOLLOWUP",destination="linkedin-profile",channel="founder_linkedin",environment="production",artifact_ref="runtime://li1",content_sha256=h,
        suppression_check_ref="evidence://suppression/li",suppression_clear=True,claim_evidence_refs=["evidence://claims/li"],sender_identity_ref="policy://founder",exact_scope="manual-native",expires_at=_ts(30),provider="manual_native",idempotency_key="li1")
    assert evaluate_resolved_external_action(packet,authority=_Resolver().resolve_current(packet)).verdict=="MANUAL_NATIVE_ONLY"


def test_tavily_is_fail_closed_without_explicit_enablement() -> None:
    result=TavilyReadOnlyAdapter(api_key="secret",enabled=False).execute(endpoint="search",payload={"query":"Saudi B2B AI"},request_id="r1")
    assert result.receipt.status=="BLOCKED_NOT_EXPLICITLY_ENABLED" and result.receipt.authority==AUTHORITY and result.payload is None


def test_tavily_mock_result_preserves_all_false_authority_and_sources() -> None:
    def handler(request:httpx.Request)->httpx.Response:
        assert request.headers["Authorization"]=="Bearer secret"; return httpx.Response(200,json={"results":[{"url":"https://example.com/a","content":"x"}]})
    result=TavilyReadOnlyAdapter(api_key="secret",enabled=True,transport=httpx.MockTransport(handler)).execute(endpoint="search",payload={"query":"q"},request_id="r2")
    assert result.receipt.source_refs==["https://example.com/a"] and result.receipt.authority["relationship"] is False and result.receipt.authority["external_send"] is False


def test_conversation_router_maps_objection_to_negotiation_without_send() -> None:
    class FakeEngine:
        def handle_objection(self,category,context=None,lang="both"): return {"category":category,"authority":{"execution_allowed":False},"context":context}
    plan=plan_conversation_turn("too expensive",evidence_refs=["email://thread/1#msg2"],route_result={"category":"OBJECTION","route":"objection_handling","suppress":False},objection_category="price",negotiation_engine=FakeEngine())
    assert plan.proposed_action=="prepare_negotiation" and plan.external_effect_allowed is False


def test_unsubscribe_is_suppression_not_sales_opportunity() -> None:
    plan=plan_conversation_turn("unsubscribe",evidence_refs=["email://thread/1#msg3"],route_result={"category":"UNSUBSCRIBE","route":"suppress_immediately","suppress":True})
    assert plan.suppress is True and plan.stage=="SUPPRESSED"


def test_gmail_provider_public_surface_is_quarantined() -> None:
    artifact=GmailArtifact(to="buyer@example.com",subject="Dealix follow-up",body_text="Requested diagnostic follow-up"); packet=_packet(body=artifact.body_text)
    with pytest.raises(PermissionError,match="CANONICAL_PROVIDER_DEPENDENCIES_NOT_WIRED"):
        send_approved_gmail_message(artifact,packet=packet)


def test_idempotency_same_committed_action_replays_receipt_without_new_reservation(tmp_path) -> None:
    packet=_packet(); ledger=SqliteIdempotencyLedger(tmp_path/"idempotency.sqlite")
    assert ledger.reserve(idempotency_key=packet.idempotency_key,action_hash=packet.action_hash,packet_integrity_sha256=packet.packet_integrity_sha256).status=="RESERVED_NEW"
    receipt={"provider":"gmail_api","provider_message_id":"msg-1","status":"PROVIDER_ACCEPTED_SEND_REQUEST"}
    ledger.commit(idempotency_key=packet.idempotency_key,action_hash=packet.action_hash,packet_integrity_sha256=packet.packet_integrity_sha256,receipt=receipt)
    replay=ledger.reserve(idempotency_key=packet.idempotency_key,action_hash=packet.action_hash,packet_integrity_sha256=packet.packet_integrity_sha256)
    assert replay.status=="REPLAY_COMMITTED" and replay.receipt==receipt


def test_idempotency_same_key_different_action_is_conflict(tmp_path) -> None:
    one=_packet(idempotency_key="same-key"); two=_packet(destination="other@example.com",idempotency_key="same-key"); ledger=SqliteIdempotencyLedger(tmp_path/"idempotency.sqlite")
    assert ledger.reserve(idempotency_key=one.idempotency_key,action_hash=one.action_hash,packet_integrity_sha256=one.packet_integrity_sha256).status=="RESERVED_NEW"
    assert ledger.reserve(idempotency_key=two.idempotency_key,action_hash=two.action_hash,packet_integrity_sha256=two.packet_integrity_sha256).status=="CONFLICT"


def test_idempotency_unknown_requires_reconciliation_not_retry(tmp_path) -> None:
    packet=_packet(); ledger=SqliteIdempotencyLedger(tmp_path/"idempotency.sqlite")
    assert ledger.reserve(idempotency_key=packet.idempotency_key,action_hash=packet.action_hash,packet_integrity_sha256=packet.packet_integrity_sha256).status=="RESERVED_NEW"
    ledger.mark_unknown(idempotency_key=packet.idempotency_key,action_hash=packet.action_hash,packet_integrity_sha256=packet.packet_integrity_sha256)
    again=ledger.reserve(idempotency_key=packet.idempotency_key,action_hash=packet.action_hash,packet_integrity_sha256=packet.packet_integrity_sha256)
    assert again.status=="IN_FLIGHT_OR_UNKNOWN" and again.state=="UNKNOWN"


def test_gmail_provider_refuses_content_drift_before_quarantine() -> None:
    artifact=GmailArtifact(to="buyer@example.com",subject="Dealix follow-up",body_text="CHANGED"); packet=_packet(body="original")
    with pytest.raises(PermissionError,match="message content changed"):
        send_approved_gmail_message(artifact,packet=packet)


def test_caller_time_overrides_cannot_make_stale_authority_fresh() -> None:
    packet = _packet()
    fresh = _Resolver().resolve_current(packet)
    stale = fresh.model_copy(
        update={
            "resolved_at": _ts(-2),
            "approval": fresh.approval.model_copy(update={"state_checked_at": _ts(-2)}),
        }
    )
    decision = evaluate_resolved_external_action(
        packet,
        authority=stale,
        evaluated_at=_ts(-120),
        max_authority_age_seconds=999999,
    )
    assert "CANONICAL_AUTHORITY_STALE" in decision.reasons
    assert "APPROVAL_STATE_STALE" in decision.reasons
    assert decision.provider_execution_allowed is False
