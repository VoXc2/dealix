"""Dealix analytics — PostHog funnel tracking + feature flags."""
from dealix.analytics.posthog_client import capture_event, get_feature_flag, FUNNEL_EVENTS

__all__ = ["capture_event", "get_feature_flag", "FUNNEL_EVENTS"]
