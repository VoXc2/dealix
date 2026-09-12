from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINEER = (ROOT / "scripts/ops/dealix_project_engineer.sh").read_text(encoding="utf-8")
INSTALLER = (ROOT / "scripts/ops/install_dealix_project_engineer.sh").read_text(encoding="utf-8")


def test_no_l5_commands():
    forbidden = [
        "gh pr merge",
        "railway up",
        "railway redeploy",
        "AUTO_SEND_ENABLED=true",
        "WHATSAPP_ALLOW_LIVE_SEND=true",
        "DEALIX_AUTO_MERGE=true",
    ]
    for token in forbidden:
        assert token not in ENGINEER


def test_engineer_uses_dealix_user_and_exact_pr_head():
    assert "exec sudo -iu dealix env" in ENGINEER
    assert 'head="$(jq -r' in ENGINEER
    assert 'git -C "$REPO" worktree add --detach "$worktree" "$head"' in ENGINEER


def test_manual_engineer_defaults_to_review_only():
    assert 'AUTOBUILD="${DEALIX_ENGINEER_AUTOBUILD:-0}"' in ENGINEER
    assert 'AUTOBUILD="${DEALIX_ENGINEER_AUTOBUILD:-1}"' not in ENGINEER


def test_hermes_is_network_and_credential_sandboxed():
    assert "IPAddressDeny=any" in ENGINEER
    assert "IPAddressAllow=localhost" in ENGINEER
    assert "InaccessiblePaths=/home/dealix/.config/gh /home/dealix/.ssh /home/dealix/.railway" in ENGINEER
    assert "ProtectSystem=strict" in ENGINEER


def test_installer_daily_timer_is_review_only_and_no_merge():
    assert "OnCalendar=*-*-* 20:30:00 Asia/Riyadh" in INSTALLER
    assert 'Environment="DEALIX_ENGINEER_AUTOBUILD=0"' in INSTALLER
    assert 'Environment="DEALIX_AUTO_MERGE=false"' in INSTALLER
    assert "AUTOBUILD is an explicit later opt-in" in INSTALLER
    assert "User=dealix" in INSTALLER


def test_build_pr_cli_uses_valid_target_and_usage():
    assert 'build_pr "$TARGET_PR"' in ENGINEER
    assert "TARGET_PRR" not in ENGINEER
    assert "{status|daily|review-pr PR|build-pr PR}" in ENGINEER


def test_post_edit_guard_covers_live_send_and_main_push():
    assert "WHATSAPP_ALLOW_LIVE_SEND[[:space:]]*=[[:space:]]*true" in ENGINEER
    assert "WHATSAP‚ALOW" not in ENGINEER
    assert "push.*[[:space:]]+main" in ENGINEER


def test_missing_or_prestep_ci_fails_closed():
    assert "no exact-head check evidence was returned; fail closed" in ENGINEER
    assert "only pre-step or unverifiable execution evidence" in ENGINEER
    assert "failed_run_step_triage" in ENGINEER
    assert "steps[]?" in ENGINEER


def test_review_threads_and_main_drift_fail_closed():
    assert "review-thread evidence could not be retrieved; fail closed" in ENGINEER
    assert "current-main comparison could not be verified; fail closed" in ENGINEER
    assert "PR head is behind current main" in ENGINEER


def test_review_pr_initializes_pr_before_packet_path():
    review = ENGINEER.split("review_pr() {", 1)[1].split("changed_files_for_pr()", 1)[0]
    assert 'local pr="$1"\n  local packet="${RUN_DIR}/PR_${pr}_MERGE_PACKET.md"' in review
    assert 'local pr="$1" packet="${RUN_DIR}/PR_${pr}_MERGE_PACKET.md"' not in review
