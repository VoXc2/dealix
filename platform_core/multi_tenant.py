"""Multi-tenant facade — re-exports existing tenant isolation primitives.

Every governed entity carries ``tenant_id``. Isolation is enforced in the
app layer today (``RLSPolicy``) and at the DB layer via row-level security
in production.
"""

from __future__ import annotations

from auto_client_acquisition.agent_identity_access_os.agent_identity import (
    AgentIdentity,
    agent_identity_valid,
)
from auto_client_acquisition.platform_v10.rls_contract import RLSPolicy, row_tenant_matches
from db.models import TenantRecord

TENANT_COLUMN = "tenant_id"

__all__ = [
    "TENANT_COLUMN",
    "AgentIdentity",
    "RLSPolicy",
    "TenantRecord",
    "agent_identity_valid",
    "row_tenant_matches",
]
