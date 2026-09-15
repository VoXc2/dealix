from __future__ import annotations

from auto_client_acquisition.company_brain_mvp.memory import ingest_chunk, query_workspace, reset_workspace
from dealix.commercial.commercial_truth_authority import (
    CURRENT_AUTHORITY,
    DEPRECATED_REPLACED,
    HISTORICAL_REFERENCE_NON_AUTHORITATIVE,
    SYNTHETIC_DEMO_ONLY,
    UNCLASSIFIED_CONTEXT,
    classify_source,
    should_exclude_from_current_retrieval,
)


def test_current_policy_is_authority() -> None:
    for source in (
        "config/company/fresh_market_execution_policy.json",
        "config/company/agentic_holding_canonical_contract.json",
        "config/company/saudi_market_signal_snapshot_2026_09_13.json",
        "landing/public-surface-manifest.json",
        "landing/assets/data/services-catalog.json",
    ):
        assert classify_source(source) == CURRENT_AUTHORITY
        assert not should_exclude_from_current_retrieval(source)


def test_phase_e_is_deprecated_even_without_price_marker() -> None:
    source = "docs/phase-e/05_PILOT_499_OFFER.md"
    assert classify_source(source) == DEPRECATED_REPLACED
    assert should_exclude_from_current_retrieval(source)


def test_demo_material_is_synthetic_only() -> None:
    source = "business/demo/DEMO_CLOSE.md"
    assert classify_source(source) == SYNTHETIC_DEMO_ONLY
    assert should_exclude_from_current_retrieval(source)


def test_unlisted_repo_doc_with_legacy_price_marker_is_historical() -> None:
    source = "docs/sectors/CLINICS_AR.md"
    text = "Revenue Intelligence Sprint — 499 ريال"
    assert classify_source(source, text=text) == HISTORICAL_REFERENCE_NON_AUTHORITATIVE
    assert should_exclude_from_current_retrieval(source, text=text)


def test_unlisted_repo_doc_with_legacy_fixed_duration_pilot_is_historical() -> None:
    source = "docs/playbooks/hospitality_events.md"
    text = "After 7-day Pilot: Arabic replies, demos booked, qualified leads."
    assert classify_source(source, text=text) == HISTORICAL_REFERENCE_NON_AUTHORITATIVE
    assert should_exclude_from_current_retrieval(source, text=text)


def test_unlisted_repo_doc_with_arabic_fixed_five_marketing_is_historical() -> None:
    source = "docs/MARKETING_AND_CONTENT_SYSTEM.md"
    text = "فريق AI لشركتك — 5 وكلاء، عمل حقيقي"
    assert classify_source(source, text=text) == HISTORICAL_REFERENCE_NON_AUTHORITATIVE
    assert should_exclude_from_current_retrieval(source, text=text)


def test_unlisted_repo_code_with_old_five_plus_eight_architecture_is_historical() -> None:
    source = "dealix/commercial/delix_service_preparation.py"
    text = "Dealix — 5 وكلاء + 8 موسعون، 44 ذراع، 500 خلية"
    assert classify_source(source, text=text) == HISTORICAL_REFERENCE_NON_AUTHORITATIVE
    assert should_exclude_from_current_retrieval(source, text=text)


def test_legacy_one_company_five_core_marker_is_historical() -> None:
    source = "docs/agents/EXPANDED_STAFF_REGISTRY.md"
    text = "One Company, Five Core"
    assert classify_source(source, text=text) == HISTORICAL_REFERENCE_NON_AUTHORITATIVE
    assert should_exclude_from_current_retrieval(source, text=text)


def test_old_pricing_document_is_explicitly_historical() -> None:
    assert classify_source("docs/pricing.md") == HISTORICAL_REFERENCE_NON_AUTHORITATIVE
    assert should_exclude_from_current_retrieval("docs/pricing.md")


def test_customer_context_is_not_hidden_just_because_it_contains_499() -> None:
    source = "customer_uploaded_quote"
    text = "Customer says the approved line item is 499 SAR."
    assert classify_source(source, text=text) == UNCLASSIFIED_CONTEXT
    assert not should_exclude_from_current_retrieval(source, text=text)


def test_customer_context_is_not_hidden_just_because_it_says_seven_day_pilot() -> None:
    source = "customer_uploaded_scope"
    text = "Customer asks whether their own internal pilot should run as a 7-day pilot."
    assert classify_source(source, text=text) == UNCLASSIFIED_CONTEXT
    assert not should_exclude_from_current_retrieval(source, text=text)


def test_customer_context_is_not_hidden_just_because_it_mentions_five_agents() -> None:
    source = "customer_uploaded_scope"
    text = "Customer asks whether their own team of 5 agents should be consolidated."
    assert classify_source(source, text=text) == UNCLASSIFIED_CONTEXT
    assert not should_exclude_from_current_retrieval(source, text=text)


