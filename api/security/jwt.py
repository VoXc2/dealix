"""
JWT token service — create, decode, and hash tokens.
خدمة رمز JWT — إنشاء الرموز وفكّها وتشفيرها.

Token types:
  access  — short-lived (default 30 min), carries user/tenant/role claims
  refresh — long-lived (default 30 days), persisted as a hashed value in DB
  invite  — medium-lived (default 72 h), carries email/tenant/role for new-user signup
"""

from __future__ import annotations

import hashlib
import hmac as _hmac
import secrets
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from core.config.settings import get_settings

# Token type discriminator stored in the "typ" claim
_TYPE_ACCESS = "access"
_TYPE_REFRESH = "refresh"
_TYPE_INVITE = "invite"


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _secret() -> str:
    return get_settings().jwt_secret_key.get_secret_value()


def _algorithm() -> str:
    return get_settings().jwt_algorithm


# ── Token creation ─────────────────────────────────────────────────

def create_access_token(
    *,
    user_id: str,
    tenant_id: str | None,
    role: str | None,
    system_role: str | None = None,
    extra_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """Issue a short-lived JWT access token."""
    settings = get_settings()
    exp_delta = expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes)
    now = _utcnow()
    payload: dict[str, Any] = {
        "sub": user_id,
        "typ": _TYPE_ACCESS,
        "tid": tenant_id,   # tenant_id
        "rol": role,        # tenant-scoped role name
        "srl": system_role, # system-level role (super_admin | None)
        "iat": now,
        "exp": now + exp_delta,
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, _secret(), algorithm=_algorithm())


def create_refresh_token(
    *,
    user_id: str,
    tenant_id: str | None,
) -> str:
    """Issue an opaque-style refresh token (JWT for convenience, treated as opaque at the server)."""
    settings = get_settings()
    now = _utcnow()
    payload: dict[str, Any] = {
        "sub": user_id,
        "typ": _TYPE_REFRESH,
        "tid": tenant_id,
        "jti": secrets.token_hex(16),  # unique nonce — prevents token replay
        "iat": now,
        "exp": now + timedelta(days=settings.jwt_refresh_token_expire_days),
    }
    return jwt.encode(payload, _secret(), algorithm=_algorithm())


def create_invite_token(
    *,
    tenant_id: str,
    email: str,
    role_id: str | None = None,
    invited_by: str,
) -> str:
    """Issue an invitation token for new-user onboarding."""
    settings = get_settings()
    now = _utcnow()
    payload: dict[str, Any] = {
        "sub": email,
        "typ": _TYPE_INVITE,
        "tid": tenant_id,
        "rid": role_id,
        "inv": invited_by,
        "jti": secrets.token_hex(16),
        "iat": now,
        "exp": now + timedelta(hours=settings.jwt_invite_token_expire_hours),
    }
    return jwt.encode(payload, _secret(), algorithm=_algorithm())


# ── Token verification ──────────────────────────────────────────────

def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    """
    Decode and validate a JWT. Raises JWTError on invalid/expired tokens.
    Optionally assert the token type matches expected_type.
    """
    payload: dict[str, Any] = jwt.decode(token, _secret(), algorithms=[_algorithm()])
    if expected_type and payload.get("typ") != expected_type:
        raise JWTError(
            f"Token type mismatch: expected {expected_type!r}, got {payload.get('typ')!r}"
        )
    return payload


def decode_access_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type=_TYPE_ACCESS)


def decode_refresh_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type=_TYPE_REFRESH)


def decode_invite_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type=_TYPE_INVITE)


# ── Token hashing (for DB storage) ─────────────────────────────────

def hash_token(token: str) -> str:
    """SHA-256 hex digest of a token — safe to store in DB."""
    return hashlib.sha256(token.encode()).hexdigest()


def verify_token_hash(token: str, stored_hash: str) -> bool:
    """Constant-time comparison of token against stored hash."""
    computed = hash_token(token)
    return _hmac.compare_digest(computed, stored_hash)


# ── Helpers ─────────────────────────────────────────────────────────

def token_expires_at(token_str: str) -> datetime | None:
    """Extract expiry datetime from a JWT without raising on expiry."""
    try:
        payload = jwt.decode(
            token_str,
            _secret(),
            algorithms=[_algorithm()],
            options={"verify_exp": False},
        )
        exp = payload.get("exp")
        if exp:
            return datetime.fromtimestamp(exp, tz=UTC)
    except JWTError:
        pass
    return None
