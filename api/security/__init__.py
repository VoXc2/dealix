"""Security module — rate limiting, API keys, JWT auth, RBAC, webhook verification."""

from api.security.api_key import (
    APIKeyMiddleware,
    require_admin_key,
    verify_admin_key,
    verify_api_key,
)
from api.security.auth_deps import (
    CurrentUser,
    OptionalUser,
    TenantID,
    get_current_user,
    get_optional_user,
    get_tenant_id,
    require_sales_manager,
    require_sales_rep,
    require_super_admin,
    require_tenant_admin,
    require_viewer,
)
from api.security.jwt import (
    create_access_token,
    create_invite_token,
    create_refresh_token,
    decode_access_token,
    decode_invite_token,
    decode_refresh_token,
    hash_token,
    verify_token_hash,
)
from api.security.rate_limit import limiter, setup_rate_limit
from api.security.rbac import (
    DEFAULT_TENANT_ROLES,
    ROLE_PERMISSIONS,
    Role,
    SystemRole,
    has_permission,
    is_at_least,
    is_super_admin,
)
from api.security.webhook_signatures import (
    verify_calendly_signature,
    verify_hubspot_signature,
    verify_n8n_signature,
)

__all__ = [
    # RBAC
    "DEFAULT_TENANT_ROLES",
    "ROLE_PERMISSIONS",
    # API key
    "APIKeyMiddleware",
    # Auth deps
    "CurrentUser",
    "OptionalUser",
    "Role",
    "SystemRole",
    "TenantID",
    # JWT
    "create_access_token",
    "create_invite_token",
    "create_refresh_token",
    "decode_access_token",
    "decode_invite_token",
    "decode_refresh_token",
    "get_current_user",
    "get_optional_user",
    "get_tenant_id",
    "has_permission",
    "hash_token",
    "is_at_least",
    "is_super_admin",
    # Rate limiting
    "limiter",
    "require_admin_key",
    "require_sales_manager",
    "require_sales_rep",
    "require_super_admin",
    "require_tenant_admin",
    "require_viewer",
    "setup_rate_limit",
    "verify_admin_key",
    "verify_api_key",
    # Webhook signatures
    "verify_calendly_signature",
    "verify_hubspot_signature",
    "verify_n8n_signature",
    "verify_token_hash",
]
