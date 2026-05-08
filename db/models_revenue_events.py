"""
SQLAlchemy 2.0 model for the revenue_events table.
جدول أحداث الإيرادات — السجل الثابت لذاكرة الإيرادات.

Append-only event log backing the Revenue Memory system.
All RevenueEvent fields are stored as columns; payload is JSONB.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.utils import utcnow
from db.models import Base


class RevenueEventRecord(Base):
    """
    Immutable event row in the revenue_events append-only log.
    صف حدث ثابت في سجل أحداث الإيرادات.

    Maps 1-to-1 with auto_client_acquisition.revenue_memory.events.RevenueEvent.
    """

    __tablename__ = "revenue_events"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(64), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(nullable=False)
    subject_type: Mapped[str] = mapped_column(String(64), nullable=False)
    subject_id: Mapped[str] = mapped_column(String(64), nullable=False)
    tenant_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    causation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    actor: Mapped[str] = mapped_column(String(128), nullable=False, default="system")
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utcnow)

    __table_args__ = (
        Index("ix_revevt_customer_occurred", "customer_id", "occurred_at"),
        Index("ix_revevt_tenant_occurred", "tenant_id", "occurred_at"),
        Index("ix_revevt_subject", "subject_type", "subject_id"),
        Index("ix_revevt_event_type", "event_type"),
        Index("ix_revevt_correlation", "correlation_id"),
    )
