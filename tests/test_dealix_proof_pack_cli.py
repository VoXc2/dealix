"""Tests for scripts/dealix_proof_pack.py."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_proof_pack.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_proof_pack
        return dealix_proof_pack
    finally:
        sys.path.pop(0)


def test_script_exists_and_has_shebang():
    assert SCRIPT.exists()
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3")


def test_no_events_returns_exit_1(tmp_path, capsys):
    mod = _import_module()
    rc = mod.main([
        "--customer-handle", "NOPE",
        "--events-dir", str(tmp_path),
    ])
    assert rc == 1
    err = capsys.readouterr().err
    assert "no events" in err.lower()


def test_assembles_markdown_from_jsonl(tmp_path, capsys):
    """Round-trip: write 3 events to JSONL, render the pack."""
    events_dir = tmp_path / "events"
    events_dir.mkdir()
    jsonl = events_dir / "2026-05-04.jsonl"

    handle = "ACME-Saudi-Pilot-EXAMPLE"
    sample = [
        {
            "id": "evt_001",
            "event_type": "delivery_task_completed",
            "customer_handle": handle,
            "service_id": "lead_intake_whatsapp",
            "outcome_metric": "qualified_opportunities_delivered",
            "outcome_value": 3,
            "consent_for_publication": False,
        },
        {
            "id": "evt_002",
            "event_type": "delivery_task_completed",
            "customer_handle": handle,
            "service_id": "outreach_drafts",
            "outcome_metric": "arabic_drafts_delivered",
            "outcome_value": 4,
            "consent_for_publication": False,
        },
        {
            "id": "evt_003",
            "event_type": "proof_pack_assembled",
            "customer_handle": handle,
            "service_id": "weekly_executive_pack",
            "outcome_metric": "pack_assembled",
            "outcome_value": 1,
            "consent_for_publication": False,
        },
    ]
    with jsonl.open("w", encoding="utf-8") as f:
        for e in sample:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    mod = _import_module()
    rc = mod.main([
        "--customer-handle", handle,
        "--events-dir", str(events_dir),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "approval_status" in out
    assert "Founder approval required before sharing externally" in out


def test_writes_to_out_path(tmp_path):
    events_dir = tmp_path / "events"
    events_dir.mkdir()
    jsonl = events_dir / "2026-05-04.jsonl"
    with jsonl.open("w", encoding="utf-8") as f:
        f.write(json.dumps({
            "id": "evt_x",
            "event_type": "delivery_task_completed",
            "customer_handle": "ACME",
            "service_id": "lead_intake_whatsapp",
            "outcome_metric": "qualified_opportunities_delivered",
            "outcome_value": 1,
            "consent_for_publication": False,
        }, ensure_ascii=False) + "\n")

    out_path = tmp_path / "pack.md"
    mod = _import_module()
    rc = mod.main([
        "--customer-handle", "ACME",
        "--events-dir", str(events_dir),
        "--out", str(out_path),
    ])
    assert rc == 0
    assert out_path.exists()
    text = out_path.read_text(encoding="utf-8")
    assert "approval_status" in text


def test_filters_by_customer_handle(tmp_path):
    """Events for a different customer must not leak into the pack."""
    events_dir = tmp_path / "events"
    events_dir.mkdir()
    jsonl = events_dir / "2026-05-04.jsonl"
    base_event = {
        "event_type": "delivery_task_completed",
        "service_id": "lead_intake_whatsapp",
        "outcome_metric": "qualified_opportunities_delivered",
        "outcome_value": 1,
        "consent_for_publication": False,
    }
    with jsonl.open("w", encoding="utf-8") as f:
        f.write(json.dumps({**base_event, "id": "evt_a", "customer_handle": "ACME"}, ensure_ascii=False) + "\n")
        f.write(json.dumps({**base_event, "id": "evt_b", "customer_handle": "OTHER"}, ensure_ascii=False) + "\n")

    mod = _import_module()
    out_path = tmp_path / "pack.md"
    rc = mod.main([
        "--customer-handle", "ACME",
        "--events-dir", str(events_dir),
        "--out", str(out_path),
    ])
    assert rc == 0
    text = out_path.read_text(encoding="utf-8")
    # ACME events present; OTHER events MUST not leak in
    assert "ACME" in text
    assert "OTHER" not in text
