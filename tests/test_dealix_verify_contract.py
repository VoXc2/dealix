import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dealix_verify.py"


def _module():
    spec = importlib.util.spec_from_file_location("dealix_verify_contract", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pr_mode_never_inherits_runtime_or_production():
    module = _module()
    assert module.MODE_GROUPS["pr"] == ["source", "tests"]
    assert "runtime" not in module.MODE_GROUPS["pr"]
    assert "production" not in module.MODE_GROUPS["pr"]


def test_arbitrary_sha_modes_are_source_only():
    module = _module()
    assert module.SHA_SAFE_MODES == {"changed", "pr", "trust", "security"}
    assert "runtime" not in module.SHA_SAFE_MODES
    assert "production" not in module.SHA_SAFE_MODES
    assert "full" not in module.SHA_SAFE_MODES


def test_receipt_contract_does_not_embed_output_tails():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "stdout_tail" not in text
    assert "stderr_tail" not in text
    assert '"log_path"' in text
    assert "os.fsync" in text


def test_commercial_lane_uses_canonical_truth_checks_not_outreach_drafts():
    module = _module()
    text = SCRIPT.read_text(encoding="utf-8")
    names = [item[0] for item in module.COMMERCIAL_CHECKS]
    commands = [" ".join(item[1]) for item in module.COMMERCIAL_CHECKS]

    assert names == ["commercial-launch-ready", "first-paid-truth"]
    assert any("scripts/verify_commercial_launch_ready.py" in command for command in commands)
    assert any("scripts/verify_first_paid_diagnostic_tracker.py --json" in command for command in commands)
    assert "build_kpi_import_from_review_queue.py" not in text


def test_external_action_commands_are_absent():
    text = SCRIPT.read_text(encoding="utf-8").lower()
    forbidden = [
        "git merge ",
        "git push origin main",
        "railway up",
        "railway deploy",
        "gh pr merge",
        "curl -x post",
    ]
    for needle in forbidden:
        assert needle not in text
