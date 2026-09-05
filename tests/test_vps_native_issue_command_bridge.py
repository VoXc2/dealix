from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "scripts" / "ops" / "dealix_vps_issue_bridge.py"
WORKFLOW = ROOT / ".github" / "workflows" / "vps-issue-command-native.yml"


def _load_bridge():
    spec = importlib.util.spec_from_file_location("dealix_vps_issue_bridge", BRIDGE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _event(*, repo="Dealix-sa/dealix", private=True, issue=1119, author="VoXc2", body="!dealix status", action="created"):
    return {
        "action": action,
        "repository": {"full_name": repo, "private": private},
        "issue": {"number": issue},
        "comment": {
            "id": 123,
            "created_at": "2026-09-03T00:00:00Z",
            "user": {"login": author},
            "body": body,
        },
    }


def test_event_authorization_is_exact_and_founder_only() -> None:
    bridge = _load_bridge()
    assert bridge.event_comment(_event()) is not None
    assert bridge.event_comment(_event(private=False)) is None
    assert bridge.event_comment(_event(repo="other/repo")) is None
    assert bridge.event_comment(_event(issue=1120)) is None
    assert bridge.event_comment(_event(author="someone-else")) is None
    assert bridge.event_comment(_event(action="edited")) is None


def test_command_parser_has_no_arbitrary_shell() -> None:
    bridge = _load_bridge()
    assert bridge.parse_command("!dealix status") == "status"
    assert bridge.parse_command("!dealix verify") == "verify"
    assert bridge.parse_command("!dealix rm -rf /") == "__DENIED__"
    assert bridge.parse_command("!dealix status\nwhoami") is None
    assert bridge.parse_command("status") is None


def test_redaction_covers_common_secret_shapes() -> None:
    bridge = _load_bridge()
    output = bridge.redact(
        "AUTHORIZATION: Bearer abcdef123456\n"
        "OPENAI_API_KEY=sk-secretsecretsecret\n"
        "TOKEN=github_pat_abcdefghijklmno\n"
        "https://x.test/?token=hello-world"
    )
    assert "abcdef123456" not in output
    assert "sk-secretsecretsecret" not in output
    assert "github_pat_abcdefghijklmno" not in output
    assert "hello-world" not in output
    assert "[REDACTED]" in output


def test_native_workflow_is_private_founder_issue_scoped() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    for required in (
        "issue_comment:",
        "types: [created]",
        "github.event.repository.private == true",
        "github.event.issue.number == 1119",
        "github.event.comment.user.login == 'VoXc2'",
        "startsWith(github.event.comment.body, '!dealix ')",
        "runs-on: [self-hosted, linux, x64, dealix-vps]",
        "python3 scripts/ops/dealix_vps_issue_bridge.py --event",
        "DEALIX_NATIVE_EVENT_GRACE_SECONDS: '75'",
        "persist-credentials: false",
    ):
        assert required in text

    for forbidden in (
        "bash -c ${{ github.event.comment.body }}",
        "eval ",
        "pull_request_target",
        "contents: write",
        "actions: write",
    ):
        assert forbidden not in text
