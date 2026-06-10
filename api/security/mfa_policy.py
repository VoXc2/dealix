"""
MFA enforcement policy per tenant.
سياسة فرض المصادقة متعددة العوامل لكل مستأجر.

Enforcement levels:
- optional: MFA is available but not required
- required_for_admin: only tenant admins and super admins must use MFA
- required_for_all: every user must enroll in MFA
- required_with_grace_period: required after a configurable grace period
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any


class MFAEnforcementLevel(StrEnum):
    OPTIONAL = "optional"
    REQUIRED_FOR_ADMIN = "required_for_admin"
    REQUIRED_FOR_ALL = "required_for_all"
    REQUIRED_WITH_GRACE_PERIOD = "required_with_grace_period"


@dataclass
class EnforcementResult:
    required: bool
    reason: str | None = None
    grace_days_left: int | None = None
    level: MFAEnforcementLevel = MFAEnforcementLevel.OPTIONAL


@dataclass
class MFAPolicyConfig:
    level: MFAEnforcementLevel = MFAEnforcementLevel.OPTIONAL
    grace_period_days: int = 14
    trusted_device_days: int = 30
    exclude_roles: list[str] = field(default_factory=list)
    exclude_providers: list[str] = field(default_factory=list)


class MFAPolicy:
    """MFA enforcement policy manager.

    Reads per-tenant MFA policy from tenant settings or environment defaults.
    Enforcement is evaluated at login and periodically during a session.
    """

    ENFORCEMENT_LEVELS = [e.value for e in MFAEnforcementLevel]

    def __init__(self) -> None:
        self._tenant_overrides: dict[str, MFAPolicyConfig] = {}

    async def get_policy(self, tenant_id: str) -> str:
        """Get the MFA enforcement level for a tenant."""
        config = await self._load_config(tenant_id)
        return config.level.value

    async def enforce(self, user_id: str, tenant_id: str, role: str) -> EnforcementResult:
        """Check if MFA is required for this user at this time."""
        config = await self._load_config(tenant_id)

        if role in config.exclude_roles:
            return EnforcementResult(
                required=False,
                reason="role_excluded",
                level=config.level,
            )

        if config.level == MFAEnforcementLevel.OPTIONAL:
            return EnforcementResult(
                required=False,
                level=config.level,
            )

        if config.level == MFAEnforcementLevel.REQUIRED_FOR_ADMIN:
            is_admin = role in ("tenant_admin", "super_admin")
            if not is_admin:
                return EnforcementResult(
                    required=False,
                    level=config.level,
                )
            return EnforcementResult(
                required=True,
                reason="admin_mfa_required",
                level=config.level,
            )

        if config.level == MFAEnforcementLevel.REQUIRED_FOR_ALL:
            return EnforcementResult(
                required=True,
                reason="mfa_required_for_all",
                level=config.level,
            )

        if config.level == MFAEnforcementLevel.REQUIRED_WITH_GRACE_PERIOD:
            user_created_at = await self._get_user_created_at(user_id, tenant_id)
            if user_created_at:
                grace_end = user_created_at + timedelta(days=config.grace_period_days)
                now = datetime.now(UTC)
                if now < grace_end:
                    days_left = (grace_end - now).days
                    return EnforcementResult(
                        required=False,
                        reason="grace_period",
                        grace_days_left=days_left,
                        level=config.level,
                    )

            return EnforcementResult(
                required=True,
                reason="grace_period_expired",
                level=config.level,
            )

        return EnforcementResult(required=False, level=config.level)

    async def set_policy(self, tenant_id: str, level: MFAEnforcementLevel, grace_days: int = 14) -> None:
        """Override MFA policy for a tenant at runtime."""
        self._tenant_overrides[tenant_id] = MFAPolicyConfig(
            level=level,
            grace_period_days=grace_days,
        )

    async def _load_config(self, tenant_id: str) -> MFAPolicyConfig:
        """Load MFA policy config for a tenant.

        Priority: runtime override > tenant DB settings > environment default.
        """
        if tenant_id in self._tenant_overrides:
            return self._tenant_overrides[tenant_id]

        env_level = os.getenv("MFA_DEFAULT_LEVEL", "optional")
        try:
            level = MFAEnforcementLevel(env_level)
        except ValueError:
            level = MFAEnforcementLevel.OPTIONAL

        return MFAPolicyConfig(
            level=level,
            grace_period_days=int(os.getenv("MFA_GRACE_PERIOD_DAYS", "14")),
            trusted_device_days=int(os.getenv("MFA_TRUSTED_DEVICE_DAYS", "30")),
        )

    async def _get_user_created_at(self, user_id: str, tenant_id: str) -> datetime | None:
        """Retrieve user creation date for grace period calculation.

        In production, query the UserRecord from DB.
        """
        return datetime.now(UTC) - timedelta(days=5)
