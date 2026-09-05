from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "scripts" / "ops" / "dealix_sovereign_adapter.py"
INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_sovereign_adapter.sh"
CONTROL = ROOT / "scripts" / "ops" / "dealix_vps_control.sh"


def test_adapter_delegates_verification_to_canonical_contract():
    text = ADAPTER.read_text(encoding="utf-8")
    assert '["bin/dealix", "verify", mode]' in text
    for needle in [
        "scripts/security_smoke.py",
        "check_alembic_single_head.py",
        "pytest -q",
        "boot_acceptance.sh",
    ]:
        assert needle not in text


def test_pr_execution_is_trusted_same_repo_only():
    text = ADAPTER.read_text(encoding="utf-8")
    assert 'TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}' in text
    assert "head_repo == REPO_SLUG" in text
    assert "if not trusted_pr(pr)" in text
    assert 'VERIFY_PR=BLOCKED_UNTRUSTED' in text
    assert 'VERIFY_PR=HEAD_RACE' in text


def test_manual_canary_surface_is_bounded_to_main_or_numeric_pr():
    text = ADAPTER.read_text(encoding="utf-8")
    assert 'sub.add_parser("verify-main")' in text
    assert 'p_verify = sub.add_parser("verify-pr")' in text
    assert 'p_verify.add_argument("pr", type=int)' in text
    assert 'return manual_verify_pr(args.pr)' in text
    assert 'return manual_verify_main()' in text
    assert 'add_argument("ref"' not in text
    assert 'add_argument("sha"' not in text


def test_runner_environment_does_not_inherit_credentials_or_real_home():
    text = ADAPTER.read_text(encoding="utf-8")
    assert '"HOME": str(RUNNER_HOME)' in text
    assert '"XDG_CONFIG_HOME": str(RUNNER_HOME / ".config")' in text
    assert "env=os.environ.copy()" in text  # fetch/report domain
    assert "env=runner_env()" in text  # tested-code domain
    for secret_name in ["GH_TOKEN", "GITHUB_TOKEN", "RAILWAY_TOKEN", "TELEGRAM_TOKEN"]:
        assert f'"{secret_name}":' not in text


def test_adapter_receipts_are_unique_and_atomic():
    text = ADAPTER.read_text(encoding="utf-8")
    assert "def run_tag()" in text
    assert "os.fsync(handle.fileno())" in text
    assert "os.replace(tmp, path)" in text
    assert 'f"{run_tag()}-pr-' in text
    assert 'f"{run_tag()}-trusted-' in text


def test_adapter_has_no_sensitive_external_actions():
    text = ADAPTER.read_text(encoding="utf-8").lower()
    forbidden = [
        "gh pr merge",
        "git merge ",
        "git push origin main",
        "railway up",
        "railway deploy",
        "moyasar",
        "godaddy",
    ]
    for needle in forbidden:
        assert needle not in text


def test_installer_has_resource_and_filesystem_guards():
    text = INSTALLER.read_text(encoding="utf-8")
    for needle in [
        "CPUQuota=200%",
        "MemoryHigh=5G",
        "MemoryMax=6G",
        "NoNewPrivileges=true",
        "ProtectSystem=strict",
        "ProtectHome=read-only",
        "ReadWritePaths=$STATE_ROOT",
        "OnUnitInactiveSec=5min",
        "Persistent=true",
    ]:
        assert needle in text


def test_founder_command_bridge_reuses_canonical_verifier_and_pr_poller():
    text = CONTROL.read_text(encoding="utf-8")
    assert "DEALIX CANONICAL SOVEREIGN VERIFY" in text
    assert "bin/dealix verify trust --worktree" in text
    assert 'SOVEREIGN_ADAPTER="/opt/dealix/control/bin/dealix_sovereign_adapter.py"' in text
    assert 'SOVEREIGN_PR_POLL=BLOCKED_ADAPTER_NOT_INSTALLED' in text
    assert '/usr/bin/python3 "$SOVEREIGN_ADAPTER" poll' in text
    assert "scripts/verify_full_autonomous_ops_stack.py --skip-api" not in text
    assert "scripts/company_ready_verify.sh --docs-only --skip-go-live" not in text


def test_founder_verify_does_not_add_dynamic_pr_or_sha_input_surface():
    text = CONTROL.read_text(encoding="utf-8")
    assert 'verify-pr:*)' not in text
    assert 'verify-sha:*)' not in text
    assert 'git fetch origin "$' not in text
    assert 'eval ' not in text
