"""Dealix Secure Agent Runtime OS."""

from __future__ import annotations

from auto_client_acquisition.secure_agent_runtime_os.agent_runtime_states import (
    AgentRuntimeState,
    RUNTIME_STATE_TRANSITIONS,
    is_valid_transition,
)
from auto_client_acquisition.secure_agent_runtime_os.deployment_rings import (
    DEPLOYMENT_RINGS,
    DeploymentRing,
)
from auto_client_acquisition.secure_agent_runtime_os.prompt_integrity import (
    PromptEnvelope,
    PromptTrust,
)
from auto_client_acquisition.secure_agent_runtime_os.risk_memory import (
    RuntimeRiskMemory,
    update_risk_memory,
)

__all__ = [
    "AgentRuntimeState",
    "RUNTIME_STATE_TRANSITIONS",
    "is_valid_transition",
    "DEPLOYMENT_RINGS",
    "DeploymentRing",
    "PromptEnvelope",
    "PromptTrust",
    "RuntimeRiskMemory",
    "update_risk_memory",
]
