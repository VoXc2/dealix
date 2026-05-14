"""Kill protocol — partner decisions + re-exports from kill_criteria."""

from __future__ import annotations

from auto_client_acquisition.command_os.kill_criteria import (
    KillMarketSignals,
    KillServiceSignals,
    kill_feature_recommended,
    kill_market_recommended,
    kill_service_recommended,
)


def kill_partner_recommended(
    *,
    sells_unsafe_promises: bool,
    bypasses_governance: bool,
    harms_brand: bool,
    qa_non_compliant: bool,
) -> bool:
    """Recommend ending or suspending partner relationship if any flag is true."""
    return (
        sells_unsafe_promises
        or bypasses_governance
        or harms_brand
        or qa_non_compliant
    )


__all__ = [
    "KillMarketSignals",
    "KillServiceSignals",
    "kill_feature_recommended",
    "kill_market_recommended",
    "kill_partner_recommended",
    "kill_service_recommended",
]
