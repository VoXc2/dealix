"""Agent Audit Levels — L1..L4."""

from __future__ import annotations

from enum import IntEnum


class AgentAuditLevel(IntEnum):
    L1_BASIC_LOGGING = 1
    L2_GOVERNANCE_LOGGING = 2
    L3_HUMAN_REVIEW_LOGGING = 3
    L4_ENTERPRISE_AUDIT = 4


AGENT_AUDIT_LEVELS: tuple[AgentAuditLevel, ...] = tuple(AgentAuditLevel)
