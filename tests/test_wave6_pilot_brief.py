"""Canonical Pilot scope renderer tests.

The historical Wave 6 public 499 SAR / 7-day sprint contract is retired. The
compatibility command now renders a non-binding 30-day Revenue Command Pilot
scope only after a customer-specific quote evidence reference is supplied.
These tests guard the current quote-only authority rather than resurrecting the
retired public price/refund ladder.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/dealix_pilot_brief.py")
QUOTE_REF = "QUOTE-EVIDENCE-TEST-001"


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _valid_args(tmp_path: Path) -> tuple[list[str], Path, Path]:
    out_md = tmp_path / "b.md"
    out_json = tmp_path / "b.json"
    return (
        [
            "--company", "Test Co",
            "--sector", "real_estate",
            "--quote-evidence-id", QUOTE_REF,
            "--out-md", str(out_md),
            "--out-json", str(out_json),
        ],
        out_md,
        out_json,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_quote_evidence_is_required_and_failure_writes_nothing(tmp_path) -> None:
    out_md = tmp_path / "b.md"
    out_json = tmp_path / "b.json"
    r = _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    assert r.returncode != 0
    assert not out_md.exists()
    assert not out_json.exists()


def test_valid_brief_is_30_day_quote_only_scope(tmp_path) -> None:
    args, out_md, out_json = _valid_args(tmp_path)
    r = _run(args)
    assert r.returncode == 0, r.stderr
    assert out_md.exists()
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["schema"] == "dealix.revenue_command_pilot_scope_draft.v1"
    assert b["truth_class"] == "DRAFT_NOT_SENT"
    assert b["duration_days"] == 30
    assert b["quote_evidence_id"] == QUOTE_REF
    assert b["price_sar"] is None
    assert b["payment_terms"] is None
    assert b["refund_policy"] is None
    assert b["outcome_guarantee"] is None
    assert b["approval_required_for_commitment"] is True


def test_any_legacy_amount_is_rejected(tmp_path) -> None:
    for amount in (1, 100, 499, 1500):
        out_md = tmp_path / f"b-{amount}.md"
        out_json = tmp_path / f"b-{amount}.json"
        r = _run([
            "--company", "Test Co",
            "--sector", "consulting",
            "--quote-evidence-id", QUOTE_REF,
            "--amount-sar", str(amount),
            "--out-md", str(out_md),
            "--out-json", str(out_json),
        ])
        assert r.returncode == 2
        assert "PRICE_NOT_AUTHORIZED_BY_PILOT_BRIEF" in r.stderr
        assert not out_md.exists()
        assert not out_json.exists()


def test_artifact_grants_no_payment_send_or_execution_authority(tmp_path) -> None:
    args, _, out_json = _valid_args(tmp_path)
    r = _run(args)
    assert r.returncode == 0, r.stderr
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["external_send_allowed"] is False
    assert b["execution_allowed"] is False
    excluded = set(b["what_is_not_authorized_by_this_artifact"])
    assert "payment_or_invoice" in excluded
    assert "contract_or_legal_term" in excluded
    assert "external_send_or_public_publish" in excluded
    assert "production_or_customer_system_mutation" in excluded


def test_brief_requires_current_commercial_preconditions(tmp_path) -> None:
    args, _, out_json = _valid_args(tmp_path)
    r = _run(args)
    assert r.returncode == 0, r.stderr
    b = json.loads(out_json.read_text(encoding="utf-8"))
    required = set(b["required_before_commitment"])
    assert "qualified_discovery" in required
    assert "customer_specific_scope" in required
    assert "acceptance_criteria" in required
    assert "quote_or_commercial_terms_approved_by_applicable_authority" in required
    assert "external_action_gates_satisfied" in required


def test_markdown_is_bilingual_and_explicitly_non_binding(tmp_path) -> None:
    args, out_md, _ = _valid_args(tmp_path)
    r = _run(args)
    assert r.returncode == 0, r.stderr
    md = out_md.read_text(encoding="utf-8")
    assert "المسار التجاري الحالي" in md
    assert "ملخص التشخيص والاستكشاف" in md
    assert "مسودة النطاق" in md
    assert "المطلوب قبل الالتزام" in md
    assert "غير مصرح به هنا" in md
    assert "not a price quote" in md
    assert "ليست تسعيرة" in md


def test_no_invoice_or_payment_provider_api_call() -> None:
    """Renderer is local-only and cannot create live commercial effects."""
    src = SCRIPT.read_text(encoding="utf-8")
    assert "requests.post" not in src
    assert "httpx.post" not in src
    assert "urllib.request.urlopen" not in src
    assert "moyasar" not in src.lower()


def test_diagnostic_file_summary_is_preserved(tmp_path) -> None:
    diag = tmp_path / "diag.json"
    diag.write_text(
        json.dumps({"executive_summary_ar": "ملخّص التشخيص للاختبار"}),
        encoding="utf-8",
    )
    args, _, out_json = _valid_args(tmp_path)
    args[args.index("--out-md"):args.index("--out-md")] = [
        "--diagnostic-file", str(diag)
    ]
    r = _run(args)
    assert r.returncode == 0, r.stderr
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert "ملخّص التشخيص" in b["diagnostic_summary"]


def test_missing_diagnostic_evidence_is_labelled_unknown(tmp_path) -> None:
    args, _, out_json = _valid_args(tmp_path)
    r = _run(args)
    assert r.returncode == 0, r.stderr
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["diagnostic_summary"] == "UNKNOWN_NOT_EVIDENCE_BACKED"


def test_dry_run_emits_draft_but_does_not_write_default_artifacts(tmp_path) -> None:
    r = _run([
        "--company", "Test Co",
        "--sector", "services",
        "--quote-evidence-id", QUOTE_REF,
        "--dry-run",
    ])
    assert r.returncode == 0, r.stderr
    assert "DRAFT_NOT_SENT" in r.stdout
    assert "Revenue Command Pilot" in r.stdout
