"""Railway production config-as-code checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from dealix.commercial_ops.railway_production import (
    _has_canonical_predeploy,
    analyze_railway_production,
    classify_release_evidence,
    parse_railway_ui_drift_hint,
    parse_railway_ui_predeploy_drift,
    parse_railway_ui_restart_retries_drift,
)

ROOT = Path(__file__).resolve().parents[1]


def test_repo_railway_config_ok() -> None:
    blob = analyze_railway_production(api_base=False)
    assert blob["repo"]["ok"], blob["repo"]["issues"]
    assert blob["verdict"] == "PASS"


def test_ui_start_command_drift_hint() -> None:
    hint = parse_railway_ui_drift_hint("./start.sh")
    assert hint is not None
    assert "/app/start.sh" in hint


def test_ui_predeploy_drift_no_migration_stub() -> None:
    hint = parse_railway_ui_predeploy_drift('echo "no migration needed"')
    assert hint is not None
    assert "railway_predeploy" in hint


def test_ui_predeploy_legacy_sh_is_rejected() -> None:
    hint = parse_railway_ui_predeploy_drift("sh /app/scripts/railway_predeploy.sh")
    assert hint is not None
    assert "bash /app/scripts/railway_predeploy.sh" in hint


def test_ui_restart_retries_drift_from_uploaded_snapshot() -> None:
    hint = parse_railway_ui_restart_retries_drift("10")
    assert hint is not None
    assert "10" in hint
    assert "3" in hint


def test_ui_restart_retries_canonical_value_has_no_drift() -> None:
    assert parse_railway_ui_restart_retries_drift("3") is None


def test_analyze_skips_live_when_api_base_false() -> None:
    blob = analyze_railway_production(api_base=False)
    assert blob["live_healthz"].get("probed") is False


def _run_verify_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "verify_railway_production_config.py"),
            *args,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_verify_cli_skip_live_does_not_probe_production() -> None:
    proc = _run_verify_cli("--skip-live")
    assert proc.returncode == 0, proc.stderr
    assert "live /healthz: skipped" in proc.stdout
    assert "RAILWAY_PRODUCTION_CONFIG_VERDICT=PASS" in proc.stdout


def test_verify_cli_ui_drift_cannot_report_false_pass() -> None:
    proc = _run_verify_cli(
        "--skip-live",
        "--ui-restart-max-retries",
        "10",
    )
    assert proc.returncode == 0, proc.stderr
    assert "FOUNDER_ACTION (restart)" in proc.stdout
    assert "RAILWAY_PRODUCTION_CONFIG_VERDICT=WARN" in proc.stdout


def test_predeploy_predicate_requires_parsed_exact_array_wrapper() -> None:
    assert _has_canonical_predeploy((ROOT / "railway.toml").read_text(encoding="utf-8"))
    assert _has_canonical_predeploy((ROOT / "railway.json").read_text(encoding="utf-8"))

    deceptive = "sh /app/scripts/railway_predeploy.sh # bash /app/scripts/railway_predeploy.sh"
    assert not _has_canonical_predeploy(
        f'[deploy]\npreDeployCommand = ["{deceptive}"]\n'
    )
    assert not _has_canonical_predeploy(
        '{"deploy":{"preDeployCommand":["' + deceptive + '"]}}'
    )


def test_predeploy_predicate_rejects_legacy_string_schema() -> None:
    direct = "bash /app/scripts/railway_predeploy.sh"
    assert not _has_canonical_predeploy(
        f'[deploy]\npreDeployCommand = "{direct}"\n'
    )
    assert not _has_canonical_predeploy(
        '{"deploy":{"preDeployCommand":"' + direct + '"}}'
    )


def test_ui_predeploy_legacy_sh_is_drift() -> None:
    hint = parse_railway_ui_predeploy_drift("sh /app/scripts/railway_predeploy.sh")
    assert hint is not None
    assert "bash /app/scripts/railway_predeploy.sh" in hint


def test_ui_predeploy_comment_smuggling_is_drift() -> None:
    hint = parse_railway_ui_predeploy_drift(
        "sh /app/scripts/railway_predeploy.sh # bash /app/scripts/railway_predeploy.sh"
    )
    assert hint is not None
    assert "bash /app/scripts/railway_predeploy.sh" in hint


def test_ui_predeploy_canonical_bash_has_no_drift() -> None:
    assert parse_railway_ui_predeploy_drift("bash /app/scripts/railway_predeploy.sh") is None


def test_github_success_cannot_promote_skipped_railway_deployment() -> None:
    evidence = classify_release_evidence(
        github_context_state="success",
        railway_deployment_status="SKIPPED",
    )
    assert evidence["github_context_is_release_authority"] is False
    assert evidence["provider_deployment_success"] is False
    assert evidence["release_evidence_valid"] is False
    assert evidence["reason"] == "RAILWAY_DEPLOYMENT_SKIPPED_NOT_RELEASE_EVIDENCE"


def test_github_success_cannot_promote_failed_railway_deployment() -> None:
    evidence = classify_release_evidence(
        github_context_state="success",
        railway_deployment_status="FAILED",
    )
    assert evidence["release_evidence_valid"] is False
    assert evidence["reason"] == "RAILWAY_DEPLOYMENT_NOT_SUCCESS:FAILED"


def test_missing_railway_status_fails_closed() -> None:
    evidence = classify_release_evidence(
        github_context_state="success",
        railway_deployment_status=None,
    )
    assert evidence["release_evidence_valid"] is False
    assert evidence["reason"] == "RAILWAY_DEPLOYMENT_STATUS_MISSING"


def _bound_success(**overrides: str) -> dict[str, object]:
    kwargs = {
        "github_context_state": "failure",
        "railway_deployment_status": "SUCCESS",
        "expected_deployment_id": "dep-123",
        "observed_deployment_id": "dep-123",
        "expected_service_id": "svc-123",
        "observed_service_id": "svc-123",
        "expected_environment_id": "env-123",
        "observed_environment_id": "env-123",
        "expected_sha": "a" * 40,
        "deployed_sha": "a" * 40,
        "live_sha": "a" * 40,
    }
    kwargs.update(overrides)
    return classify_release_evidence(**kwargs)


def test_railway_success_is_release_evidence_only_when_identity_bound() -> None:
    evidence = _bound_success()
    assert evidence["github_context_is_release_authority"] is False
    assert evidence["provider_deployment_success"] is True
    assert evidence["identity_binding_complete"] is True
    assert evidence["identity_binding_valid"] is True
    assert evidence["release_evidence_valid"] is True
    assert evidence["reason"] == "RAILWAY_DEPLOYMENT_SUCCESS"


def test_railway_success_without_identity_binding_fails_closed() -> None:
    evidence = classify_release_evidence(
        github_context_state="failure",
        railway_deployment_status="success",
    )
    assert evidence["provider_deployment_success"] is True
    assert evidence["identity_binding_complete"] is False
    assert evidence["release_evidence_valid"] is False
    assert evidence["reason"] == "RAILWAY_SUCCESS_IDENTITY_BINDING_INCOMPLETE"


def test_railway_success_from_other_deployment_fails_closed() -> None:
    evidence = _bound_success(observed_deployment_id="dep-old")
    assert evidence["identity_binding_valid"] is False
    assert evidence["release_evidence_valid"] is False
    assert evidence["reason"] == "RAILWAY_SUCCESS_IDENTITY_MISMATCH"


def test_railway_success_with_stale_live_sha_fails_closed() -> None:
    evidence = _bound_success(live_sha="b" * 40)
    assert evidence["identity_binding_valid"] is False
    assert evidence["release_evidence_valid"] is False
    assert evidence["reason"] == "RAILWAY_SUCCESS_IDENTITY_MISMATCH"
