"""Tests for market_power_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.market_power_os.benchmark_registry import get_benchmark
from auto_client_acquisition.market_power_os.category_language_tracker import (
    market_language_health_score,
)
from auto_client_acquisition.market_power_os.content_signal import (
    education_funnel_coverage_percent,
)
from auto_client_acquisition.market_power_os.market_power_score import (
    MarketPowerDimensions,
    compute_market_power_score,
)
from auto_client_acquisition.market_power_os.partner_signal import (
    PartnerGateSignals,
    compute_partner_gate_readiness,
)


def test_market_language_health_bounded() -> None:
    s = market_language_health_score(
        "governed ai operations and proof pack with governance runtime",
    )
    assert 0 <= s <= 100


def test_market_language_avoided_terms_hurt() -> None:
    low = market_language_health_score("chatbot agency and cold whatsapp")
    high = market_language_health_score("governed ai operations proof pack")
    assert high > low


def test_funnel_coverage_full_level1() -> None:
    topics = {"why_ai_fails", "tool_vs_operations", "data_before_model"}
    assert education_funnel_coverage_percent(1, topics) == 100.0


def test_funnel_unknown_topic_raises() -> None:
    with pytest.raises(ValueError, match="Unknown topic"):
        education_funnel_coverage_percent(1, {"not_a_topic"})


def test_partner_gate_full() -> None:
    assert (
        compute_partner_gate_readiness(
            PartnerGateSignals(
                understands_dealix_method=True,
                respects_no_unsafe_automation=True,
                commits_to_proof_pack=True,
                accepts_qa=True,
                accepts_audit_rights=True,
                no_guaranteed_claims=True,
            ),
        )
        == 100
    )


def test_get_benchmark() -> None:
    b = get_benchmark("revenue_intelligence")
    assert b is not None and b.title_en.startswith("Revenue")


def test_market_power_score_all_hundred() -> None:
    assert (
        compute_market_power_score(
            MarketPowerDimensions(
                category_power=100,
                trust_power=100,
                proof_power=100,
                data_benchmark_power=100,
                distribution_power=100,
                product_power=100,
                standards_power=100,
                venture_power=100,
            ),
        )
        == 100.0
    )


def test_market_power_invalid_dim() -> None:
    with pytest.raises(ValueError):
        compute_market_power_score(MarketPowerDimensions(category_power=101))
