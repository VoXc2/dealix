"""Loads and validates the 3 Assurance System YAML policy files.

Files live in ``assurance_os/config/`` and are loaded relative to this
module (mirrors the pattern used by delivery_os/service_readiness.py).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_CONFIG_DIR = Path(__file__).resolve().parent / "config"

_REQUIRED = {
    "approval_policy": {"version", "channels", "hard_rules"},
    "stage_transitions": {"version", "ladder", "rung_to_journey_stage", "hard_gates"},
    "claim_policy": {"version", "non_negotiables", "forbidden_claims",
                     "escalation_triggers"},
}


@dataclass
class AssuranceConfig:
    """Parsed + validated view of the 3 policy files."""

    approval_policy: dict[str, Any]
    stage_transitions: dict[str, Any]
    claim_policy: dict[str, Any]
    loaded_ok: bool = True
    errors: list[str] | None = None


def _load_one(name: str) -> dict[str, Any]:
    path = _CONFIG_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"assurance config missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"assurance config {name}.yaml is not a mapping")
    missing = _REQUIRED[name] - set(data.keys())
    if missing:
        raise ValueError(f"assurance config {name}.yaml missing keys: {sorted(missing)}")
    return data


@lru_cache(maxsize=1)
def load_config() -> AssuranceConfig:
    """Load all 3 files. On any failure returns a config with
    ``loaded_ok=False`` so callers can degrade to ``unknown`` rather
    than crash."""
    errors: list[str] = []
    parsed: dict[str, dict[str, Any]] = {}
    for name in _REQUIRED:
        try:
            parsed[name] = _load_one(name)
        except Exception as exc:  # noqa: BLE001 — surface, never crash
            errors.append(f"{name}: {exc}")
            parsed[name] = {}
    return AssuranceConfig(
        approval_policy=parsed["approval_policy"],
        stage_transitions=parsed["stage_transitions"],
        claim_policy=parsed["claim_policy"],
        loaded_ok=not errors,
        errors=errors or None,
    )
