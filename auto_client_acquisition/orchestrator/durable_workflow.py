"""Durable workflow runner — JSON-persisted step graph with HITL gates."""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4

_DEFAULT_PATH = "var/durable_workflows.json"
_lock = threading.Lock()
_memory_store: dict[str, dict[str, Any]] | None = None


class WorkflowStatus(StrEnum):
    RUNNING = "running"
    WAITING = "waiting"
    NEEDS_APPROVAL = "NEEDS_APPROVAL"
    COMPLETED = "completed"
    FAILED = "failed"


WORKFLOW_TEMPLATES: dict[str, tuple[dict[str, Any], ...]] = {
    "gtm_touch_cycle": (
        {"node": "run_step", "step_key": "targeting"},
        {"node": "run_step", "step_key": "enrichment"},
        {"node": "human_gate", "step_key": "outreach_approval"},
        {"node": "wait_until", "wait_seconds": 0},
        {"node": "run_step", "step_key": "qualification"},
    ),
}


@dataclass
class WorkflowRunState:
    id: str
    workflow_type: str
    status: str
    step: int
    context: dict[str, Any] = field(default_factory=dict)
    human_approval_id: str | None = None
    wait_until: str | None = None
    retries: int = 0
    max_iterations: int = 5

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> WorkflowRunState:
        return cls(
            id=str(raw["id"]),
            workflow_type=str(raw["workflow_type"]),
            status=str(raw["status"]),
            step=int(raw.get("step", 0)),
            context=dict(raw.get("context") or {}),
            human_approval_id=raw.get("human_approval_id"),
            wait_until=raw.get("wait_until"),
            retries=int(raw.get("retries", 0)),
            max_iterations=int(raw.get("max_iterations", 5)),
        )


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_DURABLE_WORKFLOWS_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = _repo_root() / p
    return p


def use_in_memory_store(enabled: bool = True) -> None:
    """Switch persistence to an in-memory dict (tests)."""
    global _memory_store
    _memory_store = {} if enabled else None


def _load_all() -> dict[str, dict[str, Any]]:
    if _memory_store is not None:
        return _memory_store
    path = _path()
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_all(store: dict[str, dict[str, Any]]) -> None:
    if _memory_store is not None:
        _memory_store.clear()
        _memory_store.update(store)
        return
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")


def _persist(state: WorkflowRunState) -> WorkflowRunState:
    with _lock:
        store = _load_all()
        store[state.id] = state.to_dict()
        _save_all(store)
    return state


def _get(run_id: str) -> WorkflowRunState:
    store = _load_all()
    raw = store.get(run_id)
    if not raw:
        raise KeyError(f"workflow run not found: {run_id}")
    return WorkflowRunState.from_dict(raw)


def _step_defs(state: WorkflowRunState) -> tuple[dict[str, Any], ...]:
    custom = state.context.get("steps")
    if isinstance(custom, list) and custom:
        return tuple(custom)
    return WORKFLOW_TEMPLATES.get(state.workflow_type, ())


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _run_step_node(state: WorkflowRunState, step_def: dict[str, Any]) -> WorkflowRunState:
    step_key = str(step_def.get("step_key") or f"step_{state.step}")
    handlers: dict[str, Callable[[dict[str, Any]], Any]] = state.context.get("step_handlers") or {}
    handler = handlers.get(step_key)
    try:
        if callable(handler):
            result = handler(state.context)
            state.context.setdefault("step_results", {})[step_key] = result
        else:
            state.context.setdefault("step_results", {})[step_key] = {
                "skipped": True,
                "step_key": step_key,
            }
    except Exception as exc:
        state.retries += 1
        state.context["last_error"] = str(exc)
        if state.retries >= state.max_iterations:
            state.status = WorkflowStatus.FAILED.value
        return state
    state.step += 1
    state.retries = 0
    state.status = WorkflowStatus.RUNNING.value
    return state


def _human_gate_node(state: WorkflowRunState, step_def: dict[str, Any]) -> WorkflowRunState:
    step_key = str(step_def.get("step_key") or f"gate_{state.step}")
    if state.context.pop("human_approved", False):
        state.human_approval_id = None
        state.context.setdefault("step_results", {})[step_key] = {"approved": True}
        state.step += 1
        state.status = WorkflowStatus.RUNNING.value
        return state
    state.human_approval_id = f"appr_{uuid4().hex[:12]}"
    state.context.setdefault("step_results", {})[step_key] = {"pending_approval": True}
    state.status = WorkflowStatus.NEEDS_APPROVAL.value
    return state


