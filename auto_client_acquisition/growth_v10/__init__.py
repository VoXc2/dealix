"""Growth v10 — PostHog-inspired event taxonomy + funnel + experiments.

Pure Python, no LLM, no live HTTP. Events are PII-redacted on insert.
Campaigns block transitions to ``running`` without consent evidence.
"""
from auto_client_acquisition.growth_v10.attribution_model import attribute_revenue
from auto_client_acquisition.growth_v10.campaign_lifecycle import transition_campaign
from auto_client_acquisition.growth_v10.content_calendar import build_calendar
from auto_client_acquisition.growth_v10.event_taxonomy import (
    list_event_names,
    validate_event,
)
from auto_client_acquisition.growth_v10.experiment_model import evaluate_experiment
from auto_client_acquisition.growth_v10.feedback_model import nps_band, record_feedback
from auto_client_acquisition.growth_v10.funnel_model import compute_funnel
from auto_client_acquisition.growth_v10.schemas import (
    Campaign,
    EventName,
    EventRecord,
    Experiment,
    FeedbackRecord,
    FunnelReport,
    FunnelStage,
    FunnelStep,
    WeeklyContentCalendar,
)

__all__ = [
    "Campaign",
    "EventName",
    "EventRecord",
    "Experiment",
    "FeedbackRecord",
    "FunnelReport",
    "FunnelStage",
    "FunnelStep",
    "WeeklyContentCalendar",
    "attribute_revenue",
    "build_calendar",
    "compute_funnel",
    "evaluate_experiment",
    "list_event_names",
    "nps_band",
    "record_feedback",
    "transition_campaign",
    "validate_event",
]
