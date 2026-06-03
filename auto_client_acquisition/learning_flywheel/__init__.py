"""Wave 12 §32.3.11 (Engine 11) — Learning Flywheel.

Composes prior modules to produce:
- Event taxonomy + append-only learning event log
- Funnel metrics calculator (5-stage conversion)
- Feature-request triage (≥3 customer rule)
- Best-of tracker (best ICP / message / channel / offer / objection)
- Weekly learning report aggregator (replaces the skeleton in
  ``revenue_os/learning_weekly.py``)

Hard rule (Article 8): every metric is calculated from real recorded
events. NEVER fabricates a number when the source data is empty —
returns None / empty list / 0 instead.

Reuses:
- ``company_brain_v6.timeline`` (Engine 3) for per-customer outcomes
- ``proof_ledger`` for proof_event counts
- ``approval_center`` for approval outcomes
- ``revenue_profitability`` for revenue truth
"""
from __future__ import annotations

from auto_client_acquisition.learning_flywheel.aggregator import (
    LearningEvent,
    WeeklyLearningReport,
    aggregate_weekly_report,
    record_learning_event,
)
from auto_client_acquisition.learning_flywheel.feature_gating import (
    FeatureRequestStatus,
    triage_feature_request,
)
from auto_client_acquisition.learning_flywheel.funnel_metrics import (
    FunnelMetrics,
    compute_funnel,
)

__all__ = [
    "FeatureRequestStatus",
    "FunnelMetrics",
    "LearningEvent",
    "WeeklyLearningReport",
    "aggregate_weekly_report",
    "compute_funnel",
    "record_learning_event",
    "triage_feature_request",
]
