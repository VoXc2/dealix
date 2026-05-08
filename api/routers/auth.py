"""
Authentication and session management endpoints.
نقاط نهاية المصادقة وإدارة الجلسات.

Endpoints:
  POST /api/v1/auth/register        — create tenant + first admin user
  POST /api/v1/auth/login           — issue access + refresh tokens
  POST /api/v1/auth/refresh         — exchange refresh → new access token
  POST /api/v1/auth/logout          — revoke refresh token (current session)
  POST /api/v1/auth/logout/all      — revoke all sessions for current user
  GET  /api/v1/auth/me              — current user profile
  POST /api/v1/auth/invite          — send invite (tenant_admin+)
  POST /api/v1/auth/invite/accept   — accept invite, set password, create user
  POST /api/v1/auth/mfa/setup       — generate TOTP secret + QR URI
  POST /api/v1/auth/mfa/verify      — verify TOTP code and enable MFA
  POST /api/v1/auth/mfa/disable     — disable MFA (requires password + TOTP)
  POST /api/v1/auth/password/reset-request — send password-reset email
  POST /api/v1/auth/password/reset  — apply new password via reset token
"""

from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import datetime, timezone

import pyotp
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from jose import JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import (
    CurrentUser,
    get_current_user,
    require_super_admin,
    require_tenant_admin,
)
from api.security.jwt import (
    create_access_token,
    create_invite_token,
    create_refresh_token,
    decode_invite_token,
    decode_refresh_token,
    hash_token,
    token_expires_at,
    verify_token_hash,
)
from api.security.rbac import DEFAULT_TENANT_ROLES, Role
from db.models import (
    RefreshTokenRecord,
    RoleRecord,
    TenantRecord,
    UserInviteRecord,
    UserRecord,
)
from db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _new_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:24]}"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _hash_password(plain: str) -> str:
    return _pwd_ctx.hash(plain)


def _verify_password(plain: str, hashed: str) -> bool:
    return _pwd_ctx.verify(plain, hashed)


def _verify_totp(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)


# ── Schemas ────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    tenant_name: str
    tenant_slug: str
    email: EmailStr
    password: str
    name: str = ""

    @field_validator("password")
    @classmethod
    def _strong_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("tenant_slug")
    @classmethod
    def _valid_slug(cls, v: str) -> str:
        import re
        if not re.match(r"^[a-z0-9][a-z0-9\-]{1,62}[a-z0-9]$", v):
            raise ValueError("Slug must be 3-64 lowercase alphanumeric chars/hyphens")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp_code: str | None = None
    tenant_slug: str | None = None  # disambiguate if same email in multiple tenants


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    mfa_required: bool = False


class RefreshRequest(BaseModel):
    refresh_token: str


class InviteRequest(BaseModel):
    email: EmailStr
    role: Role = Role.SALES_REP


class InviteAcceptRequest(BaseModel):
    token: str
    name: str
    password: str

    @field_validator("password")
    @classmethod
    def _strong_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class MFASetupResponse(BaseModel):
    secret: str
    provisioning_uri: str
    qr_data_uri: str | None = None


class MFAVerifyRequest(BaseModel):
    totp_code: str


class MFADisableRequest(BaseModel):
    password: str
    totp_code: str


class PasswordResetRequest(BaseModel):
    email: EmailStr
    tenant_slug: str | None = None


