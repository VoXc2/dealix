"""Platform v10 — reference contracts only (no stack replacement).

Per DEALIX_CAPABILITY_GAP_MAP §11: storage, auth, tenant, and RLS contracts
for future adapters while FastAPI + Postgres remain primary.
"""

from auto_client_acquisition.platform_v10.auth_contract import (
    AuthPrincipal,
    Permission,
    require_permission,
)
from auto_client_acquisition.platform_v10.rls_contract import (
    RLSPolicy,
    row_tenant_matches,
)
from auto_client_acquisition.platform_v10.storage_contract import (
    ObjectStorageContract,
    StoredObjectRef,
)
from auto_client_acquisition.platform_v10.tenant_contract import (
    TenantContext,
    assert_same_tenant,
)

__all__ = [
    "AuthPrincipal",
    "Permission",
    "ObjectStorageContract",
    "RLSPolicy",
    "StoredObjectRef",
    "TenantContext",
    "assert_same_tenant",
    "require_permission",
    "row_tenant_matches",
]
