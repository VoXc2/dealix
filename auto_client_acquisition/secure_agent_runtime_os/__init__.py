"""Secure Agent Runtime OS — kill switch, risk memory, and state evaluation."""

from __future__ import annotations

from auto_client_acquisition.secure_agent_runtime_os.agent_states import AgentRuntimeState
from auto_client_acquisition.secure_agent_runtime_os.context_boundary import untrusted_blob_tamper_score
from auto_client_acquisition.secure_agent_runtime_os.data_boundary import data_boundary_ok
from auto_client_acquisition.secure_agent_runtime_os.deployment_rings import DeploymentRing, production_requires_full_card
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import (
    activate_kill_switch,
    kill_switch_active,
    reset_kill_switch_for_tests,
)
from auto_client_acquisition.secure_agent_runtime_os.policy_engine import runtime_policy_allows_tool
from auto_client_acquisition.secure_agent_runtime_os.prompt_integrity import prompt_integrity_ok
from auto_client_acquisition.secure_agent_runtime_os.risk_memory import (
    append_risk,
    clear_risk_memory_for_tests,
    recent_risks,
)
from auto_client_acquisition.secure_agent_runtime_os.runtime_controller import evaluate_runtime_state
from auto_client_acquisition.secure_agent_runtime_os.tool_boundary import FORBIDDEN_TOOLS_MVP, tool_boundary_ok

__all__ = [
    "AgentRuntimeState",
    "DeploymentRing",
    "FORBIDDEN_TOOLS_MVP",
    "activate_kill_switch",
    "append_risk",
    "clear_risk_memory_for_tests",
    "data_boundary_ok",
    "evaluate_runtime_state",
    "kill_switch_active",
    "production_requires_full_card",
    "prompt_integrity_ok",
    "recent_risks",
    "reset_kill_switch_for_tests",
    "runtime_policy_allows_tool",
    "tool_boundary_ok",
    "untrusted_blob_tamper_score",
]