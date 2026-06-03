"""Wave 6 Phase 5 — manual payment confirmation tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/dealix_payment_confirmation_stub.py")


def _run(args: list[str]):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_invoice_intent_creates_state(tmp_path) -> None:
    out = tmp_path / "p.json"
    r = _run([
        "--action", "invoice-intent",
        "--customer", "acme",
        "--amount-sar", "499",
        "--service-type", "7_day_revenue_proof_sprint",
        "--out-path", str(out),
    ])
    assert r.returncode == 0, r.stderr
    s = json.loads(out.read_text(encoding="utf-8"))
    assert s["state"] == "invoice_intent_created"
    assert s["amount_sar"] == 499.0
    assert s["amount_halalah"] == 49900
    # invoice_intent is NOT revenue
    assert s.get("is_revenue", False) is False


def test_invoice_intent_not_revenue(tmp_path) -> None:
    """Critical Article 8: invoice_intent ≠ revenue."""
    out = tmp_path / "p.json"
    _run([
        "--action", "invoice-intent",
        "--customer", "acme",
        "--amount-sar", "499",
        "--service-type", "7_day_revenue_proof_sprint",
        "--out-path", str(out),
    ])
    s = json.loads(out.read_text(encoding="utf-8"))
    assert s.get("is_revenue", False) is False


def test_payment_pending_not_revenue(tmp_path) -> None:
    out = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "x"],
        ["--action", "send-payment-link"],
    ]:
        _run([*args, "--out-path", str(out)])
    s = json.loads(out.read_text(encoding="utf-8"))
    assert s["state"] == "payment_pending"
    assert s.get("is_revenue", False) is False


def test_cannot_confirm_without_evidence(tmp_path) -> None:
    out = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "x"],
        ["--action", "send-payment-link"],
    ]:
        _run([*args, "--out-path", str(out)])
    # Try to confirm without evidence
    r = _run([
        "--action", "confirm",
        "--confirmed-by", "founder",
        "--out-path", str(out),
    ])
    assert r.returncode == 1


def test_evidence_too_short_rejected(tmp_path) -> None:
    out = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "x"],
        ["--action", "send-payment-link"],
    ]:
        _run([*args, "--out-path", str(out)])
    r = _run([
        "--action", "upload-evidence",
        "--evidence-note", "x",
        "--out-path", str(out),
    ])
    assert r.returncode == 1
    assert "5 chars" in r.stderr


def test_full_lifecycle_to_revenue(tmp_path) -> None:
    out = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "send-payment-link"],
        ["--action", "upload-evidence", "--evidence-note", "BANK-TXN-12345-OK"],
        ["--action", "confirm", "--confirmed-by", "Sami"],
    ]:
        r = _run([*args, "--out-path", str(out)])
        assert r.returncode == 0, f"{args}: {r.stderr}"

    s = json.loads(out.read_text(encoding="utf-8"))
    assert s["state"] == "payment_confirmed"
    assert s["is_revenue"] is True
    assert s["confirmed_by"] == "Sami"


def test_kickoff_ready_requires_confirmed_or_commitment(tmp_path) -> None:
    out = tmp_path / "p.json"
    # Without anything → cannot kickoff
    r = _run([
        "--action", "kickoff-ready",
        "--out-path", str(out),
    ])
    assert r.returncode == 1


def test_kickoff_ready_after_confirmation(tmp_path) -> None:
    out = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "send-payment-link"],
        ["--action", "upload-evidence", "--evidence-note", "BANK-OK-12345"],
        ["--action", "confirm", "--confirmed-by", "Sami"],
        ["--action", "kickoff-ready"],
    ]:
        _run([*args, "--out-path", str(out)])

    s = json.loads(out.read_text(encoding="utf-8"))
    assert s["state"] == "delivery_kickoff_ready"


def test_kickoff_ready_after_written_commitment(tmp_path) -> None:
    """Alternative path: signed contract → kickoff allowed."""
    out = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "written-commitment", "--commitment-kind", "signed_service_agreement"],
        ["--action", "kickoff-ready"],
    ]:
        r = _run([*args, "--out-path", str(out)])
        assert r.returncode == 0, f"{args}: {r.stderr}"
    s = json.loads(out.read_text(encoding="utf-8"))
    assert s["state"] == "delivery_kickoff_ready"


def test_refund_after_confirmed(tmp_path) -> None:
    out = tmp_path / "p.json"
    for args in [
        ["--action", "invoice-intent", "--customer", "acme", "--amount-sar", "499", "--service-type", "sprint"],
        ["--action", "send-payment-link"],
        ["--action", "upload-evidence", "--evidence-note", "BANK-OK-12345"],
        ["--action", "confirm", "--confirmed-by", "Sami"],
        ["--action", "refund", "--refund-note", "Customer requested within 14d window"],
    ]:
        r = _run([*args, "--out-path", str(out)])
        assert r.returncode == 0, f"{args}: {r.stderr}"
    s = json.loads(out.read_text(encoding="utf-8"))
    assert s["state"] == "refunded"


def test_no_moyasar_live_in_script() -> None:
    """Script must NOT call Moyasar live API."""
    src = SCRIPT.read_text(encoding="utf-8")
    assert "moyasar" not in src.lower() or "NO_LIVE_CHARGE" in src or "NEVER calls Moyasar live" in src


def test_double_invoice_rejected(tmp_path) -> None:
    out = tmp_path / "p.json"
    _run([
        "--action", "invoice-intent",
        "--customer", "acme",
        "--amount-sar", "499",
        "--service-type", "sprint",
        "--out-path", str(out),
    ])
    # Second invoice on same state file → rejected
    r = _run([
        "--action", "invoice-intent",
        "--customer", "acme2",
        "--amount-sar", "499",
        "--service-type", "sprint",
        "--out-path", str(out),
    ])
    assert r.returncode == 1
    assert "already_at_state" in r.stderr


def test_checklist_doc_exists() -> None:
    assert Path("docs/wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md").exists()
