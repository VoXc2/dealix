"""Dealix internal dogfooding war room sync."""

from __future__ import annotations

from pathlib import Path

from dealix.commercial_ops.paths import DEALIX_INTERNAL_WAR_ROOM_CSV, REPO_ROOT


def test_internal_war_room_seed_exists():
    assert DEALIX_INTERNAL_WAR_ROOM_CSV.is_file()
    text = DEALIX_INTERNAL_WAR_ROOM_CSV.read_text(encoding="utf-8")
    assert "Dealix:" in text
    assert "internal_milestone" in text


def test_dogfooding_payload_module():
    from dealix.commercial_ops.dogfooding_war_room import build_dogfooding_payload

    payload = build_dogfooding_payload(top_n=5)
    assert payload["kind"] == "dealix_dogfooding_war_room"
    items = payload.get("targets", {}).get("items") or []
    assert len(items) >= 1
