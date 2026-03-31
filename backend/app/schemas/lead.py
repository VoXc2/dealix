"""Dealix - Lead Schemas"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class LeadCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    source: str = "other"
    notes: Optional[str] = None
    estimated_value: float = Field(ge=0, default=0)
    assigned_to: Optional[int] = None


class LeadUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None
    score: Optional[str] = None
    notes: Optional[str] = None
    estimated_value: Optional[float] = None
    assigned_to: Optional[int] = None
    is_active: Optional[bool] = None


class LeadResponse(BaseModel):
    id: int
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    job_title: Optional[str]
    source: str
    status: str
    score: str
    score_value: int
    notes: Optional[str]
    estimated_value: float
    assigned_to: Optional[int]
    organization_id: Optional[int]
    converted_deal_id: Optional[int]
    last_contacted_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    items: List[LeadResponse]
    total: int
    page: int
    per_page: int
    pages: int
