"""Agent Observability — every agent run is recorded, redacted, and queryable.

Running agents needs observability, not just prompts. Each run records what
it did, the risk it carried, the sources it used, and what it cost. Raw PII
(phone, email, national ID) is never persisted — summaries are redacted on
write.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

_DEFAULT_PATH = "data/revenue_assurance/agent_runs.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    raw = os.environ.get("DEALIX_AGENT_RUNS_PATH", _DEFAULT_PATH)
    path = Path(raw)
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[2] / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@dataclass(frozen=True, slots=True)
class AgentRunRecord:
    run_id: str
    agent_name: str
    input_event: str
    input_refs: list[str] = field(default_factory=list)
    output_summary: str = ""
    risk_level: str = "low"
    sources_used: list[str] = field(default_factory=list)
    approval_required: bool = False
    policy_result: str = ""
    latency_ms: int = 0
    cost_estimate: float = 0.0
    created_at: str = ""
    redacted: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def record_run(
    *,
    agent_name: str,
    input_event: str,
    input_refs: list[str] | None = None,
    output_summary: str = "",
    risk_level: str = "low",
    sources_used: list[str] | None = None,
    approval_required: bool = False,
    policy_result: str = "",
    latency_ms: int = 0,
    cost_estimate: float = 0.0,
) -> AgentRunRecord:
    """Append a redacted agent-run record to the JSONL observability log.

    ``output_summary`` and every ``input_ref`` are passed through the PII
    redactor before persistence — raw phone / email / national ID never land
    on disk.
    """
    if not agent_name.strip():
        raise ValueError("agent_name is required")
    record = AgentRunRecord(
        run_id=f"arun_{uuid4().hex[:20]}",
        agent_name=agent_name.strip(),
        input_event=redact_text(input_event),
        input_refs=[redact_text(r) for r in (input_refs or [])],
        output_summary=redact_text(output_summary),
        risk_level=risk_level,
        sources_used=list(sources_used or []),
        approval_required=approval_required,
        policy_result=policy_result,
        latency_ms=max(0, int(latency_ms)),
        cost_estimate=max(0.0, float(cost_estimate)),
        created_at=datetime.now(timezone.utc).isoformat(),
        redacted=True,
    )
    path = _path()
    with _lock, path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), ensure_ascii=False))
        handle.write("\n")
    return record


def list_runs(*, agent_name: str | None = None, limit: int = 200) -> list[AgentRunRecord]:
    """List recorded agent runs, newest first."""
    path = _path()
    if not path.exists():
        return []
    out: list[AgentRunRecord] = []
    with _lock, path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                record = AgentRunRecord(**data)
            except Exception:  # noqa: BLE001
                continue
            if agent_name and record.agent_name != agent_name:
                continue
            out.append(record)
    out.sort(key=lambda r: r.created_at, reverse=True)
    return out[: max(0, limit)]


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        path.unlink()


__all__ = [
    "AgentRunRecord",
    "clear_for_test",
    "list_runs",
    "record_run",
]
