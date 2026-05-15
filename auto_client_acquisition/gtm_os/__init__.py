"""GTM OS v5 — content_calendar + message_experiment.

Both modules are draft-only. The content calendar generates SUGGESTED
slots anchored to real signals (lowest-scoring landing pages); the
message experiment is a typed schema for tracking — no execution.
"""
from auto_client_acquisition.gtm_os.content_calendar import (
    ContentCalendarSlot,
    build_weekly_calendar,
)
from auto_client_acquisition.gtm_os.message_experiment import (
    MessageExperiment,
    draft_experiment,
)

__all__ = [
    "ContentCalendarSlot",
    "MessageExperiment",
    "build_weekly_calendar",
    "draft_experiment",
]
