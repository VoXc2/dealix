"""Public Doctrine endpoint.

Returns a snapshot of the Governed AI Operations Doctrine as Dealix
publishes it. Pinned to a git commit SHA so that any public claim can
reference an immutable revision.

  GET /api/v1/doctrine
      Returns: { name, commit_sha, sources, control_mapping, links, version }

  GET /api/v1/doctrine?version=v1.0.0
      Pinned snapshot at that version (commit_sha frozen to whatever
      was current when the version was tagged).

  GET /api/v1/doctrine/versions
      Versioned changelog: list of every published doctrine version.

The endpoint is public (no auth). It does NOT return:
  - commercial implementation code,
  - customer / pipeline / pricing data,
  - investor-confidential material.

Only the open doctrine published in `open-doctrine/` is exposed here.
"""
from __future__ import annotations

import json
import logging
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
OPEN_DOCTRINE_DIR = REPO_ROOT / "open-doctrine"
CONSTITUTION_DIR = REPO_ROOT / "docs" / "00_constitution"
VERSIONS_JSON = OPEN_DOCTRINE_DIR / "doctrine_versions.json"


@lru_cache(maxsize=1)
def _commit_sha() -> str:
    """Best-effort: read the current commit SHA. Falls back to 'unknown'."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        log.warning("doctrine_commit_sha_lookup_failed", exc_info=True)
    return "unknown"


def _safe_list(directory: Path, suffix: str = ".md") -> list[str]:
    if not directory.exists():
        return []
    return sorted(
        p.relative_to(REPO_ROOT).as_posix()
        for p in directory.glob(f"*{suffix}")
        if p.is_file()
    )


_TABLE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$"
)


@lru_cache(maxsize=1)
def _control_mapping() -> list[dict[str, Any]]:
    """Parse the control-mapping table from CONTROL_MAPPING.md."""
    p = OPEN_DOCTRINE_DIR / "CONTROL_MAPPING.md"
    if not p.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = _TABLE_ROW.match(line.strip())
        if not m:
            continue
        out.append({
            "number": int(m.group(1)),
            "commitment": m.group(2),
            "control_type": m.group(3),
            "reference": m.group(4),
        })
    return out


@lru_cache(maxsize=1)
def _versions() -> list[dict[str, Any]]:
    if not VERSIONS_JSON.exists():
        return []
    try:
        return list(json.loads(VERSIONS_JSON.read_text(encoding="utf-8")).get("versions") or [])
    except Exception:
        log.exception("doctrine_versions_load_failed")
        return []


def _find_version(label: str) -> dict[str, Any] | None:
    for v in _versions():
        if v.get("version") == label:
            return v
    return None


def _latest_version_label() -> str:
    vs = _versions()
    if not vs:
        return "unversioned"
    return vs[-1].get("version") or "unversioned"


@router.get("/doctrine")
async def doctrine(version: str | None = Query(default=None, description="Pinned doctrine version (e.g. v1.0.0).")) -> dict[str, Any]:
    """Public read-only doctrine snapshot pinned to a commit SHA.

    If `?version=` is supplied, the response is pinned to the
    version's recorded commit_sha (an immutable historical claim).
    Otherwise the response reflects the current HEAD plus the LATEST
    published version.
    """
    if version is not None:
        v = _find_version(version)
        if v is None:
            raise HTTPException(status_code=404, detail=f"unknown doctrine version {version!r}")
        return {
            "name": "Governed AI Operations Doctrine",
            "owner": "Dealix",
            "version": v["version"],
            "commit_sha": v.get("commit_sha"),
            "date": v.get("date"),
            "summary": v.get("summary"),
            "signed_by": v.get("signed_by"),
            "sources": {
                "open_doctrine_files": _safe_list(OPEN_DOCTRINE_DIR),
                "constitution_files": _safe_list(CONSTITUTION_DIR),
            },
            "control_mapping": _control_mapping(),
            "links": {
                "promise_endpoint": "/api/v1/dealix-promise",
                "capital_assets_public": "/api/v1/capital-assets/public",
                "versions_endpoint": "/api/v1/doctrine/versions",
                "master_verifier": "scripts/verify_all_dealix.py",
            },
            "disclaimer": (
                "This endpoint publishes Dealix's open operating doctrine. "
                "It is not legal advice, regulatory certification, or "
                "compliance approval."
            ),
        }
    return {
        "name": "Governed AI Operations Doctrine",
        "owner": "Dealix",
        "version": _latest_version_label(),
        "commit_sha": _commit_sha(),
        "sources": {
            "open_doctrine_files": _safe_list(OPEN_DOCTRINE_DIR),
            "constitution_files": _safe_list(CONSTITUTION_DIR),
        },
        "control_mapping": _control_mapping(),
        "links": {
            "promise_endpoint": "/api/v1/dealix-promise",
            "capital_assets_public": "/api/v1/capital-assets/public",
            "versions_endpoint": "/api/v1/doctrine/versions",
            "verifier_report": "/landing/assets/data/verifier-report.json",
            "master_verifier": "scripts/verify_all_dealix.py",
        },
        "disclaimer": (
            "This endpoint publishes Dealix's open operating doctrine. "
            "It is not legal advice, regulatory certification, or "
            "compliance approval. Commercial implementations live in "
            "private repositories."
        ),
    }


@router.get("/doctrine/versions")
async def doctrine_versions() -> dict[str, Any]:
    """List every published doctrine version."""
    return {
        "doctrine": "Governed AI Operations Doctrine",
        "owner": "Dealix",
        "versions": _versions(),
        "links": {
            "current": "/api/v1/doctrine",
            "pinned_example": "/api/v1/doctrine?version=v1.0.0",
        },
    }
