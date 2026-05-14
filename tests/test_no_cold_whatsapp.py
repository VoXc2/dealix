"""Contract: cold WhatsApp language is blocked in draft policy check."""

from __future__ import annotations

from auto_client_acquisition.governance_os import policy_check_draft


def test_no_cold_whatsapp_in_draft() -> None:
    assert policy_check_draft("Use cold whatsapp to reach everyone").allowed is False
