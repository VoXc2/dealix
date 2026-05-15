"""Schemas for System 30 — the Operational Memory Graph."""

from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class NodeType(StrEnum):
    PERSON = "person"
    WORKFLOW = "workflow"
    APPROVAL = "approval"
    INCIDENT = "incident"
    RISK = "risk"
    DEPARTMENT = "department"
    AGENT = "agent"


class Relation(StrEnum):
    DEPENDS_ON = "depends_on"
    AFFECTED_BY = "affected_by"
    CAUSED = "caused"
    OWNS = "owns"
    ESCALATES_TO = "escalates_to"
    RELATED_TO = "related_to"


class GraphNode(BaseModel):
    """A node in the operational memory graph."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    node_id: str = Field(..., min_length=1)
    node_type: NodeType
    label: str = ""
    attributes: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """A directed, weighted edge between two nodes."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    edge_id: str = Field(default_factory=lambda: f"edg_{uuid4().hex[:12]}")
    from_id: str
    to_id: str
    relation: Relation = Relation.RELATED_TO
    weight: float = 1.0


class IncidentImpact(BaseModel):
    """The blast radius of one incident."""

    model_config = ConfigDict(extra="forbid")

    incident_id: str
    root_cause: GraphNode | None
    affected: list[GraphNode] = Field(default_factory=list)
    related_workflows: list[str] = Field(default_factory=list)
    related_agents: list[str] = Field(default_factory=list)
    resulting_risks: list[str] = Field(default_factory=list)
