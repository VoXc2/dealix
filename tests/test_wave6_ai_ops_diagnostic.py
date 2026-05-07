"""Wave 6 Phase 3 — AI Ops Diagnostic generator tests."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/dealix_ai_ops_diagnostic.py")


def _run(args: list[str], cwd: Path | None = None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=cwd,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_diagnostic_real_estate(tmp_path) -> None:
    out_md = tmp_path / "d.md"
    out_json = tmp_path / "d.json"
    r = _run([
        "--company", "Acme Real Estate",
        "--sector", "real_estate",
        "--region", "Riyadh",
        "--problem", "leads not converting",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0, r.stderr
    d = json.loads(out_json.read_text(encoding="utf-8"))
    assert d["company"] == "Acme Real Estate"
    assert d["action_mode"] == "approval_required"
    assert d["no_guaranteed_claims"] is True


def test_diagnostic_includes_3_bottlenecks(tmp_path) -> None:
    out_json = tmp_path / "d.json"
    _run([
        "--company", "Test Co",
        "--sector", "agencies",
        "--region", "Jeddah",
        "--out-md", str(tmp_path / "d.md"),
        "--out-json", str(out_json),
    ])
    d = json.loads(out_json.read_text(encoding="utf-8"))
    assert len(d["full_ops_bottlenecks_ar"]) == 3
    assert len(d["full_ops_bottlenecks_en"]) == 3


def test_diagnostic_includes_5_recommended_agents(tmp_path) -> None:
    out_json = tmp_path / "d.json"
    _run([
        "--company", "Test Co",
        "--sector", "consulting",
        "--region", "Riyadh",
        "--out-md", str(tmp_path / "d.md"),
        "--out-json", str(out_json),
    ])
    d = json.loads(out_json.read_text(encoding="utf-8"))
    assert len(d["recommended_ai_team_ar"]) == 5
    assert len(d["recommended_ai_team_en"]) == 5


def test_diagnostic_no_forbidden_tokens_in_output(tmp_path) -> None:
    """No 'guaranteed' / 'blast' / 'scraping' / 'cold whatsapp' / 'نضمن' in output."""
    out_md = tmp_path / "d.md"
    out_json = tmp_path / "d.json"
    _run([
        "--company", "Test Co",
        "--sector", "services",
        "--region", "Riyadh",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    md_text = out_md.read_text(encoding="utf-8")
    json_text = out_json.read_text(encoding="utf-8")
    for token in [r"\bguaranteed?\b", r"\bblast\b", r"\bscraping\b",
                   r"\bcold\s+whatsapp\b", "نضمن"]:
        assert not re.search(token, md_text, re.IGNORECASE), f"md contains: {token}"
        assert not re.search(token, json_text, re.IGNORECASE), f"json contains: {token}"


def test_diagnostic_unknown_sector_returns_insufficient_data(tmp_path) -> None:
    out_json = tmp_path / "d.json"
    _run([
        "--company", "Unknown Co",
        "--sector", "spaceship_dealer",
        "--region", "Riyadh",
        "--out-md", str(tmp_path / "d.md"),
        "--out-json", str(out_json),
    ])
    d = json.loads(out_json.read_text(encoding="utf-8"))
    # Unknown sector falls back to insufficient_data
    assert any("insufficient_data" in b for b in d["full_ops_bottlenecks_ar"])


def test_diagnostic_what_not_to_automate_includes_gates(tmp_path) -> None:
    out_json = tmp_path / "d.json"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--region", "Riyadh",
        "--out-md", str(tmp_path / "d.md"),
        "--out-json", str(out_json),
    ])
    d = json.loads(out_json.read_text(encoding="utf-8"))
    blob = " ".join(d["what_not_to_automate"]).upper()
    assert "NO_LIVE_SEND" in blob
    assert "NO_LINKEDIN_AUTO" in blob
    assert "NO_LIVE_CHARGE" in blob
    assert "NO_SCRAPING" in blob


def test_diagnostic_recommends_499_sprint(tmp_path) -> None:
    out_json = tmp_path / "d.json"
    _run([
        "--company", "Test Co",
        "--sector", "training",
        "--region", "Eastern",
        "--out-md", str(tmp_path / "d.md"),
        "--out-json", str(out_json),
    ])
    d = json.loads(out_json.read_text(encoding="utf-8"))
    assert "499" in d["recommended_offer"]
    assert "Sprint" in d["recommended_offer"]


def test_diagnostic_works_without_api_keys(tmp_path) -> None:
    """Deterministic template — no API keys required."""
    import os
    # Ensure no API keys are set
    env = {k: v for k, v in os.environ.items() if not any(
        s in k for s in ["ANTHROPIC", "OPENAI", "GOOGLE", "GROQ", "RESEND"]
    )}
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--company", "Test Co",
         "--sector", "real_estate",
         "--region", "Riyadh",
         "--out-md", str(tmp_path / "d.md"),
         "--out-json", str(tmp_path / "d.json")],
        capture_output=True, text=True, env=env,
    )
    assert result.returncode == 0


def test_markdown_includes_arabic_sections(tmp_path) -> None:
    out_md = tmp_path / "d.md"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--region", "Riyadh",
        "--out-md", str(out_md),
        "--out-json", str(tmp_path / "d.json"),
    ])
    md = out_md.read_text(encoding="utf-8")
    assert "ملخّص تنفيذي" in md
    assert "Bottlenecks" in md
    assert "فريق AI المقترح" in md
    assert "خطّة ٧ أيّام" in md


def test_markdown_no_internal_terms(tmp_path) -> None:
    out_md = tmp_path / "d.md"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--region", "Riyadh",
        "--out-md", str(out_md),
        "--out-json", str(tmp_path / "d.json"),
    ])
    md = out_md.read_text(encoding="utf-8")
    for term in ["v11", "v12", "v13", "v14", "growth_beast", "stacktrace", "pytest"]:
        assert term not in md.lower(), f"diagnostic md leaks: {term}"
