"""Revenue draft pack builder tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_os.draft_pack import build_revenue_draft_pack


def test_build_draft_pack_blocks_cold_whatsapp_request() -> None:
    with pytest.raises(ValueError):
        build_revenue_draft_pack(
            {"company_name": "Co"},
            request_cold_whatsapp=True,
        )


def test_whatsapp_draft_requires_relationship() -> None:
    pack = build_revenue_draft_pack(
        {"company_name": "Co"},
        include_whatsapp_draft=True,
        relationship_status="unknown",
    )
    assert "whatsapp_blocked_reason" in pack
    assert "whatsapp_draft" not in pack


def test_whatsapp_draft_with_explicit_consent() -> None:
    pack = build_revenue_draft_pack(
        {"company_name": "Co"},
        include_whatsapp_draft=True,
        relationship_status="explicit_consent",
    )
    assert "whatsapp_draft" in pack
    assert "linkedin_draft_en" in pack
