"""Control-event ledger — the shared audit substrate for Systems 26-35.

Append-only JSONL writes to ``docs/control-events/<YYYY-MM-DD>.jsonl``.
Every one of the ten Enterprise Control Plane modules records its
state-changing events here, which is what makes the ``no_unaudited_changes``
non-negotiable hold across the whole control plane.

Template: ``auto_client_acquisition/proof_ledger/file_backend.py`` + ``factory.py``.
When Postgres lands, ``PostgresControlLedger`` implements the same public
methods and ``get_control_ledger`` selects it via ``settings.control_ledger_backend``.
"""

from __future__ import annotations

import json
import threading
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = REPO_ROOT / "docs" / "control-events"


class ControlEventType(StrEnum):
    """Every state-changing event the control plane can record."""

    # System 26 — control plane
    RUN_REGISTERED = "run_registered"
    RUN_PAUSED = "run_paused"
    RUN_RESUMED = "run_resumed"
    RUN_ROLLED_BACK = "run_rolled_back"
    RUN_REROUTED = "run_rerouted"
    RUN_COMPLETED = "run_completed"
    POLICY_EDIT_REQUESTED = "policy_edit_requested"
    POLICY_EDITED = "policy_edited"
    # approval gate
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_REJECTED = "approval_rejected"
    # System 27 — agent mesh
    AGENT_REGISTERED = "agent_registered"
    AGENT_ROUTED = "agent_routed"
    AGENT_ISOLATED = "agent_isolated"
    AGENT_TRUST_BOUNDARY_SET = "agent_trust_boundary_set"
    # System 28 — assurance contracts
    CONTRACT_REGISTERED = "contract_registered"
    CONTRACT_EVALUATED = "contract_evaluated"
    CONTRACT_FAILED = "contract_failed"
    # System 29 — sandbox
    SANDBOX_RUN = "sandbox_run"
    CANARY_ROLLOUT = "canary_rollout"
    SANDBOX_REPLAY = "sandbox_replay"
    # System 30 — org graph
    GRAPH_NODE_ADDED = "graph_node_added"
    GRAPH_EDGE_ADDED = "graph_edge_added"
    # System 31 — runtime safety
    CIRCUIT_OPENED = "circuit_opened"
    CIRCUIT_CLOSED = "circuit_closed"
    KILL_SWITCH_ENGAGED = "kill_switch_engaged"
    KILL_SWITCH_RELEASED = "kill_switch_released"
    EXECUTION_LIMIT_SET = "execution_limit_set"
    # System 32 — org simulation
    SIMULATION_RUN = "simulation_run"
    # System 33 — human-AI operating model
    DELEGATION_CREATED = "delegation_created"
    DELEGATION_REVOKED = "delegation_revoked"
    ESCALATION_RAISED = "escalation_raised"
    # System 34 — business value engine
    VALUE_MEASURED = "value_measured"
    # System 35 — self-evolving fabric
    IMPROVEMENT_PROPOSED = "improvement_proposed"
    IMPROVEMENT_APPLIED = "improvement_applied"
    IMPROVEMENT_REJECTED = "improvement_rejected"


class ControlEvent(BaseModel):
    """One recorded control-plane event. Append-only, never mutated."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str = Field(default_factory=lambda: f"evt_{uuid4().hex[:12]}")
    event_type: ControlEventType
    source_module: str
    actor: str = "system"
    subject_type: str = ""
    subject_id: str = ""
    run_id: str | None = None
    correlation_id: str | None = None
    decision: str = "n/a"  # allow | deny | escalate | n/a
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    payload: dict[str, Any] = Field(default_factory=dict)
    redacted: bool = True


def _date_file(base: Path, when: datetime | None = None) -> Path:
    when = when or datetime.now(UTC)
    return base / f"{when.strftime('%Y-%m-%d')}.jsonl"


def _redact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Redact PII from string payload values before anything hits disk."""
    out: dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(value, str):
            out[key] = redact_text(value)
        else:
            out[key] = value
    return out


