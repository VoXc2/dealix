from __future__ import annotations

import re
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


def _dispatcher_case_labels(text: str) -> set[str]:
    """Return exact command labels from the dispatcher's case arms.

    Parse labels rather than searching the whole shell file for fragments such
    as ``secrets)``. The latter can false-positive on harmless prose like
    ``environment/secrets):`` and says nothing about executable authority.
    """
    labels: set[str] = set()
    for match in re.finditer(r"^\s{2}([^#\n][^\n]*?)\)\s*$", text, re.MULTILINE):
        raw = match.group(1).strip()
        if raw == "*":
            continue
        for label in raw.split("|"):
            label = label.strip()
            if re.fullmatch(r"[A-Za-z0-9_-]+", label):
                labels.add(label)
    return labels


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
    case_labels = _dispatcher_case_labels(text)

    required_safe = {
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
    assert required_safe.issubset(case_labels), (
        f"missing expected safe VPS commands: {sorted(required_safe - case_labels)}"
    )

    forbidden_l5 = {
        "merge",
        "deploy",
        "send",
        "publish",
        "pay",
        "refund",
        "delete",
        "secrets",
    }
    assert case_labels.isdisjoint(forbidden_l5), (
        f"L5 command exposed by dispatcher: {sorted(case_labels & forbidden_l5)}"
    )


def test_repo_inspect_uses_read_only_github_api_auth() -> None:
    text = _text(DISPATCHER)
    assert "gh auth setup-git" not in text
    assert "ensure_github_api_auth" in text
    block = text.split('  repo-inspect)\n', 1)[1].split('    ;;', 1)[0]
    assert "git fetch origin main" not in block
    assert "gh api \"repos/${REPO_SLUG}/commits/main\" --jq '.sha'" in block
    assert 'echo "github_main=$GITHUB_MAIN"' in block
    assert 'echo "main_sync=UP_TO_DATE"' in block
    assert 'echo "main_sync=DRIFTED"' in block


def test_status_avoids_untracked_permission_noise_without_hiding_tracked_changes() -> None:
    text = _text(DISPATCHER)
    assert "tracked_status()" in text
    assert "git status -sb --untracked-files=no" in text
    assert text.count("tracked_status") >= 3


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

    # The current bridge rejects every non-founder author before returning an
    # event command. This fail-closed negative check is equivalent to a later
    # positive equality assertion, and is safer to pin directly.
    assert "if author != FOUNDER:" in text
    assert "return None" in text
    assert "author != FOUNDER or command is None" in text
    assert "--bootstrap" in text


def test_private_issue_bridge_allowlist_excludes_sensitive_execution() -> None:
    text = _text(ISSUE_BRIDGE)
    for command in (
        "status",
        "repo-inspect",
        "verify",
        "autonomous-dry-run",
        "daily",
        "sales-arena",
        "ollama-status",
        "n8n-status",
        "security-status",
    ):
        assert f'"{command}"' in text

    allowlist_block = text.split("ALLOWED = {", 1)[1].split("}", 1)[0]
    for command in ("merge", "deploy", "send", "pay", "delete", "secrets"):
        assert f'"{command}"' not in allowlist_block


def test_daily_and_sales_arena_stay_runtime_state_gated() -> None:
    text = _text(DISPATCHER)
    for command in ("daily", "sales-arena"):
        block = text.split(f"  {command})", 1)[1].split("    ;;", 1)[0]
        assert "require_runtime_state" in block


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


def test_self_hosted_runner_installer_recovers_configured_but_stopped_service() -> None:
    text = _text(RUNNER_INSTALLER)
    configured = text.split('if [[ -f .runner ]]; then', 1)[1].split('TMP_ARCHIVE=', 1)[0]

    # Existing registration is not enough. The installer must prove service
    # health, attempt one bounded recovery, and fail closed if it remains down.
    assert "if ! ./svc.sh status; then" in configured
    assert "./svc.sh start" in configured
    assert './svc.sh install "$RUNNER_USER"' in configured
    assert "configured runner service is still not healthy after recovery" in configured
    assert "configured_runner_recovered=true" in configured
