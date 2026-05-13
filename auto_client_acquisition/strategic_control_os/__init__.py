"""Dealix Strategic Control & Market Leadership OS.

Companion docs live under ``docs/strategic_control/``. These modules
provide typed surfaces for the leadership layer: control metrics with
doctrine thresholds, the control plane catalog, the product sequence
with forbidden inversions, the no-weak-scale and strong-scale rules,
and the Market Command Dashboard composite.

All modules are dependency-free and side-effect-free.
"""

from __future__ import annotations

from auto_client_acquisition.strategic_control_os.control_metrics import (
    CONTROL_METRIC_THRESHOLDS,
    ControlMetricResult,
    ControlMetricSnapshot,
    StrategicControlThreshold,
    evaluate_control_metrics,
)
from auto_client_acquisition.strategic_control_os.control_plane import (
    CONTROL_PLANE_COMPONENTS,
    ControlPlaneComponent,
    ControlPlaneIndex,
)
from auto_client_acquisition.strategic_control_os.market_command_dashboard import (
    MARKET_DASHBOARD_INDICATORS,
    MarketCommandDashboardReading,
    MarketDashboardIndicator,
    sustained_indicator_count,
)
from auto_client_acquisition.strategic_control_os.product_sequence import (
    FORBIDDEN_INVERSIONS,
    PRODUCT_SEQUENCE,
    ProductSequenceStep,
    is_valid_order,
)
from auto_client_acquisition.strategic_control_os.strong_scale_rule import (
    STRONG_SCALE_CONDITIONS,
    StrongScaleAssessment,
    StrongScaleEvidence,
    evaluate_strong_scale,
)
from auto_client_acquisition.strategic_control_os.weak_scale_rule import (
    WEAK_SCALE_TARGETS,
    WeakScaleResult,
    WeakScaleSignals,
    WeakScaleTarget,
    evaluate_weak_scale,
)

__all__ = [
    "CONTROL_METRIC_THRESHOLDS",
    "ControlMetricResult",
    "ControlMetricSnapshot",
    "StrategicControlThreshold",
    "evaluate_control_metrics",
    "CONTROL_PLANE_COMPONENTS",
    "ControlPlaneComponent",
    "ControlPlaneIndex",
    "MARKET_DASHBOARD_INDICATORS",
    "MarketCommandDashboardReading",
    "MarketDashboardIndicator",
    "sustained_indicator_count",
    "FORBIDDEN_INVERSIONS",
    "PRODUCT_SEQUENCE",
    "ProductSequenceStep",
    "is_valid_order",
    "STRONG_SCALE_CONDITIONS",
    "StrongScaleAssessment",
    "StrongScaleEvidence",
    "evaluate_strong_scale",
    "WEAK_SCALE_TARGETS",
    "WeakScaleResult",
    "WeakScaleSignals",
    "WeakScaleTarget",
    "evaluate_weak_scale",
]
