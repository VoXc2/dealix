"""Enterprise rollout & operating adoption playbook."""

from __future__ import annotations

from auto_client_acquisition.enterprise_rollout_os.adoption_gates import (
    ENTERPRISE_ADOPTION_GATES,
    enterprise_gate_passes,
)
from auto_client_acquisition.enterprise_rollout_os.enterprise_risk import (
    ENTERPRISE_ROLLOUT_CONTROLS,
    ENTERPRISE_ROLLOUT_RISK_IDS,
)
from auto_client_acquisition.enterprise_rollout_os.platform_pull import (
    PLATFORM_PULL_SIGNALS,
    platform_pull_coverage_score,
)
from auto_client_acquisition.enterprise_rollout_os.role_map import (
    ENTERPRISE_ROLLOUT_ROLES,
)
from auto_client_acquisition.enterprise_rollout_os.rollout_dashboard import (
    ROLLOUT_DASHBOARD_SIGNALS,
    rollout_dashboard_coverage_score,
)
from auto_client_acquisition.enterprise_rollout_os.rollout_kit import (
    ROLLOUT_KIT_ITEMS,
    rollout_kit_coverage_score,
)
from auto_client_acquisition.enterprise_rollout_os.rollout_stage import (
    ROLLOUT_STAGES,
    rollout_next_stage,
    rollout_stage_index,
)

__all__ = (
    "ENTERPRISE_ADOPTION_GATES",
    "ENTERPRISE_ROLLOUT_CONTROLS",
    "ENTERPRISE_ROLLOUT_RISK_IDS",
    "ENTERPRISE_ROLLOUT_ROLES",
    "PLATFORM_PULL_SIGNALS",
    "ROLLOUT_DASHBOARD_SIGNALS",
    "ROLLOUT_KIT_ITEMS",
    "ROLLOUT_STAGES",
    "enterprise_gate_passes",
    "platform_pull_coverage_score",
    "rollout_dashboard_coverage_score",
    "rollout_kit_coverage_score",
    "rollout_next_stage",
    "rollout_stage_index",
)
