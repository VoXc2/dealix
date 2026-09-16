from __future__ import annotations

import ast
from pathlib import Path

import pytest
from fastapi import HTTPException

from api.routers.autonomous import manual_payment_request, mark_paid

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "api/routers/autonomous.py"


@pytest.mark.asyncio
async def test_legacy_manual_payment_request_is_fail_closed() -> None:
    with pytest.raises(HTTPException) as exc:
        await manual_payment_request(None, {"deal_id": "d1"}, None)  # type: ignore[arg-type]
    assert exc.value.status_code == 410
    detail = exc.value.detail
    assert detail["code"] == "LEGACY_PAYMENT_REQUEST_QUARANTINED"
    assert detail["canonical_path"] == "POST /api/v1/payment-ops/invoice-intent"
    assert detail["external_send_allowed"] is False
    assert detail["payment_execution_allowed"] is False
    assert detail["mutation_applied"] is False


@pytest.mark.asyncio
async def test_body_only_mark_paid_can_never_mint_payment_or_customer() -> None:
    with pytest.raises(HTTPException) as exc:
        await mark_paid(
            None,
            {"deal_id": "d1", "amount": 999999, "plan": "anything"},
            None,
        )  # type: ignore[arg-type]
    assert exc.value.status_code == 410
    detail = exc.value.detail
    assert detail["code"] == "BODY_ONLY_PAYMENT_STATE_FORBIDDEN"
    assert detail["verified_payment_requires_evidence"] is True
    assert detail["delivery_requires_payment_confirmed"] is True
    assert detail["mutation_applied"] is False


def _function_source(name: str) -> str:
    tree = ast.parse(LEGACY.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return ast.unparse(node)
    raise AssertionError(name)


def test_legacy_payment_shims_have_no_db_or_customer_transition_logic() -> None:
    combined = _function_source("manual_payment_request") + "\n" + _function_source("mark_paid")
    for forbidden in (
        'deal.stage = "paid"',
        'deal.stage = "payment_requested"',
        "CustomerRecord(",
        "TaskRecord(",
        "session.commit",
        "deal.amount =",
        "pilot_end_at",
    ):
        assert forbidden not in combined
    assert "BODY_ONLY_PAYMENT_STATE_FORBIDDEN" in combined
    assert "LEGACY_PAYMENT_REQUEST_QUARANTINED" in combined
