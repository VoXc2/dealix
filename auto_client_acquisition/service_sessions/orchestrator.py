"""Service Session Runtime orchestrator (Wave 13 Phase 3).

The thin operating layer over `service_sessions/{lifecycle,store}.py`.
Provides:
  - tick(session_id, today)      — advance day counter + enforce daily artifact
  - record_artifact(...)         — append a DailyArtifact to a session
  - is_artifact_overdue(session) — pure check: 2+ days w/o artifact

Article 4: never auto-sends; never advances `active → delivered` w/o approval.
Article 8: enforcer raises ArtifactOverdueError, does NOT pretend session
ran without artifact (no fake_proof).
Article 11: ~120 LOC; no business logic — just orchestration over existing
lifecycle truth-table.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import (
    ServiceSessionRecord,
)


class ArtifactOverdueError(RuntimeError):
    """Raised when a session has gone 2+ days without a daily artifact.

    Article 8: do NOT silently advance day counter when no work happened.
    """


class SessionNotRunningError(RuntimeError):
    """Raised when tick() is called on a non-running session (draft/blocked/complete)."""


@dataclass(slots=True)
class TickResult:
    session_id: str
    previous_day: int
    new_day: int
    artifact_required_for_today: bool
    enforcer_fired: bool
    reason: str  # human-readable bilingual-safe reason


def _today_utc() -> datetime:
    return datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)


def _last_artifact_day(rec: ServiceSessionRecord) -> int:
    """Returns the largest `day_number` recorded in daily_artifacts, or 0."""
    if not rec.daily_artifacts:
        return 0
    return max(int(a.get("day_number", 0)) for a in rec.daily_artifacts)


def is_artifact_overdue(rec: ServiceSessionRecord) -> bool:
    """Pure check: True if 2+ days have advanced past last artifact day.

    Article 8: this is the deterministic enforcer — if a session is on
    day 5 but the last artifact is from day 2, we are 3 days overdue.
    """
    if rec.status != "active":
        return False
    if rec.day_number <= 1:
        return False
    last_day = _last_artifact_day(rec)
    return (rec.day_number - last_day) >= 2


def tick(
    rec: ServiceSessionRecord,
    *,
    today: datetime | None = None,
    raise_on_overdue: bool = True,
) -> TickResult:
    """Advance the session's day counter by 1.

    Hard rules:
      - Only running sessions (status='active') can tick.
      - If `raise_on_overdue=True` (default) and the session is 2+ days
        without an artifact, raises ArtifactOverdueError BEFORE advancing.
      - Caller is responsible for persisting the new state (this is a
        pure compute fn; mutates the in-memory record but does NOT call store).
    """
    if rec.status != "active":
        raise SessionNotRunningError(
            f"session_not_running: status={rec.status}, expected=active"
        )

    if raise_on_overdue and is_artifact_overdue(rec):
        last = _last_artifact_day(rec)
        raise ArtifactOverdueError(
            f"artifact_overdue: session={rec.session_id} on day={rec.day_number} "
            f"but last artifact was day={last} ({rec.day_number - last} days ago). "
            f"Record an artifact via record_artifact() before next tick."
        )

    previous_day = rec.day_number
    rec.day_number = previous_day + 1
    artifact_required = True  # every running day requires an artifact

    return TickResult(
        session_id=rec.session_id,
        previous_day=previous_day,
        new_day=rec.day_number,
        artifact_required_for_today=artifact_required,
        enforcer_fired=False,
        reason=f"advanced_day_{previous_day}_to_{rec.day_number}",
    )


def record_artifact(
    rec: ServiceSessionRecord,
    *,
    artifact_id: str | None = None,
    artifact_type: str = "deliverable",
    title_ar: str = "",
    title_en: str = "",
    customer_visible: bool = True,
    status: str = "draft",
    day_number: int | None = None,
) -> dict[str, Any]:
    """Append a DailyArtifact to the session's daily_artifacts list.

    Returns the artifact dict that was appended. Caller persists rec.
    """
    if day_number is None:
        day_number = rec.day_number if rec.day_number > 0 else 1
    artifact = {
        "artifact_id": artifact_id or f"art_{uuid.uuid4().hex[:10]}",
        "day_number": int(day_number),
        "type": artifact_type,
        "title_ar": title_ar,
        "title_en": title_en,
        "customer_visible": bool(customer_visible),
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    rec.daily_artifacts.append(artifact)
    return artifact


def set_next_actions(
    rec: ServiceSessionRecord,
    *,
    customer_action_ar: str | None = None,
    customer_action_en: str | None = None,
    founder_action_ar: str | None = None,
    founder_action_en: str | None = None,
) -> None:
    """Populate next_customer_action + next_founder_action (bilingual)."""
    if customer_action_ar is not None or customer_action_en is not None:
        rec.next_customer_action = {
            "ar": (customer_action_ar or "").strip(),
            "en": (customer_action_en or "").strip(),
        }
    if founder_action_ar is not None or founder_action_en is not None:
        rec.next_founder_action = {
            "ar": (founder_action_ar or "").strip(),
            "en": (founder_action_en or "").strip(),
        }
