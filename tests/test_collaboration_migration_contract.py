"""Static migration contract for the Collaboration OS storage extension."""

from pathlib import Path


MIGRATION = Path("db/migrations/versions/20260823_021_collaboration_events.py")


def test_collaboration_migration_extends_existing_snapshot_constraint() -> None:
    source = MIGRATION.read_text(encoding="utf-8")

    assert 'revision: str = "20260823_021_collaboration_events"' in source
    assert (
        'down_revision: str | None = "20260812_020_tenant_scope_conversations_tasks"'
        in source
    )
    assert "ck_communication_hub_collection" in source
    assert "'contact_log', 'sequences', 'collaboration_events'" in source
    assert "ON CONFLICT (collection) DO NOTHING" in source


def test_collaboration_migration_downgrade_will_not_silently_delete_history() -> None:
    source = MIGRATION.read_text(encoding="utf-8")

    assert "Cannot downgrade: collaboration_events contains durable data" in source
    assert "RAISE EXCEPTION" in source
    assert "data <> '[]'::jsonb" in source
