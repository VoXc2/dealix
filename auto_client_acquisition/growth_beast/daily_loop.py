"""Compose the daily Growth Beast loop end-to-end (deterministic)."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_growth_beast.offer_matcher import match_offer
from auto_client_acquisition.company_growth_beast.target_segment_engine import (
    rank_target_segments,
)
from auto_client_acquisition.growth_beast.account_ranker import rank_accounts
from auto_client_acquisition.growth_beast.content_engine import suggest_content_angle
from auto_client_acquisition.growth_beast.experiment_engine import suggest_experiment
from auto_client_acquisition.growth_beast.icp_score import score_icp
from auto_client_acquisition.growth_beast.market_radar import synthetic_signals_today
from auto_client_acquisition.growth_beast.offer_intelligence import best_offer_hint
from auto_client_acquisition.growth_beast.warm_route import primary_warm_route


def build_daily_growth_beast_loop(company_profile: dict[str, Any]) -> dict[str, Any]:
    signals = synthetic_signals_today()
    icp = score_icp(company_profile)
    segments = rank_target_segments(company_profile)
    ranked = rank_accounts(segments, limit=10)
    top3 = ranked[:3]
    top_seg_dict = segments[0] if segments else {}
    top_label_ar = str(top_seg_dict.get("segment_name_ar") or "الهدف الأول")
    warm = primary_warm_route(int(top_seg_dict.get("fit_score") or icp["icp_score"]))
    offer_match = match_offer(company_profile, None)
    offer_hint = best_offer_hint(top3[0] if top3 else None)
    content = suggest_content_angle(top_label_ar)
    experiment = suggest_experiment(top_label_ar)

    return {
        "schema_version": 1,
        "experience_layer": "growth_beast_loop",
        "signals_today": signals,
        "icp": icp,
        "top_10_targets": ranked,
        "top_3_targets": top3,
        "best_offer": offer_hint,
        "offer_engine_match": offer_match,
        "best_content_angle": content,
        "safe_route": warm,
        "next_experiment": experiment,
        "approval_queue_ar": [
            "اعتماد أي مسودة محتوى",
            "اعتماد أي رسالة خارجية يدوية",
            "اعتماد أي إثبات علني",
        ],
        "hard_gates": {
            "no_cold_whatsapp": True,
            "no_linkedin_automation": True,
            "no_scraping": True,
            "no_live_send": True,
        },
    }
