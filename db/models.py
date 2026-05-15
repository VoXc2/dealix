"""
SQLAlchemy 2.0 async ORM models.
نماذج قاعدة البيانات.

Changes (enterprise upgrade):
  - TenantRecord: multi-tenant isolation
  - UserRecord: user auth with hashed password + role
  - RoleRecord: RBAC role definitions
  - AuditLogRecord: data access audit trail (PDPL Art. 18)
  - BackgroundJobRecord: async task queue tracking
  - ContactEmbeddingRecord: pgvector Revenue Memory
  - ZATCAInvoiceRecord: e-invoice compliance
  - Soft-delete (deleted_at) added to key models
  - tenant_id FK added to LeadRecord, DealRecord, AccountRecord, ContactRecord
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.utils import utcnow


class Base(DeclarativeBase):
    """Base class for all models."""


class SoftDeleteMixin:
    """
    Mixin that adds soft-delete support.
    خلط يضيف دعم الحذف الناعم.

    Usage: class MyModel(SoftDeleteMixin, Base): ...
    Filter active rows: session.query(MyModel).filter(MyModel.deleted_at.is_(None))
    """

    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True, index=True)


# ── Multi-Tenancy ─────────────────────────────────────────────────

class TenantRecord(Base):
    """
    Tenant = one subscribing enterprise client.
    المستأجر = عميل مؤسسي مشترك واحد.

    Every data row in the system carries tenant_id for strict isolation.
    Row-level security policies enforce this at DB level in production.
    """

    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    plan: Mapped[str] = mapped_column(String(32), default="pilot")  # pilot/starter/growth/scale
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)  # active/suspended/churned
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Riyadh")
    locale: Mapped[str] = mapped_column(String(4), default="ar")
    currency: Mapped[str] = mapped_column(String(8), default="SAR")
    max_users: Mapped[int] = mapped_column(Integer, default=5)
    max_leads_per_month: Mapped[int] = mapped_column(Integer, default=1000)
    features: Mapped[dict] = mapped_column(JSON, default=dict)  # feature flag overrides
    meta_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    users: Mapped[list["UserRecord"]] = relationship(back_populates="tenant")


class TenantThemeRecord(Base):
    """
    Tenant white-label theme overrides (W3.2 scaffold → W7.5 wiring).

    Each subscribing agency partner / enterprise customer can override
    the Dealix default brand palette + display name. Stored as discrete
    columns (not JSON) so each field has its own validator + DB index
    and migration history is clean.

    Read via GET /api/v1/tenants/{handle}/theme.css (returns a <style>
    block with :root CSS custom properties). Set via admin endpoint
    POST /api/v1/admin/tenants/{handle}/theme.
    """

    __tablename__ = "tenant_themes"

    tenant_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True
    )
    brand_primary: Mapped[str] = mapped_column(String(32), default="#0f172a")
    brand_accent: Mapped[str] = mapped_column(String(32), default="#10b981")
    brand_muted: Mapped[str] = mapped_column(String(32), default="#64748b")
    brand_surface: Mapped[str] = mapped_column(String(32), default="#ffffff")
    brand_bg: Mapped[str] = mapped_column(String(32), default="#f8fafc")
    font_arabic: Mapped[str] = mapped_column(String(128), default="IBM Plex Sans Arabic")
    font_english: Mapped[str] = mapped_column(String(128), default="Inter")
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    display_name: Mapped[str] = mapped_column(String(128), default="Dealix")
    custom_domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class RoleRecord(Base):
    """
    RBAC role definitions.
    تعريفات دور التحكم في الوصول.

    Default roles: owner, admin, sales_rep, viewer, agent_operator
    """

    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(64), index=True)  # owner/admin/sales_rep/viewer
    permissions: Mapped[list] = mapped_column(JSON, default=list)
    # e.g. ["leads:read", "leads:write", "deals:read", "agents:run", "admin:*"]
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)  # system roles cannot be deleted
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_role_tenant_name"),)


class UserRecord(Base):
    """
    User account with hashed password + role assignment.
    حساب مستخدم مع كلمة مرور مشفرة وتعيين دور.

    Authentication: JWT tokens issued at /api/v1/auth/token
    Password: bcrypt-hashed, never stored in plaintext
    MFA: TOTP support via totp_secret
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    role_id: Mapped[str | None] = mapped_column(ForeignKey("roles.id"), nullable=True, index=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    hashed_password: Mapped[str] = mapped_column(String(255), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    # System-level role — spans all tenants (super_admin only). Null for regular users.
    system_role: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    # MFA
    totp_secret: Mapped[str | None] = mapped_column(String(64), nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    # Password reset
    reset_token: Mapped[str | None] = mapped_column(String(128), nullable=True)
    reset_token_expires_at: Mapped[datetime | None] = mapped_column(nullable=True)
    # Timestamps
    last_login_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    tenant: Mapped["TenantRecord | None"] = relationship(back_populates="users")

    __table_args__ = (UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),)


# ── Audit Log (PDPL Article 18) ──────────────────────────────────

class AuditLogRecord(Base):
    """
    Data access + mutation audit trail — required by PDPL Article 18.
    سجل تدقيق الوصول والتعديل على البيانات — مطلوب بموجب المادة 18 من نظام PDPL.

    Every sensitive read (contact PII, deal financials) and every write
    (create/update/delete) must produce one row here.
    """

    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    user_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(64), index=True)  # e.g. "contact.read", "lead.create", "contact.delete"
    entity_type: Mapped[str] = mapped_column(String(64), index=True)  # contact/lead/deal/user/tenant
    entity_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    diff: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # before/after for writes
    status: Mapped[str] = mapped_column(String(16), default="ok")  # ok/denied/error
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)

    __table_args__ = (
        Index("ix_audit_tenant_created", "tenant_id", "created_at"),
        Index("ix_audit_entity", "entity_type", "entity_id"),
    )


