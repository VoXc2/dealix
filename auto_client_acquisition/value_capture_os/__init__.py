"""Value Capture & Monetization Architecture — deterministic commercial economics."""

from __future__ import annotations

from auto_client_acquisition.value_capture_os.client_quality_score import (
    ClientQualityDimensions,
    client_quality_band,
    client_quality_score,
)
from auto_client_acquisition.value_capture_os.expansion_map import (
    TRACK_AI_QUICK_WIN,
    TRACK_COMPANY_BRAIN,
    TRACK_GOVERNANCE,
    TRACK_REVENUE_INTELLIGENCE,
    recommended_expansion_offer,
)
from auto_client_acquisition.value_capture_os.pricing_model import (
    MonetizationOfferKind,
    gross_margin_meets_target,
)
from auto_client_acquisition.value_capture_os.revenue_quality_score import (
    RevenueQualityDimensions,
    revenue_quality_band,
    revenue_quality_score,
)
from auto_client_acquisition.value_capture_os.scope_control import (
    ChangeRequestClass,
    classify_change_request,
)
from auto_client_acquisition.value_capture_os.upsell_logic import (
    ProofCommercialSignal,
    upsell_from_proof_signal,
)
from auto_client_acquisition.value_capture_os.value_capture_dashboard import (
    VALUE_CAPTURE_DASHBOARD_SIGNALS,
    value_capture_dashboard_coverage_score,
)

__all__ = (
    "TRACK_AI_QUICK_WIN",
    "TRACK_COMPANY_BRAIN",
    "TRACK_GOVERNANCE",
    "TRACK_REVENUE_INTELLIGENCE",
    "VALUE_CAPTURE_DASHBOARD_SIGNALS",
    "ChangeRequestClass",
    "ClientQualityDimensions",
    "MonetizationOfferKind",
    "ProofCommercialSignal",
    "RevenueQualityDimensions",
    "classify_change_request",
    "client_quality_band",
    "client_quality_score",
    "gross_margin_meets_target",
    "recommended_expansion_offer",
    "revenue_quality_band",
    "revenue_quality_score",
    "upsell_from_proof_signal",
    "value_capture_dashboard_coverage_score",
)
