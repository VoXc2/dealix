from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(name: str) -> str:
    return (ROOT / "scripts" / name).read_text(encoding="utf-8")


def test_readiness_scripts_prefer_repo_venv() -> None:
    for name in (
        "company_ready_verify.sh",
        "founder_go_live_verify.sh",
        "run_business_now.sh",
    ):
        text = _text(name)
        assert '${ROOT}/.venv/bin/python' in text


def test_founder_go_live_uses_selected_python_for_pytest() -> None:
    text = _text("founder_go_live_verify.sh")
    assert 'if "$PYTHON_BIN" -m pytest ' in text
    assert "\nif pytest " not in text


def test_readiness_scripts_support_shared_worktree_venv() -> None:
    for name in (
        "company_ready_verify.sh",
        "founder_go_live_verify.sh",
        "run_business_now.sh",
    ):
        text = _text(name)
        assert "--git-common-dir" in text
        assert '${COMMON_ROOT}/.venv/bin/python' in text
