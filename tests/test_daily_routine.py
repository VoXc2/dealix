"""Daily Routine Orchestrator — Wave 17."""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_daily_routine_imports_cleanly():
    """The orchestrator script must be importable so cron can wrap it."""
    script = REPO / "scripts" / "daily_routine.py"
    assert script.exists()
    # syntax-check via py_compile
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_daily_routine_emits_consolidated_brief_with_required_sections():
    """End-to-end: run the routine in --quick mode and assert the
    consolidated markdown has all 5 sections + 3 next actions + the
    bilingual disclaimer footer."""
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "daily_routine.py"), "--quick", "--json"],
        capture_output=True, text=True, timeout=180, check=False, cwd=str(REPO),
    )
    assert result.returncode == 0, f"routine failed:\nstdout:{result.stdout}\nstderr:{result.stderr}"

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    brief_path = REPO / "data" / "daily_routine" / f"{today}.md"
    assert brief_path.exists(), f"consolidated brief not written: {brief_path}"

    body = brief_path.read_text(encoding="utf-8")
    # 5 numbered sections (markdown ##)
    for section in (
        "## 1. Morning routine sub-steps",
        "## 2. Outreach drafts ready",
        "## 3. Leads to reply",
        "## 4. Renewals due next 7d",
        "## 5. Full PM brief",
    ):
        assert section in body, f"consolidated brief missing section: {section!r}"

    # 3 numbered next actions
    assert "## Top 3 next actions" in body
    for n in ("1.", "2.", "3."):
        assert n in body

    # Bilingual disclaimer footer (Article 8)
    assert "Estimated outcomes are not guaranteed outcomes" in body
    assert "النتائج التقديرية ليست نتائج مضمونة" in body


def test_daily_routine_is_idempotent():
    """Running twice in a row must produce the same consolidated brief
    without error (cron may invoke daily and on-demand)."""
    script = [sys.executable, str(REPO / "scripts" / "daily_routine.py"), "--quick"]
    first = subprocess.run(script, capture_output=True, text=True, timeout=180, check=False, cwd=str(REPO))
    assert first.returncode == 0
    second = subprocess.run(script, capture_output=True, text=True, timeout=180, check=False, cwd=str(REPO))
    assert second.returncode == 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    brief_path = REPO / "data" / "daily_routine" / f"{today}.md"
    assert brief_path.exists()
