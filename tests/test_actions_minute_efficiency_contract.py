"""Regression guards for CI cost controls that must not weaken release/security gates."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_client_acquisition_pr_trigger_matches_bounded_product_paths() -> None:
    workflow = read(".github/workflows/client-acquisition-delivery-check.yml")
    assert workflow.count('branches: [main]') == 2
    assert workflow.count('apps/web/app/client-acquisition/**') == 2
    assert workflow.count('business/acquisition/**') == 2
    assert workflow.count('scripts/verify_client_acquisition_delivery_os.py') >= 3
    assert "cancel-in-progress: true" in workflow


def test_expensive_broad_checks_cancel_superseded_pr_runs() -> None:
    for path in [
        ".github/workflows/enterprise-control-plane.yml",
        ".github/workflows/global-ai-transformation.yml",
        ".github/workflows/dealix-ultimate-os-check.yml",
    ]:
        workflow = read(path)
        assert "pull_request:" in workflow, path
        assert "push:" in workflow, path
        assert "concurrency:" in workflow, path
        assert "cancel-in-progress: true" in workflow, path
        assert "runs-on: ubuntu-latest" in workflow, path


def test_docker_and_no_crash_keep_stable_required_context_names() -> None:
    expected = {
        ".github/workflows/docker-build.yml": "Docker Build & Scan",
        ".github/workflows/no-crash-launch-guard.yml": "No-Crash Launch Guard",
    }
    for path, job_name in expected.items():
        workflow = read(path)
        assert f"name: {job_name}" in workflow, path
        jobs = workflow.split("jobs:", 1)[1]
        assert f"name: {job_name}" in jobs, path
        assert "runs-on: ubuntu-latest" in jobs, path


def test_security_workflows_are_not_removed_or_disabled() -> None:
    for path in [
        ".github/workflows/security.yml",
        ".github/workflows/codeql.yml",
    ]:
        assert (ROOT / path).is_file(), path
