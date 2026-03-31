"""Dealix - Deal Model"""
from datetime import datetime
from sqlalchemy import String, Float, Integer, Boolean, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base

class DealStage(str, enum.Enum):
    NEW = "new"; CONTACTED = "contacted"; QUALIFIED = "qualified"
    PROPOSAL = "proposal"; NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"; CLOSED_LOST = "closed_lost"

class DealType(str, enum.Enum):
    STANDARD = "standard"; FLASH = "flash"; EXCLUSIVE = "exclusive"; BUNDLE = "bundle"

class Deal(Base):
    __tablename__ = "deals"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(300), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    terms_conditions: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    gallery_urls: Mapped[str | None] = mapped_column(Text)
    deal_type: Mapped[DealType] = mapped_column(SAEnum(DealType), default=DealType.STANDARD)
    stage: Mapped[DealStage] = mapped_column(SAEnum(DealStage), default=DealStage.NEW)
    category: Mapped[str | None] = mapped_column(String(100))
    tags: Mapped[str | None] = mapped_column(Text)
    original_price: Mapped[float] = mapped_column(Float, default=0.0)
    deal_price: Mapped[float] = mapped_column(Float, default=0.0)
    discount_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    commission_amount: Mapped[float] = mapped_column(Float, default=0.0)
    commission_type: Mapped[str] = mapped_column(String(20), default="percentage")
    currency: Mapped[str] = mapped_column(String(10), default="SAR")
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    max_redemptions: Mapped[int | None] = mapped_column(Integer)
    current_redemptions: Mapped[int] = mapped_column(Integer, default=0)
    min_order_value: Mapped[float] = mapped_column(Float, default=0.0)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), index=True)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    merchant_contact_id: Mapped[int | None] = mapped_column(ForeignKey("merchants.id"), index=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    click_count: Mapped[int] = mapped_column(Integer, default=0)
    share_count: Mapped[int] = mapped_column(Integer, default=0)
    conversion_rate: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    organization: Mapped["Organization"] = relationship(back_populates="deals", lazy="selectin")
    assigned_to_user: Mapped["User"] = relationship(back_populates="deals", foreign_keys=[assigned_to], lazy="selectin")
    redemptions: Mapped[list["DealRedemption"]] = relationship(back_populates="deal", lazy="selectin")
    affiliate_links: Mapped[list["AffiliateLink"]] = relationship(back_populates="deal", lazy="selectin")
    activities: Mapped[list["Activity"]] = relationship(back_populates="deal", lazy="selectin")

class DealRedemption(Base):
    __tablename__ = "deal_redemptions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deals.id"), index=True, nullable=False)
    affiliate_link_id: Mapped[int | None] = mapped_column(ForeignKey("affiliate_links.id"), index=True)
    customer_name: Mapped[str | None] = mapped_column(String(200))
    customer_phone: Mapped[str | None] = mapped_column(String(20))
    customer_email: Mapped[str | None] = mapped_column(String(255))
    redemption_code: Mapped[str | None] = mapped_column(String(50), unique=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    commission_earned: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    deal: Mapped["Deal"] = relationship(back_populates="redemptions", lazy="selectin")
