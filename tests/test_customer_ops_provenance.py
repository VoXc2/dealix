"""Provenance follow-up: frozen snapshot + relationship refs on existing contracts.

L0-L4 only. No live send, no execution, no new store.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.customer_ops import (
    CustomerOpsEvent,
    build_provenance_attachment,
    run_customer_ops_event,
)
from auto_client_acquisition.customer_ops.provenance import (
    PROVENANCE_KEY,
    assert_no_raw_payload,
    attach_provenance_to_approval,
    attach_provenance_to_proof_event,
    case_evidence_ids,
    new_approval_request_for_outcome,
    new_proof_event_for_outcome,
    require_current_provenance,
)


def _event(**over) -> CustomerOpsEvent:
    base: dict = {
        "account_id": "acct_001",
        "contact_id": "ct_001",
        "relationship_state": "prospect",
        "consent_state": "unknown",
        "channel": "web",
        "locale": "ar",
        "sector": "technology_saas",
        "intent": "diagnostic_question",
        "data_class": "internal",
        "priority": "p2",
        "effect_class": "draft",
        "allowed_tools": [
            "knowledge_v10.retrieve",
            "support_os.draft_response",
            "distribution_os.draft_quality",
            "approval_center.create",
        ],
        "owner": "customer_ops_kernel",
        "verifier": "founder",
        "response_state": "ask",
    }
    base.update(over)
    return CustomerOpsEvent(**base)


def _rel_evidence(source: str = "crm_record") -> list[dict]:
    return [
        {
            "source": source,
            "uri": "crm://acct_001",
            "excerpt": "SHOULD NEVER BE PERSISTED",
            "evidence_level": "L3",
            "retrieved_at": "2026-09-13T00:00:00+00:00",
            "current_only": True,
        }
    ]


def _snap(**over) -> dict:
    base = {
        "snapshot_id": "snap_abc123",
        "retrieved_at": "2026-09-13T00:00:00+00:00",
        "as_of": "2026-09-13T00:00:00+00:00",
        "chunk_ids": ["chunk_1", "chunk_2"],
        "source_types": ["internal_doc"],
        "current_only": True,
    }
    base.update(over)
    return base


def _knowledge_evidence() -> list[dict]:
    return [
        {
            "source": "internal_doc",
            "uri": "doc://kb/onboarding",
            "excerpt": "BODY MUST BE STRIPPED",
            "evidence_level": "L2",
            "retrieved_at": "2026-09-13T00:00:00+00:00",
            "current_only": True,
        }
    ]


# ── escalate / hold carry provenance ──────────────────────────────

def test_escalate_carries_frozen_provenance() -> None:
    out = run_customer_ops_event(
        _event(channel="web"), message_text="أبغى استرجاع فلوسي فورا"
    )
    assert out.response_state == "escalate"
    prov = out.to_dict()["provenance"]
    assert prov["snapshot"]["snapshot_id"]
    assert prov["snapshot"]["current_only"] is True
    assert "chunk_ids" in prov["snapshot"] and "as_of" in prov["snapshot"]
    # Empty backend -> missing evidence is honestly reported, not faked.
    assert prov["provenance_status"] == "missing"
    assert prov["has_current_evidence"] is False


def test_hold_carries_missing_provenance_without_body() -> None:
    secret = "api_key: sk-1234567890abcdef1234567890"
    out = run_customer_ops_event(_event(channel="web"), message_text=secret)
    assert out.response_state == "hold"
    prov = out.to_dict()["provenance"]
    assert prov["provenance_status"] == "missing"
    blob = repr(prov)
    assert "sk-1234567890" not in blob
    assert secret not in blob


def test_action_draft_carries_current_provenance(monkeypatch) -> None:
    import auto_client_acquisition.customer_ops.pipeline as pipe

    from auto_client_acquisition.customer_ops.retrieval import KnowledgeSnapshot

    snap = KnowledgeSnapshot(
        snapshot_id="snap_live01",
        retrieved_at="2026-09-13T00:00:00+00:00",
        as_of="2026-09-13T00:00:00+00:00",
        chunk_ids=("chunk_a",),
        source_types=("internal_doc",),
        current_only=True,
    )
    monkeypatch.setattr(
        pipe, "current_only_retrieve", lambda **kw: (snap, "answer", _knowledge_evidence())
    )
    ev = _event(
        effect_class="approved_send_manual",
        allowed_tools=["approval_center.create", "channel_policy_gateway.check"],
        response_state="ask",
    )
    out = run_customer_ops_event(ev, message_text="أحتاج مساعدة في الإعداد")
    assert out.response_state == "action_draft"
    prov = out.to_dict()["provenance"]
    assert prov["provenance_status"] == "current"
    assert prov["has_current_evidence"] is True
    assert prov["snapshot"]["snapshot_id"] == "snap_live01"
    assert prov["snapshot"]["chunk_ids"] == ["chunk_a"]


# ── approval / proof / case attachment ────────────────────────────

def test_approval_builder_attaches_provenance_without_executing() -> None:
    out = run_customer_ops_event(
        _event(channel="web"), message_text="أبغى استرجاع فلوسي فورا"
    )
    req = new_approval_request_for_outcome(
        outcome=out, account_id="acct_001", channel="web"
    )
    assert req.provenance is not None
    assert req.provenance["snapshot"]["snapshot_id"]
    assert req.provenance["provenance_status"] in ("current", "missing", "stale")
    # Creation only: still pending, never executed.
    assert str(req.status) == "pending"
    assert req.action_mode in ("draft_only", "approval_required", "blocked")
    # No message body leaked into summaries or provenance.
    blob = repr(req.model_dump(mode="json"))
    assert "استرجاع" not in blob or "مسودة عملية عميل" in blob
    assert "sk-" not in blob


def test_proof_builder_refuses_missing_evidence() -> None:
    out = run_customer_ops_event(
        _event(channel="web"), message_text="أبغى استرجاع فلوسي فورا"
    )
    with pytest.raises(ValueError, match="ASK_OR_HOLD"):
        new_proof_event_for_outcome(outcome=out)


def test_proof_builder_binds_current_evidence_in_existing_payload() -> None:
    prov = build_provenance_attachment(
        snapshot_ref=_snap(),
        evidence=_knowledge_evidence(),
        trace_id="cop_t1",
        case_id="case_c1",
        response_state="action_draft",
    )
    outcome = {
        "intent": "diagnostic_question",
        "sector": "technology_saas",
        "case_id": "case_c1",
        "trace_id": "cop_t1",
        "response_state": "action_draft",
        "action_mode": "approval_required",
        "evidence": _knowledge_evidence(),
        "knowledge_snapshot": _snap(),
        "provenance": prov,
    }
    event = new_proof_event_for_outcome(outcome=outcome)
    assert event.approval_status == "approval_required"
    assert PROVENANCE_KEY in event.payload
    assert event.payload[PROVENANCE_KEY]["snapshot"]["snapshot_id"] == "snap_abc123"
    assert event.payload["knowledge_snapshot_id"] == "snap_abc123"
    assert "BODY MUST BE STRIPPED" not in repr(event.model_dump(mode="json"))


def test_stale_snapshot_refuses_proof() -> None:
    prov = build_provenance_attachment(
        snapshot_ref=_snap(current_only=False),
        evidence=_knowledge_evidence(),
        response_state="action_draft",
    )
    assert prov["provenance_status"] == "stale"
    with pytest.raises(ValueError, match="ASK_OR_HOLD"):
        require_current_provenance(prov)


def test_case_evidence_ids_are_refs_only() -> None:
    prov = build_provenance_attachment(
        snapshot_ref=_snap(),
        evidence=_knowledge_evidence() + _rel_evidence("crm_record"),
        trace_id="cop_t1",
        case_id="case_c1",
        response_state="action_draft",
    )
    ids = case_evidence_ids(prov)
    assert "snap_abc123" in ids
    assert "chunk_1" in ids
    assert "crm://acct_001" in ids
    assert not any("SHOULD NEVER" in i or "BODY" in i for i in ids)


# ── relationship / consent separation ────────────────────────────

def test_relationship_refs_never_grant_consent() -> None:
    prov = build_provenance_attachment(
        snapshot_ref=_snap(),
        evidence=_rel_evidence("crm_record"),
        response_state="escalate",
    )
    assert len(prov["relationship_refs"]) == 1
    ref = prov["relationship_refs"][0]
    assert ref["proves_relationship"] is True
    assert ref["grants_channel_consent"] is False
    assert "excerpt" not in ref


def test_public_sources_mint_no_relationship_refs() -> None:
    prov = build_provenance_attachment(
        snapshot_ref=_snap(),
        evidence=_rel_evidence("official_public_site"),
        response_state="ask",
    )
    assert prov["relationship_refs"] == []


def test_withdrawn_consent_keeps_relationship_ref_without_consent() -> None:
    ev = _event(
        relationship_state="customer",
        consent_state="withdrawn",
        channel="web",
        evidence=_rel_evidence("signed_contract"),
    )
    prov = build_provenance_attachment(
        snapshot_ref=_snap(),
        evidence=[e.model_dump(mode="json") for e in ev.evidence],
        trace_id=ev.trace_id,
        case_id=ev.case_id,
        response_state="hold",
    )
    assert len(prov["relationship_refs"]) == 1
    assert prov["relationship_refs"][0]["grants_channel_consent"] is False
    req = new_approval_request_for_outcome(
        outcome={
            "intent": "billing",
            "sector": "technology_saas",
            "case_id": ev.case_id,
            "trace_id": ev.trace_id,
            "response_state": "hold",
            "action_mode": "blocked",
            "evidence": [],
            "knowledge_snapshot": {},
            "provenance": prov,
        },
        account_id="acct_001",
        channel="web",
    )
    assert req.action_mode == "blocked"
    assert req.provenance["relationship_refs"][0]["grants_channel_consent"] is False


# ── no raw payload leakage + immutability ─────────────────────────

def test_forbidden_keys_rejected_fail_closed() -> None:
    with pytest.raises(ValueError, match="forbidden"):
        assert_no_raw_payload({"message_text": "hello"})
    with pytest.raises(ValueError, match="forbidden"):
        assert_no_raw_payload({"snapshot": {"prompt": "x"}})
    req = ApprovalRequest(
        object_type="customer_ops_outcome",
        object_id="case_x",
        action_type="support_reply_draft",
    )
    with pytest.raises(ValueError, match="forbidden"):
        attach_provenance_to_approval(req, {"message_body": "leak"})
    assert req.provenance is None


def test_provenance_immutable_after_approval_edit() -> None:
    from auto_client_acquisition.approval_center import approval_store

    store = approval_store.ApprovalStore()
    prov = build_provenance_attachment(
        snapshot_ref=_snap(snapshot_id="snap_frozen"),
        evidence=_knowledge_evidence(),
        response_state="action_draft",
    )
    req = ApprovalRequest(
        object_type="customer_ops_outcome",
        object_id="case_imm",
        action_type="support_reply_draft",
    )
    attach_provenance_to_approval(req, prov)
    stored = store.create(req)
    assert stored.provenance["snapshot"]["snapshot_id"] == "snap_frozen"
    edited = store.edit(stored.approval_id, "founder", {"summary_en": "revised"})
    assert edited.provenance["snapshot"]["snapshot_id"] == "snap_frozen"
    # provenance is not in the edit allow-list: patch attempts are ignored.
    edited2 = store.edit(
        stored.approval_id, "founder", {"provenance": {"snapshot": {}}}  # type: ignore[dict-item]
    )
    assert edited2.provenance["snapshot"]["snapshot_id"] == "snap_frozen"


def test_approval_provenance_field_backward_compatible() -> None:
    legacy = {
        "object_type": "customer_ops_outcome",
        "object_id": "case_legacy",
        "action_type": "support_reply_draft",
    }
    req = ApprovalRequest.model_validate(legacy)
    assert req.provenance is None
    dumped = req.model_dump(mode="json")
    assert ApprovalRequest.model_validate(dumped).provenance is None


def test_attach_does_not_execute_or_send() -> None:
    from auto_client_acquisition.approval_center import approval_store

    store = approval_store.ApprovalStore()
    prov = build_provenance_attachment(
        snapshot_ref=_snap(),
        evidence=_knowledge_evidence(),
        response_state="action_draft",
    )
    req = ApprovalRequest(
        object_type="customer_ops_outcome",
        object_id="case_noexec",
        action_type="support_reply_draft",
        action_mode="approval_required",
    )
    attach_provenance_to_approval(req, prov)
    stored = store.create(req)
    assert str(stored.status) == "pending"
    pending = [r.approval_id for r in store.list_pending()]
    assert stored.approval_id in pending


def test_proof_attach_rejects_stale_instead_of_fabricating() -> None:
    from auto_client_acquisition.proof_ledger.schemas import ProofEvent

    prov = build_provenance_attachment(
        snapshot_ref=_snap(chunk_ids=[]),
        evidence=[],
        response_state="ask",
    )
    assert prov["provenance_status"] == "missing"
    event = ProofEvent(
        event_type="diagnostic_delivered",
        summary_ar="x",
        summary_en="y",
    )
    with pytest.raises(ValueError, match="ASK_OR_HOLD"):
        attach_provenance_to_proof_event(event, prov)
    assert PROVENANCE_KEY not in (event.payload or {})
