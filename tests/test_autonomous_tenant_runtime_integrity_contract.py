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


def test_legacy_payment_request_has_no_side_effect_task() -> None:
    block = _function_block("manual_payment_request")
    assert "LEGACY_PAYMENT_REQUEST_QUARANTINED" in block
    assert '"mutation_applied": False' in block
    assert "TaskRecord(" not in block
    assert "session.commit" not in block


def test_legacy_mark_paid_cannot_create_onboarding_side_effects() -> None:
    block = _function_block("mark_paid")
    assert "BODY_ONLY_PAYMENT_STATE_FORBIDDEN" in block
    assert '"verified_payment_requires_evidence": True' in block
    assert "CustomerRecord(" not in block
    assert "TaskRecord(" not in block
    assert "session.commit" not in block
