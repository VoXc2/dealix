"""Map service slugs to default workflow stages (deterministic)."""

from __future__ import annotations

from auto_client_acquisition.workflow_os.workflow_model import WorkflowStage

_DEFAULT: tuple[WorkflowStage, ...] = (
    WorkflowStage.INTAKE,
    WorkflowStage.PASSPORT,
    WorkflowStage.PROCESSING,
    WorkflowStage.GOVERNANCE,
    WorkflowStage.QA,
    WorkflowStage.PROOF,
    WorkflowStage.HANDOFF,
)


def default_stages_for_service(service_slug: str) -> tuple[WorkflowStage, ...]:
    _ = service_slug
    return _DEFAULT


__all__ = ["default_stages_for_service"]
