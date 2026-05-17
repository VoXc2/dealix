"""Doctrine guard: a partner payout is never auto-paid.

Marking a payout as paid must queue a human ``ApprovalRequest`` and
leave the payout in ``awaiting_approval`` — money out of the door is
never auto-acted (non-negotiable #8).
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator

import pytest
import pytest_asyncio
from httpx import AsyncClient

_TMP = tempfile.mkdtemp(prefix="affiliate-payout-test-")
for _var in (
    "DEALIX_AFFILIATE_PARTNERS_PATH",
    "DEALIX_AFFILIATE_LINKS_PATH",
    "DEALIX_AFFILIATE_REFERRALS_PATH",
    "DEALIX_AFFILIATE_COMMISSIONS_PATH",
    "DEALIX_AFFILIATE_PAYOUTS_PATH",
    "DEALIX_AFFILIATE_COMPLIANCE_PATH",
):
    os.environ.setdefault(_var, os.path.join(_TMP, _var.lower() + ".jsonl"))
os.environ.setdefault("DEALIX_FRICTION_LOG_PATH", os.path.join(_TMP, "friction.jsonl"))
os.environ["ADMIN_API_KEYS"] = "test_affiliate_admin_key"

from auto_client_acquisition.approval_center import get_default_approval_store  # noqa: E402
from auto_client_acquisition.partnership_os import affiliate_store  # noqa: E402

_ADMIN = {"X-Admin-API-Key": "test_affiliate_admin_key"}


@pytest.fixture(autouse=True)
def _clean() -> Iterator[None]:
    affiliate_store.clear_for_test()
    yield
    affiliate_store.clear_for_test()


@pytest.mark.asyncio
async def test_payout_mark_paid_queues_approval(async_client: AsyncClient) -> None:
    # Seed a payout directly in the store.
    payout = {
        "id": "pay_guard1",
        "partner_id": "ptn_guard1",
        "period": "2026-05",
        "commission_ids": ["cmn_1"],
        "total_sar": 1500.0,
        "status": "pending",
        "partner_invoice_ref": None,
        "marked_paid_at": None,
        "marked_paid_by": None,
        "created_at": affiliate_store.now_iso(),
        "deleted_at": None,
    }
    affiliate_store.insert("payouts", payout)

    resp = await async_client.post(
        "/api/v1/payouts/mark-paid",
        json={
            "payout_id": "pay_guard1",
            "partner_invoice_ref": "INV-PARTNER-001",
            "marked_by": "founder",
        },
        headers=_ADMIN,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()

    # The payout is NOT paid — it is awaiting human approval.
    assert body["status"] == "approval_queued"
    assert body["governance_decision"] == "require_approval"
    stored = affiliate_store.get("payouts", "pay_guard1")
    assert stored["status"] == "awaiting_approval"
    assert stored["status"] != "paid"

    # A pending ApprovalRequest exists for this payout.
    pending = [
        r for r in get_default_approval_store().list_pending()
        if r.object_id == "pay_guard1"
    ]
    assert pending, "payout mark-paid did not queue an ApprovalRequest"
    assert pending[0].action_mode == "approval_required"
