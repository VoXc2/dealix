"""Doctrine guardrails for governed commercial paths — the 11 non-negotiables."""

from __future__ import annotations

import pytest

from auto_client_acquisition.safe_send_gateway import (
    doctrine_violations_for_revenue_intelligence,
    enforce_doctrine_non_negotiables,
)
from auto_client_acquisition.safe_send_gateway.doctrine import DOCTRINE_REASONS

# Every kwarg -> the violation code it must raise.
DOCTRINE_CASES: dict[str, str] = {
    "request_scraping": "no_scraping",
    "request_cold_whatsapp": "no_cold_whatsapp",
    "request_linkedin_automation": "no_linkedin_automation",
    "request_fake_proof": "no_fake_proof",
    "request_guaranteed_sales_claim": "no_guaranteed_sales_claims",
    "request_pii_in_logs": "no_pii_in_logs",
    "request_sourceless_answer": "no_sourceless_answer",
    "request_external_send_without_approval": "external_action_requires_approval",
    "request_agent_without_identity": "no_agent_without_identity",
    "request_project_without_proof_pack": "no_project_without_proof_pack",
    "request_project_without_capital_asset": "no_project_without_capital_asset",
    "request_bulk_outreach": "no_bulk_outreach",
}


def test_doctrine_clean() -> None:
    codes, _reasons = doctrine_violations_for_revenue_intelligence()
    assert codes == ()
    enforce_doctrine_non_negotiables()


def test_doctrine_registry_covers_eleven_non_negotiables() -> None:
    """The 11 canonical non-negotiables plus the bulk-outreach extension."""
    assert len(DOCTRINE_REASONS) == 12
    assert set(DOCTRINE_CASES.values()) == set(DOCTRINE_REASONS)


@pytest.mark.parametrize(("kwarg", "code"), list(DOCTRINE_CASES.items()))
def test_doctrine_blocks(kwarg: str, code: str) -> None:
    codes, reasons = doctrine_violations_for_revenue_intelligence(**{kwarg: True})
    assert codes == (code,)
    assert code in reasons
    with pytest.raises(ValueError):
        enforce_doctrine_non_negotiables(**{kwarg: True})


@pytest.mark.parametrize("code", list(DOCTRINE_REASONS))
def test_doctrine_reasons_bilingual(code: str) -> None:
    reason = DOCTRINE_REASONS[code]
    assert reason["ar"].strip()
    assert reason["en"].strip()


def test_doctrine_multi_violation() -> None:
    codes, _r = doctrine_violations_for_revenue_intelligence(
        request_cold_whatsapp=True,
        request_scraping=True,
    )
    assert "no_cold_whatsapp" in codes
    assert "no_scraping" in codes
