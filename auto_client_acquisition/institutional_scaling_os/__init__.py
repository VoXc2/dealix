"""Institutional Scaling Doctrine — deterministic gates for scale discipline."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import AgentControlCard
from auto_client_acquisition.institutional_scaling_os.agent_identity import agent_identity_mvp_ok
from auto_client_acquisition.institutional_scaling_os.control_memo import (
    CONTROL_MEMO_SECTIONS,
    build_control_memo_markdown_skeleton,
    control_memo_complete,
)
from auto_client_acquisition.institutional_scaling_os.institutional_metrics import (
    ScalingDisciplineSnapshot,
    scaling_discipline_blockers,
)
from auto_client_acquisition.institutional_scaling_os.privacy_runtime import (
    PrivacyRuntimeResult,
    privacy_runtime_audit_payload,
    privacy_runtime_outcome,
)
from auto_client_acquisition.institutional_scaling_os.risk_register import (
    InstitutionalRisk,
    RiskRegisterEntry,
    risk_register_entry_valid,
)
from auto_client_acquisition.institutional_scaling_os.trust_engine import (
    TRUST_ENGINE_COMPONENTS,
    trust_engine_coverage_score,
)

__all__ = (
    "CONTROL_MEMO_SECTIONS",
    "TRUST_ENGINE_COMPONENTS",
    "InstitutionalRisk",
    "PrivacyRuntimeResult",
    "RiskRegisterEntry",
    "ScalingDisciplineSnapshot",
    "agent_identity_mvp_ok",
    "build_control_memo_markdown_skeleton",
    "control_memo_complete",
    "privacy_runtime_audit_payload",
    "privacy_runtime_outcome",
    "risk_register_entry_valid",
    "scaling_discipline_blockers",
    "trust_engine_coverage_score",
)
