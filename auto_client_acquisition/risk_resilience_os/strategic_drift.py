"""Strategic drift — warning signals that should trigger portfolio review."""

from __future__ import annotations

STRATEGIC_DRIFT_WARNING_SIGNALS: tuple[str, ...] = (
    "custom_work_exceeds_productized",
    "no_proof_packs",
    "no_capital_assets",
    "features_without_usage",
    "clients_request_unsafe_automation",
    "founder_delivery_bottleneck",
)


def drift_warning_signal_valid(signal: str) -> bool:
    return signal in STRATEGIC_DRIFT_WARNING_SIGNALS


def drift_freeze_new_features_recommended(active_warnings: frozenset[str]) -> bool:
    """Three or more concurrent drift warnings → freeze new features until review."""
    return len(active_warnings & frozenset(STRATEGIC_DRIFT_WARNING_SIGNALS)) >= 3
