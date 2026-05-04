"""
Test: every Card emitted by the card_factory carries a risk_badge.

Vision constraint — every decision shown to a human must be ranked P0..P3
so the operator can triage at a glance without reading 6 fields.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_company_os.card_factory import build_feed
from auto_client_acquisition.revenue_company_os.cards import Role


@pytest.mark.parametrize("role", [r.value for r in Role])
def test_every_demo_card_has_risk_badge(role: str) -> None:
    cards = build_feed(role)
    for c in cards:
        assert c.risk_badge in {"P0", "P1", "P2", "P3"}, (
            f"card {c.id} (role={role}) missing risk_badge: got {c.risk_badge!r}"
        )


@pytest.mark.parametrize("role", [r.value for r in Role])
def test_to_dict_exposes_risk_badge(role: str) -> None:
    cards = build_feed(role)
    for c in cards:
        d = c.to_dict()
        assert "risk_badge" in d
        assert d["risk_badge"] in {"P0", "P1", "P2", "P3"}