class PasswordResetApply(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def _strong_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserProfileResponse(BaseModel):
    id: str
    email: str
    name: str
    tenant_id: str | None
    role_id: str | None
    system_role: str | None
    mfa_enabled: bool
    is_verified: bool
    created_at: datetime


# ── Helpers ────────────────────────────────────────────────────────

async def _get_role_name(db: AsyncSession, role_id: str | None) -> str | None:
    if not role_id:
        return None
    result = await db.execute(select(RoleRecord.name).where(RoleRecord.id == role_id))
    return result.scalar_one_or_none()


async def _issue_tokens(
    user: UserRecord,
    db: AsyncSession,
    request: Request,
) -> TokenResponse:
    """Create access + refresh tokens, persist refresh token hash."""
    from core.config.settings import get_settings

    settings = get_settings()
    role_name = await _get_role_name(db, user.role_id)

    access_token = create_access_token(
        user_id=user.id,
        tenant_id=user.tenant_id,
        role=role_name,
        system_role=user.system_role,
    )
    refresh_token = create_refresh_token(
        user_id=user.id,
        tenant_id=user.tenant_id,
    )

    # Persist hashed refresh token
    expires_at = token_expires_at(refresh_token)
    token_record = RefreshTokenRecord(
        id=_new_id("rt_"),
        user_id=user.id,
        tenant_id=user.tenant_id,
        token_hash=hash_token(refresh_token),
        ip_address=request.client.host if request.client else None,
        device_info=request.headers.get("User-Agent", "")[:512],
        expires_at=expires_at.replace(tzinfo=None) if expires_at else _utcnow(),
    )
    db.add(token_record)

    # Update last_login_at
    user.last_login_at = _utcnow()
    await db.flush()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.jwt_access_token_expire_minutes * 60,
    )


