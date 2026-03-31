from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, JSON
from sqlalchemy.sql import func
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    hashed_password = Column(String(255))
    role = Column(String(50), default="VIEWER")
    is_active = Column(Boolean, default=True)
    phone = Column(String(50))
    city = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Affiliate(Base):
    __tablename__ = "affiliates"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    status = Column(String(50), default="APPLIED")
    affiliate_code = Column(String(50), unique=True, index=True)
    city = Column(String(100))
    arabic_level = Column(String(50))
    english_level = Column(String(50))
    preferred_channels = Column(JSON, default=list)
    can_do_calls = Column(Boolean, default=False)
    can_do_whatsapp = Column(Boolean, default=True)
    can_do_field = Column(Boolean, default=False)
    total_leads = Column(Integer, default=0)
    total_deals = Column(Integer, default=0)
    total_revenue = Column(Float, default=0)
    training_completed = Boolean, default=False)
    hire_eligible = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255))
    company_name_ar = Column(String(255))
    contact_name = Column(String(255))
    contact_phone = Column(String(50))
    contact_whatsapp = Column(String(50))
    contact_email = Column(String(255))
    contact_role = Column(String(100))
    website = Column(String(500))
    city = Column(String(100))
    sector = Column(String(100))
    company_size = Column(String(50))
    source = Column(String(50), default="OTHER")
    affiliate_id = Column(Integer, index=True)
    stage = Column(String(50), default="NEW", index=True)
    score = Column(Integer, default=0)
    owner_id = Column(Integer, index=True)
    notes = Column(Text)
    tags = Column(JSON, default=list)
    language_preference = Column(String(10), default="ar")
    consent_status = Column(String(50, default="NOT_REQUESTED")
    meeting_booked = Column(Boolean, default=False)
    deal_won = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True, onupdate=func.now())

class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, unique=True)
    deal_name = Column(String(255))
    stage = Column(String(50), default="PROPOSAL", index=True)
    status = Column(String(50), default="ACTIVE", index=True)
    value = Column(Float, default=0)
    currency = Column(String(10), default="SAR")
    service_type = Column(String(100))
    expected_close = Column(DateTime(timezone=True))
    actual_close = Column(DateTime(timezone=True))
    primary_attribution = Column(String(50))
    primary_attribution_id = Column(Integer)
    guarantee_offered = Column(Boolean, default=False)
    lost_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Commission(Base):
    __tablename__ = "commissions"
    id = Column(Integer, primary_key=True, index=True)
    affiliate_id = Column(Integer, index=True)
    deal_id = Column(Integer)
    lead_id = Column(Integer)
    status = Column(String(50), default="DRAFT", index=True)
    deal_value = Column(Float, default=0)
    commission_rate = Column(Float, default=0)
    commission_amount = Column(Float, default=0)
    currency = Column(String(10), default="SAR")
    payout_status = Column(String(50), default="PENDING")
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, unique=True)
    meeting_type = Column(String(50), default="CALL")
    status = Column(String(50), default="SCHEDULED", index=True)
    scheduled_at = Column(DateTime(timezone=True))
    meeting_link = Column(String(500))
    location = Column(String(255))
    assigned_to_id = Column(Integer)
    assigned_to_name = Column(String(255))
    outcome = Column(String(100))
    outcome_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    task_type = Column(String(50), default="OTHER")
    status = Column(String(50), default="PENDING", index=True)
    priority = Column(String(20), default="MEDIUM")
    assigned_to_id = Column(Integer, index=True)
    lead_id = Column(Integer)
    due_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    type = Column(String(50))
    title = Column(String(255))
    body = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    action = Column(String(50))
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    previous_data = Column(JSON)
    new_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GuaranteeClaim(Base):
    __tablename__ = "guarantee_claims"
    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, unique=True)
    claim_number = Column(String(50), unique=True)
    status = Column(String(50), default="SUBMITTED", index=True)
    claim_reason = Column(Text)
    claim_description = Column(Text)
    claim_evidence = Column(JSON, default=list)
    eligible = Column(Boolean)
    approved_amount = Column(Float)
    abuse_flag = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100))
    title = Column(String(255))
    title_ar = Column(String(255))
    content = Column(Text)
    content_ar = Column(Text)
    tags = Column(JSON, default=list)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