class LeadRecord(Base):
    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
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
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    deals: Mapped[list["DealRecord"]] = relationship(back_populates="lead")

    __table_args__ = (Index("ix_leads_tenant_status", "tenant_id", "status"),)


class DealRecord(Base):
    __tablename__ = "deals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    lead_id: Mapped[str] = mapped_column(ForeignKey("leads.id"), index=True)
    hubspot_deal_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    hubspot_contact_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(8), default="SAR")
    stage: Mapped[str] = mapped_column(String(64), default="new")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    lead: Mapped["LeadRecord"] = relationship(back_populates="deals")

    __table_args__ = (Index("ix_deals_tenant_stage", "tenant_id", "stage"),)


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
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_agent_runs_name_status", "agent_name", "status"),)


class ConversationRecord(Base):
    """Inbound message + outbound auto-response — full audit log."""

    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lead_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)  # whatsapp/email/form/sms/linkedin
    sender: Mapped[str | None] = mapped_column(String(255), nullable=True)
    inbound_message: Mapped[str] = mapped_column(Text, default="")
    outbound_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    classification: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    sentiment: Mapped[str | None] = mapped_column(String(16), nullable=True)
    next_action: Mapped[str | None] = mapped_column(String(64), nullable=True)
    escalation_required: Mapped[bool] = mapped_column(default=False)
    auto_sent: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_conversations_channel_created", "channel", "created_at"),)


class TaskRecord(Base):
    """Follow-up tasks scheduled by the autonomous engine."""

    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lead_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    deal_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    task_type: Mapped[str] = mapped_column(String(32), index=True)  # follow_up, demo, payment_check, onboarding
    due_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)  # pending, done, skipped
    owner: Mapped[str] = mapped_column(String(64), default="auto")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_tasks_status_due", "status", "due_at"),)


class CompanyRecord(Base):
    """Subscriber company profile — one per Dealix customer."""

    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    country: Mapped[str | None] = mapped_column(String(64), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    products: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_customer_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    average_deal_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    sales_cycle_length_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_lead_sources: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_crm: Mapped[str | None] = mapped_column(String(64), nullable=True)
    booking_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sales_team_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    whatsapp_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    tone_of_voice: Mapped[str] = mapped_column(String(64), default="professional_khaliji")
    languages: Mapped[str] = mapped_column(String(64), default="ar,en")
    pricing_rules: Mapped[str | None] = mapped_column(Text, nullable=True)
    handoff_rules: Mapped[str | None] = mapped_column(Text, nullable=True)
    privacy_requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    success_metric: Mapped[str | None] = mapped_column(Text, nullable=True)
    icp_profile: Mapped[dict] = mapped_column("icp_profile", JSON, default=dict)
    channel_plan: Mapped[dict] = mapped_column("channel_plan", JSON, default=dict)
    offer_ladder: Mapped[dict] = mapped_column("offer_ladder", JSON, default=dict)
    automation_policy: Mapped[dict] = mapped_column("automation_policy", JSON, default=dict)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)


