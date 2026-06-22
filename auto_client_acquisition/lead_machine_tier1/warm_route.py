from __future__ import annotations

from .schemas import ComplianceDecision, LeadCompany, WarmRouteDecision, WarmRouteType


def choose_warm_route(lead: LeadCompany, compliance: ComplianceDecision, inbound_whatsapp: bool = False, consented_whatsapp: bool = False) -> WarmRouteDecision:
    if not compliance.allowed:
        return WarmRouteDecision(route=WarmRouteType.email_draft, allowed=False, reason="compliance_blocked")
    metadata = lead.metadata
    if metadata.get("founder_intro"):
        return WarmRouteDecision(route=WarmRouteType.founder_intro, allowed=True, reason="founder_intro_available")
    if metadata.get("partner_intro"):
        return WarmRouteDecision(route=WarmRouteType.partner_intro, allowed=True, reason="partner_intro_available")
    if metadata.get("customer_referral"):
        return WarmRouteDecision(route=WarmRouteType.customer_referral, allowed=True, reason="customer_referral_available")
    if metadata.get("inbound_reply"):
        return WarmRouteDecision(route=WarmRouteType.inbound_reply, allowed=True, reason="inbound_reply_available")
    if inbound_whatsapp or consented_whatsapp:
        return WarmRouteDecision(route=WarmRouteType.whatsapp_inbound_only, allowed=True, reason="whatsapp_inbound_or_consented")
    if lead.phone:
        return WarmRouteDecision(route=WarmRouteType.phone_script, allowed=True, reason="phone_available_manual_only")
    if metadata.get("linkedin_profile"):
        return WarmRouteDecision(route=WarmRouteType.linkedin_manual, allowed=True, reason="linkedin_manual_only")
    return WarmRouteDecision(route=WarmRouteType.email_draft, allowed=True, reason="default_email_draft")