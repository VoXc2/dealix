"""Hermes tools — standalone async tool functions grouped by domain."""

from __future__ import annotations

from dealix.hermes.tools.analysis_tools import (
    analyze_revenue_trend,
    calculate_ltv_cac,
    generate_cohort_analysis,
    generate_executive_summary,
    identify_growth_levers,
)
from dealix.hermes.tools.commercial_tools import (
    build_commercial_proof_pack,
    check_commercial_upsell,
    get_commercial_market_intel,
    run_commercial_diagnostic,
    run_commercial_sprint,
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
from dealix.hermes.tools.scoring_tools import (
    calculate_deal_probability,
    prioritize_leads,
    score_account_health,
    score_lead,
)

__all__ = [
    # analysis_tools
    "analyze_revenue_trend",
    "build_commercial_proof_pack",
    "calculate_deal_probability",
    "calculate_ltv_cac",
    "calculate_tam_sam_som",
    "check_commercial_upsell",
    "classify_vat_treatment",
    "create_deal",
    "detect_duplicates",
    "enrich_company_data",
    "format_arabic_proposal",
    "generate_cohort_analysis",
    "generate_data_passport",
    "generate_executive_summary",
    "get_commercial_market_intel",
    "get_hijri_date",
    # crm_tools
    "get_lead_profile",
    "get_saudi_market_context",
    "identify_growth_levers",
    "list_open_deals",
    "log_activity",
    "prioritize_leads",
    # commercial_tools
    "run_commercial_diagnostic",
    "run_commercial_sprint",
    "score_account_health",
    # data_tools
    "score_data_quality",
    # scoring_tools
    "score_lead",
    "update_lead_stage",
    # saudi_tools
    "validate_cr_number",
]
