"""Repository paths for commercial operations."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

EVIDENCE_TRACKER_CSV = (
    REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
)
AGENCY_TARGETS_CSV = (
    REPO_ROOT / "docs/commercial/operations/targeting/agency_accounts_seed.csv"
)
SOCIAL_QUEUE_YAML = REPO_ROOT / "dealix/config/social_content_queue.yaml"
ICP_AGENCY_YAML = REPO_ROOT / "dealix/config/icp_agency_wedge.yaml"
WAR_ROOM_TODAY_JSON = REPO_ROOT / "data/war_room_today.json"
FOUNDER_BRIEFS_DIR = REPO_ROOT / "data/founder_briefs"
GTM_ABM_WAVE1_YAML = REPO_ROOT / "dealix/config/gtm_abm_wave1.yaml"
FOUNDER_DEBRIEFS_DIR = REPO_ROOT / "data/founder_debriefs"
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
FOUNDER_WEEKLY_DECISION_DIR = REPO_ROOT / "data/founder_weekly"
FOUNDER_WEEKLY_DECISION_TEMPLATE = (
    REPO_ROOT
    / "docs/commercial/operations/founder_weekly_decision_template.yaml"
)
DEALIX_INTERNAL_WAR_ROOM_CSV = (
    REPO_ROOT
    / "docs/commercial/operations/targeting/dealix_internal_war_room_seed.csv"
)
DEALIX_DOGFOODING_WAR_ROOM_JSON = REPO_ROOT / "data/dealix_dogfooding_war_room.json"
FOUNDER_MAX_OPS_BACKLOG_YAML = REPO_ROOT / "dealix/config/founder_max_ops_backlog.yaml"
FOUNDER_AGENT_QUEUE_YAML = REPO_ROOT / "dealix/config/founder_agent_task_queue.yaml"
FOUNDER_AGENT_QUEUE_TODAY_JSON = REPO_ROOT / "data/founder_agent_queue_today.json"
PLATFORM_V10_BACKLOG_YAML = REPO_ROOT / "dealix/config/platform_v10_backlog.yaml"
