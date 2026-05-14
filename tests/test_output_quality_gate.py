"""AI output quality gate — draft audit detects prohibited patterns."""

from __future__ import annotations

from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
from auto_client_acquisition.governance_os.forbidden_actions import is_channel_forbidden


def test_draft_gate_flags_cold_whatsapp_language() -> None:
    assert audit_draft_text("We will do cold whatsapp blasting for leads")


def test_channel_plan_whatsapp_forbidden_heuristic() -> None:
    assert is_channel_forbidden("plan: cold whatsapp to everyone")
