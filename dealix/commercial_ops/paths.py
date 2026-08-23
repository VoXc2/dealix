"""Repository and runtime-state paths for commercial operations."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_REPO_ROOT_REAL = REPO_ROOT.resolve()
_RUNTIME_ROOT_RAW = (os.environ.get("DEALIX_RUNTIME_STATE_ROOT") or "").strip()


def _external_runtime_path(raw: str, *, label: str) -> Path:
    """Resolve a runtime override and fail closed if it can write into Git.

    `resolve(strict=False)` normalizes ``..`` and follows any existing symlink
    components, so both direct and symlink-assisted containment are rejected
    before a caller creates or writes the target.
    """
    candidate = Path(raw).expanduser().resolve(strict=False)
    if candidate == Path("/"):
        raise RuntimeError(f"{label} must not resolve to filesystem root")
    if candidate == _REPO_ROOT_REAL or _REPO_ROOT_REAL in candidate.parents:
        raise RuntimeError(
            f"{label} must remain outside canonical repository: {candidate}"
        )
    return candidate


RUNTIME_STATE_ROOT = (
    _external_runtime_path(_RUNTIME_ROOT_RAW, label="DEALIX_RUNTIME_STATE_ROOT")
    if _RUNTIME_ROOT_RAW
    else None
)


def _runtime_path(env_name: str, relative: str, canonical: Path) -> Path:
    """Resolve mutable operating state outside the repo when explicitly enabled.

    Local/developer behavior remains unchanged unless DEALIX_RUNTIME_STATE_ROOT
    or a path-specific override is provided. VPS automation sets the runtime
    root so routine state updates do not dirty canonical source-of-truth files.
    Every override is normalized and rejected if it resolves back into Git.
    """
    explicit = (os.environ.get(env_name) or "").strip()
    if explicit:
        return _external_runtime_path(explicit, label=env_name)
    if RUNTIME_STATE_ROOT is not None:
        return _external_runtime_path(
            str(RUNTIME_STATE_ROOT / relative), label=f"{env_name} (runtime root)"
        )
    return canonical


def display_path(path: Path) -> str:
    """Render a path for proof/UI without assuming runtime state lives in Git."""
    try:
        rendered = path.relative_to(REPO_ROOT)
    except ValueError:
        rendered = path
    return str(rendered).replace("\\", "/")


CANONICAL_EVIDENCE_TRACKER_CSV = (
    REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
)
CANONICAL_SOCIAL_QUEUE_YAML = REPO_ROOT / "dealix/config/social_content_queue.yaml"
CANONICAL_WAR_ROOM_TODAY_JSON = REPO_ROOT / "data/war_room_today.json"
CANONICAL_SOFT_LAUNCH_TRACKER_YAML = (
    REPO_ROOT / "docs/commercial/operations/soft_launch_meetings_tracker.yaml"
)

EVIDENCE_TRACKER_CSV = _runtime_path(
    "DEALIX_EVIDENCE_TRACKER_CSV",
    "commercial/evidence_events_tracker.csv",
    CANONICAL_EVIDENCE_TRACKER_CSV,
)
AGENCY_TARGETS_CSV = (
    REPO_ROOT / "docs/commercial/operations/targeting/agency_accounts_seed.csv"
)
SOCIAL_QUEUE_YAML = _runtime_path(
    "DEALIX_SOCIAL_QUEUE_YAML",
    "commercial/social_content_queue.yaml",
    CANONICAL_SOCIAL_QUEUE_YAML,
)
ICP_AGENCY_YAML = REPO_ROOT / "dealix/config/icp_agency_wedge.yaml"
WAR_ROOM_TODAY_JSON = _runtime_path(
    "DEALIX_WAR_ROOM_TODAY_JSON",
    "commercial/war_room_today.json",
    CANONICAL_WAR_ROOM_TODAY_JSON,
)
SOFT_LAUNCH_TRACKER_YAML = _runtime_path(
    "DEALIX_SOFT_LAUNCH_TRACKER_YAML",
    "commercial/soft_launch_meetings_tracker.yaml",
    CANONICAL_SOFT_LAUNCH_TRACKER_YAML,
)
FOUNDER_BRIEFS_DIR = _runtime_path(
    "DEALIX_FOUNDER_BRIEFS_DIR",
    "commercial/founder_briefs",
    REPO_ROOT / "data/founder_briefs",
)
GTM_ABM_WAVE1_YAML = REPO_ROOT / "dealix/config/gtm_abm_wave1.yaml"
FOUNDER_DEBRIEFS_DIR = _runtime_path(
    "DEALIX_FOUNDER_DEBRIEFS_DIR",
    "commercial/founder_debriefs",
    REPO_ROOT / "data/founder_debriefs",
)
GTM_DEBRIEF_TEMPLATE = (
    REPO_ROOT
    / "docs/commercial/operations/founder_meeting_debrief_template.yaml"
)
FOUNDER_GTM_CODIFICATION_REGISTRY = (
    REPO_ROOT
    / "docs/commercial/operations/founder_gtm_codification_registry.yaml"
)
FOUNDER_PDPL_PASS_YAML = (
    REPO_ROOT / "docs/commercial/operations/founder_pdpl_compliance_pass.yaml"
)
FOUNDER_WEEKLY_DECISION_DIR = _runtime_path(
    "DEALIX_FOUNDER_WEEKLY_DECISION_DIR",
    "commercial/founder_weekly",
    REPO_ROOT / "data/founder_weekly",
)
FOUNDER_WEEKLY_DECISION_TEMPLATE = (
    REPO_ROOT
    / "docs/commercial/operations/founder_weekly_decision_template.yaml"
)
DEALIX_INTERNAL_WAR_ROOM_CSV = (
    REPO_ROOT
    / "docs/commercial/operations/targeting/dealix_internal_war_room_seed.csv"
)
DEALIX_DOGFOODING_WAR_ROOM_JSON = _runtime_path(
    "DEALIX_DOGFOODING_WAR_ROOM_JSON",
    "commercial/dealix_dogfooding_war_room.json",
    REPO_ROOT / "data/dealix_dogfooding_war_room.json",
)
FOUNDER_MAX_OPS_BACKLOG_YAML = REPO_ROOT / "dealix/config/founder_max_ops_backlog.yaml"
FOUNDER_AGENT_QUEUE_YAML = REPO_ROOT / "dealix/config/founder_agent_task_queue.yaml"
FOUNDER_AGENT_QUEUE_TODAY_JSON = _runtime_path(
    "DEALIX_FOUNDER_AGENT_QUEUE_TODAY_JSON",
    "commercial/founder_agent_queue_today.json",
    REPO_ROOT / "data/founder_agent_queue_today.json",
)
PLATFORM_V10_BACKLOG_YAML = REPO_ROOT / "dealix/config/platform_v10_backlog.yaml"
FOUNDER_NORTH_STAR_YAML = REPO_ROOT / "dealix/config/founder_north_star.yaml"
FOUNDER_EXCELLENCE_OS_YAML = REPO_ROOT / "dealix/config/founder_excellence_os.yaml"
FOUNDER_WELLBEING_YAML = REPO_ROOT / "dealix/config/founder_wellbeing.yaml"
