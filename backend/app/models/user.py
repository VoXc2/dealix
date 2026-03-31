"""Dealix - User Model"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    SALES_MANAGER = "sales_manager"
    SALES_REP = "sales_rep"
    AFFILIATE_MANAGER = "affiliate_manager"
    AFFILIATE = "affiliate"
    MERCHANT = "merchant"
    VIEWER = "viewer"

class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    full_name_en: Mapped[str | None] = mapped_column(String(200))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    status: Mapped[UserStatus] = mapped_column(SAEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_phone_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    login_count: Mapped[int] = mapped_column(default=0)
    api_key: Mapped[str | None] = mapped_column(String(100), unique=True)
    locale: Mapped[str] = mapped_column(String(10), default="ar_SA")
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Riyadh")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    organization_memberships: Mapped[list["OrganizationMember"]] = relationship(back_populates="user", lazy="selectin")
    owned_organizations: Mapped[list["Organization"]] = relationship(back_populates="owner", lazy="selectin")
    deals: Mapped[list["Deal"]] = relationship(back_populates="assigned_to_user", lazy="selectin")
    activities: Mapped[list["Activity"]] = relationship(back_populates="user", lazy="selectin")
    affiliate_profile: Mapped["AffiliateProfile | None"] = relationship(back_populates="user", lazy="selectin", uselist=False)
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user", lazy="selectin")
    meetings_created: Mapped[list["Meeting"]] = relationship(back_populates="created_by_user", foreign_keys="Meeting.created_by", lazy="selectin")