def _wait_until_node(state: WorkflowRunState, step_def: dict[str, Any]) -> WorkflowRunState:
    if state.wait_until:
        if datetime.now(UTC) < _parse_iso(state.wait_until):
            state.status = WorkflowStatus.WAITING.value
            return state
        state.wait_until = None
        state.step += 1
        state.status = WorkflowStatus.RUNNING.value
        return state
    seconds = int(step_def.get("wait_seconds") or state.context.get("wait_seconds") or 0)
    if seconds <= 0:
        state.step += 1
        state.status = WorkflowStatus.RUNNING.value
        return state
    state.wait_until = (datetime.now(UTC) + timedelta(seconds=seconds)).isoformat()
    state.status = WorkflowStatus.WAITING.value
    return state


def _apply_node(state: WorkflowRunState, step_def: dict[str, Any]) -> WorkflowRunState:
    node = str(step_def.get("node") or "run_step")
    if node == "run_step":
        return _run_step_node(state, step_def)
    if node == "human_gate":
        return _human_gate_node(state, step_def)
    if node == "wait_until":
        return _wait_until_node(state, step_def)
    state.context["last_error"] = f"unknown node: {node}"
    state.status = WorkflowStatus.FAILED.value
    return state


def start_workflow(
    workflow_type: str,
    context: dict[str, Any] | None = None,
    *,
    steps: tuple[dict[str, Any], ...] | None = None,
    max_iterations: int = 5,
) -> WorkflowRunState:
    """Create and persist a new workflow run, then advance the first step."""
    ctx = dict(context or {})
    if steps:
        ctx["steps"] = list(steps)
    run_id = f"wfr_{uuid4().hex[:12]}"
    state = WorkflowRunState(
        id=run_id,
        workflow_type=workflow_type,
        status=WorkflowStatus.RUNNING.value,
        step=0,
        context=ctx,
        max_iterations=max(1, max_iterations),
    )
    _persist(state)
    return advance_workflow(run_id)


def advance_workflow(run_id: str) -> WorkflowRunState:
    """Advance one workflow node; respects wait gates and retry caps."""
    state = _get(run_id)
    if state.status in (WorkflowStatus.COMPLETED.value, WorkflowStatus.FAILED.value):
        return state
    if state.status == WorkflowStatus.NEEDS_APPROVAL.value:
        return state

    steps = _step_defs(state)
    if state.step >= len(steps):
        state.status = WorkflowStatus.COMPLETED.value
        return _persist(state)

    if state.status == WorkflowStatus.WAITING.value:
        state = _wait_until_node(state, steps[state.step])
        if state.status == WorkflowStatus.WAITING.value:
            return _persist(state)

    while state.status == WorkflowStatus.RUNNING.value and state.step < len(steps):
        step_def = steps[state.step]
        state = _apply_node(state, step_def)
        if state.status in (
            WorkflowStatus.NEEDS_APPROVAL.value,
            WorkflowStatus.WAITING.value,
            WorkflowStatus.FAILED.value,
        ):
            break
        if state.step >= len(steps):
            state.status = WorkflowStatus.COMPLETED.value
            break

    return _persist(state)


def approve_human_step(run_id: str, approval_id: str) -> WorkflowRunState:
    """Approve a human_gate step and continue the workflow."""
    state = _get(run_id)
    if state.status != WorkflowStatus.NEEDS_APPROVAL.value:
        raise ValueError(f"run {run_id} is not awaiting approval (status={state.status})")
    if state.human_approval_id != approval_id:
        raise ValueError("approval_id mismatch")
    state.context["human_approved"] = True
    state.status = WorkflowStatus.RUNNING.value
    _persist(state)
    return advance_workflow(run_id)


def get_workflow(run_id: str) -> WorkflowRunState:
    """Load a persisted workflow run."""
    return _get(run_id)


__all__ = [
    "WORKFLOW_TEMPLATES",
    "WorkflowRunState",
    "WorkflowStatus",
    "advance_workflow",
    "approve_human_step",
    "get_workflow",
    "start_workflow",
    "use_in_memory_store",
]
