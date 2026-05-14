"""Contract: outbound auto-send language is blocked (draft-only MVP)."""

from __future__ import annotations

from auto_client_acquisition.governance_os import policy_check_draft


def test_outreach_auto_send_blocked() -> None:
    assert policy_check_draft("We will auto-send WhatsApp without approval").allowed is False
    assert policy_check_draft("send automatically without approval").allowed is False
