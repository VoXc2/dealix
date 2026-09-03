from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "scripts" / "ops" / "dealix_slack_founder_bridge.py"


def load_bridge():
    spec = importlib.util.spec_from_file_location("dealix_slack_founder_bridge", BRIDGE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def init_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-b", "main", str(path)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "Dealix Test"], check=True)
    (path / "README.md").write_text("test\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-m", "test"], check=True, capture_output=True)
    sha = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    subprocess.run(["git", "-C", str(path), "update-ref", "refs/remotes/origin/main", sha], check=True)


def test_allowlisted_founder_commands_route_only_to_canonical_modes():
    bridge = load_bridge()
    expected = {
        "status",
        "heartbeat",
        "production",
        "repo-watch",
        "preflight",
        "market-radar",
        "midday",
        "evening",
        "nightly",
        "weekly",
        "local-ai",
    }
    assert expected == bridge.CANONICAL_MODES
    assert bridge.classify_command("STATUS").mode == "status"
    assert bridge.classify_command("VERIFY").mode == "preflight"
    assert bridge.classify_command("MARKET").mode == "market-radar"
    assert bridge.classify_command("دورة").mode == "midday"


def test_mentions_are_removed_before_policy_classification():
    bridge = load_bridge()
    decision = bridge.classify_command("<@U123ABC>   STATUS   now")
    assert decision.result == "EXECUTED"
    assert decision.mode == "status"


def test_unknown_or_free_form_commands_do_not_execute():
    bridge = load_bridge()
    for command in ("نفذ كلشي", "DO EVERYTHING", "run arbitrary shell", "hello"):
        decision = bridge.classify_command(command)
        assert decision.result == "FAILED"
        assert decision.mode is None
        assert decision.action == "UNSUPPORTED_FOUNDER_COMMAND"


def test_l5_intents_are_blocked_in_english_and_arabic():
    bridge = load_bridge()
    commands = (
        "SEND email to a customer",
        "PUBLISH this publicly",
        "MERGE PR 1477",
        "DEPLOY production",
        "PAY the invoice",
        "REFUND the customer",
        "DELETE production data",
        "LinkedIn DM this lead",
        "أرسل ايميل للعميل",
        "إرسال رسالة واتساب",
        "انشر هذا للعامة",
        "ادمج الطلب",
        "ادفع الفاتورة",
        "احذف البيانات",
        "لينكد ان رسالة للعميل",
    )
    for command in commands:
        decision = bridge.classify_command(command)
        assert decision.result == "APPROVAL_REQUIRED", command
        assert decision.authority_class == "APPROVAL_REQUIRED", command
        assert decision.execution_boundary == "L5_BLOCKED", command
        assert decision.mode is None, command


def test_fail_closed_environment_overrides_unsafe_values_and_strips_slack_secrets(monkeypatch):
    bridge = load_bridge()
    monkeypatch.setenv("DEALIX_EXTERNAL_SEND", "1")
    monkeypatch.setenv("AUTO_SEND_ENABLED", "true")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")
    monkeypatch.setenv("DEALIX_PAYMENT_EXECUTION", "1")
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-secret")
    monkeypatch.setenv("SLACK_APP_TOKEN", "xapp-secret")
    monkeypatch.setenv("DEALIX_SLACK_SIGNING_SECRET", "signing-secret")
    env = bridge.fail_closed_env()
    assert env["DEALIX_EXTERNAL_SEND"] == "0"
    assert env["AUTO_SEND_ENABLED"] == "false"
    assert env["WHATSAPP_ALLOW_LIVE_SEND"] == "false"
    assert env["DEALIX_PAYMENT_EXECUTION"] == "0"
    assert env["DEALIX_PRODUCTION_MUTATION"] == "0"
    assert env["DEALIX_SECRET_MUTATION"] == "0"
    assert env["AGENT_APPROVAL_MODE"] == "required"
    assert "SLACK_BOT_TOKEN" not in env
    assert "SLACK_APP_TOKEN" not in env
    assert "DEALIX_SLACK_SIGNING_SECRET" not in env


def test_workload_id_is_deterministic_and_event_specific():
    bridge = load_bridge()
    first = bridge.workload_id("C123", "1720000000.100", "U123")
    second = bridge.workload_id("C123", "1720000000.100", "U123")
    third = bridge.workload_id("C123", "1720000000.101", "U123")
    assert first == second
    assert first != third
    assert first.startswith("slack-")


