"""
Agent builder — Bring Your Own Agent (BYOA).

Accepts a customer-uploaded `agent.yaml` manifest describing the
agent's name, model, tools (drawn from skills/MANIFEST.yaml), prompt
override, and cost cap. Validates + persists into TenantRecord.meta_json
under `custom_agents.<agent_id>`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


_ID_RE = re.compile(r"^[a-z][a-z0-9_-]{2,63}$")


@dataclass
class CustomAgentSpec:
    id: str
    name: str
    description: str
    model: str
    tools: list[str]
    prompt_override: str
    max_usd_per_request: float
    locale: str
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentValidationError(ValueError):
    pass


def validate(manifest: dict[str, Any]) -> CustomAgentSpec:
    aid = str(manifest.get("id", "")).strip().lower()
    if not _ID_RE.match(aid):
        raise AgentValidationError(
            "id must be lowercase, 3-64 chars, [a-z0-9_-]"
        )
    name = str(manifest.get("name", "")).strip()
    if not name or len(name) > 120:
        raise AgentValidationError("name required, ≤ 120 chars")
    model = str(manifest.get("model", "")).strip()
    if not model:
        raise AgentValidationError("model required")
    tools = list(manifest.get("tools") or [])
    if not isinstance(tools, list):
        raise AgentValidationError("tools must be a list of skill ids")
    # Validate every referenced tool exists in the skills catalog.
    try:
        from dealix.agents.skills import by_id

        for t in tools:
            if by_id(str(t)) is None:
                raise AgentValidationError(f"unknown skill: {t}")
    except Exception as exc:
        log.warning("agent_builder_skills_check_skipped", error=str(exc))

    cap = float(manifest.get("max_usd_per_request", 0.50))
    if cap <= 0 or cap > 10:
        raise AgentValidationError("max_usd_per_request must be in (0, 10]")

    return CustomAgentSpec(
        id=aid,
        name=name,
        description=str(manifest.get("description") or "")[:500],
        model=model,
        tools=[str(t) for t in tools],
        prompt_override=str(manifest.get("prompt_override") or "")[:8000],
        max_usd_per_request=cap,
        locale=str(manifest.get("locale") or "ar"),
        metadata=dict(manifest.get("metadata") or {}),
    )
