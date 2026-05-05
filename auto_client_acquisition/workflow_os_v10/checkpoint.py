"""Checkpoint helpers — save + restore a WorkflowRun.

The checkpoint is a pure dict; it can be persisted to disk, S3, or
just held in memory. Restore returns a fresh WorkflowRun whose state
matches the snapshot.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.workflow_os_v10.schemas import WorkflowRun


def save_checkpoint(run: WorkflowRun) -> dict[str, Any]:
    """Serialize the run to a JSON-safe dict."""
    return run.to_dict()


def restore_checkpoint(checkpoint: dict[str, Any]) -> WorkflowRun:
    """Rebuild a WorkflowRun from a previously saved checkpoint."""
    if not isinstance(checkpoint, dict):
        raise TypeError("checkpoint must be a dict")
    data = dict(checkpoint)
    # Convert idempotency_keys_seen list back to a set (Pydantic accepts list).
    keys = data.get("idempotency_keys_seen")
    if isinstance(keys, list):
        data["idempotency_keys_seen"] = set(keys)
    return WorkflowRun.model_validate(data)
