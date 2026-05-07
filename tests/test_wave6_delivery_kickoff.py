"""Wave 6 Phase 6 — delivery kickoff tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/dealix_delivery_kickoff.py")
PAYMENT_SCRIPT = Path("scripts/dealix_payment_confirmation_stub.py")


def _run_kickoff(args: list[str]):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
    )


def _run_payment(args: list[str]):
    return subprocess.run(
        [sys.executable, str(PAYMENT_SCRIPT), *args],
        capture_output=True, text=True,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_kickoff_blocked_without_payment_file(tmp_path) -> None:
    payment = tmp_path / "missing.json"
    out_md = tmp_path / "s.md"
    out_json = tmp_path / "s.json"
    r = _run_kickoff([
        "--company", "Test Co",
        "--service", "7_day_revenue_proof_sprint",
        "--payment-state-file", str(payment),
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 1
    assert "BLOCKED_WAITING_PAYMENT" in r.stderr


def test_kickoff_blocked_at_invoice_intent(tmp_path) -> None:
    """Even with payment file at invoice_intent, kickoff blocked."""
    payment = tmp_path / "p.json"
    _run_payment([
        "--action", "invoice-intent",
        "--customer", "acme",
        "--amount-sar", "499",
        "--service-type", "sprint",
        "--out-path", str(payment),
    ])
    r = _run_kickoff([
        "--company", "Test Co",
        "--service", "7_day_revenue_proof_sprint",
        "--payment-state-file", str(payment),
        "--out-md", str(tmp_path / "s.md"),
        "--out-json", str(tmp_path / "s.json"),
    ])
    assert r.returncode == 1
    assert "BLOCKED_WAITING_PAYMENT" in r.stderr


def test_kickoff_blocked_at_evidence_received(tmp_path) -> None:
    """Even with evidence uploaded, kickoff blocked until confirmation."""
    payment = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "send-payment-link"],
        ["--action", "upload-evidence", "--evidence-note", "BANK-12345"],
    ]:
        _run_payment([*args, "--out-path", str(payment)])
    r = _run_kickoff([
        "--company", "Test Co",
        "--service", "7_day_revenue_proof_sprint",
        "--payment-state-file", str(payment),
        "--out-md", str(tmp_path / "s.md"),
        "--out-json", str(tmp_path / "s.json"),
    ])
    assert r.returncode == 1
    assert "BLOCKED_WAITING_PAYMENT" in r.stderr


def test_kickoff_allowed_after_payment_confirmed(tmp_path) -> None:
    payment = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "send-payment-link"],
        ["--action", "upload-evidence", "--evidence-note", "BANK-12345"],
        ["--action", "confirm", "--confirmed-by", "Sami"],
    ]:
        _run_payment([*args, "--out-path", str(payment)])

    out_json = tmp_path / "s.json"
    r = _run_kickoff([
        "--company", "Test Co",
        "--service", "7_day_revenue_proof_sprint",
        "--payment-state-file", str(payment),
        "--out-md", str(tmp_path / "s.md"),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0, r.stderr
    s = json.loads(out_json.read_text(encoding="utf-8"))
    assert s["state"] == "waiting_inputs"
    assert s["payment_basis"] == "payment_confirmed"
    assert s["is_revenue_basis"] is True


def test_kickoff_allowed_with_written_commitment(tmp_path) -> None:
    payment = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "written-commitment", "--commitment-kind", "signed_service_agreement"],
    ]:
        _run_payment([*args, "--out-path", str(payment)])

    out_json = tmp_path / "s.json"
    r = _run_kickoff([
        "--company", "Test Co",
        "--service", "7_day_revenue_proof_sprint",
        "--payment-state-file", str(payment),
        "--out-md", str(tmp_path / "s.md"),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0, r.stderr
    s = json.loads(out_json.read_text(encoding="utf-8"))
    assert s["payment_basis"] == "written_commitment_received"


def test_kickoff_invalid_service_blocked(tmp_path) -> None:
    payment = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "send-payment-link"],
        ["--action", "upload-evidence", "--evidence-note", "BANK-12345"],
        ["--action", "confirm", "--confirmed-by", "Sami"],
    ]:
        _run_payment([*args, "--out-path", str(payment)])
    r = _run_kickoff([
        "--company", "Test Co",
        "--service", "made_up_service",
        "--payment-state-file", str(payment),
        "--out-md", str(tmp_path / "s.md"),
        "--out-json", str(tmp_path / "s.json"),
    ])
    assert r.returncode == 2


def test_kickoff_session_starts_at_waiting_inputs(tmp_path) -> None:
    payment = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "send-payment-link"],
        ["--action", "upload-evidence", "--evidence-note", "BANK-12345"],
        ["--action", "confirm", "--confirmed-by", "Sami"],
    ]:
        _run_payment([*args, "--out-path", str(payment)])

    out_json = tmp_path / "s.json"
    _run_kickoff([
        "--company", "Test Co",
        "--service", "7_day_revenue_proof_sprint",
        "--payment-state-file", str(payment),
        "--out-md", str(tmp_path / "s.md"),
        "--out-json", str(out_json),
    ])
    s = json.loads(out_json.read_text(encoding="utf-8"))
    assert s["state"] == "waiting_inputs"
    assert s["next_step"]["action"] == "collect_inputs_for_diagnostic"
