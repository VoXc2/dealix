"""Dealix - Lead Model"""
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, Enum as SAEnum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base


class LeadSource(str, enum.Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    SOCIAL_MEDIA = "social_media"
    GOOGLE_ADS = "google_ads"
    COLD_CALL = "cold_call"
    EMAIL_CAMPAIGN = "email_campaign"
    AFFILIATE = "affiliate"
    EVENT = "event"
    OTHER = "other"


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    CONVERTED = "converted"
    LOST = "lost"


class LeadScore(str, enum.Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    company: Mapped[str | None] = mapped_column(String(300))
    job_title: Mapped[str | None] = mapped_column(String(200))
    source: Mapped[LeadSource] = mapped_column(SAEnum(LeadSource), default=LeadSource.OTHER)
    status: Mapped[LeadStatus] = mapped_column(SAEnum(LeadStatus), default=LeadStatus.NEW)
    score: Mapped[LeadScore] = mapped_column(SAEnum(LeadScore), default=LeadScore.COLD)
    score_value: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(Text)
    estimated_value: Mapped[float] = mapped_column(Float, default=0.0)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    converted_deal_id: Mapped[int | None] = mapped_column(ForeignKey("deals.id"), index=True)
    last_contacted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    activities: Mapped[list["Activity"]] = relationship(back_populates="lead", lazy="selectin")
