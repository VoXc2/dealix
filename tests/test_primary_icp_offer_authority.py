from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICP_PRIMARY = ROOT / "dealix" / "config" / "icp_primary.yaml"


def test_primary_icp_uses_ceo_doctrine_v3_quote_only_authority() -> None:
    text = ICP_PRIMARY.read_text(encoding="utf-8")

    assert "market_identity: governed_ai_execution_platform" in text
    assert "mechanism: signal_decision_action_proof" in text
    assert "entry_offer_id: execution_diagnostic" in text
    assert "primary_offer_id: outcome_sprint" in text
    assert "expansion_offer_id: dealix_runtime" in text
    assert "pricing_authority: customer_specific_quote_only" in text
    assert "public_fixed_price: false" in text
    assert "public_checkout: false" in text

    assert "primary_offer_id: revenue_command_pilot_30d" not in text
    assert "primary_offer_id: seven_day_governance_diagnostic" not in text
