"""Execution Engine (Engine 7) — registered governed foundation."""

from __future__ import annotations

from typing import Any

from dealix.engines.base import BaseEngine
from dealix.engines.registry import ENGINE_REGISTRY


class ExecutionEngine(BaseEngine):
    """Executes operations (CRM, proposals, approvals) — always governed.

    Phase 0: registered foundation composing `dealix.execution.GovernedPipeline`.
    Live actions always remain draft/approval-gated (no_live_send doctrine).
    Direct execution is Planned for roadmap phase 1.
    """

    spec = ENGINE_REGISTRY.get("execution")

    def _domain_report(self) -> dict[str, Any]:
        return {
            "capabilities": dict.fromkeys(self.spec.capabilities, "planned"),
            "foundation": "dealix.execution.GovernedPipeline",
            "doctrine": "all live actions stay draft/approval-gated (no_live_send)",
        }

    def execute_action(self, *args: Any, **kwargs: Any) -> Any:
        raise self._planned("execute_action")

    def dispatch_governed(self, *args: Any, **kwargs: Any) -> Any:
        raise self._planned("dispatch_governed")
