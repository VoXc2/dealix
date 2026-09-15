from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts/ops/selfhost_canary_project_name.sh"
WRAPPER = ROOT / "scripts/ops/run_selfhosted_private_release_canary.sh"
DEPLOY = ROOT / "scripts/ops/deploy_selfhosted_canary.sh"
INGRESS = ROOT / "scripts/ops/verify_selfhosted_ingress_canary.sh"


def _run(args: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _field(output: str, key: str) -> str:
    prefix = f"{key}="
    return next(line[len(prefix):] for line in output.splitlines() if line.startswith(prefix))


def test_same_sha_canaries_get_distinct_project_names() -> None:
    sha = "a" * 40
    a = _run(["bash", str(HELPER), sha, "run-a"])
    b = _run(["bash", str(HELPER), sha, "run-b"])
    assert a.returncode == b.returncode == 0
    assert a.stdout.strip() == "dealix-selfhost-aaaaaaaaaaaa-run-a"
    assert b.stdout.strip() == "dealix-selfhost-aaaaaaaaaaaa-run-b"
    assert a.stdout != b.stdout
def test_invalid_run_ids_fail_closed() -> None:
    sha = "b" * 40
    for run_id in ("", "Bad", "bad_id", "x" * 25):
        result = _run(["bash", str(HELPER), sha, run_id])
        assert result.returncode != 0
        assert "HOLD:" in result.stderr


def test_low_level_runners_require_shared_run_id() -> None:
    for path in (DEPLOY, INGRESS):
        text = path.read_text(encoding="utf-8")
        assert "DEALIX_CANARY_RUN_ID" in text
        assert "selfhost_canary_project_name.sh" in text
        assert "dealix_canary_project_name" in text
        assert "run_selfhosted_private_release_canary.sh" in text



def test_invalid_run_id_cannot_be_masked_by_export_builtin() -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    env = os.environ.copy()
    env["DEALIX_EXPECTED_SHA"] = sha
    env["DEALIX_CANARY_RUN_ID"] = "x" * 25
    env["DEALIX_CANARY_PLAN_ONLY"] = "1"

    wrapper = _run(["bash", str(WRAPPER)], env=env)
    assert wrapper.returncode != 0
    assert "HOLD: DEALIX_CANARY_RUN_ID" in wrapper.stderr
    assert "CANARY_PLAN_ONLY=PASS" not in wrapper.stdout

    for runner in (DEPLOY, INGRESS):
        result = _run(["bash", str(runner)], env=env)
        assert result.returncode != 0
        assert "HOLD: DEALIX_CANARY_RUN_ID" in result.stderr


def test_project_name_validation_status_is_not_hidden_by_export() -> None:
    for path in (WRAPPER, DEPLOY, INGRESS):
        text = path.read_text(encoding="utf-8")
        assert 'export COMPOSE_PROJECT_NAME="$(dealix_canary_project_name' not in text
        assert 'COMPOSE_PROJECT_NAME="$(dealix_canary_project_name' in text
        assert "export COMPOSE_PROJECT_NAME" in text

def test_wrapper_plan_only_is_unique_and_has_unique_ports() -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    env = os.environ.copy()
    env["DEALIX_EXPECTED_SHA"] = sha
    env["DEALIX_CANARY_PLAN_ONLY"] = "1"
    env.pop("DEALIX_CANARY_RUN_ID", None)

    first = _run(["bash", str(WRAPPER)], env=env)
    second = _run(["bash", str(WRAPPER)], env=env)
    assert first.returncode == second.returncode == 0
    assert "CANARY_PLAN_ONLY=PASS" in first.stdout
    assert "CANARY_PLAN_ONLY=PASS" in second.stdout
    assert _field(first.stdout, "COMPOSE_PROJECT_NAME") != _field(second.stdout, "COMPOSE_PROJECT_NAME")
    for output in (first.stdout, second.stdout):
        ports = _field(output, "PORTS").split(",")
        assert len(ports) == 4
        assert len(set(ports)) == 4
def test_production_project_namespace_is_not_canary_scoped() -> None:
    prepare = (ROOT / "scripts/ops/selfhost_prepare_production_database.sh").read_text(encoding="utf-8")
    cutover = (ROOT / "scripts/ops/selfhost_public_cutover.sh").read_text(encoding="utf-8")
    for source in (prepare, cutover):
        assert "DEALIX_CANARY_RUN_ID" not in source
        assert "DEALIX_PRODUCTION_PROJECT_NAME" in source
        assert "dealix-production" in source


def test_wrapper_keeps_private_canary_fail_closed() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    for needle in (
        "DEALIX_CANARY_RUN_ID",
        "DEALIX_CANARY_POSTGRES_PASSWORD",
        "DEALIX_INTERNAL_SURFACE_MODE",
        "down -v --remove-orphans",
        "PRIVATE_RELEASE_CANARY=PASS",
        "PUBLIC_CUTOVER=NOT_EXECUTED",
    ):
        assert needle in text
    assert "0.0.0.0:80" not in text
    assert "0.0.0.0:443" not in text


def test_wrapper_exports_shared_local_db_contract_for_deploy_ingress_and_cleanup() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    for needle in (
        'export POSTGRES_USER="${POSTGRES_USER:-dealix_canary}"',
        'export POSTGRES_DB="${POSTGRES_DB:-dealix_canary}"',
        'export POSTGRES_PASSWORD="$DEALIX_CANARY_POSTGRES_PASSWORD"',
        'export DEALIX_DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}"',
    ):
        assert needle in text
    assert text.index('export DEALIX_DATABASE_URL=') < text.index('bash "$SCRIPT_DIR/deploy_selfhosted_canary.sh"')
    assert text.index('export DEALIX_DATABASE_URL=') < text.index('bash "$SCRIPT_DIR/verify_selfhosted_ingress_canary.sh"')
