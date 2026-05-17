"""Doctrine guard: the mandatory disclosure must be accepted to activate.

A partner who has not accepted the paid-referral disclosure cannot have
their activation queued. The disclosure asset itself must ship in both
Arabic and English.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator

import pytest
import pytest_asyncio
from httpx import AsyncClient

_TMP = tempfile.mkdtemp(prefix="affiliate-disclosure-test-")
for _var in (
    "DEALIX_AFFILIATE_PARTNERS_PATH",
    "DEALIX_AFFILIATE_LINKS_PATH",
    "DEALIX_AFFILIATE_REFERRALS_PATH",
    "DEALIX_AFFILIATE_COMMISSIONS_PATH",
    "DEALIX_AFFILIATE_PAYOUTS_PATH",
    "DEALIX_AFFILIATE_COMPLIANCE_PATH",
):
    os.environ.setdefault(_var, os.path.join(_TMP, _var.lower() + ".jsonl"))
os.environ["ADMIN_API_KEYS"] = "test_affiliate_admin_key"

from auto_client_acquisition.partnership_os import affiliate_store, approved_assets  # noqa: E402

_ADMIN = {"X-Admin-API-Key": "test_affiliate_admin_key"}


@pytest.fixture(autouse=True)
def _clean() -> Iterator[None]:
    affiliate_store.clear_for_test()
    yield
    affiliate_store.clear_for_test()


def test_disclosure_asset_ships_in_arabic_and_english() -> None:
    ar = approved_assets.get_disclosure("ar")
    en = approved_assets.get_disclosure("en")
    assert ar["locale"] == "ar"
    assert en["locale"] == "en"
    assert ar["body"].strip()
    assert en["body"].strip()


@pytest.mark.asyncio
async def test_activation_blocked_without_disclosure(async_client: AsyncClient) -> None:
    application = {
        "company_name": "No Disclosure Co",
        "contact_name": "Test Person",
        "contact_email": "test@nodisclosure.sa",
        "country": "sa",
        "audience_type": "b2b",
        "audience_size": 1000,
        "main_channel": "consulting",
        "plan": "We will refer Dealix to our B2B clients through warm intros.",
        "prior_referrals": 1,
        "disclosure_accepted": False,
    }
    resp = await async_client.post("/api/v1/public/partner-apply", json=application)
    assert resp.status_code == 200, resp.text
    partner_id = resp.json()["partner_id"]

    # Approval cannot be queued — disclosure was never accepted.
    resp = await async_client.post(
        f"/api/v1/partners/{partner_id}/approve",
        json={"approver": "founder", "tier": "affiliate_lead"},
        headers=_ADMIN,
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail["error"] == "disclosure_not_accepted"
