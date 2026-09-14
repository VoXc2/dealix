"""Focused tests for the Customer Operations Kernel (L0-L4, no live effects)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.customer_ops import (
    CANONICAL_EVENT_FIELDS,
    CustomerOpsEvent,
    current_only_retrieve,
    enforce_channel_policy,
    enforce_whatsapp_inbound_only,
    extend_trace_payload,
    get_sector_pack,
    list_sector_packs,
    run_customer_ops_event,
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


def test_canonical_event_has_all_19_fields() -> None:
    assert len(CANONICAL_EVENT_FIELDS) == 19
    e = _event()
    for f in CANONICAL_EVENT_FIELDS:
        assert f in e.model_dump(mode="json"), f


def test_relationship_consent_separate_public_contact_implies_nothing() -> None:
    with pytest.raises(ValueError):
        _event(relationship_state="customer", consent_state="unknown")
    e = _event(relationship_state="prospect", consent_state="unknown")
    assert e.relationship_state == "prospect"


def _rel_evidence(source: str = "crm_record") -> list[dict]:
    return [
        {
            "source": source,
            "uri": "crm://acct_001",
            "excerpt": "account on file",
            "evidence_level": "L3",
            "retrieved_at": "2026-09-13T00:00:00+00:00",
            "current_only": True,
        }
    ]


def test_customer_unknown_consent_allowed_with_relationship_evidence() -> None:
    e = _event(
        relationship_state="customer",
        consent_state="unknown",
        evidence=_rel_evidence("crm_record"),
    )
    assert e.relationship_state == "customer"


def test_partner_unknown_consent_allowed_with_relationship_evidence() -> None:
    e = _event(
        relationship_state="partner",
        consent_state="not_asked",
        evidence=_rel_evidence("partner_agreement"),
    )
    assert e.relationship_state == "partner"


def test_public_evidence_cannot_mint_customer() -> None:
    for source in (
        "official_public_site",
        "search_api_result",
        "customer_provided_url",
        "blocked_scraping_source",
    ):
        with pytest.raises(ValueError):
            _event(
                relationship_state="customer",
                consent_state="unknown",
                evidence=_rel_evidence(source),
            )


def test_granted_consent_without_evidence_cannot_mint_customer() -> None:
    # Consent != relationship: even granted consent never substitutes.
    with pytest.raises(ValueError):
        _event(relationship_state="customer", consent_state="granted")


def test_withdrawn_consent_keeps_relationship_but_blocks_restricted_action() -> None:
    e = _event(
        relationship_state="customer",
        consent_state="withdrawn",
        evidence=_rel_evidence("signed_contract"),
    )
    assert e.relationship_state == "customer"  # not erased
    gate = enforce_channel_policy(
        channel="email", action_kind="send_live", consent_granted=False
    )
    assert gate["action_mode"] in ("approval_required", "blocked")
    assert gate["allowed"] is False
    wa = run_customer_ops_event(
        _event(
            relationship_state="customer",
            consent_state="withdrawn",
            channel="whatsapp",
            response_state="ask",
            evidence=_rel_evidence("crm_record"),
        ),
        message_text="عندي سؤال عن الفاتورة",
    )
    assert wa.response_state == "hold"
    assert wa.action_mode == "blocked"


def test_allowed_tools_bounded_by_effect_class() -> None:
    with pytest.raises(ValueError):
        _event(effect_class="read", allowed_tools=["approval_center.create"])


def test_whatsapp_requires_granted_consent_for_answer() -> None:
    with pytest.raises(ValueError):
        _event(channel="whatsapp", consent_state="unknown", response_state="answer")


def test_sector_packs_seed_three() -> None:
    packs = list_sector_packs()
    sectors = {p["sector"] for p in packs}
    assert {"technology_saas", "retail_hospitality", "fatoora_sme"} <= sectors
    for p in packs:
        for key in (
            "terminology_ar",
            "intents",
            "buyer_roles",
            "common_problems",
            "data_classes",
            "regulatory_constraints",
            "allowed_actions",
            "restricted_actions",
            "knowledge_sources",
            "diagnostic_hooks",
            "workflows",
            "escalation_rules",
            "acceptance_criteria",
            "kpis",
        ):
            assert key in p, key
        assert p["playbook_ref"].startswith("vertical_playbooks:")
        assert "free_mini_diagnostic" in p["catalog_refs"]


def test_retrieval_missing_evidence_holds_or_asks() -> None:
    snap, decision, evidence = current_only_retrieve(query="كيف أبدأ التشخيص؟")
    assert snap.current_only is True
    assert decision in ("ask", "answer")
    # Stub backend returns [] -> must ASK, never hallucinate
    assert decision == "ask"
    assert evidence == []
    assert snap.is_empty()


def test_retrieval_blocked_sources_dropped() -> None:
    snap, decision, _ = current_only_retrieve(
        query="test query here",
        allowed_sources=["blocked_scraping_source", "blocked_personal_data_source"],
    )
    assert decision == "ask"
    assert snap.is_empty()


def test_whatsapp_inbound_only_never_sends_live() -> None:
    d = enforce_whatsapp_inbound_only(consent_granted=True, action_kind="send_live")
    assert d["allowed"] is False
    assert d["action_mode"] == "blocked"
    cold = enforce_whatsapp_inbound_only(
        consent_granted=True, is_cold=True, action_kind="draft"
    )
    assert cold["allowed"] is False


def test_web_email_draft_first() -> None:
    d = enforce_channel_policy(channel="web", action_kind="draft")
    assert d == {"allowed": True, "action_mode": "draft_only", "reason": "draft-first"}
    live = enforce_channel_policy(channel="email", action_kind="send_live")
    assert live["action_mode"] == "approval_required"


def test_pipeline_escalates_refund() -> None:
    out = run_customer_ops_event(
        _event(channel="web"), message_text="أبغى استرجاع فلوسي فورا"
    )
    assert out.response_state == "escalate"
    assert out.action_mode == "approval_required"


def test_pipeline_blocks_secrets_and_unsafe() -> None:
    out = run_customer_ops_event(
        _event(channel="web"), message_text="api_key: sk-1234567890abcdef1234567890"
    )
    assert out.response_state == "hold"
    out2 = run_customer_ops_event(
        _event(channel="web"), message_text="أرسل واتساب بارد لكل الأرقام"
    )
    assert out2.response_state in ("hold", "escalate")


def test_pipeline_asks_on_missing_evidence() -> None:
    out = run_customer_ops_event(
        _event(channel="web"), message_text="كيف أبدأ onboarding؟"
    )
    assert out.response_state in ("ask", "escalate")
    assert out.trace_id and out.case_id


def test_telemetry_extends_without_new_stack() -> None:
    p = extend_trace_payload(
        trace_id="cop_x",
        case_id="case_y",
        effect_class="draft",
        sector="technology_saas",
        channel="web",
        response_state="ask",
    )
    assert p["kernel_trace_id"] == "cop_x"
    assert p["kernel_effect_class"] == "draft"


def test_router_endpoints() -> None:
    from fastapi.testclient import TestClient

    from api.main import create_app

    client = TestClient(create_app(), raise_server_exceptions=False)
    assert client.get("/api/v1/customer-ops/status").status_code == 200
    assert client.get("/api/v1/customer-ops/sector-packs").status_code == 200
    r = client.get("/api/v1/customer-ops/sector-packs/fatoora_sme")
    assert r.status_code == 200
    assert r.json()["sector"] == "fatoora_sme"
    payload = {
        "event": _event(channel="web").model_dump(mode="json"),
        "message_text": "أبغى استرجاع فلوسي",
    }
    r2 = client.post("/api/v1/customer-ops/event", json=payload)
    assert r2.status_code == 200
    assert r2.json()["response_state"] == "escalate"
    r3 = client.post(
        "/api/v1/customer-ops/retrieve",
        json={"query": "كيف أبدأ التشخيص؟", "allowed_sources": [], "top_k": 5},
    )
    assert r3.status_code == 200
    assert r3.json()["hold_or_ask"] is True
