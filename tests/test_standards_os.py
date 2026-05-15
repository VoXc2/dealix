"""Tests for standards_os (D-GAOS)."""

from __future__ import annotations

from auto_client_acquisition.standards_os import (
    CERTIFICATION_EXAM_COMPONENTS,
    D_GAOS_STANDARD_IDS,
    PARTNER_COVENANT_RULES,
    PROOF_PACK_V2_SECTIONS,
    RuntimeGovernanceDecision,
    SOURCE_PASSPORT_REQUIRED_KEYS,
    agent_autonomy_allowed_in_mvp,
    ai_output_qa_band,
    capital_minimum_bundle_ok,
    certification_exam_components_complete,
    data_readiness_score_band,
    partner_certification_gate,
    proof_pack_v2_sections_complete,
    runtime_governance_decision_valid,
    source_passport_keys_present,
)


def test_d_gaos_registry() -> None:
    assert len(D_GAOS_STANDARD_IDS) == 9


def test_data_readiness_bands() -> None:
    assert data_readiness_score_band(90) == "ready_for_ai_workflow"
    assert data_readiness_score_band(40) == "data_readiness_sprint_first"


def test_source_passport() -> None:
    ok, miss = source_passport_keys_present(frozenset(SOURCE_PASSPORT_REQUIRED_KEYS))
    assert ok and not miss
    assert not source_passport_keys_present(frozenset())[0]


def test_governance_enum() -> None:
    assert runtime_governance_decision_valid(RuntimeGovernanceDecision.DRAFT_ONLY.value)
    assert not runtime_governance_decision_valid("unknown")


def test_agent_mvp_and_qa() -> None:
    assert agent_autonomy_allowed_in_mvp(3)
    assert not agent_autonomy_allowed_in_mvp(4)
    assert ai_output_qa_band(92) == "client_ready"


def test_proof_pack_delegate() -> None:
    full = dict.fromkeys(PROOF_PACK_V2_SECTIONS, "x")
    assert proof_pack_v2_sections_complete(full) == (True, ())


def test_certification_exam() -> None:
    done = frozenset(CERTIFICATION_EXAM_COMPONENTS)
    assert certification_exam_components_complete(done) == (True, ())


def test_capital_bundle() -> None:
    assert capital_minimum_bundle_ok(
        trust_asset_delivered=True,
        product_or_knowledge_asset_delivered=True,
        expansion_path_documented=True,
    )
    assert not capital_minimum_bundle_ok(
        trust_asset_delivered=True,
        product_or_knowledge_asset_delivered=False,
        expansion_path_documented=True,
    )


def test_partner_cert_gate() -> None:
    assert partner_certification_gate(frozenset(PARTNER_COVENANT_RULES))[0]
