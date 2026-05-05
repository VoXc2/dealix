"""Pydantic v2 schemas for the observability_v6 module.

Maps to the trace contract in
``docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`` §1.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class IncidentSeverity(StrEnum):
    """Tiered severity per the runbook §3."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class TraceRecord(BaseModel):
    """A single structured trace record. Frozen — append-only safe."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: str
    audit_id: str
    agent_run_id: str
    tenant_id: str
    object_id: str
    action_mode: str
    approval_status: str
    risk_level: str
    proof_event_id: Optional[str] = None
    latency_ms: float = Field(ge=0)
    cost: Optional[float] = None
    error_type: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AuditEvent(BaseModel):
    """A durable audit record wrapping a trace.

    The ``action_summary`` MUST NEVER contain raw PII; the
    ``record_audit`` helper redacts it via
    ``customer_data_plane.pii_redactor.redact_text`` before insert.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: f"aud_{uuid4().hex[:12]}")
    source_module: str
    action_summary: str
    trace: TraceRecord
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Incident(BaseModel):
    """Founder-filed (or auto-filed) incident record."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: f"inc_{uuid4().hex[:12]}")
    severity: IncidentSeverity
    title: str
    summary_ar: str
    summary_en: str
    root_cause: str = ""
    customer_impact: str = ""
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resolved_at: Optional[datetime] = None
