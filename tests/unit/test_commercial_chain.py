"""Unit tests for dealix.commercial chain modules.

Covers: DiagnosticEngine, WarmIntroGenerator, PilotDeliveryKit,
ProofBuilder, UpsellEngine, CaseStudyGenerator, payment_link.
No network, no LLM, no DB — pure logic tests.
"""

from __future__ import annotations

import pytest

from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest
from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest
from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest
from dealix.commercial.proof_builder import (
    ProofBuildRequest,
    ProofBuilder,
    ProofEvent,
)
from dealix.commercial.upsell_engine import UpsellEngine
from dealix.commercial.case_study_generator import (
    CaseStudyGenerator,
    CaseStudyRequest,
)
from dealix.payments.payment_link import SERVICE_TIERS, PaymentLinkRequest


# ── DiagnosticEngine ────────────────────────────────────────────────────────

def test_diagnostic_generates_10_sections():
    req = DiagnosticRequest(company_name="اختبار", sector="b2b_services")
    result = DiagnosticEngine().generate(req)
    assert len(result.sections) == 10


def test_diagnostic_sections_have_ar_and_en():
    req = DiagnosticRequest(company_name="Test Co", sector="retail")
    result = DiagnosticEngine().generate(req)
    for section in result.sections:
        assert section.title_ar
        assert section.title_en


def test_diagnostic_to_markdown_returns_string():
    req = DiagnosticRequest(company_name="Test Co", sector="b2b_services")
    result = DiagnosticEngine().generate(req)
    assert isinstance(result.markdown_ar_en, str)
    assert "Test Co" in result.markdown_ar_en


def test_diagnostic_report_has_id():
    req = DiagnosticRequest(company_name="Biz", sector="fintech")
    result = DiagnosticEngine().generate(req)
    assert result.report_id


# ── WarmIntroGenerator ──────────────────────────────────────────────────────

def test_warm_intro_approval_required():
    req = WarmIntroRequest(
        prospect_name="أحمد", company_name="شركة X", sector="b2b_services"
    )
    result = WarmIntroGenerator().generate(req)
    assert result.approval_status == "approval_required"


def test_warm_intro_not_sent():
    req = WarmIntroRequest(
        prospect_name="محمد", company_name="شركة Y", sector="fintech"
    )
    result = WarmIntroGenerator().generate(req)
    # _NO_LIVE_SEND means nothing is auto-sent — bundle exists but is draft only
    assert result.bundle_id


def test_warm_intro_has_whatsapp_and_email():
    req = WarmIntroRequest(
        prospect_name="سارة", company_name="شركة Z", sector="retail"
    )
    result = WarmIntroGenerator().generate(req)
    assert len(result.whatsapp_drafts) >= 1
    assert len(result.email_drafts) >= 1


# ── PilotDeliveryKit ────────────────────────────────────────────────────────

def test_pilot_generates_7_day_plan():
    req = PilotStartRequest(
        account_id="acc-001",
        company_name="Pilot Co",
        sector="b2b_services",
    )
    kit = PilotDeliveryKit().create_pilot_plan(req)
    assert len(kit.day_plans) == 7


def test_pilot_approval_required():
    req = PilotStartRequest(
        account_id="acc-002",
        company_name="Pilot Co 2",
        sector="fintech",
    )
    kit = PilotDeliveryKit().create_pilot_plan(req)
    assert kit.approval_status == "approval_required"


def test_pilot_has_upsell_script():
    req = PilotStartRequest(
        account_id="acc-003",
        company_name="Pilot Co 3",
    )
    kit = PilotDeliveryKit().create_pilot_plan(req)
    assert kit.upsell_script


# ── ProofBuilder ────────────────────────────────────────────────────────────

def test_proof_builder_l0_with_zero_events():
    req = ProofBuildRequest(
        account_id="acc-001",
        company_name="Test",
        events=[],
    )
    pack = ProofBuilder().build(req)
    assert pack.proof_level == "L0"


def test_proof_builder_event_with_descriptions():
    event = ProofEvent(
        event_type="meeting_completed",
        description_ar="اجتماع أولي",
        description_en="Initial meeting",
    )
    req = ProofBuildRequest(
        account_id="acc-001",
        company_name="Test",
        events=[event],
    )
    pack = ProofBuilder().build(req)
    assert pack.event_count == 1


def test_proof_builder_approval_required():
    req = ProofBuildRequest(
        account_id="acc-002",
        company_name="Test",
    )
    pack = ProofBuilder().build(req)
    assert pack.approval_status == "approval_required"


# ── UpsellEngine ────────────────────────────────────────────────────────────

def test_upsell_not_eligible_with_zero_events():
    result = UpsellEngine().check(
        account_id="acc-001",
        company_name="Test",
        proof_event_count=0,
        proof_level="L0",
    )
    assert not result.is_eligible


def test_upsell_eligible_with_3_l1_events():
    result = UpsellEngine().check(
        account_id="acc-001",
        company_name="Test",
        proof_event_count=3,
        proof_level="L1",
    )
    assert result.is_eligible
    assert result.recommended_tier
    assert result.approval_status == "approval_required"


def test_upsell_tier_escalates_with_l3():
    result = UpsellEngine().check(
        account_id="acc-001",
        company_name="Big Corp",
        proof_event_count=5,
        proof_level="L3",
        monthly_revenue_sar=200_000,
    )
    assert result.recommended_tier == "executive_5k_25k"


def test_upsell_reason_bilingual():
    result = UpsellEngine().check(
        account_id="acc-001",
        company_name="Test",
        proof_event_count=0,
        proof_level="L0",
    )
    assert result.reason_ar
    assert result.reason_en


# ── CaseStudyGenerator ──────────────────────────────────────────────────────

def test_case_study_blocks_quote_without_consent():
    req = CaseStudyRequest(
        account_id="acc-001",
        company_name="Consent Co",
        sector="b2b_services",
        customer_consent=False,
        customer_quote_ar="هذا رائع",
    )
    with pytest.raises(AssertionError):
        CaseStudyGenerator().generate(req)


def test_case_study_generates_without_quote():
    req = CaseStudyRequest(
        account_id="acc-001",
        company_name="Consent Co",
        sector="b2b_services",
        customer_consent=False,
    )
    result = CaseStudyGenerator().generate(req)
    assert result.approval_status == "approval_required"


def test_case_study_generates_with_consent_and_quote():
    req = CaseStudyRequest(
        account_id="acc-001",
        company_name="Happy Client",
        sector="b2b_services",
        customer_consent=True,
        customer_quote_ar="نتائج رائعة",
        customer_quote_en="Amazing results",
    )
    result = CaseStudyGenerator().generate(req)
    assert result.study_id
    assert result.approval_status == "approval_required"


# ── Payment link ────────────────────────────────────────────────────────────

def test_service_tiers_defined():
    assert "sprint_499" in SERVICE_TIERS
    assert SERVICE_TIERS["sprint_499"]["amount_sar"] == 499


def test_service_tiers_has_managed_ops():
    assert "managed_ops_2999" in SERVICE_TIERS


def test_payment_link_request_validates():
    req = PaymentLinkRequest(
        service_tier="sprint_499",
        customer_name="أحمد",
        customer_email="test@example.com",
    )
    assert req.service_tier == "sprint_499"
