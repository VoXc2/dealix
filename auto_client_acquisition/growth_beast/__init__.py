"""V12.5 Beast — Growth Beast (Dealix's own self-growth engine).

Safe-by-design: all outputs are ``suggest_only`` or ``draft_only``.
NO scraping (signal sources are caller-supplied placeholders).
NO automated outbound. NO LinkedIn automation. NO cold WhatsApp.
"""
from auto_client_acquisition.growth_beast.account_ranker import rank_accounts
from auto_client_acquisition.growth_beast.content_engine import draft_content
from auto_client_acquisition.growth_beast.experiment_engine import next_experiment
from auto_client_acquisition.growth_beast.icp_score import compute_icp_score
from auto_client_acquisition.growth_beast.market_radar import (
    MarketSignal,
    SignalSource,
    SignalType,
    evaluate_signals,
)
from auto_client_acquisition.growth_beast.offer_intelligence import match_offer
from auto_client_acquisition.growth_beast.proof_to_content import (
    proof_to_content_idea,
)
from auto_client_acquisition.growth_beast.warm_route import draft_warm_route
from auto_client_acquisition.growth_beast.weekly_learning import weekly_summary

__all__ = [
    "MarketSignal",
    "SignalSource",
    "SignalType",
    "compute_icp_score",
    "draft_content",
    "draft_warm_route",
    "evaluate_signals",
    "match_offer",
    "next_experiment",
    "proof_to_content_idea",
    "rank_accounts",
    "weekly_summary",
]
