"""
Feature flags — thin wrapper over PostHog flag evaluation.

PostHog is already wired (`dealix/analytics/posthog_client.py`) for product
analytics; the same client can evaluate flags, so we avoid bringing in a
second vendor (GrowthBook / LaunchDarkly).

Public surface:
    await is_enabled(flag, tenant_id=..., user_id=...) -> bool
    await variant(flag, ...) -> str | None      # multivariate experiments
    flag_or_env(flag, env_name, tenant_id=None) -> bool  # sync helper for
                                                          # env-based fallbacks

Behaviour without POSTHOG_API_KEY:
- `is_enabled` returns the value of the ENV-backed fallback name if
  provided (e.g. `STRIPE_ENABLED`), else False.
- This lets the codebase keep working in dev / tests with zero PostHog
  setup while still respecting env overrides.

All calls are best-effort: any failure → log + treat as disabled.
"""

from __future__ import annotations

import os
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


def _env_truthy(name: str) -> bool:
    raw = os.getenv(name, "").strip().lower()
    return raw in {"1", "true", "yes", "on"}


async def is_enabled(
    flag: str,
    *,
    tenant_id: str | None = None,
    user_id: str | None = None,
    env_fallback: str | None = None,
    default: bool = False,
) -> bool:
    """Return True if `flag` is enabled for the given tenant/user.

    Resolution order:
        1. PostHog (if configured) — evaluate flag for the distinct_id.
        2. Env fallback (if `env_fallback` is set) — useful in dev.
        3. `default` (False).
    """
    try:
        from dealix.analytics import posthog_client

        distinct_id = user_id or tenant_id or "anonymous"
        try:
            result = await posthog_client.get_feature_flag(
                flag, distinct_id=distinct_id
            )
        except Exception:
            result = None
        if result is True or result == "true":
            return True
        if result is False or result == "false":
            return False
    except Exception:
        # PostHog client missing/uninstalled — fall through to env / default.
        pass

    if env_fallback and _env_truthy(env_fallback):
        return True
    return default


def flag_or_env(
    flag: str,
    env_name: str,
    *,
    tenant_id: str | None = None,
    default: bool = False,
) -> bool:
    """Synchronous helper for boot-time checks that can't await.

    Uses ONLY the env fallback path. Keeps the call shape consistent with
    `is_enabled` so call sites can later switch to the async version.
    """
    return _env_truthy(env_name) or default


async def variant(
    flag: str,
    *,
    tenant_id: str | None = None,
    user_id: str | None = None,
) -> str | None:
    """Return the assigned variant string (multivariate experiments)."""
    try:
        from dealix.analytics import posthog_client

        distinct_id = user_id or tenant_id or "anonymous"
        result = await posthog_client.get_feature_flag(flag, distinct_id=distinct_id)
    except Exception:
        return None
    if isinstance(result, str):
        return result
    if result is True:
        return "on"
    if result is False:
        return "off"
    return None