class PartnerRecord(Base):
    """Partner/agency record for distribution channel."""

    __tablename__ = "partners"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255))
    partner_type: Mapped[str] = mapped_column(String(32), index=True)  # AGENCY/IMPLEMENTATION/REFERRAL/STRATEGIC
    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="prospecting", index=True)  # prospecting/active/paused
    commission_terms: Mapped[str | None] = mapped_column(Text, nullable=True)
    setup_fee_sar: Mapped[float] = mapped_column(Float, default=0.0)
    mrr_share_pct: Mapped[float] = mapped_column(Float, default=0.0)
    clients_signed: Mapped[int] = mapped_column(default=0)
    next_action: Mapped[str | None] = mapped_column(String(64), nullable=True)
    next_action_at: Mapped[datetime | None] = mapped_column(nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)


class CustomerRecord(Base):
    """Customer = subscribed paying company. One per closed deal."""

    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    deal_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    plan: Mapped[str] = mapped_column(String(32), default="pilot")  # pilot/starter/growth/scale
    onboarding_status: Mapped[str] = mapped_column(String(32), default="kickoff_pending", index=True)
    pilot_start_at: Mapped[datetime | None] = mapped_column(nullable=True)
    pilot_end_at: Mapped[datetime | None] = mapped_column(nullable=True)
    success_metric: Mapped[str | None] = mapped_column(Text, nullable=True)
    daily_report_sent: Mapped[int] = mapped_column(default=0)
    nps_score: Mapped[int | None] = mapped_column(nullable=True)
    churn_risk: Mapped[str] = mapped_column(String(16), default="low")  # low/medium/high
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)


class OutreachQueueRecord(Base):
    """Outreach message queue — auto or human-approval."""

    __tablename__ = "outreach_queue"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lead_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)
    message: Mapped[str] = mapped_column(Text)
    approval_required: Mapped[bool] = mapped_column(default=True)
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)  # queued/approved/sent/skipped
    due_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    sent_at: Mapped[datetime | None] = mapped_column(nullable=True)
    risk_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


# ── Data Lake + Lead Graph (Phase 12) ──────────────────────────────
# Compliant ingestion: every row carries source/allowed_use/risk/opt-out.

class RawLeadImport(Base):
    """One row per uploaded dataset (CSV/Excel/JSON)."""

    __tablename__ = "raw_lead_imports"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_name: Mapped[str] = mapped_column(String(255), index=True)
    source_type: Mapped[str] = mapped_column(String(32), index=True)  # owned/public/paid/partner/google_maps/google_search/manual
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    imported_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    allowed_use: Mapped[str] = mapped_column(String(128), default="business_contact_research_only")
    consent_status: Mapped[str] = mapped_column(String(32), default="unknown")  # unknown/opted_in/legitimate_interest/owned
    risk_level: Mapped[str] = mapped_column(String(16), default="medium", index=True)  # low/medium/high
    rows_total: Mapped[int] = mapped_column(Integer, default=0)
    rows_normalized: Mapped[int] = mapped_column(Integer, default=0)
    rows_rejected: Mapped[int] = mapped_column(Integer, default=0)
    rows_duplicate: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="raw", index=True)  # raw/normalizing/normalized/deduped/done/error
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class RawLeadRow(Base):
    """One row per record inside an import."""

    __tablename__ = "raw_lead_rows"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    import_id: Mapped[str] = mapped_column(String(64), index=True)
    raw_json: Mapped[dict] = mapped_column(JSON, default=dict)
    normalized_status: Mapped[str] = mapped_column(String(32), default="pending", index=True)  # pending/ok/rejected/duplicate
    account_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    error: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class AccountRecord(Base):
    """Canonical company entity in the lead graph."""

    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), index=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    country: Mapped[str | None] = mapped_column(String(64), nullable=True, default="SA")
    sector: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    google_place_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    source_count: Mapped[int] = mapped_column(Integer, default=1)
    best_source: Mapped[str | None] = mapped_column(String(64), nullable=True)
    risk_level: Mapped[str] = mapped_column(String(16), default="medium", index=True)
    status: Mapped[str] = mapped_column(String(32), default="new", index=True)  # new/enriched/qualified/blocked
    data_quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    extra: Mapped[dict] = mapped_column("extra_json", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        Index("ix_accounts_sector_status", "sector", "status"),
        Index("ix_accounts_city_sector", "city", "sector"),
    )


