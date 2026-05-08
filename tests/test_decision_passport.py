"""Tests for Decision Passport, evidence levels, and readiness bootstrap."""

from __future__ import annotations

from auto_client_acquisition.agents.intake import Lead, LeadSource, LeadStatus
from auto_client_acquisition.customer_readiness.scores import (
    compute_comfort_and_expansion,
    from_passport_meta,
)
from auto_client_acquisition.decision_passport.builder import build_from_pipeline_result
from auto_client_acquisition.pipeline import PipelineResult
from auto_client_acquisition.proof_engine.evidence import (
    EvidenceLevel,
    assert_public_proof_allowed,
)


def _minimal_pipeline_result() -> PipelineResult:
    lead = Lead(
        id="lead_test_1",
        source=LeadSource.WEBSITE,
        company_name="شركة اختبار",
        contact_name="أحمد",
        contact_email="a@test.sa",
        contact_phone="+966501234567",
        sector="technology",
        region="Saudi Arabia",
        budget=50_000.0,
        message="نحتاج نظام متابعة عملاء",
        locale="ar",
        status=LeadStatus.DISCOVERY,
        fit_score=0.77,
        urgency_score=0.3,
    )
    from auto_client_acquisition.agents.icp_matcher import FitScore
    from auto_client_acquisition.agents.qualification import QualificationResult

    fit = FitScore(
        overall_score=0.77,
        industry_match=1.0,
        size_match=0.4,
        region_match=1.0,
        budget_match=1.0,
        pain_match=0.3,
        reasons=["ICP match"],
        recommendations=["Qualify"],
    )
    qual = QualificationResult(
        budget_clarified=True,
        authority_confirmed=False,
        need_explicit=True,
        timeline_known=False,
        new_status=LeadStatus.DISCOVERY,
    )
    return PipelineResult(lead=lead, fit_score=fit, qualification=qual, warnings=[])


def test_build_passport_has_blocked_actions():
    p = build_from_pipeline_result(_minimal_pipeline_result())
    assert p.lead_id == "lead_test_1"
    assert "cold_whatsapp" in p.blocked_actions
    assert p.scores.fit_score == 0.77
    assert p.icp_tier == "B"
    assert p.priority_bucket in {"P0_NOW", "P1_THIS_WEEK", "P2_NURTURE", "P3_LOW_PRIORITY", "BLOCKED"}


def test_readiness_from_passport():
    p = build_from_pipeline_result(_minimal_pipeline_result())
    r = from_passport_meta(p.model_dump())
    assert "customer_comfort_score" in r
    assert "expansion_readiness_score" in r


def test_comfort_score_bounds():
    r = compute_comfort_and_expansion(
        has_status_timeline=True,
        has_next_action=True,
        pending_approvals=0,
    )
    assert 0 <= r["customer_comfort_score"] <= 100


def test_evidence_public_guard():
    assert_public_proof_allowed(int(EvidenceLevel.L4_PUBLIC_APPROVED), consent_public=True)
    try:
        assert_public_proof_allowed(int(EvidenceLevel.L2_CUSTOMER_REVIEWED), consent_public=True)
    except ValueError as e:
        assert "public_proof_requires" in str(e)
    else:
        raise AssertionError("expected ValueError below L4")

    try:
        assert_public_proof_allowed(int(EvidenceLevel.L4_PUBLIC_APPROVED), consent_public=False)
    except ValueError as e:
        assert "consent" in str(e)
    else:
        raise AssertionError("expected ValueError without consent")
