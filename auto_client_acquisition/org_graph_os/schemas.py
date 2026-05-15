"""Org graph schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GraphNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    node_id: str = Field(..., min_length=1)
    node_type: str = Field(..., min_length=1)
    label: str = ""


__all__ = ["GraphNode"]
