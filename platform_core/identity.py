"""Identity facade — agent IAM records and human user accounts.

Agent identity (``AgentIdentity``) is the IAM layer; ``AgentAccessBinding``
scopes tool sets to a tenant; ``UserRecord`` is the human account model.
"""

from __future__ import annotations

from auto_client_acquisition.agent_identity_access_os.agent_access import (
    AgentAccessBinding,
    access_binding_valid,
)
from auto_client_acquisition.agent_identity_access_os.agent_identity import (
    AgentIdentity,
    agent_identity_valid,
)
from db.models import UserRecord

__all__ = [
    "AgentAccessBinding",
    "AgentIdentity",
    "UserRecord",
    "access_binding_valid",
    "agent_identity_valid",
]
