"""Dealix Agent Identity, Access & Kill-Switch OS.

Companion doc: ``docs/agent_identity_access/AGENT_IDENTITY_ACCESS_KILL_SWITCH.md``.
"""

from __future__ import annotations

from auto_client_acquisition.agent_identity_access_os.access_classes import (
    ACCESS_CLASSES,
    AccessClass,
    AccessCard,
    is_access_allowed_in_mvp,
)
from auto_client_acquisition.agent_identity_access_os.agent_identity import (
    AgentIdentityCard,
    AgentRiskTier,
)
from auto_client_acquisition.agent_identity_access_os.kill_switch import (
    KILL_SWITCH_TRIGGERS,
    KillEvent,
    KillSwitchTrigger,
    KillType,
)
from auto_client_acquisition.agent_identity_access_os.session_control import (
    AgentSession,
)

__all__ = [
    "ACCESS_CLASSES",
    "AccessClass",
    "AccessCard",
    "is_access_allowed_in_mvp",
    "AgentIdentityCard",
    "AgentRiskTier",
    "KILL_SWITCH_TRIGGERS",
    "KillEvent",
    "KillSwitchTrigger",
    "KillType",
    "AgentSession",
]
