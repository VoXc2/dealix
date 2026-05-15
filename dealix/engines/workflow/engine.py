"""Workflow Orchestration Engine (Engine 2) — registered governed foundation."""

from __future__ import annotations

from typing import Any

from dealix.engines.base import BaseEngine
from dealix.engines.registry import ENGINE_REGISTRY


class WorkflowEngine(BaseEngine):
    """Event -> reasoning -> workflow -> orchestration -> approval -> execution.

    Phase 0: registered foundation. It composes `workflow_os_v10` and the
    `dealix.execution.GovernedPipeline` (verified by `status_report`). Domain
    capabilities are Planned for roadmap phase 1 and fail loudly.
    """

    spec = ENGINE_REGISTRY.get("workflow")

    def _domain_report(self) -> dict[str, Any]:
        return {
            "capabilities": dict.fromkeys(self.spec.capabilities, "planned"),
            "foundation": "workflow_os_v10 + dealix.execution.GovernedPipeline",
        }

    def select_workflow(self, *args: Any, **kwargs: Any) -> Any:
        raise self._planned("select_workflow")

    def orchestrate(self, *args: Any, **kwargs: Any) -> Any:
        raise self._planned("orchestrate")
