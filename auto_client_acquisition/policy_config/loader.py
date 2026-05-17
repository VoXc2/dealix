"""Load declarative policy YAML files.

Mirrors the convention in ``governance_os/rules/loader.py``: ``yaml.safe_load`` +
``isinstance(data, dict)`` guard + ``ValueError`` on malformed input. Results are
cached; set ``DEALIX_POLICY_DIR`` to point at an alternate config directory (ops
override / tests) — the cache is keyed on the resolved directory.
"""

from __future__ import annotations

import functools
import os
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parent


def _config_dir() -> Path:
    override = os.getenv("DEALIX_POLICY_DIR")
    return Path(override).resolve() if override else CONFIG_DIR


def policy_path(name: str) -> Path:
    """Resolve a policy file by bare name (no extension)."""
    return _config_dir() / f"{name}.yaml"


@functools.cache
def _load(directory: str, name: str) -> dict[str, Any]:
    path = Path(directory) / f"{name}.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"invalid_policy_yaml:{name}"
        raise ValueError(msg)
    return data


def load_policy(name: str) -> dict[str, Any]:
    """Return the parsed policy mapping for ``name`` (e.g. ``approval_policy``)."""
    return _load(str(_config_dir()), name)


__all__ = ["CONFIG_DIR", "load_policy", "policy_path"]
