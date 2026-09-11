from __future__ import annotations

from datetime import UTC, datetime

import pytest

from scripts.ops.prepare_railway_migration_packet import build_packet


BASE = dict(
    project_id="project-1",
    environment_id="env-1",
    service_id="service-1",
    release_sha="a" * 40,
    builder_source_sha="b" * 40,
    alembic_heads=["20260908_023_consent_events"],
    backup_ref="proof://backup/verified-1",
    rollback_ref="docs/ops/ROLLBACK_RUNBOOK.md#path-b",
    created_at=datetime(2026, 9, 11, 0, 0, tzinfo=UTC),
    ttl_minutes=15,
)


def test_packet_is_non_executing_and_action_bound() -> None:
    packet = build_packet(**BASE)
    assert packet["packet_state"] == "PENDING_EXACT_L5_AUTHORITY"
    assert packet["execution_allowed"] is False
    assert packet["automatic_predeploy_authority"] is False
    assert packet["operation"] == "alembic upgrade 20260908_023_consent_events"
    assert len(packet["action_hash"]) == 16
    assert len(packet["payload_sha256"]) == 64


def test_packet_hash_changes_when_release_changes() -> None:
    one = build_packet(**BASE)
    changed = {**BASE, "release_sha": "c" * 40}
    two = build_packet(**changed)
    assert one["action_hash"] != two["action_hash"]
    assert one["idempotency_key"] != two["idempotency_key"]


def test_packet_requires_single_head_and_real_evidence_refs() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        build_packet(**{**BASE, "alembic_heads": ["a", "b"]})
    with pytest.raises(ValueError, match="backup_ref"):
        build_packet(**{**BASE, "backup_ref": "UNKNOWN"})
    with pytest.raises(ValueError, match="rollback_ref"):
        build_packet(**{**BASE, "rollback_ref": "TBD"})
    with pytest.raises(ValueError, match="backup_ref"):
        build_packet(**{**BASE, "backup_ref": "synthetic://backup"})


def test_packet_ttl_is_bounded() -> None:
    with pytest.raises(ValueError, match="ttl_minutes"):
        build_packet(**{**BASE, "ttl_minutes": 0})
    with pytest.raises(ValueError, match="ttl_minutes"):
        build_packet(**{**BASE, "ttl_minutes": 61})


def test_packet_rejects_naive_created_at() -> None:
    with pytest.raises(ValueError, match="created_at"):
        build_packet(**{**BASE, "created_at": datetime(2026, 9, 11, 0, 0)})
