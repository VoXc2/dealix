"""LLM Gateway v10 — routing + budget tests (Phase B v10)."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.llm_gateway_v10 import (
    BudgetPolicy,
    CostEstimate,
    ModelTier,
    RoutingPolicy,
    enforce_budget,
    estimate_cost,
    route,
)
from auto_client_acquisition.llm_gateway_v10.cache_policy import cache_key
from auto_client_acquisition.llm_gateway_v10.fallback_policy import fallback_chain
from auto_client_acquisition.llm_gateway_v10.run_summary import summarize_run
from auto_client_acquisition.llm_gateway_v10.token_estimator import estimate_tokens


def _client() -> TestClient:
    return TestClient(create_app())


def test_model_tier_enum_has_four_values():
    values = {t.value for t in ModelTier}
    assert values == {
        "cheap_for_classification",
        "balanced_for_drafts",
        "strong_for_strategy",
        "local_no_model",
    }


def test_route_classification_maps_to_cheap_tier():
    req = RoutingPolicy(task_purpose="lead classification", language="en")
    decision = route(req)
    assert decision.tier == ModelTier.cheap_for_classification
    assert decision.reason_ar
    assert decision.reason_en


def test_route_strategy_maps_to_strong_tier():
    req = RoutingPolicy(task_purpose="weekly strategy review", language="bilingual")
    decision = route(req)
    assert decision.tier == ModelTier.strong_for_strategy


def test_route_draft_maps_to_balanced_tier():
    req = RoutingPolicy(task_purpose="draft Arabic follow-up", language="ar")
    decision = route(req)
    assert decision.tier == ModelTier.balanced_for_drafts


def test_route_lookup_maps_to_local_no_model():
    req = RoutingPolicy(task_purpose="deterministic lookup", language="en")
    decision = route(req)
    assert decision.tier == ModelTier.local_no_model


def test_estimate_cost_is_bounded_and_positive_for_strong_tier():
    req = RoutingPolicy(task_purpose="strategy audit", language="en")
    est = estimate_cost(req)
    assert est.tier == ModelTier.strong_for_strategy
    assert est.estimated_usd >= 0.0
    assert est.estimated_usd <= 0.40  # ceiling


def test_enforce_budget_over_per_run_returns_hard_stop():
    estimates = [
        CostEstimate(
            tier=ModelTier.strong_for_strategy,
            estimated_input_tokens=100,
            estimated_output_tokens=100,
            estimated_usd=0.30,
        ),
        CostEstimate(
            tier=ModelTier.strong_for_strategy,
            estimated_input_tokens=100,
            estimated_output_tokens=100,
            estimated_usd=0.30,
        ),
    ]
    policy = BudgetPolicy(per_run_budget_usd=0.50)
    result = enforce_budget(estimates, policy)
    assert result["action"] == "hard_stop"
    assert result["within_budget"] is False
    assert result["breached"] == "per_run"


def test_enforce_budget_within_returns_proceed():
    estimates = [
        CostEstimate(
            tier=ModelTier.cheap_for_classification,
            estimated_input_tokens=100,
            estimated_output_tokens=50,
            estimated_usd=0.001,
        )
    ]
    policy = BudgetPolicy()
    result = enforce_budget(estimates, policy)
    assert result["action"] == "proceed"
    assert result["within_budget"] is True
    assert result["breached"] is None


def test_cache_key_is_deterministic_for_identical_inputs():
    a = RoutingPolicy(task_purpose="qualification", language="ar", customer_handle="cust_42")
    b = RoutingPolicy(task_purpose="qualification", language="ar", customer_handle="cust_42")
    assert cache_key(a) == cache_key(b)
    # sha256 hex is 64 chars
    assert len(cache_key(a)) == 64


def test_cache_key_differs_for_different_inputs():
    a = RoutingPolicy(task_purpose="qualification", language="ar")
    b = RoutingPolicy(task_purpose="strategy", language="ar")
    c = RoutingPolicy(task_purpose="qualification", language="en")
    assert cache_key(a) != cache_key(b)
    assert cache_key(a) != cache_key(c)


def test_fallback_chain_strong_includes_all_four_tiers_in_order():
    chain = fallback_chain(ModelTier.strong_for_strategy)
    assert chain == [
        ModelTier.strong_for_strategy,
        ModelTier.balanced_for_drafts,
        ModelTier.cheap_for_classification,
        ModelTier.local_no_model,
    ]


def test_fallback_chain_balanced_skips_strong():
    chain = fallback_chain(ModelTier.balanced_for_drafts)
    assert chain[0] == ModelTier.balanced_for_drafts
    assert ModelTier.strong_for_strategy not in chain


def test_token_estimator_handles_empty_and_non_string():
    assert estimate_tokens("") == 0
    assert estimate_tokens(None) == 0  # type: ignore[arg-type]
    assert estimate_tokens("hello world") > 0


def test_summarize_run_counts_and_totals():
    decisions = [
        route(RoutingPolicy(task_purpose="classification", language="en")),
        route(RoutingPolicy(task_purpose="strategy", language="en")),
        route(RoutingPolicy(task_purpose="draft", language="en")),
    ]
    summary = summarize_run(decisions)
    assert summary["decision_count"] == 3
    assert summary["total_usd"] >= 0.0
    assert sum(slot["count"] for slot in summary["per_tier"].values()) == 3


def test_router_post_route_with_valid_body_returns_200():
    resp = _client().post(
        "/api/v1/llm-gateway-v10/route",
        json={"task_purpose": "lead qualification", "language": "ar"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["tier"] == "cheap_for_classification"
    assert "reason_ar" in body
    assert "reason_en" in body


def test_router_post_route_with_empty_task_purpose_returns_422():
    resp = _client().post(
        "/api/v1/llm-gateway-v10/route",
        json={"task_purpose": "", "language": "ar"},
    )
    assert resp.status_code == 422


def test_router_post_route_with_extra_field_returns_422():
    resp = _client().post(
        "/api/v1/llm-gateway-v10/route",
        json={"task_purpose": "draft", "language": "en", "rogue": "x"},
    )
    assert resp.status_code == 422


def test_router_status_advertises_no_external_http():
    resp = _client().get("/api/v1/llm-gateway-v10/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "llm_gateway_v10"
    assert body["guardrails"]["no_external_http"] is True
    assert body["guardrails"]["no_llm_api_calls"] is True


def test_router_post_estimate_cost_returns_200():
    resp = _client().post(
        "/api/v1/llm-gateway-v10/estimate-cost",
        json={"task_purpose": "strategy plan", "language": "en"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["tier"] == "strong_for_strategy"
    assert body["estimated_usd"] >= 0.0


def test_router_post_enforce_budget_returns_action():
    resp = _client().post(
        "/api/v1/llm-gateway-v10/enforce-budget",
        json={
            "estimates": [
                {
                    "tier": "strong_for_strategy",
                    "estimated_input_tokens": 1000,
                    "estimated_output_tokens": 500,
                    "estimated_usd": 0.40,
                }
            ],
            "policy": {"per_run_budget_usd": 0.10},
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["action"] == "hard_stop"
    assert body["breached"] == "per_run"
