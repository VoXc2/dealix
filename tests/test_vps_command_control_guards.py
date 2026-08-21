from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPATCHER = ROOT / "scripts" / "ops" / "dealix_vps_control.sh"
WORKFLOW = ROOT / ".github" / "workflows" / "vps-command-control.yml"
ISSUE_BRIDGE = ROOT / "scripts" / "ops" / "dealix_vps_issue_bridge.py"
ISSUE_INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_vps_issue_bridge.sh"
RUNNER_INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_self_hosted_runner.sh"


def _text(path: Path) -> str:
    assert path.is_file(), f"missing {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def test_dispatcher_has_no_arbitrary_shell_execution() -> None:
    text = _text(DISPATCHER)
    forbidden = (
        "eval ",
        "bash -c \"$",
        "sh -c \"$",
        "source $",
        "git push --force",
        "gh pr merge",
        "railway up",
        "railway redeploy",
        "vercel --prod",
        "docker system prune -a",
    )
    for token in forbidden:
        assert token not in text, f"unsafe token present: {token}"


def test_dispatcher_allowlist_excludes_l5_actions() -> None:
    text = _text(DISPATCHER)
    allowed = {
        "status",
        "repo-inspect",
        "verify",
        "autonomous-dry-run",
        "daily",
        "sales-arena",
        "ollama-status",
        "n8n-status",
        "security-status",
    }
    for command in allowed:
        assert f"{command})" in text

    for forbidden_command in (
        "merge)",
        "deploy)",
        "send)",
        "publish)",
        "pay)",
        "refund)",
        "delete)",
        "secrets)",
    ):
        assert forbidden_command not in text


def test_workflow_blocks_vps_execution_while_public() -> None:
    text = _text(WORKFLOW)
    assert "github.event.repository.private != true" in text
    assert "DEALIX_VPS_EXECUTION=BLOCKED_PUBLIC_REPOSITORY" in text
    assert "github.event.repository.private == true && github.actor == 'VoXc2'" in text
    assert "runs-on: [self-hosted, linux, x64, dealix-vps]" in text


def test_workflow_exposes_only_allowlisted_choice_input() -> None:
    text = _text(WORKFLOW)
    assert "type: choice" in text
    assert "command:" in text
    assert "workflow_dispatch:" in text
    assert 'AUTO_SEND_ENABLED: "false"' in text
    assert 'AGENT_APPROVAL_MODE: "required"' in text


def test_private_issue_bridge_has_no_arbitrary_shell() -> None:
    text = _text(ISSUE_BRIDGE)
    assert "shell=True" not in text
    assert "os.system(" not in text
    assert "eval(" not in text
    assert "subprocess.run(" in text
    assert "[str(CONTROL), command]" in text


def test_private_issue_bridge_requires_private_repo_and_founder() -> None:
    text = _text(ISSUE_BRIDGE)
    assert 'REPO = "Dealix-sa/dealix"' in text
    assert 'FOUNDER = "VoXc2"' in text
    assert 'PREFIX = "!dealix "' in text
    assert 'repo.get("private") is not True' in text
    assert "author == FOUNDER" in text
    assert "--bootstrap" in text


def test_private_issue_bridge_allowlist_excludes_sensitive_execution() -> None:
    text = _text(ISSUE_BRIDGE)
    for command in (
        "status",
        "repo-inspect",
        "verify",
        "autonomous-dry-run",
        "ollama-status",
        "n8n-status",
        "security-status",
    ):
        assert f'"{command}"' in text

    # Higher-impact runners are deliberately not exposed through the issue bridge yet.
    allowlist_block = text.split("ALLOWED = {", 1)[1].split("}", 1)[0]
    for command in ("daily", "sales-arena", "merge", "deploy", "send", "pay"):
        assert f'"{command}"' not in allowlist_block


def test_private_issue_bridge_redacts_secret_shapes_and_caps_output() -> None:
    text = _text(ISSUE_BRIDGE)
    assert "SECRET_PATTERNS" in text
    assert "[REDACTED]" in text
    assert "MAX_OUTPUT_CHARS = 6000" in text
    assert "OUTPUT TRUNCATED" in text


def test_issue_bridge_installer_bootstraps_without_replaying_history() -> None:
    text = _text(ISSUE_INSTALLER)
    assert "must be private" in text
    assert 'FOUNDER="VoXc2"' in text
    assert "python3 \"$BRIDGE\" --bootstrap" in text
    assert "historical_comments_ignored=true" in text
    assert "User=${RUNNER_USER}" in text
    assert "NoNewPrivileges=true" in text
    assert "ProtectSystem=full" in text


def test_self_hosted_runner_installer_does_not_print_registration_token() -> None:
    text = _text(RUNNER_INSTALLER)
    assert "registration-token" in text
    assert "unset TOKEN" in text
    assert "secret_values_printed=false" in text
    assert 'RUNNER_USER="dealix"' in text
    assert 'RUNNER_NAME="dealix-vps"' in text
    assert "must be private" in text
