"""Wave 6 Phase 7 — proof pack generator tests."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/dealix_wave6_proof_pack.py")


def _run(args: list[str]):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_proof_pack_empty_returns_internal_draft(tmp_path) -> None:
    """No proof events + no --allow-empty → EMPTY_INTERNAL_DRAFT."""
    session = tmp_path / "session.json"
    session.write_text(json.dumps({
        "session_id": "sess_empty",
        "service_type": "7_day_revenue_proof_sprint",
        "proof_event_ids": [],
        "deliverables": [],
    }), encoding="utf-8")
    out_json = tmp_path / "p.json"
    r = _run([
        "--company", "Empty Co",
        "--delivery-session", str(session),
        "--out-md", str(tmp_path / "p.md"),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0
    p = json.loads(out_json.read_text(encoding="utf-8"))
    assert p["status"] == "EMPTY_INTERNAL_DRAFT"
    assert p["public_allowed"] is False
    assert p["is_publishable"] is False


def test_proof_pack_with_events_internal_draft(tmp_path) -> None:
    session = tmp_path / "session.json"
    session.write_text(json.dumps({
        "session_id": "sess_001",
        "service_type": "7_day_revenue_proof_sprint",
        "proof_event_ids": ["pe_001", "pe_002", "pe_003"],
        "deliverables": [{"name": "Lead Audit"}, {"name": "Pipeline Audit"}],
    }), encoding="utf-8")
    out_json = tmp_path / "p.json"
    r = _run([
        "--company", "Acme Co",
        "--delivery-session", str(session),
        "--out-md", str(tmp_path / "p.md"),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0
    p = json.loads(out_json.read_text(encoding="utf-8"))
    assert p["status"] == "INTERNAL_DRAFT"
    assert p["proof_event_count"] == 3
    assert p["deliverable_count"] == 2
    # Still not publishable
    assert p["is_publishable"] is False
    assert p["public_allowed"] is False
    # Hard rules
    assert p["no_fake_proof"] is True
    assert p["no_fake_metrics"] is True
    assert p["no_fake_testimonial"] is True


def test_proof_pack_allow_empty_forced(tmp_path) -> None:
    session = tmp_path / "session.json"
    session.write_text(json.dumps({
        "session_id": "sess_empty",
        "service_type": "7_day_revenue_proof_sprint",
        "proof_event_ids": [],
        "deliverables": [],
    }), encoding="utf-8")
    out_json = tmp_path / "p.json"
    _run([
        "--company", "Empty Co",
        "--delivery-session", str(session),
        "--allow-empty",
        "--out-md", str(tmp_path / "p.md"),
        "--out-json", str(out_json),
    ])
    p = json.loads(out_json.read_text(encoding="utf-8"))
    assert "EMPTY_INTERNAL_DRAFT" in p["status"]


def test_proof_pack_no_session_file_refused(tmp_path) -> None:
    r = _run([
        "--company", "Test Co",
        "--delivery-session", str(tmp_path / "nonexistent.json"),
        "--out-md", str(tmp_path / "p.md"),
        "--out-json", str(tmp_path / "p.json"),
    ])
    assert r.returncode == 2
    assert "REFUSING" in r.stderr


def test_proof_pack_no_forbidden_tokens(tmp_path) -> None:
    session = tmp_path / "session.json"
    session.write_text(json.dumps({
        "session_id": "sess_x",
        "service_type": "sprint",
        "proof_event_ids": ["pe_1"],
        "deliverables": [],
    }), encoding="utf-8")
    out_md = tmp_path / "p.md"
    out_json = tmp_path / "p.json"
    _run([
        "--company", "Test Co",
        "--delivery-session", str(session),
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    md = out_md.read_text(encoding="utf-8")
    js = out_json.read_text(encoding="utf-8")
    for token in [r"\bguaranteed?\b", r"\bblast\b", r"\bscraping\b", "نضمن"]:
        assert not re.search(token, md, re.IGNORECASE), f"md: {token}"
        assert not re.search(token, js, re.IGNORECASE), f"json: {token}"


def test_proof_pack_markdown_arabic_present(tmp_path) -> None:
    session = tmp_path / "session.json"
    session.write_text(json.dumps({
        "session_id": "sess_x",
        "proof_event_ids": ["pe_1"],
        "deliverables": [],
    }), encoding="utf-8")
    out_md = tmp_path / "p.md"
    _run([
        "--company", "Test Co",
        "--delivery-session", str(session),
        "--out-md", str(out_md),
        "--out-json", str(tmp_path / "p.json"),
    ])
    md = out_md.read_text(encoding="utf-8")
    assert "النصّ" in md or "Internal" in md


def test_proof_pack_consent_and_approval_required(tmp_path) -> None:
    session = tmp_path / "session.json"
    session.write_text(json.dumps({
        "session_id": "sess_x",
        "proof_event_ids": ["pe_1"],
        "deliverables": [],
    }), encoding="utf-8")
    out_json = tmp_path / "p.json"
    _run([
        "--company", "Test Co",
        "--delivery-session", str(session),
        "--out-md", str(tmp_path / "p.md"),
        "--out-json", str(out_json),
    ])
    p = json.loads(out_json.read_text(encoding="utf-8"))
    assert p["consent_required"] is True
    assert p["approval_required"] is True
    assert p["redaction_required"] is True
