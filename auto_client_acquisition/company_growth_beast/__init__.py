"""V12.5 Company Growth Beast — sells the same self-growth engine
to client companies. Same hard gates as Growth Beast: draft_only,
no scraping, no live action, no fake proof."""
from auto_client_acquisition.company_growth_beast.engine import (
    CompanyProfile,
    build_company_profile,
    build_content_pack,
    build_growth_diagnostic,
    build_offer_recommendation,
    build_target_segments,
    build_weekly_report,
    support_to_growth_insight,
)

__all__ = [
    "CompanyProfile",
    "build_company_profile",
    "build_content_pack",
    "build_growth_diagnostic",
    "build_offer_recommendation",
    "build_target_segments",
    "build_weekly_report",
    "support_to_growth_insight",
]