class ContactRecord(Base):
    """Person attached to an account. PDPL-aware: opt_out + consent_status mandatory."""

    __tablename__ = "contacts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str | None] = mapped_column(String(128), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source: Mapped[str] = mapped_column(String(64), default="manual", index=True)
    consent_status: Mapped[str] = mapped_column(String(32), default="unknown", index=True)
    opt_out: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    risk_level: Mapped[str] = mapped_column(String(16), default="medium")
    pdpl_erasure_requested_at: Mapped[datetime | None] = mapped_column(nullable=True)
    pdpl_erased_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_contacts_tenant_account", "tenant_id", "account_id"),)


class SignalRecord(Base):
    """Time-series signals attached to an account (tech, intent, hire, news)."""

    __tablename__ = "signals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    account_id: Mapped[str] = mapped_column(String(64), index=True)
    signal_type: Mapped[str] = mapped_column(String(64), index=True)  # tech/intent/hire/news/funding/integration
    signal_value: Mapped[str] = mapped_column(String(500))
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    detected_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)


class LeadScoreRecord(Base):
    """Latest score per account (one current row per account)."""

    __tablename__ = "lead_scores"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    account_id: Mapped[str] = mapped_column(String(64), index=True)
    fit_score: Mapped[float] = mapped_column(Float, default=0.0)
    intent_score: Mapped[float] = mapped_column(Float, default=0.0)
    urgency_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    total_score: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    priority: Mapped[str] = mapped_column(String(8), default="P3", index=True)  # P0/P1/P2/P3/BACKLOG
    recommended_channel: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)


