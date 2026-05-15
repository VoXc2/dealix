"""State-machine engine for workflow_os_v10.

Public API:
  - ``start_workflow(definition, customer_handle="...")`` → WorkflowRun
  - ``advance_workflow(run, step_name, idempotency_key, result=None)``
       → WorkflowRun

The engine enforces:
  - Allowed transitions (per ALLOWED_TRANSITIONS).
  - Idempotency: replaying the same key is a no-op.
  - Retry budget: failures beyond ``max_retries`` set state=failed.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.workflow_os_v10.idempotency import (
    is_duplicate,
    record_key,
)
from auto_client_acquisition.workflow_os_v10.retry_policy import (
    compute_next_retry,
)
from auto_client_acquisition.workflow_os_v10.run_store import get_run_store
from auto_client_acquisition.workflow_os_v10.schemas import (
    ALLOWED_TRANSITIONS,
    RetryPolicy,
    WorkflowDefinition,
    WorkflowRun,
    WorkflowState,
    WorkflowStep,
)

# Workflow definitions stay process-local. Runs are persisted through the
# active WorkflowRunStore (in-memory by default; swappable to Postgres).
_DEFINITION_BUFFER: dict[str, WorkflowDefinition] = {}


def _reset_workflow_buffer() -> None:
    """Clear the run store + definition buffer. For tests + CI."""
    get_run_store().clear()
    _DEFINITION_BUFFER.clear()


def register_definition(definition: WorkflowDefinition) -> WorkflowDefinition:
    """Make a workflow definition retrievable by id."""
    _DEFINITION_BUFFER[definition.workflow_id] = definition
    return definition


def get_definition(workflow_id: str) -> WorkflowDefinition:
    """Look up a previously registered definition."""
    if workflow_id not in _DEFINITION_BUFFER:
        raise KeyError(f"workflow_id {workflow_id!r} not registered")
    return _DEFINITION_BUFFER[workflow_id]


def list_definitions() -> list[WorkflowDefinition]:
    return list(_DEFINITION_BUFFER.values())


def get_run(run_id: str) -> WorkflowRun:
    run = get_run_store().get(run_id)
    if run is None:
        raise KeyError(f"run_id {run_id!r} not found")
    return run


def start_workflow(
    definition: WorkflowDefinition,
    customer_handle: str = "Saudi B2B customer",
) -> WorkflowRun:
    """Start a new run from a workflow definition."""
    if not definition.workflow_id:
        raise ValueError("definition.workflow_id is required")
    if not isinstance(customer_handle, str) or not customer_handle.strip():
        raise ValueError("customer_handle must be a non-empty string")

    # Make sure the definition is retrievable downstream.
    register_definition(definition)

    run = WorkflowRun(
        workflow_id=definition.workflow_id,
        customer_handle=customer_handle,
        state="pending",
        current_step=definition.steps[0] if definition.steps else "",
    )
    get_run_store().save(run)
    return run


def _transition_state(
    run: WorkflowRun,
    next_state: WorkflowState,
) -> None:
    """Mutate ``run`` to ``next_state`` if the transition is allowed."""
    current = run.state
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if next_state == current:
        return
    # Special cases: pending → running and any → blocked are always allowed
    # provided they're listed in ALLOWED_TRANSITIONS.
    if next_state not in allowed:
        raise ValueError(
            f"transition {current} → {next_state} not allowed; "
            f"valid: {sorted(allowed) or '[terminal]'}"
        )
    run.state = next_state
    run.updated_at = datetime.now(UTC)


def advance_workflow(
    run: WorkflowRun,
    step_name: str,
    idempotency_key: str,
    result: dict[str, Any] | None = None,
    *,
    policy: RetryPolicy | None = None,
    simulate_failure: bool = False,
) -> WorkflowRun:
    """Advance ``run`` by executing ``step_name`` once.

    Idempotency: if ``idempotency_key`` has been seen before in this run,
    the call is a no-op (returns the run unchanged).

    Retry: if ``simulate_failure`` is True and the step still has retry
    budget, the step transitions to ``retrying``. After exhausting
    ``policy.max_retries``, the run state becomes ``failed``.
    """
    if not step_name:
        raise ValueError("step_name is required")
    if not idempotency_key:
        raise ValueError("idempotency_key is required")

    # Idempotency check — same key replayed is a no-op.
    if is_duplicate(run, idempotency_key):
        return run

    record_key(run, idempotency_key)

    # Find or create the step record.
    step = None
    for s in run.step_history:
        if s.name == step_name and s.state in {"running", "retrying", "pending"}:
            step = s
            break

    if step is None:
        step = WorkflowStep(
            name=step_name,
            idempotency_key=idempotency_key,
            state="pending",
            max_retries=(policy.max_retries if policy else 3),
            retry_after_seconds=(policy.initial_delay_seconds if policy else 60),
            started_at=datetime.now(UTC),
        )
        run.step_history.append(step)

    # Promote to running.
    if step.state == "pending":
        step.state = "running"
    if run.state in {"pending", "paused_for_approval"}:
        # Allowed: pending → running. paused_for_approval → running.
        _transition_state(run, "running")
    elif run.state == "retrying":
        _transition_state(run, "running")

    run.current_step = step_name

    if simulate_failure:
        step.attempt += 1
        active_policy = policy or RetryPolicy(
            max_retries=step.max_retries,
            backoff_factor=2.0,
            initial_delay_seconds=step.retry_after_seconds,
        )
        if step.attempt < active_policy.max_retries:
            step.state = "retrying"
            step.retry_after_seconds = compute_next_retry(step.attempt, active_policy)
            step.error = f"simulated failure on attempt {step.attempt}"
            _transition_state(run, "retrying")
        else:
            step.state = "failed"
            step.error = f"exhausted {active_policy.max_retries} retries"
            step.completed_at = datetime.now(UTC)
            _transition_state(run, "failed")
        run.updated_at = datetime.now(UTC)
        return run

    # Success path.
    step.state = "completed"
    step.result = dict(result or {})
    step.completed_at = datetime.now(UTC)
    run.updated_at = datetime.now(UTC)

    # If this was the last step in the registered definition, mark complete.
    try:
        definition = get_definition(run.workflow_id)
    except KeyError:
        definition = None

    if definition and definition.steps:
        completed_step_names = [s.name for s in run.step_history if s.state == "completed"]
        if all(name in completed_step_names for name in definition.steps):
            _transition_state(run, "completed")

    # Persist the advanced run.
    get_run_store().save(run)
    return run


def block_workflow(run: WorkflowRun, reason: str = "manual_block") -> WorkflowRun:
    """Force the run into the blocked terminal state."""
    run.state = "blocked"
    run.updated_at = datetime.now(UTC)
    if run.step_history:
        run.step_history[-1].error = reason
    get_run_store().save(run)
    return run
