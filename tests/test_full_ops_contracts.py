"""Phase 1 — canonical Full-Ops contracts validation.

Asserts:
- Every schema is Pydantic v2 with extra='forbid'
- customer_handle required where external-facing
- safety_summary present on cross-layer envelopes
- ServiceSession transitions match the truth table
- CaseStudyCandidate.is_publishable() enforces consent+redaction+approval
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_client_acquisition.full_ops_contracts.schemas import (
    SESSION_TRANSITIONS,
    ApprovalRequestEnriched,
    CaseStudyCandidate,
    CustomerBrainSnapshot,
    CustomerHandle,
    CustomerPortalView,
    ExecutivePackRecord,
    LeadOpsRecord,
    PaymentStateRecord,
    ProofEventEnriched,
    ServiceSessionRecord,
    SupportTicketEnriched,
)


# ── CustomerHandle ────────────────────────────────────────────
def test_customer_handle_accepts_valid() -> None:
    h = CustomerHandle(handle="acme-real-estate")
    assert h.handle == "acme-real-estate"


def test_customer_handle_rejects_invalid_chars() -> None:
    with pytest.raises(ValidationError):
        CustomerHandle(handle="contains spaces")
    with pytest.raises(ValidationError):
        CustomerHandle(handle="has/slash")
    with pytest.raises(ValidationError):
        CustomerHandle(handle="-starts-with-hyphen")


def test_customer_handle_rejects_too_long() -> None:
    with pytest.raises(ValidationError):
        CustomerHandle(handle="a" * 65)


# ── extra='forbid' on every schema ────────────────────────────
def test_all_schemas_forbid_extra() -> None:
    schemas = [
        (LeadOpsRecord, {"leadops_id": "L1", "source": "form"}),
        (CustomerBrainSnapshot, {"customer_handle": "acme"}),
        (ServiceSessionRecord, {"session_id": "S1", "customer_handle": "acme", "service_type": "diagnostic"}),
        (ApprovalRequestEnriched, {"approval_id": "A1"}),
        (PaymentStateRecord, {"payment_id": "P1", "customer_handle": "acme", "amount_sar": 5000.0, "method": "bank_transfer"}),
        (SupportTicketEnriched, {"ticket_id": "T1", "customer_handle": "acme", "category": "refund", "priority": "p0"}),
        (ProofEventEnriched, {"proof_event_id": "E1", "customer_handle": "acme", "event_type": "DELIVERY_TASK_COMPLETED"}),
        (ExecutivePackRecord, {"pack_id": "X1", "customer_handle": "acme", "cadence": "daily"}),
        (CustomerPortalView, {"customer_handle": "acme"}),
        (CaseStudyCandidate, {"candidate_id": "C1", "customer_handle": "acme", "proof_event_ids": ["E1"]}),
    ]
    for model, payload in schemas:
        with pytest.raises(ValidationError):
            model(**{**payload, "this_field_does_not_exist": "X"})


# ── customer_handle required in external-facing schemas ────────
def test_customer_handle_required_external_facing() -> None:
    """Schemas that go to customers MUST have customer_handle."""
    with pytest.raises(ValidationError):
        ServiceSessionRecord(session_id="S1", service_type="diagnostic")
    with pytest.raises(ValidationError):
        PaymentStateRecord(payment_id="P1", amount_sar=5000.0, method="bank_transfer")
    with pytest.raises(ValidationError):
        SupportTicketEnriched(ticket_id="T1", category="refund", priority="p0")
    with pytest.raises(ValidationError):
        ExecutivePackRecord(pack_id="X1", cadence="daily")


# ── safety_summary present everywhere external ─────────────────
def test_safety_summary_defaults() -> None:
    lead = LeadOpsRecord(leadops_id="L1", source="form")
    assert lead.safety_summary == "approval_required_for_external_actions"

    sess = ServiceSessionRecord(session_id="S1", customer_handle="acme", service_type="diagnostic")
    assert "no_live_send" in sess.safety_summary

    pay = PaymentStateRecord(payment_id="P1", customer_handle="acme", amount_sar=5000.0, method="bank_transfer")
    assert "no_live_charge" in pay.safety_summary
    assert "no_fake_revenue" in pay.safety_summary

    proof = ProofEventEnriched(proof_event_id="E1", customer_handle="acme", event_type="DELIVERY_TASK_COMPLETED")
    assert "pii_redacted" in proof.safety_summary

    portal = CustomerPortalView(customer_handle="acme")
    assert "no_internal_terms" in portal.safety_summary
    assert "8_section_invariant" in portal.safety_summary


# ── ServiceSession transitions match truth table ──────────────
def test_session_transitions_truth_table() -> None:
    assert "waiting_for_approval" in SESSION_TRANSITIONS["draft"]
    assert "active" in SESSION_TRANSITIONS["waiting_for_approval"]
    assert "delivered" in SESSION_TRANSITIONS["active"]
    assert "complete" in SESSION_TRANSITIONS["proof_pending"]
    # Terminal states
    assert SESSION_TRANSITIONS["complete"] == set()
    assert SESSION_TRANSITIONS["blocked"] == set()
    # Cannot go backwards
    assert "draft" not in SESSION_TRANSITIONS["active"]


# ── CaseStudyCandidate publishability gate ────────────────────
def test_case_study_not_publishable_without_consent() -> None:
    c = CaseStudyCandidate(candidate_id="C1", customer_handle="acme", proof_event_ids=["E1"])
    assert not c.is_publishable()


def test_case_study_not_publishable_consent_only() -> None:
    c = CaseStudyCandidate(
        candidate_id="C1", customer_handle="acme", proof_event_ids=["E1"],
        consent_status="signed", consent_signature_id="sig_1",
    )
    # missing redaction + approval
    assert not c.is_publishable()


def test_case_study_publishable_when_all_gates_pass() -> None:
    c = CaseStudyCandidate(
        candidate_id="C1", customer_handle="acme", proof_event_ids=["E1"],
        consent_status="signed", consent_signature_id="sig_1",
        redaction_status="complete",
        approval_status="approved",
    )
    assert c.is_publishable()


def test_case_study_requires_at_least_one_proof_event() -> None:
    with pytest.raises(ValidationError):
        CaseStudyCandidate(candidate_id="C1", customer_handle="acme", proof_event_ids=[])


# ── PaymentState revenue invariant ────────────────────────────
def test_payment_state_intent_is_not_revenue() -> None:
    """Per Article 8 / NO_FAKE_REVENUE: invoice_intent ≠ revenue."""
    pay = PaymentStateRecord(
        payment_id="P1", customer_handle="acme",
        amount_sar=5000.0, method="bank_transfer",
    )
    # Default status is invoice_intent
    assert pay.status == "invoice_intent"
    assert pay.confirmed_at is None
    assert pay.confirmed_by is None


def test_payment_state_amount_capped() -> None:
    with pytest.raises(ValidationError):
        PaymentStateRecord(
            payment_id="P1", customer_handle="acme",
            amount_sar=2_000_000.0, method="bank_transfer",
        )
    with pytest.raises(ValidationError):
        PaymentStateRecord(
            payment_id="P1", customer_handle="acme",
            amount_sar=-1.0, method="bank_transfer",
        )
