"""Workflow model — deterministic stages for governed delivery."""

from __future__ import annotations

from enum import StrEnum


class WorkflowStage(StrEnum):
    INTAKE = "intake"
    PASSPORT = "passport"
    PROCESSING = "processing"
    GOVERNANCE = "governance"
    QA = "qa"
    PROOF = "proof"
    HANDOFF = "handoff"


WORKFLOW_STAGE_ORDER: tuple[WorkflowStage, ...] = (
    WorkflowStage.INTAKE,
    WorkflowStage.PASSPORT,
    WorkflowStage.PROCESSING,
    WorkflowStage.GOVERNANCE,
    WorkflowStage.QA,
    WorkflowStage.PROOF,
    WorkflowStage.HANDOFF,
)


__all__ = ["WORKFLOW_STAGE_ORDER", "WorkflowStage"]
