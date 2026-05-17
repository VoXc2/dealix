"""Thin runtime layer over the in-memory orchestrator task queue."""

from __future__ import annotations

from auto_client_acquisition.orchestrator.queue import TaskQueue

_DEFAULT: TaskQueue | None = None


def get_default_task_queue() -> TaskQueue:
    """Return the process-wide orchestrator task queue singleton."""
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = TaskQueue()
    return _DEFAULT


def reset_default_task_queue() -> None:
    """Test helper: drop the cached queue singleton."""
    global _DEFAULT
    _DEFAULT = None
