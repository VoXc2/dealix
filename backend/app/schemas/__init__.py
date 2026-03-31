"""Dealix - All Schemas"""
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserLogin,
    TokenResponse, RefreshTokenRequest, PasswordChange,
    PasswordResetRequest, PasswordResetConfirm
)
from app.schemas.deal import (
    DealCreate, DealUpdate, DealResponse, DealListResponse,
    DealRedemptionCreate, DealRedemptionResponse
)
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadListResponse
from app.schemas.affiliate import (
    AffiliateProfileUpdate, AffiliateProfileResponse,
    AffiliateLinkCreate, AffiliateLinkResponse,
    AffiliateDashboardResponse, PayoutRequest
)
from app.schemas.meeting import (
    MeetingCreate, MeetingUpdate, MeetingResponse, MeetingListResponse
)
from app.schemas.dashboard import DashboardResponse, DashboardStats

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin",
    "TokenResponse", "RefreshTokenRequest", "PasswordChange",
    "PasswordResetRequest", "PasswordResetConfirm",
    "DealCreate", "DealUpdate", "DealResponse", "DealListResponse",
    "DealRedemptionCreate", "DealRedemptionResponse",
    "LeadCreate", "LeadUpdate", "LeadResponse", "LeadListResponse",
    "AffiliateProfileUpdate", "AffiliateProfileResponse",
    "AffiliateLinkCreate", "AffiliateLinkResponse",
    "AffiliateDashboardResponse", "PayoutRequest",
    "MeetingCreate", "MeetingUpdate", "MeetingResponse", "MeetingListResponse",
    "DashboardResponse", "DashboardStats",
]
