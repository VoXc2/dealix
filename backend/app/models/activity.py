"""Dealix - Activity Model"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base


class ActivityType(str, enum.Enum):
    DEAL_CREATED = "deal_created"
    DEAL_UPDATED = "deal_updated"
    DEAL_STAGE_CHANGED = "deal_stage_changed"
    DEAL_CLOSED_WON = "deal_closed_won"
    DEAL_CLOSED_LOST = "deal_closed_lost"
    LEAD_CREATED = "lead_created"
    LEAD_STATUS_CHANGED = "lead_status_changed"
    MEETING_SCHEDULED = "meeting_scheduled"
    MEETING_COMPLETED = "meeting_completed"
    AFFILIATE_APPROVED = "affiliate_approved"
    PAYOUT_PROCESSED = "payout_processed"
    REDEMPTION_VERIFIED = "redemption_verified"
    NOTE_ADDED = "note_added"
    EMAIL_SENT = "email_sent"
    CALL_MADE = "call_made"
    USER_LOGIN = "user_login"


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[ActivityType] = mapped_column(SAEnum(ActivityType), nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[str | None] = mapped_column(Text)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    deal_id: Mapped[int | None] = mapped_column(ForeignKey("deals.id"), index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("leads.id"), index=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="activities", foreign_keys=[user_id], lazy="selectin")
    deal: Mapped["Deal"] = relationship(back_populates="activities", foreign_keys=[deal_id], lazy="selectin")
    lead: Mapped["Lead"] = relationship(back_populates="activities", foreign_keys=[lead_id], lazy="selectin")
