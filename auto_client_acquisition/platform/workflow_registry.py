"""Workflow registration and rollback controls."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.workflow_versioning import valid_workflow_upgrade


@dataclass(frozen=True, slots=True)
class WorkflowRegistration:
    workflow_id: str
    version: str
    owner: str
    sla_minutes: int
    metrics: tuple[str, ...]
    rollbackable: bool
    evals_enabled: bool
    status: str = 'active'


_WORKFLOWS: dict[str, WorkflowRegistration] = {}
_WORKFLOW_HISTORY: dict[str, list[WorkflowRegistration]] = {}


def register_workflow(workflow: WorkflowRegistration, *, allow_replace: bool = False) -> None:
    if not workflow.workflow_id.strip() or not workflow.owner.strip() or workflow.sla_minutes <= 0:
        raise ValueError('invalid_workflow_registration')
    existing = _WORKFLOWS.get(workflow.workflow_id)
    if existing is not None and not allow_replace:
        raise ValueError('workflow_already_registered')
    if existing is not None and not valid_workflow_upgrade(existing.version, workflow.version):
        raise ValueError('workflow_version_must_increase')
    _WORKFLOWS[workflow.workflow_id] = workflow
    _WORKFLOW_HISTORY.setdefault(workflow.workflow_id, []).append(workflow)


def get_workflow(workflow_id: str) -> WorkflowRegistration | None:
    return _WORKFLOWS.get(workflow_id)


def list_workflows() -> tuple[WorkflowRegistration, ...]:
    return tuple(_WORKFLOWS.values())


def rollback_workflow(workflow_id: str, version: str) -> WorkflowRegistration:
    history = _WORKFLOW_HISTORY.get(workflow_id, [])
    for candidate in reversed(history):
        if candidate.version == version:
            _WORKFLOWS[workflow_id] = candidate
            _WORKFLOW_HISTORY[workflow_id].append(candidate)
            return candidate
    raise ValueError('rollback_version_not_found')


def clear_workflow_registry_for_tests() -> None:
    _WORKFLOWS.clear()
    _WORKFLOW_HISTORY.clear()


__all__ = [
    'WorkflowRegistration',
    'clear_workflow_registry_for_tests',
    'get_workflow',
    'list_workflows',
    'register_workflow',
    'rollback_workflow',
]
