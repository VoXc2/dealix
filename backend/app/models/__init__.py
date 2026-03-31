"""Dealix - All Models"""
from app.models.user import User, UserRole, UserStatus
from app.models.organization import Organization, OrganizationMember, OrgType, OrgStatus
from app.models.deal import Deal, DealRedemption, DealStage, DealType
from app.models.lead import Lead, LeadSource, LeadStatus, LeadScore
from app.models.affiliate import (
    AffiliateProfile, AffiliateLink, AffiliateClick,
    AffiliatePayout, CommissionTier, AffiliateStatus, PayoutStatus
)
from app.models.merchant import Merchant, MerchantStatus
from app.models.meeting import Meeting, MeetingStatus, MeetingType
from app.models.activity import Activity, ActivityType
from app.models.notification import Notification, NotificationType, NotificationChannel
from app.models.api_key import APIKey
from app.models.app_settings import AppSetting

__all__ = [
    "User", "UserRole", "UserStatus",
    "Organization", "OrganizationMember", "OrgType", "OrgStatus",
    "Deal", "DealRedemption", "DealStage", "DealType",
    "Lead", "LeadSource", "LeadStatus", "LeadScore",
    "AffiliateProfile", "AffiliateLink", "AffiliateClick",
    "AffiliatePayout", "CommissionTier", "AffiliateStatus", "PayoutStatus",
    "Merchant", "MerchantStatus",
    "Meeting", "MeetingStatus", "MeetingType",
    "Activity", "ActivityType",
    "Notification", "NotificationType", "NotificationChannel",
    "APIKey", "AppSetting",
]
