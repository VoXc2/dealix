"""
Test: every Card emitted by the card_factory carries a non-empty why_now_ar.

Vision constraint — "every decision shown to a human must answer 'why now?'
in Arabic". This is enforced at the Card schema level (__post_init__ raises
if missing); this test confirms the demo + role builders never miss it.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_company_os.card_factory import build_feed
from auto_client_acquisition.revenue_company_os.cards import Role


@pytest.mark.parametrize("role", [r.value for r in Role])
def test_every_demo_card_has_why_now(role: str) -> None:
    cards = build_feed(role)
    for c in cards:
        assert c.why_now_ar and c.why_now_ar.strip(), (
            f"card {c.id} (role={role}) missing why_now_ar"
        )
        # And it should be Arabic — at least one Arabic char.
        assert any('؀' <= ch <= 'ۿ' for ch in c.why_now_ar), (
            f"card {c.id} (role={role}) why_now_ar is not Arabic: {c.why_now_ar!r}"
        )
