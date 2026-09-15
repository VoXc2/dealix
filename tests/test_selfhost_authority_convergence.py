from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_legacy_production_compose_is_fail_closed_history() -> None:
    text = (ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    assert "HISTORICAL_REFERENCE_NON_AUTHORITATIVE" in text
    assert "canonical_compose: deploy/selfhost/compose.yml" in text
    assert "services: {}" in text
    assert "postgres:16" not in text
    assert '"80:80"' not in text
    assert '"443:443"' not in text


def test_legacy_server_entrypoints_refuse_execution() -> None:
    for relative in (
        "scripts/server_deploy.sh",
        "scripts/server_healthcheck.sh",
        "scripts/server_backup.sh",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "SELFHOST_LEGACY_ENTRYPOINT=HOLD" in text
        assert "deploy/selfhost" in text or "SELFHOSTED_PRODUCTION_PLANE.md" in text
        assert "exit 78" in text
        assert "docker compose" not in text


def test_release_engineer_points_at_canonical_selfhost_authority() -> None:
    text = (ROOT / ".agents/skills/dealix/release-engineer/SKILL.md").read_text(encoding="utf-8")
    assert "deploy/selfhost/compose.yml" in text
    assert "python scripts/ops/verify_selfhosted_production_plane.py" in text
    assert "docker compose -f docker-compose.prod.yml config" not in text


def test_current_runbooks_require_exact_sha_and_l5_cutover() -> None:
    plane = (ROOT / "docs/ops/SELFHOSTED_PRODUCTION_PLANE.md").read_text(encoding="utf-8")
    runbook = (ROOT / "docs/ops/SELF_HOSTED_DOCKER_RUNBOOK_AR.md").read_text(encoding="utf-8")
    for text in (plane, runbook):
        assert "DEALIX_EXPECTED_SHA" in text
        assert "deploy/selfhost/compose.yml" in text
        assert "L5" in text
    assert "PRODUCTION_GREEN=NOT_PROVEN" in plane
    assert "DEALIX_SELFHOST_API_PORT" in runbook
    assert "DEALIX_SELFHOST_WEB_PORT" in runbook


def test_canonical_compose_forwards_required_production_auth_env() -> None:
    text = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    for key in ("APP_SECRET_KEY", "JWT_SECRET_KEY", "API_KEYS", "ADMIN_API_KEYS"):
        assert f"{key}: ${{{key}:-}}" in text


def test_pg18_canary_volume_uses_version_aware_parent_mount() -> None:
    text = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    assert "pgvector/pgvector:pg18" in text
    assert "dealix-postgres-canary:/var/lib/postgresql" in text
    assert "dealix-postgres-canary:/var/lib/postgresql/data" not in text
    assert 'profiles: ["local-db"]' in text


def test_pg18_canary_host_auth_requires_runtime_password() -> None:
    compose = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
    runner = (ROOT / "scripts/ops/deploy_selfhosted_canary.sh").read_text(encoding="utf-8")
    assert "POSTGRES_HOST_AUTH_METHOD: trust" not in compose
    assert "POSTGRES_PASSWORD: ${DEALIX_CANARY_POSTGRES_PASSWORD:-}" in compose
    assert "POSTGRES_INITDB_ARGS: --auth-host=scram-sha-256" in compose
    assert "postgresql+asyncpg://dealix_canary@postgres:5432/dealix_canary" not in compose
    assert "DATABASE_URL: ${DEALIX_DATABASE_URL:?set DEALIX_DATABASE_URL}" in compose
    assert 'DEALIX_CANARY_POSTGRES_PASSWORD:?set DEALIX_CANARY_POSTGRES_PASSWORD' in runner
    assert "CANARY_POSTGRES_PASSWORD_CONTRACT=PASS" in runner
    assert "16-128 URL-safe unreserved characters" in runner
