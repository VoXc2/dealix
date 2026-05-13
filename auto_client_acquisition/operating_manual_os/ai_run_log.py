"""AI Run Log — canonical schema for every governed AI invocation.

See ``docs/operating_manual/ULTIMATE_OPERATING_MANUAL.md`` §13 and
``docs/sovereignty/MODEL_ROUTER_STRATEGY.md``.

Every AI call inside Dealix MUST be recorded as an ``AIRunLogEntry``.
The ledger is the operational evidence behind the Trust Pack, the
Audit Trail, and the Proof Pack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from auto_client_acquisition.endgame_os.governance_product import (
    GovernanceDecision,
)


_VALID_RISK_LEVELS: frozenset[str] = frozenset({"low", "medium", "high", "critical"})


@dataclass(frozen=True)
class AIRunLogEntry:
    """Canonical record of a single AI run.

    The fields mirror the JSON shape in the doctrine. ``inputs_redacted``
    is required to default to ``True`` whenever PII could be present —
    the doctrine fails closed.
    """

    ai_run_id: str
    agent: str
    task: str
    prompt_version: str
    inputs_redacted: bool
    output_schema: str
    governance_status: GovernanceDecision
    qa_score: int                  # 0..100
    risk_level: str                # low | medium | high | critical
    model_class: str | None = None
    cost_usd: float | None = None
    latency_ms: int | None = None
    audit_event_id: str | None = None
    engagement_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.ai_run_id:
            raise ValueError("ai_run_id_required")
        if not self.agent:
            raise ValueError("agent_required")
        if not self.task:
            raise ValueError("task_required")
        if not self.prompt_version:
            raise ValueError("prompt_version_required")
        if not self.output_schema:
            raise ValueError("output_schema_required")
        if not 0 <= self.qa_score <= 100:
            raise ValueError("qa_score_out_of_range_0_100")
        if self.risk_level not in _VALID_RISK_LEVELS:
            raise ValueError(f"invalid_risk_level:{self.risk_level}")
        if self.cost_usd is not None and self.cost_usd < 0:
            raise ValueError("cost_must_be_non_negative")
        if self.latency_ms is not None and self.latency_ms < 0:
            raise ValueError("latency_must_be_non_negative")

    def to_dict(self) -> dict[str, object]:
        return {
            "ai_run_id": self.ai_run_id,
            "agent": self.agent,
            "task": self.task,
            "prompt_version": self.prompt_version,
            "inputs_redacted": self.inputs_redacted,
            "output_schema": self.output_schema,
            "governance_status": self.governance_status.value,
            "qa_score": self.qa_score,
            "risk_level": self.risk_level,
            "model_class": self.model_class,
            "cost_usd": self.cost_usd,
            "latency_ms": self.latency_ms,
            "audit_event_id": self.audit_event_id,
            "engagement_id": self.engagement_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }


class AIRunLedger:
    """Append-only AI run ledger.

    Storage is intentionally out of scope; this is the typed surface.
    """

    def __init__(self) -> None:
        self._entries: list[AIRunLogEntry] = []
        self._seen_ids: set[str] = set()

    def append(self, entry: AIRunLogEntry) -> AIRunLogEntry:
        if entry.ai_run_id in self._seen_ids:
            raise ValueError(f"duplicate_ai_run_id:{entry.ai_run_id}")
        self._seen_ids.add(entry.ai_run_id)
        self._entries.append(entry)
        return entry

    def all(self) -> tuple[AIRunLogEntry, ...]:
        return tuple(self._entries)

    def by_agent(self, agent: str) -> tuple[AIRunLogEntry, ...]:
        return tuple(e for e in self._entries if e.agent == agent)

    def by_engagement(self, engagement_id: str) -> tuple[AIRunLogEntry, ...]:
        return tuple(e for e in self._entries if e.engagement_id == engagement_id)

    def export(self) -> list[dict[str, object]]:
        return [e.to_dict() for e in self._entries]
