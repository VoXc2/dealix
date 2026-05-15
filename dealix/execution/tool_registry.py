"""
Typed Tool Registry — every integration is a governed, typed tool.

Per the enterprise blueprint: an integration is never a bare function call.
It becomes a *typed tool* carrying its own risk classification so the
Workflow Engine can route it through policy, approvals, audit, observability,
and — critically — rollback.

    registry = ToolRegistry()
    registry.register(Tool(
        name="whatsapp.send_message",
        description="Send a WhatsApp message to a lead",
        approval_class=ApprovalClass.A1,
        reversibility_class=ReversibilityClass.R2,
        sensitivity_class=SensitivityClass.S2,
        handler=_send_whatsapp,
        compensation=_post_correction_note,
    ))

Tools are deterministic units of work. Agents may *choose* tools, but tools
execute inside workflows — they never replace workflows.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from dealix.classifications import (
    ApprovalClass,
    ReversibilityClass,
    SensitivityClass,
)

# A tool handler receives the resolved input dict and returns a result dict.
ToolHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]

# A compensation receives (original_input, original_output) and best-effort
# undoes the side effect. It must be idempotent and must not raise.
Compensation = Callable[[dict[str, Any], dict[str, Any]], Awaitable[dict[str, Any]]]


class RiskLevel(StrEnum):
    """Human-readable risk band, derived from the (A, R, S) classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class Tool:
    """A typed, classified unit of work the engine can execute."""

    name: str
    description: str
    handler: ToolHandler
    approval_class: ApprovalClass = ApprovalClass.A0
    reversibility_class: ReversibilityClass = ReversibilityClass.R0
    sensitivity_class: SensitivityClass = SensitivityClass.S1
    # Maps to the action_type used for classification + audit. Defaults to name.
    action_type: str = ""
    compensation: Compensation | None = None
    # Side-effecting tools should be retried; pure reads usually need not be.
    max_attempts: int = 3
    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if not self.action_type:
            self.action_type = self.name

    @property
    def risk(self) -> RiskLevel:
        """Derive a coarse risk band from the classification triple."""
        if (
            self.approval_class in (ApprovalClass.A2, ApprovalClass.A3)
            or self.reversibility_class == ReversibilityClass.R3
            or self.sensitivity_class == SensitivityClass.S3
        ):
            return RiskLevel.HIGH
        if (
            self.approval_class == ApprovalClass.A1
            or self.reversibility_class == ReversibilityClass.R2
            or self.sensitivity_class == SensitivityClass.S2
        ):
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    @property
    def requires_approval(self) -> bool:
        return self.approval_class.requires_approval

    @property
    def reversible(self) -> bool:
        """Whether a failed downstream step can roll this one back."""
        return self.compensation is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "action_type": self.action_type,
            "approval_class": self.approval_class.value,
            "reversibility_class": self.reversibility_class.value,
            "sensitivity_class": self.sensitivity_class.value,
            "risk": self.risk.value,
            "requires_approval": self.requires_approval,
            "reversible": self.reversible,
            "max_attempts": self.max_attempts,
        }


class ToolRegistry:
    """A namespace of typed tools available to workflows."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> Tool:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool
        return tool

    def get(self, name: str) -> Tool:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Tool not found in registry: {name}")
        return tool

    def has(self, name: str) -> bool:
        return name in self._tools

    def all(self) -> list[Tool]:
        return list(self._tools.values())

    def to_dict(self) -> dict[str, Any]:
        return {"count": len(self._tools), "tools": [t.to_dict() for t in self._tools.values()]}


def tool(
    name: str,
    description: str,
    *,
    approval_class: ApprovalClass = ApprovalClass.A0,
    reversibility_class: ReversibilityClass = ReversibilityClass.R0,
    sensitivity_class: SensitivityClass = SensitivityClass.S1,
    action_type: str = "",
    compensation: Compensation | None = None,
    max_attempts: int = 3,
) -> Callable[[ToolHandler], Tool]:
    """Decorator form: wrap an async handler into a Tool."""

    def _wrap(handler: ToolHandler) -> Tool:
        return Tool(
            name=name,
            description=description,
            handler=handler,
            approval_class=approval_class,
            reversibility_class=reversibility_class,
            sensitivity_class=sensitivity_class,
            action_type=action_type,
            compensation=compensation,
            max_attempts=max_attempts,
        )

    return _wrap


__all__ = ["Compensation", "RiskLevel", "Tool", "ToolHandler", "ToolRegistry", "tool"]
