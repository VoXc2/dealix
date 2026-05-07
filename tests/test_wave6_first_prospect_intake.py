"""Wave 6 Phase 2 — first prospect intake tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/dealix_first_prospect_intake.py")


def _run(args: list[str], cwd: Path | None = None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=cwd,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_template_exists() -> None:
    assert Path("docs/wave6/FIRST_PROSPECT_INTAKE_TEMPLATE.md").exists()
    assert Path("docs/wave6/FIRST_PROSPECT_INTAKE_TEMPLATE.json").exists()


def test_template_json_is_template_marker() -> None:
    template = json.loads(
        Path("docs/wave6/FIRST_PROSPECT_INTAKE_TEMPLATE.json").read_text(encoding="utf-8")
    )
    assert template["is_template"] is True
    assert template["is_real_data"] is False


def test_intake_writes_to_live_path(tmp_path) -> None:
    out = tmp_path / "intake.json"
    result = _run([
        "--company-name", "Test Co",
        "--sector", "real_estate",
        "--region", "Riyadh",
        "--out-path", str(out),
    ])
    assert result.returncode == 0, result.stderr
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["company_name"] == "Test Co"
    assert data["is_real_data"] is True


def test_intake_rejects_invalid_sector(tmp_path) -> None:
    out = tmp_path / "intake.json"
    result = _run([
        "--company-name", "Test Co",
        "--sector", "made_up_sector",
        "--region", "Riyadh",
        "--out-path", str(out),
    ])
    assert result.returncode == 1
    assert "sector must be one of" in result.stderr


def test_intake_rejects_cold_relationship(tmp_path) -> None:
    """Cold = blocked per Wave 5 tool guardrails."""
    out = tmp_path / "intake.json"
    result = _run([
        "--company-name", "Test Co",
        "--sector", "agencies",
        "--region", "Jeddah",
        "--relationship", "cold",
        "--out-path", str(out),
    ])
    assert result.returncode == 1
    assert "warm_intro" in result.stderr


def test_intake_rejects_email_in_notes(tmp_path) -> None:
    """PII scan blocks raw email."""
    out = tmp_path / "intake.json"
    result = _run([
        "--company-name", "Test Co",
        "--sector", "agencies",
        "--region", "Jeddah",
        "--notes", "contact me at sami@example.com",
        "--out-path", str(out),
    ])
    assert result.returncode == 1
    assert "raw_email" in result.stderr


def test_intake_rejects_phone_in_notes(tmp_path) -> None:
    out = tmp_path / "intake.json"
    result = _run([
        "--company-name", "Test Co",
        "--sector", "consulting",
        "--region", "Riyadh",
        "--notes", "call +966500000000",
        "--out-path", str(out),
    ])
    assert result.returncode == 1
    assert "raw_phone" in result.stderr


def test_intake_refuses_overwrite_without_force(tmp_path) -> None:
    out = tmp_path / "intake.json"
    out.write_text("{}", encoding="utf-8")
    result = _run([
        "--company-name", "Test Co",
        "--sector", "services",
        "--region", "Riyadh",
        "--out-path", str(out),
    ])
    assert result.returncode == 2
    assert "REFUSING" in result.stderr


def test_intake_overwrites_with_force(tmp_path) -> None:
    out = tmp_path / "intake.json"
    out.write_text("{}", encoding="utf-8")
    result = _run([
        "--company-name", "Force Co",
        "--sector", "services",
        "--region", "Riyadh",
        "--out-path", str(out),
        "--force",
    ])
    assert result.returncode == 0
    assert json.loads(out.read_text(encoding="utf-8"))["company_name"] == "Force Co"


def test_intake_default_consent_pending(tmp_path) -> None:
    out = tmp_path / "intake.json"
    _run([
        "--company-name", "Consent Co",
        "--sector", "consulting",
        "--region", "Riyadh",
        "--out-path", str(out),
    ])
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["consent_status"] == "pending"


def test_gitignore_includes_wave6_live() -> None:
    """The live/ directory must be gitignored."""
    gitignore = Path(".gitignore").read_text(encoding="utf-8")
    assert "docs/wave6/live/" in gitignore
