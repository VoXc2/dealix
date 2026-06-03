"""Canonical artefact-type enum for DesignOps.

Generators in a later phase fan out off this enum; the skill
registry and the design-system loader both reference it.
"""
from __future__ import annotations

from enum import StrEnum


class ArtifactType(StrEnum):
    """Every output Dealix can render."""

    MINI_DIAGNOSTIC = "mini_diagnostic"
    PROOF_PACK = "proof_pack"
    EXECUTIVE_WEEKLY_PACK = "executive_weekly_pack"
    PROPOSAL_PAGE = "proposal_page"
    PRICING_PAGE = "pricing_page"
    CUSTOMER_ROOM_DASHBOARD = "customer_room_dashboard"
    SERVICE_STATUS_CONSOLE = "service_status_console"
    PARTNERSHIP_ONE_PAGER = "partnership_one_pager"
    SALES_EMAIL_DRAFT = "sales_email_draft"
    LINKEDIN_WARM_INTRO_DRAFT = "linkedin_warm_intro_draft"
    SOCIAL_CAROUSEL = "social_carousel"
    INVESTOR_STYLE_DECK = "investor_style_deck"
    CUSTOMER_ONBOARDING_GUIDE = "customer_onboarding_guide"
    DELIVERY_WORKFLOW_REPORT = "delivery_workflow_report"
    INVOICE_BRIEF = "invoice_brief"
