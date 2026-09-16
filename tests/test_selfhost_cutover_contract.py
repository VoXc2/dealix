from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_selfhost_cutover_contract() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/ops/verify_selfhost_production_cutover_contract.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SELFHOST_CUTOVER_CONTRACT=PASS" in result.stdout


def test_single_runnable_selfhost_plane() -> None:
    """deploy/selfhost/compose.yml is the only runnable plane; the retired
    stack must not define any runnable service."""
    canonical = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    retired = (ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    assert "services: {}" in retired
    assert "container_name: dealix" not in retired
    assert "api:" in canonical and "web:" in canonical
    assert "127.0.0.1:${DEALIX_SELFHOST_API_PORT" in canonical
    assert "127.0.0.1:${DEALIX_SELFHOST_WEB_PORT" in canonical


def test_exact_sha_and_explicit_cutover_gates() -> None:
    """Exact full-SHA gates plus explicit flags; no silent cutover path."""
    canary = (ROOT / "scripts/ops/deploy_selfhosted_canary.sh").read_text(encoding="utf-8")
    rollback = (ROOT / "scripts/ops/selfhost_release_rollback.sh").read_text(encoding="utf-8")
    migrate = (ROOT / "scripts/ops/migrate_railway_backup_to_selfhost.py").read_text(encoding="utf-8")
    assert "DEALIX_EXPECTED_SHA" in canary
    assert "exact-head mismatch" in canary
    assert "[0-9a-f]{40}" in rollback
    assert "DEALIX_DB_MIGRATION" in migrate
    assert "PUBLIC_CUTOVER=NOT_EXECUTED" in canary


def test_no_production_secrets_in_repo() -> None:
    """Real .env.prod is never tracked; only the CHANGE_ME template ships."""
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    assert ".env.prod" not in tracked
    assert ".env.prod.example" in tracked
    template = (ROOT / ".env.prod.example").read_text(encoding="utf-8")
    assert "CHANGE_ME" in template


def test_canonical_compose_fails_closed_without_release_identity() -> None:
    compose = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    assert "DEALIX_GIT_SHA:?set exact DEALIX_GIT_SHA" in compose
    assert "DEALIX_IMAGE_TAG:?set exact DEALIX_IMAGE_TAG" in compose
    assert "DEALIX_GIT_SHA:-unknown" not in compose


def test_application_rollback_uses_only_canonical_compose() -> None:
    rollback = (ROOT / "scripts/ops/selfhost_release_rollback.sh").read_text(encoding="utf-8")
    assert "deploy/selfhost/compose.yml" in rollback
    assert "docker-compose.prod.yml" not in rollback
    assert "DEALIX_GIT_SHA" in rollback
    assert "DEALIX_IMAGE_TAG" in rollback
    assert "database_rollback=NEVER" in rollback


def test_single_canonical_graph_contains_safe_public_cutover_profile() -> None:
    compose = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    assert 'profiles: ["public-cutover"]' in compose
    assert "${DEALIX_PUBLIC_HTTP_BIND:-127.0.0.1:18080}:80" in compose
    assert "${DEALIX_PUBLIC_HTTPS_BIND:-127.0.0.1:18443}:443" in compose
    assert "../../ops/caddy/Caddyfile:/etc/caddy/Caddyfile:ro" in compose
    assert '"80:80"' not in compose
    assert '"443:443"' not in compose


def test_public_cutover_controller_is_explicitly_action_gated() -> None:
    source = (ROOT / "scripts/ops/selfhost_public_cutover.sh").read_text(encoding="utf-8")
    for needle in ("DEALIX_EXPECTED_SHA", "CONFIRM_SHA", "DEALIX_STAGE_PRODUCTION", "DEALIX_PUBLIC_CUTOVER", "DEALIX_L5_APPROVAL_ACTION", "dealix-production-stage-v1:", "dealix-public-cutover-v1:", "0.0.0.0:80", "0.0.0.0:443"):
        assert needle in source
    assert "DNS_MUTATION=NOT_EXECUTED" in source
    assert "PRODUCTION_GREEN=NOT_PROVEN" in source
    assert "railway up" not in source
    assert "railway redeploy" not in source


def test_canonical_database_profile_is_passworded_and_loopback_only() -> None:
    compose = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    assert 'profiles: ["local-db", "production-db"]' in compose
    assert "POSTGRES_PASSWORD:" in compose
    assert "POSTGRES_HOST_AUTH_METHOD: trust" not in compose
    assert "127.0.0.1:${DEALIX_SELFHOST_DB_PORT:-15432}:5432" in compose
    assert "0.0.0.0:${DEALIX_SELFHOST_DB_PORT" not in compose
    assert "dealix-postgres-data:/var/lib/postgresql" in compose
    assert "dealix-postgres-data:/var/lib/postgresql/data" not in compose


def test_railway_migration_requires_restored_backup_and_exact_release() -> None:
    source = (ROOT / "scripts/ops/migrate_railway_backup_to_selfhost.py").read_text(encoding="utf-8")
    for needle in (
        "DEALIX_SOURCE_IS_RESTORED_BACKUP",
        "DEALIX_RAILWAY_BACKUP_SHA256",
        "DEALIX_TARGET_RELEASE_SHA",
        "DEALIX_L5_APPROVAL_ACTION",
        "default_transaction_read_only",
        "LIVE_PROVIDER_HOST_MARKERS",
        "dealix.railway-data-migration-receipt.v1",
    ):
        assert needle in source
    assert "must not point at live Railway infrastructure" in source


def test_backup_and_quiescence_are_receipt_bound() -> None:
    backup = (ROOT / "scripts/ops/backup_postgres_snapshot.sh").read_text(encoding="utf-8")
    quiet = (ROOT / "scripts/ops/verify_railway_source_quiescence.sh").read_text(encoding="utf-8")
    receipts = (ROOT / "scripts/ops/verify_selfhost_cutover_receipts.py").read_text(encoding="utf-8")
    for needle in (
        "DEALIX_BACKUP_ROLE",
        "database_changed_during_backup_capture",
        "dealix.railway-source-backup-receipt.v1",
        "dealix.selfhost-backup-receipt.v1",
        "information_schema.columns",
        "required_column",
    ):
        assert needle in backup
    assert "migration_count proof_events evidence_source" in backup
    assert "RAILWAY_QUIESCENCE=PASS" in quiet
    assert "source receipt outside 30-minute cutover window" in quiet
    assert "dealix.railway-quiescence-receipt.v1" in quiet
    assert "SELFHOST_CUTOVER_RECEIPTS=PASS" in receipts
    assert "scratch migration receipt cannot authorize cutover" in receipts
    assert "quiescence proof must follow migration and target backup" in receipts


def test_production_database_preparation_is_separate_l5_gate() -> None:
    source = (ROOT / "scripts/ops/selfhost_prepare_production_database.sh").read_text(encoding="utf-8")
    for needle in ("--preflight", "--execute", "DEALIX_PREPARE_PRODUCTION_DB", "DEALIX_BOOTSTRAP_PRODUCTION_DB", "CONFIRM_SHA", "DEALIX_L5_APPROVAL_ACTION", "dealix-production-db-prepare-v1:"):
        assert needle in source
    assert "PRODUCTION_DB_MUTATION=NOT_EXECUTED" in source
    assert "RAILWAY_DATA_MIGRATION=NOT_EXECUTED" in source
    assert "PUBLIC_CUTOVER=NOT_EXECUTED" in source


def test_public_cutover_requires_complete_receipt_chain_before_public_bind() -> None:
    source = (ROOT / "scripts/ops/selfhost_public_cutover.sh").read_text(encoding="utf-8")
    for needle in (
        "DEALIX_DATA_MIGRATION_RECEIPT",
        "DEALIX_SOURCE_BACKUP_RECEIPT",
        "DEALIX_SELFHOST_BACKUP_RECEIPT",
        "DEALIX_QUIESCENCE_RECEIPT",
        "verify_selfhost_cutover_receipts.py",
        "RAILWAY_DECOMMISSION=NOT_EXECUTED",
    ):
        assert needle in source
    verify_at = source.index("verify_selfhost_cutover_receipts.py")
    public_bind_at = source.index('DEALIX_PUBLIC_HTTP_BIND="0.0.0.0:80"')
    assert verify_at < public_bind_at
    assert "production cutover DB must be canonical self-host postgres" in source


def test_database_credentials_never_travel_in_process_argv() -> None:
    prepare = (ROOT / "scripts/ops/selfhost_prepare_production_database.sh").read_text(encoding="utf-8")
    cutover = (ROOT / "scripts/ops/selfhost_public_cutover.sh").read_text(encoding="utf-8")
    for source in (prepare, cutover):
        assert 'python3 - "$DEALIX_DATABASE_URL"' not in source
        assert 'os.environ["DEALIX_DATABASE_URL"]' in source
        assert 'os.environ["POSTGRES_USER"]' in source
        assert 'os.environ["POSTGRES_DB"]' in source


def test_material_selfhost_actions_are_exact_action_bound() -> None:
    prepare = (ROOT / "scripts/ops/selfhost_prepare_production_database.sh").read_text(encoding="utf-8")
    cutover = (ROOT / "scripts/ops/selfhost_public_cutover.sh").read_text(encoding="utf-8")
    assert 'PREPARE_ACTION_ID="dealix-production-db-prepare-v1:${EXPECTED_SHA}"' in prepare
    assert '${DEALIX_L5_APPROVAL_ACTION:-}' in prepare
    assert 'ACTION_ID="dealix-production-stage-v1:${EXPECTED_SHA}"' in cutover
    assert 'ACTION_ID="dealix-public-cutover-v1:${EXPECTED_SHA}"' in cutover
    assert '${DEALIX_L5_APPROVAL_ACTION:-}' in cutover
