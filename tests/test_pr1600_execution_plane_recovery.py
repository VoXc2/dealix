from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "recover_and_accept_pr1600.sh"


def _text() -> str:
    assert SCRIPT.is_file()
    return SCRIPT.read_text(encoding="utf-8")


def test_recovery_keeps_all_material_actions_disabled() -> None:
    text = _text()
    for token in (
        "DEALIX_EXTERNAL_SEND=0",
        "EMAIL_LIVE_SEND=0",
        "WHATSAPP_OUTBOUND=0",
        "PUBLIC_PUBLISH=0",
        "PAID_SPEND=0",
        "PAYMENT_EXECUTION=0",
        "PRODUCTION_MUTATION=0",
        "RAILWAY_STAGED_APPLY=0",
        "DNS_MUTATION=0",
        "DB_MUTATION=0",
        "SECRET_MUTATION=0",
        "CONTRACT_EXECUTION=0",
        "TENDER_EXECUTION=0",
    ):
        assert token in text

    for forbidden in (
        "gh pr merge",
        "railway up",
        "railway redeploy",
        "git push --force",
        "eval ",
        "curl | bash",
    ):
        assert forbidden not in text


def test_recovery_never_bootstraps_or_reinstalls_issue_bridge() -> None:
    text = _text()
    assert "install_dealix_vps_issue_bridge.sh" not in text
    assert "--bootstrap" not in text
    assert 'BRIDGE_TIMER="dealix-vps-issue-bridge.timer"' in text
    assert 'BRIDGE_SERVICE="dealix-vps-issue-bridge.service"' in text
    assert 'systemctl start "$BRIDGE_SERVICE"' in text


def test_recovery_refreshes_bridge_from_same_source_without_state_reset() -> None:
    text = _text()
    assert 'SOURCE_BRIDGE="$SCRIPT_DIR/dealix_vps_issue_bridge.py"' in text
    assert 'SOURCE_DISPATCHER="$SCRIPT_DIR/dealix_vps_control.sh"' in text
    assert 'INSTALLED_BRIDGE="$CONTROL_BIN/dealix_vps_issue_bridge.py"' in text
    assert 'INSTALLED_DISPATCHER="$CONTROL_BIN/dealix_vps_control.sh"' in text
    assert 'python3 -m py_compile "$SOURCE_BRIDGE"' in text
    assert 'bash -n "$SOURCE_DISPATCHER"' in text
    assert "BRIDGE_INSTALL_DIGEST_MISMATCH" in text
    assert "DISPATCHER_INSTALL_DIGEST_MISMATCH" in text
    assert "state_preserved=true bootstrap=false" in text
    assert "BRIDGE_ALREADY_ACTIVE_REVIEW" in text


def test_recovery_restores_runner_before_bridge_and_exact_head_acceptance() -> None:
    text = _text()
    runner_pos = text.index('bash "$RUNNER_INSTALLER"')
    refresh_pos = text.index('install -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$SOURCE_BRIDGE"')
    bridge_pos = text.index('systemctl start "$BRIDGE_SERVICE"')
    acceptance_pos = text.index('bash "$ACCEPTANCE"')
    assert runner_pos < refresh_pos < bridge_pos < acceptance_pos
    assert "SELF_HOSTED_RUNNER=PASS" in text
    assert "BRIDGE_SOURCE_REFRESH=PASS" in text
    assert "ISSUE_BRIDGE=PASS" in text
    assert "PR1600_EXACT_HEAD_ACCEPTANCE=PASS" in text


def test_recovery_requires_acceptance_receipt_and_stable_head() -> None:
    text = _text()
    assert "RESULT=PR1600_CURRENT_EXACT_FULL_PASS" in text
    assert "EXACT_HEAD_STABILITY=PASS" in text
    assert "RESULT=PR1600_EXECUTION_PLANE_RECOVERED_AND_EXACT_HEAD_ACCEPTED" in text
    assert "PRODUCTION_GREEN=false" in text
