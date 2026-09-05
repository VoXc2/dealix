from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "scripts" / "ops" / "dealix_vps_issue_bridge.py"
WORKFLOW = ROOT / ".github" / "workflows" / "vps-issue-command-native.yml"
STAMP = "2026-09-05T02:00:00Z"


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


def _comment(ident, body="founder note", author="VoXc2", created=STAMP):
    return {"id": ident, "created_at": created, "updated_at": STAMP,
            "user": {"login": author}, "body": body}


def _proof(ident, command="status"):
    return ("DEALIX_VPS_COMMAND_PROOF\n\n"
            f"- source_comment_id: `{ident}`\n- command: `{command}`\n"
            "- exit_code: `0`\n")


@pytest.fixture
def harness(tmp_path, monkeypatch):
    """All network/dispatcher effects are fakes; only temp state files are real."""
    bridge = _load_bridge()
    bridge.STATE = tmp_path / "state.json"
    bridge.LOCK = tmp_path / "bridge.lock"
    bridge.CONTROL = tmp_path / "control.sh"
    bridge.CONTROL.write_text("not executed", encoding="utf-8")
    monkeypatch.setattr(bridge, "now_iso", lambda: STAMP)
    h = SimpleNamespace(bridge=bridge, comments=[], calls=[], posts=[], reads=[],
                        returncode=0, failure=None, publish_failure=False)

    def read(endpoint, **kwargs):
        if endpoint == f"repos/{bridge.REPO}":
            return {"private": True}
        assert endpoint.startswith(f"repos/{bridge.REPO}/issues/{bridge.ISSUE}/comments?")
        q = parse_qs(urlsplit(endpoint).query)
        page = int(q["page"][0])
        assert q["per_page"] == ["100"]
        h.reads.append(q)
        rows = sorted(h.comments, key=lambda row: row["id"])
        if "since" in q:
            rows = [row for row in rows if row["updated_at"] > q["since"][0]]
        return copy.deepcopy(rows[(page - 1) * 100:page * 100])

    def dispatch(args, **kwargs):
        # State must reach disk BEFORE the external process starts.
        pending = json.loads(bridge.STATE.read_text())["pending"]
        assert pending["phase"] == "STARTED"
        assert args == [str(bridge.CONTROL), pending["command"]]
        assert not kwargs.get("shell", False)
        h.calls.append(args[-1])
        if h.failure is not None:
            raise h.failure
        return subprocess.CompletedProcess(args, h.returncode, "TOKEN=secretvalue\nOK", "")

    def publish(body):
        assert json.loads(bridge.STATE.read_text())["pending"]["phase"] == "FINISHED"
        if h.publish_failure:
            raise RuntimeError("simulated network outage")
        h.posts.append(body)
        h.comments.append(_comment(max([r["id"] for r in h.comments] + [0]) + 1,
                                   body=body, author="github-actions[bot]"))

    monkeypatch.setattr(bridge, "gh_json", read)
    monkeypatch.setattr(bridge, "gh_comment", publish)
    monkeypatch.setattr(bridge, "subprocess", SimpleNamespace(run=dispatch))
    bridge._write_state({"last_comment_id": 0, "last_created_at": STAMP})
    return h


def test_bootstrap_skips_all_pages_and_never_resets_existing_state(harness):
    h = harness
    b = h.bridge
    b.STATE.unlink()
    h.comments = [_comment(i, "!dealix status") for i in range(1, 260)]
    assert b.bootstrap_state() == 0
    assert b.load_state()["last_comment_id"] == 259
    assert [q["page"][0] for q in h.reads] == ["1", "2", "3"]
    assert h.calls == []
    before = b.STATE.read_bytes()
    with pytest.raises(RuntimeError, match="BOOTSTRAP_STATE_EXISTS"):
        b.bootstrap_state()
    assert b.STATE.read_bytes() == before


@pytest.mark.parametrize("bad", [None, "{", "[]", '{"last_comment_id": true}',
                                  '{"last_comment_id": -1}',
                                  '{"last_comment_id": 5, "last_created_at": "bad"}'])
def test_missing_or_corrupt_state_never_replays(harness, bad):
    h = harness
    if bad is None:
        h.bridge.STATE.unlink()
    else:
        h.bridge.STATE.write_text(bad)
    with pytest.raises(RuntimeError, match="BRIDGE_HOLD_STATE"):
        h.bridge.process_poll_cycle()
    assert h.calls == []


