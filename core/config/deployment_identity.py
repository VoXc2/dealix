"""Resolve the deployed commit from platform-managed identity variables.

Platform-provided commit SHAs are authoritative for runtime proof. A generic
``GIT_SHA`` may be injected by Docker builds or left stale in project settings,
so it must not override Vercel or Railway's immutable deployment metadata.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

_UNKNOWN = "unknown"
_PLATFORM_CONTEXT_KEYS = (
    "VERCEL",
    "VERCEL_ENV",
    "RAILWAY_PROJECT_ID",
    "RAILWAY_ENVIRONMENT_ID",
    "RAILWAY_DEPLOYMENT_ID",
    "RAILWAY_SERVICE_ID",
)


def resolve_deployment_git_sha(
    configured_sha: str | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> str:
    """Return the best available exact deployment SHA, failing closed to unknown.

    Precedence:

    1. Vercel's system-managed commit SHA.
    2. Railway's system-managed commit SHA.
    3. If a platform context is present but its immutable SHA is missing,
       ``unknown`` (never a mutable/stale generic ``GIT_SHA``).
    4. The already parsed application setting (normally ``GIT_SHA``) for
       non-platform/container-build contexts.
    5. A direct generic ``GIT_SHA`` lookup for non-platform contexts.
    6. ``unknown``.
    """
    env = os.environ if environ is None else environ

    for key in ("VERCEL_GIT_COMMIT_SHA", "RAILWAY_GIT_COMMIT_SHA"):
        value = str(env.get(key, "")).strip()
        if value:
            return value

    if any(str(env.get(key, "")).strip() for key in _PLATFORM_CONTEXT_KEYS):
        return _UNKNOWN

    configured = str(configured_sha or "").strip()
    if configured and configured.casefold() != _UNKNOWN:
        return configured

    generic = str(env.get("GIT_SHA", "")).strip()
    return generic or _UNKNOWN
