"""Wave 12.5 §33.2.3 (Engine 7) — Delivery OS Workflow Schema + Daily Artifact Enforcer.

Defines the 7 Dealix delivery workflows as YAML data files and provides
a deterministic enforcer that fires when a service session passes
N consecutive days without a recorded artifact.

Hard rule (Article 8): "اشتغلنا" (we worked on it) without an artifact
is BLOCKED. Every day of a multi-day workflow must produce a tangible
deliverable OR explicitly state a blocker.

The 7 workflows (per plan §32.3.7):
1. onboarding         — Day 0 customer setup
2. diagnostic         — 24h diagnostic session
3. lead_radar          — weekly opportunity scan
4. outreach_draft      — bilingual draft pack
5. support             — ticket triage + reply draft
6. proof_pack          — multi-event narrative assembly
7. expansion           — next-best-offer recommendation
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

import yaml

# Repo-relative path to the workflow YAMLs.
REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = REPO_ROOT / "data" / "workflows"

# Canonical 7 workflow names (must match YAML filenames).
WorkflowName = Literal[
    "onboarding",
    "diagnostic",
    "lead_radar",
    "outreach_draft",
    "support",
    "proof_pack",
    "expansion",
]

CANONICAL_WORKFLOWS: tuple[WorkflowName, ...] = (
    "onboarding",
    "diagnostic",
    "lead_radar",
    "outreach_draft",
    "support",
    "proof_pack",
    "expansion",
)


# Step owner taxonomy (matches Decision Passport Owner Literal).
StepOwner = Literal["founder", "csm", "sales_rep", "customer", "system_auto"]

# Action mode taxonomy (matches Engine 6 ActionType / canonical 5 modes).
StepActionMode = Literal[
    "suggest_only", "draft_only", "approval_required",
    "approved_manual", "blocked",
]


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    """A single step in a delivery workflow."""

    step_id: str
    day: int
    title_ar: str
    title_en: str
    owner: StepOwner
    daily_artifact_required: bool
    artifact_kind: str
    risk_level: Literal["low", "medium", "high"]
    next_action_kind: str
    approval_points: tuple[str, ...] = field(default_factory=tuple)
    blockers_ar: tuple[str, ...] = field(default_factory=tuple)
    blockers_en: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    """A complete workflow YAML loaded into memory."""

    name: WorkflowName
    duration_days: int
    description_ar: str
    description_en: str
    proof_target: str
    final_deliverable: str
    steps: tuple[WorkflowStep, ...]


class WorkflowLoadError(ValueError):
    """Raised when a workflow YAML is malformed or missing."""


def load_workflow(name: WorkflowName, *, base_dir: Path | None = None) -> WorkflowDefinition:
    """Load a single workflow YAML by name.

    Args:
        name: Canonical workflow name (must be in CANONICAL_WORKFLOWS).
        base_dir: Override workflows directory (for tests).

    Returns:
        WorkflowDefinition (frozen).

    Raises:
        WorkflowLoadError: missing file, malformed YAML, or schema mismatch.
    """
    if name not in CANONICAL_WORKFLOWS:
        raise WorkflowLoadError(
            f"unknown workflow {name!r}; must be one of {CANONICAL_WORKFLOWS}"
        )
    base = base_dir or WORKFLOWS_DIR
    path = base / f"{name}.yaml"
    if not path.exists():
        raise WorkflowLoadError(f"workflow YAML missing: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise WorkflowLoadError(f"malformed YAML at {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise WorkflowLoadError(f"workflow YAML at {path} must be a mapping")

    # Required top-level keys
    required = {"name", "duration_days", "description_ar", "description_en",
                "proof_target", "final_deliverable", "steps"}
    missing = required - set(data.keys())
    if missing:
        raise WorkflowLoadError(f"workflow {name} missing keys: {missing}")

    if data["name"] != name:
        raise WorkflowLoadError(
            f"workflow file {path} declares name={data['name']!r} but loaded as {name!r}"
        )

    # Parse steps
    raw_steps = data.get("steps") or []
    if not isinstance(raw_steps, list):
        raise WorkflowLoadError(f"workflow {name} 'steps' must be a list")

    steps: list[WorkflowStep] = []
    for i, raw in enumerate(raw_steps):
        if not isinstance(raw, dict):
            raise WorkflowLoadError(f"workflow {name} step {i} must be a mapping")
        step_required = {
            "step_id", "day", "title_ar", "title_en", "owner",
            "daily_artifact_required", "artifact_kind",
            "risk_level", "next_action_kind",
        }
        step_missing = step_required - set(raw.keys())
        if step_missing:
            raise WorkflowLoadError(
                f"workflow {name} step {i} missing keys: {step_missing}"
            )
        steps.append(WorkflowStep(
            step_id=str(raw["step_id"]),
            day=int(raw["day"]),
            title_ar=str(raw["title_ar"]),
            title_en=str(raw["title_en"]),
            owner=raw["owner"],
            daily_artifact_required=bool(raw["daily_artifact_required"]),
            artifact_kind=str(raw["artifact_kind"]),
            risk_level=raw["risk_level"],
            next_action_kind=str(raw["next_action_kind"]),
            approval_points=tuple(raw.get("approval_points") or ()),
            blockers_ar=tuple(raw.get("blockers_ar") or ()),
            blockers_en=tuple(raw.get("blockers_en") or ()),
        ))

    return WorkflowDefinition(
        name=name,
        duration_days=int(data["duration_days"]),
        description_ar=str(data["description_ar"]),
        description_en=str(data["description_en"]),
        proof_target=str(data["proof_target"]),
        final_deliverable=str(data["final_deliverable"]),
        steps=tuple(steps),
    )


def load_all_workflows(*, base_dir: Path | None = None) -> dict[WorkflowName, WorkflowDefinition]:
    """Load all 7 canonical workflows. Raises if any is missing/malformed."""
    return {name: load_workflow(name, base_dir=base_dir) for name in CANONICAL_WORKFLOWS}


# ─────────────────────────────────────────────────────────────────────
# Daily Artifact Enforcer (Article 8 — no "اشتغلنا" without proof)
# ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class DailyArtifactReport:
    """Result of running the artifact enforcer on a session."""

    session_id: str
    workflow_name: WorkflowName
    days_elapsed: int
    expected_artifacts: int
    recorded_artifacts: int
    missing_artifact_days: tuple[int, ...]
    blocked: bool
    blocker_reason_ar: str
    blocker_reason_en: str


def check_daily_artifacts(
    *,
    session_id: str,
    workflow_name: WorkflowName,
    started_at: date,
    recorded_artifact_days: list[int] | tuple[int, ...],
    on_date: date | None = None,
    grace_days: int = 1,
) -> DailyArtifactReport:
    """Check whether a session has artifacts recorded for each elapsed day.

    Hard rule (Article 8): if a session has gone >grace_days without
    a recorded artifact, the enforcer flags it as ``blocked=True`` and
    provides a bilingual reason. The caller (founder dashboard) shows
    the blocker prominently.

    Args:
        session_id: Service session identifier.
        workflow_name: One of the 7 canonical workflows.
        started_at: When the session started (date).
        recorded_artifact_days: List of day-numbers (1-indexed) that
            already have artifacts on file.
        on_date: Reference date (default: today UTC).
        grace_days: How many days a session can go without an artifact
            before being flagged. Default 1 (yesterday + today both
            missing → blocked).

    Returns:
        DailyArtifactReport — never raises.
    """
    today = on_date or datetime.now(timezone.utc).date()
    days_elapsed = max(0, (today - started_at).days + 1)

    # Days 1..days_elapsed must have artifacts (or be flagged)
    expected = list(range(1, days_elapsed + 1))
    recorded_set = set(int(d) for d in recorded_artifact_days)
    missing = tuple(d for d in expected if d not in recorded_set)

    # Block when consecutive missing exceeds grace_days
    if not missing:
        return DailyArtifactReport(
            session_id=session_id, workflow_name=workflow_name,
            days_elapsed=days_elapsed,
            expected_artifacts=len(expected),
            recorded_artifacts=len(expected),
            missing_artifact_days=(),
            blocked=False,
            blocker_reason_ar="",
            blocker_reason_en="",
        )

    consecutive_missing = _max_consecutive_run(missing, days_elapsed)
    blocked = consecutive_missing > grace_days

    if blocked:
        ar = (
            f"الجلسة {session_id} في تدفق {workflow_name} مرَّت "
            f"{consecutive_missing} أيام بدون مخرَج (Article 8)."
        )
        en = (
            f"Session {session_id} in workflow {workflow_name} has gone "
            f"{consecutive_missing} consecutive days without an artifact "
            f"(Article 8 — 'اشتغلنا' blocked without proof)."
        )
    else:
        ar = ""
        en = ""

    return DailyArtifactReport(
        session_id=session_id, workflow_name=workflow_name,
        days_elapsed=days_elapsed,
        expected_artifacts=len(expected),
        recorded_artifacts=len(expected) - len(missing),
        missing_artifact_days=missing,
        blocked=blocked,
        blocker_reason_ar=ar,
        blocker_reason_en=en,
    )


def _max_consecutive_run(missing: tuple[int, ...], total_days: int) -> int:
    """Compute the longest run of consecutive missing days
    ending at ``total_days`` (the current day).

    We care most about the trailing run because old missing days
    might be deliberately skipped (vacation, holiday) but a current
    streak means the session is stuck NOW.
    """
    if not missing:
        return 0
    missing_set = set(missing)
    run = 0
    d = total_days
    while d >= 1 and d in missing_set:
        run += 1
        d -= 1
    return run
