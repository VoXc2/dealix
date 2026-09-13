from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_public_footer_contains_no_placeholder_contact_or_blanket_certification_claims() -> None:
    text = _text("frontend/src/components/layout/FooterSection.tsx")
    lowered = text.lower()
    assert "966500000000" not in text
    assert 'en: "pdpl compliant"' not in lowered
    assert 'en: "zatca ready"' not in lowered
    assert "subject to citc regulations" not in lowered
    assert "customer-specific scope" in lowered
    assert "reviewable evidence trail" in lowered


def test_trust_center_is_evidence_bound_not_self_certifying() -> None:
    text = _text("frontend/src/components/trust/TrustCenter.tsx")
    lowered = text.lower()
    forbidden = (
        "fully aligned with the personal data protection law",
        "operational data is hosted entirely within the kingdom",
        "quarterly security review by an independent third party",
        "0\",\n    valueen: \"0",
        "zatca readiness certificate",
        "pdpl compliance report",
    )
    for claim in forbidden:
        assert claim not in lowered
    assert "compliance support — not a certification" in lowered
    assert "verify per customer" in lowered
    assert "unknown/hold" in lowered


def test_partner_enablement_cannot_mint_price_duration_or_compliance() -> None:
    text = _text("docs/partnerships/PARTNER_ENABLEMENT_KIT_AR.md")
    lowered = text.lower()
    assert "pricing: from 9,999" not in lowered
    assert "diagnostic: 1,500-5,000" not in lowered
    assert '"is this pdpl compliant?" (yes)' not in lowered
    assert "all diagnostics free" not in lowered or "diagnostic = free" in lowered
    assert "no public fixed price authority" in lowered
    assert "no public fixed duration authority" in lowered
    assert "partner hypothesis ≠ approved partner" in lowered


def test_compliance_inventory_distinguishes_controls_from_attestation() -> None:
    text = _text("docs/legal/COMPLIANCE_CERTIFICATIONS.md")
    lowered = text.lower()
    assert "pdpl (personal data protection law)** | compliant by design" not in lowered
    assert "zatca phase 2 e-invoicing** | wired (production-ready)" not in lowered
    assert "all invoices are:" not in lowered
    assert "all invoices clear automatically" in lowered  # explicitly blocked claim example
    assert "control_implemented_not_attested" in lowered
    assert "source capability != source acceptance != runtime acceptance" in lowered
