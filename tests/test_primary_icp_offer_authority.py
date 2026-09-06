from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICP_PRIMARY = ROOT / "dealix" / "config" / "icp_primary.yaml"


def test_primary_icp_uses_v3_positioning_with_canonical_quote_only_authority() -> None:
    text = ICP_PRIMARY.read_text(encoding="utf-8")

    # V3 defines the market identity and vocabulary.
    assert "market_identity: governed_ai_execution_platform" in text
    assert "mechanism: signal_decision_action_proof" in text
    assert "market_entry_label: execution_diagnostic" in text
    assert "market_paid_offer_label: outcome_sprint" in text
    assert "market_expansion_label: dealix_runtime" in text

    # Operational authority remains on the accepted launch IDs until an explicit
    # authority migration updates runtime/public/delivery/proof contracts together.
    assert "entry_offer_id: free_mini_diagnostic" in text
    assert "primary_offer_id: revenue_command_pilot_30d" in text
    assert "pricing_authority: customer_specific_quote_only" in text
    assert "public_fixed_price: false" in text
    assert "public_checkout: false" in text

    assert "primary_offer_id: outcome_sprint" not in text
    assert "primary_offer_id: seven_day_governance_diagnostic" not in text
