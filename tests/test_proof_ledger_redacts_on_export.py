"""Hard rule: proof ledger exports must strip customer_handle +
free-text summaries when consent_for_publication=False.

This test exercises the redaction-on-export contract end-to-end —
the redacted export is what the founder shares with auditors / DPO."""
from __future__ import annotations

import tempfile
from pathlib import Path

from auto_client_acquisition.proof_ledger import (
    FileProofLedger,
    ProofEvent,
    ProofEventType,
    export_redacted,
    export_for_audit,
)


def test_export_redacted_anonymizes_handle_without_consent():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = FileProofLedger(base_dir=Path(tmp))
        ledger.record(ProofEvent(
            event_type=ProofEventType.DELIVERY_TASK_COMPLETED,
            customer_handle="ACME-Saudi-Co",
            summary_ar="تم تسليم 10 فرص.",
            summary_en="Delivered 10 opportunities.",
            consent_for_publication=False,
        ))

        bundle = export_redacted(
            customer_handle="ACME-Saudi-Co",
            ledger=ledger,
        )
        assert bundle["total_returned"] == 1
        ev = bundle["events"][0]
        assert ev["customer_handle"] == "<anonymized>"
        assert ev["summary_ar"] == ""
        assert ev["summary_en"] == ""


def test_export_redacted_preserves_handle_with_consent():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = FileProofLedger(base_dir=Path(tmp))
        ledger.record(ProofEvent(
            event_type=ProofEventType.PROOF_PACK_SENT,
            customer_handle="PublicTestimonialCo",
            summary_ar="نشرت Proof Pack بإذنه.",
            summary_en="Published proof pack with consent.",
            consent_for_publication=True,
        ))

        bundle = export_redacted(
            customer_handle="PublicTestimonialCo",
            ledger=ledger,
        )
        assert bundle["total_returned"] == 1
        ev = bundle["events"][0]
        assert ev["customer_handle"] == "PublicTestimonialCo"


def test_export_redacted_strips_pii_from_summaries():
    """If a summary slips a phone or email through, the redactor
    must catch it on export even if the underlying record stored it."""
    with tempfile.TemporaryDirectory() as tmp:
        ledger = FileProofLedger(base_dir=Path(tmp))
        ledger.record(ProofEvent(
            event_type=ProofEventType.DELIVERY_TASK_COMPLETED,
            customer_handle="ACME",
            summary_ar="اتصل بـ ali@example.sa أو +966501234567",
            summary_en="Email ali@example.sa or +966501234567",
            consent_for_publication=False,
        ))

        bundle = export_redacted(ledger=ledger)
        flat = repr(bundle)
        assert "ali@example.sa" not in flat
        assert "501234567" not in flat


def test_export_for_audit_redacts_unconditionally():
    """The audit export (DPO / SDAIA) redacts EVERYTHING regardless
    of consent. Even consented records get phone/email stripped."""
    with tempfile.TemporaryDirectory() as tmp:
        ledger = FileProofLedger(base_dir=Path(tmp))
        ledger.record(ProofEvent(
            event_type=ProofEventType.PROOF_PACK_SENT,
            customer_handle="ConsentingCo",
            summary_ar="نشرت بـ +966501234567 و ali@example.sa",
            summary_en="Published with +966501234567 and ali@example.sa",
            consent_for_publication=True,
        ))

        audit = export_for_audit(ledger=ledger)
        flat = repr(audit)
        # PII still redacted unconditionally
        assert "501234567" not in flat
        assert "ali@example.sa" not in flat
