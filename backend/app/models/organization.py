"""Dealix - Organization Model"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Text, Enum as SAEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base

class OrgType(str, enum.Enum):
    MERCHANT = "merchant"
    AFFILIATE_NETWORK = "affiliate_network"
    AGENCY = "agency"
    INDIVIDUAL = "individual"

class OrgStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(300))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    logo_url: Mapped[str | None] = mapped_column(String(500))
    website: Mapped[str | None] = mapped_column(String(500))
    cr_number: Mapped[str | None] = mapped_column(String(50))
    vat_number: Mapped[str | None] = mapped_column(String(50))
    org_type: Mapped[OrgType] = mapped_column(SAEnum(OrgType), default=OrgType.MERCHANT)
    status: Mapped[OrgStatus] = mapped_column(SAEnum(OrgStatus), default=OrgStatus.PENDING)
    industry: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100), default="Saudi Arabia")
    address: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(index=True, nullable=False)
    max_deals: Mapped[int] = mapped_column(Integer, default=100)
    max_users: Mapped[int] = mapped_column(Integer, default=10)
    commission_rate: Mapped[float] = mapped_column(default=0.0)
    subscription_tier: Mapped[str] = mapped_column(String(50), default="free")
    stripe_customer_id: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    owner: Mapped["User"] = relationship(back_populates="owned_organizations", foreign_keys=[owner_id], lazy="selectin")
    members: Mapped[list["OrganizationMember"]] = relationship(back_populates="organization", lazy="selectin")
    deals: Mapped[list["Deal"]] = relationship(back_populates="organization", lazy="selectin")
    api_keys: Mapped[list["APIKey"]] = relationship(back_populates="organization", lazy="selectin")

class OrganizationMember(Base):
    __tablename__ = "organization_members"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    role_in_org: Mapped[str] = mapped_column(String(50), default="member")
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    organization: Mapped["Organization"] = relationship(back_populates="members", lazy="selectin")
    user: Mapped["User"] = relationship(back_populates="organization_memberships", lazy="selectin")
