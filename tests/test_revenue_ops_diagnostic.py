"""Tests for the Revenue Ops Diagnostic core (create, score, upload, passport)."""

from __future__ import annotations

from auto_client_acquisition.commercial_os.engine import CommercialEngine
from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore
from auto_client_acquisition.revenue_ops.decision_passport import (
    build_decision_passport,
)
from auto_client_acquisition.revenue_ops.diagnostic import create_diagnostic
from auto_client_acquisition.revenue_ops.scoring import (
    READINESS_SIGNALS,
    score_readiness,
)
from auto_client_acquisition.revenue_ops.upload import intake_csv


def _engine() -> CommercialEngine:
    return CommercialEngine(store=InMemoryEventStore())


def test_create_diagnostic_records_cel2_prepared() -> None:
    engine = _engine()
    diag = create_diagnostic(
        customer_id="c1", account_id="acc1", engine=engine
    )
    assert diag.service_id == "governed_revenue_ops_diagnostic"
    assert diag.cel == "CEL2"
    assert diag.commercial_state == "prepared_not_sent"
    # An event was recorded into the store.
    events = list(engine.store.read_for_customer("c1"))
    assert len(events) == 1
    assert events[0].event_type == "commercial.prepared"


def test_score_readiness_is_deterministic_and_bounded() -> None:
    empty = score_readiness({})
    assert empty.score == 0
    assert empty.band == "foundational_gaps"

    full = score_readiness({s: True for s in READINESS_SIGNALS})
    assert full.score == 100
    assert full.band == "ai_ready"

    # Same input -> same output.
    a = score_readiness({"crm_source_documented": True})
    b = score_readiness({"crm_source_documented": True})
    assert a == b


def test_intake_csv_parses_and_rejects_empty() -> None:
    ok = intake_csv("name,email\nAcme Co,info@acme.test\n")
    assert ok.ok is True
    assert ok.row_count >= 1

    empty = intake_csv("")
    assert empty.ok is False
    assert empty.error == "empty_csv"


def test_build_decision_passport_recommends_next_service() -> None:
    score = score_readiness(
        {"crm_source_documented": True, "pipeline_stages_defined": True}
    )
    passport = build_decision_passport(
        diagnostic_id="diag_x",
        customer_id="c1",
        account_id="acc1",
        readiness=score,
    )
    assert passport.is_estimate is True
    assert passport.recommended_next_service in {
        "revenue_intelligence_sprint",
        "governed_ops_retainer",
        "crm_data_readiness_for_ai",
    }
    assert "guarantee" not in passport.rationale_en.lower()
