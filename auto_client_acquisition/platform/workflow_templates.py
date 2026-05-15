"""Workflow templates for modular reusable orchestration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowTemplate:
    template_id: str
    description: str
    steps: tuple[str, ...]
    default_retry_limit: int = 3


def validate_template(template: WorkflowTemplate) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not template.template_id.strip():
        errors.append('template_id_missing')
    if len(template.steps) == 0:
        errors.append('template_steps_missing')
    if len(set(template.steps)) != len(template.steps):
        errors.append('template_steps_not_unique')
    if template.default_retry_limit < 0:
        errors.append('template_retry_limit_invalid')
    return len(errors) == 0, tuple(errors)


__all__ = ['WorkflowTemplate', 'validate_template']
