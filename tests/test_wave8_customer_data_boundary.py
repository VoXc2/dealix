"""Wave 8 — Customer Data Boundary tests."""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GITIGNORE = REPO_ROOT / ".gitignore"
BOUNDARY_MD = REPO_ROOT / "docs" / "WAVE8_CUSTOMER_DATA_BOUNDARY.md"
BOUNDARY_SH = REPO_ROOT / "scripts" / "wave8_customer_data_boundary_check.sh"


def test_boundary_md_exists():
    assert BOUNDARY_MD.exists(), "WAVE8_CUSTOMER_DATA_BOUNDARY.md must exist"


def test_boundary_sh_exists():
    assert BOUNDARY_SH.exists(), "wave8_customer_data_boundary_check.sh must exist"


def test_gitignore_has_customer_data_pattern():
    content = GITIGNORE.read_text(encoding="utf-8")
    assert "data/customers/**" in content or "data/customers/" in content, \
        "data/customers/** must be gitignored"


def test_gitignore_has_env_pattern():
    content = GITIGNORE.read_text(encoding="utf-8")
    assert ".env" in content, ".env must be in .gitignore"


def test_gitignore_has_proof_events_pattern():
    content = GITIGNORE.read_text(encoding="utf-8")
    assert "proof-events" in content, "proof-events must be gitignored"


def test_no_customer_data_in_git():
    """Verify no actual customer data files are tracked in git."""
    result = subprocess.run(
        ["git", "ls-files", "data/customers/"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    tracked = result.stdout.strip()
    assert not tracked, f"Customer data should not be tracked in git: {tracked}"


def test_no_env_file_committed():
    """Verify .env is not committed to git."""
    result = subprocess.run(
        ["git", "ls-files", ".env"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert not result.stdout.strip(), ".env must not be committed to git"


def test_no_hardcoded_live_secrets_in_tracked_py():
    """Basic scan for live secret patterns in Python source."""
    import re
    patterns = [
        re.compile(r"sk_live_[A-Za-z0-9]{10,}"),
        re.compile(r"sk-ant-api[A-Za-z0-9\-]{10,}"),
    ]
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    py_files = result.stdout.strip().splitlines()
    for py_file in py_files[:50]:  # Check first 50 files
        try:
            content = (REPO_ROOT / py_file).read_text(encoding="utf-8", errors="ignore")
            for pat in patterns:
                matches = pat.findall(content)
                assert not matches, \
                    f"Possible hardcoded secret in {py_file}: {matches[:1]}"
        except (OSError, UnicodeDecodeError):
            pass


def test_boundary_md_mentions_pdpl():
    content = BOUNDARY_MD.read_text(encoding="utf-8")
    assert "PDPL" in content, "Data boundary doc must mention PDPL"


def test_boundary_md_mentions_dpa():
    content = BOUNDARY_MD.read_text(encoding="utf-8")
    assert "DPA" in content, "Data boundary doc must mention DPA requirement"
