"""
Revenue Science — forecasting, attribution, causal impact, churn/expansion.

This module turns "reporting" into "prediction" — ROI projections, deal
forecasts, channel attribution, and the Revenue Impact Simulator (the
"if I sped up follow-up by 4 hours, what would change?" tool).
"""

from auto_client_acquisition.revenue_science.attribution import (
    AttributionResult,
    compute_first_touch,
    compute_last_touch,
    compute_linear,
    compute_time_decay,
)
from auto_client_acquisition.revenue_science.causal_impact import (
    ImpactScenario,
    simulate_impact,
)
from auto_client_acquisition.revenue_science.churn_model import (
    ChurnPrediction,
    predict_churn,
)
from auto_client_acquisition.revenue_science.expansion_model import (
    ExpansionSignal,
    predict_expansion,
)
from auto_client_acquisition.revenue_science.forecast import (
    Forecast,
    ForecastBand,
    compute_forecast,
)

__all__ = [
    "AttributionResult",
    "ChurnPrediction",
    "ExpansionSignal",
    "Forecast",
    "ForecastBand",
    "ImpactScenario",
    "compute_first_touch",
    "compute_forecast",
    "compute_last_touch",
    "compute_linear",
    "compute_time_decay",
    "predict_churn",
    "predict_expansion",
    "simulate_impact",
]
