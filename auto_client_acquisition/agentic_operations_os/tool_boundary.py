"""Tool Boundary — 6 classes; MVP allows A/B/C only."""

from __future__ import annotations

from enum import Enum


class ToolClass(str, Enum):
    A_READ_ONLY = "read_only"
    B_ANALYSIS = "analysis"
    C_DRAFT_GENERATION = "draft_generation"
    D_INTERNAL_WRITE = "internal_write"          # requires approval
    E_EXTERNAL_ACTION = "external_action"        # blocked in MVP
    F_HIGH_RISK = "high_risk"                    # forbidden


TOOL_CLASSES: tuple[ToolClass, ...] = tuple(ToolClass)


def is_tool_class_allowed_in_mvp(c: ToolClass) -> bool:
    return c in {
        ToolClass.A_READ_ONLY,
        ToolClass.B_ANALYSIS,
        ToolClass.C_DRAFT_GENERATION,
    }
