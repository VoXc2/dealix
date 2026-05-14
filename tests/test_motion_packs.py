"""Smoke: motion packs (partner / investor / client) exist and reference core assets."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_partner_motion_pack_exists() -> None:
    p = REPO_ROOT / "docs/strategic/packs/PARTNER_MOTION_PACK_AR.md"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "HOLDING_OFFER_MATRIX_AR.md" in text
    assert "IP_LICENSE_OUTLINE_AR.md" in text
    assert "ما لا يُرسل" in text


def test_investor_motion_pack_exists() -> None:
    p = REPO_ROOT / "docs/strategic/packs/INVESTOR_MOTION_PACK_AR.md"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "HOLDING_VALUE_REGISTRY_AR.md" in text
    assert "USE_OF_FUNDS.md" in text
    assert "FIRST_3_HIRES.md" in text


def test_client_demo_pack_exists() -> None:
    p = REPO_ROOT / "docs/strategic/packs/CLIENT_DEMO_PACK_AR.md"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "PROOF_DEMO_PACK_5_CLIENTS_AR.md" in text
    assert "RETAINER_PILOT_MINI_AR.md" in text
