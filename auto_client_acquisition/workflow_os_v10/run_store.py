"""Pluggable store for workflow runs.

The state machine persists runs through a ``WorkflowRunStore``. The default
backend is in-memory (process-local, used by tests and the sync engine).
A durable Postgres backend lives in ``pg_run_store`` for async callers that
need runs to survive a restart and be resumed.
"""

from __future__ import annotations

from typing import Protocol

from auto_client_acquisition.workflow_os_v10.schemas import WorkflowRun


class WorkflowRunStore(Protocol):
    """Synchronous run store used by the in-process state machine."""

    def save(self, run: WorkflowRun) -> None: ...

    def get(self, run_id: str) -> WorkflowRun | None: ...

    def delete(self, run_id: str) -> None: ...

    def list_ids(self) -> list[str]: ...

    def clear(self) -> None: ...


class InMemoryWorkflowRunStore:
    """Process-local run store — fast, deterministic, the default backend."""

    def __init__(self) -> None:
        self._runs: dict[str, WorkflowRun] = {}

    def save(self, run: WorkflowRun) -> None:
        self._runs[run.run_id] = run

    def get(self, run_id: str) -> WorkflowRun | None:
        return self._runs.get(run_id)

    def delete(self, run_id: str) -> None:
        self._runs.pop(run_id, None)

    def list_ids(self) -> list[str]:
        return list(self._runs)

    def clear(self) -> None:
        self._runs.clear()


_active_store: WorkflowRunStore = InMemoryWorkflowRunStore()


def get_run_store() -> WorkflowRunStore:
    """Return the active run store used by the state machine."""
    return _active_store


def set_run_store(store: WorkflowRunStore) -> None:
    """Swap the active run store (e.g. to inject a custom backend in tests)."""
    global _active_store
    _active_store = store


def reset_run_store() -> None:
    """Reset to a fresh in-memory store. For tests + CI."""
    global _active_store
    _active_store = InMemoryWorkflowRunStore()
