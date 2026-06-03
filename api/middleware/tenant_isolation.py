"""Wave 12.6 §33.2.6 — Tenant Isolation Middleware.

FastAPI middleware + dependency that enforces multi-tenant isolation
on every request, defending against OWASP API1:2023 BOLA (Broken
Object-Level Authorization).

Pattern (research-validated, FastAPI 2026 best practice):
1. Resolve ``tenant_id`` from one of: JWT claim · X-Tenant-ID header ·
   API key prefix · subdomain
2. Inject into ``request.state.tenant_id``
3. Every repository function calls ``assert_tenant_match(request, obj)``
   before returning customer-scoped data
4. Cross-tenant access raises ``CrossTenantAccessDenied`` (HTTP 403)

Reuses ``api/security/rbac.py`` Role enum + ``api/security/auth_deps.py``
``TenantID`` dependency.

Source: https://blog.greeden.me/en/2026/03/10/introduction-to-multi-tenant-design-with-fastapi-practical-patterns-for-tenant-isolation-authorization-database-strategy-and-audit-logs/
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


class CrossTenantAccessDenied(Exception):
    """Raised when a request attempts to access data outside its tenant.

    Caller (FastAPI route handler / dependency) catches and converts to
    HTTPException(403). The exception itself stays generic so it can
    be raised from non-HTTP contexts (background jobs, CLI scripts).

    Attributes:
        request_tenant: The tenant_id resolved from the request context.
        object_tenant: The tenant_id stamped on the requested object.
        object_type: e.g. "lead" / "customer" / "proof_event".
        object_id: The object identifier (for audit log).
    """

    def __init__(
        self,
        *,
        request_tenant: str,
        object_tenant: str,
        object_type: str,
        object_id: str,
    ) -> None:
        self.request_tenant = request_tenant
        self.object_tenant = object_tenant
        self.object_type = object_type
        self.object_id = object_id
        super().__init__(
            f"Cross-tenant access blocked: request_tenant={request_tenant!r} "
            f"object_tenant={object_tenant!r} object_type={object_type!r} "
            f"object_id={object_id!r}"
        )


@dataclass(frozen=True, slots=True)
class TenantContext:
    """The tenant context for a request.

    Resolved by ``resolve_tenant_context()`` and injected into
    ``request.state.tenant_context``.
    """

    tenant_id: str
    """The resolved tenant identifier (NEVER empty when valid)."""

    source: Literal["jwt", "header", "api_key", "subdomain", "test_override"]
    """Where the tenant_id came from — for audit + debug."""

    user_id: str = ""
    """The authenticated user (when available)."""

    is_super_admin: bool = False
    """When True, bypasses tenant_isolation (cross-tenant reads allowed)
    for system-admin operations. Use SPARINGLY — every super-admin
    access MUST be audit-logged separately."""


# Resolution order (priority high → low):
# 1. test_override via direct kwarg (testing only)
# 2. JWT claim ``tenant_id``
# 3. ``X-Tenant-ID`` header (B2B API key auth)
# 4. API key prefix (e.g. ``apikey_acme_xxx`` → tenant=``acme``)
# 5. Subdomain (e.g. ``acme.api.dealix.me`` → tenant=``acme``)


def resolve_tenant_context(
    *,
    jwt_claim_tenant_id: str | None = None,
    header_tenant_id: str | None = None,
    api_key: str | None = None,
    host: str | None = None,
    user_id: str = "",
    is_super_admin: bool = False,
    test_override: str | None = None,
) -> TenantContext:
    """Resolve the tenant_id for the current request.

    Args:
        jwt_claim_tenant_id: From verified JWT (api/security/jwt.py).
        header_tenant_id: From X-Tenant-ID header (B2B API).
        api_key: From X-API-Key header — extract tenant from prefix.
        host: From Host header — extract tenant from subdomain.
        user_id: Authenticated user (for audit).
        is_super_admin: When True, no tenant required.
        test_override: Test injection — highest priority.

    Returns:
        TenantContext (frozen).

    Raises:
        CrossTenantAccessDenied: when no tenant could be resolved AND
            user is not super_admin.
    """
    # Test override
    if test_override:
        return TenantContext(
            tenant_id=test_override, source="test_override",
            user_id=user_id, is_super_admin=is_super_admin,
        )

    # Super admin doesn't need a tenant (but logs the access)
    if is_super_admin:
        return TenantContext(
            tenant_id="__super_admin__",
            source="jwt",  # super admin must come from verified JWT
            user_id=user_id, is_super_admin=True,
        )

    # 1. JWT claim (highest trust)
    if jwt_claim_tenant_id:
        return TenantContext(
            tenant_id=jwt_claim_tenant_id, source="jwt",
            user_id=user_id, is_super_admin=False,
        )

    # 2. X-Tenant-ID header
    if header_tenant_id:
        return TenantContext(
            tenant_id=header_tenant_id, source="header",
            user_id=user_id, is_super_admin=False,
        )

    # 3. API key prefix → tenant
    if api_key:
        parsed = _parse_tenant_from_api_key(api_key)
        if parsed:
            return TenantContext(
                tenant_id=parsed, source="api_key",
                user_id=user_id, is_super_admin=False,
            )

    # 4. Subdomain
    if host:
        parsed = _parse_tenant_from_host(host)
        if parsed:
            return TenantContext(
                tenant_id=parsed, source="subdomain",
                user_id=user_id, is_super_admin=False,
            )

    # No tenant resolved + not super admin → REJECT
    raise CrossTenantAccessDenied(
        request_tenant="(none)",
        object_tenant="(any)",
        object_type="request",
        object_id="(no_tenant_in_request)",
    )


def assert_tenant_match(
    *,
    request_tenant: str,
    object_tenant: str,
    object_type: str,
    object_id: str,
    is_super_admin: bool = False,
) -> None:
    """Hard-rule guard — raises ``CrossTenantAccessDenied`` on mismatch.

    Every repository function that returns customer-scoped data MUST
    call this BEFORE returning. Defense in depth — the middleware
    pre-filters but per-object check catches issues like joined queries
    or background jobs that bypass the request layer.

    Args:
        request_tenant: From ``request.state.tenant_context.tenant_id``.
        object_tenant: From the requested object's ``tenant_id`` field.
        object_type: For audit log (e.g. "lead", "proof_event").
        object_id: For audit log.
        is_super_admin: When True, allows cross-tenant access (still
            recorded in audit log by caller).

    Raises:
        CrossTenantAccessDenied: when tenants mismatch and not super admin.
    """
    if is_super_admin:
        return  # super admin can read across tenants
    if not request_tenant or not object_tenant:
        # Either missing → block (Article 8 — never silent fallback)
        raise CrossTenantAccessDenied(
            request_tenant=request_tenant or "(empty)",
            object_tenant=object_tenant or "(empty)",
            object_type=object_type,
            object_id=object_id,
        )
    if request_tenant != object_tenant:
        raise CrossTenantAccessDenied(
            request_tenant=request_tenant,
            object_tenant=object_tenant,
            object_type=object_type,
            object_id=object_id,
        )


def filter_tenant_scoped_list(
    items: list[Any],
    *,
    request_tenant: str,
    tenant_id_attr: str = "tenant_id",
    is_super_admin: bool = False,
) -> list[Any]:
    """Filter a list to only items matching the request's tenant.

    Use when fetching collections — repository returns the unfiltered
    list, this helper enforces the boundary defensively. Super admin
    bypasses (returns the full list).

    Args:
        items: The unfiltered list (each item must have tenant_id_attr).
        request_tenant: From ``request.state.tenant_context.tenant_id``.
        tenant_id_attr: Attribute name on each item (default "tenant_id").
        is_super_admin: When True, returns items unchanged.

    Returns:
        Filtered list. Items without the attribute are EXCLUDED (Article 8 —
        unknown ownership = blocked).
    """
    if is_super_admin:
        return list(items)
    out: list[Any] = []
    for item in items:
        # Support both dict and dataclass/Pydantic
        if hasattr(item, tenant_id_attr):
            obj_tenant = getattr(item, tenant_id_attr, "")
        elif isinstance(item, dict):
            obj_tenant = item.get(tenant_id_attr, "")
        else:
            continue  # unknown ownership → exclude
        if obj_tenant == request_tenant:
            out.append(item)
    return out


# ─────────────────────────────────────────────────────────────────────
# Internal parsers
# ─────────────────────────────────────────────────────────────────────


def _parse_tenant_from_api_key(api_key: str) -> str | None:
    """Extract tenant from API key prefix.

    Convention: ``apikey_<tenant>_<random>`` or ``dealix_<tenant>_<random>``.
    Examples:
      ``apikey_acme_real_estate_xyz789`` → ``acme_real_estate``
      ``dealix_pilot_abc123`` → ``pilot``

    Returns None if format doesn't match — caller falls through to
    other resolution methods.
    """
    if not api_key:
        return None
    parts = api_key.strip().split("_")
    if len(parts) < 3:
        return None
    if parts[0] not in ("apikey", "dealix"):
        return None
    # Tenant is everything between prefix and last segment (random part)
    tenant_parts = parts[1:-1]
    if not tenant_parts:
        return None
    tenant = "_".join(tenant_parts)
    # Sanity: must be alphanumeric + hyphen/underscore
    if not all(c.isalnum() or c in "_-" for c in tenant):
        return None
    if len(tenant) > 64:
        return None
    return tenant


def _parse_tenant_from_host(host: str) -> str | None:
    """Extract tenant from subdomain.

    Convention: ``<tenant>.api.dealix.me`` → ``<tenant>``.
    The reserved subdomains (api / www / dealix) return None.

    Returns None if format doesn't match — caller falls through.
    """
    if not host:
        return None
    host = host.strip().lower().split(":")[0]  # drop port
    parts = host.split(".")
    # Need at least: subdomain.api.dealix.me (4 parts) or subdomain.dealix.me (3 parts)
    if len(parts) < 3:
        return None
    subdomain = parts[0]
    if subdomain in ("api", "www", "dealix", "app", "admin"):
        return None
    if not all(c.isalnum() or c in "-" for c in subdomain):
        return None
    if len(subdomain) > 64:
        return None
    return subdomain
