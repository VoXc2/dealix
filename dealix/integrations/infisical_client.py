"""
Infisical secrets manager — pulls runtime secrets from a HashiCorp-Vault-
class store so production no longer relies on long-lived `.env` files.

We use the REST API directly (no `infisical-python` SDK pull) so the
import path costs nothing when the workspace isn't configured. The client
is *additive*: it merges Infisical secrets into `os.environ` at boot if
INFISICAL_TOKEN + INFISICAL_PROJECT_ID + INFISICAL_ENV are set. Local dev
and tests behave exactly as before.

Reference: https://infisical.com/docs/api-reference/endpoints/secrets/list
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_BASE = "https://app.infisical.com/api"


class InfisicalNotConfigured(RuntimeError):
    pass


def is_configured() -> bool:
    return all(
        os.getenv(name, "").strip()
        for name in ("INFISICAL_TOKEN", "INFISICAL_PROJECT_ID", "INFISICAL_ENV")
    )


async def fetch_secrets() -> dict[str, str]:
    """Return a dict of secret_name -> value from Infisical for the current env.

    Returns an empty dict (and logs) if the workspace isn't configured.
    """
    token = os.getenv("INFISICAL_TOKEN", "").strip()
    project_id = os.getenv("INFISICAL_PROJECT_ID", "").strip()
    env = os.getenv("INFISICAL_ENV", "").strip()
    if not (token and project_id and env):
        return {}
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"{_BASE}/v3/secrets/raw",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "workspaceId": project_id,
                    "environment": env,
                    "secretPath": os.getenv("INFISICAL_SECRET_PATH", "/"),
                },
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("infisical_fetch_failed")
        return {}
    out: dict[str, str] = {}
    for entry in data.get("secrets", []):
        key = entry.get("secretKey")
        val = entry.get("secretValue")
        if key and isinstance(val, str):
            out[key] = val
    log.info("infisical_secrets_loaded", count=len(out), environment=env)
    return out


async def populate_env(*, override: bool = False) -> int:
    """Merge fetched secrets into os.environ. Returns count merged."""
    secrets_map = await fetch_secrets()
    n = 0
    for k, v in secrets_map.items():
        if override or k not in os.environ:
            os.environ[k] = v
            n += 1
    return n
