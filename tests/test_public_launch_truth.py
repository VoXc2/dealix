"""Public launch truth must distinguish current authority from retired surfaces."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"


def test_homepage_has_no_unproved_speed_or_customer_result() -> None:
    html = (LANDING / "index.html").read_text(encoding="utf-8")

    for retired_claim in (
        "٤٠٪ من leads",
        "يرد خلال ٤٥ ثانية",
        "سيناريو حقيقي",
        "محادثة حقيقية",
        "موظف مبيعات AI حقيقي",
    ):
        assert retired_claim not in html

    # The current WADL block is explicitly an operating example, not customer proof.
    assert "DEMO" in html
    assert "هذا مثال تشغيلي، وليس Claim لنتيجة عميل" in html
    assert "Evidence before claims" in html


def test_homepage_explains_current_governed_boundary() -> None:
    html = (LANDING / "index.html").read_text(encoding="utf-8")

    assert "خدمات Live" not in html
    assert "Approval-first" in html
    assert "Proof-backed" in html
    assert "مراجعة بشرية قبل أي عرض مدفوع" in html
    assert "Free Mini Diagnostic" in html
    assert "30-day Revenue Command Pilot" in html
    assert "لا self-serve checkout" in html


def test_status_console_is_retired_fail_closed_not_public_authority() -> None:
    html = (LANDING / "status.html").read_text(encoding="utf-8")

    assert "DEALIX_RETIRED_PUBLIC_SURFACE" in html
    assert "noindex,nofollow" in html.replace(" ", "").lower()
    assert 'http-equiv="refresh" content="0; url=/"' in html
    assert 'rel="canonical" href="https://dealix.me/"' in html
    assert "هذه الصفحة قديمة وليست مرجعًا حاليًا" in html

    # Retiring the old console must also remove its historical live/code-ready claims.
    assert "جاهز للكود" not in html
    assert "Code-ready" not in html
