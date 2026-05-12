"""
Prompt registry — every production system prompt lives in this package
as a YAML file with `id`, `version`, `description`, `body`. The loader
hashes each prompt at startup; tests assert the hash matches the snapshot
so prompt drift can't sneak in without a code review.

Public surface:
    load("proposal") -> Prompt
    Prompt.render(ctx) -> str
    snapshot_all() -> dict[str, str]  # for tests
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Any

import yaml

from core.logging import get_logger

log = get_logger(__name__)

_DIR = Path(__file__).parent


@dataclass(frozen=True)
class Prompt:
    id: str
    version: str
    description: str
    body: str
    sha256: str

    def render(self, ctx: dict[str, Any]) -> str:
        """Render with $variable substitution. Missing vars left as-is."""
        return Template(self.body).safe_substitute(ctx)


def _file_for(prompt_id: str) -> Path:
    return _DIR / f"{prompt_id}.yaml"


def load(prompt_id: str) -> Prompt:
    path = _file_for(prompt_id)
    if not path.is_file():
        raise FileNotFoundError(f"prompt_not_found:{prompt_id}")
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}
    body = data.get("body", "")
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return Prompt(
        id=data["id"],
        version=str(data.get("version", "v0")),
        description=data.get("description", ""),
        body=body,
        sha256=sha,
    )


def snapshot_all() -> dict[str, str]:
    """Map prompt_id -> sha256(body). Used by tests/test_prompt_snapshot.py."""
    out: dict[str, str] = {}
    for p in sorted(_DIR.glob("*.yaml")):
        try:
            prompt = load(p.stem)
            out[prompt.id] = prompt.sha256
        except Exception:
            log.exception("prompt_snapshot_failed", file=str(p))
    return out
