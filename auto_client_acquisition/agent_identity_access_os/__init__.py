"""Agent Identity & Access OS — session and chain gates."""

from __future__ import annotations

from auto_client_acquisition.agent_identity_access_os.agent_access import (
    AgentAccessBinding,
    access_binding_valid,
)
from auto_client_acquisition.agent_identity_access_os.agent_identity import (
    AgentIdentity,
    agent_identity_valid,
)
from auto_client_acquisition.agent_identity_access_os.chain_control import (
    AgentChainDeclaration,
    chain_declaration_valid,
)
from auto_client_acquisition.agent_identity_access_os.permission_review import (
    PERMISSION_REVIEW_SIGNALS,
    permission_review_coverage_score,
)
from auto_client_acquisition.agent_identity_access_os.session_control import (
    AgentSessionScope,
    session_allows_context,
)

__all__ = [
    "PERMISSION_REVIEW_SIGNALS",
    "AgentAccessBinding",
    "AgentChainDeclaration",
    "AgentIdentity",
    "AgentSessionScope",
    "access_binding_valid",
    "agent_identity_valid",
    "chain_declaration_valid",
    "permission_review_coverage_score",
    "session_allows_context",
]
