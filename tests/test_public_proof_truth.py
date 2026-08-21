"""Public Proof page must not resurrect retired launch claims."""

from pathlib import Path

PROOF = Path(__file__).resolve().parents[1] / "landing" / "proof.html"


def _html() -> str:
    return PROOF.read_text(encoding="utf-8")


def test_public_proof_keeps_evidence_and_publication_boundaries() -> None:
    html = _html()
    assert 'id="evidence-levels"' in html
    for level in ("L1", "L2", "L3", "L4", "L5"):
        assert level in html
    assert "Publication Consent" in html
    assert "NO_FAKE_PROOF" in html
    assert "NO_FAKE_REVENUE" in html
    assert "Delivery وCustomer Value وPayment وRevenue وPublication Permission حالات منفصلة" in html


def test_public_proof_uses_current_quote_only_pilot_path() -> None:
    html = _html()
    assert "30-day Revenue Command Pilot" in html
    assert "/diagnostic.html" in html
    assert "/pricing.html" in html
    assert "Quote معتمد" in html


def test_public_proof_rejects_retired_fixed_price_and_fake_social_proof() -> None:
    html = _html()
    retired = (
        "499",
        "7-Day",
        "7-day",
        "٧ أيّام",
        "/start.html",
        "real Saudi B2B pilots",
        "البايلوتات الحقيقيّة",
        "فاتورة ZATCA + شهادة العميل + رابط Moyasar",
    )
    for token in retired:
        assert token not in html, f"retired public proof token returned: {token}"


def test_public_proof_does_not_claim_customer_proof_by_default() -> None:
    html = _html()
    assert "الحالة الافتراضية: لا Customer Proof عام" in html
    assert "لا تعرض هذه الصفحة Customer Proof افتراضيًا" in html
    assert "وجود عميل أو إيراد أو Case Study منشورًا" in html
