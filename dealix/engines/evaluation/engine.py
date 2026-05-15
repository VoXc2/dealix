"""Evaluation Engine (Engine 8) — registered governed foundation."""

from __future__ import annotations

from typing import Any

from dealix.engines.base import BaseEngine
from dealix.engines.registry import ENGINE_REGISTRY


class EvaluationEngine(BaseEngine):
    """Hallucination, grounding, execution success, escalation correctness,
    policy compliance, business impact.

    Phase 0: registered foundation composing `dealix.trust` (tool
    verification). Scoring capabilities are Planned for roadmap phase 2.
    """

    spec = ENGINE_REGISTRY.get("evaluation")

    def _domain_report(self) -> dict[str, Any]:
        return {
            "metrics": dict.fromkeys(self.spec.capabilities, "planned"),
            "foundation": "dealix.trust.tool_verification",
        }

    def score(self, metric: str, *args: Any, **kwargs: Any) -> Any:
        raise self._planned(f"score:{metric}")
