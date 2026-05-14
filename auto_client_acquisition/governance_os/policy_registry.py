"""Load governance policy registry from packaged YAML."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import yaml


def _registry_path() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        "policies",
        "default_registry.yaml",
    )


@lru_cache(maxsize=1)
def load_policy_registry() -> dict[str, Any]:
    path = _registry_path()
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return {"version": 0, "forbidden_customer_facing_actions": []}
    return data


def forbidden_actions() -> list[str]:
    reg = load_policy_registry()
    raw = reg.get("forbidden_customer_facing_actions", [])
    return [str(x) for x in raw] if isinstance(raw, list) else []
