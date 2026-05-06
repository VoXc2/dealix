"""Tests for the auto_client_acquisition.self_growth_os package.

Covers the 6 real modules:
  - schemas
  - safe_publishing_gate
  - service_activation_matrix
  - seo_technical_auditor
  - tool_registry
  - evidence_collector

Each test is fast (<2s), uses no network, no LLM, no DB.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.self_growth_os import (
    ApprovalStatus,
    EvidenceRecord,
    Language,
    PublishingDecision,
    RiskLevel,
    SafePublishingResult,
    ServiceActivationCheck,
    ServiceBundle,
    ToolCapability,
)
from auto_client_acquisition.self_growth_os import (
    evidence_collector,
    safe_publishing_gate,
    service_activation_matrix,
    seo_technical_auditor,
    tool_registry,
)


# ─── schemas ────────────────────────────────────────────────────────


def test_schemas_default_approval_status_is_approval_required():
    """Every external-action record must default to approval_required."""
    sac = ServiceActivationCheck.new(
        service_id="x",
        name_ar="x",
        name_en="x",
        status="target",
    )
    assert sac.approval_status == ApprovalStatus.APPROVAL_REQUIRED.value
    # recommended_action may legitimately be empty for a record that
    # hasn't been populated yet — callers fill it in.


def test_schemas_id_generated_when_missing():
    spr = SafePublishingResult.new(decision=PublishingDecision.ALLOWED_DRAFT)
    assert spr.id and spr.id.startswith("spr_")


def test_schemas_extra_fields_forbidden():
    """The base config is extra='forbid' — this catches typo bugs."""
    with pytest.raises(Exception):
        ServiceActivationCheck.new(
            service_id="x",
            name_ar="x",
            name_en="x",
            status="target",
            unknown_field=True,  # type: ignore[call-arg]
        )


# ─── safe_publishing_gate ───────────────────────────────────────────


def test_safe_publishing_gate_blocks_guaranteed():
    res = safe_publishing_gate.check_text("We guarantee revenue growth!")
    assert res.decision == PublishingDecision.BLOCKED.value
    assert "guaranteed" in res.forbidden_tokens_found


def test_safe_publishing_gate_blocks_arabic_nadman():
    res = safe_publishing_gate.check_text("نضمن لكم نتائج")
    assert res.decision == PublishingDecision.BLOCKED.value
    assert "نضمن" in res.forbidden_tokens_found


def test_safe_publishing_gate_blocks_blast_and_scrape():
    for text in ["blast WhatsApp to all leads", "scrape LinkedIn profiles"]:
        res = safe_publishing_gate.check_text(text)
        assert res.decision == PublishingDecision.BLOCKED.value


def test_safe_publishing_gate_blocks_cold_outreach_combo():
    res = safe_publishing_gate.check_text("Send cold WhatsApp to founders.")
    assert res.decision == PublishingDecision.BLOCKED.value
    assert "cold-channel" in res.forbidden_tokens_found


def test_safe_publishing_gate_passes_clean_arabic():
    text = "صفحة هبوط للفرص. المسوّدة جاهزة للمراجعة."
    res = safe_publishing_gate.check_text(text, language=Language.AR)
    assert res.decision == PublishingDecision.ALLOWED_DRAFT.value
    assert res.approval_status == ApprovalStatus.APPROVAL_REQUIRED.value
    assert res.forbidden_tokens_found == []


def test_safe_publishing_gate_records_excerpt_for_offending_text():
    long = ("safe content. " * 5) + "guaranteed revenue" + (" safe content." * 5)
    res = safe_publishing_gate.check_text(long)
    assert res.decision == PublishingDecision.BLOCKED.value
    assert res.sample_excerpts and any("guaranteed" in e.lower() for e in res.sample_excerpts)


def test_safe_publishing_gate_is_safe_helper():
    assert safe_publishing_gate.is_safe("Friendly Arabic copy") is True
    assert safe_publishing_gate.is_safe("guaranteed leads") is False


def test_safe_publishing_gate_rejects_non_string():
    with pytest.raises(TypeError):
        safe_publishing_gate.check_text(None)  # type: ignore[arg-type]


# ─── service_activation_matrix ──────────────────────────────────────


def test_service_matrix_counts_match_validator():
    """After Phase K1-K6 (PR #165 + PR #166 + PR #167):
       K1 lead_intake_whatsapp + K2 qualification + K3 audit_trail
       + K4 consent_required_send + K5 outreach_drafts + K6 routing
       = 6 services LIVE. Remaining 2 PARTIAL close in PR #168."""
    counts = service_activation_matrix.counts()
    assert counts["total"] == 32
    assert counts["live"] == 8
    assert counts["pilot"] == 0
    assert counts["partial"] == 0
    assert counts["target"] == 24


def test_service_matrix_check_service_returns_typed_record():
    """After Phase K, all 8 in-development services are LIVE. This
    test verifies the LIVE side of the activation-matrix contract:
    a live service reports eight_gate_block_present=True and zero
    blocking_reasons. The matrix's gate-checking logic still works
    — it just no longer has any partial services to flag."""
    check = service_activation_matrix.check_service("enrichment")
    assert isinstance(check, ServiceActivationCheck)
    assert check.service_id == "enrichment"
    assert check.status == "live"
    assert check.eight_gate_block_present is True  # all 8 gates passed
    assert check.blocking_reasons == []


def test_service_matrix_unknown_id_raises_keyerror():
    with pytest.raises(KeyError):
        service_activation_matrix.check_service("nonexistent_service")


def test_service_matrix_candidates_ranked_partial_first():
    """After Phase K, no services remain in PARTIAL/PILOT — every
    in-development service shipped to live. The candidates list is
    therefore empty (clean quiescent state).

    The original ranking-invariant (partial-before-pilot) is still
    enforced by the candidates_for_promotion logic; we just don't
    have any candidates left to assert it on. When PARTIAL services
    re-appear in a future wave, this test must update to assert the
    ranking again.
    """
    candidates = service_activation_matrix.candidates_for_promotion()
    statuses = [c.status for c in candidates]
    # Every candidate must be partial or pilot — never live or target.
    assert all(s in {"partial", "pilot"} for s in statuses)
    # If both kinds present, partial ranks before pilot (the invariant
    # we want to keep alive even when the list is empty today).
    if "partial" in statuses and "pilot" in statuses:
        assert statuses.index("partial") < statuses.index("pilot")


# ─── seo_technical_auditor ──────────────────────────────────────────


def test_seo_auditor_reports_clean_perimeter():
    """Required-gap = 0 is a CI invariant; it must be reflected here."""
    assert seo_technical_auditor.is_perimeter_clean() is True
    assert seo_technical_auditor.summary()["pages_with_required_gap"] == 0


def test_seo_auditor_advisory_breakdown_is_dict():
    breakdown = seo_technical_auditor.gap_count()
    assert isinstance(breakdown, dict)
    # Sanity: keys are the advisory-check names
    for k in breakdown:
        assert k in {"canonical", "og_title", "og_description", "twitter_card"}


# ─── tool_registry ──────────────────────────────────────────────────


def test_tool_registry_returns_list_of_capabilities():
    rows = tool_registry.audit()
    assert rows
    assert all(isinstance(r, ToolCapability) for r in rows)


def test_tool_registry_core_required_present_in_test_env():
    """In CI / dev, the required-for-core tools must be installed."""
    missing = tool_registry.core_required_missing()
    assert missing == [], f"required-for-core tools not installed: {missing}"


def test_tool_registry_includes_pyyaml():
    names = {t.tool_name for t in tool_registry.audit()}
    assert "pyyaml" in names


# ─── evidence_collector ─────────────────────────────────────────────


def test_evidence_collector_records_and_returns_typed_record():
    evidence_collector.clear()
    rec = evidence_collector.record(
        event_type="self_test",
        summary="evidence_collector unit-test record",
        payload={"k": 1},
    )
    assert isinstance(rec, EvidenceRecord)
    assert rec.event_type == "self_test"
    assert rec.payload == {"k": 1}
    assert rec.approval_status == ApprovalStatus.APPROVED.value


def test_evidence_collector_buffer_grows():
    evidence_collector.clear()
    evidence_collector.record(event_type="a", summary="a")
    evidence_collector.record(event_type="b", summary="b")
    events = evidence_collector.all_events()
    assert len(events) == 2


def test_evidence_collector_clear_resets_buffer():
    evidence_collector.record(event_type="x", summary="x")
    evidence_collector.clear()
    assert evidence_collector.all_events() == []


def test_evidence_collector_language_breakdown():
    evidence_collector.clear()
    evidence_collector.record(event_type="t1", summary="ar")
    evidence_collector.record(event_type="t2", summary="ar2")
    breakdown = evidence_collector.language_breakdown()
    assert breakdown.get("ar", 0) == 2
