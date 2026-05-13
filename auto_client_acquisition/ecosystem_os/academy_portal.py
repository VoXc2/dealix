"""Academy Portal — typed catalog of academy tracks + portal sections."""

from __future__ import annotations

from enum import Enum


class AcademyTrack(str, Enum):
    AI_OPS_EXECUTIVE = "ai_ops_executive"
    REVENUE_AI_OPERATOR = "revenue_ai_operator"
    COMPANY_BRAIN_BUILDER = "company_brain_builder"
    AI_GOVERNANCE_LEAD = "ai_governance_lead"
    DEALIX_CERTIFIED_PARTNER = "dealix_certified_partner"
    DEALIX_DELIVERY_ANALYST = "dealix_delivery_analyst"


ACADEMY_TRACKS: tuple[AcademyTrack, ...] = tuple(AcademyTrack)


class AcademyPortalSection(str, Enum):
    COURSES = "courses"
    ASSESSMENTS = "assessments"
    CERTIFICATES = "certificates"
    TEMPLATES = "templates"
    PRACTICE_CASES = "practice_cases"


ACADEMY_PORTAL_SECTIONS: tuple[AcademyPortalSection, ...] = tuple(AcademyPortalSection)
