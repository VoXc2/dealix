"""CRM v10 — typed object model + scoring + state machine tests.

Hard-rule guards: no real customer name (use Acme-Saudi-Pilot-EXAMPLE),
no PII fields, no marketing claims, deterministic scoring.
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.main import create_app
from auto_client_acquisition.crm_v10 import (
    Account, ApprovalRequestRef, Campaign, Contact, CustomerHealth, Deal,
    InvalidStageTransition, InvoiceIntent, Lead, ManualPaymentRecord,
    Opportunity, Partner, ProofEventRef, Proposal, ServiceSession,
    SupportTicket, advance_deal, advance_lead, build_timeline,
    compute_health, get_object_schema, list_object_types, score_deal,
    score_lead,
)

CUST = "Acme-Saudi-Pilot-EXAMPLE"


def _account(**kw) -> Account:
    return Account(**{
        "id": "acct_001", "name": CUST, "sector": "b2b_services",
        "region": "riyadh", "tier": "growth_starter", **kw,
    })


def _lead(**kw) -> Lead:
    return Lead(**{
        "id": "lead_001", "account_id": "acct_001",
        "source": "warm_intro", **kw,
    })


def _deal(**kw) -> Deal:
    return Deal(**{
        "id": "deal_001", "account_id": "acct_001", "lead_id": "lead_001",
        "stage": "pilot_offered", "amount_sar": 499.0, **kw,
    })


# ---- Object model registry ----

def test_all_14_object_types_defined_and_importable():
    types = (
        Account, Contact, Lead, Deal, Opportunity, ServiceSession,
        ProofEventRef, Partner, SupportTicket, Campaign, Proposal,
        InvoiceIntent, ManualPaymentRecord, ApprovalRequestRef,
    )
    assert len(types) == 14
    for t in types:
        assert getattr(t, "model_config", {}).get("extra") == "forbid"


def test_list_object_types_returns_14_canonical_names():
    names = list_object_types()
    assert len(names) == 14
    for n in ("Account", "Contact", "Lead", "Deal", "ApprovalRequestRef"):
        assert n in names
    # CustomerHealth is derived, not registered.
    assert "CustomerHealth" not in names


def test_get_object_schema_account_returns_valid_jsonschema():
    schema = get_object_schema("Account")
    assert schema.get("type") == "object"
    assert "id" in schema.get("properties", {})
    assert "customer_health_score" in schema.get("properties", {})
    assert schema.get("additionalProperties") is False


def test_get_object_schema_unknown_raises_keyerror():
    with pytest.raises(KeyError):
        get_object_schema("NotARealObject")


def test_lead_model_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        Lead(id="x", account_id="a", source="warm_intro", unknown_field="boom")


def test_no_pii_fields_on_contact():
    fields = set(Contact.model_fields.keys())
    assert "email" not in fields and "phone" not in fields
    assert "phone_number" not in fields
    assert "full_name_redacted_handle" in fields


# ---- Scoring ----

def test_score_lead_is_deterministic_for_same_inputs():
    assert score_lead(_lead(), _account()) == score_lead(_lead(), _account())


def test_score_lead_warm_intro_bonus_present():
    warm = score_lead(_lead(source="warm_intro"), _account())
    inbound = score_lead(_lead(source="inbound"), _account())
    assert warm["fit_score"] > inbound["fit_score"]
    assert any("warm_intro" in r for r in warm["reasons"])


def test_score_lead_urgency_token_arabic_or_english():
    s_ar = score_lead(_lead(notes="عاجل follow up"), _account())
    s_en = score_lead(_lead(notes="please reply, urgent"), _account())
    s_no = score_lead(_lead(notes="kind regards"), _account())
    assert s_ar["urgency_score"] >= 0.5 and s_en["urgency_score"] >= 0.5
    assert s_no["urgency_score"] == 0.0


def test_score_lead_clamps_to_0_1_and_redacts_notes():
    out = score_lead(
        _lead(notes="ping me at user@example.com or +966555000111 urgent"),
        _account(),
    )
    assert 0.0 <= out["fit_score"] <= 1.0
    assert 0.0 <= out["urgency_score"] <= 1.0
    assert "[redacted]" in out["notes_redacted"]


def test_score_deal_returns_required_keys():
    out = score_deal(_deal(), _account(customer_health_score=0.6), 3)
    assert {"win_probability", "days_in_stage", "risk_flags"} <= out.keys()
    assert 0.0 <= out["win_probability"] <= 1.0


# ---- Stage machine ----

def test_advance_lead_new_to_qualifying_allowed():
    assert advance_lead(_lead(stage="new"), "qualifying").stage == "qualifying"


def test_advance_lead_new_to_won_invalid():
    with pytest.raises(InvalidStageTransition):
        advance_lead(_lead(stage="new"), "won")


def test_advance_deal_pilot_offered_to_payment_pending_allowed():
    out = advance_deal(_deal(stage="pilot_offered"), "payment_pending")
    assert out.stage == "payment_pending"


def test_advance_deal_payment_pending_to_won_invalid_must_pay_first():
    deal = _deal(stage="payment_pending")
    with pytest.raises(InvalidStageTransition):
        advance_deal(deal, "won")
    after = advance_deal(advance_deal(advance_deal(
        deal, "paid_or_committed"), "in_delivery"), "won")
    assert after.stage == "won"


# ---- Customer health + timeline ----

def test_compute_health_returns_health_with_score_in_0_1():
    health = compute_health(
        _account(),
        deals=[_deal(stage="won")],
        service_sessions=[ServiceSession(
            id="ss1", account_id="acct_001", service_id="svc_pilot",
            status="completed",
        )],
        proof_events=[ProofEventRef(
            id="p1", account_id="acct_001", event_type="pilot_kickoff",
            redacted_summary="kickoff completed",
        )],
        support_tickets=[],
    )
    assert isinstance(health, CustomerHealth)
    assert 0.0 <= health.score <= 1.0
    for k in ("delivery_consistency", "support_load", "recent_proof"):
        assert k in health.factors


def test_build_timeline_chronologically_ordered_and_pii_free():
    t0 = datetime(2026, 1, 1, tzinfo=UTC)
    t1 = datetime(2026, 2, 1, tzinfo=UTC)
    t2 = datetime(2026, 3, 1, tzinfo=UTC)
    leads = [
        _lead(id="L1", created_at=t1),
        _lead(id="L_other", account_id="acct_999", created_at=t0),
    ]
    sessions = [ServiceSession(
        id="S1", account_id="acct_001", service_id="svc_pilot",
        status="in_progress", started_at=t2,
    )]
    proofs = [ProofEventRef(
        id="P1", account_id="acct_001", event_type="proof_signed",
        redacted_summary="ok", created_at=t0,
    )]
    tl = build_timeline("acct_001", leads, [], sessions, proofs)
    assert all(ev["id"] != "L_other" for ev in tl)
    assert [ev["id"] for ev in tl] == ["P1", "L1", "S1"]
    for ev in tl:
        for k in ev.keys():
            assert "email" not in k and "phone" not in k


# ---- Router ----

def test_router_status_advertises_canonical_guardrails():
    resp = TestClient(create_app()).get("/api/v1/crm-v10/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "crm_v10"
    g = body["guardrails"]
    for k in (
        "no_llm_calls", "no_external_http", "no_database",
        "approval_required", "deterministic_scoring", "no_pii_fields",
    ):
        assert g[k] is True
    assert body["object_type_count"] == 14


def test_router_object_types_lists_14_names():
    resp = TestClient(create_app()).get("/api/v1/crm-v10/object-types")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 14 and len(body["names"]) == 14


def test_router_schema_returns_all_object_schemas():
    resp = TestClient(create_app()).get("/api/v1/crm-v10/schema")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 14
    assert body["schemas"]["Account"]["additionalProperties"] is False


def test_router_post_score_lead_with_valid_body_returns_200():
    resp = TestClient(create_app()).post(
        "/api/v1/crm-v10/score-lead",
        json={
            "lead": _lead().model_dump(mode="json"),
            "account": _account().model_dump(mode="json"),
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "fit_score" in body and "urgency_score" in body


def test_router_post_score_lead_with_unknown_field_returns_422():
    resp = TestClient(create_app()).post(
        "/api/v1/crm-v10/score-lead",
        json={
            "lead": _lead().model_dump(mode="json"),
            "account": _account().model_dump(mode="json"),
            "unknown_field": "boom",
        },
    )
    assert resp.status_code == 422


def test_router_post_lead_advance_invalid_returns_400():
    resp = TestClient(create_app()).post(
        "/api/v1/crm-v10/lead/advance",
        json={
            "lead": _lead(stage="new").model_dump(mode="json"),
            "target_stage": "won",
        },
    )
    assert resp.status_code == 400


def test_router_post_deal_advance_valid_returns_200():
    resp = TestClient(create_app()).post(
        "/api/v1/crm-v10/deal/advance",
        json={
            "deal": _deal(stage="pilot_offered").model_dump(mode="json"),
            "target_stage": "payment_pending",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["stage"] == "payment_pending"


def test_router_post_customer_health_returns_score_in_0_1():
    resp = TestClient(create_app()).post(
        "/api/v1/crm-v10/customer-health",
        json={
            "account": _account().model_dump(mode="json"),
            "deals": [], "service_sessions": [],
            "proof_events": [], "support_tickets": [],
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert 0.0 <= body["score"] <= 1.0
    assert isinstance(body["factors"], dict)


def test_no_marketing_claims_in_module_outputs():
    a = _account(notes="urgent pilot kickoff").model_dump_json()
    forbidden = ("نضمن", "guaranteed", "blast", "scrape")
    for term in forbidden:
        if term.isascii():
            assert term not in a.lower()
        else:
            assert term not in a


def test_no_real_customer_name_in_test_fixture():
    assert "EXAMPLE" in _account().name
