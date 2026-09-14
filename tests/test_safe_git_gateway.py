"""Unit contracts for the safe git gateway (no network, no gh, no merges)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "scripts" / "ops"


def _load():
    spec = importlib.util.spec_from_file_location(
        "dealix_safe_git_gateway", OPS / "dealix_safe_git_gateway.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gw = _load()


def test_secret_scan_blocks_token_assignment() -> None:
    diff = '+LINKEDIN_ACCESS_TOKEN = "abc123xyz456"\n+ok = 1\n'
    assert len(gw.secret_scan(diff)) == 1
    assert gw.secret_scan('+ok = 1\n') == []


def test_secret_scan_blocks_private_key() -> None:
    assert gw.secret_scan("+-----BEGIN RSA PRIVATE KEY-----\n")


def test_whitespace_check_rejects_trailing_space() -> None:
    ok, _ = gw.whitespace_check("+clean = 1\n")
    assert ok is True
    ok, detail = gw.whitespace_check("+dirty = 1   \n")
    assert ok is False and "trailing" in detail


def test_whitespace_check_rejects_empty_diff() -> None:
    assert gw.whitespace_check("   \n")[0] is False


def test_merge_rejects_admin_and_non_merge_method() -> None:
    assert gw.main(["pr-merge", "1", "--head", "a" * 40, "--admin"]) == 2
    assert gw.main(["pr-merge", "1", "--head", "a" * 40, "--method", "squash"]) == 2


def test_feature_push_refuses_main_and_force(capsys) -> None:
    assert gw.main(["feature-push", "--branch", "main"]) == 2
    assert gw.main(["feature-push", "--branch", "feat/x", "--force"]) == 2


def test_pr_close_requires_merged_superseder() -> None:
    assert gw.main(["pr-close", "1"]) == 2


def test_unknown_command_fails_closed() -> None:
    try:
        gw.main(["nope"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("expected SystemExit")
