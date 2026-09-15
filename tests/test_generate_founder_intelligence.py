from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("founder_intel", ROOT / "scripts/ops/generate_founder_intelligence.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def fixture_tree(tmp_path: Path) -> tuple[Path, Path, Path]:
    current = tmp_path / "current"
    gtm = tmp_path / "gtm"
    repo = tmp_path / "repo"
    write_json(current / "LATEST_TRUTH.json", {
        "generated_at": "2026-09-10T03:50:38+03:00",
        "economic_truth": {
            "real_contacts": 0,
            "paid_pilot_markers": 1,
            "verified_paid_pilots": 0,
            "verified_revenue_sar": 0,
            "generated_pipeline_pressure": "HIGH",
        },
    })
    write_json(current / "ECONOMIC_KPI.json", {
        "generated_at": "2026-09-10T03:50:39+03:00",
        "real_relationships": 0,
        "verified_revenue_sar": 0,
    })
    write_json(gtm / "state/opportunity-summary.json", {
        "production_green": "false",
        "external_send_authorized": False,
        "top": [{"company": "iMini", "score": 74.75, "stage": "QUOTE", "next": "PREPARE_QUOTE_FOLLOWUP"}],
    })
    write_json(gtm / "queues/material-approval-queue.json", [{
        "action": "EMAIL_SEND",
        "target": "iMini",
        "authority_required": "L5_ACTION_BOUND",
        "status": "PREPARED_NOT_EXECUTED",
    }])
    write_json(repo / "reports/probability_revenue_engine/2026-09-15.json", {
        "ranked_targets": [{
            "rank": 1,
            "company_name": "iMini",
            "commercial_stage": "SCRIPT_READY_FOR_REVIEW",
            "evidence_priority": 98.5,
            "next_action": "SEND_SCRIPT_DRAFT_TO_JANNIE — exact action-bound L5 required",
        }],
    })
    return current, gtm, repo


def test_generator_preserves_truth_boundaries_and_writes_atomically(tmp_path: Path) -> None:
    current, gtm, repo = fixture_tree(tmp_path)
    out = current / "HERMES_FOUNDER_INTELLIGENCE.md"
    rc = module.main([
        "--current-dir", str(current), "--gtm-dir", str(gtm), "--repo", str(repo),
        "--output", str(out), "--now", "2026-09-15T06:00:00+03:00", "--source-sha", "abc123",
    ])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "Verified Dealix revenue: **0 SAR**" in text
    assert "Paid-pilot markers: **1**; markers are not payment evidence" in text
    assert "Canonical KPI reports **0** real relationships" in text
    assert "interaction is not silently upgraded" in text
    assert "external_effect=NONE" in text
    assert "L5_ACTION_BOUND" in text
    assert "do not treat HTTP 200 as release parity" in text
    assert "source_sha=abc123" in text


def test_generator_marks_old_truth_stale_and_holds_send(tmp_path: Path) -> None:
    current, gtm, repo = fixture_tree(tmp_path)
    text = module.build_markdown(
        truth=json.loads((current / "LATEST_TRUTH.json").read_text()),
        kpi=json.loads((current / "ECONOMIC_KPI.json").read_text()),
        opportunity=json.loads((gtm / "state/opportunity-summary.json").read_text()),
        approvals=json.loads((gtm / "queues/material-approval-queue.json").read_text()),
        ranked=module.first_ranked(repo, "2026-09-15"),
        now=module.parse_time("2026-09-15T06:00:00+03:00"),
        source_sha="abc123",
    )
    assert "Source freshness is **STALE**" in text
    assert "execution remains held for exact action-bound authority" in text
    assert "Review and improve the existing **iMini** draft/qualification packet internally" in text


def test_missing_required_truth_does_not_overwrite_existing_output(tmp_path: Path) -> None:
    current = tmp_path / "current"
    current.mkdir()
    out = current / "HERMES_FOUNDER_INTELLIGENCE.md"
    out.write_text("KEEP_ME", encoding="utf-8")
    write_json(current / "ECONOMIC_KPI.json", {"generated_at": "2026-09-15T05:00:00+03:00"})
    try:
        module.main(["--current-dir", str(current), "--output", str(out), "--now", "2026-09-15T06:00:00+03:00"])
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("missing truth must fail closed")
    assert out.read_text(encoding="utf-8") == "KEEP_ME"
