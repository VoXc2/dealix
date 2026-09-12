import importlib.util
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_proposal.py"
spec = importlib.util.spec_from_file_location("dealix_generate_proposal", SCRIPT)
assert spec and spec.loader
proposal_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proposal_module)


def test_research_live_proposal_is_blocked() -> None:
    allowed, artifact_kind, basis = proposal_module.proposal_gate(
        mode="live",
        qualification_state="RESEARCH_ONLY",
        explicit_customer_request=False,
        problem_evidence_refs=[],
    )

    assert allowed is False
    assert artifact_kind == "BLOCKED"
    assert basis == "QUALIFIED_PROBLEM_OR_EXPLICIT_REQUEST_REQUIRED"


def test_qualified_problem_allows_customer_draft_without_price_authority() -> None:
    allowed, artifact_kind, basis = proposal_module.proposal_gate(
        mode="live",
        qualification_state="QUALIFIED_PROBLEM",
        explicit_customer_request=False,
        problem_evidence_refs=["customer::problem-1"],
    )
    assert allowed is True
    assert artifact_kind == "CUSTOMER_PROPOSAL_DRAFT"
    assert basis == "QUALIFIED_PROBLEM"

    proposal = proposal_module.build_proposal(
        proposal_module.DEMO_ACCOUNT,
        "Revenue Command Pilot",
        "en",
        "TBD_AFTER_DISCOVERY",
        "live",
        "QUALIFIED_PROBLEM",
        ["customer::problem-1"],
        artifact_kind,
        basis,
        proposal_module.UNKNOWN,
    )
    assert proposal["29_commercial_structure"]["status"] == "FOUNDER_APPROVAL_REQUIRED"
    assert proposal["29_commercial_structure"]["fixed_public_price"] is False
    assert proposal["pricing"]["setup"] == "FOUNDER_APPROVAL_REQUIRED"
    assert proposal["meta"]["external_send_authority"] is False


def test_explicit_customer_request_allows_draft_without_faking_qualification() -> None:
    allowed, artifact_kind, basis = proposal_module.proposal_gate(
        mode="live",
        qualification_state="REAL_INTERACTION",
        explicit_customer_request=True,
        problem_evidence_refs=[],
    )

    assert allowed is True
    assert artifact_kind == "CUSTOMER_PROPOSAL_DRAFT"
    assert basis == "EXPLICIT_CUSTOMER_REQUEST"


def test_demo_is_internal_hypothesis_not_customer_proposal() -> None:
    allowed, artifact_kind, basis = proposal_module.proposal_gate(
        mode="demo",
        qualification_state="RESEARCH_ONLY",
        explicit_customer_request=False,
        problem_evidence_refs=[],
    )

    assert allowed is True
    assert artifact_kind == "INTERNAL_HYPOTHESIS"
    assert basis == "RESEARCH_OR_DEMO_ONLY"


def test_only_canonical_or_legacy_mapped_offers_are_allowed() -> None:
    assert proposal_module.canonical_offer("Revenue OS") == "Revenue Command Pilot"
    assert proposal_module.canonical_offer("AI Company OS Setup") == "AI Company OS Setup"
    with pytest.raises(ValueError, match="not canonical"):
        proposal_module.canonical_offer("Random Offer")
