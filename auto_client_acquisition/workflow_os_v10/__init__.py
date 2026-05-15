"""Workflow OS v10 — Temporal-style state machine + retry + idempotency.

Pure native Python. No Temporal SDK, no external worker queue. The
engine in ``state_machine.py`` is in-process and deterministic; it
enforces:

  - ALLOWED_TRANSITIONS for every state move.
  - Idempotency via per-run ``idempotency_keys_seen``.
  - Retry budget via ``RetryPolicy`` (exponential backoff).
  - Checkpoint round-trip preserves run state.

Pre-defined workflows are registered automatically on import:
  - ``GROWTH_STARTER_7_DAY``  (≥7 steps — one per Pilot day)
  - ``PROOF_PACK_ASSEMBLY``
  - ``MINI_DIAGNOSTIC``
"""

from auto_client_acquisition.workflow_os_v10.checkpoint import (
    restore_checkpoint,
    save_checkpoint,
)
from auto_client_acquisition.workflow_os_v10.diagnostic_workflow import (
    MINI_DIAGNOSTIC,
)
from auto_client_acquisition.workflow_os_v10.idempotency import (
    is_duplicate,
    record_key,
)
from auto_client_acquisition.workflow_os_v10.proof_pack_workflow import (
    PROOF_PACK_ASSEMBLY,
)
from auto_client_acquisition.workflow_os_v10.retry_policy import (
    compute_next_retry,
    should_retry,
)
from auto_client_acquisition.workflow_os_v10.run_store import (
    InMemoryWorkflowRunStore,
    WorkflowRunStore,
    get_run_store,
    reset_run_store,
    set_run_store,
)
from auto_client_acquisition.workflow_os_v10.schemas import (
    ALLOWED_TRANSITIONS,
    IdempotencyKey,
    RetryPolicy,
    WorkflowDefinition,
    WorkflowRun,
    WorkflowState,
    WorkflowStep,
)
from auto_client_acquisition.workflow_os_v10.service_session_workflow import (
    GROWTH_STARTER_7_DAY,
)
from auto_client_acquisition.workflow_os_v10.state_machine import (
    _reset_workflow_buffer,
    advance_workflow,
    block_workflow,
    get_definition,
    get_run,
    list_definitions,
    register_definition,
    start_workflow,
)

# Auto-register the pre-defined workflows so the API can list them.
register_definition(GROWTH_STARTER_7_DAY)
register_definition(PROOF_PACK_ASSEMBLY)
register_definition(MINI_DIAGNOSTIC)


__all__ = [
    "ALLOWED_TRANSITIONS",
    "GROWTH_STARTER_7_DAY",
    "MINI_DIAGNOSTIC",
    "PROOF_PACK_ASSEMBLY",
    "IdempotencyKey",
    "InMemoryWorkflowRunStore",
    "RetryPolicy",
    "WorkflowDefinition",
    "WorkflowRun",
    "WorkflowRunStore",
    "WorkflowState",
    "WorkflowStep",
    "_reset_workflow_buffer",
    "advance_workflow",
    "block_workflow",
    "compute_next_retry",
    "get_definition",
    "get_run",
    "get_run_store",
    "is_duplicate",
    "list_definitions",
    "record_key",
    "register_definition",
    "reset_run_store",
    "restore_checkpoint",
    "save_checkpoint",
    "set_run_store",
    "should_retry",
    "start_workflow",
]
