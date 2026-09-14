from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "scripts" / "ops"


def _load(name: str):
    path = OPS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


policy = _load("model_cost_policy")
broker = _load("go_resource_broker")
free_broker = _load("opencode_model_broker")


def test_cost_policy_requires_explicit_free_suffix_or_included_go_namespace() -> None:
    assert policy.is_explicit_free_model("opencode/deepseek-v4-flash-free") is True
    assert policy.is_explicit_free_model("opencode/deepseek-v4-flash") is False
    assert policy.is_included_opencode_go_model("opencode-go/deepseek-v4.1-flash") is True
    assert policy.is_included_opencode_go_model("opencode/deepseek-v4.1-flash") is False
    assert policy.is_auto_selectable_model("opencode/paid-x") is False
    assert policy.is_deepseek_model("opencode-go/deepseek-v4.1-flash") is True
    assert policy.is_deepseek_model("opencode/nemotron-3-ultra-free") is False
    assert policy.is_auto_selectable_model("opencode/deepseek-v4-flash-free") is False
    assert policy.is_auto_selectable_model("opencode-go/deepseek-v4-pro") is False


def test_free_selector_never_contains_unproven_or_included_subscription_models() -> None:
    availability = {
        "models": [
            "opencode/nemotron-3-ultra-free",
            "opencode/paid-x",
            "opencode-go/glm-5.3",
        ],
        "free_models": ["opencode/nemotron-3-ultra-free"],
    }
    assert free_broker.candidate_order(availability, "opencode/paid-x") == [
        "opencode/nemotron-3-ultra-free"
    ]


def test_free_selector_never_contains_deepseek_models() -> None:
    availability = {
        "models": [
            "opencode/deepseek-v4-flash-free",
            "opencode/nemotron-3-ultra-free",
        ],
        "free_models": ["opencode/deepseek-v4-flash-free"],
    }
    assert free_broker.candidate_order(availability, "opencode/paid-x") == [
        "opencode/nemotron-3-ultra-free"
    ]


def test_r4_never_falls_back_to_arbitrary_catalog_model() -> None:
    catalog = ["opencode/paid-a", "vendor/unknown-model"]
    assert broker.pick_model("R4_INCLUDED_HIGH", catalog, [], []) == policy.UNKNOWN_INCLUDED_HIGH


def test_r5_never_falls_back_to_arbitrary_catalog_model() -> None:
    catalog = ["opencode/paid-a", "vendor/unknown-model"]
    assert broker.pick_model("R5_STRONG_REASONING", catalog, [], []) == policy.UNKNOWN_INCLUDED_STRONG


def test_r3_does_not_use_unclassified_router_model_as_included_fallback() -> None:
    assert broker.pick_model("R3_INCLUDED_LIGHT", [], [], ["router/unknown-cost"]) == policy.UNKNOWN_INCLUDED_LIGHT


def test_r4_uses_included_non_deepseek_only_with_verified_use_balance_disabled(monkeypatch) -> None:
    # Included-Go routing requires live provider cost authority (balance-off
    # verified); the explicit provider_state argument alone cannot mint it.
    # Canonical unattended law is NO_DEEPSEEK in all cases.
    monkeypatch.setenv("DEALIX_OPENCODE_GO_USE_BALANCE", "disabled")
    monkeypatch.setenv("DEALIX_OPENCODE_GO_COST_AUTHORITY_REF", "test_verified_disabled")
    catalog = [
        "opencode/paid-a",
        "opencode/nemotron-3-ultra-free",
        "opencode/deepseek-v4-flash-free",
        "opencode-go/glm-5.3",
        "opencode-go/deepseek-v4.1-flash",
    ]
    assert broker.pick_model(
        "R4_INCLUDED_HIGH", catalog, [], [], broker.GO_COST_VERIFIED_DISABLED
    ) == "opencode-go/glm-5.3"
    assert broker.pick_model(
        "R4_INCLUDED_HIGH", catalog, [], [], broker.GO_COST_UNKNOWN
    ) == "opencode/nemotron-3-ultra-free"
    assert broker.pick_model(
        "R4_INCLUDED_HIGH", ["opencode/deepseek-v4-flash-free"], [], []
    ) == policy.UNKNOWN_INCLUDED_HIGH


def test_r6_remains_explicit_paid_pending_approval() -> None:
    assert broker.pick_model("R6_PAID_EXCEPTION", ["opencode/paid-a"], [], []) == policy.PAID_PENDING_APPROVAL
