"""
Salla Data Models — Pydantic schemas for webhook payloads and API responses.
نماذج بيانات Salla — مخططات Pydantic لـ Webhooks وردود API.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class SallaMerchant(BaseModel):
    """بيانات التاجر من Salla."""

    id: int
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    plan: Optional[str] = None


class SallaTokens(BaseModel):
    """رموز OAuth للتاجر / OAuth tokens for a merchant."""

    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"
    scope: Optional[str] = None
    merchant_id: Optional[int] = None


class SallaOrderCustomer(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None


class SallaOrderTotal(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = "SAR"


class SallaOrder(BaseModel):
    id: Optional[int] = None
    reference_id: Optional[str] = None
    status: Optional[str] = None
    customer: Optional[SallaOrderCustomer] = None
    total: Optional[SallaOrderTotal] = None
    created_at: Optional[str] = None


class SallaWebhookEvent(BaseModel):
    """Salla webhook event envelope."""

    event: str
    merchant: Optional[int] = None
    created_at: Optional[str] = None
    data: Optional[dict] = None
