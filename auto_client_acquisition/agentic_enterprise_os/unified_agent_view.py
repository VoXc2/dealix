"""Unified Agent OS view — one per-agent record across identity and governance.

عرض موحَّد للوكلاء — يدمج هوية الوكيل مع الحوكمة وتقييم المخاطر في سجل واحد.

The Agent OS pieces are scattered across ``agent_os`` (identity) and
``agentic_operations_os`` (governance, risk, lifecycle). This is a read-only
merge layer — it does not replace either registry. Governance and ops fields
are Optional and default to ``None`` when not supplied (no fabricated risk).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.agent_registry import list_agents


@dataclass(frozen=True, slots=True)
class UnifiedAgentView:
    """A single agent merged across identity, governance, and operations."""

    agent_id: str
    name: str
    owner: str
    purpose: str
    autonomy_level: int
    status: str
    risk_score: int | None = None
    risk_band: str | None = None
    lifecycle_state: str | None = None
    governance_decision: str | None = None
    matched_rules: tuple[str, ...] = field(default_factory=tuple)


def build_unified_agent_view(
    card: AgentCard,
    *,
    risk_score: int | None = None,
    risk_band: str | None = None,
    lifecycle_state: str | None = None,
    governance_decision: str | None = None,
    matched_rules: tuple[str, ...] = (),
) -> UnifiedAgentView:
    """Merge an agent identity card with optional governance and risk signals."""
    return UnifiedAgentView(
        agent_id=card.agent_id,
        name=card.name,
        owner=card.owner,
        purpose=card.purpose,
        autonomy_level=card.autonomy_level,
        status=card.status,
        risk_score=risk_score,
        risk_band=risk_band,
        lifecycle_state=lifecycle_state,
        governance_decision=governance_decision,
        matched_rules=tuple(matched_rules),
    )


def list_unified_agent_views() -> tuple[UnifiedAgentView, ...]:
    """Unified view over every agent in the Agent OS registry."""
    return tuple(build_unified_agent_view(card) for card in list_agents().values())


__all__ = [
    "UnifiedAgentView",
    "build_unified_agent_view",
    "list_unified_agent_views",
]
