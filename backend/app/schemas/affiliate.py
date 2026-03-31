"""Dealix - Affiliate Schemas"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class AffiliateProfileUpdate(BaseModel):
    bio: Optional[str] = None
    website: Optional[str] = None
    social_links: Optional[dict] = None
    niche: Optional[str] = None
    bank_name: Optional[str] = None
    iban: Optional[str] = None
    paypal_email: Optional[str] = None


class AffiliateProfileResponse(BaseModel):
    id: int
    user_id: int
    bio: Optional[str]
    website: Optional[str]
    niche: Optional[str]
    audience_size: int
    status: str
    base_commission_rate: float
    tier_level: int
    total_earnings: float
    total_clicks: int
    total_conversions: int
    created_at: datetime

    class Config:
        from_attributes = True


class AffiliateLinkCreate(BaseModel):
    deal_id: int
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None


class AffiliateLinkResponse(BaseModel):
    id: int
    slug: str
    deal_id: int
    click_count: int
    conversion_count: int
    earnings: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AffiliateDashboardResponse(BaseModel):
    total_earnings: float
    total_clicks: int
    total_conversions: int
    conversion_rate: float
    active_links: int
    recent_clicks: List[dict]
    top_deals: List[dict]
    monthly_earnings: List[dict]


class PayoutRequest(BaseModel):
    amount: float = Field(gt=0)
    payment_method: str = "bank_transfer"