def test_company_brain_default_current_mode_quarantines_legacy_price() -> None:
    workspace = "commercial-firewall-current"
    reset_workspace(workspace)
    ingest_chunk(
        workspace_id=workspace,
        source_id="docs/phase-e/05_PILOT_499_OFFER.md",
        text="Pilot 499 SAR for 7 days.",
    )
    ingest_chunk(
        workspace_id=workspace,
        source_id="config/company/fresh_market_execution_policy.json",
        text="Current pricing policy: no public fixed prices; quote is customer-specific after qualified discovery.",
    )
    out = query_workspace(workspace_id=workspace, question="current pricing policy")
    assert out["answer_mode"] == "evidence_backed"
    assert out["commercial_truth_mode"] == "CURRENT_ONLY"
    assert out["citations"][0]["source_id"] == "config/company/fresh_market_execution_policy.json"
    assert out["citations"][0]["commercial_authority_class"] == CURRENT_AUTHORITY
    assert "499" not in out["answer_en"]


def test_company_brain_default_current_mode_quarantines_fixed_five_repo_context() -> None:
    workspace = "commercial-firewall-fixed-five"
    reset_workspace(workspace)
    ingest_chunk(
        workspace_id=workspace,
        source_id="docs/MARKETING_AND_CONTENT_SYSTEM.md",
        text="فريق AI لشركتك — 5 وكلاء، عمل حقيقي",
    )
    ingest_chunk(
        workspace_id=workspace,
        source_id="config/company/agentic_holding_canonical_contract.json",
        text="Current architecture: Dealix Holding -> Sector Companies -> Arm Pods -> Specialist Logical Agents.",
    )
    out = query_workspace(workspace_id=workspace, question="current Dealix agent architecture")
    assert out["answer_mode"] == "evidence_backed"
    assert out["commercial_truth_mode"] == "CURRENT_ONLY"
    assert out["citations"][0]["source_id"] == "config/company/agentic_holding_canonical_contract.json"
    assert "5 وكلاء" not in out["answer_ar"]


def test_company_brain_recomputes_authority_class_at_retrieval() -> None:
    workspace = "commercial-firewall-live-authority"
    reset_workspace(workspace)
    chunk = ingest_chunk(
        workspace_id=workspace,
        source_id="config/company/fresh_market_execution_policy.json",
        text="Current pricing policy is customer-specific after qualified discovery.",
    )
    chunk["commercial_authority_class"] = HISTORICAL_REFERENCE_NON_AUTHORITATIVE
    out = query_workspace(workspace_id=workspace, question="current pricing policy")
    assert out["answer_mode"] == "evidence_backed"
    assert out["commercial_truth_mode"] == "CURRENT_ONLY"
    assert out["citations"][0]["commercial_authority_class"] == CURRENT_AUTHORITY


def test_company_brain_only_legacy_source_is_insufficient_by_default() -> None:
    workspace = "commercial-firewall-only-legacy"
    reset_workspace(workspace)
    ingest_chunk(
        workspace_id=workspace,
        source_id="docs/phase-e/05_PILOT_499_OFFER.md",
        text="Pilot 499 SAR for 7 days.",
    )
    out = query_workspace(workspace_id=workspace, question="pilot 499")
    assert out["answer_mode"] == "insufficient_evidence"
    assert out["citations"] == []
    assert out["commercial_truth_mode"] == "CURRENT_ONLY"


def test_explicit_history_mode_preserves_provenance_without_promoting_authority() -> None:
    workspace = "commercial-firewall-history"
    reset_workspace(workspace)
    ingest_chunk(
        workspace_id=workspace,
        source_id="docs/phase-e/05_PILOT_499_OFFER.md",
        text="Pilot 499 SAR for 7 days.",
    )
    out = query_workspace(workspace_id=workspace, question="pilot 499", include_historical=True)
    assert out["answer_mode"] == "evidence_backed"
    assert out["commercial_truth_mode"] == "HISTORICAL_LOOKUP_ONLY"
    assert out["citations"][0]["commercial_authority_class"] == DEPRECATED_REPLACED


def test_stale_revenue_and_sales_docs_are_explicitly_historical() -> None:
    stale = (
        "docs/ops/FIRST_REVENUE_ATTEMPT.md",
        "docs/ops/manual_payment_log.md",
        "docs/revenue/INVOICE_FLOW.md",
        "docs/revenue/REVENUE_READINESS.md",
        "docs/sales-kit/dealix_invoicing_guide.md",
        "docs/sales-kit/dealix_saudi_business_setup.md",
    )
    for source in stale:
        assert classify_source(source) == HISTORICAL_REFERENCE_NON_AUTHORITATIVE
        assert should_exclude_from_current_retrieval(source)
