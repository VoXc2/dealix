"""Load Execution Assurance YAML registry (immutable reference for audits)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


def _registry_path() -> Path:
    return Path(__file__).resolve().parent / "registry.yaml"


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    data = yaml.safe_load(_registry_path().read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def assurance_version() -> int:
    v = load_registry().get("version")
    return int(v) if isinstance(v, int) else 1
