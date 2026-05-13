"""Partner Portal — typed catalog of portal sections (later in launch sequence)."""

from __future__ import annotations

from enum import Enum


class PartnerPortalSection(str, Enum):
    LEADS = "leads"
    CERTIFICATION_STATUS = "certification_status"
    APPROVED_MATERIALS = "approved_materials"
    PROOF_TEMPLATES = "proof_templates"
    QA_SUBMISSIONS = "qa_submissions"
    COMMISSION_STATUS = "commission_status"


PARTNER_PORTAL_SECTIONS: tuple[PartnerPortalSection, ...] = tuple(PartnerPortalSection)
