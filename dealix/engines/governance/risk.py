"""
Risk snapshot — a thin facade composing existing Dealix risk signals.

No new scoring logic lives here. It aggregates signals that already exist:
the always-available NEVER_AUTO_EXECUTE set, the Saudi governance policy
registry, and the importability of the risk subsystems. Where a source is
unavailable it is reported in `degraded` — never silently dropped.
"""

from __future__ import annotations

import importlib

from pydantic import BaseModel, ConfigDict, Field

from dealix.classifications import NEVER_AUTO_EXECUTE

_RISK_SUBSYSTEMS: tuple[str, ...] = (
    "auto_client_acquisition.compliance_os.risk_engine",
    "auto_client_acquisition.secure_agent_runtime_os.risk_memory",
    "auto_client_acquisition.agentic_operations_os.agent_risk_score",
)


class RiskSnapshot(BaseModel):
    """Aggregated, read-only risk posture across existing Dealix signals."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0"
    never_auto_execute_actions: list[str] = Field(default_factory=list)
    policy_registry_version: int = 0
    forbidden_actions: list[str] = Field(default_factory=list)
    risk_subsystems_available: dict[str, bool] = Field(default_factory=dict)
    degraded: list[str] = Field(default_factory=list)


def build_risk_snapshot() -> RiskSnapshot:
    """Compose the current risk posture from existing signals."""
    degraded: list[str] = []

    registry_version = 0
    forbidden: list[str] = []
    try:
        from auto_client_acquisition.governance_os.policy_registry import (
            forbidden_actions,
            load_policy_registry,
        )

        reg = load_policy_registry()
        registry_version = int(reg.get("version", 0))
        forbidden = sorted(forbidden_actions())
    except Exception as exc:
        degraded.append(f"policy_registry unavailable: {exc!r}")

    subsystems: dict[str, bool] = {}
    for module_path in _RISK_SUBSYSTEMS:
        try:
            importlib.import_module(module_path)
            subsystems[module_path] = True
        except Exception as exc:
            subsystems[module_path] = False
            degraded.append(f"{module_path} unavailable: {exc!r}")

    return RiskSnapshot(
        never_auto_execute_actions=sorted(NEVER_AUTO_EXECUTE),
        policy_registry_version=registry_version,
        forbidden_actions=forbidden,
        risk_subsystems_available=subsystems,
        degraded=degraded,
    )
