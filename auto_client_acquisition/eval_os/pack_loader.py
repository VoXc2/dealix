"""Loader and validator for the YAML evaluation packs in ``evals/``.

A pack declares ``what good means`` for a workflow. This module reads a
pack and checks its shape; it never runs an eval itself.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

# The 4 packs introduced for the 4-category taxonomy.
TAXONOMY_PACKS: tuple[str, ...] = (
    "retrieval_quality_eval",
    "response_quality_eval",
    "workflow_quality_eval",
    "business_quality_eval",
)

_REQUIRED_KEYS: tuple[str, ...] = ("eval_id", "version", "checks")


def _evals_dir() -> Path:
    """Resolve the repository ``evals/`` directory."""
    override = os.environ.get("DEALIX_EVALS_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent.parent / "evals"


def load_pack(name: str) -> dict[str, Any]:
    """Load ``evals/<name>.yaml`` as a dict. Raises FileNotFoundError."""
    if not name:
        raise ValueError("pack name is required")
    stem = name[:-5] if name.endswith(".yaml") else name
    path = _evals_dir() / f"{stem}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"eval pack not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"eval pack {name} is not a mapping")
    return data


def validate_pack(pack: dict[str, Any]) -> list[str]:
    """Return a list of structural problems with a loaded pack (empty = ok)."""
    problems: list[str] = []
    for key in _REQUIRED_KEYS:
        if key not in pack:
            problems.append(f"missing required key: {key}")
    checks = pack.get("checks")
    if checks is not None:
        if not isinstance(checks, list) or not checks:
            problems.append("checks must be a non-empty list")
        else:
            for i, check in enumerate(checks):
                if not isinstance(check, dict):
                    problems.append(f"check[{i}] is not a mapping")
                    continue
                if "id" not in check:
                    problems.append(f"check[{i}] missing id")
                if "pass" not in check:
                    problems.append(f"check[{i}] missing pass criterion")
    return problems


def list_packs() -> list[str]:
    """All eval pack stems present in the ``evals/`` directory."""
    evals_dir = _evals_dir()
    if not evals_dir.exists():
        return []
    return sorted(p.stem for p in evals_dir.glob("*.yaml"))


def validate_taxonomy_packs() -> dict[str, list[str]]:
    """Validate the 4 taxonomy packs; map pack name to its problems."""
    out: dict[str, list[str]] = {}
    for name in TAXONOMY_PACKS:
        try:
            out[name] = validate_pack(load_pack(name))
        except (FileNotFoundError, ValueError) as e:
            out[name] = [str(e)]
    return out
