"""Kill Switch — 5 kill types + trigger taxonomy."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class KillSwitchTrigger(str, Enum):
    OWNER_REMOVED = "owner_removed"
    POLICY_VIOLATION = "policy_violation"
    UNEXPECTED_TOOL_REQUEST = "unexpected_tool_request"
    ATTEMPTED_EXTERNAL_ACTION = "attempted_external_action"
    PII_EXPOSURE_RISK = "pii_exposure_risk"
    REPEATED_LOW_QA = "repeated_low_qa_score"
    CLIENT_BOUNDARY_VIOLATION = "client_boundary_violation"
    PROMPT_INJECTION_SUSPECTED = "prompt_injection_suspected"
    UNUSED_90_DAYS = "unused_90_days"


KILL_SWITCH_TRIGGERS: tuple[KillSwitchTrigger, ...] = tuple(KillSwitchTrigger)


class KillType(str, Enum):
    SOFT_KILL = "soft_kill"          # pause session
    TOOL_KILL = "tool_kill"          # revoke a tool
    CLIENT_KILL = "client_kill"      # block agent per client/project
    AGENT_KILL = "agent_kill"        # disable agent globally
    FLEET_KILL = "fleet_kill"        # pause all agents of a class


@dataclass(frozen=True)
class KillEvent:
    kill_event_id: str
    kill_type: KillType
    agent_id: str
    trigger: KillSwitchTrigger
    reason: str
    incident_id: str | None = None
    reactivation_required: str = "governance_review"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tool_revoked: str | None = None
    affected_client_id: str | None = None
