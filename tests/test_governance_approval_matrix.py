"""Governance OS — approval matrix + forbidden channel helper."""

from __future__ import annotations

from auto_client_acquisition.governance_os import approval_for_action, is_channel_forbidden


def test_whatsapp_high_risk() -> None:
    risk, _who = approval_for_action("send whatsapp blast")
    assert risk == "high"


def test_forbidden_channel_detection() -> None:
    assert is_channel_forbidden("cold whatsapp script") is True
