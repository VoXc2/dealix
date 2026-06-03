"""Hermes tools — standalone async tool functions grouped by domain."""

from __future__ import annotations

from dealix.hermes.tools.analysis_tools import (
    analyze_revenue_trend,
    calculate_ltv_cac,
    generate_cohort_analysis,
    generate_executive_summary,
    identify_growth_levers,
)
from dealix.hermes.tools.crm_tools import (
    create_deal,
    get_lead_profile,
    list_open_deals,
    log_activity,
    update_lead_stage,
)
from dealix.hermes.tools.data_tools import (
    calculate_tam_sam_som,
    detect_duplicates,
    enrich_company_data,
    generate_data_passport,
    score_data_quality,
)
from dealix.hermes.tools.saudi_tools import (
    classify_vat_treatment,
    format_arabic_proposal,
    get_hijri_date,
    get_saudi_market_context,
    validate_cr_number,
)
from dealix.hermes.tools.commercial_tools import (
    build_commercial_proof_pack,
    check_commercial_upsell,
    get_commercial_market_intel,
    run_commercial_diagnostic,
    run_commercial_sprint,
)
from dealix.hermes.tools.scoring_tools import (
    calculate_deal_probability,
    prioritize_leads,
    score_account_health,
    score_lead,
)

__all__ = [
    # crm_tools
    "get_lead_profile",
    "update_lead_stage",
    "create_deal",
    "list_open_deals",
    "log_activity",
    # data_tools
    "score_data_quality",
    "detect_duplicates",
    "enrich_company_data",
    "calculate_tam_sam_som",
    "generate_data_passport",
    # scoring_tools
    "score_lead",
    "score_account_health",
    "prioritize_leads",
    "calculate_deal_probability",
    # analysis_tools
    "analyze_revenue_trend",
    "generate_cohort_analysis",
    "calculate_ltv_cac",
    "generate_executive_summary",
    "identify_growth_levers",
    # saudi_tools
    "validate_cr_number",
    "get_hijri_date",
    "classify_vat_treatment",
    "get_saudi_market_context",
    "format_arabic_proposal",
    # commercial_tools
    "run_commercial_diagnostic",
    "run_commercial_sprint",
    "build_commercial_proof_pack",
    "check_commercial_upsell",
    "get_commercial_market_intel",
]
