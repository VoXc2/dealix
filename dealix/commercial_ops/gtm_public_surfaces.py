"""GTM public surfaces registry — web routes + API trust layer."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import REPO_ROOT

_SURFACES_YAML = REPO_ROOT / "dealix" / "config" / "gtm_public_surfaces.yaml"


@lru_cache(maxsize=1)
def load_gtm_public_surfaces_config() -> dict[str, Any]:
    if not _SURFACES_YAML.is_file():
        return {}
    data = yaml.safe_load(_SURFACES_YAML.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def verify_gtm_public_surfaces_repo() -> dict[str, Any]:
    """Ensure registry files and hinted frontend paths exist."""
    issues: list[str] = []
    cfg = load_gtm_public_surfaces_config()
    if not cfg:
        issues.append("missing dealix/config/gtm_public_surfaces.yaml")

    for route in cfg.get("frontend_public_routes") or []:
        hint = (route.get("file_hint") or "").strip()
        if hint and not (REPO_ROOT / hint).is_file():
            issues.append(f"frontend route missing file: {hint}")

    doc = REPO_ROOT / "docs" / "ops" / "GTM_PUBLIC_SURFACES_AR.md"
    if not doc.is_file():
        issues.append("missing docs/ops/GTM_PUBLIC_SURFACES_AR.md")

    return {"issues": issues, "ok": len(issues) == 0, "config": cfg}


def build_gtm_public_surfaces_snapshot() -> dict[str, Any]:
    cfg = load_gtm_public_surfaces_config()
    return {
        "version": cfg.get("version"),
        "api_base_production": cfg.get("api_base_production"),
        "api_trust_endpoints": cfg.get("api_trust_endpoints") or [],
        "frontend_public_routes": cfg.get("frontend_public_routes") or [],
        "ops_admin_routes": cfg.get("ops_admin_routes") or {},
        "registry_path": str(_SURFACES_YAML.relative_to(REPO_ROOT)).replace("\\", "/"),
    }
