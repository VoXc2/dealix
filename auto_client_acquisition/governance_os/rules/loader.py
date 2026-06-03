"""Load declarative governance rule YAML files (documentation-first; engine may extend)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

RULES_DIR = Path(__file__).resolve().parent


def rule_yaml_paths() -> tuple[Path, ...]:
    return tuple(sorted(RULES_DIR.glob("*.yaml")))


def load_rule_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"invalid_rule_yaml:{path.name}"
        raise ValueError(msg)
    return data


def load_all_rules() -> list[dict[str, Any]]:
    return [load_rule_yaml(p) for p in rule_yaml_paths()]


__all__ = ["RULES_DIR", "load_all_rules", "load_rule_yaml", "rule_yaml_paths"]
