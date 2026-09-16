"""Resolve Dealix runtime release identity from the canonical self-host build SHA.

The production authority is now the self-host release controller, which injects an
exact ``GIT_SHA`` into API/Web images. Legacy provider metadata is intentionally
ignored so Railway/Vercel cannot regain runtime identity authority.
"""
from __future__ import annotations

import os
from collections.abc import Mapping

_UNKNOWN = "unknown"


def resolve_deployment_git_sha(
    configured_sha: str | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> str:
    """Return the canonical self-host release SHA, failing closed to ``unknown``."""
    env = os.environ if environ is None else environ
    configured = str(configured_sha or "").strip()
    if configured and configured.casefold() != _UNKNOWN:
        return configured
    generic = str(env.get("GIT_SHA", "")).strip()
    return generic or _UNKNOWN
