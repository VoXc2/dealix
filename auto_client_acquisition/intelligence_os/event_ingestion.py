"""Placeholder for event ingestion pipeline hooks (no network, no DB)."""

from __future__ import annotations

from auto_client_acquisition.intelligence_os.events_to_metrics import (
    EVENT_METRIC_FAMILY,
    metric_family_for_event,
)

__all__ = ["EVENT_METRIC_FAMILY", "metric_family_for_event"]
