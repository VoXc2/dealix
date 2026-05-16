"""Value-based pricing engine."""

from __future__ import annotations

from auto_client_acquisition.value_os.pricing_engine import quote_value_based


def test_quote_higher_with_evidence() -> None:
    low = quote_value_based(offer_tier="pilot_499", measured_value_sar=0, evidence_level="L1")
    high = quote_value_based(offer_tier="pilot_499", measured_value_sar=50_000, evidence_level="L5")
    assert high.quoted_sar >= low.quoted_sar
