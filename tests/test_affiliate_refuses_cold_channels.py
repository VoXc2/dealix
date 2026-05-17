"""Doctrine guard: the affiliate machine refuses forbidden channels.

A partner recruitment plan that proposes cold WhatsApp, LinkedIn
automation, or scraping is refused (non-negotiables #1-3). Guaranteed
ROI / outcome claims in partner content are also refused (#5).
"""

from __future__ import annotations

import os
import tempfile

import pytest
import pytest_asyncio
from httpx import AsyncClient

from auto_client_acquisition.partnership_os import compliance_guard

_TMP = tempfile.mkdtemp(prefix="affiliate-cold-test-")
for _var in (
    "DEALIX_AFFILIATE_PARTNERS_PATH",
    "DEALIX_AFFILIATE_LINKS_PATH",
    "DEALIX_AFFILIATE_REFERRALS_PATH",
    "DEALIX_AFFILIATE_COMMISSIONS_PATH",
    "DEALIX_AFFILIATE_PAYOUTS_PATH",
    "DEALIX_AFFILIATE_COMPLIANCE_PATH",
):
    os.environ.setdefault(_var, os.path.join(_TMP, _var.lower() + ".jsonl"))


def test_compliance_guard_refuses_cold_whatsapp() -> None:
    scan = compliance_guard.scan_recruitment_request(
        "We will do a cold WhatsApp blast to thousands of numbers."
    )
    assert scan.ok is False
    assert any(v.code == "cold_whatsapp" for v in scan.violations)


def test_compliance_guard_refuses_linkedin_automation() -> None:
    scan = compliance_guard.scan_recruitment_request(
        "Our plan is to use LinkedIn automation bots to auto-connect."
    )
    assert scan.ok is False
    assert any(v.code == "linkedin_automation" for v in scan.violations)


def test_compliance_guard_refuses_scraping() -> None:
    scan = compliance_guard.scan_recruitment_request(
        "We will scrape company directories and harvest emails."
    )
    assert scan.ok is False
    assert any(v.code == "scraping" for v in scan.violations)


def test_compliance_guard_flags_guaranteed_claim() -> None:
    violations = compliance_guard.scan_partner_content(
        "Join via my link — we guarantee ROI within 30 days."
    )
    assert any(v.code == "forbidden_claim" for v in violations)


def test_clean_plan_passes() -> None:
    scan = compliance_guard.scan_recruitment_request(
        "We will introduce Dealix to our B2B clients through warm intros "
        "and quarterly business reviews."
    )
    assert scan.ok is True
    assert scan.violations == []


@pytest.mark.asyncio
async def test_partner_apply_rejects_cold_channel_plan(async_client: AsyncClient) -> None:
    application = {
        "company_name": "Cold Outreach Co",
        "contact_name": "Test Person",
        "contact_email": "test@coldoutreach.sa",
        "country": "sa",
        "audience_type": "b2b",
        "audience_size": 1000,
        "main_channel": "agency",
        "plan": "We will run a cold WhatsApp blast and scrape LinkedIn for leads.",
        "disclosure_accepted": True,
    }
    resp = await async_client.post("/api/v1/public/partner-apply", json=application)
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail["error"] == "recruitment_plan_violates_doctrine"
    assert detail["governance_decision"] == "block"
