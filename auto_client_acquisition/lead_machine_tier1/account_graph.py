from __future__ import annotations

from .schemas import LeadCompany


def build_account_graph(lead: LeadCompany) -> dict[str, object]:
    return {
        "company_name": lead.company_name,
        "domain": lead.domain,
        "city": lead.city,
        "sector": lead.sector,
        "connected_nodes": {
            "crm_external_id": lead.crm_external_id,
            "google_place_id": lead.google_place_id,
            "website_url": lead.website_url,
        },
    }