"""Tests for the customer room dashboard generator.

Pure unit tests — no network, no LLM, no DB. Verifies the 11-card
layout, the bilingual structure, and the no-data-yet sentinel.
"""
from __future__ import annotations

from auto_client_acquisition.designops.generators import (
    generate_customer_room_dashboard,
)
from auto_client_acquisition.designops.generators.customer_room_dashboard import (
    _SECTIONS,
)


_NO_DATA = "no data yet"
_NO_DATA_AR = "لا بيانات بعد"


def test_dashboard_renders_all_eleven_sections() -> None:
    payload = {
        "stage": "pilot",
        "active_services": ["growth_starter"],
        "health_score": 72,
        "proof_events_count": 5,
        "pending_approvals": ["proof_pack_v1"],
        "blocked_unsafe_actions": ["cold_whatsapp"],
        "next_best_actions": ["follow up via inbound channel"],
        "weekly_summary": "10 qualified opportunities",
        "channel_policy": "inbound + warm intros only",
        "delivery_sessions": [{"id": "d1"}],
        "executive_notes": ["founder review pending"],
    }
    art = generate_customer_room_dashboard("ACME", payload)
    # Spec demands 11 cards.
    assert len(_SECTIONS) == 11
    # AR titles all present in the markdown.
    for _key, title_ar, title_en, _kind in _SECTIONS:
        assert title_ar in art["markdown_ar"], f"missing AR section: {title_ar}"
        assert title_en in art["markdown_en"], f"missing EN section: {title_en}"
    # Manifest summary.
    assert art["manifest"]["section_count"] == 11
    assert art["manifest"]["safe_to_send"] is False


def test_dashboard_missing_data_renders_no_data_yet_banner() -> None:
    art = generate_customer_room_dashboard("anon", {})
    assert _NO_DATA in art["markdown_en"]
    assert _NO_DATA_AR in art["markdown_ar"]
    # Every section has the sentinel because payload is empty.
    for _key, title_ar, title_en, _kind in _SECTIONS:
        # The bilingual sentinel string used in HTML cards.
        # In the AR markdown we render the AR side; in EN the EN side.
        assert title_ar in art["markdown_ar"]
        assert title_en in art["markdown_en"]


def test_dashboard_bilingual_structure_intact() -> None:
    art = generate_customer_room_dashboard(
        "ACME",
        {"stage": "live", "active_services": ["data_to_revenue"]},
    )
    # Arabic primary signal: the document begins with the AR title.
    assert art["markdown_ar"].splitlines()[0].startswith("# ")
    assert "ACME" in art["markdown_ar"]
    # English block has the customer handle too.
    assert "ACME" in art["markdown_en"]
    # HTML carries both the AR title and the EN title.
    assert "غرفة العميل" in art["html"]
    assert "Customer Room" in art["html"]
    # Approval-required banner present.
    assert "approval_required" in art["html"]
