"""Market Power OS — category and inbound signals."""

from __future__ import annotations

from auto_client_acquisition.market_power_os.benchmark_registry import get_benchmark
from auto_client_acquisition.market_power_os.category_language_tracker import (
    market_language_health_score,
)
from auto_client_acquisition.market_power_os.category_metrics import (
    CATEGORY_PHRASES,
    category_hit_count,
)
from auto_client_acquisition.market_power_os.content_signal import education_funnel_coverage_percent
from auto_client_acquisition.market_power_os.inbound_quality import inbound_quality_score
from auto_client_acquisition.market_power_os.language_tracking import language_drift_score
from auto_client_acquisition.market_power_os.market_power_score import (
    MarketPowerDimensions,
    compute_market_power_score,
)
from auto_client_acquisition.market_power_os.partner_signal import (
    PartnerGateSignals,
    compute_partner_gate_readiness,
)

__all__ = [
    "CATEGORY_PHRASES",
    "MarketPowerDimensions",
    "PartnerGateSignals",
    "category_hit_count",
    "compute_market_power_score",
    "compute_partner_gate_readiness",
    "education_funnel_coverage_percent",
    "get_benchmark",
    "inbound_quality_score",
    "language_drift_score",
    "market_language_health_score",
]
