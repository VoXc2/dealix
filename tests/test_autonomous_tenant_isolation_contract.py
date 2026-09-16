"""Acceptance contract for P0 autonomous-route tenant isolation (#1070).

These tests intentionally describe the target state.  The Draft PR must remain
red until the ORM and runtime surfaces are tenant-bound.  They are source-level
contract tests so they fail before a database is available and complement the
Postgres migration proof required before readiness.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = (ROOT / "db" / "models.py").read_text(encoding="utf-8")
ROUTER = (ROOT / "api" / "routers" / "autonomous.py").read_text(encoding="utf-8")


def _class_block(name: str, next_name: str) -> str:
    match = re.search(
        rf"class {name}\b.*?(?=\nclass {next_name}\b)",
        MODELS,
        flags=re.DOTALL,
    )
    assert match, f"missing model block: {name}"
    return match.group(0)


def _function_block(name: str) -> str:
    match = re.search(
        rf"async def {name}\b.*?(?=\n(?:@router|async def|def)\b|\Z)",
        ROUTER,
        flags=re.DOTALL,
    )
    assert match, f"missing route function: {name}"
    return match.group(0)


def test_conversation_and_task_models_have_tenant_ownership() -> None:
    conversation = _class_block("ConversationRecord", "TaskRecord")
    task = _class_block("TaskRecord", "CompanyRecord")

    for name, block in (("ConversationRecord", conversation), ("TaskRecord", task)):
        assert "tenant_id:" in block, f"{name} must carry tenant_id"
        tenant_decl = next(line for line in block.splitlines() if "tenant_id:" in line)
        assert "String(64)" in tenant_decl, (
            f"{name}.tenant_id must match revision 020 length"
        )
        assert 'ForeignKey("tenants.id", ondelete="CASCADE")' in tenant_decl, (
            f"{name}.tenant_id must match revision 020 delete behavior"
        )
        assert "index=True" not in tenant_decl, (
            f"{name}.tenant_id must not create a redundant single-column index"
        )


def test_sensitive_autonomous_routes_require_authenticated_tenant_scope() -> None:
    for name in (
        "create_conversation",
        "list_conversations",
        "create_task",
        "update_task",
        "list_tasks",
        "dashboard_metrics",
    ):
        block = _function_block(name)
        assert "Depends(get_current_user)" in block, f"{name} must require authenticated user"
        assert "Request" in block, f"{name} must accept Request for canonical tenant resolution"
        assert "_tenant_scope(" in block, f"{name} must resolve canonical tenant scope"


def test_conversation_queries_are_tenant_filtered_and_creates_are_stamped() -> None:
    create_block = _function_block("create_conversation")
    list_block = _function_block("list_conversations")

    assert "tenant_id=tenant_id" in create_block
    assert "ConversationRecord.tenant_id == tenant_id" in list_block


def test_task_queries_are_tenant_filtered_and_creates_are_stamped() -> None:
    create_block = _function_block("create_task")
    update_block = _function_block("update_task")
    list_block = _function_block("list_tasks")

    assert "tenant_id=tenant_id" in create_block
    assert "TaskRecord.tenant_id == tenant_id" in update_block
    assert "TaskRecord.tenant_id == tenant_id" in list_block


def test_legacy_payment_routes_are_authenticated_and_side_effect_free() -> None:
    """Quarantined payment compatibility routes authenticate but never mutate tenant state."""
    for name in ("manual_payment_request", "mark_paid"):
        block = _function_block(name)
        assert "Depends(get_current_user)" in block, f"{name} must require authenticated user"
        assert '"mutation_applied": False' in block
        assert "TaskRecord(" not in block
        assert "CustomerRecord(" not in block
        assert "session.commit" not in block


def test_runtime_model_imports_cover_downstream_autonomous_routes() -> None:
    """Prevent source rewrites from silently deleting imports used below the patched block."""
    for model in ("CompanyRecord", "CustomerRecord", "OutreachQueueRecord", "PartnerRecord"):
        assert re.search(rf"\b{model}\b", ROUTER), f"{model} must remain imported/available"
    import_block = ROUTER.split("from db.session import", 1)[0]
    for model in ("CompanyRecord", "CustomerRecord", "OutreachQueueRecord", "PartnerRecord"):
        assert model in import_block, f"{model} must be imported before route execution"


def test_dashboard_aggregates_are_tenant_scoped() -> None:
    block = _function_block("dashboard_metrics")

    for model in ("LeadRecord", "DealRecord", "ConversationRecord", "TaskRecord"):
        assert f"{model}.tenant_id == tenant_id" in block, (
            f"dashboard must tenant-scope {model} aggregates"
        )


def test_cross_tenant_task_lookup_fails_closed() -> None:
    block = _function_block("update_task")
    assert "TaskRecord.id == task_id" in block
    assert "TaskRecord.tenant_id == tenant_id" in block
    assert 'status_code=404' in block


def test_auto_sent_cannot_be_enabled_directly_by_request_body() -> None:
    """Direct API input must not be able to bypass approval-first communication."""
    block = _function_block("create_conversation")
    forbidden = 'auto_sent=bool(body.get("auto_sent", False))'
    assert forbidden not in block, (
        "create_conversation must not trust caller-provided auto_sent; controlled execution "
        "belongs behind the canonical approval/action adapter"
    )
