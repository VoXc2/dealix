"""Agent OS — governed agent identity, lifecycle, permissions, and telemetry.

The canonical runtime spine for Dealix agents. Honors the 11 non-negotiables:
no agent without identity, owner, scope, and audit; L4+ needs a kill-switch
owner; L5 is blocked in the MVP; forbidden tools are hard-blocked.
"""

from auto_client_acquisition.agent_os.agent_card import (
    RISK_LEVELS,
    AgentCard,
    agent_card_valid,
    new_card,
    valid_risk_level,
)
from auto_client_acquisition.agent_os.agent_escalation import (
    EscalationDecision,
    EscalationTrigger,
    escalation_for_card,
    evaluate_escalation,
)
from auto_client_acquisition.agent_os.agent_handoff import (
    HandoffEnvelope,
    HandoffValidation,
    accept_handoff,
    new_handoff,
    validate_handoff,
)
from auto_client_acquisition.agent_os.agent_kpi import (
    AgentKPI,
    KPIValidation,
    kpi_attainment,
    new_kpi,
    validate_kpi,
)
from auto_client_acquisition.agent_os.agent_lifecycle import (
    AgentLifecycleState,
    kill_agent,
    lifecycle_allows_production_tools,
)
from auto_client_acquisition.agent_os.agent_memory_contract import (
    AgentMemoryContract,
    DataClass,
    LawfulBasis,
    MemoryItem,
    MemoryValidation,
    is_expired,
    new_memory_contract,
    validate_memory_contract,
)
from auto_client_acquisition.agent_os.agent_performance import (
    AgentPerformanceSummary,
    summarize_agent,
    summarize_all,
)
from auto_client_acquisition.agent_os.agent_permissions import (
    BUILT_IN_ROLES,
    OperationType,
    PermissionDecision,
    PermissionResult,
    card_permission,
    evaluate_permission,
)
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    clear_for_test,
    get_agent,
    list_agents,
    register_agent,
    update_agent,
)
from auto_client_acquisition.agent_os.agent_status import (
    DEFAULT_STATUS,
    AgentStatus,
    valid_status,
)
from auto_client_acquisition.agent_os.autonomy_levels import (
    DEFAULT_AUTONOMY,
    AutonomyLevel,
    autonomy_blocked_in_mvp,
    coerce_autonomy,
    requires_kill_switch_owner,
)
from auto_client_acquisition.agent_os.tool_permissions import (
    ALLOWED_TOOLS_MVP,
    FORBIDDEN_TOOLS_MVP,
    forbidden_tools_in,
    is_tool_allowed,
    tool_allowed_mvp,
)

__all__ = [
    "ALLOWED_TOOLS_MVP",
    "BUILT_IN_ROLES",
    "DEFAULT_AUTONOMY",
    "DEFAULT_STATUS",
    "FORBIDDEN_TOOLS_MVP",
    "RISK_LEVELS",
    "AgentCard",
    "AgentKPI",
    "AgentLifecycleState",
    "AgentMemoryContract",
    "AgentPerformanceSummary",
    "AgentStatus",
    "AutonomyLevel",
    "DataClass",
    "EscalationDecision",
    "EscalationTrigger",
    "HandoffEnvelope",
    "HandoffValidation",
    "KPIValidation",
    "LawfulBasis",
    "MemoryItem",
    "MemoryValidation",
    "OperationType",
    "PermissionDecision",
    "PermissionResult",
    "accept_handoff",
    "agent_card_valid",
    "autonomy_blocked_in_mvp",
    "card_permission",
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "coerce_autonomy",
    "escalation_for_card",
    "evaluate_escalation",
    "evaluate_permission",
    "forbidden_tools_in",
    "get_agent",
    "is_expired",
    "is_tool_allowed",
    "kill_agent",
    "kpi_attainment",
    "lifecycle_allows_production_tools",
    "list_agents",
    "new_card",
    "new_handoff",
    "new_kpi",
    "new_memory_contract",
    "register_agent",
    "requires_kill_switch_owner",
    "summarize_agent",
    "summarize_all",
    "tool_allowed_mvp",
    "update_agent",
    "valid_risk_level",
    "valid_status",
    "validate_handoff",
    "validate_kpi",
    "validate_memory_contract",
]