# ── Endpoints ──────────────────────────────────────────────────────

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def register(
    body: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Register a new tenant + first tenant_admin user.
    Bootstraps the four default system roles for the tenant.
    """
    # Check slug uniqueness
    existing = await db.execute(
        select(TenantRecord).where(TenantRecord.slug == body.tenant_slug)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "Tenant slug already taken")

    tenant_id = _new_id("ten_")
    tenant = TenantRecord(
        id=tenant_id,
        name=body.tenant_name,
        slug=body.tenant_slug,
        plan="pilot",
        status="active",
    )
    db.add(tenant)

    # Bootstrap default roles
    roles: dict[str, RoleRecord] = {}
    for role_def in DEFAULT_TENANT_ROLES:
        r = RoleRecord(
            id=_new_id("rol_"),
            tenant_id=tenant_id,
            name=role_def["name"],
            permissions=role_def["permissions"],
            description=role_def["description"],
            is_system=role_def["is_system"],
        )
        db.add(r)
        roles[role_def["name"]] = r

    await db.flush()  # populate role IDs

    admin_role = roles[Role.TENANT_ADMIN]

    user = UserRecord(
        id=_new_id("usr_"),
        tenant_id=tenant_id,
        role_id=admin_role.id,
        email=body.email,
        name=body.name or body.email.split("@")[0],
        hashed_password=_hash_password(body.password),
        is_active=True,
        is_verified=True,  # first user is auto-verified
    )
    db.add(user)
    await db.flush()

    return await _issue_tokens(user, db, request)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Login — returns access + refresh tokens. MFA required if enabled."""
    stmt = select(UserRecord).where(UserRecord.email == body.email)
    if body.tenant_slug:
        sub = select(TenantRecord.id).where(TenantRecord.slug == body.tenant_slug)
        stmt = stmt.where(UserRecord.tenant_id == sub.scalar_subquery())

    result = await db.execute(stmt)
    users = result.scalars().all()

    # Find the matching user (may exist in multiple tenants with same email)
    user: UserRecord | None = None
    for u in users:
        if u.deleted_at is None and u.is_active and _verify_password(body.password, u.hashed_password):
            user = u
            break

    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid email, password, or tenant",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # MFA check
    if user.mfa_enabled:
        if not body.totp_code:
            return TokenResponse(
                access_token="",
                refresh_token="",
                expires_in=0,
                mfa_required=True,
            )
        if not user.totp_secret or not _verify_totp(user.totp_secret, body.totp_code):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid TOTP code")

    return await _issue_tokens(user, db, request)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    body: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Exchange a valid refresh token for a new access + refresh token pair (rotation)."""
    try:
        payload = decode_refresh_token(body.refresh_token)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token")

    user_id = payload.get("sub")
    token_hash = hash_token(body.refresh_token)

    # Find and validate stored token
    result = await db.execute(
        select(RefreshTokenRecord).where(
            and_(
                RefreshTokenRecord.user_id == user_id,
                RefreshTokenRecord.token_hash == token_hash,
                RefreshTokenRecord.revoked_at.is_(None),
                RefreshTokenRecord.expires_at > _utcnow(),
            )
        )
    )
    stored = result.scalar_one_or_none()
    if not stored:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token not found or revoked")

    # Revoke old token (rotation)
    stored.revoked_at = _utcnow()
    await db.flush()

    user_result = await db.execute(select(UserRecord).where(UserRecord.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active or user.deleted_at:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User no longer active")

    return await _issue_tokens(user, db, request)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    body: RefreshRequest,
    user: UserRecord = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Revoke the supplied refresh token (current session)."""
    token_hash = hash_token(body.refresh_token)
    await db.execute(
        delete(RefreshTokenRecord).where(
            and_(
                RefreshTokenRecord.user_id == user.id,
                RefreshTokenRecord.token_hash == token_hash,
            )
        )
    )


@router.post("/logout/all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Revoke ALL refresh tokens for the current user (sign out everywhere)."""
    await db.execute(
        delete(RefreshTokenRecord).where(RefreshTokenRecord.user_id == user.id)
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_me(user: CurrentUser) -> UserProfileResponse:
    """Return current user profile."""
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        tenant_id=user.tenant_id,
        role_id=user.role_id,
        system_role=user.system_role,
        mfa_enabled=user.mfa_enabled,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )


# ── Invite flow ─────────────────────────────────────────────────────

@router.post("/invite", status_code=status.HTTP_201_CREATED)
async def send_invite(
    body: InviteRequest,
    user: UserRecord = Depends(require_tenant_admin),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Create and return an invite token for the given email.
    Tenant-admin+ only. In production, send via email instead of returning raw token.
    """
    if not user.tenant_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Caller has no tenant context")

    # Resolve role_id for the requested role name
    role_result = await db.execute(
        select(RoleRecord).where(
            and_(RoleRecord.tenant_id == user.tenant_id, RoleRecord.name == body.role.value)
        )
    )
    role_record = role_result.scalar_one_or_none()

    # Remove any pending invite for same tenant+email
    await db.execute(
        delete(UserInviteRecord).where(
            and_(
                UserInviteRecord.tenant_id == user.tenant_id,
                UserInviteRecord.email == body.email,
                UserInviteRecord.accepted_at.is_(None),
            )
        )
    )

    invite_token = create_invite_token(
        tenant_id=user.tenant_id,
        email=body.email,
        role_id=role_record.id if role_record else None,
        invited_by=user.id,
    )

    from core.config.settings import get_settings
    settings = get_settings()
    expires_at = token_expires_at(invite_token)

    invite_record = UserInviteRecord(
        id=_new_id("inv_"),
        tenant_id=user.tenant_id,
        email=body.email,
        role_id=role_record.id if role_record else None,
        invited_by=user.id,
        token_hash=hash_token(invite_token),
        expires_at=expires_at.replace(tzinfo=None) if expires_at else _utcnow(),
    )
    db.add(invite_record)

    return {
        "invite_token": invite_token,
        "email": body.email,
        "role": body.role.value,
        "expires_hours": settings.jwt_invite_token_expire_hours,
        "note": "Share this token via email — POST /api/v1/auth/invite/accept to redeem",
    }


@router.post("/invite/accept", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def accept_invite(
    body: InviteAcceptRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Accept an invite token, set name + password, and create the user account."""
    try:
        payload = decode_invite_token(body.token)
    except JWTError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired invite token")

    email: str = payload["sub"]
    tenant_id: str = payload["tid"]
    role_id: str | None = payload.get("rid")
    token_hash = hash_token(body.token)

    # Validate invite record
    inv_result = await db.execute(
        select(UserInviteRecord).where(
            and_(
                UserInviteRecord.tenant_id == tenant_id,
                UserInviteRecord.email == email,
                UserInviteRecord.token_hash == token_hash,
                UserInviteRecord.accepted_at.is_(None),
                UserInviteRecord.expires_at > _utcnow(),
            )
        )
    )
    invite = inv_result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invite not found, expired, or already used")

    # Check email not already registered in this tenant
    existing = await db.execute(
        select(UserRecord).where(
            and_(UserRecord.tenant_id == tenant_id, UserRecord.email == email)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered for this tenant")

    user = UserRecord(
        id=_new_id("usr_"),
        tenant_id=tenant_id,
        role_id=role_id,
        email=email,
        name=body.name,
        hashed_password=_hash_password(body.password),
        is_active=True,
        is_verified=True,
    )
    db.add(user)

    invite.accepted_at = _utcnow()
    await db.flush()

    return await _issue_tokens(user, db, request)


# ── MFA ─────────────────────────────────────────────────────────────

@router.post("/mfa/setup", response_model=MFASetupResponse)
async def mfa_setup(
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> MFASetupResponse:
    """
    Generate a TOTP secret and provisioning URI.
    The user must call /mfa/verify to activate MFA.
    """
    if user.mfa_enabled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "MFA is already enabled")

    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user.email, issuer_name="Dealix")

    # Store secret temporarily (unverified) — not activated until /mfa/verify
    user.totp_secret = secret
    await db.flush()

    # Attempt QR code generation (optional — requires qrcode + Pillow)
    qr_data_uri: str | None = None
    try:
        import io
        import qrcode
        import base64
        img = qrcode.make(uri)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_data_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        pass

    return MFASetupResponse(secret=secret, provisioning_uri=uri, qr_data_uri=qr_data_uri)


@router.post("/mfa/verify", status_code=status.HTTP_200_OK)
async def mfa_verify(
    body: MFAVerifyRequest,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Verify TOTP code and enable MFA for the account."""
    if user.mfa_enabled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "MFA is already enabled")
    if not user.totp_secret:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Call /mfa/setup first")

    if not _verify_totp(user.totp_secret, body.totp_code):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid TOTP code")

    user.mfa_enabled = True
    await db.flush()

    return {"mfa_enabled": True, "message": "MFA successfully enabled"}


@router.post("/mfa/disable", status_code=status.HTTP_200_OK)
async def mfa_disable(
    body: MFADisableRequest,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Disable MFA — requires current password + valid TOTP code."""
    if not user.mfa_enabled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "MFA is not enabled")

    if not _verify_password(body.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid password")

    if not user.totp_secret or not _verify_totp(user.totp_secret, body.totp_code):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid TOTP code")

    user.mfa_enabled = False
    user.totp_secret = None
    await db.flush()

    return {"mfa_enabled": False, "message": "MFA successfully disabled"}


# ── Password reset ───────────────────────────────────────────────────

@router.post("/password/reset-request", status_code=status.HTTP_200_OK)
async def password_reset_request(
    body: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Initiate password reset — generates a reset token.
    Always returns 200 to prevent user enumeration.
    In production, send token via email rather than returning it.
    """
    stmt = select(UserRecord).where(
        and_(UserRecord.email == body.email, UserRecord.is_active.is_(True))
    )
    if body.tenant_slug:
        sub = select(TenantRecord.id).where(TenantRecord.slug == body.tenant_slug)
        stmt = stmt.where(UserRecord.tenant_id == sub.scalar_subquery())

    result = await db.execute(stmt)
    user = result.scalars().first()

    token_plaintext: str | None = None
    if user:
        reset_token = secrets.token_urlsafe(48)
        user.reset_token = hashlib.sha256(reset_token.encode()).hexdigest()
        user.reset_token_expires_at = datetime.now(timezone.utc).replace(tzinfo=None)

        from datetime import timedelta
        user.reset_token_expires_at = (
            datetime.now(timezone.utc) + timedelta(hours=1)
        ).replace(tzinfo=None)
        await db.flush()
        token_plaintext = reset_token

    return {
        "message": "If an account exists for that email, a reset link has been sent.",
        # In dev/staging return the token for convenience; remove in production!
        "_dev_reset_token": token_plaintext,
    }


@router.post("/password/reset", status_code=status.HTTP_200_OK)
async def password_reset(
    body: PasswordResetApply,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Apply a new password using the reset token."""
    token_hash = hashlib.sha256(body.token.encode()).hexdigest()
    now = _utcnow()

    result = await db.execute(
        select(UserRecord).where(
            and_(
                UserRecord.reset_token == token_hash,
                UserRecord.reset_token_expires_at > now,
            )
        )
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired reset token")

    user.hashed_password = _hash_password(body.new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    await db.flush()

    # Revoke all sessions
    await db.execute(
        delete(RefreshTokenRecord).where(RefreshTokenRecord.user_id == user.id)
    )

    return {"message": "Password successfully updated. All sessions have been invalidated."}
