from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICP_PRIMARY = ROOT / "dealix" / "config" / "icp_primary.yaml"


def test_primary_icp_uses_current_quote_only_pilot_authority() -> None:
    text = ICP_PRIMARY.read_text(encoding="utf-8")

    assert "primary_offer_id: revenue_command_pilot_30d" in text
    assert "primary_offer_id: seven_day_governance_diagnostic" not in text
