from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LoginReq(BaseModel):
    email: str
    password: str

class AffiliateApplyReq(BaseModel):
    full_name: str
    full_name_ar: Optional[str] = None
    email: str
    phone: str
    city: str
    arabic_level: str = "FLUENT"
    english_level: str = "BASIC"
    prior_experience: Optional[str] = None
    preferred_channels: List[str] = []
    can_do_calls: bool = False
    can_do_whatsapp: bool = True
    can_do_field: bool = False
    ksa_work_status: Optional[str] = None
    referral_source: Optional[str] = None
    motivation: Optional[str] = None
    sector_comfort: List[str] = []

class LeadCreateReq(BaseModel):
    company_name: str
    company_name_ar: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_whatsapp: Optional[str] = None
    contact_email: Optional[str] = None
    contact_role: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None
    sector: Optional[str] = None
    company_size: Optional[str] = None
    source: str = "OTHER"
    affiliate_id: Optional[int] = None
    notes: Optional[str] = None
    tags: List[str] = []

class MeetingCreateReq(BaseModel):
    lead_id: int
    meeting_type: str = "CALL"
    scheduled_at: datetime
    meeting_link: Optional[str] = None
    location: Optional[str] = None
    assigned_to_name: Optional[str] = None

class DealCreateReq(BaseModel):
    lead_id: int
    deal_name: str
    value: float = 0
    service_type: Optional[str] = None
    primary_attribution: Optional[str] = None
    primary_attribution_id: Optional[int] = None
