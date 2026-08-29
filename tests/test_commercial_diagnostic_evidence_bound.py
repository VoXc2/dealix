"""Regression tests for the evidence-bound commercial diagnostic."""

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
    assert first.customer_value_claim is False
    assert first.guarantee is False
    assert first.customer_validation_status == "CUSTOMER_VALIDATED_WITH_REFERENCE"
    assert first.approval_status == "approval_required"
    assert first.governance_decision == "pending"
    assert "499" not in first.markdown_ar_en
    assert "20-35%" not in first.markdown_ar_en
    assert "UNKNOWN_NOT_EVIDENCE_BACKED" not in first.markdown_ar_en


def test_missing_evidence_stays_unknown() -> None:
    report = DiagnosticEngine().generate(
        DiagnosticRequest(company_name="Example Co")
    )

    assert UNKNOWN in report.unknowns
    assert report.customer_value_claim is False
    assert report.guarantee is False
    assert report.customer_validation_status == UNKNOWN
    assert "UNKNOWN_NOT_EVIDENCE_BACKED" in report.markdown_ar_en
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

    assert report.customer_validation_ref == ""
    assert report.customer_validation_status == UNKNOWN
    assert any("customer-validation reference" in item for item in report.unknowns)
