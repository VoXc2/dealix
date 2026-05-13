"""Dealix Value Capture & Monetization OS.

Companion doc: ``docs/value_capture/VALUE_CAPTURE_DOCTRINE.md``.
"""

from __future__ import annotations

from auto_client_acquisition.value_capture_os.client_quality_score import (
    CLIENT_QUALITY_WEIGHTS,
    ClientQualityComponents,
    ClientTier,
    classify_client_tier,
    compute_client_quality_score,
)
from auto_client_acquisition.value_capture_os.expansion_map import (
    EXPANSION_MAP,
    next_expansion_step,
)
from auto_client_acquisition.value_capture_os.revenue_quality_score import (
    REVENUE_QUALITY_WEIGHTS,
    RevenueQualityComponents,
    RevenueTier,
    classify_revenue_tier,
    compute_revenue_quality_score,
)
from auto_client_acquisition.value_capture_os.scope_control import (
    ChangeRequestClass,
    classify_change_request,
)
from auto_client_acquisition.value_capture_os.upsell_logic import (
    UpsellRecommendation,
    recommend_upsell,
)
from auto_client_acquisition.value_capture_os.value_capture_ladder import (
    VALUE_CAPTURE_LADDER,
    ValueCaptureStage,
)
from auto_client_acquisition.value_capture_os.value_capture_dashboard import (
    ValueCaptureDashboardSnapshot,
)

__all__ = [
    "CLIENT_QUALITY_WEIGHTS",
    "ClientQualityComponents",
    "ClientTier",
    "classify_client_tier",
    "compute_client_quality_score",
    "EXPANSION_MAP",
    "next_expansion_step",
    "REVENUE_QUALITY_WEIGHTS",
    "RevenueQualityComponents",
    "RevenueTier",
    "classify_revenue_tier",
    "compute_revenue_quality_score",
    "ChangeRequestClass",
    "classify_change_request",
    "UpsellRecommendation",
    "recommend_upsell",
    "VALUE_CAPTURE_LADDER",
    "ValueCaptureStage",
    "ValueCaptureDashboardSnapshot",
]
