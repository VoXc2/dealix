from pathlib import Path

from integrations.pdpl import build_breach_notification, build_monthly_audit_report

ROOT = Path(__file__).resolve().parents[1]


def test_consent_request_prepare_path_never_claims_delivery() -> None:
    source = (ROOT / "api/routers/pdpl.py").read_text(encoding="utf-8")
    segment = source.split('async def request_consent', 1)[1].split('@router.post("/consent/grant"', 1)[0]
    assert 'status="sent"' not in segment
    assert "consent_request_sent" not in segment
    assert '"channels_queued"' not in segment
    assert 'status="prepared"' in segment
    assert '"delivery_executed": False' in segment
    assert '"status": "prepared"' in segment


def test_consent_request_model_defaults_to_prepared() -> None:
    source = (ROOT / "db/models.py").read_text(encoding="utf-8")
    segment = source.split("class ConsentRequestRecord", 1)[1].split("class PaymentRecord", 1)[0]
    assert 'default="prepared"' in segment
    assert '# prepared | sent | delivered' in segment


def test_monthly_report_is_evidence_not_certification() -> None:
    report = build_monthly_audit_report(
        tenant_id="tenant-test",
        report_month="2026-09",
        audit_records=[],
        consent_stats={"total_records": 0},
        erasure_requests=[],
        breach_incidents=[],
        processing_activities=[],
    )
    assert "certifications" not in report
    assert report["assurance"]["pdpl_compliance_certified"] is False
    assert report["assurance"]["assurance_status"] == "CONTROL_IMPLEMENTED_NOT_ATTESTED"
    assert all(item["status"] != "compliant" for item in report["compliance_checklist"])


def test_breach_package_separates_preparation_from_submission() -> None:
    package = build_breach_notification(
        tenant_id="tenant-test",
        breach_description="synthetic test only",
        affected_data_categories=["contact"],
        estimated_subjects_count=1,
        discovery_datetime="2026-09-15T00:00:00Z",
        mitigation_steps=["contain"],
    )
    assert package["status"] == "prepared"
    assert package["submission_executed"] is False
    assert package["notification_deadlines"]["competent_authority_notification_hours"] == 72
    assert package["notification_deadlines"]["applicability"] == "QUALIFYING_BREACH_ONLY"
    assert "Implementing Regulations Art. 24" in package["pdpl_article"]


def test_hermes_data_passport_cannot_self_certify_pdpl() -> None:
    source = (ROOT / "dealix/hermes/tools/data_tools.py").read_text(encoding="utf-8")
    segment = source.split("async def generate_data_passport", 1)[1].split("__all__", 1)[0]
    assert '"pdpl_compliant": True' not in segment
    assert '"pdpl_compliance_certified": False' in segment
    assert '"pdpl_assurance_status": "CONTROL_IMPLEMENTED_NOT_ATTESTED"' in segment
    assert '"data_mode": "synthetic_example"' in segment


def test_weekly_pdpl_metric_fails_closed_and_is_not_labeled_certification() -> None:
    source = (ROOT / "dealix/commercial_ops/weekly_report_generator.py").read_text(encoding="utf-8")
    assert 'd.get("pdpl_compliant_pct", 100)' not in source
    assert 'd.get("pdpl_compliant_pct", 0)' in source
    assert "PDPL Policy Gate Coverage" in source
    assert "policy_gate_coverage_not_legal_compliance" in source
