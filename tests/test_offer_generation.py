from __future__ import annotations

from saudi_ai_provider.offers import generate_offer


def test_offer_generation_creates_expected_files(tmp_path) -> None:
    outputs = generate_offer(
        "CUSTOMER_PORTAL_GOLD",
        "smb",
        lang="ar",
        output_dir=tmp_path,
    )

    for path in outputs.values():
        assert path.exists()
        assert path.read_text(encoding="utf-8").strip()

    assert "customer_portal_gold_smb_offer.md" in str(outputs["offer"])
    assert "customer_portal_gold_smb_sow.md" in str(outputs["sow"])
    assert "customer_portal_gold_smb_risk_register.md" in str(outputs["risk_register"])
