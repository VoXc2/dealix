"""V11 Phase 9 — phase E today script tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "dealix_phase_e_today.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp"},
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_text_output_contains_required_sections() -> None:
    r = _run()
    assert r.returncode == 0
    out = r.stdout
    # Bilingual title
    assert "Phase E" in out
    # Hard gates block
    for gate in ("no_live_send", "no_live_charge", "no_scraping",
                 "no_cold_outreach"):
        assert gate in out
    assert out.count("BLOCKED") >= 6
    # Checklist times
    for time in ("08:30", "10:00", "13:00", "16:00", "18:00"):
        assert time in out
    # Next-best action
    assert "Next best action" in out


def test_json_output_is_valid() -> None:
    r = _run("--json")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["schema_version"] == 1
    assert "ksa_date" in data
    assert "checklist" in data
    assert len(data["checklist"]) == 5
    assert all(g == "BLOCKED" for g in data["hard_gates"].values())
    assert "next_best_action" in data
    assert data["next_best_action"]["action_ar"]
    assert data["next_best_action"]["action_en"]


def test_no_external_send_messaging() -> None:
    """Output must NOT instruct any auto-send / cold action."""
    r = _run()
    forbidden = ("auto-send", "automatic blast", "scrape", "cold whatsapp")
    out = r.stdout.lower()
    for f in forbidden:
        assert f not in out, f"forbidden phrase: {f}"


def test_does_not_leak_pii_or_secrets() -> None:
    r = _run()
    out = r.stdout.lower()
    forbidden_prefixes = ("sk_live_", "ghp_", "aiza", "+966")
    for tok in forbidden_prefixes:
        assert tok not in out, f"suspected PII/secret: {tok}"


def test_exit_code_is_zero_always() -> None:
    """This is read-only diagnostics — always exit 0."""
    r = _run()
    assert r.returncode == 0
    r2 = _run("--json")
    assert r2.returncode == 0
