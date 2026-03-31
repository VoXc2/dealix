"""Dealix - Deal Schemas"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class DealCreate(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    title_en: Optional[str] = None
    description: Optional[str] = None
    terms_conditions: Optional[str] = None
    image_url: Optional[str] = None
    deal_type: str = "standard"
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    original_price: float = Field(ge=0)
    deal_price: float = Field(ge=0)
    discount_percentage: float = Field(ge=0, le=100)
    commission_amount: float = Field(ge=0)
    commission_type: str = "percentage"
    currency: str = "SAR"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_redemptions: Optional[int] = None
    min_order_value: float = Field(ge=0, default=0)
    is_featured: bool = False
    merchant_contact_id: Optional[int] = None


class DealUpdate(BaseModel):
    title: Optional[str] = None
    title_en: Optional[str] = None
    description: Optional[str] = None
    terms_conditions: Optional[str] = None
    image_url: Optional[str] = None
    deal_type: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    original_price: Optional[float] = None
    deal_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    commission_amount: Optional[float] = None
    commission_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_redemptions: Optional[int] = None
    min_order_value: Optional[float] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    stage: Optional[str] = None
    priority: Optional[int] = None


class DealResponse(BaseModel):
    id: int
    title: str
    title_en: Optional[str]
    slug: str
    description: Optional[str]
    deal_type: str
    stage: str
    category: Optional[str]
    tags: Optional[str]
    original_price: float
    deal_price: float
    discount_percentage: float
    commission_amount: float
    commission_type: str
    currency: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    published_at: Optional[datetime]
    closed_at: Optional[datetime]
    max_redemptions: Optional[int]
    current_redemptions: int
    view_count: int
    click_count: int
    share_count: int
    conversion_rate: float
    is_active: bool
    is_featured: bool
    is_verified: bool
    priority: int
    organization_id: int
    assigned_to: Optional[int]
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DealListResponse(BaseModel):
    items: List[DealResponse]
    total: int
    page: int
    per_page: int
    pages: int


class DealRedemptionCreate(BaseModel):
    deal_id: int
    affiliate_link_id: Optional[int] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    amount: float = Field(ge=0)


class DealRedemptionResponse(BaseModel):
    id: int
    deal_id: int
    customer_name: Optional[str]
    amount: float
    commission_earned: float
    status: str
    redemption_code: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