def test_receipt_is_verifier_compatible_for_l5_block(monkeypatch, tmp_path):
    bridge = load_bridge()
    monkeypatch.setattr(bridge, "RECEIPT_DIR", tmp_path)
    decision = bridge.classify_command("PAY invoice")
    receipt = bridge.make_receipt(
        work_id="slack-1234567890abcdef1234",
        slack_ref="slack:C0BTMAWR3NY:1720000000.100",
        sha="a" * 40,
        decision=decision,
        elapsed_ms=0,
        runner_rc=None,
    )
    assert receipt["system_id"] == "command_os"
    assert receipt["agent"] == "dealix-pm"
    assert receipt["runner"] == str(bridge.AUTOPILOT)
    assert receipt["source_sha"] == "a" * 40
    assert receipt["authority_class"] == "APPROVAL_REQUIRED"
    assert receipt["execution_boundary"] == "L5_BLOCKED"
    assert receipt["result"] == "APPROVAL_REQUIRED"
    assert receipt["state_after"] == "BLOCKED_AT_AUTHORITY_GATE"
    assert receipt["input_evidence_refs"] == ["slack:C0BTMAWR3NY:1720000000.100"]
    assert receipt["idempotency_key"] == receipt["workload_id"]
    serialized = json.dumps(receipt)
    assert "xoxb-" not in serialized
    assert "xapp-" not in serialized


def test_nonzero_canonical_runner_result_is_not_reported_as_executed(monkeypatch, tmp_path):
    bridge = load_bridge()
    monkeypatch.setattr(bridge, "RECEIPT_DIR", tmp_path)
    decision = bridge.classify_command("STATUS")
    receipt = bridge.make_receipt(
        work_id="slack-abcdef1234567890abcd",
        slack_ref="slack:C0BTMAWR3NY:1720000001.100",
        sha="b" * 40,
        decision=decision,
        elapsed_ms=51,
        runner_rc=7,
    )
    assert receipt["result"] == "FAILED"
    assert receipt["state_after"] == "CANONICAL_AUTOPILOT_FAILED"
    assert receipt["runner_rc"] == 7


def test_receipt_write_is_atomic_and_readable(monkeypatch, tmp_path):
    bridge = load_bridge()
    monkeypatch.setattr(bridge, "RECEIPT_DIR", tmp_path)
    decision = bridge.classify_command("STATUS")
    receipt = bridge.make_receipt(
        work_id="slack-feedfacefeedfacefeed",
        slack_ref="slack:C0BTMAWR3NY:1720000002.100",
        sha="c" * 40,
        decision=decision,
        elapsed_ms=15,
        runner_rc=0,
    )
    path = bridge.write_receipt(receipt)
    assert path.is_file()
    assert bridge.existing_receipt(receipt["workload_id"]) == receipt
    assert oct(path.stat().st_mode & 0o777) == "0o640"
    assert not path.with_suffix(".tmp").exists()


def test_corrupt_receipt_fails_closed(monkeypatch, tmp_path):
    bridge = load_bridge()
    monkeypatch.setattr(bridge, "RECEIPT_DIR", tmp_path)
    work_id = "slack-deadbeefdeadbeefdead"
    (tmp_path / f"{work_id}.json").write_text("not-json", encoding="utf-8")
    with pytest.raises(bridge.ReceiptStateError):
        bridge.existing_receipt(work_id)


def test_workload_lock_creates_private_lock_file(monkeypatch, tmp_path):
    bridge = load_bridge()
    monkeypatch.setattr(bridge, "RECEIPT_DIR", tmp_path)
    work_id = "slack-locktest1234567890"
    with bridge.workload_lock(work_id):
        lock_path = tmp_path / f".{work_id}.lock"
        assert lock_path.is_file()
        assert oct(lock_path.stat().st_mode & 0o777) == "0o640"


def test_runtime_repo_state_requires_clean_main_equal_origin(tmp_path):
    bridge = load_bridge()
    repo = tmp_path / "repo"
    init_repo(repo)
    assert bridge.runtime_repo_state(repo).canonical is True
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    assert bridge.runtime_repo_state(repo).canonical is False


def test_runner_log_is_bound_and_slack_secrets_do_not_reach_child(monkeypatch, tmp_path):
    bridge = load_bridge()
    repo = tmp_path / "repo"
    init_repo(repo)
    receipts = tmp_path / "receipts"
    runner = tmp_path / "autopilot.sh"
    runner.write_text(
        "#!/usr/bin/env bash\n"
        "set -eu\n"
        "printf 'bot=%s\\n' \"${SLACK_BOT_TOKEN-unset}\"\n"
        "printf 'external=%s\\n' \"${DEALIX_EXTERNAL_SEND-unset}\"\n",
        encoding="utf-8",
    )
    runner.chmod(0o750)
    monkeypatch.setattr(bridge, "REPO_ROOT", repo)
    monkeypatch.setattr(bridge, "RECEIPT_DIR", receipts)
    monkeypatch.setattr(bridge, "AUTOPILOT", runner)
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-must-not-leak")
    monkeypatch.setenv("SLACK_APP_TOKEN", "xapp-must-not-leak")
    work_id = "slack-abcdef1234567890abcd"
    run = bridge.run_autopilot_with_evidence("status", work_id)
    output = run.log_path.read_text(encoding="utf-8")
    assert "xoxb-must-not-leak" not in output
    assert "bot=unset" in output
    assert "external=0" in output
    assert len(run.log_sha256) == 64
    with pytest.raises(bridge.IndeterminatePriorAttempt):
        bridge.run_autopilot_with_evidence("status", work_id)
