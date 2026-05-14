"""Weekly CEO Review — Wave 18."""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _iso_week() -> str:
    d = datetime.now(timezone.utc)
    iso_year, iso_week, _ = d.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def test_weekly_ceo_review_imports_cleanly():
    script = REPO / "scripts" / "weekly_ceo_review.py"
    assert script.exists()
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_weekly_ceo_review_emits_markdown_with_required_sections():
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "weekly_ceo_review.py")],
        capture_output=True, text=True, timeout=60, check=False, cwd=str(REPO),
    )
    assert result.returncode == 0, f"weekly review failed:\n{result.stderr}"
    week = _iso_week()
    out = REPO / "data" / "weekly_ceo_review" / f"{week}.md"
    assert out.exists(), f"weekly review markdown not written: {out}"
    body = out.read_text(encoding="utf-8")
    for section in (
        "## 1. Where we are in the 90-day plan",
        "## 2. Commercial pacing",
        "## 3. Anchor partner pipeline",
        "## 4. Capital + friction",
        "## 5. Doctrine health",
        "## Top 3 decisions for next week",
    ):
        assert section in body, f"missing section: {section!r}"
    # Bilingual disclaimer footer
    assert "Estimated outcomes are not guaranteed outcomes" in body
    assert "النتائج التقديرية ليست نتائج مضمونة" in body
    # 3 numbered decisions
    decisions = re.findall(r"^[123]\. ", body, flags=re.MULTILINE)
    assert len(decisions) >= 3, f"expected 3 numbered decisions, got {len(decisions)}"


def test_weekly_ceo_review_is_idempotent():
    script = [sys.executable, str(REPO / "scripts" / "weekly_ceo_review.py")]
    first = subprocess.run(script, capture_output=True, text=True, timeout=60, check=False, cwd=str(REPO))
    assert first.returncode == 0
    second = subprocess.run(script, capture_output=True, text=True, timeout=60, check=False, cwd=str(REPO))
    assert second.returncode == 0


def test_weekly_ceo_review_json_mode_emits_payload():
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "weekly_ceo_review.py"), "--json"],
        capture_output=True, text=True, timeout=60, check=False, cwd=str(REPO),
    )
    assert result.returncode == 0
    import json
    payload = json.loads(result.stdout)
    for field in (
        "week", "generated_at", "capital_assets", "friction",
        "renewals", "anchor_partners", "doctrine", "cadence",
        "top_three_decisions", "output_path",
    ):
        assert field in payload, f"--json mode missing field: {field}"
    assert len(payload["top_three_decisions"]) == 3
