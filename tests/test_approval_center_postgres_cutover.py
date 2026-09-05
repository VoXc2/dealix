from __future__ import annotations

import importlib.util
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy import create_engine

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
    reset_default_approval_store_for_tests,
)
from auto_client_acquisition.approval_center.postgres_store import PostgresApprovalStore
from auto_client_acquisition.approval_center.schemas import ApprovalRequest, ApprovalStatus


class _RuleEngine:
    def __init__(self) -> None:
        self.matches = 0

    def match(self, req, *, confidence: float, content: str):
        assert req.action_mode == "approval_required"
        assert confidence == 0.95
        assert content == "approved pattern"
        return SimpleNamespace(rule_id="rule_1", name="safe_email")

    def record_match(self, rule, req, *, confidence: float) -> None:
        self.matches += 1


@pytest.fixture(autouse=True)
def _reset_backend(monkeypatch):
    for key in (
        "DEALIX_APPROVAL_STORE_BACKEND",
        "DEALIX_APPROVAL_DATABASE_URL",
        "DATABASE_URL",
    ):
        monkeypatch.delenv(key, raising=False)
    reset_default_approval_store_for_tests()
    yield
    reset_default_approval_store_for_tests()


def _request(
    suffix: str,
    *,
    expires_at: datetime | None = None,
    proof_impact: str = "leadops:test",
) -> ApprovalRequest:
    return ApprovalRequest(
        approval_id=f"apr_{suffix}",
        object_type="lead",
        object_id=f"lead_{suffix}",
        action_type="draft_email",
        action_mode="approval_required",
        channel="email",
        summary_en=f"request {suffix}",
        proof_impact=proof_impact,
        expires_at=expires_at,
    )


def _stores(tmp_path: Path):
    yield ApprovalStore()
    yield PostgresApprovalStore(
        database_url=f"sqlite:///{tmp_path / 'contract.sqlite3'}",
        create_tables=True,
    )


def test_default_backend_remains_memory() -> None:
    assert isinstance(get_default_approval_store(), ApprovalStore)