class FileControlLedger:
    """Thread-safe append-only JSONL control-event ledger."""

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._base = Path(base_dir) if base_dir else DEFAULT_DIR
        self._base.mkdir(parents=True, exist_ok=True)

    def record(self, event: ControlEvent) -> ControlEvent:
        """Persist one event with payload redaction. Returns the stored event."""
        stored = event.model_copy(
            update={"payload": _redact_payload(event.payload), "redacted": True}
        )
        line = stored.model_dump_json() + "\n"
        path = _date_file(self._base)
        with self._lock:
            with path.open("a", encoding="utf-8") as f:
                f.write(line)
        return stored

    def list_events(
        self,
        *,
        source_module: str | None = None,
        run_id: str | None = None,
        event_type: str | None = None,
        limit: int = 200,
    ) -> list[ControlEvent]:
        """Read recent events (last 7 daily files), newest file first."""
        out: list[ControlEvent] = []
        with self._lock:
            files = sorted(self._base.glob("*.jsonl"), reverse=True)[:7]
        for f in files:
            try:
                with f.open("r", encoding="utf-8") as fh:
                    for raw in fh:
                        raw = raw.strip()
                        if not raw:
                            continue
                        try:
                            ev = ControlEvent.model_validate(json.loads(raw))
                        except Exception:  # noqa: BLE001 — skip corrupt lines
                            continue
                        if source_module and ev.source_module != source_module:
                            continue
                        if run_id and ev.run_id != run_id:
                            continue
                        if event_type and str(ev.event_type) != event_type:
                            continue
                        out.append(ev)
                        if len(out) >= limit:
                            return out
            except OSError:
                continue
        return out

    def clear_dir(self) -> None:
        """Test-only: drop the JSONL files in the ledger directory."""
        with self._lock:
            for f in list(self._base.glob("*.jsonl")):
                try:
                    f.unlink()
                except OSError:
                    pass


class PostgresControlLedger:
    """Postgres-backed control ledger — same interface as FileControlLedger.

    Deferred: v1 ships JSONL-first. Flipping ``settings.control_ledger_backend``
    to ``postgres`` activates this once a ``control_events`` table exists.
    """

    def record(self, event: ControlEvent) -> ControlEvent:  # pragma: no cover
        raise NotImplementedError("PostgresControlLedger is a deferred backend")

    def list_events(self, **kwargs: Any) -> list[ControlEvent]:  # pragma: no cover
        raise NotImplementedError("PostgresControlLedger is a deferred backend")

    def clear_dir(self) -> None:  # pragma: no cover
        raise NotImplementedError("PostgresControlLedger is a deferred backend")


ControlLedger = FileControlLedger | PostgresControlLedger

_DEFAULT: ControlLedger | None = None


def _backend_name() -> str:
    try:
        from core.config.settings import get_settings

        return getattr(get_settings(), "control_ledger_backend", "file") or "file"
    except Exception:  # noqa: BLE001 — settings never blocks the ledger
        return "file"


def get_control_ledger() -> ControlLedger:
    """Return the process-scoped control ledger singleton."""
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = (
            PostgresControlLedger()
            if _backend_name().lower().strip() == "postgres"
            else FileControlLedger()
        )
    return _DEFAULT


def reset_control_ledger() -> None:
    """Test helper: drop the cached singleton."""
    global _DEFAULT
    _DEFAULT = None


def emit(
    *,
    event_type: ControlEventType,
    source_module: str,
    actor: str = "system",
    subject_type: str = "",
    subject_id: str = "",
    run_id: str | None = None,
    correlation_id: str | None = None,
    decision: str = "n/a",
    payload: dict[str, Any] | None = None,
) -> ControlEvent:
    """Construct + record a control event in one call."""
    event = ControlEvent(
        event_type=event_type,
        source_module=source_module,
        actor=actor,
        subject_type=subject_type,
        subject_id=subject_id,
        run_id=run_id,
        correlation_id=correlation_id,
        decision=decision,
        payload=payload or {},
    )
    return get_control_ledger().record(event)


__all__ = [
    "ControlEvent",
    "ControlEventType",
    "ControlLedger",
    "FileControlLedger",
    "PostgresControlLedger",
    "emit",
    "get_control_ledger",
    "reset_control_ledger",
]
