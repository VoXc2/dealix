from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from scripts.ops.prepare_railway_migration_packet import build_packet

ROOT = Path(__file__).resolve().parents[1]

BACKUP_RECEIPT = {
    "schema_version": "dealix.railway-backup-receipt.v1",
    "provider": "railway",
    "status": "SUCCESS",
    "project_id": "project-1",
    "environment_id": "env-1",
    "service_id": "service-1",
    "backup_id": "backup-1",
    "provider_ref": "railway://backups/backup-1",
    "completed_at": "2026-09-10T23:55:00Z",
}

BASE = dict(
    project_id="project-1",
    environment_id="env-1",
    service_id="service-1",
    release_sha="a" * 40,
    builder_source_sha="b" * 40,
    alembic_heads=["20260908_023_consent_events"],
    backup_receipt=BACKUP_RECEIPT,
    rollback_ref="docs/ops/ROLLBACK_RUNBOOK.md#path-b",
    created_at=datetime(2026, 9, 11, 0, 0, tzinfo=UTC),
    ttl_minutes=15,
    repo_root=ROOT,
)


def test_packet_is_non_executing_action_bound_and_proof_bound() -> None:
    packet = build_packet(**BASE)
    assert packet["packet_state"] == "PENDING_EXACT_L5_AUTHORITY"
    assert packet["execution_allowed"] is False
    assert packet["automatic_predeploy_authority"] is False
    assert packet["operation"] == "alembic upgrade 20260908_023_consent_events"
    assert packet["backup_ref"] == "railway-backup:backup-1"
    assert len(packet["backup_receipt_sha256"]) == 64
    assert len(packet["rollback_artifact_sha256"]) == 64
    assert len(packet["action_hash"]) == 16
    assert len(packet["payload_sha256"]) == 64


def test_packet_hash_changes_when_release_changes() -> None:
    one = build_packet(**BASE)
    changed = {**BASE, "release_sha": "c" * 40}
    two = build_packet(**changed)
    assert one["action_hash"] != two["action_hash"]
    assert one["idempotency_key"] != two["idempotency_key"]


def test_packet_requires_single_head() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        build_packet(**{**BASE, "alembic_heads": ["a", "b"]})


def test_packet_rejects_unverified_or_cross_scope_backup_receipt() -> None:
    with pytest.raises(ValueError, match="status"):
        build_packet(**{**BASE, "backup_receipt": {**BACKUP_RECEIPT, "status": "PENDING"}})
    with pytest.raises(ValueError, match="service_id mismatch"):
        build_packet(**{**BASE, "backup_receipt": {**BACKUP_RECEIPT, "service_id": "service-other"}})
    with pytest.raises(ValueError, match="schema_version"):
        build_packet(**{**BASE, "backup_receipt": {**BACKUP_RECEIPT, "schema_version": "example"}})


def test_packet_rejects_future_backup_receipt() -> None:
    future = {**BACKUP_RECEIPT, "completed_at": "2026-09-11T00:01:00Z"}
    with pytest.raises(ValueError, match="cannot be after"):
        build_packet(**{**BASE, "backup_receipt": future})


def test_packet_requires_existing_repo_scoped_rollback_artifact() -> None:
    with pytest.raises(ValueError, match="artifact not found"):
        build_packet(**{**BASE, "rollback_ref": "docs/ops/missing.md"})
    with pytest.raises(ValueError, match="repository-relative"):
        build_packet(**{**BASE, "rollback_ref": str((ROOT / "docs/ops/ROLLBACK_RUNBOOK.md").resolve())})


def test_packet_ttl_is_bounded() -> None:
    with pytest.raises(ValueError, match="ttl_minutes"):
        build_packet(**{**BASE, "ttl_minutes": 0})
    with pytest.raises(ValueError, match="ttl_minutes"):
        build_packet(**{**BASE, "ttl_minutes": 61})


def test_packet_rejects_naive_created_at() -> None:
    with pytest.raises(ValueError, match="created_at"):
        build_packet(**{**BASE, "created_at": datetime(2026, 9, 11, 0, 0)})