"""V11 Phase 8 — proof pack v11 readiness tests.

Asserts:
- ``--allow-empty`` produces a clearly-marked Draft / Internal pack
- Empty pack contains NO fabricated events / metrics / testimonials
- Empty pack is bilingual (Arabic + English)
- Empty pack carries ``approval_status: approval_required``,
  ``audience: internal_only``, ``decision: review_required``
- Without ``--allow-empty`` and no events, script exits non-zero
- No forbidden tokens (`نضمن` / `guaranteed` / `blast` / `scrape`)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "dealix_proof_pack.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp"},
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_no_events_without_allow_empty_returns_nonzero(tmp_path: Path) -> None:
    """Honest behavior: no events + no --allow-empty → fail loudly."""
    r = _run(
        "--customer-handle", "Customer-Slot-A",
        "--events-dir", str(tmp_path),  # empty dir
    )
    assert r.returncode != 0
    assert "no events" in r.stderr.lower() or "fabricate" in r.stderr.lower()


def test_allow_empty_produces_draft_internal_pack(tmp_path: Path) -> None:
    r = _run(
        "--customer-handle", "Customer-Slot-A",
        "--events-dir", str(tmp_path),
        "--allow-empty",
    )
    assert r.returncode == 0, f"stderr={r.stderr}"
    out = r.stdout
    # Required markers
    assert "approval_status: approval_required" in out
    assert "audience: internal_only" in out
    assert "decision: review_required" in out
    assert "EMPTY DRAFT" in out


def test_empty_pack_is_bilingual(tmp_path: Path) -> None:
    r = _run(
        "--customer-handle", "Customer-Slot-A",
        "--events-dir", str(tmp_path),
        "--allow-empty",
        "--lang", "both",
    )
    assert r.returncode == 0
    # Arabic markers
    assert "الملخّص" in r.stdout
    assert "لم يتم تسجيل" in r.stdout
    # English markers
    assert "Summary" in r.stdout
    assert "No verifiable events" in r.stdout


def test_empty_pack_does_not_fabricate(tmp_path: Path) -> None:
    r = _run(
        "--customer-handle", "Customer-Slot-A",
        "--events-dir", str(tmp_path),
        "--allow-empty",
    )
    out = r.stdout
    # No fabricated metrics
    forbidden_substrings = (
        "10 leads",
        "5 deals",
        "guaranteed",
        "نضمن لكم",
        "blast",
        "scrape every",
        "100% ROI",
        "10x growth",
    )
    for f in forbidden_substrings:
        assert f not in out, f"empty pack contains fabricated/forbidden: {f}"


def test_empty_pack_writes_to_file(tmp_path: Path) -> None:
    out_path = tmp_path / "empty_pack.md"
    r = _run(
        "--customer-handle", "Customer-Slot-A",
        "--events-dir", str(tmp_path),
        "--allow-empty",
        "--out", str(out_path),
    )
    assert r.returncode == 0
    assert out_path.exists()
    text = out_path.read_text(encoding="utf-8")
    assert "EMPTY DRAFT" in text
    assert "approval_status: approval_required" in text


def test_empty_pack_explicitly_says_internal_only(tmp_path: Path) -> None:
    """V11 hard rule: every pack starts internal-only."""
    r = _run(
        "--customer-handle", "Customer-Slot-A",
        "--events-dir", str(tmp_path),
        "--allow-empty",
    )
    assert "internal_only" in r.stdout
