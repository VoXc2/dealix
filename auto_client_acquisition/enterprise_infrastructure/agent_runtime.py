"""Agent identity + permission loader for governed runtime."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.enterprise_infrastructure.schemas import AgentSpec, GovernanceDecision


class AgentSpecError(ValueError):
    """Raised when an agent runtime profile is invalid."""


def load_agent_spec(path: str | Path) -> AgentSpec:
    raw = _read_yaml(path)
    required = {
        "name",
        "version",
        "risk_level",
        "allowed_tools",
        "requires_approval_for",
        "memory_scope",
    }
    missing = required - set(raw.keys())
    if missing:
        raise AgentSpecError(f"agent profile missing fields: {sorted(missing)}")

    return AgentSpec(
        name=str(raw["name"]),
        version=str(raw["version"]),
        risk_level=str(raw["risk_level"]),  # type: ignore[arg-type]
        allowed_tools=tuple(str(v) for v in raw.get("allowed_tools", [])),
        requires_approval_for=tuple(str(v) for v in raw.get("requires_approval_for", [])),
        memory_scope=tuple(str(v) for v in raw.get("memory_scope", [])),
    )


def evaluate_agent_permission(spec: AgentSpec, action: str) -> GovernanceDecision:
    """Map agent identity/permission policy to governance decision vocabulary."""
    if action in spec.requires_approval_for:
        return "require_approval"
    if action in spec.allowed_tools:
        return "allow"
    return "block"


def _read_yaml(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise AgentSpecError(f"agent profile not found: {p}")
    parsed = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise AgentSpecError(f"agent profile is not a YAML object: {p}")
    return parsed
