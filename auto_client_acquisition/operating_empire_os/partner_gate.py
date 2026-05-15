"""Partner gate — thin façade over market_power_os partner signals."""

from __future__ import annotations

from auto_client_acquisition.market_power_os.partner_signal import (
    PartnerGateSignals,
    compute_partner_gate_readiness,
)


def partner_empire_gate_readiness(signals: PartnerGateSignals) -> int:
    """0-100 readiness to promote/activate partners."""
    return compute_partner_gate_readiness(signals)
