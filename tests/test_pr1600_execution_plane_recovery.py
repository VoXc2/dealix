from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "recover_and_accept_pr1600.sh"
ACCEPTANCE = ROOT / "scripts" / "ops" / "run_pr1600_live_full_acceptance.sh"


def _text() -> str:
    assert SCRIPT.is_file()
    return SCRIPT.read_text(encoding="utf-8")


def _acceptance_text() -> str:
    assert ACCEPTANCE.is_file()
    return ACCEPTANCE.read_text(encoding="utf-8")


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


def test_recovery_is_observe_only_for_live_control_plane() -> None:
    text = _text()
    assert "control_plane_mutation=false" in text
    assert "CONTROL_PLANE_MUTATION=false" in text
    assert "observed_only=true" in text
    assert "install_dealix_self_hosted_runner.sh" not in text
    assert "install_dealix_vps_issue_bridge.sh" not in text
    assert "--bootstrap" not in text
    assert 'systemctl stop "$BRIDGE_TIMER"' not in text
    assert 'systemctl start "$BRIDGE_TIMER"' not in text
    assert 'systemctl start "$BRIDGE_SERVICE"' not in text
    assert 'install -m 0750 -o "$RUN_USER"' not in text
    assert 'cp -a "$INSTALLED_BRIDGE"' not in text


def test_recovery_accepts_exact_head_before_runner_or_bridge_health_checks() -> None:
    text = _text()
    acceptance_pos = text.index('bash "$ACCEPTANCE"')
    runner_pos = text.index('"$RUNNER_DIR/svc.sh" status')
    bridge_pos = text.index('systemctl is-active "$BRIDGE_TIMER"')
    assert acceptance_pos < runner_pos < bridge_pos
    assert "PR1600_EXACT_HEAD_ACCEPTANCE=PASS" in text
    assert "SELF_HOSTED_RUNNER=PASS observed_only=true" in text
    assert "ISSUE_BRIDGE=PASS observed_only=true" in text


def test_unhealthy_control_plane_requires_action_bound_l5_instead_of_repair() -> None:
    text = _text()
    assert "RUNNER_REPAIR_REQUIRES_ACTION_BOUND_L5" in text
    assert "BRIDGE_REPAIR_REQUIRES_ACTION_BOUND_L5" in text
    assert "DEPLOY_EXECUTED=false" in text


def test_recovery_requires_acceptance_receipt_and_stable_head() -> None:
    text = _text()
    assert "RESULT=PR1600_CURRENT_EXACT_FULL_PASS" in text
    assert "EXACT_HEAD_STABILITY=PASS" in text
    assert "RESULT=PR1600_EXECUTION_PLANE_HEALTHY_AND_EXACT_HEAD_ACCEPTED" in text
    assert "PRODUCTION_GREEN=false" in text


def test_exact_head_acceptance_uses_nonpersistent_gh_git_credentials() -> None:
    text = _acceptance_text()
    assert 'GIT_REMOTE="https://github.com/${REPOSITORY}.git"' in text
    assert "credential.helper=!gh auth git-credential" in text
    assert "gh auth setup-git" not in text
    assert "as_dealix gh auth status" in text
    assert "GH_FOUNDER_AUTH_MISMATCH" in text
    assert 'git_repo fetch "$GIT_REMOTE" "+refs/heads/main:refs/remotes/origin/main"' in text
    assert 'git_repo fetch "$GIT_REMOTE" "+refs/pull/$PR/head:$REF"' in text