def test_state_symlink_is_rejected(harness, tmp_path):
    b = harness.bridge
    target = tmp_path / "target.json"
    target.write_bytes(b.STATE.read_bytes())
    b.STATE.unlink()
    b.STATE.symlink_to(target)
    with pytest.raises(RuntimeError, match="STATE_MISSING_OR_UNSAFE"):
        b.load_state()


def test_pagination_reaches_new_command_after_edited_old_comments(harness):
    h = harness
    h.bridge.save_state(200, STAMP)
    h.comments = [_comment(i, created="2026-09-03T00:00:00Z") for i in range(1, 151)]
    h.comments.append(_comment(201, "!dealix status"))
    assert h.bridge.process_poll_cycle() == 0
    assert h.calls == ["status"]
    assert h.bridge.load_state()["last_comment_id"] == 201
    assert any(q["page"] == ["2"] for q in h.reads)


def test_founder_notes_and_untrusted_commands_advance_without_dispatch(harness):
    h = harness
    h.comments = [_comment(1), _comment(2, "!dealix status", author="other-user"),
                  _comment(3, "!dealix merge"), _comment(4, "!dealix status\necho nope")]
    assert h.bridge.process_poll_cycle() == 0
    assert h.bridge.load_state()["last_comment_id"] == 4
    assert h.calls == []
    assert h.posts == []


def test_proof_on_later_page_prevents_dispatch(harness):
    h = harness
    h.comments = [_comment(1, "!dealix status")]
    h.comments.extend(_comment(i) for i in range(2, 130))
    h.comments.append(_comment(130, _proof(1), author="github-actions[bot]"))
    assert h.bridge.process_poll_cycle() == 0
    assert h.calls == []
    assert h.bridge.load_state()["last_comment_id"] == 130


@pytest.mark.parametrize("author,body", [
    ("attacker", _proof(1)),
    ("VoXc2", "Quoted text:\n" + _proof(1)),
    ("VoXc2", _proof(1, "verify")),
    ("VoXc2", _proof(10)),
])
def test_proof_requires_trusted_author_exact_header_id_and_command(harness, author, body):
    harness.comments = [_comment(2, body, author=author)]
    assert not harness.bridge.proof_exists(1, "status")


def test_native_event_cannot_leapfrog_earlier_command(harness):
    h = harness
    h.comments = [_comment(1, "!dealix status"), _comment(2, "!dealix repo-inspect")]
    with h.bridge.execution_lock():
        assert h.bridge.drain_queue(target=copy.deepcopy(h.comments[1])) == 0
    assert h.calls == ["status", "repo-inspect"]
    assert h.bridge.load_state()["last_comment_id"] == 2
    assert h.bridge.process_poll_cycle() == 0
    assert h.calls == ["status", "repo-inspect"]


@pytest.mark.parametrize("missing", [True, False])
def test_native_missing_or_changed_event_does_not_dispatch(harness, missing):
    h = harness
    target = _comment(2, "!dealix status")
    h.comments = [_comment(1)] if missing else [_comment(2, "!dealix verify")]
    with h.bridge.execution_lock(), pytest.raises(RuntimeError, match="BRIDGE_HOLD_EVENT"):
        h.bridge.drain_queue(target=target)
    assert h.calls == []
    assert h.bridge.load_state()["last_comment_id"] == 0


@pytest.mark.parametrize("failure", [OSError("dispatcher unavailable"),
                                      subprocess.TimeoutExpired(["control", "status"], 3300)])
def test_started_command_is_not_replayed_after_ambiguous_failure(harness, failure):
    h = harness
    h.comments = [_comment(1, "!dealix status")]
    h.failure = failure
    with pytest.raises(type(failure)):
        h.bridge.process_poll_cycle()
    assert h.bridge.load_state()["pending"]["phase"] == "STARTED"
    h.failure = None
    with pytest.raises(RuntimeError, match="AMBIGUOUS_DISPATCH_REVIEW_REQUIRED"):
        h.bridge.process_poll_cycle()
    assert h.calls == ["status"]
    assert h.posts == []


