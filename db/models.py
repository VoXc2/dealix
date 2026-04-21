"""
SQLAlchemy 2.0 async ORM models.
نماذج قاعدة البيانات.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Float, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.utils import utcnow


class Base(DeclarativeBase):
    """Base class for all models."""


class LeadRecord(Base):
    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(String(32), index=True)
    company_name: Mapped[str] = mapped_column(String(255), default="")
    contact_name: Mapped[str] = mapped_column(String(255), default="")
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    contact_phone: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    sector: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    region: Mapped[str | None] = mapped_column(String(128), nullable=True)
    company_size: Mapped[str | None] = mapped_column(String(32), nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="new", index=True)
    fit_score: Mapped[float] = mapped_column(Float, default=0.0)
    urgency_score: Mapped[float] = mapped_column(Float, default=0.0)
    locale: Mapped[str] = mapped_column(String(4), default="ar")
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    pain_points: Mapped[list] = mapped_column(JSON, default=list)
    meta_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    dedup_hash: Mapped[str] = mapped_column(String(32), default="", index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    deals: Mapped[list["DealRecord"]] = relationship(back_populates="lead")


class DealRecord(Base):
    __tablename__ = "deals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lead_id: Mapped[str] = mapped_column(ForeignKey("leads.id"), index=True)
    hubspot_deal_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    hubspot_contact_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(8), default="SAR")
    stage: Mapped[str] = mapped_column(String(64), default="new")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    lead: Mapped["LeadRecord"] = relationship(back_populates="deals")


class AgentRunRecord(Base):
    """Audit log — every agent invocation."""
    __tablename__ = "agent_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(64), index=True)
    lead_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(16), default="success")
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    input_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
