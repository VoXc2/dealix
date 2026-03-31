"""Dealix - Affiliate Models"""
from datetime import datetime
from sqlalchemy import String, Float, Integer, Boolean, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base


class AffiliateStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class PayoutStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"


class AffiliateProfile(Base):
    __tablename__ = "affiliate_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True, nullable=False)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    bio: Mapped[str | None] = mapped_column(Text)
    website: Mapped[str | None] = mapped_column(String(500))
    social_links: Mapped[str | None] = mapped_column(Text)
    niche: Mapped[str | None] = mapped_column(String(200))
    audience_size: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[AffiliateStatus] = mapped_column(SAEnum(AffiliateStatus), default=AffiliateStatus.PENDING)
    base_commission_rate: Mapped[float] = mapped_column(Float, default=10.0)
    tier_level: Mapped[int] = mapped_column(Integer, default=1)
    total_earnings: Mapped[float] = mapped_column(Float, default=0.0)
    total_clicks: Mapped[int] = mapped_column(Integer, default=0)
    total_conversions: Mapped[int] = mapped_column(Integer, default=0)
    bank_name: Mapped[str | None] = mapped_column(String(200))
    iban: Mapped[str | None] = mapped_column(String(34))
    paypal_email: Mapped[str | None] = mapped_column(String(255))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="affiliate_profile", lazy="selectin")
    links: Mapped[list["AffiliateLink"]] = relationship(back_populates="affiliate", lazy="selectin")
    payouts: Mapped[list["AffiliatePayout"]] = relationship(back_populates="affiliate", lazy="selectin")


class AffiliateLink(Base):
    __tablename__ = "affiliate_links"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    affiliate_id: Mapped[int] = mapped_column(ForeignKey("affiliate_profiles.id"), index=True, nullable=False)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deals.id"), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    destination_url: Mapped[str] = mapped_column(String(500), nullable=False)
    utm_source: Mapped[str | None] = mapped_column(String(100))
    utm_medium: Mapped[str | None] = mapped_column(String(100))
    utm_campaign: Mapped[str | None] = mapped_column(String(100))
    click_count: Mapped[int] = mapped_column(Integer, default=0)
    conversion_count: Mapped[int] = mapped_column(Integer, default=0)
    earnings: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    affiliate: Mapped["AffiliateProfile"] = relationship(back_populates="links", lazy="selectin")
    deal: Mapped["Deal"] = relationship(back_populates="affiliate_links", lazy="selectin")
    clicks: Mapped[list["AffiliateClick"]] = relationship(back_populates="link", lazy="selectin")


class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("affiliate_links.id"), index=True, nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(500))
    referrer: Mapped[str | None] = mapped_column(String(500))
    country: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str | None] = mapped_column(String(100))
    converted: Mapped[bool] = mapped_column(Boolean, default=False)
    conversion_amount: Mapped[float] = mapped_column(Float, default=0.0)
    commission_earned: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    link: Mapped["AffiliateLink"] = relationship(back_populates="clicks", lazy="selectin")


class AffiliatePayout(Base):
    __tablename__ = "affiliate_payouts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    affiliate_id: Mapped[int] = mapped_column(ForeignKey("affiliate_profiles.id"), index=True, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="SAR")
    status: Mapped[PayoutStatus] = mapped_column(SAEnum(PayoutStatus), default=PayoutStatus.PENDING)
    payment_method: Mapped[str] = mapped_column(String(50), default="bank_transfer")
    reference_number: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    affiliate: Mapped["AffiliateProfile"] = relationship(back_populates="payouts", lazy="selectin")


class CommissionTier(Base):
    __tablename__ = "commission_tiers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), index=True, nullable=False)
    tier_level: Mapped[int] = mapped_column(Integer, nullable=False)
    min_conversions: Mapped[int] = mapped_column(Integer, default=0)
    max_conversions: Mapped[int] = mapped_column(Integer, default=0)
    commission_rate: Mapped[float] = mapped_column(Float, nullable=False)
    bonus_amount: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
