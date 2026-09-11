from __future__ import annotations

from core.llm.model_economics import (
    build_usage_event,
    estimate_budget_cost_usd,
    find_model,
    load_registry,
    production_allowed,
)


def test_registry_tracks_official_v41_flash_name_without_promoting_production() -> None:
    names={entry["model_name"] for entry in load_registry()}
    assert "deepseek-flash" in names
    entry=find_model("deepseek-flash")
    assert entry is not None
    assert entry["lifecycle"] == "stable"
    assert entry["status"] == "testing"
    assert entry["production_eligible"] is False
    assert production_allowed("deepseek-flash", on_date="2026-09-11") is False


def test_retired_v4_flash_and_vision_are_fail_closed() -> None:
    for name in ("deepseek-v4-flash", "deepseek-v4-flash-vision-exp"):
        entry=find_model(name)
        assert entry is not None
        assert entry["lifecycle"] == "expired"
        assert entry["production_eligible"] is False
        assert production_allowed(name, on_date="2026-09-11") is False


def test_v4_pro_is_held_before_announced_provider_reroute() -> None:
    entry=find_model("deepseek-v4-pro")
    assert entry is not None
    assert entry["production_eligible"] is False
    assert "2026-09-14" in entry["notes"]


def test_expired_v41_beta_is_never_production_eligible() -> None:
    name="deepseek-v4.1-flash-expires-on-0910"
    entry=find_model(name)
    assert entry is not None
    assert entry["lifecycle"] == "expired"
    assert entry["production_eligible"] is False
    assert entry["concurrency_limit"] == 20
    assert production_allowed(name, on_date="2026-09-09") is False
    assert production_allowed(name, on_date="2026-09-10") is False


def test_new_v41_numeric_rate_card_stays_unknown_until_officially_verified() -> None:
    entry=find_model("deepseek-flash")
    assert entry is not None
    assert entry["pricing"]["rate_card_verified"] is False
    candidate=entry["pricing"]["announced_pricing_candidate"]
    assert candidate["official_rate_card_verified"] is False
    assert estimate_budget_cost_usd("deepseek-flash", input_tokens=1_000_000, output_tokens=1_000_000) is None


def test_historical_flash_budget_keeps_last_verified_rate_for_audit() -> None:
    cost=estimate_budget_cost_usd("deepseek-v4-flash", input_tokens=1_000_000, output_tokens=1_000_000)
    assert cost == 1.76


def test_pro_budget_keeps_last_verified_rate_for_audit() -> None:
    cost=estimate_budget_cost_usd("deepseek-v4-pro", input_tokens=1_000_000, output_tokens=1_000_000)
    assert cost == 5.28


def test_usage_event_separates_requested_and_effective_models() -> None:
    event=build_usage_event(logical_route="proof_summary", requested_model="deepseek-v4-pro", effective_model="deepseek-flash", input_tokens=1000, output_tokens=250, retries=1, accepted=True)
    assert event.requested_model == "deepseek-v4-pro"
    assert event.effective_model == "deepseek-flash"
    assert event.logical_route == "proof_summary"
    assert event.retries == 1
    assert event.budget_cost_usd is None
    assert event.cost_per_accepted_result_usd is None