def test_receipt_publication_retries_without_running_command_again(harness):
    h = harness
    h.comments = [_comment(1, "!dealix status")]
    h.publish_failure = True
    with pytest.raises(RuntimeError, match="network outage"):
        h.bridge.process_poll_cycle()
    assert h.bridge.load_state()["pending"]["phase"] == "FINISHED"
    h.publish_failure = False
    assert h.bridge.process_poll_cycle() == 0
    assert h.calls == ["status"]
    assert len(h.posts) == 1
    assert "secretvalue" not in h.posts[0]
    assert "secretvalue" not in h.bridge.STATE.read_text()
    assert h.bridge.load_state()["pending"] is None


def test_already_posted_finished_receipt_is_not_posted_again(harness):
    h = harness
    h.comments = [_comment(1, "!dealix status")]
    h.publish_failure = True
    with pytest.raises(RuntimeError):
        h.bridge.process_poll_cycle()
    pending = h.bridge.load_state()["pending"]
    h.comments.append(_comment(2, pending["proof"], author="github-actions[bot]"))
    h.publish_failure = False
    assert h.bridge.process_poll_cycle() == 0
    assert h.calls == ["status"]
    assert h.posts == []


def test_nonzero_command_is_recorded_then_next_poll_continues(harness):
    h = harness
    h.comments = [_comment(1, "!dealix status"), _comment(2, "!dealix repo-inspect")]
    h.returncode = 7
    assert h.bridge.process_poll_cycle() == 7
    assert h.bridge.load_state()["last_comment_id"] == 1
    assert h.bridge.load_state()["pending"] is None
    h.returncode = 0
    assert h.bridge.process_poll_cycle() == 0
    assert h.calls == ["status", "repo-inspect"]


def test_pagination_limit_does_not_advance_partial_cursor(harness, monkeypatch):
    h = harness
    h.comments = [_comment(i, "!dealix status") for i in range(1, 102)]
    monkeypatch.setattr(h.bridge, "MAX_COMMENT_PAGES", 1)
    before = h.bridge.STATE.read_bytes()
    with pytest.raises(RuntimeError, match="PAGINATION_LIMIT"):
        h.bridge.process_poll_cycle()
    assert h.bridge.STATE.read_bytes() == before
    assert h.calls == []


def test_page_failure_does_not_advance_partial_cursor(harness, monkeypatch):
    h = harness
    h.comments = [_comment(i) for i in range(1, 102)]
    original = h.bridge.gh_json

    def fail_page_two(endpoint, **kwargs):
        if "page=2" in endpoint:
            raise OSError("network failure")
        return original(endpoint, **kwargs)

    monkeypatch.setattr(h.bridge, "gh_json", fail_page_two)
    with pytest.raises(OSError):
        h.bridge.process_poll_cycle()
    assert h.bridge.load_state()["last_comment_id"] == 0
    assert h.calls == []


def test_changed_duplicate_page_entry_fails_closed(harness, monkeypatch):
    h = harness
    first = [_comment(i) for i in range(1, 101)]
    pages = iter([first, [_comment(100, "edited")]])
    monkeypatch.setattr(h.bridge, "gh_json", lambda *a, **k: next(pages))
    with pytest.raises(RuntimeError, match="COMMENT_INVALID_OR_CHANGED"):
        h.bridge.list_comments()
    assert h.bridge.load_state()["last_comment_id"] == 0


def test_state_is_private_and_cursor_cannot_regress(harness):
    b = harness.bridge
    assert b.STATE.stat().st_mode & 0o777 == 0o600
    b.save_state(9, STAMP)
    with pytest.raises(RuntimeError, match="CURSOR_REGRESSION"):
        b.save_state(8, STAMP)
    assert b.load_state()["last_comment_id"] == 9
    assert b._since(STAMP) == "2026-09-05T01:59:59Z"


def test_native_and_poll_entrypoints_share_durable_dispatch_state(harness, tmp_path, monkeypatch):
    h = harness
    event = _event()
    event["comment"] = _comment(1, "!dealix status")
    h.comments = [copy.deepcopy(event["comment"])]
    path = tmp_path / "event.json"
    path.write_text(json.dumps(event))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(path))
    monkeypatch.setenv("DEALIX_NATIVE_EVENT_GRACE_SECONDS", "0")
    assert h.bridge.process_native_event() == 0
    assert h.bridge.process_poll_cycle() == 0
    assert h.bridge.process_native_event() == 0
    assert h.calls == ["status"]
