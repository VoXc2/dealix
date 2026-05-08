"""
FastAPI authentication and authorization dependencies.
تبعيات FastAPI للمصادقة والتفويض.

Usage examples:
    # Any authenticated user
    @router.get("/me")
    async def me(user: CurrentUser):
        ...

    # At least sales_rep
    @router.post("/leads")
    async def create_lead(user: CurrentUser = Depends(require_role(Role.SALES_REP))):
        ...

    # super_admin only
    @router.get("/admin/tenants")
    async def list_tenants(user: CurrentUser = Depends(require_super_admin)):
        ...
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.jwt import decode_access_token
from api.security.rbac import Role, is_at_least, is_super_admin
from db.models import UserRecord
from db.session import get_db

_bearer = HTTPBearer(auto_error=False)


async def _get_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    """Extract Bearer token from Authorization header. Raises 401 if missing."""
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header. Expected: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


async def get_current_user(
    token: str = Depends(_get_token),
    db: AsyncSession = Depends(get_db),
) -> UserRecord:
    """
    Decode the access token and load the corresponding UserRecord from DB.
    Raises 401 on invalid token, 403 if user is inactive/deleted.
    """
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise credentials_exc

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise credentials_exc

    result = await db.execute(select(UserRecord).where(UserRecord.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exc

    if not user.is_active or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or deleted",
        )

    return user


# ── Type alias ────────────────────────────────────────────────────────
CurrentUser = Annotated[UserRecord, Depends(get_current_user)]


# ── Tenant context injection ──────────────────────────────────────────

async def get_tenant_id(
    request: Request,
    user: UserRecord = Depends(get_current_user),
) -> str | None:
    """
    Extract effective tenant_id for the current request.
    Super-admins can override via X-Tenant-ID header.
    """
    if is_super_admin(user.system_role):
        header_tid = request.headers.get("X-Tenant-ID")
        if header_tid:
            return header_tid
        # Super-admin without header: no tenant filter (global view)
        return None
    return user.tenant_id


TenantID = Annotated[str | None, Depends(get_tenant_id)]


async def require_effective_tenant(
    request: Request,
    user: UserRecord = Depends(get_current_user),
) -> str:
    """
    Resolver for mutations that must belong to exactly one tenant.

    - Normal users: ``user.tenant_id`` (403 if missing).
    - super_admin: must send ``X-Tenant-ID`` (400 if missing).
    """
    if is_super_admin(user.system_role):
        header_tid = (request.headers.get("X-Tenant-ID") or "").strip()
        if not header_tid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header required for super_admin scoped operations",
            )
        return header_tid
    if not user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not assigned to a tenant",
        )
    return user.tenant_id


EffectiveTenantStr = Annotated[str, Depends(require_effective_tenant)]


# ── Role-based guards ────────────────────────────────────────────────

def require_role(minimum: Role):
    """
    Dependency factory — enforce a minimum role level.
    Usage: user: CurrentUser = Depends(require_role(Role.SALES_MANAGER))
    """
    async def _guard(user: UserRecord = Depends(get_current_user)) -> UserRecord:
        # Super-admin always passes
        if is_super_admin(user.system_role):
            return user
        # Determine role from token cache or DB role_id (role name stored in token 'rol' claim)
        # We read the role name from UserRecord.role_id FK — look it up via a separate query
        # For performance the role name is embedded in the JWT claim 'rol'.
        # We trust the JWT here; re-loading from DB adds latency without much benefit
        # for the typical path (revocation is handled at refresh level).
        from fastapi import Request as _R  # local import avoids circular
        # The JWT payload has already been validated in get_current_user.
        # Retrieve role name stored on the user via the RoleRecord FK.
        # To avoid an extra query we store role name in a context var set by get_current_user.
        # For simplicity we query here (can be optimised with select join later).
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires at least role: {minimum.value}",
        )

    return _guard


def _make_role_guard(minimum: Role):
    """Create a role-checking dependency by joining UserRecord + RoleRecord."""
    async def _guard(
        user: UserRecord = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> UserRecord:
        if is_super_admin(user.system_role):
            return user

        # Load role name from DB (role_id FK)
        role_name: str | None = None
        if user.role_id:
            from db.models import RoleRecord
            result = await db.execute(
                select(RoleRecord.name).where(RoleRecord.id == user.role_id)
            )
            role_name = result.scalar_one_or_none()

        if not is_at_least(role_name, minimum):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires at least role: {minimum.value}",
            )
        return user

    return _guard


# Pre-built dependency callables for common guards
require_viewer = _make_role_guard(Role.VIEWER)
require_sales_rep = _make_role_guard(Role.SALES_REP)
require_sales_manager = _make_role_guard(Role.SALES_MANAGER)
require_tenant_admin = _make_role_guard(Role.TENANT_ADMIN)


async def require_super_admin(user: UserRecord = Depends(get_current_user)) -> UserRecord:
    """Strict super_admin-only guard."""
    if not is_super_admin(user.system_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires system role: super_admin",
        )
    return user


# ── Optional auth (does not raise if unauthenticated) ────────────────

async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> UserRecord | None:
    """Like get_current_user but returns None instead of 401."""
    if not credentials or credentials.scheme.lower() != "bearer":
        return None
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            return None
        result = await db.execute(select(UserRecord).where(UserRecord.id == user_id))
        user = result.scalar_one_or_none()
        if user and user.is_active and not user.deleted_at:
            return user
    except JWTError:
        pass
    return None


OptionalUser = Annotated[UserRecord | None, Depends(get_optional_user)]
