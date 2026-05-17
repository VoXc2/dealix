"""Revenue Autopilot orchestrator — engagement lifecycle + dispatch.

Sequences the 10 automations over an ``AutopilotEngagement`` and persists
each snapshot. Persistence follows the ``leadops_spine`` pattern:
in-memory index + append-only JSONL + operational stream mirror.

NEVER executes an external send. NEVER auto-approves a draft.

Doctrine: docs/REVENUE_AUTOPILOT.md
"""
from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timezone

from auto_client_acquisition.revenue_autopilot.automations import (
    AUTOMATIONS,
    automation_1_lead_capture,
)
from auto_client_acquisition.revenue_autopilot.funnel import (
    FunnelStage,
    advance_stage,
)
from auto_client_acquisition.revenue_autopilot.lead_scorer import LeadSignals
from auto_client_acquisition.revenue_autopilot.records import (
    AutomationResult,
    AutopilotEngagement,
    Contact,
    StageTransition,
)

_JSONL_PATH = os.path.join("data", "revenue_autopilot.jsonl")
_INDEX: dict[str, AutopilotEngagement] = {}


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(engagement: AutopilotEngagement) -> None:
    """Update the in-memory index, append a JSONL snapshot, mirror it."""
    engagement.updated_at = datetime.now(UTC)
    _INDEX[engagement.engagement_id] = engagement
    _ensure_dir()
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(engagement.model_dump_json() + "\n")
    from auto_client_acquisition.persistence.operational_stream_mirror import (
        mirror_append,
    )

    mirror_append(
        stream_id="revenue_autopilot_jsonl",
        payload=engagement.model_dump(mode="json"),
        event_id=engagement.engagement_id,
    )


def capture_lead(
    *, contact: dict, signals: dict
) -> tuple[AutopilotEngagement, AutomationResult]:
    """Automation 1 — create an engagement, score it, draft a first response."""
    engagement = AutopilotEngagement(
        contact=Contact(**contact),
        signals=LeadSignals(**signals),
    )
    result = automation_1_lead_capture(engagement, {})
    _persist(engagement)
    return engagement, result


def run_automation(
    name: str, engagement_id: str, payload: dict | None = None
) -> tuple[AutopilotEngagement, AutomationResult]:
    """Run automations 2-10 by name against an existing engagement."""
    engagement = _INDEX.get(engagement_id)
    if engagement is None:
        raise KeyError(f"unknown engagement: {engagement_id}")
    fn = AUTOMATIONS.get(name)
    if fn is None:
        raise ValueError(
            f"unknown automation: {name!r}; "
            f"known: {sorted(AUTOMATIONS)}"
        )
    result = fn(engagement, payload or {})
    _persist(engagement)
    return engagement, result


def advance_funnel(
    engagement_id: str, target: FunnelStage, *, actor: str = "founder"
) -> AutopilotEngagement:
    """Founder-driven explicit funnel advance (e.g. scope_sent → invoice_sent)."""
    engagement = _INDEX.get(engagement_id)
    if engagement is None:
        raise KeyError(f"unknown engagement: {engagement_id}")
    new_stage = advance_stage(engagement.current_stage, target)
    engagement.stage_history.append(StageTransition(
        from_stage=engagement.current_stage,
        to_stage=new_stage,
        automation="manual_advance",
        actor=actor,
    ))
    engagement.current_stage = new_stage
    _persist(engagement)
    return engagement


def get_engagement(engagement_id: str) -> AutopilotEngagement | None:
    """Return one engagement by id, or None."""
    return _INDEX.get(engagement_id)


def list_engagements(*, limit: int = 50) -> list[AutopilotEngagement]:
    """Most-recently-updated-first list of engagements."""
    return sorted(
        _INDEX.values(),
        key=lambda e: e.updated_at,
        reverse=True,
    )[:limit]


def reset() -> None:
    """Test-only — wipe the in-memory index."""
    _INDEX.clear()


__all__ = [
    "advance_funnel",
    "capture_lead",
    "get_engagement",
    "list_engagements",
    "reset",
    "run_automation",
]
