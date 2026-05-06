"""Company Growth Beast — deterministic service wrapper over existing OS modules."""

from __future__ import annotations

from auto_client_acquisition.company_growth_beast.command_center import build_command_center
from auto_client_acquisition.company_growth_beast.company_profile import upsert_company_profile
from auto_client_acquisition.company_growth_beast.content_pack_builder import build_content_pack
from auto_client_acquisition.company_growth_beast.experiment_planner import plan_growth_experiment
from auto_client_acquisition.company_growth_beast.growth_diagnostic import build_growth_diagnostic
from auto_client_acquisition.company_growth_beast.offer_matcher import match_offer
from auto_client_acquisition.company_growth_beast.proof_loop import build_proof_loop
from auto_client_acquisition.company_growth_beast.support_to_growth import support_questions_to_insights
from auto_client_acquisition.company_growth_beast.target_segment_engine import rank_target_segments
from auto_client_acquisition.company_growth_beast.warm_route_builder import build_warm_route_pack
from auto_client_acquisition.company_growth_beast.weekly_report import build_weekly_growth_report

__all__ = [
    "build_command_center",
    "build_content_pack",
    "build_growth_diagnostic",
    "build_proof_loop",
    "build_warm_route_pack",
    "build_weekly_growth_report",
    "match_offer",
    "plan_growth_experiment",
    "rank_target_segments",
    "support_questions_to_insights",
    "upsert_company_profile",
]
