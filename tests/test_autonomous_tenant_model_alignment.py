"""Runtime metadata alignment for conversation/task tenant ownership (#1070)."""
from __future__ import annotations

from sqlalchemy import String

from db.models import ConversationRecord, TaskRecord


def _assert_tenant_column(model, composite_index: str) -> None:
    table = model.__table__
    column = table.c.tenant_id

    assert isinstance(column.type, String)
    assert column.type.length == 64
    assert column.nullable is True

    foreign_keys = list(column.foreign_keys)
    assert len(foreign_keys) == 1
    assert foreign_keys[0].target_fullname == "tenants.id"
    assert foreign_keys[0].ondelete == "CASCADE"

    indexes = {index.name for index in table.indexes}
    assert composite_index in indexes
    assert f"ix_{table.name}_tenant_id" not in indexes, (
        "a redundant single-column tenant index would drift from revision 020"
    )


def test_conversation_tenant_metadata_matches_revision_020() -> None:
    _assert_tenant_column(
        ConversationRecord,
        "ix_conversations_tenant_created",
    )


def test_task_tenant_metadata_matches_revision_020() -> None:
    _assert_tenant_column(
        TaskRecord,
        "ix_tasks_tenant_status_due",
    )
