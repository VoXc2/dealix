from __future__ import annotations

from scripts.commercial.verify_event_market_intelligence import load_pack, validate_pack


def test_live_event_market_intelligence_pack_is_fail_closed() -> None:
    payload = load_pack(
        __import__("pathlib").Path("data/founder/event_market_intelligence_2026-08-30.json")
    )
    validate_pack(payload)
    assert payload["status"] == "RESEARCH_ONLY_NO_RELATIONSHIP_TRUTH"
    assert all(value is False for value in payload["authority"].values())
    assert all(value is False for value in payload["truth_firewall"].values())
    assert payload["post_interaction_internal_sla"]["external_send"] is False


def test_big5_targets_are_questions_and_evidence_not_leads() -> None:
    payload = load_pack(
        __import__("pathlib").Path("data/founder/event_market_intelligence_2026-08-30.json")
    )
    targets = [
        target
        for route in payload["big5_founder_route"]
        for target in route["targets"]
    ]
    assert len(targets) == 6
    assert all(len(target["conversation_questions"]) == 3 for target in targets)
    assert all(target["next_evidence"] for target in targets)
    assert all(target["package_hypotheses_only"] for target in targets)
