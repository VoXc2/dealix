"""Schemas for the unified operating graph (Phase 3)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

NodeType = Literal[
    "company",
    "contact",
    "lead",
    "deal",
    "service_session",
    "approval",
    "payment_state",
    "support_ticket",
    "proof_event",
    "executive_pack",
    "case_study_candidate",
    "partner",
]

EdgeType = Literal[
    "lead_belongs_to_company",
    "deal_created_from_lead",
    "payment_unblocks_service",
    "service_creates_proof",
    "support_ticket_blocks_delivery",
    "approval_blocks_action",
    "proof_enables_case_study",
]


class GraphNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node_id: str
    node_type: NodeType
    customer_handle: str
    label_ar: str = ""
    label_en: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    source_module: str = ""


class GraphEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_node_id: str
    target_node_id: str
    edge_type: EdgeType


class UnifiedGraph(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_handle: str
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
    degraded_sections: list[dict[str, Any]] = Field(default_factory=list)
    data_status: Literal["insufficient_data", "partial", "live"] = "insufficient_data"
    safety_summary: str = "no_pii_no_internal_terms_read_only"
    built_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def is_empty(self) -> bool:
        return len(self.nodes) == 0
