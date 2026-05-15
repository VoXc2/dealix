"""Operating finance & capital allocation — deterministic spend discipline."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os.ai_cost_accounting import (
    ai_cost_per_proof_pack_usd,
    total_ai_run_cost_usd,
)
from auto_client_acquisition.operating_finance_os.bad_revenue_filter import (
    BadRevenueSignals,
    GoodRevenueSignals,
    good_revenue_green,
    is_bad_revenue,
)
from auto_client_acquisition.operating_finance_os.budget_stage import (
    OperatingBudgetStage,
    spend_allowed_for_stage,
)
from auto_client_acquisition.operating_finance_os.capital_allocation_score import (
    CapitalAllocationDimensions,
    capital_allocation_band,
    capital_allocation_score,
)
from auto_client_acquisition.operating_finance_os.capital_review import (
    CAPITAL_REVIEW_OUTPUT_KEYS,
    capital_review_outputs_complete,
)
from auto_client_acquisition.operating_finance_os.cost_guard import (
    ai_spend_ratio,
    cost_guard_breached,
)
from auto_client_acquisition.operating_finance_os.delivery_cost_accounting import delivery_cost_usd
from auto_client_acquisition.operating_finance_os.financial_metrics import (
    FINANCIAL_CONTROL_METRICS,
    financial_metrics_tracking_score,
)
from auto_client_acquisition.operating_finance_os.hiring_triggers import (
    HireFocus,
    recommended_hire_focus,
)
from auto_client_acquisition.operating_finance_os.investment_backlog import (
    INVESTMENT_BACKLOG_FIELDS,
    InvestmentBacklogEntry,
    investment_entry_complete,
)
from auto_client_acquisition.operating_finance_os.margin_by_offer import margin_percent_by_offer
from auto_client_acquisition.operating_finance_os.margin_protection import (
    MarginAction,
    margin_protection_action,
)
from auto_client_acquisition.operating_finance_os.model_cost_tracker import (
    estimate_run_cost_usd,
    usd_per_1k_tokens,
)
from auto_client_acquisition.operating_finance_os.offer_unit_economics import OfferUnitEconomics
from auto_client_acquisition.operating_finance_os.opportunity_cost import (
    opportunity_acceptance_ok,
)
from auto_client_acquisition.operating_finance_os.retainer_economics import RetainerEconomics

__all__ = (
    "CAPITAL_REVIEW_OUTPUT_KEYS",
    "FINANCIAL_CONTROL_METRICS",
    "INVESTMENT_BACKLOG_FIELDS",
    "BadRevenueSignals",
    "CapitalAllocationDimensions",
    "GoodRevenueSignals",
    "HireFocus",
    "InvestmentBacklogEntry",
    "MarginAction",
    "OfferUnitEconomics",
    "OperatingBudgetStage",
    "RetainerEconomics",
    "ai_cost_per_proof_pack_usd",
    "ai_spend_ratio",
    "capital_allocation_band",
    "capital_allocation_score",
    "capital_review_outputs_complete",
    "cost_guard_breached",
    "delivery_cost_usd",
    "estimate_run_cost_usd",
    "financial_metrics_tracking_score",
    "good_revenue_green",
    "investment_entry_complete",
    "is_bad_revenue",
    "margin_percent_by_offer",
    "margin_protection_action",
    "opportunity_acceptance_ok",
    "recommended_hire_focus",
    "spend_allowed_for_stage",
    "total_ai_run_cost_usd",
    "usd_per_1k_tokens",
)
