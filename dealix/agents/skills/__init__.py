"""
Skill loader + registry. Reads `skills/MANIFEST.yaml` once at module
import (with `reload()` for tests) and exposes the catalog to:

- `api/routers/skills.py` (HTTP surface).
- `dealix/mcp/server.py` (MCP tools — extends in T6a).
- `dealix/agents/builder/` (BYOA skill picker — extends in T6d).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from core.logging import get_logger

log = get_logger(__name__)

_MANIFEST = Path(__file__).resolve().parents[3] / "skills" / "MANIFEST.yaml"


@dataclass(frozen=True)
class Skill:
    id: str
    path: str
    description: str
    inputs: list[str]
    output_shape: str
    permissions: dict[str, Any] = field(default_factory=dict)


_cache: list[Skill] | None = None


def load() -> list[Skill]:
    """Return the parsed skill catalog. Cached per process."""
    global _cache
    if _cache is not None:
        return _cache
    if not _MANIFEST.is_file():
        _cache = []
        return _cache
    raw = yaml.safe_load(_MANIFEST.read_text(encoding="utf-8")) or {}
    out: list[Skill] = []
    for entry in raw.get("skills", []) or []:
        try:
            out.append(
                Skill(
                    id=str(entry["id"]),
                    path=str(entry["path"]),
                    description=str(entry.get("description", "")),
                    inputs=list(entry.get("inputs", []) or []),
                    output_shape=str(entry.get("output_shape", "")),
                    permissions=dict(entry.get("permissions") or {}),
                )
            )
        except KeyError as exc:
            log.warning("skill_manifest_row_invalid", error=str(exc), entry=entry)
    _cache = out
    return out


def reload() -> list[Skill]:
    """Clear + re-read the manifest. Tests use this."""
    global _cache
    _cache = None
    return load()


def by_id(skill_id: str) -> Skill | None:
    for s in load():
        if s.id == skill_id:
            return s
    return None
