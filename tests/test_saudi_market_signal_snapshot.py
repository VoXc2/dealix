from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "config/company/saudi_market_signal_snapshot_2026_09_13.json"
EXPECTED_AUTHORITY = "MARKET_SIGNAL_ONLY_NOT_RELATIONSHIP_NOT_BUYER_DEMAND_NOT_PIPELINE"
FORBIDDEN_TRANSITIONS = {
    "RELATIONSHIP",
    "CONSENT",
    "QUALIFIED_PROBLEM",
    "PIPELINE",
    "QUOTE",
    "INVOICE",
    "REVENUE",
    "PUBLIC_PROOF",
}


def _snapshot() -> dict:
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def _signals_by_id() -> dict[str, dict]:
    payload = _snapshot()
    return {str(signal["id"]): signal for signal in payload["signals"]}


def test_market_snapshot_is_research_authority_only() -> None:
    payload = _snapshot()
    assert payload["authority"] == EXPECTED_AUTHORITY
    laws = set(payload["truth_law"])
    assert "market_signal != named_customer_demand" in laws
    assert "research != relationship" in laws
    assert "public_contact != consent" in laws
    assert "regulatory_deadline != authorization_to_advise_or_certify" in laws
    assert "consultation_document != final_binding_requirement" in laws

    activation = payload["activation_policy"]
    assert FORBIDDEN_TRANSITIONS <= set(activation["market_signal_cannot_create"])
    assert set(activation["market_signal_can_create"]) <= {
        "RESEARCH_JOB",
        "SECTOR_HYPOTHESIS",
        "FREE_DIAGNOSTIC_TEMPLATE",
        "INTERNAL_ACCOUNT_RESEARCH",
    }
    assert "real interaction" in activation["named_customer_progression_requires"].lower()


def test_fatoora_wave_25_is_primary_source_bounded_and_actionable() -> None:
    signal = _signals_by_id()["FATOORA_WAVE_25"]
    assert signal["source_type"] == "official_tax_authority"
    assert signal["source"].startswith("https://www.zatca.gov.sa/")
    assert signal["verified_on"] == "2026-09-13"

    facts = " ".join(signal["facts"]).lower()
    assert "24 july 2026" in facts
    assert "187,500" in facts
    for year in ("2022", "2023", "2024", "2025"):
        assert year in facts
    assert "2027-02-01" in facts
    assert "fatoora" in facts
    assert "format" in facts
    assert "additional invoice fields" in facts

    # The Wave-25 source supports the threshold/deadline/integration contract.
    # It must not be inflated into a penalty/non-compliance/legal-advice claim.
    serialized = json.dumps(signal, ensure_ascii=False).lower()
    assert "penalt" not in facts
    assert "non-compliance" not in facts
    assert "penalties" not in facts
    boundaries = signal["what_it_does_not_prove"].lower()
    assert "tax adviser" in boundaries
    assert "certifier" in boundaries
    assert "named taxpayer" in boundaries
    assert "penalties" in boundaries or "penalty" in boundaries

    uses = {item.lower() for item in signal["dealix_use"]}
    assert "technical integration readiness" in uses
    assert "erp/accounting workflow discovery" in uses
    assert any("evidence-gap" in item for item in uses)
    assert any("data-field" in item for item in uses)


def test_nca_ai_guidelines_remain_closed_consultation_research_evidence() -> None:
    signal = _signals_by_id()["PRIVATE_SECTOR_CYBER_CONTROLS"]
    assert signal["source_type"] == "official_cybersecurity_authority"
    assert any("public-consultations" in source for source in signal.get("additional_sources", []))

    facts = " ".join(signal["facts"]).lower()
    assert "consultation" in facts
    assert "2026-07-05" in facts
    assert "2026-08-05" in facts
    assert "closed" in facts
    for domain in ("governance", "defense", "resilience", "third-party cybersecurity"):
        assert domain in facts
    assert "agentic ai" in facts

    boundaries = signal["what_it_does_not_prove"].lower()
    assert "final binding control" in boundaries
    assert "certification" in boundaries
    assert "applicability to every company" in boundaries


def test_ai_adoption_signal_is_readiness_context_not_buyer_intent() -> None:
    signal = _signals_by_id()["AI_ADOPTION_GUIDE_2026"]
    facts = " ".join(signal["facts"]).lower()
    assert "internal operations" in facts
    assert "customer-facing" in facts
    assert "ai agents" in facts
    for dimension in ("business context", "data", "infrastructure", "skills", "culture"):
        assert dimension in facts
    assert "45.2%" in facts

    boundary = signal["what_it_does_not_prove"].lower()
    for concept in ("named company", "budget", "purchase intent", "authorized outreach"):
        assert concept in boundary


def test_all_signals_have_explicit_proof_and_nonproof_boundaries() -> None:
    payload = _snapshot()
    seen: set[str] = set()
    for signal in payload["signals"]:
        signal_id = str(signal["id"])
        assert signal_id not in seen
        seen.add(signal_id)
        assert signal.get("source")
        assert signal.get("source_type")
        assert signal.get("verified_on") == "2026-09-13"
        assert signal.get("facts")
        assert signal.get("what_it_proves")
        assert signal.get("what_it_does_not_prove")
        assert signal.get("dealix_use")