def test_explicit_postgres_requires_database_url(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_APPROVAL_STORE_BACKEND", "postgres")
    with pytest.raises(
        RuntimeError,
        match="approval_store_postgres_requested_but_database_url_missing",
    ):
        get_default_approval_store()


def test_explicit_postgres_requires_migrated_schema(monkeypatch, tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'unmigrated.sqlite3'}"
    monkeypatch.setenv("DEALIX_APPROVAL_STORE_BACKEND", "postgres")
    monkeypatch.setenv("DEALIX_APPROVAL_DATABASE_URL", database_url)
    with pytest.raises(RuntimeError, match="approval_center_schema_not_migrated"):
        get_default_approval_store()


def test_unknown_backend_fails_closed(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_APPROVAL_STORE_BACKEND", "redis-magic")
    with pytest.raises(RuntimeError, match="unsupported_approval_store_backend"):
        get_default_approval_store()


def test_postgres_factory_survives_singleton_reset(monkeypatch, tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'approval.sqlite3'}"
    PostgresApprovalStore(database_url=database_url, create_tables=True)
    monkeypatch.setenv("DEALIX_APPROVAL_STORE_BACKEND", "postgres")
    monkeypatch.setenv("DEALIX_APPROVAL_DATABASE_URL", database_url)

    first = get_default_approval_store()
    assert isinstance(first, PostgresApprovalStore)
    first.create(_request("persisted"))

    reset_default_approval_store_for_tests()
    second = get_default_approval_store()
    assert isinstance(second, PostgresApprovalStore)
    restored = second.get("apr_persisted")
    assert restored is not None
    assert restored.summary_en == "request persisted"


@pytest.mark.parametrize("backend", ["memory", "postgres"])
def test_full_contract_parity(backend: str, tmp_path: Path) -> None:
    if backend == "memory":
        store = ApprovalStore()
    else:
        store = PostgresApprovalStore(
            database_url=f"sqlite:///{tmp_path / 'parity.sqlite3'}",
            create_tables=True,
        )

    editable = store.create(_request("edit"))
    assert editable.approval_id == "apr_edit"
    edited = store.edit(
        "apr_edit",
        "founder",
        {"summary_en": "updated", "approval_id": "must_not_change"},
    )
    assert edited.summary_en == "updated"
    assert edited.approval_id == "apr_edit"
    approved = store.approve("apr_edit", "founder")
    assert ApprovalStatus(approved.status) == ApprovalStatus.APPROVED
    assert approved.edit_history[-1]["action"] == "approve"

    rejected = store.create(_request("reject"))
    rejected = store.reject(rejected.approval_id, "founder", "not aligned")
    assert ApprovalStatus(rejected.status) == ApprovalStatus.REJECTED
    assert rejected.reject_reason == "not aligned"

    store.create(
        _request("expired", expires_at=datetime.now(UTC) - timedelta(minutes=1))
    )
    assert store.expire_overdue() == 1
    expired = store.get("apr_expired")
    assert expired is not None
    assert ApprovalStatus(expired.status) == ApprovalStatus.EXPIRED

    store.create(_request("bulk_1", proof_impact="leadops:batch"))
    store.create(_request("bulk_2", proof_impact="leadops:batch"))
    bulk = store.bulk_approve(who="founder", proof_impact_prefix="leadops:")
    assert bulk["total"] == 2
    assert sorted(bulk["approved"]) == ["apr_bulk_1", "apr_bulk_2"]

    engine = _RuleEngine()
    automatic = store.create_with_founder_rules(
        _request("auto"),
        confidence=0.95,
        content="approved pattern",
        engine=engine,
    )
    assert ApprovalStatus(automatic.status) == ApprovalStatus.APPROVED
    assert automatic.action_mode == "approved_execute"
    assert automatic.edit_history[-1]["action"] == "auto_approve"
    assert engine.matches == 1

    history = store.list_history(limit=500)
    assert {item.approval_id for item in history} == {
        "apr_edit",
        "apr_reject",
        "apr_expired",
        "apr_bulk_1",
        "apr_bulk_2",
        "apr_auto",
    }
    assert store.list_pending() == []
    store.clear()
    assert store.list_history(limit=500) == []


def test_postgres_failed_mutation_rolls_back(tmp_path: Path) -> None:
    store = PostgresApprovalStore(
        database_url=f"sqlite:///{tmp_path / 'rollback.sqlite3'}",
        create_tables=True,
    )
    store.create(_request("stable"))

    def _fail(items):
        items["apr_partial"] = _request("partial")
        raise RuntimeError("forced rollback")

    with pytest.raises(RuntimeError, match="forced rollback"):
        store._mutate(_fail)

    assert store.get("apr_stable") is not None
    assert store.get("apr_partial") is None


def test_migration_merges_both_current_heads() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "db/migrations/versions/20260905_022_approval_center_snapshots.py"
    )
    spec = importlib.util.spec_from_file_location("approval_center_migration", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.revision == "20260905_022_approval_center_snapshots"
    assert set(module.down_revision) == {
        "20260823_021_collaboration_events",
        "20260815_020_governed_orchestrator_state",
    }


def test_backend_status_is_redacted_and_read_only(monkeypatch, tmp_path: Path) -> None:
    from auto_client_acquisition.approval_center import approval_store_backend_status

    database_url = f"sqlite:///{tmp_path / 'status.sqlite3'}"
    PostgresApprovalStore(database_url=database_url, create_tables=True)
    monkeypatch.setenv("DEALIX_APPROVAL_STORE_BACKEND", "postgres")
    monkeypatch.setenv("DEALIX_APPROVAL_DATABASE_URL", database_url)

    receipt = approval_store_backend_status()
    assert receipt == {
        "verdict": "PASS",
        "backend": "postgres",
        "process_scoped": False,
        "database_url_configured": True,
        "schema_ready": True,
        "reason": "approval_center_postgres_ready",
    }
    assert database_url not in repr(receipt)


def test_read_only_verifier_never_prints_database_url(monkeypatch, tmp_path: Path, capsys) -> None:
    from scripts.verify_approval_center_backend import main

    database_url = f"sqlite:///{tmp_path / 'verifier.sqlite3'}"
    PostgresApprovalStore(database_url=database_url, create_tables=True)
    monkeypatch.setenv("DEALIX_APPROVAL_STORE_BACKEND", "postgres")
    monkeypatch.setenv("DEALIX_APPROVAL_DATABASE_URL", database_url)
    monkeypatch.setattr("sys.argv", ["verify_approval_center_backend.py", "--json"])

    assert main() == 0
    output = capsys.readouterr().out
    assert '"verdict": "PASS"' in output
    assert '"read_only": true' in output
    assert database_url not in output
