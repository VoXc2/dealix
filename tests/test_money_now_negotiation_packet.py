"""Contracts for the draft-only Money Now negotiation packet (no invention)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load() -> object:
    path = ROOT / "scripts" / "commercial" / "render_money_now_negotiation_packet.py"
    spec = importlib.util.spec_from_file_location("render_money_now_negotiation_packet", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


packet_mod = _load()

QUEUE = {
    "schema": "company_work_queue_v1",
    "generated_at": "2026-09-11T13:48:54+00:00",
    "fingerprint": "abc",
    "items": [
        {
            "id": "v18-pi-imini-001",
            "target": "iMini / Jannie",
            "owner": "dealix-sales",
            "area": "COMMERCIAL/WARM_NETWORK",
            "status": "NEGOTIATION",
            "priority": 214.5,
            "next_action": "NEGOTIATION",
            "founder_minutes": 10,
            "evidence": ["two-way email 2026-08-24"],
            "counts_as_revenue": False,
            "counts_as_pipeline": False,
        },
        {
            "id": "ready-1",
            "target": "Other",
            "status": "READY",
            "priority": 100,
            "counts_as_revenue": False,
            "counts_as_pipeline": False,
        },
    ],
}


def test_only_negotiation_items_are_selected() -> None:
    selected = packet_mod.select_negotiation_items(QUEUE)
    assert [item["id"] for item in selected] == ["v18-pi-imini-001"]


def test_packet_keeps_truth_flags_and_never_invents_amount_or_hash() -> None:
    packet = packet_mod.build_packet(QUEUE, generated_at="2026-09-12T00:00:00Z")
    assert packet["item_count"] == 1
    item = packet["items"][0]
    assert item["counts_as_revenue"] is False
    assert item["counts_as_pipeline"] is False
    assert item["external_send"] is False
    assert item["amount"] == "UNKNOWN_NOT_INVENTED"
    assert item["action_hash"] == "PENDING_EXACT_DRAFT_PAYLOAD"
    assert item["approval_hash_input"]["payload"] == "PENDING_EXACT_DRAFT_PAYLOAD"
    assert packet["firewalls"]["external_send"] is False
    assert packet_mod.verify_packet(packet) == []


def test_verify_rejects_promoted_revenue_or_fabricated_hash() -> None:
    packet = packet_mod.build_packet(QUEUE, generated_at="2026-09-12T00:00:00Z")
    packet["items"][0]["counts_as_revenue"] = True
    packet["items"][0]["action_hash"] = "deadbeef" * 4
    failures = packet_mod.verify_packet(packet)
    assert any("revenue/pipeline" in failure for failure in failures)
    assert any("fabricated action hash" in failure for failure in failures)


def test_render_markdown_lists_target_and_firewall() -> None:
    packet = packet_mod.build_packet(QUEUE, generated_at="2026-09-12T00:00:00Z")
    markdown = packet_mod.render_markdown(packet)
    assert "iMini / Jannie" in markdown
    assert "UNKNOWN_NOT_INVENTED" in markdown
    assert "external_send: `False`" in markdown
