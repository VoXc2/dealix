"""Public Doctrine endpoint.

Returns a snapshot of the Governed AI Operations Doctrine as Dealix
publishes it. Pinned to a git commit SHA so that any public claim can
reference an immutable revision.

  GET /api/v1/doctrine
      Returns: { name, commit_sha, sources, control_mapping, links }

The endpoint is public (no auth). It does NOT return:
  - commercial implementation code,
  - customer / pipeline / pricing data,
  - investor-confidential material.

Only the open doctrine published in `open-doctrine/` is exposed here.
"""
from __future__ import annotations

import logging
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
OPEN_DOCTRINE_DIR = REPO_ROOT / "open-doctrine"
CONSTITUTION_DIR = REPO_ROOT / "docs" / "00_constitution"


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


@router.get("/doctrine")
async def doctrine() -> dict[str, Any]:
    """Public read-only doctrine snapshot pinned to a commit SHA."""
    return {
        "name": "Governed AI Operations Doctrine",
        "owner": "Dealix",
        "commit_sha": _commit_sha(),
        "sources": {
            "open_doctrine_files": _safe_list(OPEN_DOCTRINE_DIR),
            "constitution_files": _safe_list(CONSTITUTION_DIR),
        },
        "control_mapping": _control_mapping(),
        "links": {
            "promise_endpoint": "/api/v1/dealix-promise",
            "capital_assets_public": "/api/v1/capital-assets/public",
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
