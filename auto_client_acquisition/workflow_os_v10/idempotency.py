"""Idempotency helpers — same key + same input → same outcome."""
from __future__ import annotations

from auto_client_acquisition.workflow_os_v10.schemas import WorkflowRun


def is_duplicate(run: WorkflowRun, key: str) -> bool:
    """True iff ``key`` has already been seen in this run."""
    return key in run.idempotency_keys_seen


def record_key(run: WorkflowRun, key: str) -> None:
    """Persist the key on the run so future advances see it as a dup."""
    run.idempotency_keys_seen.add(key)
