"""Source contract for tenant-owned side effects in autonomous routes (#1070)."""
from __future__ import annotations

import re
from pathlib import Path

ROUTER = (Path(__file__).resolve().parents[1] / "api" / "routers" / "autonomous.py").read_text(encoding="utf-8")


def _function_block(name: str) -> str:
    match = re.search(
        rf"(?ms)^@router\.(?:get|post|patch)\([^\n]+\)\nasync def {re.escape(name)}\b.*?(?=^@router\.|^# ──|\Z)",
        ROUTER,
    )
    assert match, f"missing route function: {name}"
    return match.group(0)


def test_router_keeps_models_used_after_dashboard_imported() -> None:
    for name in (
        "CompanyRecord",
        "CustomerRecord",
        "OutreachQueueRecord",
        "PartnerRecord",
    ):
        assert re.search(rf"\b{name}\b", ROUTER.split("router = APIRouter", 1)[0]), (
            f"{name} must be imported before route execution"
        )


def test_payment_request_task_is_tenant_owned() -> None:
    block = _function_block("manual_payment_request")
    assert "tenant_id = _tenant_scope(" in block
    constructor = block.split("task = TaskRecord(", 1)[1]
    assert "tenant_id=tenant_id" in constructor


def test_mark_paid_onboarding_task_is_tenant_owned() -> None:
    block = _function_block("mark_paid")
    assert "tenant_id = _tenant_scope(" in block
    constructor = block.split("task = TaskRecord(", 1)[1]
    assert "tenant_id=tenant_id" in constructor
