"""Contract: guaranteed-outcome language is blocked in draft audit."""

from __future__ import annotations

from auto_client_acquisition.governance_os import policy_check_draft


def test_no_guaranteed_claims_in_draft() -> None:
    assert policy_check_draft("نضمن لك نتائج مبيعات خلال أسبوع").allowed is False
    assert policy_check_draft("We guarantee ROI in 30 days").allowed is False
