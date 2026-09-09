import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
WEB_PACKAGE = ROOT / "apps" / "web" / "package.json"


def _workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_ci_runs_full_push_only_on_main_and_prs_into_main():
    text = _workflow_text()
    header = text.split("permissions:", 1)[0]

    assert "push:\n    branches:\n      - main" in header
    assert "pull_request:\n    branches:\n      - main" in header

    for duplicate_branch_trigger in [
        "dealix-v3-autonomous-revenue-os",
        "'copilot/**'",
        "'feat/**'",
        "'fix/**'",
        "'chore/**'",
        "'claude/**'",
        "'release/**'",
    ]:
        assert duplicate_branch_trigger not in header


def test_ci_keeps_superseded_revision_cancellation():
    text = _workflow_text()

    assert "github.event.pull_request.number || github.ref" in text
    assert "cancel-in-progress: true" in text


def test_ci_consolidates_web_validation_without_repeating_typecheck_or_build():
    text = _workflow_text()
    package = json.loads(WEB_PACKAGE.read_text(encoding="utf-8"))

    assert package["scripts"]["verify"] == "npm run typecheck && npm run build"
    assert "web-build:" in text
    assert "frontend-build:" not in text
    assert text.count("working-directory: apps/web") == 1
    assert text.count("run: npm ci") == 1
    assert text.count("run: npm run verify") == 1
    assert "run: npm run typecheck" not in text
    assert "run: npm run build" not in text


def test_ci_preserves_core_trust_jobs_and_doctrine_guards():
    text = _workflow_text()

    for required_job in [
        "python-checks:",
        "web-build:",
        "railway-docker-builds:",
        "live-railway-smoke:",
    ]:
        assert required_job in text

    for required_gate in [
        "python scripts/check_env_contract.py",
        "python scripts/verify_railway_surfaces.py",
        "python scripts/check_no_secrets.py",
        "tests/test_no_cold_whatsapp.py",
        "tests/test_no_guaranteed_claims.py",
        "tests/test_no_linkedin_automation.py",
        "--cov-fail-under=30",
        "docker build -t dealix-api-ci .",
        "docker build -t dealix-apps-web-ci apps/web",
    ]:
        assert required_gate in text


def test_live_railway_smoke_remains_explicit_only():
    text = _workflow_text()

    assert "workflow_dispatch:" in text
    assert "if: github.event_name == 'workflow_dispatch'" in text
    assert "python scripts/railway_smoke_matrix.py" in text


def test_ci_does_not_hide_changes_with_path_ignore():
    text = _workflow_text()

    assert "paths-ignore:" not in text