class SuppressionRecord(Base):
    """Opt-out / do-not-contact list. Checked before any outbound queue write."""

    __tablename__ = "data_suppression_list"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    reason: Mapped[str] = mapped_column(String(128), default="opt_out")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class GmailDraftRecord(Base):
    """Gmail draft created by the revenue machine — Sami reviews + sends."""

    __tablename__ = "gmail_drafts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    account_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    queue_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    to_email: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(500))
    body_plain: Mapped[str] = mapped_column(Text)
    sender_email: Mapped[str] = mapped_column(String(255), default="")
    gmail_draft_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    gmail_message_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="created", index=True)
    # created | reviewed | sent | discarded | failed
    sequence_step: Mapped[int] = mapped_column(Integer, default=0)
    sent_at: Mapped[datetime | None] = mapped_column(nullable=True, index=True)
    discarded_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class LinkedInDraftRecord(Base):
    """LinkedIn drafts — manual send only (no automation per LinkedIn ToS)."""

    __tablename__ = "linkedin_drafts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    account_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255))
    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    profile_search_query: Mapped[str] = mapped_column(String(500))
    company_context: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason_for_outreach: Mapped[str | None] = mapped_column(Text, nullable=True)
    message_ar: Mapped[str] = mapped_column(Text)
    message_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    followup_day_3: Mapped[str | None] = mapped_column(Text, nullable=True)
    followup_day_7: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    # draft | sent | replied | unreachable
    sent_at: Mapped[datetime | None] = mapped_column(nullable=True)
    reply_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    reply_received_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class DataSourceProvenance(Base):
    """Provenance record — every signal/account/contact pointer back to source.

    Required for PDPL audit trail + to dedupe "same lead from 3 sources".
    """

    __tablename__ = "data_source_provenance"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(32), index=True)  # account|contact|signal|deal
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    source_name: Mapped[str] = mapped_column(String(255), index=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_type: Mapped[str] = mapped_column(String(32))  # public|paid|partner|owned|google_maps|google_search|manual
    allowed_use: Mapped[str] = mapped_column(String(128), default="business_contact_research_only")
    collected_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    refresh_needed: Mapped[bool] = mapped_column(Boolean, default=False)


class EmailSendLog(Base):
    """Auditable log of every email send attempt — required for compliance + bounce tracking."""

    __tablename__ = "email_send_log"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    account_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    queue_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    to_email: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(500))
    body_preview: Mapped[str] = mapped_column(Text, default="")
    sender_email: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    # queued | sent | bounced | replied | opt_out | blocked_compliance | failed
    gmail_message_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    bounce_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reply_classification: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reply_received_at: Mapped[datetime | None] = mapped_column(nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(nullable=True, index=True)
    batch_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    sequence_step: Mapped[int] = mapped_column(Integer, default=0)  # 0=initial, 2/5/10 for follow-ups
    compliance_check: Mapped[dict] = mapped_column("compliance_check_json", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class WebhookSubscriptionRecord(Base):
    """Outbound webhook subscription — Scale tier ecosystem play.

    Customers register an HTTPS endpoint + secret. Dealix POSTs signed events
    when matching activity occurs (lead.created, deal.won, payment.received...).
    """

    __tablename__ = "webhook_subscriptions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(64), index=True)
    endpoint_url: Mapped[str] = mapped_column(String(500))
    secret: Mapped[str] = mapped_column(String(128))  # HMAC signing key — never exposed back
    events: Mapped[list] = mapped_column(JSON, default=list)  # empty list = all events
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_delivery_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class WebhookDeliveryRecord(Base):
    """Per-attempt delivery audit — debug + replay support."""

    __tablename__ = "webhook_deliveries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    subscription_id: Mapped[str] = mapped_column(String(64), index=True)
    customer_id: Mapped[str] = mapped_column(String(64), index=True)
    event_id: Mapped[str] = mapped_column(String(64), index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    endpoint_url: Mapped[str] = mapped_column(String(500))
    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    error: Mapped[str | None] = mapped_column(String(500), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    request_signature: Mapped[str] = mapped_column(String(255), default="")
    payload: Mapped[dict] = mapped_column("payload_json", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)


# ── Async Task Queue ──────────────────────────────────────────────

class BackgroundJobRecord(Base):
    """
    Persistent record for every background/async job (agent run, LLM call, outreach batch).
    سجل مستمر لكل مهمة خلفية.

    Status lifecycle: pending → running → succeeded | failed | retrying
    Worker polls this table via ARQ or Celery result backend.
    """

    __tablename__ = "background_jobs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    job_type: Mapped[str] = mapped_column(String(64), index=True)
    # e.g. "lead_score", "proposal_draft", "outreach_batch", "email_campaign"
    status: Mapped[str] = mapped_column(String(16), default="pending", index=True)
    # pending / running / succeeded / failed / retrying
    input_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    output_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (Index("ix_jobs_tenant_status", "tenant_id", "status"),)


# ── Revenue Memory (pgvector) ─────────────────────────────────────

class AccountEmbeddingRecord(Base):
    """
    Vector embedding of account profile for semantic search — Revenue Memory.
    تضمين متجهي لملف الحساب للبحث الدلالي — ذاكرة الإيرادات.

    Stored as JSON array (compatible with all PostgreSQL setups).
    For production with pgvector extension: migrate to VECTOR(1536) column type.
    Usage: semantic similarity search to find accounts matching a query profile.

    Example:
        embedding = await EmbeddingService().embed("logistics startup Riyadh 50 employees")
        similar_accounts = await semantic_search(embedding, top_k=10)
    """

    __tablename__ = "account_embeddings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), unique=True, index=True)
    embedding_json: Mapped[list] = mapped_column(JSON, default=list)
    # Serialised float array — use pgvector VECTOR column in production migration
    model_name: Mapped[str] = mapped_column(String(128), default="text-embedding-3-small")
    text_used: Mapped[str | None] = mapped_column(Text, nullable=True)
    # The text that was embedded (for cache invalidation / re-embedding)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class ConversationEmbeddingRecord(Base):
    """
    Vector embedding of conversation turns for agent memory / retrieval.
    تضمين متجهي لمحادثة — ذاكرة الوكيل.
    """

    __tablename__ = "conversation_embeddings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"), index=True)
    embedding_json: Mapped[list] = mapped_column(JSON, default=list)
    model_name: Mapped[str] = mapped_column(String(128), default="text-embedding-3-small")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


# ── ZATCA E-Invoice (Phase 2 — Saudi legal requirement) ──────────

class ZATCAInvoiceRecord(Base):
    """
    ZATCA Phase 2 e-invoice record — Fatoorah API compliant.
    سجل الفاتورة الإلكترونية وفق المرحلة الثانية لنظام فاتورة ZATCA.

    Required for any Saudi B2B VAT invoice.
    Phase 2 mandate: all invoices must be cleared/reported to ZATCA in real-time.
    """

    __tablename__ = "zatca_invoices"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    deal_id: Mapped[str | None] = mapped_column(ForeignKey("deals.id"), nullable=True, index=True)
    customer_id: Mapped[str | None] = mapped_column(ForeignKey("customers.id"), nullable=True, index=True)
    invoice_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    # Format: SELLER_TAX_NUMBER-YEAR-SEQUENCE e.g. 311111111100003-1-1
    invoice_type: Mapped[str] = mapped_column(String(32), default="simplified")
    # simplified (B2C) | standard (B2B)
    issue_date: Mapped[str] = mapped_column(String(10))  # YYYY-MM-DD
    issue_time: Mapped[str] = mapped_column(String(8))   # HH:MM:SS
    seller_vat_number: Mapped[str] = mapped_column(String(15))
    buyer_vat_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    buyer_name: Mapped[str] = mapped_column(String(255))
    subtotal_sar: Mapped[float] = mapped_column(Float)
    vat_amount_sar: Mapped[float] = mapped_column(Float)
    total_sar: Mapped[float] = mapped_column(Float)
    vat_rate: Mapped[float] = mapped_column(Float, default=0.15)  # 15% standard KSA VAT
    line_items: Mapped[list] = mapped_column(JSON, default=list)
    # zatca_xml: Base64-encoded UBL XML
    zatca_xml_b64: Mapped[str | None] = mapped_column(Text, nullable=True)
    # QR code (TLV encoded, Base64)
    qr_code_b64: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    # Clearance/Reporting
    zatca_status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    # draft | pending_clearance | cleared | reported | rejected | error
    zatca_response: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    zatca_cleared_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (Index("ix_zatca_tenant_status", "tenant_id", "zatca_status"),)


# ── Session Management ─────────────────────────────────────────────

class RefreshTokenRecord(Base):
    """
    JWT refresh token — one row per active session.
    Each user can have multiple sessions (different devices/browsers).
    Token value is hashed (SHA-256) for DB storage — never persisted in plaintext.
    رمز تحديث JWT — صف واحد لكل جلسة نشطة.
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    tenant_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    device_info: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    __table_args__ = (Index("ix_refresh_user_expires", "user_id", "expires_at"),)


class UserInviteRecord(Base):
    """
    Pending user invitations — token-based invite flow.
    An invite is single-use and has a TTL (default 72 h).
    دعوات المستخدمين المعلقة — تدفق الدعوة المستند إلى الرمز.
    """

    __tablename__ = "user_invites"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    role_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    invited_by: Mapped[str] = mapped_column(String(64), index=True)  # user_id of sender
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(index=True)
    accepted_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_invite_tenant_email"),
    )


# ── PDPL Consent Request (Art. 5) ─────────────────────────────────

class ConsentRequestRecord(Base):
    """
    Tracks PDPL consent request dispatches (email + WhatsApp).
    سجل إرسال طلبات الموافقة وفق المادة الخامسة من نظام PDPL.

    One record per (contact_id × channel × purpose) dispatch.
    Enables audit of when consent was requested and via which channel.
    """

    __tablename__ = "consent_requests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    contact_id: Mapped[str] = mapped_column(String(64), index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)   # email | whatsapp | sms
    purpose: Mapped[str] = mapped_column(String(64), index=True)   # PDPL_PURPOSES constant
    status: Mapped[str] = mapped_column(String(32), default="sent", index=True)
    # sent | delivered | responded_grant | responded_revoke | expired
    consent_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    locale: Mapped[str] = mapped_column(String(8), default="ar")
    responded_at: Mapped[datetime | None] = mapped_column(nullable=True)
    response_kind: Mapped[str | None] = mapped_column(String(16), nullable=True)  # grant | revoke
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_consent_requests_contact_channel", "contact_id", "channel", "purpose"),
    )


class PaymentRecord(Base):
    """
    Payment events from Moyasar — source of truth for reconciliation + audit.
    سجل المدفوعات — مرجع المطابقة والتدقيق.

    Populated by api.routers.pricing.moyasar_webhook on signature-verified events.
    Used by scripts/reconcile_moyasar.py to detect drift vs Moyasar's view.

    Idempotent on (provider, provider_payment_id).
    Append-mostly: status transitions update an existing row; no row is deleted.
    """

    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(
        ForeignKey("tenants.id"), nullable=True, index=True
    )
    provider: Mapped[str] = mapped_column(String(32), default="moyasar", index=True)
    provider_payment_id: Mapped[str] = mapped_column(String(128), index=True)
    plan: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    amount_halalas: Mapped[int] = mapped_column(Integer, default=0)
    currency: Mapped[str] = mapped_column(String(8), default="SAR")
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    # pending | authorized | captured | paid | failed | refunded | voided
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    customer_handle: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    last_event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    last_event_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    raw_event: Mapped[dict] = mapped_column(JSON, default=dict)
    error_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint("provider", "provider_payment_id", name="uq_payments_provider_id"),
        Index("ix_payments_status_created_at", "status", "created_at"),
    )


class SectorReportRecord(Base):
    """
    Generated Sector Intelligence Reports — R4 monetization (W8.2).

    Each row captures one generation of a sector report. The full
    payload is stored as JSON; lookups happen by report_id (the
    deterministic sha256-based ID from sector_intel router).
    """

    __tablename__ = "sector_reports"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # sr_<hash>
    sector: Mapped[str] = mapped_column(String(64), index=True)
    customer_handle: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    price_sar: Mapped[int] = mapped_column(Integer)
    period_start: Mapped[str | None] = mapped_column(String(32), nullable=True)
    period_end: Mapped[str | None] = mapped_column(String(32), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON)  # the full report dict
    payment_status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    delivered_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_sector_reports_sector_created", "sector", "created_at"),
    )


class CustomerWebhookSubscription(Base):
    """
    Customer-side webhook subscriptions — Dealix pings customers when events
    happen in their tenant (W12.1).

    Each row = one HTTPS endpoint a customer wants Dealix to call. Customer
    can subscribe to a subset of event types via the `event_types` JSON list.

    Examples of events Dealix will emit:
      lead.created, lead.replied, lead.demo_booked,
      payment.received, decision_passport.entry_added,
      tenant.usage.over_cap, tenant.health.score_changed
    """

    __tablename__ = "customer_webhook_subscriptions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # cwh_<hash>
    tenant_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    url: Mapped[str] = mapped_column(String(2048))  # must be HTTPS
    secret: Mapped[str] = mapped_column(String(128))  # HMAC signing key
    event_types: Mapped[list] = mapped_column(JSON)  # list[str] of subscribed events
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    last_delivery_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_delivery_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_cwh_tenant_active", "tenant_id", "is_active"),
    )


class CustomerWebhookDelivery(Base):
    """
    Webhook delivery attempts — audit trail of every event delivery.
    Used for: at-least-once semantics, idempotency, debugging customer
    integration failures.
    """

    __tablename__ = "customer_webhook_deliveries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # del_<hash>
    subscription_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("customer_webhook_subscriptions.id", ondelete="CASCADE"),
        index=True,
    )
    event_id: Mapped[str] = mapped_column(String(128), index=True)  # idempotency key
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    delivered_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    response_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_body_preview: Mapped[str | None] = mapped_column(String(500), nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("subscription_id", "event_id",
                         name="uq_webhook_subscription_event"),
        Index("ix_cwd_event_type_created", "event_type", "delivered_at"),
    )
