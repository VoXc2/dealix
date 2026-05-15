from __future__ import annotations

import json
from pathlib import Path

from saudi_ai_provider.commercial import load_intake
from saudi_ai_provider.monetization import (
    compute_proposal_scorecard,
    orchestrate_renewal_expansion,
    recommend_auto_package,
)


def test_proposal_scorecard_computes_recommendation() -> None:
    intake = load_intake(Path("intake/demo_customer_intake.json"))
    score = compute_proposal_scorecard("CUSTOMER_PORTAL_GOLD", intake)
    assert score.total_score > 60
    assert score.recommendation in {"GO", "GO_WITH_CONDITIONS"}


def test_auto_package_recommendation_returns_ranked_services() -> None:
    intake = load_intake(Path("intake/demo_customer_intake.json"))
    rec = recommend_auto_package(intake, max_services=4)
    assert rec.segment == "mid_market"
    assert len(rec.ranked_services) == 4
    assert rec.ranked_services[0]["fit_score"] >= rec.ranked_services[-1]["fit_score"]


def test_renewal_expansion_orchestrator_returns_actions() -> None:
    state = json.loads(Path("revenue/demo_customer_state.json").read_text(encoding="utf-8"))
    plan = orchestrate_renewal_expansion(state)
    assert plan.renewal_risk == "LOW"
    assert len(plan.renewal_actions) >= 2
