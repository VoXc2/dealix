"""Contract: case-study marketing requires verified claim class + client permission."""

from __future__ import annotations

from auto_client_acquisition.risk_resilience_os.claim_safety import (
    claim_may_appear_in_case_study,
)


def test_case_study_requires_verified_value() -> None:
    assert claim_may_appear_in_case_study("verified", client_permission=True) is True
    assert claim_may_appear_in_case_study("observed", client_permission=True) is False
    assert claim_may_appear_in_case_study("estimated", client_permission=True) is False
    assert claim_may_appear_in_case_study("verified", client_permission=False) is False
