"""Tool boundary enforcement (delegates to agent MVP permissions)."""

from __future__ import annotations

from auto_client_acquisition.agent_os.tool_permissions import FORBIDDEN_TOOLS_MVP, tool_allowed_mvp


def tool_boundary_ok(tool: str) -> bool:
    return tool_allowed_mvp(tool)


__all__ = ["FORBIDDEN_TOOLS_MVP", "tool_boundary_ok"]
