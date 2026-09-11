from __future__ import annotations

import os
from pathlib import Path
import subprocess
import textwrap


ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "scripts/ops/dealix_company_autopilot.sh"


def _write_executable(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content), encoding="utf-8")
    path.chmod(0o755)


def _run_production_truth(
    tmp_path: Path,
    *,
    expected_sha: str,
    api_sha: str,
    web_sha: str,
    api_http: str = "200",
    web_http: str = "200",
    branch: str = "main",
    local_sha: str | None = None,
) -> tuple[subprocess.CompletedProcess[str], str]:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    repo = tmp_path / "repo"
    repo.mkdir()
    state_root = tmp_path / "autopilot"

    local_sha = local_sha or expected_sha

    _write_executable(
        fake_bin / "git",
        r'''#!/usr/bin/env bash
        set -euo pipefail
        args="$*"
        case "$args" in
          *" fetch origin main --quiet") exit 0 ;;
          *" branch --show-current") printf '%s\n' "$FAKE_BRANCH" ;;
          *" rev-parse HEAD") printf '%s\n' "$FAKE_LOCAL_SHA" ;;
          *" rev-parse origin/main") printf '%s\n' "$FAKE_EXPECTED_SHA" ;;
          *) echo "unexpected fake git invocation: $args" >&2; exit 90 ;;
        esac
        ''',
    )
    _write_executable(
        fake_bin / "curl",
        r'''#!/usr/bin/env bash
        set -euo pipefail
        url="${!#}"
        if [[ " $* " == *" -w "* ]]; then
          case "$url" in
            "${FAKE_API_BASE%/}/healthz") printf '%s' "$FAKE_API_HTTP" ;;
            "${FAKE_WEB_BASE%/}/") printf '%s' "$FAKE_WEB_HTTP" ;;
            *) printf '404' ;;
          esac
          exit 0
        fi
        case "$url" in
          "${FAKE_API_BASE%/}/version") printf '{"git_sha":"%s"}' "$FAKE_API_SHA" ;;
          "${FAKE_WEB_BASE%/}/healthz") printf '{"status":"ok","git_sha":"%s"}' "$FAKE_WEB_SHA" ;;
          *) exit 22 ;;
        esac
        ''',
    )

    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{fake_bin}:{env['PATH']}",
            "DEALIX_REPO_ROOT": str(repo),
            "DEALIX_AUTOPILOT_ROOT": str(state_root),
            "DEALIX_PUBLIC_API_BASE": "https://api.test",
            "DEALIX_PUBLIC_WEB_BASE": "https://web.test",
            "DEALIX_PYTHON": os.environ.get("DEALIX_PYTHON_BIN", os.sys.executable),
            "FAKE_API_BASE": "https://api.test",
            "FAKE_WEB_BASE": "https://web.test",
            "FAKE_EXPECTED_SHA": expected_sha,
            "FAKE_LOCAL_SHA": local_sha,
            "FAKE_BRANCH": branch,
            "FAKE_API_SHA": api_sha,
            "FAKE_WEB_SHA": web_sha,
            "FAKE_API_HTTP": api_http,
            "FAKE_WEB_HTTP": web_http,
        }
    )
    result = subprocess.run(
        ["bash", str(AUTOPILOT), "production"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    state = (state_root / "state/production.state").read_text(encoding="utf-8").strip()
    return result, state


def test_http_200_with_stale_release_identity_is_hold(tmp_path: Path) -> None:
    expected = "a" * 40
    result, state = _run_production_truth(
        tmp_path,
        expected_sha=expected,
        api_sha="b" * 40,
        web_sha="c" * 40,
    )
    assert result.returncode == 0, result.stderr
    assert state == "HOLD"
    assert "production_reason=running_release_not_equal_current_main" in result.stdout
    assert "PRODUCTION_GREEN=false" in result.stdout


def test_exact_web_api_identity_is_required_for_green(tmp_path: Path) -> None:
    expected = "d" * 40
    result, state = _run_production_truth(
        tmp_path,
        expected_sha=expected,
        api_sha=expected,
        web_sha=expected,
    )
    assert result.returncode == 0, result.stderr
    assert state == "GREEN"
    assert f"expected_main_sha={expected}" in result.stdout
    assert f"api_release_sha={expected}" in result.stdout
    assert f"web_release_sha={expected}" in result.stdout
    assert "PRODUCTION_GREEN=true" in result.stdout


def test_liveness_failure_cannot_preserve_green(tmp_path: Path) -> None:
    expected = "e" * 40
    result, state = _run_production_truth(
        tmp_path,
        expected_sha=expected,
        api_sha=expected,
        web_sha=expected,
        api_http="503",
    )
    assert result.returncode == 0, result.stderr
    assert state == "HOLD"
    assert "production_reason=public_liveness_failed_pending_hysteresis" in result.stdout
    assert "PRODUCTION_GREEN=false" in result.stdout


def test_noncanonical_checkout_is_hold_even_when_public_sha_matches(tmp_path: Path) -> None:
    expected = "f" * 40
    result, state = _run_production_truth(
        tmp_path,
        expected_sha=expected,
        api_sha=expected,
        web_sha=expected,
        branch="feature/test",
    )
    assert result.returncode == 0, result.stderr
    assert state == "HOLD"
    assert "production_reason=canonical_source_not_exact_current_main" in result.stdout


def test_guard_contains_release_identity_invariants() -> None:
    source = AUTOPILOT.read_text(encoding="utf-8")
    assert "/version" in source
    assert "/healthz" in source
    assert "origin/main" in source
    assert "immutable_release_identity_missing" in source
    assert "running_release_not_equal_current_main" in source
    assert 'transition_notify production GREEN "Public API/site probes are responding."' not in source
