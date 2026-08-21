"""The public Free Mini Diagnostic must not become a real-customer PII intake."""

from pathlib import Path

DIAGNOSTIC = (
    Path(__file__).resolve().parents[1] / "landing" / "diagnostic.html"
).read_text(encoding="utf-8")


def test_diagnostic_matches_canonical_free_entry_deliverables() -> None:
    for required in (
        "Free Mini Diagnostic",
        "Credible leak hypothesis",
        "Written diagnosis",
        "Missing-evidence report",
        "Pilot hypothesis",
        "HUMAN_REVIEW_REQUIRED",
    ):
        assert required in DIAGNOSTIC, required


def test_diagnostic_does_not_collect_contact_pii_or_persist_a_lead() -> None:
    for forbidden in (
        'name="contact_name"',
        'name="phone"',
        'name="email"',
        "/api/v1/public/demo-request",
        "contact_name.value",
        "form.phone",
        "form.email",
        "sami.assiri11@gmail.com",
    ):
        assert forbidden not in DIAGNOSTIC, forbidden
    assert "NO_PII_CAPTURE" in DIAGNOSTIC
    assert "NO_LEAD_PERSISTENCE" in DIAGNOSTIC


def test_diagnostic_requests_only_business_operating_context() -> None:
    for field in (
        'name="company_handle"',
        'name="sector"',
        'name="company_url"',
        'name="biggest_problem"',
        'name="target_metric"',
        'name="tech_level"',
        'name="current_channels"',
        'name="minimum_data_ack"',
    ):
        assert field in DIAGNOSTIC, field
    assert "لا تضع بيانات شخصية" in DIAGNOSTIC
    assert "لا تضع رابطًا خاصًا أو يحمل token" in DIAGNOSTIC


def test_diagnostic_api_call_is_analysis_only() -> None:
    assert "/api/v1/company-growth-beast/diagnostic" in DIAGNOSTIC
    assert "offer: 'free_mini_diagnostic'" in DIAGNOSTIC
    assert "consent_for_diagnostic: true" in DIAGNOSTIC
    assert "fetch(`${API_BASE}/api/v1/public/" not in DIAGNOSTIC


def test_human_follow_up_is_user_initiated() -> None:
    assert "mailto:hello@dealix.me" in DIAGNOSTIC
    assert "المتابعة اختيارية وبإرسال منك" in DIAGNOSTIC
    assert "لا نحفظ بيانات اتصال من هذا النموذج" in DIAGNOSTIC
