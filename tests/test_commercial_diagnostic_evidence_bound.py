"""Regression tests for the Dealix evidence-bound commercial diagnostic."""

from __future__ import annotations

from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest, UNKNOWN


def test_diagnostic_is_deterministic_and_non_committing() -> None:
    request = DiagnosticRequest(
        company_name="Example Co",
        sector="b2b_services",
        pain_points=["reporting"],
        evidence_refs=["evidence://process/1"],
        baseline_ref="baseline://1",
        source_context="Customer supplied process note.",
        customer_validation_ref="customer://validation/1",
    )
    first = DiagnosticEngine().generate(request)
    second = DiagnosticEngine().generate(request)

    assert first.report_id == second.report_id
    assert len(first.sections) == 10
    assert first.evidence_refs == ["evidence://process/1"]
    assert first.baseline_ref == "baseline://1"
    assert first.source_context_present is True
    assert first.customer_validation_ref == "customer://validation/1"
    assert first.customer_validation_status == "CUSTOMER_VALIDATED_WITH_REFERENCE"
    assert first.customer_value_claim is False
    assert first.guarantee is False
    assert first.payment_url_placeholder == ""
    assert first.approval_status == "approval_required"
    assert first.governance_decision == "pending"
    assert first.llm_used is False
    assert "499" not in first.markdown_ar_en
    assert "20-35%" not in first.markdown_ar_en
    assert "15,000" not in first.markdown_ar_en
    assert "+40%" not in first.markdown_ar_en
    assert UNKNOWN not in first.markdown_ar_en


def test_missing_evidence_stays_unknown() -> None:
    report = DiagnosticEngine().generate(DiagnosticRequest(company_name="Example Co"))

    assert UNKNOWN in report.unknowns
    assert "customer_approved_baseline" in report.unknowns
    assert "source_linked_evidence" in report.unknowns
    assert "customer_validated_business_impact" in report.unknowns
    assert report.customer_validation_ref == ""
    assert report.customer_validation_status == UNKNOWN
    assert report.customer_value_claim is False
    assert report.guarantee is False
    assert UNKNOWN in report.markdown_ar_en
    assert "does not establish revenue" in report.markdown_ar_en


def test_source_context_alone_never_becomes_customer_validation() -> None:
    report = DiagnosticEngine().generate(
        DiagnosticRequest(
            company_name="Example Co",
            evidence_refs=["evidence://internal/1"],
            baseline_ref="baseline://1",
            source_context="Internal analyst note; not customer acceptance.",
        )
    )

    assert report.source_context_present is True
    assert report.customer_validation_ref == ""
    assert report.customer_validation_status == UNKNOWN
    assert "customer_validated_business_impact" in report.unknowns


def test_evidence_order_does_not_change_report_identity() -> None:
    first = DiagnosticEngine().generate(
        DiagnosticRequest(
            company_name="Example Co",
            evidence_refs=["evidence://2", "evidence://1"],
            pain_points=["reporting", "automation"],
        )
    )
    second = DiagnosticEngine().generate(
        DiagnosticRequest(
            company_name="Example Co",
            evidence_refs=["evidence://1", "evidence://2", "evidence://1"],
            pain_points=["automation", "reporting"],
        )
    )

    assert first.report_id == second.report_id
    assert first.evidence_refs == ["evidence://1", "evidence://2"]


def test_quote_is_not_presented_as_current_authority_before_discovery() -> None:
    report = DiagnosticEngine().generate(DiagnosticRequest(company_name="Example Co"))

    assert report.recommended_service == "qualified_discovery"
    assert report.recommendation_status == "HYPOTHESIS_ONLY"
    assert "Only after Discovery may a Customer-Specific Quote" in report.markdown_ar_en
