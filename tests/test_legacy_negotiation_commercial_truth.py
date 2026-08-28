"""Commercial-truth regression tests for the legacy negotiation API surface."""
from __future__ import annotations

import json
from pathlib import Path

from intelligence.negotiation_engine import NegotiationEngine


RETIRED_MARKERS = (
    "7-day",
    "7 days",
    "7 أيام",
    "sar 499",
    "499 ريال",
    "prove roi in 7 days",
)


def _dump(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).lower()


def _assert_no_retired_markers(value: object) -> None:
    payload = _dump(value)
    for marker in RETIRED_MARKERS:
        assert marker.lower() not in payload


def test_all_negotiation_surfaces_reject_retired_launch_language() -> None:
    engine = NegotiationEngine()

    outputs = [
        engine.list_objections("both"),
        engine.handle_objection("price", lang="both"),
        engine.handle_objection("trust", lang="both"),
        engine.build_persuasion_map(
            "deal_test",
            [
                {
                    "name": "Decision Owner",
                    "role": "CEO",
                    "influence_level": "decision_maker",
                    "key_concern_en": "Evidence",
                    "key_concern_ar": "الأدلة",
                }
            ],
            lang="both",
        ),
        engine.generate_deal_strategy(
            company_name="Example Co",
            sector="software",
            city="Riyadh",
            package_sku="Revenue Command Pilot",
            budget_hint=499.0,
            employees=50,
            lang="both",
        ),
        engine.get_script("discovery_call", "both"),
        engine.get_script("objection_price", "both"),
        engine.get_script("closing", "both"),
    ]

    for output in outputs:
        _assert_no_retired_markers(output)


def test_deal_strategy_is_quote_only_and_non_committing() -> None:
    engine = NegotiationEngine()
    result = engine.generate_deal_strategy(
        company_name="Example Co",
        sector="software",
        city="Riyadh",
        package_sku="Revenue Command Pilot",
        budget_hint=999999.0,
        employees=100,
        lang="en",
    )
    payload = _dump(result)

    assert "quote_only_after_qualified_discovery" in payload
    assert "founder_approved_named_customer_quote_after_qualified_discovery" in payload
    assert '"adjusted_price_sar": null' in payload
    assert '"roi_estimate_percent": null' in payload
    assert '"execution_allowed": false' in payload
    assert '"approval_required": true' in payload


def test_current_commercial_path_is_present() -> None:
    engine = NegotiationEngine()
    payload = _dump(engine.handle_objection("trust", lang="en"))

    assert "free mini diagnostic" in payload
    assert "30-day revenue command pilot" in payload
    assert "stop/expand/redesign" in payload
    assert "public_fixed_pilot_price_allowed" in payload
    assert '"public_fixed_pilot_price_allowed": false' in payload


def test_source_does_not_reintroduce_hard_coded_retired_close() -> None:
    source = Path("intelligence/negotiation_engine.py").read_text(encoding="utf-8").lower()

    for marker in RETIRED_MARKERS:
        assert marker.lower() not in source
