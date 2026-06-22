from __future__ import annotations

from .schemas import RiskLevel, SourceDefinition


SOURCE_REGISTRY: dict[str, SourceDefinition] = {
    "manual_warm_network": SourceDefinition(source_name="manual_warm_network", allowed_use="warm_manual_only", consent_requirement="contextual", risk_level=RiskLevel.low, retention_policy="customer_defined", can_auto_ingest=False, can_contact=True, provenance_required=True),
    "customer_uploaded_csv": SourceDefinition(source_name="customer_uploaded_csv", allowed_use="customer_authorized", consent_requirement="customer_attested", risk_level=RiskLevel.medium, retention_policy="customer_defined", can_auto_ingest=True, can_contact=True, provenance_required=True),
    "customer_crm_import": SourceDefinition(source_name="customer_crm_import", allowed_use="customer_authorized", consent_requirement="customer_attested", risk_level=RiskLevel.medium, retention_policy="customer_defined", can_auto_ingest=True, can_contact=True, provenance_required=True),
    "google_places_if_configured": SourceDefinition(source_name="google_places_if_configured", allowed_use="business_listing_only", consent_requirement="legitimate_interest_review", risk_level=RiskLevel.medium, retention_policy="90_days_review", can_auto_ingest=True, can_contact=False, provenance_required=True),
    "website_form": SourceDefinition(source_name="website_form", allowed_use="inbound_request", consent_requirement="inbound", risk_level=RiskLevel.low, retention_policy="customer_defined", can_auto_ingest=True, can_contact=True, provenance_required=True),
    "inbound_whatsapp": SourceDefinition(source_name="inbound_whatsapp", allowed_use="inbound_request", consent_requirement="inbound", risk_level=RiskLevel.low, retention_policy="customer_defined", can_auto_ingest=True, can_contact=True, provenance_required=True),
    "inbound_email": SourceDefinition(source_name="inbound_email", allowed_use="inbound_request", consent_requirement="inbound", risk_level=RiskLevel.low, retention_policy="customer_defined", can_auto_ingest=True, can_contact=True, provenance_required=True),
    "partner_referral": SourceDefinition(source_name="partner_referral", allowed_use="partner_referred", consent_requirement="partner_attested", risk_level=RiskLevel.medium, retention_policy="180_days_review", can_auto_ingest=False, can_contact=True, provenance_required=True),
    "public_directory_allowed": SourceDefinition(source_name="public_directory_allowed", allowed_use="directory_review_only", consent_requirement="legitimate_interest_review", risk_level=RiskLevel.medium, retention_policy="30_days_review", can_auto_ingest=False, can_contact=False, provenance_required=True),
    "paid_vendor_allowed_after_review": SourceDefinition(source_name="paid_vendor_allowed_after_review", allowed_use="approval_required", consent_requirement="vendor_review", risk_level=RiskLevel.high, retention_policy="contract_defined", can_auto_ingest=False, can_contact=False, provenance_required=True),
    "linkedin_manual_research_only": SourceDefinition(source_name="linkedin_manual_research_only", allowed_use="manual_research_only", consent_requirement="manual_review", risk_level=RiskLevel.medium, retention_policy="30_days_review", can_auto_ingest=False, can_contact=False, provenance_required=True),
    "blocked_scraping_source": SourceDefinition(source_name="blocked_scraping_source", allowed_use="blocked", consent_requirement="blocked", risk_level=RiskLevel.blocked, retention_policy="do_not_store", can_auto_ingest=False, can_contact=False, provenance_required=True),
}


def get_source_definition(source_name: str) -> SourceDefinition:
    return SOURCE_REGISTRY.get(source_name, SOURCE_REGISTRY["blocked_scraping_source"])