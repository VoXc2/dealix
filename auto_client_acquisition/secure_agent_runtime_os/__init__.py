"""Canonical Secure Agent Runtime — Wave 4 lite (14F).

Runtime states + four-boundary protection + kill switch for AI agents.
"""
from auto_client_acquisition.secure_agent_runtime_os.runtime_states import (
    RuntimeState,
    can_transition,
    is_safe_to_run,
)
from auto_client_acquisition.secure_agent_runtime_os.four_boundaries import (
    BoundaryCheck,
    check_context_boundary,
    check_data_boundary,
    check_prompt_integrity,
    check_tool_boundary,
    check_all_boundaries,
)
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import (
    activate_kill_switch,
)

__all__ = [
    "BoundaryCheck",
    "RuntimeState",
    "activate_kill_switch",
    "can_transition",
    "check_all_boundaries",
    "check_context_boundary",
    "check_data_boundary",
    "check_prompt_integrity",
    "check_tool_boundary",
    "is_safe_to_run",
]
