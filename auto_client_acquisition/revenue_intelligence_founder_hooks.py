"""Hooks for Revenue Intelligence → Founder Command Summary snapshot (§39).

Import ``record_engagement_progress`` from pipeline routers after each successful
HTTP step so ``GET /api/v1/founder-summary`` aggregates live state.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.founder_command_summary.engagement_registry import (
    merge_pipeline_stage,
)

__all__ = ["merge_pipeline_stage", "record_engagement_progress"]


def record_engagement_progress(engagement_id: str, **kwargs: Any) -> Any:
    """Typed alias for pipeline modules — forwards to ``merge_pipeline_stage``."""
    return merge_pipeline_stage(engagement_id, **kwargs)
