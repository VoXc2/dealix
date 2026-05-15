"""Contract: LinkedIn automation language is blocked in draft policy check."""

from __future__ import annotations

from auto_client_acquisition.governance_os import policy_check_draft


def test_no_linkedin_automation_in_draft() -> None:
    assert policy_check_draft("We will run linkedin automation for you").allowed is False
