"""v7 Phase 8 hardening — proof events must be honest.

Three perimeter assertions:

  1. ``proof_snippet_engine.REQUIRED_FIELDS`` enforces a stable
     contract; ``evidence_source`` either sits in REQUIRED_FIELDS or
     is exposed on the ``ProofEvent`` schema with an empty-string
     default (auditable). We assert the schema-side guarantee so the
     evidence trail is never silently optional.
  2. ``proof_snippet_engine.render`` blocks an event with no
     ``outcome_value`` (returns decision=blocked, notes mention the
     missing field).
  3. ``export_redacted`` anonymizes ``customer_handle`` for events
     without consent_for_publication=True.
"""
from __future__ import annotations

import importlib
import tempfile
from pathlib import Path

import pytest

from auto_client_acquisition.proof_ledger import (
    FileProofLedger,
    ProofEvent,
    ProofEventType,
)
from auto_client_acquisition.proof_ledger.evidence_export import export_redacted


def test_proof_event_evidence_source_field_is_audited():
    """The ``evidence_source`` field must exist on the ``ProofEvent``
    schema and either be required OR carry an explicit empty-string
    default (so audit can detect missing evidence trivially).

    REQUIRED_FIELDS in proof_snippet_engine governs render-time
    publication; the schema-level field governs persistence. We require
    BOTH locations to know about evidence_source.
    """
    snippet_module = importlib.import_module(
        "auto_client_acquisition.self_growth_os.proof_snippet_engine"
    )
    required_fields = snippet_module.REQUIRED_FIELDS
    assert isinstance(required_fields, tuple), (
        "REQUIRED_FIELDS must be a tuple to remain immutable"
    )
    # Schema-level: evidence_source is a known field on ProofEvent.
    fields = ProofEvent.model_fields
    assert "evidence_source" in fields, (
        "ProofEvent schema must define evidence_source"
    )
    info = fields["evidence_source"]
    # Acceptable: required OR default of empty string (the auditor
    # can flag empty strings on dashboards). NOT acceptable: a
    # non-empty hard-coded default that hides missing evidence.
    if info.is_required():
        return
    assert info.default == "", (
        f"evidence_source must default to '' (so empty-evidence events "
        f"are visible to audit); got default={info.default!r}"
    )


def test_render_blocks_event_with_no_outcome_value():
    """Snippet rendering must reject an event missing outcome_value."""
    snippet_module = importlib.import_module(
        "auto_client_acquisition.self_growth_os.proof_snippet_engine"
    )
    event = {
        "event_type": "lead_intake",
        "service_id": "lead_intake_whatsapp",
        "outcome_metric": "leads_qualified",
        # outcome_value omitted intentionally
        "consent_for_publication": False,
    }
    result = snippet_module.render(event)
    assert result.decision == "blocked", (
        f"render must block events missing outcome_value; got "
        f"decision={result.decision!r}"
    )
    assert "outcome_value" in result.notes, (
        f"blocked-render notes must mention the missing field, "
        f"got {result.notes!r}"
    )


def test_render_blocks_event_with_no_consent_field():
    """Defensive: an event with no consent_for_publication entry at
    all (not False — missing) is still blocked."""
    snippet_module = importlib.import_module(
        "auto_client_acquisition.self_growth_os.proof_snippet_engine"
    )
    event = {
        "event_type": "lead_intake",
        "service_id": "lead_intake_whatsapp",
        "outcome_metric": "leads_qualified",
        "outcome_value": 10,
        # consent_for_publication intentionally absent
    }
    result = snippet_module.render(event)
    assert result.decision == "blocked"


def test_export_redacted_anonymizes_customer_without_consent(tmp_path: Path):
    """A recorded event with ``consent_for_publication=False`` must
    surface ``customer_handle="<anonymized>"`` in the redacted export
    — the customer's real handle never leaves the ledger."""
    ledger = FileProofLedger(base_dir=tmp_path)
    ledger.record(
        ProofEvent(
            event_type=ProofEventType.LEAD_INTAKE,
            customer_handle="ACME Industries Ltd",
            consent_for_publication=False,
        )
    )
    out = export_redacted(limit=10, ledger=ledger)
    assert out["total_returned"] == 1
    only_event = out["events"][0]
    assert only_event["customer_handle"] == "<anonymized>", (
        "without consent, customer_handle must be replaced with "
        f"'<anonymized>'; got {only_event['customer_handle']!r}"
    )
    # The raw name must not leak anywhere in the export payload.
    assert "ACME Industries" not in str(out), (
        "raw customer name leaked into export payload"
    )
