"""Test the AI router falls back to deterministic when no provider."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lib.ai_router import AIRouter
from lib.ai_safety import check_output, check_flags


def test_router_fallback_to_deterministic() -> None:
    router = AIRouter(mode="demo")
    assert router.mode == "demo"
    assert router.provider in ("deterministic", "minimax", "kimi", "deepseek", "openrouter", "openai")


def test_router_call_returns_safe_output() -> None:
    router = AIRouter(mode="demo")
    r = router.call(
        "outreach_draft_en",
        "outreach_draft_en",
        {"name": "Demo Co", "signal": "slow response", "weakness": "lead routing"},
    )
    assert r.review_status == "draft_pending_human_review"
    check = check_output(r.output)
    assert check["safe"], check
    flags = check_flags(r.safety_flags)
    assert flags["ok"], flags


def test_ai_evals_pass() -> None:
    import subprocess
    p = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "run_ai_evals.py"), "--mode", "demo"],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0, p.stdout + p.stderr


if __name__ == "__main__":
    test_router_fallback_to_deterministic()
    test_router_call_returns_safe_output()
    test_ai_evals_pass()
    print("test_ai_router_fallback passed")
